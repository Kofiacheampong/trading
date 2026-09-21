#!/usr/bin/env python3
"""
Paper-trading simulator for Kofi's budget watchlist.
- Dip-buy strategy: buys when price <= threshold, exits at +6% / -6% / 15 trading days.
- Weekly put sim: sells a ~10% OTM put every Monday (nearest Friday expiry),
  resolves Friday close vs strike, logs win/loss with real option credit when available.
- State in state.json; run with --step (daily) or --report (weekly summary).
"""
import json, os, subprocess, sys, datetime, math, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opportunity
import options_data as od
import mes_sim
import mes_intraday
import covered_calls
import fade_flags

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state.json")
START_CASH = 1500.0
NOTIONAL = 120.0          # ~$120 per dip-buy position
TP = 1.06                 # take profit
SL = 0.94                 # stop loss
MAX_HOLD_DAYS = 15
PUT_CREDIT_FALLBACK = 0.012  # 1.2% of strike if quote fetch fails

# Legacy absolute thresholds (Jul 2026 vintage). They were permanently breached
# by Sep 2026 (LULU 98 vs 112, KMB 97 vs 103, ZTS 71 vs 73, PYPL 52 vs 53), so the
# 'dip' signal was firing on every single session -> meaningless. Kept only as a
# reference/audit trail; the live trigger is now the relative DIP_MULT rule below.
THRESHOLDS = {"LULU": 112.0, "KMB": 103.0, "ZTS": 73.0, "PYPL": 53.0, "PAYC": 152.0}
UNIVERSE = list(THRESHOLDS)
# Dip rule (fixed 2026-09-21): buy when price <= 95% of the 20-day SMA.
# Self-normalising, so it can never get stuck permanently true.
DIP_MULT = 0.95
SMA_WINDOW = 20
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
CJ = "/tmp/sim_cookie.txt"

def default_state():
    return {"cash": START_CASH, "positions": {}, "closed": [], "puts": [],
            "events": [], "opportunities": []}

def load():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return default_state()

def save(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE)

def fetch_close(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1mo&interval=1d"
    out = subprocess.run(["curl","-s","-m","15","-H",f"User-Agent: {UA}",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["chart"]["result"][0]
        closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
        ts = res["timestamp"]
        return closes[-1], datetime.date.fromtimestamp(ts[-1])
    except Exception:
        return None, None

def fetch_sma(sym, window=SMA_WINDOW):
    """20-day SMA of daily closes, or None on failure."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=3mo&interval=1d"
    out = subprocess.run(["curl","-s","-m","15","-H",f"User-Agent: {UA}",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        closes = [c for c in d["chart"]["result"][0]["indicators"]["quote"][0]["close"]
                  if c is not None]
        if len(closes) < window:
            return None
        return sum(closes[-window:]) / window
    except Exception:
        return None

def get_crumb():
    subprocess.run(["curl","-s","-m","15","-c",CJ,"-H",f"User-Agent: {UA}","https://fc.yahoo.com","-o","/dev/null"], check=False)
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H",f"User-Agent: {UA}","https://query1.finance.yahoo.com/v1/test/getcrumb"], capture_output=True, text=True)
    return out.stdout.strip()

def nearest_expiry_ts(sym, crumb):
    """Next listed options expiry for sym (timestamp), from the chain."""
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{sym}?crumb={crumb}"
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H",f"User-Agent: {UA}",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        exps = d["optionChain"]["result"][0].get("expirationDates") or []
        today = datetime.date.today()
        for e in exps:
            if datetime.date.fromtimestamp(e) > today:
                return e
    except Exception:
        pass
    return None

def fetch_put_quote(sym, strike, expiry_ts, crumb):
    """Fetch real put mid-price for strike/expiry via Yahoo v7 options API."""
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{sym}?date={expiry_ts}&crumb={crumb}"
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H",f"User-Agent: {UA}",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        opts = d["optionChain"]["result"][0]["options"][0]["puts"]
        for p in opts:
            if abs(p["strike"] - strike) < 1e-6:
                bid, ask = p.get("bid", 0), p.get("ask", 0)
                if bid > 0 and ask > 0:
                    return (bid + ask) / 2
    except Exception:
        pass
    # Fallback: Cboe delayed quotes (official, free, no key) — match strike, nearest expiry.
    try:
        import re as _re
        cua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
        out = subprocess.run(["curl","-s","-m","20","-H",f"User-Agent: {cua}",
                              f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"],
                             capture_output=True, text=True)
        d = json.loads(out.stdout)
        want = datetime.date.fromtimestamp(expiry_ts)
        pat = _re.compile(r"^[A-Z]+\d{6}P(\d{8})$")
        best, best_gap, best_strike_gap = None, 10**9, 10**9
        for o in d["data"]["options"]:
            m = pat.match(o["option"])
            if not m:
                continue
            # nearest listed strike (strike intervals vary: $2.5 vs $5.0)
            strike_gap = abs(int(m.group(1)) / 1000.0 - strike)
            if strike_gap > 2.6:
                continue
            y = o["option"][len(sym):len(sym)+6]
            exp = datetime.date(2000+int(y[:2]), int(y[2:4]), int(y[4:6]))
            gap = abs((exp - want).days)
            if gap < best_gap or (gap == best_gap and strike_gap < best_strike_gap):
                best_gap = gap
                best_strike_gap = strike_gap
                best = (o.get("bid") or 0, o.get("ask") or 0)
        if best and best[0] > 0 and best[1] > 0:
            return (best[0] + best[1]) / 2
        return None
    except Exception:
        return None

def weekdays_between(d1, d2):
    n = 0
    d = d1
    while d < d2:
        if d.weekday() < 5:
            n += 1
        d += datetime.timedelta(days=1)
    return n

def next_friday(today):
    d = today
    while d.weekday() != 4:
        d += datetime.timedelta(days=1)
    return d

def fetch_call_mid(sym, strike, expiry, crumb):
    """Current mid of a specific call (strike/expiry date) via options_data."""
    ts = None
    for e in od.expirations(sym, crumb):
        if datetime.date.fromtimestamp(e) == expiry:
            ts = e
            break
    if ts is None:
        return None
    chain = od.fetch_best_chain(sym, ts, crumb)
    for c in chain:
        if c.get("strike") is not None and abs(c["strike"] - strike) < 1e-6:
            return c.get("mid") or None
    return None


def resolve_call_flags(state, crumb):
    """Paper-trade momentum-call alerts with the real exit plan:
    TP +100% / SL -50% / time stop 7 DTE (per-flag), expired = intrinsic value.
    Returns list of newly resolved flags."""
    flags = state.get("call_flags", [])
    resolved = []
    today = datetime.date.today()
    for f in flags:
        if f.get("outcome") is not None:
            continue
        sym, strike, premium = f["ticker"], f["strike"], f["premium"]
        expiry = datetime.date.fromisoformat(f["expiry"])
        time_stop = datetime.date.fromisoformat(f["time_stop"])

        # expired without an exit -> settle at intrinsic value
        if today > expiry:
            px = fetch_close(sym)[0]
            val = max((px or 0) - strike, 0)
            f["outcome"] = "expired"
            f["ret"] = round((val / premium - 1) * 100, 1) if premium else 0.0
            f["resolved_date"] = str(today)
            resolved.append(f)
            continue

        mid = fetch_call_mid(sym, strike, expiry, crumb)
        if mid is None:
            continue  # no chain data today; retry next step

        # time stop: exit at market regardless
        if today >= time_stop:
            f["outcome"] = "time"
            f["ret"] = round((mid / premium - 1) * 100, 1) if premium else 0.0
            f["resolved_date"] = str(today)
            resolved.append(f)
        elif mid >= premium * 2.0:
            f["outcome"] = "win"
            f["ret"] = round((mid / premium - 1) * 100, 1)
            f["resolved_date"] = str(today)
            resolved.append(f)
        elif mid <= premium * 0.5:
            f["outcome"] = "loss"
            f["ret"] = round((mid / premium - 1) * 100, 1)
            f["resolved_date"] = str(today)
            resolved.append(f)
    return resolved


def fetch_put_mid(sym, strike, expiry_ts, crumb):
    """Mid of one put (strike/expiry) via Yahoo v7 — the puts array, NOT calls.
    (options_data.fetch_chain returns calls only; putting calls here = garbage.)"""
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{sym}?date={expiry_ts}&crumb={crumb}"
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H",f"User-Agent: {UA}",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        for p in d["optionChain"]["result"][0]["options"][0]["puts"]:
            if abs(p["strike"] - strike) < 1e-6:
                bid, ask = p.get("bid", 0), p.get("ask", 0)
                if bid > 0 and ask > 0:
                    return (bid + ask) / 2
    except Exception:
        pass
    return None


def fetch_put_spread_mid(sym, k_buy, k_sell, expiry_ts, crumb):
    """Current mid of a bear put debit spread (buy k_buy put / sell k_sell put)."""
    mb = fetch_put_mid(sym, k_buy, expiry_ts, crumb)
    ms = fetch_put_mid(sym, k_sell, expiry_ts, crumb)
    if mb is not None and ms is not None:
        return mb - ms
    return None


def resolve_put_flags(state, crumb):
    """Paper-trade fade-the-rip put debit spreads with the standard exit rules:
    TP +100% / SL -50% / time stop 7 days before expiry / expired = intrinsic.
    Returns newly resolved flags."""
    flags = state.get("put_flags", [])
    resolved = []
    today = datetime.date.today()
    for f in flags:
        if f.get("outcome") is not None:
            continue
        sym, k_buy, k_sell, debit = f["ticker"], f["k_buy"], f["k_sell"], f["debit"]
        expiry = datetime.date.fromisoformat(f["expiry"])
        time_stop = datetime.date.fromisoformat(f["time_stop"])

        if today > expiry:
            px = fetch_close(sym)[0] or 0
            val = max(k_buy - px, 0) - max(k_sell - px, 0)
            f["outcome"] = "expired"
            f["ret"] = round((val / debit - 1) * 100, 1) if debit else 0.0
            f["resolved_date"] = str(today)
            resolved.append(f)
            continue

        ts = None
        for e in od.expirations(sym, crumb):
            if datetime.date.fromtimestamp(e) == expiry:
                ts = e
                break
        if ts is None:
            continue
        mid = fetch_put_spread_mid(sym, k_buy, k_sell, ts, crumb)
        if mid is None:
            continue
        if today >= time_stop:
            f["outcome"] = "time"
            f["ret"] = round((mid / debit - 1) * 100, 1)
            f["resolved_date"] = str(today)
            resolved.append(f)
        elif mid >= debit * 2.0:
            f["outcome"] = "win"
            f["ret"] = round((mid / debit - 1) * 100, 1)
            f["resolved_date"] = str(today)
            resolved.append(f)
        elif mid <= debit * 0.5:
            f["outcome"] = "loss"
            f["ret"] = round((mid / debit - 1) * 100, 1)
            f["resolved_date"] = str(today)
            resolved.append(f)
    return resolved


def step():
    state = load()
    today = datetime.date.today()
    prices = {}
    smas = {}
    for sym in UNIVERSE:
        px, dt = fetch_close(sym)
        if px:
            prices[sym] = px
        s = fetch_sma(sym)
        if s:
            smas[sym] = s

    if not prices:
        print("NO_EVENTS (no price data)")
        return

    # --- exit checks ---
    for sym in list(state["positions"]):
        px = prices.get(sym)
        if not px:
            continue
        pos = state["positions"][sym]
        entry = pos["entry"]
        entry_date = datetime.date.fromisoformat(pos["entry_date"])
        held = weekdays_between(entry_date, today)
        reason = None
        if px >= entry * TP:
            reason = "take-profit"
        elif px <= entry * SL:
            reason = "stop-loss"
        elif held >= MAX_HOLD_DAYS:
            reason = "time"
        if reason:
            pnl = (px / entry - 1) * pos["notional"]
            state["cash"] += pos["notional"] + pnl
            rec = {"ticker": sym, "entry": round(entry,2), "exit": round(px,2),
                   "entry_date": pos["entry_date"], "exit_date": str(today),
                   "pnl_pct": round((px/entry-1)*100,2), "pnl_usd": round(pnl,2),
                   "hold_days": held, "reason": reason}
            state["closed"].append(rec)
            del state["positions"][sym]
            print(f"EVENT CLOSED {sym} {reason} exit ${px:.2f} pnl {rec['pnl_pct']:.1f}%")

    # --- buy checks ---
    for sym in UNIVERSE:
        if sym in state["positions"] or sym not in prices:
            continue
        px = prices[sym]
        sma = smas.get(sym)
        if sma is None:
            continue
        if px <= sma * DIP_MULT and state["cash"] >= NOTIONAL:
            shares = NOTIONAL / px
            state["positions"][sym] = {"shares": round(shares, 4), "entry": px,
                                       "entry_date": str(today), "notional": NOTIONAL,
                                       "sma20": round(sma, 2)}
            state["cash"] -= NOTIONAL
            print(f"EVENT BUY {sym} @ ${px:.2f} (dip: {px/sma-1:+.1%} vs 20d SMA "
                  f"{sma:.2f}; legacy thr {THRESHOLDS[sym]:.0f})")

    # --- opportunity scan: spot setups + resolve old flags ---
    resolved = opportunity.resolve_open_opportunities(state, prices)
    for o in resolved:
        print(f"EVENT OPPORTUNITY {o['ticker']} RESOLVED {o['outcome']} ret {o['ret']:+.1f}% "
              f"(flagged ${o['price']:.2f} on {o['date']})")

    flagged = opportunity.scan()
    for o in flagged[:3]:
        # skip if we already logged this ticker today
        if any(x["ticker"] == o["ticker"] and x["date"] == o["date"]
               for x in state["opportunities"]):
            continue
        state["opportunities"].append(o)
        print(f"EVENT OPPORTUNITY {o['ticker']} score {o['score']:.0f} px ${o['price']:.2f} "
              f"rsi {o['rsi']} volx{o['relvol']} vs200ma {o['vs_200ma']}% "
              f"[{', '.join(o['flags'])}]")

    # --- momentum call flags: paper trade alerts with the real exit rules ---
    crumb = get_crumb()
    resolved_flags = resolve_call_flags(state, crumb)
    for f in resolved_flags:
        print(f"EVENT CALLFLAG {f['ticker']} {f['outcome'].upper()} ret {f['ret']:+.1f}% "
              f"(flag ${f['premium']:.2f} on {f['date']})")

    # --- put fades (debit spreads): paper-trade fade-the-rip entries ---
    resolved_pfs = resolve_put_flags(state, crumb)
    for f in resolved_pfs:
        print(f"EVENT PUTFLAG {f['ticker']} {f['outcome'].upper()} ret {f['ret']:+.1f}% "
              f"(debit ${f['debit']:.2f} on {f['date']})")

    # --- fade-the-flag (short call spreads vs momentum flags) ---
    resolved_ff = fade_flags.step(state, crumb)
    for f in resolved_ff:
        print(f"EVENT FADEFLAG {f['ticker']} {f['outcome'].upper()} ret {f['ret']:+.1f}% "
              f"(credit ${f['credit']:.2f}, flag {f['flag_date']})")

    # --- weekly put sim: open when none open, resolve on expiry day ---
    for sym in UNIVERSE:
        px = prices.get(sym)
        if not px:
            continue
        open_puts = [p for p in state["puts"] if p["ticker"] == sym and p.get("outcome") is None]
        if open_puts:
            p = open_puts[0]
            if today >= datetime.date.fromisoformat(p["expiry"]):
                win = px >= p["strike"]
                p["outcome"] = "win" if win else "loss"
                p["expiry_close"] = round(px, 2)
                print(f"EVENT PUT {sym} {'WIN' if win else 'LOSS'} strike ${p['strike']:.0f} close ${px:.2f} credit ${p['credit']:.2f}")
        else:
            last = [p for p in state["puts"] if p["ticker"] == sym]
            if last and last[-1].get("outcome") is not None and datetime.date.fromisoformat(last[-1]["expiry"]) >= today:
                continue  # just resolved today; open fresh tomorrow
            exp_ts = nearest_expiry_ts(sym, crumb)
            if not exp_ts:
                continue
            exp = datetime.date.fromtimestamp(exp_ts)
            strike = round(px * 0.90 / 2.5) * 2.5
            credit = fetch_put_quote(sym, strike, exp_ts, crumb)
            if credit is None:
                credit = strike * PUT_CREDIT_FALLBACK
            state["puts"].append({"ticker": sym, "date": str(today), "strike": strike,
                                  "spot": round(px, 2), "expiry": str(exp),
                                  "credit": round(credit, 2), "outcome": None})
            print(f"EVENT PUT {sym} opened strike ${strike:.0f} exp {exp} credit ${credit:.2f}")

    # --- covered calls (buy-write, synthetic 100-sh lots) ---
    covered_calls.step(state, crumb)

    # --- MES futures paper sim (extended paper period) ---
    for ev in mes_sim.step(state):
        print(f"EVENT {ev}")

    # --- MES intraday OR-fade (replayed at 4:15 PM, flat by 3:50) ---
    for ev in mes_intraday.step(state):
        print(f"EVENT {ev}")

    save(state)
    print("DONE")

def report():
    state = load()
    closed = state["closed"]
    puts = state["puts"]
    resolved_puts = [p for p in puts if p.get("outcome")]
    pos = state["positions"]

    print("=== SIM REPORT ===")
    print(f"Cash: ${state['cash']:.2f} | Open positions: {len(pos)}")
    for sym, p in pos.items():
        print(f"  {sym}: {p['shares']:.2f} sh @ ${p['entry']:.2f}")
    if closed:
        wins = [c for c in closed if c["pnl_pct"] > 0]
        losses = [c for c in closed if c["pnl_pct"] <= 0]
        wr = len(wins)/len(closed)*100
        avg_win = statistics.mean([c["pnl_pct"] for c in wins]) if wins else 0
        avg_loss = statistics.mean([c["pnl_pct"] for c in losses]) if losses else 0
        tot = sum(c["pnl_usd"] for c in closed)
        print(f"\nDIP-BUY TRADES: {len(closed)} closed | win rate {wr:.0f}% | avg win +{avg_win:.1f}% | avg loss {avg_loss:.1f}% | net ${tot:.2f}")
        for c in closed[-8:]:
            print(f"  {c['exit_date']} {c['ticker']} {c['reason']} {c['pnl_pct']:+.1f}% (${c['pnl_usd']:+.1f})")
    else:
        print("\nDIP-BUY TRADES: none closed yet")
    if resolved_puts:
        pwins = [p for p in resolved_puts if p["outcome"] == "win"]
        wr = len(pwins)/len(resolved_puts)*100
        credits = sum(p["credit"] for p in resolved_puts)
        print(f"\nWEEKLY PUT SIM: {len(resolved_puts)} resolved | win rate {wr:.0f}% | premium collected ${credits:.2f}")
        by_ticker = {}
        for p in resolved_puts:
            by_ticker.setdefault(p["ticker"], []).append(p)
        for t, ps in sorted(by_ticker.items()):
            w = sum(1 for p in ps if p["outcome"] == "win")
            print(f"  {t}: {w}/{len(ps)} wins")
        for p in resolved_puts[-10:]:
            print(f"  {p['expiry']} {p['ticker']} strike ${p['strike']:.0f} {p['outcome']} credit ${p['credit']:.2f}")
    else:
        print("\nWEEKLY PUT SIM: no resolved puts yet (first resolution next Friday)")
    open_puts = [p for p in puts if p.get("outcome") is None]
    if open_puts:
        print(f"\nOpen puts: {len(open_puts)}")

    # --- opportunity track record (the bot's intuition scorecard) ---
    opps = state.get("opportunities", [])
    resolved_opps = [o for o in opps if o.get("outcome")]
    if resolved_opps:
        bounces = [o for o in resolved_opps if o["outcome"] == "bounce"]
        wr = len(bounces) / len(resolved_opps) * 100
        avg_ret = sum(o.get("ret", 0) for o in resolved_opps) / len(resolved_opps)
        print(f"\nOPPORTUNITY SCANNER: {len(resolved_opps)} flags resolved | "
              f"bounce rate {wr:.0f}% | avg move {avg_ret:+.1f}%")
        by_t = {}
        for o in resolved_opps:
            by_t.setdefault(o["ticker"], []).append(o)
        for t, os_ in sorted(by_t.items()):
            w = sum(1 for o in os_ if o["outcome"] == "bounce")
            print(f"  {t}: {w}/{len(os_)} bounces")
    else:
        print("\nOPPORTUNITY SCANNER: no flags resolved yet (flags need 3+ days to judge)")
    open_opps = [o for o in opps if o.get("outcome") is None]
    if open_opps:
        print(f"Open opportunity flags: {len(open_opps)}")
        for o in open_opps[-5:]:
            print(f"  {o['date']} {o['ticker']} score {o['score']:.0f} @ ${o['price']:.2f}")

    # --- momentum call flags (paper-traded alerts) ---
    flags = state.get("call_flags", [])
    resolved_flags = [f for f in flags if f.get("outcome")]
    if resolved_flags:
        rets = [f.get("ret", 0) for f in resolved_flags]
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        wr = len(wins) / len(rets) * 100
        avg_ret = sum(rets) / len(rets)
        avg_win = sum(wins) / len(wins) if wins else 0.0
        avg_loss = sum(losses) / len(losses) if losses else 0.0
        print(f"\nCALL FLAGS (momentum): {len(resolved_flags)} resolved | win rate {wr:.0f}% | "
              f"avg ret {avg_ret:+.1f}% | avg win {avg_win:+.1f}% | avg loss {avg_loss:+.1f}%")
        by_t = {}
        for f in resolved_flags:
            by_t.setdefault(f["ticker"], []).append(f)
        for t, fs in sorted(by_t.items()):
            w = sum(1 for f in fs if f.get("ret", 0) > 0)
            print(f"  {t}: {w}/{len(fs)} wins")
        for f in resolved_flags[-10:]:
            print(f"  {f.get('resolved_date','?')} {f['ticker']} ${f['strike']:.2f}C {f['outcome']} ret {f.get('ret',0):+.1f}% (flag {f['date']})")
        if len(resolved_flags) >= 10:
            rr = abs(avg_win / avg_loss) if avg_loss < 0 else 0
            if wr >= 55.0 and rr >= 1.5:
                print("LEVER 3: CALL FLAGS GO-LIVE GATE PASSED — momentum calls have empirical backing "
                      "(≥10 flags, ≥55% WR, R:R ≥1.5). Trade $100-150 risk/trade in IBKR, 1-2/wk.")
            else:
                print(f"LEVER 3: {len(resolved_flags)} flags resolved — gate NOT passed yet "
                      f"(need ≥55% WR + avg win/avg loss ≥1.5; now {wr:.0f}% / {rr:.1f}). Keep paper trading.")
        else:
            print(f"LEVER 3: {len(resolved_flags)}/10 flags resolved — keep paper trading until gate clears.")
    else:
        print("\nCALL FLAGS (momentum): none resolved yet (alerts paper-trade via daily sim step)")
    open_flags = [f for f in flags if f.get("outcome") is None]
    if open_flags:
        print(f"Open call flags: {len(open_flags)}")
        for f in open_flags:
            print(f"  {f['date']} {f['ticker']} ${f['strike']:.2f}C exp {f['expiry']} "
                  f"premium ${f['premium']:.2f} conf {f.get('confidence')} time-stop {f['time_stop']}")
    # --- MES futures paper sim (extended paper period) ---
    print()
    print(mes_sim.report(state))

    # --- MES intraday OR-fade ---
    print()
    print(mes_intraday.report(state))

    # --- covered calls (buy-write, synthetic 100-sh lots) ---
    print(covered_calls.report(state))

    # --- fade-the-flag (short call spreads vs momentum flags) ---
    print(fade_flags.report(state))

    # --- put fades (debit spreads, paper-tracked) ---
    pfs = state.get("put_flags", [])
    rpfs = [f for f in pfs if f.get("outcome")]
    if rpfs:
        rets = [f.get("ret", 0) for f in rpfs]
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        wr = len(wins) / len(rets) * 100
        avg_ret = sum(rets) / len(rets)
        net = sum((f.get("ret", 0) / 100) * f["debit"] * 100 for f in rpfs)
        print(f"\nPUT FADES (debit spreads): {len(rpfs)} resolved | win rate {wr:.0f}% | "
              f"avg ret {avg_ret:+.1f}% | net ${net:+.2f}")
        for f in rpfs[-8:]:
            print(f"  {f.get('resolved_date','?')} {f['ticker']} {f['k_buy']:.0f}/{f['k_sell']:.0f}P "
                  f"{f['outcome']} ret {f.get('ret',0):+.1f}% (debit ${f['debit']:.2f}, {f['date']})")
        if len(rpfs) >= 10:
            avg_w = statistics.mean(wins) if wins else 0.0
            avg_l = statistics.mean(losses) if losses else 0.0
            rr = abs(avg_w / avg_l) if avg_l < 0 else 0.0
            if wr >= 55.0 and rr >= 1.5:
                print("  LEVER 3B: PUT-FADE GATE PASSED — fade-the-rip debit spreads have "
                      "empirical backing (≥10, ≥55% WR, R:R ≥1.5).")
            else:
                print(f"  LEVER 3B: {len(rpfs)} resolved — gate NOT passed (need ≥55% WR + "
                      f"R:R ≥1.5; now {wr:.0f}% / {rr:.1f}). Keep paper trading.")
        else:
            print(f"  LEVER 3B: {len(rpfs)}/10 put fades resolved — keep paper trading.")
    else:
        print("\nPUT FADES (debit spreads): none resolved yet")
    open_pfs = [f for f in pfs if f.get("outcome") is None]
    if open_pfs:
        print(f"Open put fades: {len(open_pfs)}")
        for f in open_pfs:
            print(f"  {f['date']} {f['ticker']} {f['k_buy']:.0f}/{f['k_sell']:.0f}P exp {f['expiry']} "
                  f"debit ${f['debit']:.2f} spot ${f['spot']:.2f} time-stop {f['time_stop']}")

    print("\nLEVER: put win rate above ~75% on a ticker => selling weeklies on it has empirical backing; below ~60% => skip or widen strike.")
    print("LEVER 2: if a ticker's opportunity flags bounce 70%+ of the time, its oversold flags are a green light to sell puts that week.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        report()
    else:
        step()

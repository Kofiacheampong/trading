#!/usr/bin/env python3
"""
Momentum-call scanner (Phase 2 of MOMENTUM_CALLS_SPEC.md).

Replicates the friend's alert system: find overbought momentum names (RSI >= 70,
Z-score vs 20-day >= +2.5σ, volume surge), confirm the market regime (SPY > 200d
SMA, VIX < 20), pick a 10-21 DTE call at/just ITM, score confidence 0-1, and
print trade cards with the standard exit plan (TP +100%, SL -50%, time stop 7 DTE).

Modes:
    python3 momentum_calls.py                     # live scan (default)
    python3 momentum_calls.py --backtest "2026-08-06 10:42"   # replay a moment using 5m bars
    python3 momentum_calls.py --verbose           # show sub-threshold scores too

Note on volume: the friend's feed reports "N× avg" as a burst rate. Ours is the
honest time-of-day-corrected version (today's volume so far / fraction of trading
day elapsed / 20-day avg) — a real surge at 10:40 AM still needs ~2× the pace.
Threshold is 1.5× corrected; the confidence score does the rest.

Extra gates (added 8/10/26):
  - ADX(14) >= 25 trend-strength gate (RSI/Z can fire in chop; ADX proves trend)
  - no entries into candidates that gapped up > GAP_SKIP % into the sweep (move already spent)
  - no 10-21 DTE call that straddles the next earnings print (the FSLY lesson)
"""
import json, os, sys, time, datetime
import options_data as od
import opportunity as opp   # reuses fetch_history + rsi + sma

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state.json")
_EARN_CACHE = {}          # per-run earnings-date cache (quoteSummary is slow)

# Curated universe: Kofi's watchlists + quality names + liquid high-beta
# momentum names where RSI-70+ call setups actually occur. Will evolve.
UNIVERSE = (
    # budget watchlist / quality
    "LULU", "KMB", "ZTS", "PYPL", "PAYC", "QCOM", "ADBE", "IT", "PNR",
    # DC power / semis
    "TXN", "ADI", "VRT", "ON", "INTC", "MP", "NVTS",
    # friend's momentum names (so the backtest + live scan cover them)
    "TOST", "PRGO", "FSLY",
    # liquid momentum / high-beta
    "NVDA", "AMD", "MU", "AVGO", "TSM", "PLTR", "CRWD", "SNOW", "NET",
    "SMCI", "ARM", "MRVL", "ANET", "OKLO", "SMR", "IONQ", "RGTI", "HOOD",
    "COIN", "MSTR", "TSLA", "NFLX", "META", "AMZN", "GOOGL", "MSFT", "LLY",
    "NOW", "CRM", "DECK", "SHOP", "UBER", "SOFI", "CVNA", "AFRM", "DKNG",
    # watchlist adds — NVO 9/22/26 (watch name; only fires if GLP-1 sentiment
    # actually turns: RSI>=70 + Z>=2.5 + ADX gate. Won't flag while washed out.)
    "NVO",
)

# --- filters ---
MIN_RSI = 70.0
MIN_Z = 2.5
MIN_RELVOL = 1.5          # time-of-day corrected
MIN_OI = 500
MAX_IV = 1.50
SPREAD_TRADE = 15.0       # % of mid: ok to trade
SPREAD_REJECT = 30.0      # % of mid: reject above this
TARGET_DTE, MIN_DTE, MAX_DTE = 15, 10, 21
MIN_SCORE = 0.60          # confidence trade threshold
MIN_ADX = 25.0            # Wilder ADX(14) trend-strength gate (noise filter)
GAP_SKIP = 3.0            # skip candidates that gapped up > this % into the sweep

# --- exit plan ---
TP_MULT = 2.0             # +100%
SL_MULT = 0.5             # -50%
TIME_STOP_DTE = 7         # calendar days before expiry

# --- misc ---
SPOT_WINDOW = 0.08        # strikes within ±8% of spot (catches one-strike-ITM on low-priced names)
PREF_DELTA = 0.55
SCAN_SLEEP = 0.15         # be polite to Yahoo


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def time_fraction(dt=None):
    """Fraction of the 9:30-16:00 ET session elapsed at dt (None = now)."""
    if dt is None:
        dt = datetime.datetime.now()
    open_t = dt.replace(hour=9, minute=30, second=0, microsecond=0)
    close_t = dt.replace(hour=16, minute=0, second=0, microsecond=0)
    if dt < open_t:
        return None
    if dt >= close_t:
        return 1.0
    return (dt - open_t).total_seconds() / (close_t - open_t).total_seconds()


def relvol_corrected(vol_today, avg20, frac):
    """Volume pace vs 20-day average, corrected for time of day."""
    if not vol_today or not avg20 or not frac:
        return None
    return (vol_today / frac) / avg20


def fetch_5m(sym, start_dt, end_dt):
    """5-minute bars between naive-local datetimes; (ts, closes, vols)."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           f"?period1={int(start_dt.timestamp())}&period2={int(end_dt.timestamp())}&interval=5m")
    ok, out = od._curl(url)
    if not ok:
        return None, None, None
    try:
        d = json.loads(out)
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        ts = res.get("timestamp") or []
        closes, vols = q["close"], q["volume"]
        return ts, closes, vols
    except Exception:
        return None, None, None


def fetch_5m_ohlc(sym, start_dt, end_dt):
    """5-minute OHLCV bars between naive-local datetimes (for backtests)."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           f"?period1={int(start_dt.timestamp())}&period2={int(end_dt.timestamp())}&interval=5m")
    ok, out = od._curl(url)
    if not ok:
        return None, None, None, None, None, None
    try:
        d = json.loads(out)
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        ts = res.get("timestamp") or []
        return ts, q["close"], q["open"], q["high"], q["low"], q["volume"]
    except Exception:
        return None, None, None, None, None, None


def build_series(sym, target_dt=None):
    """Return (closes, vols, px, vol_today, frac, opens, highs, lows).

    Live: 1y daily bars (last bar = today's live print, incl. developing OHLC).
    Backtest: daily bars strictly before target day, plus a 5m-bar snapshot
    reconstructed up to target_dt as the final bar (O/H/L approximated).
    """
    ts, closes, opens, highs, lows, vols = od.fetch_ohlc(sym, "1y")
    if not closes or len(closes) < 60:
        return None, None, None, None, None, None, None, None

    if target_dt is None:
        px = closes[-1]
        vol_today = vols[-1] if vols else 0
        frac = time_fraction()
        return closes, vols, px, vol_today, frac, opens, highs, lows

    # backtest: drop bars on/after the target day
    cut = len(ts)
    for i, t in enumerate(ts):
        if datetime.date.fromtimestamp(t) >= target_dt.date():
            cut = i
            break
    closes_d, vols_d = closes[:cut], vols[:cut]
    opens_d, highs_d, lows_d = opens[:cut], highs[:cut], lows[:cut]

    # reconstruct the target day up to target_dt via 5m bars
    start = target_dt.replace(hour=9, minute=0, second=0, microsecond=0)
    end = target_dt + datetime.timedelta(minutes=5)
    t5, c5, o5, h5, l5, v5 = fetch_5m_ohlc(sym, start, end)
    if not c5:
        return None, None, None, None, None, None, None, None
    px = day_open = vol_today = None
    hi = lo = None
    for t, c, o, h, l, v in zip(t5, c5, o5, h5, l5, v5):
        dt = datetime.datetime.fromtimestamp(t)
        if dt > target_dt:
            break
        if c is not None:
            px = c
        if day_open is None and o is not None:
            day_open = o
        if v is not None:
            vol_today = (vol_today or 0) + v
        if h is not None and (hi is None or h > hi):
            hi = h
        if l is not None and (lo is None or l < lo):
            lo = l
    if px is None:
        return None, None, None, None, None, None, None, None
    closes = closes_d + [px]
    vols = vols_d + [vol_today or 0]
    opens = opens_d + [day_open or px]
    highs = highs_d + [hi or px]
    lows = lows_d + [lo or px]
    frac = time_fraction(target_dt)
    return closes, vols, px, vol_today or 0, frac, opens, highs, lows


def adx(closes, highs, lows, period=14):
    """Wilder ADX(14). None if insufficient data. 0-100; >= 25 = trending."""
    n = len(closes)
    if n < period * 2 + 1:
        return None
    trs, pdms, mdms = [], [], []
    for i in range(1, n):
        hi, lo, pc = highs[i], lows[i], closes[i - 1]
        trs.append(max(hi - lo, abs(hi - pc), abs(lo - pc)))
        up, dn = hi - highs[i - 1], lows[i - 1] - lo
        pdms.append(up if (up > dn and up > 0) else 0.0)
        mdms.append(dn if (dn > up and dn > 0) else 0.0)
    atr = sum(trs[:period]) / period
    pdi = sum(pdms[:period]) / period
    mdi = sum(mdms[:period]) / period
    dxs = []
    for i in range(period, len(trs)):
        atr = (atr * (period - 1) + trs[i]) / period
        pdi = (pdi * (period - 1) + pdms[i]) / period
        mdi = (mdi * (period - 1) + mdms[i]) / period
        if atr > 0 and (pdi + mdi) > 0:
            dxs.append(100.0 * abs(pdi - mdi) / (pdi + mdi))
        else:
            dxs.append(0.0)
    if len(dxs) < period:
        return None
    a = sum(dxs[:period]) / period
    for i in range(period, len(dxs)):
        a = (a * (period - 1) + dxs[i]) / period
    return a


def score_confidence(r, z, rv, spread, vix, trend_ok):
    """Confidence 0-1 per MOMENTUM_CALLS_SPEC.md scoring table."""
    c = 0.0
    if r is not None:
        c += 0.20 if r >= 75 else (0.10 if r >= 70 else 0.0)
    if z is not None:
        c += 0.20 if z >= 3.0 else (0.10 if z >= MIN_Z else 0.0)
    if rv is not None:
        c += 0.20 if rv >= 2.5 else (0.10 if rv >= MIN_RELVOL else 0.0)
    if spread is not None:
        c += 0.20 if spread < 10.0 else (0.10 if spread <= SPREAD_TRADE else 0.0)
    if vix is not None:
        c += 0.10 if vix < 18.0 else (0.05 if vix < 20.0 else 0.0)
    if trend_ok:
        c += 0.10
    return round(c, 2)


def pick_contract(chain, spot):
    """Best call within ±5% of spot passing liquidity gates.

    Prefers delta near 0.55 (ATM / one strike ITM). Returns dict or None.
    """
    best = None
    for c in chain:
        strike = c.get("strike")
        if strike is None or c["bid"] <= 0 or c["ask"] <= 0:
            continue
        if abs(strike - spot) > spot * SPOT_WINDOW:
            continue
        if c["oi"] < MIN_OI:
            continue
        if c["iv"] is None or c["iv"] >= MAX_IV:
            continue
        spr = od.spread_pct(c["bid"], c["ask"])
        if spr is None or spr > SPREAD_REJECT:
            continue
        delta = c.get("delta")
        # prefer delta near 0.55 (ATM); Cboe fallback has no delta -> use distance to spot
        d_score = abs((delta or 0.0) - PREF_DELTA) if delta is not None \
            else abs(strike - spot) / spot
        rec = {"strike": strike, "bid": c["bid"], "ask": c["ask"],
               "mid": c["mid"], "iv": c["iv"], "oi": c["oi"],
               "volume": c["volume"], "delta": delta, "spread": round(spr, 1),
               "d_score": d_score}
        if best is None or d_score < best["d_score"]:
            best = rec
    return best


def conf_label(conf):
    return "HIGH" if conf >= 0.75 else "TRADE" if conf >= MIN_SCORE else "MARGINAL"


# --------------------------------------------------------------------------
# Alert mode: dedupe + Thursday cutoff (Phase 3)
# --------------------------------------------------------------------------
def load_state():
    """Full sim state.json (shared with sim.py)."""
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {}


def save_state(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE)


def alert():
    """--alert: scan, dedupe against today's already-logged flags, print new cards.

    Guards: weekends skip; no new entries after 11 AM Thursday (no weekend holds).
    Logs each alert into state.json call_flags for the Phase 4 paper trade.
    """
    now = datetime.datetime.now()
    today = now.date()
    if today.weekday() >= 5:
        print("NO_ALERTS (weekend)")
        return
    if today.weekday() == 3 and now.time() > datetime.time(11, 0):
        print("NO_ALERTS (Thursday cutoff 11 AM — no weekend holds)")
        return

    cands = scan()
    if not cands:
        print("NO_ALERTS")
        return

    state = load_state()
    flags = state.get("call_flags", [])
    today_s = str(today)
    new = []
    for o in cands:
        if any(f.get("ticker") == o["ticker"] and f.get("strike") == o["strike"]
               and f.get("expiry") == o["expiry"] and f.get("date") == today_s
               for f in flags):
            continue
        new.append(o)
    if not new:
        print("NO_ALERTS (already alerted)")
        return

    for o in new:
        flags.append({
            "ticker": o["ticker"], "date": today_s, "spot": o["spot"],
            "strike": o["strike"], "expiry": o["expiry"], "dte": o["dte"],
            "premium": o["mid"], "cost": o["cost"], "be": o["be"],
            "be_pct": o["be_pct"], "confidence": o["confidence"],
            "adx": o.get("adx"), "gap": o.get("gap"),
            "earnings": o.get("earnings"),
            "time_stop": o["time_stop"], "outcome": None,
        })
    state["call_flags"] = flags
    save_state(state)
    print_cards(new)


# --------------------------------------------------------------------------
# Scan
# --------------------------------------------------------------------------
def get_next_earnings(sym, crumb):
    """Next earnings date for sym (cached per run)."""
    if sym in _EARN_CACHE:
        return _EARN_CACHE[sym]
    e = od.next_earnings(sym, crumb)
    _EARN_CACHE[sym] = e
    return e


def scan(target_dt=None, verbose=False):
    spy_ok, vix, spy_px, spy_sma = od.fetch_regime()
    if not spy_ok:
        print(f"REGIME BLOCKED (SPY {spy_px:.0f} < SMA200 {spy_sma:.0f})")
        return []
    if vix is not None and vix >= 20:
        print(f"REGIME BLOCKED (VIX {vix:.1f} >= 20)")
        return []
    print(f"REGIME OK (SPY {spy_px:.0f} vs 200MA {spy_sma:.0f}, VIX {vix:.1f})")

    crumb = od.get_crumb()
    if not crumb:
        print("NO_CRUMB")
        return []

    out = []
    entry_day = target_dt.date() if target_dt else datetime.date.today()
    for sym in UNIVERSE:
        closes, vols, px, vol_today, frac, opens, highs, lows = build_series(sym, target_dt)
        if not closes:
            continue
        if frac is None:          # pre-market: no intraday volume signal yet
            continue

        r = opp.rsi(closes)
        z = od.zscore(closes, 20)
        avg20 = sum(vols[-21:-1]) / 20 if len(vols) >= 21 else 0
        rv = relvol_corrected(vol_today, avg20, frac)
        sma50 = opp.sma(closes, 50)
        sma200 = opp.sma(closes, 200)
        trend_ok = sma50 and sma200 and px > sma50 > sma200

        # entry gates (cheap first)
        if r is None or r < MIN_RSI:
            continue
        if z is None or z < MIN_Z:
            continue
        if rv is None or rv < MIN_RELVOL:
            continue
        if not trend_ok:
            continue

        # ADX trend-strength gate: RSI/Z can fire in chop; require a real trend
        a = adx(closes, highs, lows)
        if a is None or a < MIN_ADX:
            if verbose:
                print(f"  skip {sym}: ADX {a if a is not None else 'n/a'} < {MIN_ADX}")
            continue

        # Overnight-gap check: move already spent if it gapped up into the sweep
        gap = (opens[-1] / closes[-2] - 1) * 100 if len(closes) >= 2 and closes[-2] else 0.0
        if gap > GAP_SKIP:
            if verbose:
                print(f"  skip {sym}: gapped {gap:+.1f}% into sweep")
            continue

        # options leg
        exp_ts, dte = od.pick_expiry(sym, crumb, TARGET_DTE, MIN_DTE, MAX_DTE)
        if not exp_ts:
            continue
        exp_date = datetime.date.fromtimestamp(exp_ts)

        # earnings-straddle gate (the FSLY lesson): no call whose life covers a print
        earn = get_next_earnings(sym, crumb)
        if earn is not None and entry_day <= earn <= exp_date:
            if verbose:
                print(f"  skip {sym}: earnings {earn} inside option life (exp {exp_date})")
            continue

        chain = od.fetch_best_chain(sym, exp_ts, crumb)
        c = pick_contract(chain, px)
        if not c:
            continue

        conf = score_confidence(r, z, rv, c["spread"], vix, trend_ok)
        if conf < MIN_SCORE and not verbose:
            continue

        be = c["strike"] + c["mid"]
        time_stop = exp_date - datetime.timedelta(days=TIME_STOP_DTE)
        out.append({
            "ticker": sym, "spot": round(px, 2), "strike": c["strike"],
            "expiry": str(exp_date), "dte": dte, "mid": c["mid"],
            "cost": round(c["mid"] * 100, 2), "be": round(be, 2),
            "be_pct": round((be / px - 1) * 100, 2), "rsi": round(r, 1),
            "z": round(z, 1), "relvol": round(rv, 2), "spread": c["spread"],
            "iv": round(c["iv"] * 100, 0), "delta": c["delta"], "oi": c["oi"],
            "adx": round(a, 1), "gap": round(gap, 2),
            "earnings": str(earn) if earn else None,
            "confidence": conf, "time_stop": str(time_stop),
            "tp": round(c["mid"] * TP_MULT * 100, 2),
            "sl": round(c["mid"] * SL_MULT * 100, 2),
            "backtest": target_dt.strftime("%Y-%m-%d %H:%M") if target_dt else None,
        })
        time.sleep(SCAN_SLEEP)

    out.sort(key=lambda o: o["confidence"], reverse=True)
    return out


def print_cards(cands):
    if not cands:
        print("NO_ALERTS")
        return
    for o in cands:
        tag = f" [BACKTEST @ {o['backtest']}]" if o.get("backtest") else ""
        wide = " ⚠️ WIDE SPREAD — use limit near mid" if o["spread"] > SPREAD_TRADE else ""
        print(f"{o['ticker']} CALL @ ${o['spot']:.2f}{tag}")
        print(f"  Spot ${o['spot']:.2f} -> Buy Strike ${o['strike']:.2f} | Exp {o['expiry']} ({o['dte']} DTE)")
        print(f"  Mid ${o['mid']:.2f} = ${o['cost']:.0f}/ct | Break-even ${o['be']:.2f} ({o['be_pct']:+.1f}%)")
        d = f"{o['delta']:.2f}" if o['delta'] is not None else "n/a"
        print(f"  RSI {o['rsi']:.0f} | Z {o['z']:+.1f}σ | vol {o['relvol']:.1f}× | spread {o['spread']:.0f}% | "
              f"IV {o['iv']:.0f}% | delta {d} | OI {o['oi']}")
        earn = f" | next earnings {o['earnings']}" if o.get("earnings") else ""
        print(f"  ADX {o['adx']:.0f} | gap {o['gap']:+.1f}%{earn}")
        print(f"  Confidence {o['confidence']:.2f} — {conf_label(o['confidence'])}{wide}")
        print(f"  EXIT: TP +100% (${o['tp']:.0f}) | SL -50% (${o['sl']:.0f}) | time stop {o['time_stop']} ({TIME_STOP_DTE} DTE)")
        print()


def main():
    if "--alert" in sys.argv:
        alert()
        return
    verbose = "--verbose" in sys.argv
    target_dt = None
    if "--backtest" in sys.argv:
        i = sys.argv.index("--backtest")
        target_dt = datetime.datetime.strptime(sys.argv[i + 1], "%Y-%m-%d %H:%M")
    t0 = time.time()
    cands = scan(target_dt=target_dt, verbose=verbose)
    print_cards(cands)
    print(f"SCANNED {len(UNIVERSE)} names in {time.time() - t0:.0f}s | {len(cands)} candidate(s)")


if __name__ == "__main__":
    main()

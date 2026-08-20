#!/usr/bin/env python3
"""
Opportunity scanner for the trading sim.
Looks for market setups on the watchlist (plus a few quality extras) using
price/volume/RSI/200-day-MA math — no news needed:

  - oversold_quality : deep discount vs 200-day MA + oversold RSI  (fear priced in)
  - deep_value_52w   : sitting within ~8% of its 52-week low       (capitulation zone)
  - early_reversal   : RSI just crossed back above 30              (bounce ignition)
  - accumulation     : volume surge on a green day after a slide   (smart money?)
  - momentum_breakout: new 20-day high on heavy volume             (trend starting)

Each setup gets a score (0-100). Score >= MIN_SCORE = a flag worth logging.
Tracked over time so the weekly report can show the bot's "intuition" hit rate:
did flagged names actually bounce, and which tickers' flags reliably precede
moves (that's the data lever for selling weeklies on them).
"""
import json, os, subprocess, datetime, math

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Core watchlist + quality extras with decent liquidity (from earlier screens).
# AI-power tier (CEG/VST/GEV/CCJ/BWXT) + story tier (OKLO/SMR/FCEL) + solar corner (TE)
# added 8/16/26 per AI-power watchlist (projects/ai-power-watchlist.md).
UNIVERSE = ["LULU", "KMB", "ZTS", "PYPL", "PAYC", "QCOM", "ADBE", "IT", "PNR",
            "AVAV", "KTOS", "RCAT", "ONDS",
            "CEG", "VST", "GEV", "CCJ", "BWXT", "OKLO", "SMR", "FCEL", "TE"]

# Quality score = ROIC % (from our fundamental screens). Used to weight setups:
# a cheap price on a 27% ROIC business is an opportunity; on a 9% one it's a value trap.
# Drone + AI-power names have no verified ROIC on file -> default 15 weight.
QUALITY = {"LULU": 27.7, "KMB": 23.7, "ZTS": 27.8, "PYPL": 22.3, "PAYC": 30.0,
           "QCOM": 25.0, "ADBE": 30.0, "IT": 30.0, "PNR": 14.0,
           "AVAV": 15.0, "KTOS": 15.0, "RCAT": 15.0, "ONDS": 15.0,
           "CEG": 15.0, "VST": 15.0, "GEV": 15.0, "CCJ": 15.0, "BWXT": 15.0,
           "OKLO": 15.0, "SMR": 15.0, "FCEL": 15.0, "TE": 15.0}

MIN_SCORE = 40.0
BOUNCE_TARGET = 0.05     # +5% from flag price => "bounce" (good flag)
DUD_THRESHOLD = -0.08    # -8% from flag price   => "dud" (bad flag)

# ---------------------------------------------------------------------------
# VALUE SCREEN (--value) — quality-on-discount, added 8/20/26 per Kofi's 5-gate
# framework: Gate1 quality (ROIC/ROE/FCF/debt), Gate2 discount (FCF yield /
# EV-EBITDA / earnings yield), Gate4 price (below 200-day MA + washed-out RSI).
# Gate3 ("why is it cheap?") stays a human call — the report prints the flags so
# the fear category is visible. Fundamentals come from Yahoo quoteSummary
# (crumb-authed). Cached 7 days in state.json under value_cache.
# ---------------------------------------------------------------------------

# Wider universe for value mode: existing UNIVERSE + Market-Map quality names.
VALUE_UNIVERSE = UNIVERSE + ["ACN", "INTU", "DECK", "FDS", "MCD", "PEP"]

TAX_RATE = 0.21          # flat corporate-tax proxy for NOPAT estimate
VALUE_CACHE_DAYS = 7     # refresh fundamentals weekly

_CRUMB = {"cookie": None, "crumb": None}


def fetch_fundamentals(sym):
    """Return dict of fundamentals from Yahoo quoteSummary (or None).
    Uses the crumb dance: fc.yahoo.com cookie -> getcrumb -> v10 quoteSummary.
    Modules: defaultKeyStatistics (stats) + financialData (fin)."""
    if not _CRUMB["crumb"]:
        try:
            cookie = subprocess.run(
                ["curl", "-s", "-m", "15", "-c", "-", "-H", f"User-Agent: {UA}",
                 "https://fc.yahoo.com"],
                capture_output=True, text=True).stdout
            m = [l for l in cookie.splitlines() if "\tA3\t" in l]
            if not m:
                return None
            _CRUMB["cookie"] = m[0].split("\t")[-1]
            crumb = subprocess.run(
                ["curl", "-s", "-m", "15", "-b", f"A3={_CRUMB['cookie']}",
                 "-H", f"User-Agent: {UA}",
                 "https://query1.finance.yahoo.com/v1/test/getcrumb"],
                capture_output=True, text=True).stdout.strip()
            if not crumb:
                return None
            _CRUMB["crumb"] = crumb
        except Exception:
            return None
    url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{sym}"
           f"?modules=defaultKeyStatistics,financialData&crumb={_CRUMB['crumb']}")
    out = subprocess.run(["curl", "-s", "-m", "20", "-b",
                          f"A3={_CRUMB['cookie']}", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["quoteSummary"]["result"][0]
        st = (res.get("defaultKeyStatistics") or {})
        fn = (res.get("financialData") or {})
        raw = lambda mod, k: (mod.get(k) or {}).get("raw")
        px = raw(fn, "currentPrice") or raw(st, "currentPrice")
        shares = raw(st, "sharesOutstanding")
        teps = raw(st, "trailingEps")
        market_cap = (px * shares) if px and shares else None
        trailing_pe = (px / teps) if px and teps else None
        return {
            "market_cap": market_cap,
            "enterprise_value": raw(st, "enterpriseValue"),
            "trailing_pe": trailing_pe,
            "forward_pe": raw(st, "forwardPE"),
            "ev_to_ebitda": raw(st, "enterpriseToEbitda"),
            "ev_to_revenue": raw(st, "enterpriseToRevenue"),
            "fcf": raw(fn, "freeCashflow") or raw(st, "freeCashflow"),
            "ocf": raw(fn, "operatingCashflow") or raw(st, "operatingCashflow"),
            "roe": raw(fn, "returnOnEquity") or raw(st, "returnOnEquity"),
            "roa": raw(fn, "returnOnAssets") or raw(st, "returnOnAssets"),
            "gross_margin": raw(fn, "grossMargins") or raw(st, "grossMargins"),
            "oper_margin": raw(fn, "operatingMargins") or raw(st, "operatingMargins"),
            "net_margin": raw(fn, "profitMargins") or raw(st, "profitMargins"),
            "revenue_growth": raw(fn, "revenueGrowth") or raw(st, "revenueGrowth"),
            "earnings_growth": raw(fn, "earningsGrowth") or raw(st, "earningsGrowth"),
            "total_debt": raw(fn, "totalDebt") or raw(st, "totalDebt"),
            "total_cash": raw(fn, "totalCash") or raw(st, "totalCash"),
            "debt_to_equity": raw(fn, "debtToEquity") or raw(st, "debtToEquity"),
            "book_value": raw(st, "bookValue"),
            "shares_out": shares,
            "current_ratio": raw(fn, "currentRatio") or raw(st, "currentRatio"),
            "target_price": raw(fn, "targetMeanPrice"),
            "recommendation": raw(fn, "recommendationMean"),
        }
    except Exception:
        return None


def est_roic(f):
    """ROIC proxy = NOPAT / (total debt + equity - cash).
    NOPAT = revenue x net margin x (1 - tax). Equity = book value x shares.
    Returns % or None. Clearly an estimate — good enough to separate 15%+
    compounders from 9% value traps."""
    try:
        rev = None  # revenue not in the two modules; derive from EV/EV-to-rev
        if f.get("ev_to_revenue") and f.get("enterprise_value"):
            rev = f["enterprise_value"] / f["ev_to_revenue"]
        if not rev or not f.get("net_margin") or not f.get("book_value") or not f.get("shares_out"):
            return None
        nopat = rev * f["net_margin"] * (1 - TAX_RATE)
        equity = f["book_value"] * f["shares_out"]
        invested = (f.get("total_debt") or 0) + equity - (f.get("total_cash") or 0)
        if invested <= 0:
            return None
        return nopat / invested * 100
    except Exception:
        return None


def value_scan():
    """Quality-on-discount scan: rank tickers by Gate1 (quality) + Gate2
    (discount) + Gate4 (price). Returns list of value dicts."""
    state = load()
    cache = state.setdefault("value_cache", {})
    today = str(datetime.date.today())
    stale = datetime.date.today() - datetime.timedelta(days=VALUE_CACHE_DAYS)
    found = []
    for sym in VALUE_UNIVERSE:
        ent = cache.get(sym) or {}
        ent_date = ent.get("date") or ""
        if not ent or not ent_date or datetime.date.fromisoformat(ent_date) < stale:
            ent = fetch_fundamentals(sym) or {}
            ent["date"] = today
            cache[sym] = ent
        ts, closes, vols = fetch_history(sym)
        if not closes or len(closes) < 60:
            continue
        px = closes[-1]
        sma200 = sma(closes, 200)
        r = rsi(closes)
        fcf_yield = (ent.get("fcf") / ent.get("market_cap") * 100) if ent.get("fcf") and ent.get("market_cap") else None
        ey = (1 / ent["trailing_pe"] * 100) if ent.get("trailing_pe") else None
        roic = est_roic(ent)

        score = 0.0
        gates = []
        # Gate 1: quality
        if roic is not None:
            if roic >= 15: score += 20; gates.append(f"ROIC~{roic:.0f}%")
            elif roic >= 10: score += 10; gates.append(f"ROIC~{roic:.0f}%")
        if ent.get("roe"):
            roe = ent["roe"] * 100
            if roe >= 15: score += 10; gates.append(f"ROE {roe:.0f}%")
            elif roe >= 10: score += 5
        if ent.get("fcf") and ent["fcf"] > 0:
            score += 5; gates.append("FCF+")
        if ent.get("total_cash") and ent.get("total_debt"):
            if ent["total_cash"] >= ent["total_debt"]:
                score += 5; gates.append("net-cash")
        elif ent.get("debt_to_equity") is not None and ent["debt_to_equity"] < 0.8:
            score += 3
        # Gate 2: discount
        if fcf_yield is not None:
            if fcf_yield >= 6: score += 20; gates.append(f"FCFy {fcf_yield:.1f}%")
            elif fcf_yield >= 4: score += 12; gates.append(f"FCFy {fcf_yield:.1f}%")
            elif fcf_yield >= 2: score += 6
        if ent.get("ev_to_ebitda"):
            if ent["ev_to_ebitda"] < 10: score += 10; gates.append(f"EV/EBITDA {ent['ev_to_ebitda']:.1f}")
            elif ent["ev_to_ebitda"] < 15: score += 5
        if ey is not None:
            if ey >= 6: score += 10; gates.append(f"EY {ey:.1f}%")
            elif ey >= 4: score += 5
        # Gate 4: price (fear priced in?)
        if sma200 and px < sma200:
            below = (px / sma200 - 1) * 100
            if below <= -10: score += 8; gates.append(f"-{abs(below):.0f}% vs 200ma")
            else: score += 4
        if r is not None and r < 40:
            score += 5; gates.append(f"RSI {r:.0f}")

        found.append({
            "ticker": sym, "date": today, "price": round(px, 2),
            "score": round(score, 1),
            "roic_est": round(roic, 1) if roic is not None else None,
            "roe": round(ent["roe"] * 100, 1) if ent.get("roe") else None,
            "fcf_yield": round(fcf_yield, 1) if fcf_yield is not None else None,
            "ev_ebitda": round(ent["ev_to_ebitda"], 1) if ent.get("ev_to_ebitda") else None,
            "earn_yield": round(ey, 1) if ey is not None else None,
            "net_cash": ent.get("total_cash") is not None and ent.get("total_debt") is not None
                         and ent["total_cash"] >= ent["total_debt"],
            "rev_growth": round(ent["revenue_growth"] * 100, 1) if ent.get("revenue_growth") else None,
            "vs_200ma": round((px / sma200 - 1) * 100, 1) if sma200 else None,
            "rsi": round(r, 1) if r is not None else None,
            "gates": gates,
            "flag": score >= 55,
        })
    found.sort(key=lambda v: v["score"], reverse=True)
    save(state)  # persist fundamentals cache (refreshed weekly)
    return found


def fetch_history(sym, rng="1y"):
    """Return (dates, closes, volumes) lists from Yahoo chart API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d"
    out = subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        closes, vols, ts = [], [], res.get("timestamp") or []
        for c, v in zip(q["close"], q["volume"]):
            if c is not None:
                closes.append(c)
                vols.append(v or 0)
        return ts, closes, vols
    except Exception:
        return None, None, None


def rsi(closes, period=14):
    """Wilder's RSI on the close series; returns last value (None if too short)."""
    if len(closes) < period + 1:
        return None
    gains = losses = 0.0
    for i in range(1, period + 1):
        ch = closes[i] - closes[i - 1]
        if ch >= 0:
            gains += ch
        else:
            losses -= ch
    avg_g, avg_l = gains / period, losses / period
    for i in range(period + 1, len(closes)):
        ch = closes[i] - closes[i - 1]
        g = max(ch, 0.0)
        l = max(-ch, 0.0)
        avg_g = (avg_g * (period - 1) + g) / period
        avg_l = (avg_l * (period - 1) + l) / period
    if avg_l == 0:
        return 100.0
    return 100.0 - 100.0 / (1.0 + avg_g / avg_l)


def sma(closes, period):
    if len(closes) < period:
        return None
    return sum(closes[-period:]) / period


def scan():
    """Return ranked list of opportunity dicts."""
    found = []
    for sym in UNIVERSE:
        ts, closes, vols = fetch_history(sym)
        if not closes or len(closes) < 60:
            continue
        px = closes[-1]
        prev = closes[-2] if len(closes) > 1 else px
        sma200 = sma(closes, 200)
        sma50 = sma(closes, 50)
        hi52 = max(closes[-252:]) if len(closes) >= 252 else max(closes)
        lo52 = min(closes[-252:]) if len(closes) >= 252 else min(closes)
        r = rsi(closes)
        r_prev = rsi(closes[:-1]) if len(closes) > 15 else None
        vol20 = vols[-20:] and (sum(vols[-20:]) / 20) or 0
        relvol = vols[-1] / vol20 if vol20 > 0 else 0.0
        hi20 = max(closes[-21:-1]) if len(closes) > 21 else px

        flags = []
        score = 0.0

        # Deep discount vs 200-day MA (fear priced in)
        if sma200:
            below = (px / sma200 - 1) * 100
            if below <= -10:
                score += 20
            if below <= -20:
                score += 10
            if below <= -30:
                score += 10
            if below <= -10:
                flags.append(f"oversold_quality({below:.0f}% vs 200ma)")
        # Oversold RSI
        if r is not None:
            if r < 30:
                score += 25
                flags.append(f"rsi({r:.0f})")
            elif r < 35:
                score += 15
                flags.append(f"rsi({r:.0f})")
            elif r < 40:
                score += 8
        # 52-week-low zone (capitulation)
        if lo52 and px <= lo52 * 1.08:
            score += 10
            flags.append("near_52w_low")
        # Early reversal: RSI crossed back above 30
        if r is not None and r_prev is not None and r >= 30 and r_prev < 30:
            score += 20
            flags.append("early_reversal")
        # Accumulation: heavy volume green day after a slide
        if relvol >= 1.6 and px > prev:
            down20 = closes[-20] if len(closes) >= 21 else None
            if down20 and px < down20 and px > prev:
                score += 12
                flags.append(f"accumulation(volx{relvol:.1f})")
        # Momentum breakout: new 20-day high on volume
        if px >= hi20 and relvol >= 1.4:
            score += 15
            flags.append(f"breakout(volx{relvol:.1f})")

        # Quality multiplier: real ROIC makes a discount real, not a trap
        q = QUALITY.get(sym, 15)
        score += min(q, 30.0) / 30.0 * 15

        if score >= MIN_SCORE and flags:
            found.append({
                "ticker": sym, "date": str(datetime.date.today()),
                "price": round(px, 2), "score": round(score, 1),
                "rsi": round(r, 1) if r is not None else None,
                "relvol": round(relvol, 2),
                "vs_200ma": round((px / sma200 - 1) * 100, 1) if sma200 else None,
                "vs_52w_high": round((px / hi52 - 1) * 100, 1) if hi52 else None,
                "flags": flags,
            })

    found.sort(key=lambda o: o["score"], reverse=True)
    return found


def load():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {}


def save(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE)


def resolve_open_opportunities(state, prices):
    """Check previously flagged opportunities: did they bounce or die?
    Returns list of resolved events (ticker, outcome, ret)."""
    resolved = []
    today = datetime.date.today()
    for opp in list(state.get("opportunities", [])):
        if opp.get("outcome") is not None:
            continue
        px = prices.get(opp["ticker"])
        if not px:
            continue
        age = (today - datetime.date.fromisoformat(opp["date"])).days
        if age < 3:  # give it a few days before judging
            continue
        ret = px / opp["price"] - 1
        if ret >= BOUNCE_TARGET:
            opp["outcome"] = "bounce"
            opp["ret"] = round(ret * 100, 1)
            opp["resolved_date"] = str(today)
            resolved.append(opp)
        elif ret <= DUD_THRESHOLD:
            opp["outcome"] = "dud"
            opp["ret"] = round(ret * 100, 1)
            opp["resolved_date"] = str(today)
            resolved.append(opp)
    return resolved


def main():
    import sys
    if "--value" in sys.argv:
        vals = value_scan()
        print("=== QUALITY-ON-DISCOUNT SCREEN ===")
        for v in vals:
            mark = "FLAG" if v["flag"] else "    "
            print(f"{mark} {v['ticker']:5s} score {v['score']:5.1f} px ${v['price']:8.2f} "
                  f"ROIC~{v['roic_est'] if v['roic_est'] is not None else '--':>4} ROE {v['roe'] if v['roe'] is not None else '--':>4} "
                  f"FCFy {v['fcf_yield'] if v['fcf_yield'] is not None else '--':>4} EV/EBITDA {v['ev_ebitda'] if v['ev_ebitda'] is not None else '--':>4} "
                  f"200ma {v['vs_200ma'] if v['vs_200ma'] is not None else '--':>5} RSI {v['rsi'] if v['rsi'] is not None else '--':>4} [{', '.join(v['gates'])}]")
        return
    opps = scan()
    for o in opps[:5]:
        print(f"OPPORTUNITY {o['ticker']} score {o['score']:.0f} px ${o['price']:.2f} "
              f"rsi {o['rsi']} volx{o['relvol']} 200ma {o['vs_200ma']}% 52w {o['vs_52w_high']}%  [{', '.join(o['flags'])}]")


if __name__ == "__main__":
    main()

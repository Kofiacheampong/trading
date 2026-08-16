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
UNIVERSE = ["LULU", "KMB", "ZTS", "PYPL", "PAYC", "QCOM", "ADBE", "IT", "PNR",
            "AVAV", "KTOS", "RCAT", "ONDS"]

# Quality score = ROIC % (from our fundamental screens). Used to weight setups:
# a cheap price on a 27% ROIC business is an opportunity; on a 9% one it's a value trap.
# Drone names (AVAV/KTOS/RCAT/ONDS) have no verified ROIC on file -> default 15 weight.
QUALITY = {"LULU": 27.7, "KMB": 23.7, "ZTS": 27.8, "PYPL": 22.3, "PAYC": 30.0,
           "QCOM": 25.0, "ADBE": 30.0, "IT": 30.0, "PNR": 14.0,
           "AVAV": 15.0, "KTOS": 15.0, "RCAT": 15.0, "ONDS": 15.0}

MIN_SCORE = 40.0
BOUNCE_TARGET = 0.05     # +5% from flag price => "bounce" (good flag)
DUD_THRESHOLD = -0.08    # -8% from flag price   => "dud" (bad flag)


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
    state = load()
    opps = scan()
    for o in opps[:5]:
        print(f"OPPORTUNITY {o['ticker']} score {o['score']:.0f} px ${o['price']:.2f} "
              f"rsi {o['rsi']} volx{o['relvol']} 200ma {o['vs_200ma']}% 52w {o['vs_52w_high']}%  [{', '.join(o['flags'])}]")


if __name__ == "__main__":
    main()

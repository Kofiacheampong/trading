#!/usr/bin/env python3
"""
Options data layer for the momentum-call scanner (Phase 1 of MOMENTUM_CALLS_SPEC.md).

Generalizes the Yahoo v7 options fetching that sim.py already uses for puts into
a shared module: full call chains, expiry picking, spread math, Z-score, and the
SPY/VIX market-regime check. Cboe delayed quotes (free, official) as fallback.

Demo:
    python3 options_data.py PRGO          # regime + best 15-DTE expiry + liquid calls
"""
import json, os, subprocess, datetime, statistics, re

BASE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
CJ = "/tmp/sim_cookie.txt"          # shared cookie jar with sim.py
_REGIME_CACHE = {}


def _curl(url, cookie=False, timeout=20):
    """curl GET with optional cookie jar; returns (ok, text)."""
    cmd = ["curl", "-s", "-m", str(timeout), "-H", f"User-Agent: {UA}"]
    if cookie:
        cmd += ["-b", CJ]
    cmd += [url]
    out = subprocess.run(cmd, capture_output=True, text=True)
    return out.returncode == 0, out.stdout


# --------------------------------------------------------------------------
# Yahoo auth (crumb) — same flow sim.py already uses successfully for puts
# --------------------------------------------------------------------------
def get_crumb():
    """Return a valid Yahoo crumb (cookies + crumb endpoint). None on failure."""
    subprocess.run(["curl", "-s", "-m", "15", "-c", CJ, "-H", f"User-Agent: {UA}",
                    "https://fc.yahoo.com", "-o", "/dev/null"], check=False)
    ok, body = _curl("https://query1.finance.yahoo.com/v1/test/getcrumb", cookie=True)
    if ok and body.strip():
        return body.strip()
    return None


# --------------------------------------------------------------------------
# Price history / quotes (same chart API opportunity.py uses)
# --------------------------------------------------------------------------
def fetch_history(sym, rng="1y"):
    """Return (timestamps, closes, volumes) from Yahoo chart API; (None,None,None) on failure."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d"
    ok, out = _curl(url)
    if not ok:
        return None, None, None
    try:
        d = json.loads(out)
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


def fetch_quote(sym):
    """Latest price for sym (live during market hours)."""
    ts, closes, _ = fetch_history(sym, rng="1d")
    if not closes:
        return None
    return closes[-1]


def fetch_ohlc(sym, rng="1y"):
    """Return (ts, closes, opens, highs, lows, vols); Nones on failure.

    Same chart API as fetch_history but also parses open/high/low, which the
    momentum scanner needs for ADX and overnight-gap checks.
    """
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d"
    ok, out = _curl(url)
    if not ok:
        return None, None, None, None, None, None
    try:
        d = json.loads(out)
        res = d["chart"]["result"][0]
        q = res["indicators"]["quote"][0]
        closes, opens, highs, lows, vols = [], [], [], [], []
        ts = res.get("timestamp") or []
        for c, o, h, l, v in zip(q["close"], q["open"], q["high"], q["low"], q["volume"]):
            if c is not None:
                closes.append(c)
                opens.append(o if o is not None else c)
                highs.append(h if h is not None else c)
                lows.append(l if l is not None else c)
                vols.append(v or 0)
        return ts, closes, opens, highs, lows, vols
    except Exception:
        return None, None, None, None, None, None


def next_earnings(sym, crumb):
    """Next earnings date (datetime.date or None) via Yahoo quoteSummary calendarEvents."""
    url = (f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{sym}"
           f"?modules=calendarEvents&crumb={crumb}")
    ok, out = _curl(url, cookie=True)
    if not ok:
        return None
    try:
        d = json.loads(out)
        evs = d["quoteSummary"]["result"][0]["calendarEvents"]["earnings"]["earningsDate"]
        if not evs:
            return None
        ts = evs[0].get("raw")
        if not ts:
            return None
        return datetime.date.fromtimestamp(ts)
    except Exception:
        return None


# --------------------------------------------------------------------------
# Market regime: SPY vs 200-day SMA + VIX level
# --------------------------------------------------------------------------
def fetch_regime():
    """Return (spy_ok, vix, spy_px, spy_sma200). Cached per process run.

    spy_ok = SPY above its 200-day SMA (bull regime). vix = last close.
    """
    if "v" in _REGIME_CACHE:
        return _REGIME_CACHE["v"]
    spy_ok = vix = spy_px = spy_sma = None
    ts, closes, _ = fetch_history("SPY", rng="1y")
    if closes and len(closes) >= 200:
        spy_px = closes[-1]
        spy_sma = sum(closes[-200:]) / 200
        spy_ok = spy_px > spy_sma
    ts, closes, _ = fetch_history("%5EVIX", rng="1mo")
    if closes:
        vix = closes[-1]
    out = (spy_ok, vix, spy_px, spy_sma)
    _REGIME_CACHE["v"] = out
    return out


# --------------------------------------------------------------------------
# Math helpers
# --------------------------------------------------------------------------
def zscore(closes, period=20):
    """Std devs the latest close sits above the trailing `period` mean."""
    if len(closes) < period + 1:
        return None
    window = closes[-period:]
    mu = statistics.mean(window)
    sd = statistics.stdev(window)
    if sd == 0:
        return 0.0
    return (closes[-1] - mu) / sd


def spread_pct(bid, ask):
    """Bid/ask spread as % of mid. None if quotes are unusable."""
    if bid is None or ask is None or bid <= 0 or ask <= 0 or ask <= bid:
        return None
    return (ask - bid) / ((bid + ask) / 2) * 100


# --------------------------------------------------------------------------
# Expiries + option chains
# --------------------------------------------------------------------------
def expirations(sym, crumb):
    """List of unix expiry timestamps listed for sym (Yahoo)."""
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{sym}?crumb={crumb}"
    ok, out = _curl(url, cookie=True)
    if not ok:
        return []
    try:
        d = json.loads(out)
        return d["optionChain"]["result"][0].get("expirationDates") or []
    except Exception:
        return []


def pick_expiry(sym, crumb, target_dte=15, min_dte=10, max_dte=21):
    """Nearest listed expiry with DTE in [min_dte, max_dte], preferring target.

    Returns (expiry_unix_ts, dte) or (None, None).
    """
    today = datetime.date.today()
    cands = []
    for e in expirations(sym, crumb):
        dte = (datetime.date.fromtimestamp(e) - today).days
        if min_dte <= dte <= max_dte:
            cands.append((abs(dte - target_dte), dte, e))
    if not cands:
        return None, None
    cands.sort()
    return cands[0][2], cands[0][1]


def _norm(c):
    """Normalize one Yahoo call dict."""
    bid, ask = c.get("bid") or 0, c.get("ask") or 0
    last = c.get("lastPrice") or 0
    mid = (bid + ask) / 2 if bid > 0 and ask > 0 else last
    return {
        "strike": c.get("strike"),
        "bid": bid, "ask": ask, "last": last, "mid": mid,
        "iv": c.get("impliedVolatility"),
        "oi": c.get("openInterest") or 0,
        "volume": c.get("volume") or 0,
        "delta": c.get("delta"),
        "expiry": c.get("expiration"),
    }


def fetch_chain(sym, expiry_ts, crumb):
    """Call options for sym/expiry via Yahoo v7; [] on failure."""
    url = (f"https://query1.finance.yahoo.com/v7/finance/options/{sym}"
           f"?date={expiry_ts}&crumb={crumb}")
    ok, out = _curl(url, cookie=True)
    if not ok:
        return []
    try:
        d = json.loads(out)
        opts = d["optionChain"]["result"][0]["options"][0]["calls"]
        return [_norm(c) for c in opts]
    except Exception:
        return []


def fetch_chain_cboe(sym, expiry_ts, max_dte_gap=3):
    """Calls via Cboe delayed quotes (free, official). Matches nearest listed
    expiry to expiry_ts (Cboe symbols carry their own dates). [] on failure."""
    cua = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/120 Safari/537.36")
    out = subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {cua}",
                          f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        want = datetime.date.fromtimestamp(expiry_ts)
        pat = re.compile(r"^[A-Z]+\d{6}C(\d{8})$")
        best, best_gap = None, 10 ** 9
        for o in d["data"]["options"]:
            m = pat.match(o["option"])
            if not m:
                continue
            y = o["option"][len(sym):len(sym) + 6]
            exp = datetime.date(2000 + int(y[:2]), int(y[2:4]), int(y[4:6]))
            gap = abs((exp - want).days)
            if gap > max_dte_gap:
                continue
            bid, ask = o.get("bid") or 0, o.get("ask") or 0
            last = o.get("last_trade_price") or o.get("last_price") or 0
            mid = (bid + ask) / 2 if bid > 0 and ask > 0 else last
            rec = {"strike": int(m.group(1)) / 1000.0, "bid": bid, "ask": ask,
                   "last": last, "mid": mid, "iv": o.get("iv"), "oi": o.get("open_interest") or 0,
                   "volume": o.get("volume") or 0, "delta": None, "expiry": str(exp)}
            if gap < best_gap:
                best_gap = gap
                best = rec
        return [best] if best else []
    except Exception:
        return []


def fetch_best_chain(sym, expiry_ts, crumb):
    """Yahoo chain, Cboe fallback."""
    chain = fetch_chain(sym, expiry_ts, crumb)
    if not chain:
        chain = fetch_chain_cboe(sym, expiry_ts)
    return chain


# --------------------------------------------------------------------------
# Demo: regime + picked expiry + liquid calls near spot for one ticker
# --------------------------------------------------------------------------
def main(sym):
    crumb = get_crumb()
    if not crumb:
        print("NO_CRUMB")
        return
    spy_ok, vix, spy_px, spy_sma = fetch_regime()
    print(f"REGIME SPY ${spy_px:.2f} vs SMA200 ${spy_sma:.2f} -> "
          f"{'OK' if spy_ok else 'RISK'} | VIX {vix:.1f}" if vix else "REGIME SPY n/a")
    ts, dte = pick_expiry(sym, crumb)
    if not ts:
        print(f"NO_EXPIRY {sym}")
        return
    print(f"EXPIRY {datetime.date.fromtimestamp(ts)} ({dte} DTE)")
    spot = fetch_quote(sym)
    chain = fetch_best_chain(sym, ts, crumb)
    print(f"SPOT {sym} ${spot:.2f}" if spot else f"SPOT {sym} n/a")
    rows = [c for c in chain if c["strike"] and c["bid"] > 0 and c["ask"] > 0]
    rows.sort(key=lambda c: abs(c["strike"] - spot) if spot else 0)
    for c in rows[:8]:
        sp = spread_pct(c["bid"], c["ask"])
        iv = c["iv"] * 100 if c["iv"] else 0
        print(f"  {c['strike']:>7.2f}  bid {c['bid']:.2f} ask {c['ask']:.2f} "
              f"mid {c['mid']:.2f}  spr {sp:.0f}%  IV {iv:.0f}%  OI {c['oi']}  vol {c['volume']}")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "PRGO")

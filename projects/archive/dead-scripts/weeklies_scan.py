#!/usr/bin/env python3
"""Weeklies Scanner — bull call spreads for small account ($50-150 debit).
Data: Cboe delayed quotes (full chains) + Yahoo chart API for spot.
Usage: python3 weeklies_scan.py TICKER1 TICKER2 ...
"""
import json, re, sys, urllib.request, datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())

def spot(ticker):
    try:
        d = fetch(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d")
        m = d["chart"]["result"][0]["meta"]
        return m.get("regularMarketPrice") or m.get("chartPreviousClose")
    except Exception:
        return None

def chain(ticker):
    try:
        d = fetch(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{ticker}.json")
        return d["data"]["options"]
    except Exception as e:
        print(f"  ! chain fetch failed: {e}")
        return []

PAT = re.compile(r"^([A-Z]+)(\d{6})([CP])(\d+)$")

def scan(ticker, expiries=("260814", "260821"), widths=(1, 2)):
    px = spot(ticker)
    opts = chain(ticker)
    if not opts:
        print(f"{ticker}: NO CHAIN"); return
    by_exp = {}
    for o in opts:
        sym = o["option"]
        m = PAT.match(sym)
        if not m: continue
        exp = m.group(2)
        kind = m.group(3)
        strike = int(m.group(4)) / 1000.0
        by_exp.setdefault(exp, []).append((kind, strike, o))
    print(f"\n=== {ticker} | spot ~${px} | expiries: {sorted(by_exp.keys())}")
    for exp in expiries:
        if exp not in by_exp:
            print(f"  {exp}: no chain"); continue
        calls = sorted([(s, o) for k, s, o in by_exp[exp] if k == "C"], key=lambda x: x[0])
        if not calls:
            print(f"  {exp}: no calls"); continue
        print(f"  --- expiry {exp} ({len(calls)} calls) ---")
        rows = []
        for i, (s1, o1) in enumerate(calls):
            for s2, o2 in calls[i+1:]:
                w = round(s2 - s1, 2)
                if w not in widths: continue
                ask1, bid2 = o1["ask"], o2["bid"]
                if not ask1 or not bid2 or ask1 <= 0 or bid2 < 0.01: continue
                cost = round(ask1 - bid2, 2)
                cost_usd = cost * 100
                if not (40 <= cost_usd <= 160): continue
                maxp = round((w - cost) * 100, 2)
                if maxp <= 0: continue
                be = round(s1 + cost, 2)
                need = (be - px) / px * 100 if px else 0
                roi = maxp / cost_usd * 100 if cost_usd else 0
                liq = min(o1["open_interest"] or 0, o2["open_interest"] or 0) + min(o1["volume"] or 0, o2["volume"] or 0)
                rows.append((s1, s2, cost_usd, maxp, roi, be, need, liq, o1, o2))
        # sort: prefer lower % move needed (>=0), then higher ROI, then liquidity
        rows.sort(key=lambda r: ((r[6] if r[6] >= 0 else 99), -r[4], -r[7]))
        for r in rows[:8]:
            s1, s2, cost_usd, maxp, roi, be, need, liq, o1, o2 = r
            print(f"    {s1:>6}/{s2:<6} cost ${cost_usd:>6.2f} | max ${maxp:>7.2f} ({roi:>5.0f}%) | B/E {be:>6.2f} | need {need:>5.1f}% | OI {o1['open_interest'] or 0}/{o2['open_interest'] or 0} vol {o1['volume'] or 0}/{o2['volume'] or 0}")

if __name__ == "__main__":
    for t in sys.argv[1:]:
        scan(t.upper())

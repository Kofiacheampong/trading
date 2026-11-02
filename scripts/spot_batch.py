#!/usr/bin/env python3
"""Batch spot/quote fetch from Yahoo v8 chart. Usage: spot_batch.py TICK..."""
import json, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

def q(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1mo&interval=1d"
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=15) as r:
            d = json.loads(r.read().decode())
        res = d["chart"]["result"][0]
        m = res["meta"]
        px = m.get("regularMarketPrice")
        qd = res["indicators"]["quote"][0]
        closes = [c for c in qd["close"] if c is not None]
        wk = closes[0] if closes else None
        prev = closes[-2] if len(closes) >= 2 else None
        chg = (px - prev) / prev * 100 if prev else 0
        wchg = (px - wk) / wk * 100 if wk else 0
        print(f"{t}\t{px}\t{chg:+.1f}%\t{wchg:+.1f}%\t{m.get('fiftyTwoWeekLow')}\t{m.get('fiftyTwoWeekHigh')}\t{m.get('regularMarketVolume')}")
    except Exception as e:
        print(f"{t}\tERR\t{type(e).__name__}")

for t in sys.argv[1:]:
    q(t.upper())

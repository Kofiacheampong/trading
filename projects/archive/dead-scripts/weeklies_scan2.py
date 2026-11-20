#!/usr/bin/env python3
"""Weeklies Scanner v2 — bull call spreads for small account.
Cboe delayed quotes (chains) + Yahoo chart API (spot). Usage: weeklies_scan2.py EXP1 EXP2 TICK...
EXPs are YYMMDD. Prints best 1-wide/2-wide debit spreads per expiry.
"""
import json, re, sys, urllib.request, datetime

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
PAT = re.compile(r"^([A-Z0-9\.]+?)(\d{6})([CP])(\d{8})$")


def fetch(url, timeout=20):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def spot(ticker):
    try:
        d = fetch(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d")
        res = d["chart"]["result"][0]
        m = res["meta"]
        px = m.get("regularMarketPrice")
        q = res["indicators"]["quote"][0]
        closes = [c for c in q["close"] if c is not None]
        prev = closes[-2] if len(closes) >= 2 else m.get("chartPreviousClose")
        return px, prev, m.get("regularMarketTime")
    except Exception:
        return None, None, None


def chain(ticker):
    try:
        d = fetch(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{ticker}.json")
        return d["data"]["options"]
    except Exception as e:
        return None


def scan(ticker, expiries, widths=(1, 2)):
    px, prev, ts = spot(ticker)
    opts = chain(ticker)
    if opts is None:
        print(f"{ticker}\tNO_CHAIN"); return
    if px is None:
        print(f"{ticker}\tNO_SPOT"); return
    by_exp = {}
    for o in opts:
        sym = o["option"]
        m = PAT.match(sym)
        if not m: continue
        exp = m.group(2); kind = m.group(3)
        strike = int(m.group(4)) / 1000.0
        by_exp.setdefault(exp, {})("C") if False else None
        by_exp.setdefault(exp, []).append((kind, strike, o))
    avail = sorted(by_exp.keys())
    chg = (px - prev) / prev * 100 if prev else 0
    print(f"\n=== {ticker} | spot ${px:.2f} (prev {prev:.2f}, {chg:+.1f}%) | exps {','.join(avail[:12])}")
    for exp in expiries:
        if exp not in by_exp:
            print(f"  {exp}: no chain"); continue
        calls = sorted([(s, o) for k, s, o in by_exp[exp] if k == "C"], key=lambda x: x[0])
        if not calls:
            print(f"  {exp}: no calls"); continue
        rows = []
        for i, (s1, o1) in enumerate(calls):
            for s2, o2 in calls[i+1:]:
                w = round(s2 - s1, 2)
                if w not in widths: continue
                a1 = o1.get("ask") or 0; b2 = o2.get("bid") or 0
                if not a1 or b2 < 0.01: continue
                cost = round(a1 - b2, 2)
                cu = cost * 100
                if not (35 <= cu <= 170): continue
                maxp = round((w - cost) * 100, 2)
                if maxp < cu * 0.6: continue   # want decent R:R
                be = round(s1 + cost, 2)
                need = (be - px) / px * 100 if px else 0
                roi = maxp / cu * 100
                oi1 = o1.get("open_interest") or 0; oi2 = o2.get("open_interest") or 0
                v1 = o1.get("volume") or 0; v2 = o2.get("volume") or 0
                spr1 = (o1.get("ask",0)-o1.get("bid",0))
                rows.append((s1, s2, cu, maxp, roi, be, need, oi1, oi2, v1, v2))
        # prefer low %-move-needed, then ROI, then OI
        rows.sort(key=lambda r: ((r[6] if r[6] >= 0 else 99), -r[4], -(r[7]+r[8])))
        print(f"  --- {exp} ({len(calls)} calls) ---")
        for r in rows[:6]:
            s1,s2,cu,maxp,roi,be,need,oi1,oi2,v1,v2 = r
            print(f"    {s1:>7.2f}/{s2:<7.2f} cost ${cu:>6.0f} | max ${maxp:>7.0f} ({roi:>4.0f}%) | B/E {be:>7.2f} | need {need:>5.1f}% | OI {oi1}/{oi2} vol {v1}/{v2}")


if __name__ == "__main__":
    exps = sys.argv[1].split(",")
    tks = sys.argv[2:]
    for t in tks:
        try:
            scan(t.upper(), exps)
        except Exception as e:
            print(f"{t}\tERR {type(e).__name__}: {e}")

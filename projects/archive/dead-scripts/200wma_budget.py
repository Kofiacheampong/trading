#!/usr/bin/env python3
import json, subprocess, sys, statistics

SYMBOLS = "TPR PAYC PNR RL CROX SKX DOCU SCI BBY TPX MKC TXRH DKNG ESTC TWLO".split()

def fetch(sym):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=5y&interval=1wk"
    out = subprocess.run(["curl","-s","-m","15","-H","User-Agent: Mozilla/5.0",url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["chart"]["result"][0]
        closes = res["indicators"]["quote"][0]["close"]
        return closes
    except Exception:
        return None

rows = []
for sym in SYMBOLS:
    closes = fetch(sym)
    if not closes:
        print(f"{sym}: FAILED", file=sys.stderr); continue
    closes = [c for c in closes if c is not None]
    if len(closes) < 205:
        print(f"{sym}: only {len(closes)} weeks", file=sys.stderr); continue
    last = closes[-1]
    sma200 = statistics.mean(closes[-200:])
    dist = (last/sma200 - 1)*100
    rows.append((sym, last, sma200, dist))

rows.sort(key=lambda r: r[3])
print(f"{'SYM':6s} {'LAST':>9s} {'200W':>9s} {'DIST%':>8s}")
for sym, last, sma, dist in rows:
    flag = "  <-- BELOW" if dist < 0 else ("  <-- near line" if dist < 10 else "")
    print(f"{sym:6s} {last:9.2f} {sma:9.2f} {dist:7.1f}%{flag}")

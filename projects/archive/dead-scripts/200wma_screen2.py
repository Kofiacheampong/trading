#!/usr/bin/env python3
import json, subprocess, sys, statistics

SYMBOLS = """AAPL MSFT GOOGL META NVDA AVGO ASML TSM TXN QCOM
V MA ADP COST HD LIN NKE PEP KO PG JNJ UNH LLY ABBV
NOW CRM ADBE ORCL INTU MSCI SPGI MCO DHR TMO ISRG
NFLX MELI AMZN IBM MU CAT ITW ROP SHW WM CMG
SNPS CDNS ANSS TYL WDAY TEAM DDOG PANW CRWD ZS
SNOW VEEV ACN IT GIB FDS BR MKTX CBOE NDAQ ICE CME
PYPL FI GPN FIS AXP DFS SBUX MCD YUM DRI DPZ TGT WMT
LULU DECK EL CL KMB MDLZ HSY STZ MNST PM MO KDP UL
ABT BDX BSX EW HCA MRK AMGN GILD VRTX REGN ZTS IDXX
WAT STE PH EMR HON FAST GWW CTAS CMI DE PCAR TT OTIS
TDG HEI URI POOL WSO EXP WAB LMT RTX HWM ROK ETN AME
IEX GGG LRCX AMAT KLAC ADI NXPI MCHP SWKS CSCO MSI
FFIV BRK.B MMC AJG WTW BX APO ARES TRV CB BABA TCEHY BTI""".split()

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
    flag = ""
    if dist < 0: flag = "  <-- BELOW"
    elif dist < 10: flag = "  <-- near line"
    print(f"{sym:6s} {last:9.2f} {sma:9.2f} {dist:7.1f}%{flag}")

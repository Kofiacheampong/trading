#!/usr/bin/env python3
import json, subprocess, sys, datetime

CJ = "/tmp/cj_opt.txt"

def get_crumb():
    subprocess.run(["curl","-s","-m","15","-c",CJ,"-H","User-Agent: Mozilla/5.0","https://fc.yahoo.com","-o","/dev/null"], check=False)
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H","User-Agent: Mozilla/5.0","https://query1.finance.yahoo.com/v1/test/getcrumb"], capture_output=True, text=True)
    return out.stdout.strip()

CRUMB = get_crumb()

WATCH = {
    "ADBE": (250.41, 415.65), "ACN": (165.92, 290.11), "QCOM": (147.61, 151.01),
    "DECK": (96.88, 114.56), "ZTS": (77.29, 156.46), "FDS": (263.20, 391.52),
    "PYPL": (57.21, 66.00), "IT": (151.02, 354.67),
}

def fetch(sym, date=None):
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{sym}?crumb={CRUMB}"
    if date: url += f"&date={date}"
    out = subprocess.run(["curl","-s","-m","15","-b",CJ,"-H","User-Agent: Mozilla/5.0",url],
                         capture_output=True, text=True)
    try:
        return json.loads(out.stdout)["optionChain"]["result"][0]
    except Exception:
        return None

def main():
    today = datetime.date(2026, 8, 1)
    for sym, (px, ma) in WATCH.items():
        res = fetch(sym)
        if not res:
            print(f"{sym}: fetch failed"); continue
        exps = res.get("expirationDates") or []
        if not exps:
            print(f"{sym}: no expirations"); continue
        target = None
        for e in exps:
            d = datetime.date.fromtimestamp(e)
            if (d - today).days >= 30:
                target = e; break
        if target is None: target = exps[-1]
        d = datetime.date.fromtimestamp(target)
        dte = (d - today).days
        res2 = fetch(sym, target)
        if not res2:
            print(f"{sym}: chain fail"); continue
        calls = {c["strike"]: c for c in res2["options"][0].get("calls", [])}
        puts = {p["strike"]: p for p in res2["options"][0].get("puts", [])}
        strikes = sorted(puts.keys())
        if not strikes:
            print(f"{sym}: no puts"); continue
        def near(t):
            return min(strikes, key=lambda s: abs(s - t))
        print(f"\n=== {sym}  px={px:.2f}  200wk={ma:.0f}  exp={d} ({dte}d) ===")
        for lbl, mult in (("~12% OTM", 0.88), ("~20% OTM", 0.80)):
            s = near(px * mult)
            p = puts[s]
            bid, ask = p.get("bid",0), p.get("ask",0)
            iv, oi = p.get("impliedVolatility",0), p.get("openInterest",0)
            mid = (bid+ask)/2
            coll = s*100
            spr = (ask-bid)/mid*100 if mid > 0 else 0
            yld = mid/coll*100 if coll > 0 else 0
            print(f"  PUT {lbl}: ${s:.0f} | bid {bid:.2f} ask {ask:.2f} (spread {spr:.0f}%) | IV {iv*100:.0f}% | OI {oi} | prem ${mid*100:.0f} = {yld:.1f}% on ${coll:,.0f}")
        sc = min(calls.keys(), key=lambda s: abs(s - px))
        c = calls[sc]
        print(f"  ATM CALL: ${sc:.0f} | bid {c.get('bid',0):.2f} ask {c.get('ask',0):.2f} | IV {c.get('impliedVolatility',0)*100:.0f}% | OI {c.get('openInterest',0)}")

if __name__ == "__main__":
    main()

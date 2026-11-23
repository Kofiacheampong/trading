import warnings, yfinance as yf
warnings.filterwarnings("ignore")
for s in ["SOFI","HPQ","RIOT","HIMS","RIVN","KSS","CHWY","MARA","PLUG","SOUN","ACHR","NNE","UUUU","MP","TEVA","GRAB","SNAP","PATH","AI","LCID","NIO"]:
    try:
        t=yf.Ticker(s); px=float(t.fast_info.get("lastPrice"))
        if not(3<=px<=50): print(f"{s} skip px={px:.2f}"); continue
        exps=[e for e in t.options if e.startswith("2026-12-04")]
        if not exps: print(f"{s} ${px:.2f} no 12/04 weekly"); continue
        c=t.option_chain(exps[0]).calls
        c=c.assign(oi=c.openInterest.fillna(0)).sort_values("oi",ascending=False).drop_duplicates("strike").sort_values("strike")
        c=c[(c.strike>=px*0.93)&(c.strike<=px*1.28)&(c.ask>0)]
        print(f"\n{s} ${px:.2f} 2026-12-04")
        for _,r in c.iterrows():
            print(f"  {r.strike:>6.1f} {r.bid:>5.2f}/{r.ask:<5.2f} oi={r.oi:>6.0f} v={(r.volume if r.volume==r.volume else 0):>5.0f} iv={r.impliedVolatility*100:>3.0f}%")
    except Exception as e: print(s,"ERR",str(e)[:60])

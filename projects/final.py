import warnings, datetime as dt, yfinance as yf
warnings.filterwarnings("ignore")
today=dt.date(2026,11,22)
N={"SOFI":"2026-11-27","RIOT":"2026-11-27","HIMS":"2026-11-27","RIVN":"2026-11-27",
"HPQ":"2026-11-27","KSS":"2026-11-27","CHWY":"2026-11-27","SYM":"2026-11-27",
"TCOM":"2026-12-18","BILI":"2026-12-18","LI":"2026-11-27","MARA":"2026-11-27"}
for s,exp in N.items():
    try:
        t=yf.Ticker(s); px=float(t.fast_info.get("lastPrice"))
        c=t.option_chain(exp).calls
        c=c.assign(oi=c.openInterest.fillna(0)).sort_values("oi",ascending=False).drop_duplicates("strike").sort_values("strike")
        c=c[(c.strike>=px*0.92)&(c.strike<=px*1.32)]
        print(f"\n{s} ${px:.2f} exp={exp}")
        for _,r in c.iterrows():
            if r.ask<=0: continue
            print(f"  {r.strike:>6.0f} bid={r.bid:>5.2f} ask={r.ask:>5.2f} oi={r.oi:>6.0f} v={(r.volume if r.volume==r.volume else 0):>5.0f} iv={r.impliedVolatility*100:>3.0f}%")
    except Exception as e: print(s,"ERR",e)

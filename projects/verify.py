import warnings, datetime as dt, yfinance as yf
warnings.filterwarnings("ignore")
today = dt.date(2026,11,22)
tick = {"CLSK":"2026-11-24","BILI":"2026-11-24","LI":"2026-11-25","HPQ":"2026-11-24",
"NAT":"2026-11-27","AEXA":"2026-11-25","CMBT":"2026-11-24","AMTM":"2026-11-23",
"KSS":"2026-11-24","VIPS":"2026-11-24","TCOM":"2026-11-23","BZ":"2026-11-25",
"SYM":"2026-11-23","MMED":"2026-11-24","GASS":"2026-11-24","TITN":"2026-11-24"}
for s,er in tick.items():
    try:
        t=yf.Ticker(s); fi=t.fast_info; px=float(fi.get("lastPrice"))
        prev=float(fi.get("previousClose") or px); av=float(fi.get("lastVolume") or 0)
        exps=[e for e in t.options if 3<=(dt.datetime.strptime(e,"%Y-%m-%d").date()-today).days<=40]
        exps.sort(key=lambda e: dt.datetime.strptime(e,"%Y-%m-%d").date())
        print(f"\n=== {s} ${px:.2f} ({100*(px-prev)/prev:+.1f}%) vol={av/1e6:.1f}M ER={er} exps={exps[:3]}")
        ch=t.option_chain(exps[0]); c=ch.calls
        c=c[(c.strike>=px*0.95)&(c.strike<=px*1.30)]
        for _,r in c.iterrows():
            print(f"  {r.strike:>6.0f}C bid={r.bid:>5.2f} ask={r.ask:>5.2f} iv={r.impliedVolatility*100:>5.0f}% oi={r.openInterest:>6.0f} v={r.volume:>5.0f}")
    except Exception as e:
        print(f"{s}: ERR {e}")

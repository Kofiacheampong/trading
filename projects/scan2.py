import warnings, datetime as dt, yfinance as yf, json
warnings.filterwarnings("ignore")
today=dt.date(2026,11,22)

# earnings names <=$50 from this week's calendar (filtered) + curated liquid sub-$50
EARN={"HPQ":"11/24 BMO","KSS":"11/24 BMO","SYM":"11/23 AMC","TCOM":"11/23","BILI":"11/24",
"LI":"11/25","CLSK":"11/24","VIPS":"11/24","AMTM":"11/23","BZ":"11/25","NAT":"11/27",
"DLTR":"11/24","BBY":"11/24","SJM":"11/24","PD":"11/24","MMED":"11/24","GDS":"11/25",
"CMBT":"11/24","TITN":"11/24","GASS":"11/24","CMP":"11/23","AEXA":"11/25"}
CUR=["SOFI","HIMS","RIVN","LCID","NIO","MARA","RIOT","CLSK","AAL","UAL","SNAP","PATH",
"SOUN","ACHR","JOBY","SMR","NNE","PLUG","RUN","GRAB","CHWY","TEVA","VALE","HL","EXK",
"AG","UUUU","REMX","LIT","URA","GDX","KWEB","FXI","SOXS","TNA","BITO","AI","BBAI","IONQ"]
UNIV={**{k:EARN[k] for k in EARN}, **{k:"momentum" for k in CUR}}
rows=[]
for s,cat in UNIV.items():
    try:
        t=yf.Ticker(s); fi=t.fast_info; px=float(fi.get("lastPrice"))
        if not(3<=px<=50): continue
        ch_prev=float(fi.get("previousClose") or px)
        try: av=float(fi.get("threeMonthAverageVolume") or 0)
        except: av=0
        exps=[e for e in t.options if 3<=(dt.datetime.strptime(e,"%Y-%m-%d").date()-today).days<=45]
        if not exps: continue
        exps.sort(key=lambda e: dt.datetime.strptime(e,"%Y-%m-%d").date())
        exp=exps[0]
        c=t.option_chain(exp).calls
        c=c.dropna(subset=["strike"]).sort_values("strike")
        # dedupe strikes: keep row with max OI
        c=c.assign(oi=c.openInterest.fillna(0)).sort_values("oi",ascending=False).drop_duplicates("strike").sort_values("strike")
        best=None
        for i in range(len(c)):
            a=c.iloc[i]
            if not(px*0.96<=a.strike<=px*1.08): continue
            if a.ask<=0 or a.oi<150: continue
            for j in range(i+1,len(c)):
                b=c.iloc[j]; w=b.strike-a.strike
                if w<=0 or w>3.01: continue
                if b.strike>px*1.30: continue
                if b.bid<=0 or b.oi<150: continue
                deb=a.ask-b.bid
                if deb<=0: continue
                cost=deb*100
                if not(40<=cost<=155): continue
                maxp=(w-deb)*100
                if maxp<=0: continue
                mid_deb=(a.bid+a.ask)/2-(b.bid+b.ask)/2
                mid_cost=mid_deb*100
                rr=maxp/cost; be=a.strike+deb; mv=(be-px)/px*100
                sp=(a.ask-a.bid)/a.ask
                score=rr*100-mv*4-sp*60
                if best is None or score>best["score"]:
                    best=dict(score=score,exp=exp,k1=float(a.strike),k2=float(b.strike),cost=cost,
                        midcost=mid_cost,maxp=maxp,rr=rr,be=be,mv=mv,
                        oi1=float(a.oi),oi2=float(b.oi),spreadpct=sp)
        if best:
            best.update(sym=s,px=px,chg=100*(px-ch_prev)/ch_prev,cat=cat,vol=av)
            rows.append(best)
    except Exception as e: pass
rows.sort(key=lambda r:-r["score"])
json.dump(rows,open("scan2.json","w"),indent=1)
for r in rows[:18]:
    print(f"{r['sym']:5s} ${r['px']:>6.2f} {r['chg']:>+6.1f}% {r['exp']} {r['k1']:.0f}/{r['k2']:.0f}C "
          f"cost=${r['cost']:>3.0f}(mid${r['midcost']:>3.0f}) max=${r['maxp']:>3.0f} rr={r['rr']:.2f} "
          f"be={r['be']:.2f} need={r['mv']:>4.1f}% oi={r['oi1']:.0f}/{r['oi2']:.0f} sp={r['spreadpct']*100:.0f}% | {r['cat']}")

#!/usr/bin/env python3
import json
M=json.load(open('model.json'))
R=json.load(open('model_rows.json'))

def q(rows,n): return rows[n*3:(n+1)*3]
def qsum(rows,n,key): return sum(r[key] for r in q(rows,n))

print('=== BASE 2028 QUARTERLY ===')
for n in range(4):
    rs=q(R['base']['rows28'],n)
    print(f"2028 Q{n+1} loc {rs[-1]['loc']:.0f} pay {rs[-1]['paying']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} cogs {sum(r['cogs'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} costs {sum(r['cogs']+r['opex'] for r in rs):,.0f} net {sum(r['net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")
print('=== BASE 2029 QUARTERLY ===')
for n in range(4):
    rs=q(R['base']['rows29'],n)
    print(f"2029 Q{n+1} loc {rs[-1]['loc']:.0f} pay {rs[-1]['paying']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} cogs {sum(r['cogs'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} costs {sum(r['cogs']+r['opex'] for r in rs):,.0f} net {sum(r['net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")

print('\n=== SCENARIO TABLE ===')
for k,s in M.items():
    y27,y28,y29=s['y27'],s['y28'],s['y29']
    print(f"{k:18s} 27rev {y27['rev']:>9,.0f} 27net {y27['net']:>9,.0f} tr {s['trough']['month']:>3s} {s['trough']['cash']:>8,.0f} 27cash {y27['cash']:>8,.0f} | 28rev {y28['rev']:>9,.0f} 28net {y28['net']:>9,.0f} 28low {y28['low']:>8,.0f} | 29rev {y29['rev']:>10,.0f} 29net {y29['net']:>9,.0f} 29low {y29['low']:>8,.0f}")

print('\n=== DELAY 2028 MONTHLY (cash no protocol / protocol) ===')
for a,b in zip(R['delay']['rows28'], R['delay_protocol']['rows28']):
    print(f"{a['month']} rev {a['rev']+a['setup']:>7,.0f} / {b['rev']+b['setup']:>7,.0f}  net {a['net']:>7,.0f} / {b['net']:>7,.0f}  cash {a['cash']:>8,.0f} / {b['cash']:>8,.0f}")

print('\n=== BASE 2027 COST LINES ===')
for r in R['base']['rows27']:
    print(f"{r['month']} infra {r['infra']:>5,.0f} pay {r['payments']:>5,.0f} sup {r['support']:>5,.0f} opex {r['opex']:>5,.0f}")

print('\n=== BASE 2028 Q1 COST LINES ===')
for r in R['base']['rows28'][:3]:
    print(f"{r['month']} infra {r['infra']:>5,.0f} pay {r['payments']:>5,.0f} sup {r['support']:>5,.0f} onb {r['onboarding']:>5,.0f} opex {r['opex']:>5,.0f}")

print('\n=== PER-GROUP UNIT ECONOMICS ===')
def per_group(loc=14, arpu=98, gm=0.89, churn=0.015, selling_h=18, close='1-in-4'):
    rev=loc*arpu
    gp=rev*gm
    cac=selling_h*55+600
    onboarding=loc*2*60
    setup=1500
    upfront=cac+onboarding-setup
    payback=upfront/gp
    life=1/churn
    ltv=gp*life
    return dict(loc=loc,rev=rev,gp=gp,cac=cac,onboarding=onboarding,setup=setup,upfront=upfront,payback=payback,life=life,ltv=ltv,ratio=ltv/cac)
for name,kw in [('base',{}),('g10',dict(loc=10)),('slowchurn',dict(churn=0.025)),('c6',dict(selling_h=24)),('stress',dict(loc=10,selling_h=24,churn=0.025,arpu=84))]:
    d=per_group(**kw)
    print(name, {k:round(v,2) for k,v in d.items()})

print('\n=== FOUNDER HOURS (400h build, 60/40) ===')
# quarterly totals per founder
A={'Q1':180+16+32.5,'Q2':60+24+84+32.5,'Q3':16+56+32.5,'Q4':24+70+30+32.5}
B={'Q1':120+38+32.5,'Q2':40+57+84+32.5,'Q3':38+56+32.5,'Q4':57+70+30+32.5}
for n in ['Q1','Q2','Q3','Q4']:
    print(n, f"A {A[n]:.1f}h {A[n]/13:.1f}h/wk  B {B[n]:.1f}h {B[n]/13:.1f}h/wk")
print('annual', f"A {sum(A.values()):.0f}h {sum(A.values())/52:.1f}h/wk  B {sum(B.values()):.0f}h {sum(B.values())/52:.1f}h/wk")

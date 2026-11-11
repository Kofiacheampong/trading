#!/usr/bin/env python3
import json
M=json.load(open('model_v3.json'))
R=json.load(open('model_v3_rows.json'))

def q(rows,n): return rows[n*3:(n+1)*3]
print('=== BASE 2027 MONTHLY ===')
for r in R['base'][:12]:
    print(f"{r['month']} live {r['live']:.0f} pay {r['pay']:.0f} rev {r['rev']+r['setup']:,.0f} cashnet {r['cash_net']:,.0f} econ {r['econ_net']:,.0f} cash {r['cash']:,.0f} ar {r['ar']:,.0f}")
print('\n=== BASE 2028 QUARTERLY ===')
for n in range(4):
    rs=q(R['base'][12:24],n)
    print(f"2028 Q{n+1} live {rs[-1]['live']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} net {sum(r['econ_net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")
print('\n=== BASE 2029 QUARTERLY ===')
for n in range(4):
    rs=q(R['base'][24:36],n)
    print(f"2029 Q{n+1} live {rs[-1]['live']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} net {sum(r['econ_net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")
print('\n=== SCENARIOS ===')
for k,s in M.items():
    y27,y28,y29=s['y27'],s['y28'],s['y29']
    print(f"{k:11s} 27rev {y27['rev']:>8,.0f} 27econ {y27['econ_net']:>8,.0f} 27cash {y27['cash_net']:>8,.0f} tr {s['trough']['month']} {s['trough']['cash']:>7,.0f} ye {y27['cash']:>7,.0f} | 28rev {y28['rev']:>9,.0f} net {y28['econ_net']:>8,.0f} low {y28['low']:>7,.0f} grp {y28['groups']:>4.1f} | 29rev {y29['rev']:>10,.0f} net {y29['econ_net']:>9,.0f} low {y29['low']:>8,.0f} grp {y29['groups']:>5.1f}")

print('\n=== PER-GROUP ECONOMICS ===')
for name,loc,arpu,cac,churn in [('base',14,98,1590,0.02),('g10',10,98,1590,0.02),('c6',14,98,1920,0.02),('downside',10,98,1920,0.035)]:
    rev=loc*arpu; gp=rev*0.89; onb=loc*2*60; upfront=cac+onb-1500; payback=upfront/gp; life=1/churn; ltv=gp*life
    print(f"{name}: rev {rev:,.0f} gp {gp:,.0f} cac {cac:,.0f} onb {onb:,.0f} netonb {onb-1500:,.0f} upfront {upfront:,.0f} payback {payback:.2f} life {life:.0f} ltv {ltv:,.0f} ratio {ltv/cac:.1f}")

print('\n=== SETUP FEE ===')
for loc in [10,12,14,16]:
    cost=loc*2*60
    print(f"{loc} locations: onboarding {cost:,.0f} setup 1,500 margin {1500-cost:,.0f} breakeven hours {1500/(loc*60):.2f}")

print('\n=== FOUNDER HOURS ===')
A={'Q1':180+16+32.5,'Q2':60+24+84+32.5,'Q3':16+56+32.5,'Q4':24+70+30+32.5}
B={'Q1':120+38+32.5,'Q2':40+57+84+32.5,'Q3':38+56+32.5,'Q4':57+70+30+32.5}
for n in ['Q1','Q2','Q3','Q4']:
    print(n, f"A {A[n]:.1f}h {A[n]/13:.1f}h/wk B {B[n]:.1f}h {B[n]/13:.1f}h/wk")
print('annual', f"A {sum(A.values()):.0f}h {sum(A.values())/52:.1f}h/wk B {sum(B.values()):.0f}h {sum(B.values())/52:.1f}h/wk")
EOF
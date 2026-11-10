#!/usr/bin/env python3
import json
M = json.load(open('model.json'))['scenarios']

def q(rows, n):
    return rows[n*3:(n+1)*3]

print('=== BASE QUARTERLY 2028 ===')
for n in range(4):
    rs = q(M['base']['rows28'], n)
    print(f"2028 Q{n+1}: loc {rs[-1]['loc']:.0f} pay {rs[-1]['paying']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} "
          f"cogs {sum(r['cogs'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} net {sum(r['net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")
print('=== BASE QUARTERLY 2029 ===')
for n in range(4):
    rs = q(M['base']['rows29'], n)
    print(f"2029 Q{n+1}: loc {rs[-1]['loc']:.0f} pay {rs[-1]['paying']:.0f} rev {sum(r['rev']+r['setup'] for r in rs):,.0f} "
          f"cogs {sum(r['cogs'] for r in rs):,.0f} opex {sum(r['opex'] for r in rs):,.0f} net {sum(r['net'] for r in rs):,.0f} cash {rs[-1]['cash']:,.0f}")

print('\n=== SCENARIO TABLE ===')
for k in ['base','slow','delay','delay_brakes','p45','p35','p25']:
    s=M[k]; y27=s['y27']; y28=s['y28']; y29=s['y29']
    print(f"{k:12s} 27rev {y27['rev']:>9,.0f} 27net {y27['net']:>9,.0f} trough {s['trough']['month']:>3s} {s['trough']['cash']:>8,.0f} "
          f"27cash {y27['cash']:>8,.0f} 28rev {y28['rev']:>9,.0f} 28net {y28['net']:>9,.0f} 28low {y28['low']:>8,.0f} "
          f"29rev {y29['rev']:>10,.0f} 29net {y29['net']:>9,.0f} 29low {y29['low']:>8,.0f} 27GM {y27['gm']*100:5.1f}")

print('\n=== BASE 2028 MONTHLY ===')
for r in M['base']['rows28']:
    print(f"{r['month']} loc {r['loc']:.0f} pay {r['paying']:.0f} rev {r['rev']+r['setup']:,.0f} cogs {r['cogs']:,.0f} opex {r['opex']:,.0f} net {r['net']:,.0f} cash {r['cash']:,.0f}")

print('\n=== 2027 COST LINES ===')
for r in M['base']['rows27']:
    print(f"{r['month']} infra {r['infra']:,.0f} pay {r['payments']:,.0f} support {r['support']:,.0f} opex {r['opex']:,.0f}")

print('\n=== 2028 COST LINES (Q1) ===')
for r in M['base']['rows28'][:3]:
    print(f"{r['month']} infra {r['infra']:,.0f} pay {r['payments']:,.0f} support {r['support']:,.0f} onboard {r['onboarding']:,.0f} opex {r['opex']:,.0f}")

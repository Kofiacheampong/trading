#!/usr/bin/env python3
"""Garnsh v2.1 — month-by-month cash model. Single source of truth for the
plan (docs) and the deck. COGS includes support + onboarding labour, so
reported gross margin is ~88% (not the flattering 95% software-only number).
"""
import json

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
INFRA_PER_LOC = 1.70
PAYMENT_PCT = 0.029

# ------------------------------------------------------------------ base 2027
LOC_2027   = [0,0,0,14,42,84,112,126,140,168,196,210]   # 1/3/6/8/9/10/12/14/15 groups x 14
ARPU_2027  = [0,0,0,48,50,52,55,57,61,61,61,61]
SETUP_2027 = [0,0,0,0,0,0,0,0,0,3000,3000,1500]   # 5 full-price groups, Oct-Dec
COGS_2027 = {                    # support contractor lands with the first big month
 'Support contractor': [0,0,0,0,0,0,0,0,0,1500,1500,1500],
}
OPEX_2027 = {
 'Design (milestone payments)': [1667,1667,1666,0,0,0,0,0,0,0,0,0],
 'Entity / legal / IP':         [2500,0,0,0,0,0,500,0,0,0,0,0],
 'Insurance (E&O, cyber)':      [0,1500,0,0,0,0,0,0,0,0,0,0],
 'Tools & SaaS':                [300,300,300,300,300,300,450,450,450,450,450,450],
 'Brand / site / demo':         [0,2000,0,0,0,0,0,0,0,0,0,0],
 'Travel & demos':              [0,0,800,800,800,800,0,0,1200,0,1200,0],
 'Toast certification':         [0,0,0,0,0,0,0,0,3000,0,0,0],
 'Marketing & content':         [0,0,0,0,0,150,150,150,150,150,150,150],
 'Admin & misc':                [150,150,150,150,150,150,150,150,150,150,150,150],
}

# 2028 drivers
LOC_2028 = [210]
for i in range(12): LOC_2028.append(LOC_2028[-1] + (36 if i < 11 else 34))
ARPU_2028 = [72,75,78,81,84,87,89,91,93,95,96,98]
SETUP_2028 = [3875]*12                       # 31 new groups x $1,500
COGS_2028 = {
 'Support contractor': [2500]*12,
 'Onboarding (2h/loc x $60)': [3720]*12,
}
OPEX_2028 = {
 'Founder draws (2 x $3K/mo)': [0]*6 + [6000]*6,
 'Engineer (from July)': [0]*6 + [9000]*6,
 'Growth hire (from Oct)': [0]*9 + [7500]*3,
 'Tools & SaaS': [800]*12,
 'Travel & demos': [1500]*12,
 'Marketing & content': [2000]*12,
 'Legal / insurance / admin': [1000]*12,
 'Contract design': [1000]*12,
}

# 2029 drivers
LOC_2029 = [640]
for i in range(12): LOC_2029.append(LOC_2029[-1] + (51 if i < 11 else 49))
ARPU_2029 = [100,102,104,106,108,110,112,114,115,116,117,118]
SETUP_2029 = [5750]*12                       # 46 new groups x $1,500
COGS_2029 = {
 'Support team (1.5 FTE)': [7500]*12,
 'Onboarding (2h/loc x $60)': [5500]*12,
}
OPEX_2029 = {
 'Founders (2 x $50K)': [8333]*12,
 'Engineers (2 x $115K)': [19166]*12,
 'Growth / account mgmt': [9167]*12,
 'Tools & SaaS': [1500]*12,
 'Travel & demos': [2500]*12,
 'Marketing & content': [5000]*12,
 'Legal / insurance / audit': [2083]*12,
 'Contract design': [2000]*12,
 'Admin & misc': [1500]*12,
}

def run(prev_loc, loc, arpu, setup, cogs_lines, opex_lines):
    sub = (prev_loc + loc)/2 * arpu
    rev = sub + setup
    infra = (prev_loc + loc)/2 * INFRA_PER_LOC
    payments = rev * PAYMENT_PCT
    cogs = infra + payments + sum(v for v in cogs_lines.values())
    opex = sum(v for v in opex_lines.values())
    return dict(sub=sub, setup=setup, rev=rev, infra=infra, payments=payments,
                cogs=cogs, opex=opex, cost=cogs+opex, gp=rev-cogs, net=rev-cogs-opex)

def year(start_cash, locs_prev, locs, arpus, setups, cogs_by_month, opex_by_month):
    rows, cash = [], start_cash
    for i in range(12):
        r = run(locs_prev[i], locs[i], arpus[i], setups[i],
                {k: v[i] for k, v in cogs_by_month.items()},
                {k: v[i] for k, v in opex_by_month.items()})
        cash += r['net']
        r.update(month=MONTHS[i], loc=locs[i], arpu=arpus[i], cash=cash)
        rows.append(r)
    return rows

rows27 = year(20000.0, [0]+LOC_2027[:-1], LOC_2027, ARPU_2027, SETUP_2027, COGS_2027, OPEX_2027)
rows28 = year(rows27[-1]['cash'], LOC_2028[:-1], LOC_2028[1:], ARPU_2028, SETUP_2028, COGS_2028, OPEX_2028)
rows29 = year(rows28[-1]['cash'], LOC_2029[:-1], LOC_2029[1:], ARPU_2029, SETUP_2029, COGS_2029, OPEX_2029)

def yr(rows):
    return dict(rev=sum(r['rev'] for r in rows), cogs=sum(r['cogs'] for r in rows),
                gp=sum(r['gp'] for r in rows), opex=sum(r['opex'] for r in rows),
                cost=sum(r['cost'] for r in rows), net=sum(r['net'] for r in rows),
                loc=rows[-1]['loc'], exit_mrr=rows[-1]['loc']*rows[-1]['arpu'],
                cash=rows[-1]['cash'], low=min(r['cash'] for r in rows),
                gm=sum(r['gp'] for r in rows)/sum(r['rev'] for r in rows),
                setup=sum(r['setup'] for r in rows))

y27, y28, y29 = yr(rows27), yr(rows28), yr(rows29)

# ------------------------------------------------------------------ conservative
C_LOC_2027  = [0,0,0,4,10,20,30,40,48,54,58,60]
C_ARPU_2027 = [0,0,0,45,45,45,48,48,48,48,48,48]
C_SETUP_2027 = [0,0,0,0,0,1500,0,0,1500,0,0,1500]
C_COGS_2027 = {'Support contractor': [0]*9 + [800]*3}
C_OPEX_2027 = {
 'Legal / entity': [2500,0,0,0,0,0,0,0,0,0,0,0],
 'Design (milestones)': [1000,1000,1000,0,0,0,0,0,0,0,0,0],
 'Insurance': [0,1200,0,0,0,0,0,0,0,0,0,0],
 'Tools & SaaS': [250]*12,
 'Brand / site': [1000,0,0,0,0,0,0,0,0,0,0,0],
 'Travel & demos': [0,500,500,500,500,500,0,0,0,0,0,0],
 'Admin & misc': [150]*12,
}
c27 = year(20000.0, [0]+C_LOC_2027[:-1], C_LOC_2027, C_ARPU_2027, C_SETUP_2027, C_COGS_2027, C_OPEX_2027)

C_LOC_2028 = [60]
for i in range(12): C_LOC_2028.append(C_LOC_2028[-1] + (23 if i < 11 else 21))
C_ARPU_2028 = [48]*12
c28 = year(c27[-1]['cash'], C_LOC_2028[:-1], C_LOC_2028[1:], C_ARPU_2028, [1000]*12,
  {'Support contractor': [2000]*12},
  {'Founders (2 x $30K)': [5000]*12, 'Tools & SaaS': [500]*12, 'Travel & demos': [300]*12,
   'Marketing & content': [200]*12, 'Legal / insurance / admin': [400]*12, 'Contract design': [300]*12})

C_LOC_2029 = [320]
for i in range(12): C_LOC_2029.append(C_LOC_2029[-1] + (49 if i < 11 else 45))
C_ARPU_2029 = [61]*12
c29 = year(c28[-1]['cash'], C_LOC_2029[:-1], C_LOC_2029[1:], C_ARPU_2029, [0]*12,
  {'Support / CS (1 FTE)': [4583]*12},
  {'Founders (2 x $60K)': [10000]*12, 'Tools & SaaS': [700]*12, 'Travel & demos': [400]*12,
   'Marketing & content': [500]*12, 'Legal / insurance / admin': [500]*12, 'Contract design': [300]*12})

cy27, cy28, cy29 = yr(c27), yr(c28), yr(c29)

# ------------------------------------------------------------------ unit economics
ATT = {2027: (0.05, 0.00, 0.000), 2028: (0.55, 0.17, 0.000), 2029: (0.65, 0.28, 0.035)}
ue = {y: 59 + 40*b + 99*o + 149*a for y, (b, o, a) in ATT.items()}
GM = {2027: y27['gm'], 2028: y28['gm'], 2029: y29['gm']}
CHURN_M, CHURN_S = 0.015, 0.035
CAC_M, CAC_S = 1200, 150
# LTV uses RECURRING gross margin (excludes one-time onboarding labour)
ONBOARD_2028 = 44640.0
ONBOARD_2029 = 66000.0
REC_GM = {2027: (y27['rev']-y27['cogs'])/y27['rev'],
          2028: (y28['rev']-(y28['cogs']-ONBOARD_2028))/y28['rev'],
          2029: (y29['rev']-(y29['cogs']-ONBOARD_2029))/y29['rev']}
ltv_m = ue[2028]*REC_GM[2028]/CHURN_M
ltv_s = 59*REC_GM[2028]/CHURN_S
onb_cost_per_brand = 12*3*60               # 12 locations x 3 h x $60 fully-loaded
setup_fee = 1500

out = dict(base=dict(rows27=rows27, rows28=rows28, rows29=rows29, y27=y27, y28=y28, y29=y29,
                     trough=min(rows27, key=lambda r: r['cash']),
                     first_positive=next(r['month'] for r in rows27 if r['net'] > 0),
                     capital_back=next(r['month'] for r in rows27 if r['cash'] >= 20000)),
           cons=dict(rows27=c27, rows28=c28, rows29=c29, y27=cy27, y28=cy28, y29=cy29,
                     trough=min(c27, key=lambda r: r['cash'])),
           unit=dict(arpu=ue, gm=GM, rec_gm=REC_GM, ltv_multi=ltv_m, ltv_single=ltv_s,
                     cac_multi=CAC_M, cac_single=CAC_S,
                     payback_multi=(CAC_M+120)/(ue[2028]*REC_GM[2028]),
                     payback_single=(CAC_S+120)/(59*REC_GM[2028]),
                     ltv_cac_multi=ltv_m/CAC_M, ltv_cac_single=ltv_s/CAC_S,
                     onboarding_per_brand=onb_cost_per_brand, setup_fee=setup_fee,
                     setup_gap=setup_fee-onb_cost_per_brand))
json.dump(out, open('model.json','w'), indent=1)

print('=== BASE 2027 MONTHLY ===')
print('| Month | Locations | Revenue | COGS | Gross profit | Opex | Net | Cash |')
print('|---|---|---|---|---|---|---|---|')
for r in rows27:
    print(f"| {r['month']} | {r['loc']} | ${r['rev']:,.0f} | ${r['cogs']:,.0f} | ${r['gp']:,.0f} | ${r['opex']:,.0f} | ${r['net']:,.0f} | ${r['cash']:,.0f} |")
print('\n| | 2027 | 2028 | 2029 |')
print('|---|---|---|---|')
for k, lab in [('loc','Locations (end)'), ('rev','Revenue'), ('cogs','COGS (incl. support)'), ('gp','Gross profit'),
               ('opex','Operating costs'), ('net','Operating result'), ('exit_mrr','Exit MRR'), ('cash','Year-end cash')]:
    print(f"| {lab} | ${y27[k]:,.0f} | ${y28[k]:,.0f} | ${y29[k]:,.0f} |" if k not in ('loc',) else f"| {lab} | {y27[k]:,.0f} | {y28[k]:,.0f} | {y29[k]:,.0f} |")
print(f"\nGM: {GM[2027]*100:.1f}% / {GM[2028]*100:.1f}% / {GM[2029]*100:.1f}%")
print(f"2027 trough: {out['base']['trough']['month']} ${out['base']['trough']['cash']:,.0f}; first positive month {out['base']['first_positive']}; capital back {out['base']['capital_back']}")
print(f"Cash floor 2028 ${y28['low']:,.0f} · 2029 ${y29['low']:,.0f}")
print(f"ARPU build ${ue[2027]:.0f} / ${ue[2028]:.0f} / ${ue[2029]:.0f}")
print(f"LTV multi ${ltv_m:,.0f} (CAC ${CAC_M}, {out['unit']['payback_multi']:.1f} mo payback, {ltv_m/CAC_M:.1f}x)")
print(f"LTV single ${ltv_s:,.0f} (CAC ${CAC_S}, {out['unit']['payback_single']:.1f} mo payback, {ltv_s/CAC_S:.1f}x)")
print(f"Onboarding/brand ${onb_cost_per_brand:,.0f} vs setup ${setup_fee:,} → gap ${setup_fee-onb_cost_per_brand:,.0f}")
print('\n=== CONSERVATIVE ===')
for lab, y in [('2027',cy27),('2028',cy28),('2029',cy29)]:
    print(f"{lab}: rev ${y['rev']:,.0f} · cost ${y['cost']:,.0f} · net ${y['net']:,.0f} · loc {y['loc']} · exit MRR ${y['exit_mrr']:,.0f} · cash ${y['cash']:,.0f} · GM {y['gm']*100:.0f}%")
print(f"Trough: {out['cons']['trough']['month']} ${out['cons']['trough']['cash']:,.0f}")

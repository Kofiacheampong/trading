#!/usr/bin/env python3
"""Garnsh v2.3 — cohort-level monthly cash model (36 months, Jan 2027-Dec 2029).

Why cohort-level: v2.2's 2027 revenue line assumed every live location paid
list price. The plan actually sells 20% showcase pricing to six groups, gives
four design partners a free year, and waives setup for all ten. A per-group
schedule has to drive the revenue line, not a blended ARPU path.

Price build (list): core $59 + boards $40 x attach. Boards attach ramps
5% (2027) -> 55% (Dec 2028) -> 65% (Dec 2029); ordering $99 x attach ramps
0 -> 17% (Dec 2028) -> 28% (Dec 2029); app $149 x 0 -> 3.5% (Dec 2029).

Setup is $1,500 per 14-location group for full-price groups only; showcase
and design cohorts pay no setup. Design partners are free for 12 months from
go-live, then convert at list. Showcase pricing is 20% off core for 12 months
from go-live, then list.

COGS includes support + onboarding labour, so gross margin is fully loaded.
"""
import json

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
INFRA = 1.70
PAY = 0.029
CORE = 59.0
BOARDS = 40.0
ORDERING = 99.0
APP = 149.0
SETUP = 1500.0
SHOWCASE_DISC = 0.20
FREE_MONTHS = 12
LOC_PER_GROUP = 14.0

# ---------------------------------------------------------------- attach ramps
def b_attach(m):            # menu boards
    if m < 12: return 0.05
    if m < 24: return 0.05 + 0.50 * (m - 12) / 11
    return 0.55 + 0.10 * (m - 24) / 11

def o_attach(m):            # Gen 2 ordering
    if m < 12: return 0.0
    if m < 24: return 0.17 * (m - 12) / 11
    return 0.17 + 0.11 * (m - 24) / 11

def a_attach(m):            # Gen 3 app
    if m < 24: return 0.0
    return 0.035 * (m - 24) / 11

# ---------------------------------------------------------------- cohorts
def C(kind, loc, start):
    return dict(kind=kind, loc=float(loc), start=int(start))

BASE_2027 = [
    C('showcase', 14, 3),                       # S1 Apr
    C('showcase', 14, 4), C('showcase', 14, 4), # S2-S3 May
    C('showcase', 14, 5), C('showcase', 14, 5), C('showcase', 14, 5),  # S4-S6 Jun
    C('design',   14, 6), C('design',   14, 6), # D1-D2 Jul
    C('design',   14, 7),                       # D3 Aug
    C('design',   14, 8),                       # D4 Sep
    C('full', 14, 9), C('full', 14, 9),         # F1-F2 Oct
    C('full', 14, 10), C('full', 14, 10),       # F3-F4 Nov
    C('full', 14, 11),                          # F5 Dec
]

SLOW_2027 = [
    C('showcase', 14, 3),                       # S1 Apr
    C('showcase', 14, 5), C('showcase', 14, 5), # S2-S3 Jun (3 live by Jun)
    C('showcase', 14, 7), C('showcase', 14, 7), C('showcase', 14, 7),  # S4-S6 Aug
    C('design',   14, 8), C('design',   14, 8), # D1-D2 Sep
    C('design',   14, 9), C('design',   14, 9), # D3-D4 Oct
    C('full', 14, 10), C('full', 14, 10),       # F1-F2 Nov
    C('full', 14, 11), C('full', 14, 11), C('full', 14, 11),  # F3-F5 Dec
]

def shift(cohorts, months):
    return [C(c['kind'], c['loc'], c['start'] + months) for c in cohorts
            if c['start'] + months <= 11]

# ---------------------------------------------------------------- revenue
def price_per_loc(c, m, core):
    age = m - c['start']
    if age < 0:
        return 0.0
    if c['kind'] == 'design' and age < FREE_MONTHS:
        return 0.0
    if c['kind'] == 'showcase' and age < FREE_MONTHS:
        base = core * (1 - SHOWCASE_DISC)
    else:
        base = core
    return base + BOARDS * b_attach(m) + ORDERING * o_attach(m) + APP * a_attach(m)

def month_rev(cohorts, m, core):
    rev = setup = 0.0
    live = pay = 0.0
    for c in cohorts:
        age = m - c['start']
        if age < 0:
            continue
        live += c['loc']
        p = price_per_loc(c, m, core)
        if p > 0:
            pay += c['loc']
        rev += c['loc'] * p * (0.5 if age == 0 else 1.0)
        if age == 0 and c['kind'] in ('full', 'new'):
            setup += (c['loc'] / LOC_PER_GROUP) * SETUP
    return rev, setup, live, pay

# ---------------------------------------------------------------- opex
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
OPEX_2028 = {
 'Founder draws (2 x $3K/mo)':  [0]*6 + [6000]*6,
 'Engineer (from July)':        [0]*6 + [9000]*6,
 'Growth hire (from Oct)':      [0]*9 + [7500]*3,
 'Tools & SaaS':                [800]*12,
 'Travel & demos':              [1500]*12,
 'Marketing & content':         [2000]*12,
 'Legal / insurance / admin':   [1000]*12,
 'Contract design':             [1000]*12,
}
OPEX_2029 = {
 'Founders (2 x $50K)':         [8333]*12,
 'Engineers (2 x $115K)':       [19166]*12,
 'Growth / account mgmt':       [9167]*12,
 'Tools & SaaS':                [1500]*12,
 'Travel & demos':              [2500]*12,
 'Marketing & content':         [5000]*12,
 'Legal / insurance / audit':   [2083]*12,
 'Contract design':             [2000]*12,
 'Admin & misc':                [1500]*12,
}

def build_2028(start=12, loc_per_month=36, last=34):
    return [C('new', loc_per_month, start + i) for i in range(11)] + [C('new', last, start + 11)]

def build_2029(start=24, loc_per_month=51, last=49):
    return [C('new', loc_per_month, start + i) for i in range(11)] + [C('new', last, start + 11)]

# ---------------------------------------------------------------- year runner
def run_year(cohorts, start_cash, opex_by_month, support_by_month,
             onboarding_by_month=None, core=CORE, prev_live=0.0, offset=0):
    rows, cash = [], start_cash
    for i, mon in enumerate(MONTHS):
        m = offset + i
        rev, setup, live_end, pay = month_rev(cohorts, m, core)
        avg_live = (prev_live + live_end) / 2
        infra = avg_live * INFRA
        payments = (rev + setup) * PAY
        support = support_by_month[i]
        onboarding = onboarding_by_month[i] if onboarding_by_month else 0.0
        cogs = infra + payments + support + onboarding
        opex = sum(v[i] for v in opex_by_month.values())
        net = rev + setup - cogs - opex
        cash += net
        rows.append(dict(month=mon, rev=rev, sub=rev, setup=setup, loc=live_end,
                         paying=pay, avg_loc=avg_live, infra=infra, payments=payments,
                         support=support, onboarding=onboarding, cogs=cogs,
                         opex=opex, net=net, cash=cash))
        prev_live = live_end
    return rows

def support_sched(cohorts, amount=1500.0, threshold=150):
    """First month end-of-month live locations reach the support threshold."""
    live = 0.0
    out = []
    for m in range(12):
        _, _, live, _ = month_rev(cohorts, m, CORE)
        out.append(amount if live >= threshold else 0.0)
    return out

def run_all(g27, core=CORE, start_cash=20000.0, opex27=None):
    sched27 = support_sched(g27)
    rows27 = run_year(g27, start_cash, opex27 or OPEX_2027, sched27, core=core, offset=0)
    prev = rows27[-1]['loc']
    g28 = g27 + build_2028()
    onb28 = [120.0 * sum(c['loc'] for c in g28 if c['start'] == 12 + i) for i in range(12)]
    rows28 = run_year(g28, rows27[-1]['cash'], OPEX_2028, [2500.0]*12, onb28,
                      core=core, prev_live=rows27[-1]['loc'], offset=12)
    prev = rows28[-1]['loc']
    g29 = g28 + build_2029()
    onb29 = [120.0 * sum(c['loc'] for c in g29 if c['start'] == 24 + i) for i in range(12)]
    rows29 = run_year(g29, rows28[-1]['cash'], OPEX_2029, [7500.0]*12, onb29,
                      core=core, prev_live=rows28[-1]['loc'], offset=24)
    return rows27, rows28, rows29

def yr(rows):
    rev = sum(r['rev'] + r['setup'] for r in rows)
    sub = sum(r['sub'] for r in rows)
    setup = sum(r['setup'] for r in rows)
    cogs = sum(r['cogs'] for r in rows)
    opex = sum(r['opex'] for r in rows)
    return dict(rev=rev, sub=sub, setup=setup, cogs=cogs, gp=rev - cogs, opex=opex,
                net=rev - cogs - opex, loc=rows[-1]['loc'], pay=rows[-1]['paying'],
                exit_mrr=rows[-1]['sub'], cash=rows[-1]['cash'],
                low=min(r['cash'] for r in rows), gm=(rev - cogs) / rev if rev else 0)

def trough(rows):
    return min(rows, key=lambda r: r['cash'])

def first_positive(rows):
    for r in rows:
        if r['net'] > 0:
            return r['month']
    return None

def capital_back(rows, target=20000.0):
    for r in rows:
        if r['cash'] >= target:
            return r['month']
    return None

# ---------------------------------------------------------------- scenarios
SCEN = {}
for name, sched, core in [
        ('base', BASE_2027, CORE),
        ('delay', shift(BASE_2027, 2), CORE),
        ('slow', SLOW_2027, CORE),
        ('p45', BASE_2027, 45.0),
        ('p35', BASE_2027, 35.0),
        ('p25', BASE_2027, 25.0)]:
    r27, r28, r29 = run_all(sched, core=core)
    SCEN[name] = dict(rows27=r27, rows28=r28, rows29=r29,
                      y27=yr(r27), y28=yr(r28), y29=yr(r29),
                      trough=trough(r27), first_positive=first_positive(r27),
                      capital_back=capital_back(r27))

# Delay + brakes: if nothing is live by 1 May, freeze travel/demos Apr-Jun and
# move Toast certification out of 2027. This is the delay protocol, not a new plan.
import copy
OPEX_DELAY_BRAKES = copy.deepcopy(OPEX_2027)
OPEX_DELAY_BRAKES['Travel & demos'] = [0, 0, 0, 0, 0, 0, 0, 0, 1200, 0, 1200, 0]
OPEX_DELAY_BRAKES['Toast certification'] = [0] * 12
for nm, sch in [('delay_brakes', shift(BASE_2027, 2))]:
    r27, r28, r29 = run_all(sch, core=CORE, opex27=OPEX_DELAY_BRAKES)
    SCEN[nm] = dict(rows27=r27, rows28=r28, rows29=r29,
                    y27=yr(r27), y28=yr(r28), y29=yr(r29),
                    trough=trough(r27), first_positive=first_positive(r27),
                    capital_back=capital_back(r27))

out = dict(scenarios=SCEN)
json.dump(out, open('model.json', 'w'), indent=1)

def table27(rows):
    print('| Month | Live loc | Paying loc | Revenue | COGS | Gross profit | Operating costs | Net | Cash |')
    print('|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        print(f"| {r['month']} | {r['loc']:.0f} | {r['paying']:.0f} | ${r['rev']+r['setup']:,.0f} | ${r['cogs']:,.0f} | ${r['rev']+r['setup']-r['cogs']:,.0f} | ${r['opex']:,.0f} | ${r['net']:,.0f} | ${r['cash']:,.0f} |")

def summary(name):
    s = SCEN[name]
    print(f"\n=== {name.upper()} ===")
    y27, y28, y29 = s['y27'], s['y28'], s['y29']
    print(f"2027 rev ${y27['rev']:,.0f} (sub ${y27['sub']:,.0f} + setup ${y27['setup']:,.0f}) cogs ${y27['cogs']:,.0f} gp ${y27['gp']:,.0f} opex ${y27['opex']:,.0f} net ${y27['net']:,.0f} GM {y27['gm']*100:.1f}%")
    print(f"2027 end loc {y27['loc']:.0f} paying {y27['pay']:.0f} exit MRR ${y27['exit_mrr']:,.0f} cash ${y27['cash']:,.0f} trough {s['trough']['month']} ${s['trough']['cash']:,.0f} first+ {s['first_positive']} capback {s['capital_back']}")
    print(f"2028 rev ${y28['rev']:,.0f} net ${y28['net']:,.0f} GM {y28['gm']*100:.1f}% end loc {y28['loc']:.0f} exitMRR ${y28['exit_mrr']:,.0f} cash ${y28['cash']:,.0f} low ${y28['low']:,.0f}")
    print(f"2029 rev ${y29['rev']:,.0f} net ${y29['net']:,.0f} GM {y29['gm']*100:.1f}% end loc {y29['loc']:.0f} exitMRR ${y29['exit_mrr']:,.0f} cash ${y29['cash']:,.0f} low ${y29['low']:,.0f}")

for n in ['base','delay','slow','delay_brakes','p45','p35','p25']:
    summary(n)

print('\n=== BASE 2027 MONTHLY ===')
table27(SCEN['base']['rows27'])
print('\n=== DELAY 2027 MONTHLY ===')
table27(SCEN['delay']['rows27'])
print('\n=== SLOW 2027 MONTHLY ===')
table27(SCEN['slow']['rows27'])

# per-group schedule for the doc
print('\n=== PER-GROUP 2027 SCHEDULE (base) ===')
print('| Group | Type | Locations | Go-live | Price / loc / mo | Setup | 2027 revenue |')
print('|---|---|---|---|---|---|---|')
labels = ['S1','S2','S3','S4','S5','S6','D1','D2','D3','D4','F1','F2','F3','F4','F5']
tot = 0
for lab, c in zip(labels, BASE_2027):
    rev = 0
    for m in range(12):
        age = m - c['start']
        if age < 0: continue
        rev += c['loc'] * price_per_loc(c, m, CORE) * (0.5 if age == 0 else 1.0)
    setup = (c['loc']/LOC_PER_GROUP)*SETUP if c['kind'] == 'full' else 0
    p = price_per_loc(c, c['start'], CORE)
    tot += rev + setup
    print(f"| {lab} | {c['kind']} | {c['loc']:.0f} | {MONTHS[c['start']]} | ${p:.2f} | ${setup:,.0f} | ${rev+setup:,.0f} |")
print(f"| **Total** | | **210** | | | **$7,500** | **${tot:,.0f}** |")

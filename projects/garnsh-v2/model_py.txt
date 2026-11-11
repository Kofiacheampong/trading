#!/usr/bin/env python3
"""Garnsh v2.4 — parameterised cohort model (36 months, Jan 2027-Dec 2029).

Scenario knobs: average group size, 2027 go-live schedule, core price,
support-contractor cost, 2028 MRR gates, delay protocol, Toast-denies-ordering
revenue-line removal, and Gen 2 ordering delay after a certification slip.

Units: groups, not locations. Locations = groups x group_size. Setup is
$1,500 per group; onboarding labour is 2h/location at $60/h. COGS includes
support and onboarding, so gross margin is fully loaded.
"""
import json, copy

MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
INFRA = 1.70
PAY = 0.029
CORE = 59.0
BOARDS = 40.0
ORDERING = 99.0
APP = 149.0
SETUP = 1500.0
DISC = 0.20
FREE = 12
SUPPORT = 2500.0

def b(m):
    if m < 12: return 0.05
    if m < 24: return 0.05 + 0.50 * (m - 12) / 11
    return 0.55 + 0.10 * (m - 24) / 11

def o(m):
    if m < 12: return 0.0
    if m < 24: return 0.17 * (m - 12) / 11
    return 0.17 + 0.11 * (m - 24) / 11

def a(m):
    if m < 24: return 0.0
    return 0.035 * (m - 24) / 11

# ---------------------------------------------------------------- schedules
BASE_2027 = [
    ('showcase', 3, 1), ('showcase', 4, 2), ('showcase', 5, 3),
    ('design', 6, 2), ('design', 7, 1), ('design', 8, 1),
    ('full', 9, 2), ('full', 10, 2), ('full', 11, 1),
]
SLOW_2027 = [
    ('showcase', 3, 1), ('showcase', 5, 2), ('showcase', 7, 3),
    ('design', 8, 2), ('design', 9, 2),
    ('full', 10, 2), ('full', 11, 3),
]
CLOSE6_2027 = [
    ('showcase', 3, 1), ('showcase', 4, 2), ('showcase', 5, 1), ('showcase', 6, 2),
    ('design', 7, 2), ('design', 8, 2),
    ('full', 9, 2), ('full', 10, 2), ('full', 11, 1),
]
C6SLOW_2027 = [
    ('showcase', 3, 1), ('showcase', 5, 2), ('showcase', 6, 1), ('showcase', 7, 2),
    ('design', 8, 2), ('design', 9, 2),
    ('full', 10, 2), ('full', 11, 1),
]

def shift(schedule, months):
    out = []
    for kind, start, groups in schedule:
        if start + months <= 11:
            out.append((kind, start + months, groups))
    return out

def cohorts_from(schedule, group_size):
    return [dict(kind=k, start=s, groups=g, loc=g * group_size) for k, s, g in schedule]

def add_groups(start_groups, target, year_start):
    n = target - start_groups
    base, rem = divmod(n, 12)
    out = []
    for i in range(12):
        g = base + (1 if i < rem else 0)
        if g > 0:
            out.append(dict(kind='new', start=year_start + i, groups=g, loc=0))
    return out

# ---------------------------------------------------------------- revenue
def price_per_loc(c, m, core, ord_delay=0, remove_ordering=False, remove_app=False):
    age = m - c['start']
    if age < 0:
        return 0.0
    if c['kind'] == 'design' and age < FREE:
        return 0.0
    base = core * (1 - DISC) if (c['kind'] == 'showcase' and age < FREE) else core
    ordering = 0.0 if remove_ordering else ORDERING * o(m - ord_delay)
    app = 0.0 if remove_app else APP * a(m)
    return base + BOARDS * b(m) + ordering + app

def month_rev(cohorts, m, core, group_size, ord_delay=0,
              remove_ordering=False, remove_app=False):
    rev = setup = 0.0
    live = pay = 0.0
    for c in cohorts:
        age = m - c['start']
        if age < 0:
            continue
        loc = c['groups'] * group_size
        live += loc
        p = price_per_loc(c, m, core, ord_delay, remove_ordering, remove_app)
        if p > 0:
            pay += loc
        rev += loc * p * (0.5 if age == 0 else 1.0)
        if age == 0 and c['kind'] in ('full', 'new'):
            setup += c['groups'] * SETUP
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

def opex_2027(protocol=False):
    o = copy.deepcopy(OPEX_2027)
    if protocol:
        o['Travel & demos'] = [0, 0, 800, 0, 0, 0, 0, 0, 1200, 0, 1200, 0]
        o['Toast certification'] = [0] * 12
    return o

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

# ---------------------------------------------------------------- runners
def support_2027(rows_live):
    out = []
    for live in rows_live:
        out.append(SUPPORT if live >= 150 else 0.0)
    return out

def run_year(cohorts, start_cash, opex_by_month, support_by_month,
             onboarding_by_month=None, core=CORE, group_size=14,
             prev_live=0.0, offset=0, ord_delay=0,
             remove_ordering=False, remove_app=False):
    rows, cash = [], start_cash
    for i, mon in enumerate(MONTHS):
        m = offset + i
        rev, setup, live_end, pay = month_rev(cohorts, m, core, group_size,
                                              ord_delay, remove_ordering, remove_app)
        avg_live = (prev_live + live_end) / 2
        infra = avg_live * INFRA
        payments = (rev + setup) * PAY
        support = support_by_month[i]
        onboarding = onboarding_by_month[i] if onboarding_by_month else 0.0
        cogs = infra + payments + support + onboarding
        opex = sum(v[i] for v in opex_by_month.values()) if opex_by_month else 0.0
        net = rev + setup - cogs - opex
        cash += net
        rows.append(dict(month=mon, rev=rev, setup=setup, loc=live_end, paying=pay,
                         avg_loc=avg_live, infra=infra, payments=payments,
                         support=support, onboarding=onboarding, cogs=cogs,
                         opex=opex, net=net, cash=cash))
        prev_live = live_end
    return rows

def total_groups(cohorts):
    return sum(c['groups'] for c in cohorts)

def build_2028(cohorts27, group_size, target=46):
    start_groups = total_groups(cohorts27)
    new = add_groups(start_groups, target, 12)
    for c in new:
        c['loc'] = c['groups'] * group_size
    return cohorts27 + new

def build_2029(cohorts28, group_size, target=92):
    start_groups = total_groups(cohorts28)
    new = add_groups(start_groups, target, 24)
    for c in new:
        c['loc'] = c['groups'] * group_size
    return cohorts28 + new

def opex_2028_gated(cohorts, group_size, core, ord_delay=0,
                    remove_ordering=False, remove_app=False):
    # precompute subscription MRR by month
    subs = []
    for i in range(12):
        rev, _, _, _ = month_rev(cohorts, 12 + i, core, group_size,
                                 ord_delay, remove_ordering, remove_app)
        subs.append(rev)
    def active_from(threshold):
        for i, v in enumerate(subs):
            if v >= threshold:
                return i + 1  # month after crossing
        return 99
    t = active_from(15000)
    mkt = active_from(25000)
    design = active_from(35000)
    lines = {
      'Founder draws (2 x $3K/mo)': [0]*6 + [6000]*6,
      'Engineer (from July)':       [0]*6 + [9000]*6,
      'Growth hire (from Oct)':     [0]*9 + [7500]*3,
      'Tools & SaaS':               [800]*12,
      'Legal / insurance / admin':  [1000]*12,
      'Travel & demos':             [1500 if i >= t else 0 for i in range(12)],
      'Marketing & content':        [2000 if i >= mkt else 0 for i in range(12)],
      'Contract design':            [1000 if i >= design else 0 for i in range(12)],
    }
    return lines, subs, dict(travel=t, marketing=mkt, design=design)

def run_all(schedule, group_size=14, core=CORE, protocol=False,
            ord_delay=0, remove_ordering=False, remove_app=False,
            start_cash=20000.0, target28=46, target29=92):
    c27 = cohorts_from(schedule, group_size)
    r27 = run_year(c27, start_cash, opex_2027(protocol),
                   support_2027([month_rev(c27, m, core, group_size)[2] for m in range(12)]),
                   core=core, group_size=group_size, offset=0,
                   remove_ordering=remove_ordering, remove_app=remove_app)
    c28 = build_2028(c27, group_size, target28)
    o28, subs, gates = opex_2028_gated(c28, group_size, core, ord_delay,
                                       remove_ordering, remove_app)
    live28 = [month_rev(c28, 12 + i, core, group_size, ord_delay,
                        remove_ordering, remove_app)[2] for i in range(12)]
    sup28 = [SUPPORT if l >= 150 else 0.0 for l in live28]
    onb28 = [120.0 * sum(c['groups'] * group_size for c in c28 if c['start'] == 12 + i)
             for i in range(12)]
    r28 = run_year(c28, r27[-1]['cash'], o28, sup28, onb28, core=core,
                   group_size=group_size, prev_live=r27[-1]['loc'], offset=12,
                   ord_delay=ord_delay, remove_ordering=remove_ordering,
                   remove_app=remove_app)
    c29 = build_2029(c28, group_size, target29)
    live29 = [month_rev(c29, 24 + i, core, group_size, ord_delay,
                        remove_ordering, remove_app)[2] for i in range(12)]
    onb29 = [120.0 * sum(c['groups'] * group_size for c in c29 if c['start'] == 24 + i)
             for i in range(12)]
    r29 = run_year(c29, r28[-1]['cash'], OPEX_2029, [7500.0]*12, onb29,
                   core=core, group_size=group_size, prev_live=r28[-1]['loc'],
                   offset=24, ord_delay=ord_delay,
                   remove_ordering=remove_ordering, remove_app=remove_app)
    return dict(rows27=r27, rows28=r28, rows29=r29, gates=gates, subs28=subs,
                groups27=total_groups(c27), groups28=total_groups(c28), groups29=total_groups(c29))

def yr(rows):
    rev = sum(r['rev'] + r['setup'] for r in rows)
    sub = sum(r['rev'] for r in rows)
    setup = sum(r['setup'] for r in rows)
    cogs = sum(r['cogs'] for r in rows)
    opex = sum(r['opex'] for r in rows)
    return dict(rev=rev, sub=sub, setup=setup, cogs=cogs, gp=rev-cogs, opex=opex,
                net=rev-cogs-opex, loc=rows[-1]['loc'], pay=rows[-1]['paying'],
                exit_mrr=rows[-1]['rev'], cash=rows[-1]['cash'],
                low=min(r['cash'] for r in rows), gm=(rev-cogs)/rev if rev else 0)

def summary(res):
    y27, y28, y29 = yr(res['rows27']), yr(res['rows28']), yr(res['rows29'])
    tr = min(res['rows27'], key=lambda r: r['cash'])
    return dict(y27=y27, y28=y28, y29=y29, trough=tr, gates=res['gates'],
                groups27=res['groups27'], groups28=res['groups28'],
                groups29=res['groups29'])

SCEN = {}
for name, kw in [
    ('base', dict(schedule=BASE_2027)),
    ('delay', dict(schedule=shift(BASE_2027, 2))),
    ('delay_protocol', dict(schedule=shift(BASE_2027, 2), protocol=True, ord_delay=6)),
    ('slow', dict(schedule=SLOW_2027)),
    ('g10', dict(schedule=BASE_2027, group_size=10)),
    ('c6', dict(schedule=CLOSE6_2027)),
    ('g10_slow', dict(schedule=SLOW_2027, group_size=10)),
    ('c6_slow', dict(schedule=C6SLOW_2027)),
    ('toast_denies', dict(schedule=BASE_2027, remove_ordering=True)),
    ('toast_denies_app', dict(schedule=BASE_2027, remove_ordering=True, remove_app=True)),
    ('p45', dict(schedule=BASE_2027, core=45.0)),
    ('p35', dict(schedule=BASE_2027, core=35.0)),
    ('p25', dict(schedule=BASE_2027, core=25.0)),
]:
    res = run_all(**kw)
    SCEN[name] = dict(res=res, **summary(res))

json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'res'} for k, v in SCEN.items()},
          open('model.json', 'w'), indent=1)
json.dump({k: v['res'] for k, v in SCEN.items()}, open('model_rows.json', 'w'), indent=1)

print('=== SCENARIOS ===')
for k, s in SCEN.items():
    y27, y28, y29 = s['y27'], s['y28'], s['y29']
    print(f"{k:18s} 27rev {y27['rev']:>9,.0f} 27net {y27['net']:>9,.0f} tr {s['trough']['month']:>3s} {s['trough']['cash']:>8,.0f} "
          f"27cash {y27['cash']:>8,.0f} | 28rev {y28['rev']:>9,.0f} 28net {y28['net']:>9,.0f} 28low {y28['low']:>8,.0f} "
          f"| 29rev {y29['rev']:>10,.0f} 29net {y29['net']:>9,.0f} 29low {y29['low']:>8,.0f} | gates {s['gates']}")

print('\n=== BASE 2027 ===')
for r in SCEN['base']['res']['rows27']:
    print(f"{r['month']} loc {r['loc']:.0f} pay {r['paying']:.0f} rev {r['rev']+r['setup']:,.0f} cogs {r['cogs']:,.0f} opex {r['opex']:,.0f} net {r['net']:,.0f} cash {r['cash']:,.0f}")
print('\n=== BASE 2028 ===')
for r in SCEN['base']['res']['rows28']:
    print(f"{r['month']} loc {r['loc']:.0f} pay {r['paying']:.0f} rev {r['rev']+r['setup']:,.0f} cogs {r['cogs']:,.0f} opex {r['opex']:,.0f} net {r['net']:,.0f} cash {r['cash']:,.0f}")
print('\n=== DELAY 2028 (no protocol) ===')
for r in SCEN['delay']['res']['rows28']:
    print(f"{r['month']} rev {r['rev']+r['setup']:,.0f} cogs {r['cogs']:,.0f} opex {r['opex']:,.0f} net {r['net']:,.0f} cash {r['cash']:,.0f}")
print('\n=== DELAY 2028 (protocol + 6mo ordering slip) ===')
for r in SCEN['delay_protocol']['res']['rows28']:
    print(f"{r['month']} rev {r['rev']+r['setup']:,.0f} cogs {r['cogs']:,.0f} opex {r['opex']:,.0f} net {r['net']:,.0f} cash {r['cash']:,.0f}")

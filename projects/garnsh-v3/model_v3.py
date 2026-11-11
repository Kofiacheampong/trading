#!/usr/bin/env python3
"""Garnsh v3.0 financial model — audited rebuild.

Changes from v2.4:
  * 2027 onboarding labour is modelled explicitly: imputed at $60/h when the
    founders perform it, and as cash when a contractor performs it.
  * Group logo churn and location churn are applied monthly.
  * Cash flow is separated from revenue recognition: subscription collection
    lag is a parameter, and setup fees are collected 50% at go-live / 50% the
    following month. AR is tracked.
  * Gross group adds are calibrated so the plan's net group targets survive
    churn, and the extra onboarding/setup cost is visible.
  * Base, downside and sensitivity scenarios all run through the same engine.
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
CLOSE6_2027 = [
    ('showcase', 3, 1), ('showcase', 4, 2), ('showcase', 5, 1), ('showcase', 6, 2),
    ('design', 7, 2), ('design', 8, 2),
    ('full', 9, 2), ('full', 10, 2), ('full', 11, 1),
]
SLOW_2027 = [
    ('showcase', 3, 1), ('showcase', 5, 2), ('showcase', 7, 3),
    ('design', 8, 2), ('design', 9, 2),
    ('full', 10, 2), ('full', 11, 3),
]

def schedule_by_month(sched):
    d = {}
    for kind, start, groups in sched:
        d.setdefault(start, []).append((kind, groups))
    return d

def distribute(n, year_start):
    base, rem = divmod(n, 12)
    out = {}
    for i in range(12):
        g = base + (1 if i < rem else 0)
        if g:
            out[year_start + i] = [('new', g)]
    return out

def merge(*dicts):
    out = {}
    for d in dicts:
        for k, v in d.items():
            out.setdefault(k, []).extend(v)
    return out

# ---------------------------------------------------------------- revenue
def price_per_loc(c, m, core, remove_ordering=False, remove_app=False):
    age = m - c['start']
    if age < 0:
        return 0.0
    if c['kind'] == 'design' and age < FREE:
        return 0.0
    base = core * (1 - DISC) if (c['kind'] == 'showcase' and age < FREE) else core
    ordering = 0.0 if remove_ordering else ORDERING * o(m)
    app = 0.0 if remove_app else APP * a(m)
    return base + BOARDS * b(m) + ordering + app

def month_revenue(active, m, core, remove_ordering=False, remove_app=False):
    rev = setup = live = pay = 0.0
    for c in active:
        age = m - c['start']
        if age < 0:
            continue
        loc = c['loc']
        if loc <= 0:
            continue
        live += loc
        p = price_per_loc(c, m, core, remove_ordering, remove_app)
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

def opex_2028(m, mrr_prev):
    lines = {
      'Founder draws (2 x $3K/mo)': 6000 if m >= 6 else 0,
      'Engineer (from July)':       9000 if m >= 6 else 0,
      'Growth hire (from Oct)':     7500 if m >= 9 else 0,
      'Tools & SaaS':               800,
      'Legal / insurance / admin':  1000,
      'Travel & demos':             1500 if mrr_prev >= 15000 else 0,
      'Marketing & content':        2000 if mrr_prev >= 25000 else 0,
      'Contract design':            1000 if mrr_prev >= 35000 else 0,
    }
    return sum(lines.values()), lines

# ---------------------------------------------------------------- simulation
def simulate(sched, gross28=37, gross29=56, group_size=14, core=CORE,
             gc=0.015, lc=0.005, lag=0, onboarding_cash_2027=False,
             onboarding_hours=2, remove_ordering=False, remove_app=False,
             start_cash=20000.0):
    adds = merge(schedule_by_month(sched), distribute(gross28, 12), distribute(gross29, 24))
    active = []
    cash = start_cash
    total_rev = total_collect = 0.0
    prev_live = 0.0
    sub_hist = []
    setup_cash = [0.0] * 36
    rows = []
    for m in range(36):
        # churn first
        for c in active:
            c['groups'] *= (1 - gc)
            c['loc'] *= (1 - gc) * (1 - lc)
        # new cohorts
        new_locs = 0.0
        for kind, g in adds.get(m, []):
            loc = float(g * group_size)
            active.append(dict(kind=kind, start=m, groups=float(g), loc=loc))
            new_locs += loc
            if kind in ('full', 'new'):
                amt = g * SETUP
                setup_cash[m] += amt * 0.5
                setup_cash[m + 1 if m + 1 < 36 else m] += amt * 0.5
        # revenue
        rev, setup_rev, live, pay = month_revenue(active, m, core,
                                                  remove_ordering, remove_app)
        sub_hist.append(rev)
        sub_collected = sub_hist[m - lag] if m - lag >= 0 else 0.0
        collections = sub_collected + setup_cash[m]
        # costs
        avg_live = (prev_live + live) / 2
        infra = avg_live * INFRA
        payments = rev * PAY
        mrr_prev = sub_hist[-2] if len(sub_hist) >= 2 else 0.0
        if m < 12:
            support = SUPPORT if live >= 150 else 0.0
            opex = sum(v[m] for v in OPEX_2027.values())
            onb_cash = new_locs * 60 * onboarding_hours if onboarding_cash_2027 else 0.0
            onb_imp = new_locs * 60 * onboarding_hours if not onboarding_cash_2027 else 0.0
        elif m < 24:
            support = SUPPORT if live >= 150 else 0.0
            opex, _ = opex_2028(m - 12, mrr_prev)
            onb_cash = new_locs * 60 * onboarding_hours
            onb_imp = 0.0
        else:
            support = 7500.0
            opex = sum(v[m - 24] for v in OPEX_2029.values())
            onb_cash = new_locs * 60 * onboarding_hours
            onb_imp = 0.0
        cogs_cash = infra + payments + support + onb_cash
        cogs_econ = cogs_cash + onb_imp
        cash_net = collections - cogs_cash - opex
        econ_net = rev + setup_rev - cogs_econ - opex
        cash += cash_net
        total_rev += rev + setup_rev
        total_collect += collections
        rows.append(dict(month=MONTHS[m % 12], year=2027 + m // 12, m=m,
                         rev=rev, setup=setup_rev, live=live, pay=pay,
                         groups=sum(c['groups'] for c in active),
                         infra=infra, payments=payments, support=support,
                         onb_cash=onb_cash, onb_imputed=onb_imp,
                         cogs_cash=cogs_cash, cogs_econ=cogs_econ,
                         opex=opex, cash_net=cash_net, econ_net=econ_net,
                         cash=cash, ar=total_rev - total_collect,
                         mrr=mrr_prev))
        prev_live = live
    return rows

def year_rows(rows, year):
    return [r for r in rows if r['year'] == year]

def summary(rows, year):
    rs = year_rows(rows, year)
    rev = sum(r['rev'] + r['setup'] for r in rs)
    cogs_cash = sum(r['cogs_cash'] for r in rs)
    cogs_econ = sum(r['cogs_econ'] for r in rs)
    opex = sum(r['opex'] for r in rs)
    return dict(
        rev=rev, cogs_cash=cogs_cash, cogs_econ=cogs_econ,
        gp_cash=rev - cogs_cash, gp_econ=rev - cogs_econ,
        gm_cash=(rev - cogs_cash) / rev if rev else 0,
        gm_econ=(rev - cogs_econ) / rev if rev else 0,
        opex=opex, econ_net=rev - cogs_econ - opex,
        cash_net=sum(r['cash_net'] for r in rs),
        cash=rs[-1]['cash'], low=min(r['cash'] for r in rs),
        live=rs[-1]['live'], pay=rs[-1]['pay'], groups=rs[-1]['groups'],
        exit_mrr=rs[-1]['rev'], ar=rs[-1]['ar'],
        new_locs=sum(r['onb_cash'] + r['onb_imputed'] for r in rs) / (60 * 2),
    )

def run(name, **kw):
    rows = simulate(**kw)
    out = dict(rows=rows, y27=summary(rows, 2027), y28=summary(rows, 2028),
               y29=summary(rows, 2029))
    out['trough'] = min(year_rows(rows, 2027), key=lambda r: r['cash'])
    return out

BASE = dict(sched=BASE_2027)
SCEN = {
  'base': run('base', **BASE),
  'downside': run('downside', sched=CLOSE6_2027, gross28=31, gross29=46,
                  group_size=10, gc=0.025, lc=0.010, lag=1),
  'churn25': run('churn25', sched=BASE_2027, gc=0.025, lc=0.010),
  'g10': run('g10', sched=BASE_2027, group_size=10),
  'close6': run('close6', sched=CLOSE6_2027),
  'slow': run('slow', sched=SLOW_2027),
  'lag1': run('lag1', sched=BASE_2027, lag=1),
  'onb_paid': run('onb_paid', sched=BASE_2027, onboarding_cash_2027=True),
  'onb4h': run('onb4h', sched=BASE_2027, onboarding_hours=4),
  'p45': run('p45', sched=BASE_2027, core=45.0),
  'toast': run('toast', sched=BASE_2027, remove_ordering=True),
  'toast_app': run('toast_app', sched=BASE_2027, remove_ordering=True, remove_app=True),
}

json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'rows'} for k, v in SCEN.items()},
          open('model_v3.json','w'), indent=1)
json.dump({k: v['rows'] for k, v in SCEN.items()}, open('model_v3_rows.json','w'), indent=1)

print('=== SCENARIOS ===')
for k, v in SCEN.items():
    y27,y28,y29 = v['y27'],v['y28'],v['y29']
    print(f"{k:11s} 27rev {y27['rev']:>8,.0f} econ {y27['econ_net']:>8,.0f} cash {y27['cash_net']:>8,.0f} tr {v['trough']['month']} {v['trough']['cash']:>7,.0f} ye {y27['cash']:>7,.0f} | "
          f"28rev {y28['rev']:>9,.0f} econ {y28['econ_net']:>8,.0f} low {y28['low']:>7,.0f} grp {y28['groups']:>4.1f} | "
          f"29rev {y29['rev']:>10,.0f} econ {y29['econ_net']:>9,.0f} low {y29['low']:>8,.0f} grp {y29['groups']:>5.1f}")

print('\n=== BASE 2027 ===')
for r in year_rows(SCEN['base']['rows'], 2027):
    print(f"{r['month']} live {r['live']:>4.0f} pay {r['pay']:>4.0f} rev {r['rev']+r['setup']:>7,.0f} cashnet {r['cash_net']:>7,.0f} econ {r['econ_net']:>7,.0f} cash {r['cash']:>7,.0f} AR {r['ar']:>7,.0f}")

print('\n=== BASE 2028 ===')
for r in year_rows(SCEN['base']['rows'], 2028):
    print(f"{r['month']} live {r['live']:>4.0f} rev {r['rev']+r['setup']:>7,.0f} opex {r['opex']:>6,.0f} onb {r['onb_cash']:>6,.0f} cashnet {r['cash_net']:>7,.0f} cash {r['cash']:>7,.0f} AR {r['ar']:>7,.0f}")

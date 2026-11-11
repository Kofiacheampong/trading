#!/usr/bin/env python3
"""Garnsh financial model v3.1 — Gen 1-only base case.

What changed from v3.0:
  * The base case contains NO Gen 2 ordering and NO Gen 3 app revenue.
    v3.0's 2028-29 projections embedded 17%/28% ordering attach and 3.5% app
    attach, so they were not Gen 1 numbers.
  * Expansion revenue is modelled separately and never merged into the base.
  * Setup pricing is cost-recovery: $120/location, $1,500 minimum (this is the
    approved v3.1 revision; v3.0 used a flat $1,500 that lost money above 12
    locations).
  * One 2027 funnel drives cohorts, founder hours and revenue: 60 qualified
    conversations -> 24 pilots -> 15 gross groups (4 free, 6 discounted,
    5 full price).
  * Adds a combined stress case and an explicit cost-reduction response.
  * Tracks churned groups explicitly instead of inferring them.

Conventions:
  * Month 0 = January 2027. Cohorts first bill at 50% of a month.
  * Churn is monthly and multiplicative: group logo churn and location churn.
  * Cash != revenue: subscriptions can lag (lag parameter); setup fees are
    50% at go-live, 50% the following month; AR is tracked.
  * Founder onboarding labour is imputed at $60/h in 2027 (cash 0) unless
    onboarding_paid is set, in which case it is cash.
"""
import json
from copy import deepcopy

MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# ---------------------------------------------------------------- price book
CORE = 59.0              # $/location/month
BOARDS = 40.0            # $/location/month where screens exist
SETUP_MIN = 1500.0       # $/brand floor
SETUP_PER_LOC = 120.0    # $/location, cost-recovery on 2h @ $60
DISC = 0.20              # showcase discount
FREE_MONTHS = 3          # v3.1: 90-day free design-partner program
DISC_MONTHS = 6          # v3.1: 6-month showcase discount
INFRA = 1.70             # $/live location/month
PAY = 0.029              # payment processing, % of revenue
ONB_HOURS = 2.0
ONB_RATE = 60.0
SUPPORT_FROM = 150       # live locations that trigger a support contractor
SUPPORT_COST = 2500.0
START_CASH = 20000.0
RESERVE = 5000.0

# ---------------------------------------------------------------- ramp curves
def boards_attach(m):
    """Share of locations buying the board product, by month index."""
    if m < 12:
        return 0.05
    if m < 24:
        return 0.05 + 0.50 * (m - 12) / 11
    return 0.55 + 0.10 * (m - 24) / 11


# ---------------------------------------------------------------- 2027 cohorts
# (kind, first month index, groups). kind: free | disc | full
BASE_2027 = [
    ('free', 3, 1), ('free', 4, 1), ('free', 5, 2),          # 4 free partners
    ('disc', 3, 1), ('disc', 4, 1), ('disc', 5, 1),          # 6 discounted
    ('disc', 6, 1), ('disc', 7, 1), ('disc', 8, 1),
    ('full', 9, 1), ('full', 9, 1), ('full', 10, 2), ('full', 11, 1),  # 5 full
]

# Combined-stress 2027: 10 groups, first live in June, smaller groups.
STRESS_2027 = [
    ('free', 5, 1), ('free', 6, 1), ('free', 7, 1), ('free', 8, 1),
    ('disc', 5, 1), ('disc', 6, 1), ('disc', 7, 1), ('disc', 8, 1),
    ('full', 9, 1), ('full', 10, 1),
]


def schedule_map(sched):
    out = {}
    for kind, start, groups in sched:
        out.setdefault(start, []).append((kind, groups))
    return out


def spread(n, start_month):
    """Spread n gross adds evenly across 12 months from start_month."""
    base, rem = divmod(n, 12)
    out = {}
    for i in range(12):
        g = base + (1 if i < rem else 0)
        if g:
            out.setdefault(start_month + i, []).append(('full', g))
    return out


def merge(*maps):
    out = {}
    for mp in maps:
        for k, v in mp.items():
            out.setdefault(k, []).extend(v)
    return out


# ---------------------------------------------------------------- operating cost
def opex_2027(m):
    lines = {
        'Design (milestone payments)': 1667 if m < 3 else 0,
        'Entity / legal / IP': 2500 if m == 0 else (500 if m == 6 else 0),
        'Insurance (E&O, cyber)': 1500 if m == 1 else 0,
        'Tools & SaaS': 300 if m < 6 else 450,
        'Brand / site / demo': 2000 if m == 1 else 0,
        'Travel & demos': [0, 0, 800, 800, 800, 800, 0, 0, 1200, 0, 1200, 0][m],
        'Toast certification / partner fees': 3000 if m == 8 else 0,
        'Marketing & content': 150 if m >= 5 else 0,
        'Admin & misc': 150,
    }
    return sum(lines.values()), lines


def opex_2028(m, mrr_prev):
    """m = 0..11 for 2028."""
    lines = {
        'Founder draws (2 x $3K/mo, from Jul)': 6000 if m >= 6 else 0,
        'Engineer (from Jul)': 9000 if m >= 6 else 0,
        'Growth / account mgmt (from Oct)': 7500 if m >= 9 else 0,
        'Tools & SaaS': 800,
        'Legal / insurance / admin': 1000,
        'Travel & demos': 1500 if mrr_prev >= 15000 else 0,
        'Marketing & content': 2000 if mrr_prev >= 25000 else 0,
        'Contract design': 1000 if mrr_prev >= 30000 else 0,
    }
    return sum(lines.values()), lines


OPEX_2029_MONTHLY = {
    'Founders (2 x $50K)': 8333,
    'Engineer': 10000,
    'Growth / account management': 9167,
    'Tools & SaaS': 1500,
    'Travel & demos': 2000,
    'Marketing & content': 4000,
    'Legal / insurance / audit': 2000,
    'Contract design': 1000,
    'Admin & misc': 1250,
}


def opex_2029():
    return sum(OPEX_2029_MONTHLY.values()), dict(OPEX_2029_MONTHLY)


# ---------------------------------------------------------------- engine
def simulate(sched, gross28=37, gross29=56, group_size=14, core=CORE,
             gc=0.015, lc=0.005, lag=0, onboarding_paid=False,
             onboarding_hours=ONB_HOURS, setup_min=SETUP_MIN,
             setup_per_loc=SETUP_PER_LOC, start_cash=START_CASH,
             opex_scale=1.0, response=False, months=36):
    adds = merge(schedule_map(sched), spread(gross28, 12), spread(gross29, 24))
    active = []
    cash = start_cash
    rows = []
    ar = 0.0
    sub_hist = [0.0] * (months + 1)
    setup_cash = [0.0] * (months + 2)
    churned_total = 0.0
    live_prev = 0.0
    total_imputed = 0.0

    for m in range(months):
        # --- churn (applied before adds)
        month_churn = 0.0
        for c in active:
            lost = c['groups'] * gc
            c['groups'] -= lost
            month_churn += lost
            c['loc'] *= (1 - gc) * (1 - lc)
        churned_total += month_churn

        # --- new cohorts
        new_locs = 0.0
        setup_rev = 0.0
        for kind, g in adds.get(m, []):
            loc = float(g * group_size)
            active.append(dict(kind=kind, start=m, groups=float(g), loc=loc))
            new_locs += loc
            if kind in ('full', 'disc'):
                fee_per_group = max(setup_min, setup_per_loc * loc / g)
                fee = fee_per_group * g
                setup_cash[m] += fee * 0.5
                setup_cash[m + 1] += fee * 0.5
                setup_rev += fee

        # --- revenue
        rev = 0.0
        live = pay = 0.0
        for c in active:
            age = m - c['start']
            if c['loc'] <= 0:
                continue
            live += c['loc']
            if c['kind'] == 'free' and age < FREE_MONTHS:
                continue
            price = core
            if c['kind'] == 'disc' and age < DISC_MONTHS:
                price = core * (1 - DISC)
            price += BOARDS * boards_attach(m)
            rev += c['loc'] * price * (0.5 if age == 0 else 1.0)
            pay += c['loc']
        sub_hist[m] = rev

        collections = (sub_hist[m - lag] if m - lag >= 0 else 0.0) + setup_cash[m]

        # --- cost of revenue
        avg_live = (live_prev + live) / 2
        infra = avg_live * INFRA
        payments = rev * PAY
        # Support sits in cost of revenue, not opex, to avoid double counting.
        support = 0.0
        if live >= 800:
            support = 7500.0
        elif live >= SUPPORT_FROM:
            support = 2500.0
        # 2027: founders perform onboarding (imputed, no cash) unless paid.
        # 2028-29: a contractor performs onboarding, so it is cash either way.
        if (m < 12 and not onboarding_paid) or response:
            onb_cash = 0.0
            onb_imputed = new_locs * ONB_RATE * onboarding_hours
        else:
            onb_cash = new_locs * ONB_RATE * onboarding_hours
            onb_imputed = 0.0
        total_imputed += onb_imputed

        # --- operating expense
        mrr_prev = sub_hist[m - 1] if m >= 1 else 0.0
        if response:
            # Explicit freeze: no hires, no founder pay, no marketing beyond
            # the website; part-time support from 150 live locations.
            opex = 2450.0
            if live >= SUPPORT_FROM:
                opex += SUPPORT_COST
            opex *= opex_scale
        elif m < 12:
            opex, _ = opex_2027(m)
        elif m < 24:
            opex, _ = opex_2028(m - 12, mrr_prev)
        else:
            opex, _ = opex_2029()
        opex *= opex_scale
        if response and m < 12:
            opex = opex_2027(m)[0] * 0.8

        cogs_cash = infra + payments + support + onb_cash
        cogs_econ = cogs_cash + onb_imputed
        cash_net = collections - cogs_cash - opex
        econ_net = rev + setup_rev - cogs_econ - opex
        cash += cash_net
        recognized = rev + setup_rev
        ar += recognized - collections

        rows.append(dict(
            m=m, year=2027 + m // 12, month=MONTHS[m % 12],
            rev=rev, setup_rev=setup_rev, live=live, pay=pay,
            groups=sum(c['groups'] for c in active),
            infra=infra, payments=payments, support=support,
            onb_cash=onb_cash, onb_imputed=onb_imputed,
            cogs_cash=cogs_cash, cogs_econ=cogs_econ, opex=opex,
            cash_net=cash_net, econ_net=econ_net, cash=cash, ar=ar,
            mrr=rev, new_locs=new_locs, churned=month_churn,
            new_groups=sum(g for _, g in adds.get(m, [])),
        ))
        live_prev = live

    return dict(rows=rows, imputed=total_imputed)


def yr(sim, year):
    rs = [r for r in sim['rows'] if r['year'] == year]
    rev = sum(r['rev'] for r in rs)
    cogs = sum(r['cogs_cash'] for r in rs)
    cogs_econ = sum(r['cogs_econ'] for r in rs)
    opex = sum(r['opex'] for r in rs)
    return dict(
        rev=rev, cogs=cogs, cogs_econ=cogs_econ,
        gp=rev - cogs, gm=(rev - cogs) / rev if rev else 0.0,
        opex=opex, econ=rev - cogs_econ - opex,
        cash_ops=sum(r['cash_net'] for r in rs),
        cash_end=rs[-1]['cash'], cash_min=min(r['cash'] for r in rs),
        mrr=rs[-1]['rev'], arr=rs[-1]['rev'] * 12,
        gross_groups=sum(r['new_groups'] for r in rs),
        churned=sum(r['churned'] for r in rs),
        net_groups=rs[-1]['groups'], live=rs[-1]['live'], pay=rs[-1]['pay'],
        new_locs=sum(r['new_locs'] for r in rs),
        onb_cash=sum(r['onb_cash'] for r in rs),
        onb_imputed=sum(r['onb_imputed'] for r in rs),
        setup_rev=sum(r['setup_rev'] for r in rs),
        ar=rs[-1]['ar'],
    )


def build(sched=BASE_2027, **kw):
    sim = simulate(sched, **kw)
    out = dict(sim=sim, y27=yr(sim, 2027), y28=yr(sim, 2028), y29=yr(sim, 2029),
               imputed=sim['imputed'])
    out['low'] = min(sim['rows'], key=lambda r: r['cash'])
    return out


BASE = build()
DOWN = build(sched=BASE_2027, gross28=31, gross29=46, group_size=10,
             gc=0.025, lc=0.010, lag=1)
STRESS = build(sched=STRESS_2027, gross28=22, gross29=30, group_size=10,
               gc=0.025, lc=0.010, lag=1, onboarding_paid=True,
               onboarding_hours=4.0)
STRESS_RESP = build(sched=STRESS_2027, gross28=22, gross29=30, group_size=10,
                    gc=0.025, lc=0.010, lag=1, onboarding_paid=False,
                    onboarding_hours=4.0, response=True)
STRESS_BRIDGE = build(sched=STRESS_2027, gross28=22, gross29=30, group_size=10,
                      gc=0.025, lc=0.010, lag=1, onboarding_paid=False,
                      onboarding_hours=4.0, response=True, start_cash=50000.0)
DOWN_RESP = build(sched=BASE_2027, gross28=31, gross29=46, group_size=10,
                  gc=0.025, lc=0.010, lag=1, response=True)


def sensitivity():
    cases = {
        'Base': {},
        'Group size 10': dict(group_size=10),
        'Close 1 in 6 (10 groups)': dict(sched=STRESS_2027),
        'Launch delayed to June': dict(sched=[(k, s + 2, g) for k, s, g in BASE_2027]),
        'Churn 2.5% / 1.0%': dict(gc=0.025, lc=0.010),
        '30-day collection lag': dict(lag=1),
        'Paid 2027 onboarding': dict(onboarding_paid=True),
        'Onboarding 4h/location': dict(onboarding_hours=4.0),
        'Core price $45': dict(core=45.0),
        'Setup flat $1,500': dict(setup_per_loc=0.0),
        'Setup $2,500': dict(setup_min=2500.0),
    }
    out = {}
    for name, kw in cases.items():
        r = build(**kw)
        out[name] = dict(rev27=r['y27']['rev'], econ27=r['y27']['econ'],
                         low=r['low']['cash'], low_month=r['low']['month'],
                         cash28=r['y28']['cash_min'], cash29=r['y29']['cash_end'])
    return out


SENS = sensitivity()

# ---------------------------------------------------------------- expansion case
def expansion(base):
    """Gen 2 ordering from Jul 2028, Gen 3 app from Jul 2029.

    Incremental only. Costs are explicit; revenue is recognised only after
    launch. Attach rates are of live locations.
    """
    rows = []
    cum = 0.0
    for r in base['sim']['rows']:
        m = r['m']
        ordering = app = 0.0
        dev = cert = 0.0
        if 12 <= m < 18:
            dev += 5000.0        # Gen 2 contract engineering, $30K over 6 months
        if m == 17:
            cert += 15000.0      # certification, security review, legal
        if m >= 18:
            attach = min(0.22, 0.04 + 0.015 * (m - 18))
            ordering = r['live'] * attach * 99.0
        if 24 <= m < 30:
            dev += 8333.0        # Gen 3 build, $50K over 6 months
        if m == 29:
            cert += 10000.0
        if m >= 30:
            attach = min(0.035, 0.010 + 0.004 * (m - 30))
            app = r['live'] * attach * (149.0 + 5000.0 / 36.0)
        inc = ordering + app - dev - cert
        cum += inc
        rows.append(dict(m=m, year=r['year'], month=r['month'],
                         ordering=ordering, app=app, dev=dev + cert,
                         incremental=inc, cumulative=cum))
    return rows


EXP = expansion(BASE)


# ---------------------------------------------------------------- funnel 2027
FUNNEL = dict(
    qualified=60,
    conversations_h1=40,
    pilots=24,
    converted=15,
    free=4,
    discounted=6,
    full=5,
)

# ---------------------------------------------------------------- founder hours
def founder_hours():
    sell = FUNNEL['qualified'] * 3 + FUNNEL['pilots'] * 6
    onb = 15 * 14 * 2
    build_h = 400
    support = 60
    admin = 260
    total = sell + onb + build_h + support + admin
    return dict(build=build_h, selling=sell, onboarding=onb, support=support,
                admin=admin, total=total,
                per_week_each=total / 52 / 2)

HOURS = founder_hours()


def money(x):
    return f"${x:,.0f}"


def show(name, r):
    y27, y28, y29 = r['y27'], r['y28'], r['y29']
    print(f"{name:12s} "
          f"27 rev {money(y27['rev']):>9s} econ {money(y27['econ']):>9s} cash {money(y27['cash_end']):>8s} low {money(y27['cash_min']):>8s} | "
          f"28 rev {money(y28['rev']):>9s} econ {money(y28['econ']):>8s} low {money(y28['cash_min']):>8s} grp {y28['net_groups']:5.1f} | "
          f"29 rev {money(y29['rev']):>9s} econ {money(y29['econ']):>8s} cash {money(y29['cash_end']):>8s} grp {y29['net_groups']:5.1f}")


if __name__ == '__main__':
    print('=== SCENARIOS (Gen 1 only) ===')
    show('base', BASE)
    show('downside', DOWN)
    show('stress', STRESS)
    show('stress+resp', STRESS_RESP)
    show('stress+resp+bridge', STRESS_BRIDGE)
    show('down+resp', DOWN_RESP)
    print('\nbase trough', BASE['low']['month'], money(BASE['low']['cash']))
    print('down trough', DOWN['low']['month'], money(DOWN['low']['cash']))
    print('stress trough', STRESS['low']['month'], money(STRESS['low']['cash']),
          'breach first at', next(r['month'] for r in STRESS['sim']['rows'] if r['cash'] < RESERVE))
    print('stress+resp trough', STRESS_RESP['low']['month'], money(STRESS_RESP['low']['cash']))
    print('\nhours', HOURS)
    print('\n=== BASE 2027 ===')
    for r in BASE['sim']['rows'][:12]:
        print(f"{r['month']} live {r['live']:5.0f} pay {r['pay']:5.0f} rev {r['rev']:8,.0f} "
              f"cashnet {r['cash_net']:8,.0f} econ {r['econ_net']:8,.0f} cash {r['cash']:8,.0f}")
    print('\n=== BASE 2028/29 ===')
    for r in BASE['sim']['rows'][12:]:
        print(f"{r['year']} {r['month']} live {r['live']:5.0f} rev {r['rev']:9,.0f} opex {r['opex']:8,.0f} "
              f"cashnet {r['cash_net']:8,.0f} cash {r['cash']:9,.0f}")

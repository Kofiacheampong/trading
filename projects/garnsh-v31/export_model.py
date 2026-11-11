#!/usr/bin/env python3
"""Export the v3.1 model to JSON, XLSX and markdown tables."""
import json, importlib.util, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('m', os.path.join(HERE, 'model_v31.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

BASE, DOWN, STRESS, RESP, BRIDGE, DOWNR = (
    m.BASE, m.DOWN, m.STRESS, m.STRESS_RESP, m.STRESS_BRIDGE, m.DOWN_RESP)
ROWS = BASE['sim']['rows']

# ---------------------------------------------------------------- expansion
def expansion(base_rows):
    rows, cum = [], 0.0
    prev_app_groups = 0.0
    for r in base_rows:
        mo = r['m']
        ordering = app = oneoff = 0.0
        dev = cert = support = fees = 0.0
        # Gen 2: 6-month build Jan-Jun 2028, certification June, launch July.
        if 12 <= mo <= 17:
            dev += 10000.0
        if mo == 17:
            cert += 15000.0
        if mo >= 18:
            attach = min(0.22, 0.04 + 0.015 * (mo - 18))
            ordering = r['live'] * attach * 99.0
        # Gen 3: 6-month build Jan-Jun 2029, certification June, launch July.
        if 24 <= mo <= 29:
            dev += 10000.0
        if mo == 29:
            cert += 10000.0
        if mo >= 30:
            attach = min(0.035, 0.010 + 0.004 * (mo - 30))
            app_groups = attach * r['groups']
            oneoff = max(0.0, app_groups - prev_app_groups) * 5000.0
            prev_app_groups = app_groups
            app = r['live'] * attach * 149.0
        if mo >= 18:
            support += 2500.0 if mo < 30 else 5000.0
        fees = (ordering + app) * 0.029
        inc_rev = ordering + app + oneoff
        inc_cost = dev + cert + support + fees
        net = inc_rev - inc_cost
        cum += net
        rows.append(dict(m=mo, year=r['year'], month=r['month'],
                         ordering=ordering, app=app, oneoff=oneoff,
                         revenue=inc_rev, dev=dev + cert, support=support,
                         fees=fees, cost=inc_cost, net=net, cum=cum))
    return rows

EXP = expansion(ROWS)
def ysum(rows, y):
    s = [r for r in rows if r['year'] == y]
    return {k: sum(r[k] for r in s) for k in ('ordering','app','oneoff','revenue','dev','support','fees','cost','net')}
EXP_Y = {y: ysum(EXP, y) for y in (2027, 2028, 2029)}

# ---------------------------------------------------------------- quarterly 2027
def quarters(sim):
    out = []
    for q in range(4):
        rs = [r for r in sim['rows'] if r['m'] // 3 == q]
        out.append(dict(q=q + 1,
                        rev=sum(r['rev'] + r['setup_rev'] for r in rs),
                        cash_ops=sum(r['cash_net'] for r in rs),
                        econ=sum(r['econ_net'] for r in rs),
                        cash=rs[-1]['cash'],
                        live=rs[-1]['live'], pay=rs[-1]['pay'],
                        groups=rs[-1]['groups']))
    return out
Q27 = quarters(BASE['sim'])

# ---------------------------------------------------------------- founder hours by quarter
def hours_by_quarter():
    # build 40h/mo Jan-Apr (10 weeks), sales evenly, onboarding at cohort month.
    cohorts = {}
    for kind, start, g in m.BASE_2027:
        cohorts[start] = cohorts.get(start, 0) + g * 14 * 2
    out = []
    for q in range(4):
        months = range(q * 3, q * 3 + 3)
        build = sum(40 for mo in months if mo < 3)
        sell = (m.FUNNEL['qualified'] * 3 + m.FUNNEL['pilots'] * 6) / 4
        onb = sum(cohorts.get(mo, 0) for mo in months)
        sup = sum(15 for mo in months if mo >= 9)
        admin = 5 * 13
        a = build * 0.6 + sell * 0.3 + onb * 0.5 + (sup + admin) * 0.5
        b = build * 0.4 + sell * 0.7 + onb * 0.5 + (sup + admin) * 0.5
        out.append(dict(q=q + 1, build=build, sell=sell, onboarding=onb,
                        support=sup, admin=admin,
                        total=build + sell + onb + sup + admin,
                        a=a / 13, b=b / 13))
    return out
HOURS_Q = hours_by_quarter()

# ---------------------------------------------------------------- unit economics
UG = dict(loc=14, arpu=98.0, rev=14 * 98.0, gm=0.89)
UG['gp'] = UG['rev'] * UG['gm']
UG['cac'] = 18 * 55 + 600
UG['onb'] = 14 * 2 * 60
UG['setup'] = max(1500.0, 120 * 14)
UG['net_onb'] = UG['onb'] - UG['setup']
UG['upfront'] = UG['cac'] + UG['net_onb']
UG['payback'] = UG['upfront'] / UG['gp']
UG['life'] = 1 / 0.02
UG['ltv'] = UG['gp'] * UG['life']
UG['ltv_cac'] = UG['ltv'] / UG['cac']
UG['down_life'] = 1 / 0.035
UG['down_ltv'] = UG['gp'] * UG['down_life']
UG['down_ltv_cac'] = UG['down_ltv'] / UG['cac']

# ---------------------------------------------------------------- save json
def clean(d):
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()}

out = dict(
    base={y: clean(BASE[y]) for y in ('y27', 'y28', 'y29')},
    downside={y: clean(DOWN[y]) for y in ('y27', 'y28', 'y29')},
    stress={y: clean(STRESS[y]) for y in ('y27', 'y28', 'y29')},
    stress_response={y: clean(RESP[y]) for y in ('y27', 'y28', 'y29')},
    stress_bridge={y: clean(BRIDGE[y]) for y in ('y27', 'y28', 'y29')},
    down_response={y: clean(DOWNR[y]) for y in ('y27', 'y28', 'y29')},
    trough=dict(base=BASE['low']['month'], base_cash=BASE['low']['cash'],
                down=DOWN['low']['month'], down_cash=DOWN['low']['cash'],
                stress=STRESS['low']['month'], stress_cash=STRESS['low']['cash'],
                resp=RESP['low']['month'], resp_cash=RESP['low']['cash']),
    expansion=EXP_Y, unit=UG, funnel=m.FUNNEL, hours=m.HOURS,
    hours_q=HOURS_Q, quarters=Q27, sensitivity=m.SENS, months=ROWS,
)
json.dump(out, open(os.path.join(HERE, 'model_v31.json'), 'w'), indent=1)

# ---------------------------------------------------------------- xlsx
wb = Workbook()
H1 = Font(bold=True, size=14, color='151515')
BOLD = Font(bold=True)
HEAD = PatternFill('solid', fgColor='151515')
HFONT = Font(bold=True, color='FFFDF8')
NOTE = Font(italic=True, size=9, color='5E5E5A')
MONEY = '#,##0'
PCT = '0.0%'
thin = Side(style='thin', color='D9D7D0')

def style_header(ws, row=1):
    for c in ws[row]:
        c.fill = HEAD; c.font = HFONT; c.alignment = Alignment(vertical='center')
    ws.row_dimensions[row].height = 22
    ws.freeze_panes = ws.cell(row=row + 1, column=1)

def widths(ws, w):
    for i, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(i)].width = x

# Assumptions
ws = wb.active; ws.title = 'Assumptions'
ws['A1'] = 'Garnsh financial model v3.1 — assumptions'; ws['A1'].font = H1
ws['A2'] = 'Modeled. Not actuals. Generated by model_v31.py; edit drivers there and re-run, or override here for scenario work.'
ws['A2'].font = NOTE
rows = [
    ('Driver', 'Value', 'Unit', 'Basis'),
    ('Core publishing price', m.CORE, '$/location/month', 'Founder assumption; untested'),
    ('Menu boards add-on', m.BOARDS, '$/location/month', 'Founder assumption'),
    ('Board attach, 2027 / 2028 / 2029', '5% / 55% / 65%', 'of locations', 'Modeled ramp'),
    ('Setup fee, per location', m.SETUP_PER_LOC, '$/location, 2h @ $60', 'Cost-recovery (v3.1 change)'),
    ('Setup fee, minimum', m.SETUP_MIN, '$/brand', 'Floor for small groups'),
    ('Showcase discount', m.DISC, '% of core, 12 months', 'Design-partner program'),
    ('Free design partners', m.FREE_MONTHS, 'months', 'Capped program'),
    ('Average group size', 14, 'locations', 'Modeled; ICP 10-50'),
    ('Group logo churn', 0.015, 'per month', 'Modeled; no cohort data'),
    ('Location churn', 0.005, 'per month', 'Modeled; no cohort data'),
    ('Subscription collection', 'same month', '', 'Card on file'),
    ('Setup collection', '50% go-live / 50% next month', '', 'Modeled'),
    ('Onboarding labour', '2h/location @ $60', '', 'Founder estimate'),
    ('Infrastructure', m.INFRA, '$/live location/month', 'Modeled'),
    ('Payment fees', m.PAY, '% of revenue', 'Stripe standard'),
    ('Support contractor', m.SUPPORT_COST, '$/month from 150 locations', 'Modeled'),
    ('Founder capital', 20000, '$', 'Actual commitment'),
    ('Cash reserve floor', m.RESERVE, '$', "Management policy"),
    ('Gross adds 2028 / 2029', '37 / 56 groups', '', 'Modeled'),
]
for r in rows:
    ws.append(r)
style_header(ws, 3)
for row in ws.iter_rows(min_row=4, max_row=3 + len(rows)):
    for c in row:
        c.border = Border(bottom=thin)
widths(ws, [40, 30, 28, 34])
for i in range(4, 4 + len(rows)):
    v = ws.cell(row=i, column=2).value
    if isinstance(v, float) and v < 1:
        ws.cell(row=i, column=2).number_format = PCT

# Annual
ws = wb.create_sheet('Annual_Gen1')
ws['A1'] = 'Scenario A — Gen 1 only (no ordering, no app revenue)'; ws['A1'].font = H1
hdr = ['Metric', '2027', '2028', '2029']
ws.append([]); ws.append(hdr); style_header(ws, 3)
def line(label, key, fmt=MONEY):
    ws.append([label] + [BASE[y][key] for y in ('y27', 'y28', 'y29')])
    for c in ws[ws.max_row][1:]:
        c.number_format = fmt
for label, key, fmt in [
    ('Revenue', 'rev', MONEY), ('Cost of revenue (cash)', 'cogs', MONEY),
    ('Gross profit', 'gp', MONEY), ('Gross margin', 'gm', PCT),
    ('Operating expenses', 'opex', MONEY),
    ('Economic result after founder labour', 'econ', MONEY),
    ('Cash from operations', 'cash_ops', MONEY),
    ('Year-end cash', 'cash_end', MONEY),
    ('Minimum cash in year', 'cash_min', MONEY),
    ('Exit MRR', 'mrr', MONEY), ('Exit ARR', 'arr', MONEY),
    ('Gross group additions', 'gross_groups', '#,##0'),
    ('Churned groups', 'churned', '#,##0.0'),
    ('Net groups', 'net_groups', '#,##0.0'),
    ('Live locations', 'live', '#,##0'), ('Paying locations', 'pay', '#,##0'),
    ('Setup-fee revenue', 'setup_rev', MONEY),
    ('Onboarding cash cost', 'onb_cash', MONEY),
    ('Onboarding imputed cost', 'onb_imputed', MONEY),
    ('Accounts receivable', 'ar', MONEY),
]:
    line(label, key, fmt)
widths(ws, [40, 16, 16, 16])

# Monthly
ws = wb.create_sheet('Monthly')
ws['A1'] = 'Monthly schedule — Gen 1 base case'; ws['A1'].font = H1
cols = ['Month', 'Year', 'Live loc', 'Paying loc', 'Groups', 'Revenue', 'Setup rev',
        'COGS cash', 'COGS economic', 'Opex', 'Cash from ops', 'Economic result',
        'Opening cash', 'Closing cash', 'AR']
ws.append([]); ws.append(cols); style_header(ws, 3)
start = 4
for i, r in enumerate(ROWS):
    opening = r['cash'] - r['cash_net']
    ws.append([r['month'], r['year'], r['live'], r['pay'], round(r['groups'], 2),
               r['rev'], r['setup_rev'], r['cogs_cash'], r['cogs_econ'], r['opex'],
               r['cash_net'], r['econ_net'], opening, None, r['ar']])
    rr = start + i
    ws.cell(row=rr, column=14).value = f'=M{rr}+K{rr}'
    for col in (6, 7, 8, 9, 10, 11, 12, 13, 14, 15):
        ws.cell(row=rr, column=col).number_format = MONEY
    for col in (3, 4):
        ws.cell(row=rr, column=col).number_format = '#,##0'
widths(ws, [8, 8, 9, 10, 8, 13, 11, 12, 13, 11, 13, 14, 12, 12, 10])

# Expansion
ws = wb.create_sheet('Expansion')
ws['A1'] = 'Scenario B — conditional expansion (incremental to Gen 1, never merged)'; ws['A1'].font = H1
ws['A2'] = 'Gen 2 ordering launches Jul 2028 after six months of build and certification. Gen 3 apps launch Jul 2029. Both are gated on Toast approval and commercial terms.'
ws['A2'].font = NOTE
ws.append([]); ws.append(['Metric', '2027', '2028', '2029']); style_header(ws, 4)
for label, key in [('Gen 2 ordering revenue', 'ordering'), ('Gen 3 app subscription revenue', 'app'),
                   ('Gen 3 build fees', 'oneoff'), ('Total incremental revenue', 'revenue'),
                   ('Development and certification', 'dev'), ('Incremental support', 'support'),
                   ('Payment fees', 'fees'), ('Total incremental cost', 'cost'),
                   ('Incremental contribution', 'net')]:
    ws.append([label] + [EXP_Y[y][key] for y in (2027, 2028, 2029)])
    for c in ws[ws.max_row][1:]:
        c.number_format = MONEY
widths(ws, [36, 16, 16, 16])

# Downside / stress
ws = wb.create_sheet('Downside')
ws['A1'] = 'Combined downside and stress cases'; ws['A1'].font = H1
ws.append([]); ws.append(['Case', '2027 revenue', '2027 economic', '2027 min cash',
                          '2028 revenue', '2029 revenue', '2029 year-end cash'])
style_header(ws, 3)
for name, sc in [('Downside', DOWN), ('Downside + cost response', DOWNR),
                 ('Combined stress', STRESS), ('Combined stress + response', RESP),
                 ('Combined stress + response + $30K bridge', BRIDGE)]:
    ws.append([name, sc['y27']['rev'], sc['y27']['econ'], sc['y27']['cash_min'],
               sc['y28']['rev'], sc['y29']['rev'], sc['y29']['cash_end']])
    for c in ws[ws.max_row][1:]:
        c.number_format = MONEY
widths(ws, [42, 15, 16, 14, 15, 15, 18])

# Stress monthly
ws = wb.create_sheet('Stress_monthly')
ws['A1'] = 'Combined stress — monthly cash'; ws['A1'].font = H1
ws.append([]); ws.append(['Month', 'Year', 'Live loc', 'Revenue', 'Cash from ops', 'Cash'])
style_header(ws, 3)
for r in STRESS['sim']['rows']:
    ws.append([r['month'], r['year'], r['live'], r['rev'], r['cash_net'], r['cash']])
    for c in ws[ws.max_row][1:]:
        c.number_format = MONEY if ws[ws.max_row].index(c) > 1 else '#,##0'
widths(ws, [8, 8, 10, 13, 15, 14])

# Sensitivity
ws = wb.create_sheet('Sensitivity')
ws['A1'] = 'Sensitivity — one variable at a time'; ws['A1'].font = H1
ws.append([]); ws.append(['Case', '2027 revenue', '2027 economic', 'Lowest cash', 'Month'])
style_header(ws, 3)
for name, v in m.SENS.items():
    ws.append([name, v['rev27'], v['econ27'], v['low'], v['low_month']])
    for c in ws[ws.max_row][1:4]:
        c.number_format = MONEY
widths(ws, [34, 15, 16, 15, 10])

# Funnel
ws = wb.create_sheet('Funnel_2027')
ws['A1'] = '2027 customer funnel — one system, reconciled with the model'; ws['A1'].font = H1
ws.append([]); ws.append(['Stage', 'Count', 'Conversion', 'Note']); style_header(ws, 3)
f = m.FUNNEL
frows = [
    ('Qualified conversations', f['qualified'], '', 'Target; 40 in H1'),
    ('30-day paid pilots started', f['pilots'], f"{f['pilots']/f['qualified']:.0%} of conversations", '3 locations each'),
    ('Pilots converted to annual', f['converted'], f"{f['converted']/f['pilots']:.0%} of pilots", 'Includes design partners'),
    ('Free design partners', f['free'], '', '12 months free, setup waived'),
    ('Discounted showcase partners', f['discounted'], '', '20% off core for 12 months'),
    ('Full-price customers', f['full'], '', 'List price, $1,680 setup at 14 locations'),
    ('Gross groups acquired', 15, '', 'Model input'),
    ('Churned groups', 0.9, '', '1.5%/month group churn'),
    ('Net groups at 31 Dec', 14.1, '', 'Model output'),
    ('Live locations', 192, '', 'Model output'),
    ('Paying locations', 144, '', 'Free groups excluded'),
]
for r in frows:
    ws.append(r)
widths(ws, [32, 10, 26, 40])

# Unit economics
ws = wb.create_sheet('Unit_Economics')
ws['A1'] = 'Unit economics — one 14-location group (modeled, no cohort data)'; ws['A1'].font = H1
ws.append([]); ws.append(['Line', 'Value', 'Definition']); style_header(ws, 3)
for label, val, note in [
    ('Monthly revenue', UG['rev'], '14 locations x $98 blended ARPU'),
    ('Recurring gross profit', UG['gp'], '89% margin after infrastructure, payment fees, support'),
    ('CAC', UG['cac'], '18 selling hours x $55 + $600 travel/content'),
    ('Onboarding cost', UG['onb'], '14 x 2h x $60'),
    ('Setup fee', UG['setup'], '$120/location, $1,500 floor'),
    ('Net onboarding cost', UG['net_onb'], 'Onboarding less setup fee'),
    ('Upfront investment', UG['upfront'], 'CAC + net onboarding'),
    ('Payback (months)', UG['payback'], 'Upfront / monthly gross profit'),
    ('Average life (months)', UG['life'], 'At 2.0% monthly revenue churn'),
    ('LTV', UG['ltv'], 'Gross profit x average life'),
    ('LTV : CAC', UG['ltv_cac'], 'LTV / CAC'),
    ('LTV : CAC at 3.5% churn', UG['down_ltv_cac'], 'Downside churn'),
]:
    ws.append([label, val, note])
    ws.cell(row=ws.max_row, column=2).number_format = ('0.0' if isinstance(val, float) and val < 100 else MONEY)
widths(ws, [32, 16, 62])

# Hours
ws = wb.create_sheet('Founder_Hours')
ws['A1'] = '2027 founder hours'; ws['A1'].font = H1
ws.append([]); ws.append(['Activity', 'Hours', 'Basis']); style_header(ws, 3)
h = m.HOURS
for label, val, note in [
    ('Build', h['build'], '10 weeks x 40 hours total'),
    ('Selling', h['selling'], '60 conversations x 3h + 24 pilots x 6h'),
    ('Onboarding', h['onboarding'], '15 groups x 14 locations x 2h'),
    ('Support', h['support'], '~1 hour/day from October'),
    ('Admin', h['admin'], '5 hours/week'),
    ('Total', h['total'], f"{h['per_week_each']:.1f} hours/week each on average"),
]:
    ws.append([label, val, note])
ws.append([])
ws.append(['Quarter', 'Build', 'Selling', 'Onboarding', 'Support+admin', 'Founder A h/wk', 'Founder B h/wk'])
style_header(ws, ws.max_row)
for q in HOURS_Q:
    ws.append([f"Q{q['q']}", q['build'], q['sell'], q['onboarding'],
               q['support'] + q['admin'], round(q['a'], 1), round(q['b'], 1)])
widths(ws, [18, 10, 10, 12, 14, 15, 15])

# Sources
ws = wb.create_sheet('Sources')
ws['A1'] = 'Primary sources used for external claims (verified 11 November 2026)'; ws['A1'].font = H1
ws.append([]); ws.append(['Claim', 'Source', 'Date', 'Type']); style_header(ws, 3)
for r in [
    ('Toast has ~189,000 locations, +21% YoY, ARR $2.5B', 'Toast Q3 2026 results, investors.toasttab.com', '3 Nov 2026', 'Primary'),
    ('Standard API access is read-only, location-specific, no sandbox', 'doc.toasttab.com/devguide/devApiAccessUserGuide.html', '11 Nov 2026', 'Primary'),
    ('Partner access requires application and certification', 'doc.toasttab.com/devguide/apiPartnerIntegrationOverview.html', '11 Nov 2026', 'Primary'),
    ('Menus API supports GET for partner, custom and standard access', 'doc.toasttab.com/devguide/apiOverview.html', '11 Nov 2026', 'Primary'),
    ('Marqii $90-$250/location/month, annual contract', 'marqii.com/pricing', '11 Nov 2026', 'Primary'),
    ('Popmenu $179/$299/$499 per month', 'get.popmenu.com/pricing', '11 Nov 2026', 'Primary'),
    ('Owner.com $249/mo + 5% or $499/mo flat', 'owner.com/pricing', '11 Nov 2026', 'Primary'),
    ('ChowNow from $229/mo annual, $119-$499 setup', 'get.chownow.com/pricing', '11 Nov 2026', 'Primary'),
    ('BentoBox $119-$479/mo website tiers, Clover-only', 'Published pricing roundups', 'Oct 2026', 'Secondary'),
]:
    ws.append(r)
widths(ws, [64, 62, 14, 12])

path = os.path.join(HERE, 'garnsh-financial-model-v3.1.xlsx')
wb.save(path)
print('wrote', path)
print('EXP', {y: {k: round(v) for k, v in EXP_Y[y].items()} for y in EXP_Y})
print('Q27', [{k: (round(v) if isinstance(v, float) else v) for k, v in q.items()} for q in Q27])
print('HOURS_Q', [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in q.items()} for q in HOURS_Q])
print('UG', {k: round(v, 3) if isinstance(v, float) else v for k, v in UG.items()})
print('cum expansion 2029', round(EXP[-1]['cum']))

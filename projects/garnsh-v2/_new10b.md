## 10. Financials

*Every figure in this section comes from a 36-month, cohort-level monthly model (`model.py`, cash basis, January 2027 – December 2029). The model is the source of truth, not this prose: change an assumption there and every table here — and the deck — moves with it. All figures are founder assumptions. Pricing is validated only by the Q1 2027 conversations; the ramp is a plan, not a forecast.*

### 10.1 Unit economics — the engine under everything

The price is $59 per location per month for publishing, plus $40 for menu boards. Blended revenue per location at list is that price stack multiplied by attach rates, nothing else.

| Revenue per location per month (list) | 2027 | 2028 | 2029 |
|---|---|---|---|
| Core publishing — $59 × 100% | $59 | $59 | $59 |
| Menu boards — $40 × attach rate | $2 (5%) | $22 (55%) | $26 (65%) |
| Gen 2 ordering — $99 × attach rate | — | $17 (17%) | $28 (28%) |
| Gen 3 app — $149 × attach rate | — | — | $5 (3.5%) |
| **Blended ARPU at list** | **$61** | **$98** | **$118** |

Boards attach at almost nothing in 2027 because the first cohort is buying publishing to fix a specific problem, not screens. The ordering attach rate (17% of the installed base in Gen 2's first year) is deliberately conservative — it is the one number that depends on Toast, and it should not be load-bearing in year one.

Cost to serve, per **live** location-month — including the four free design partners, because infrastructure and support are paid whether or not the location is invoiced:

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Infrastructure, CDN, image processing | $1.70 | $1.70 | $1.70 |
| Payment processing (2.9% of revenue) | $1.30 | $2.48 | $3.33 |
| Support labour, allocated | $7.60 | $5.59 | $7.67 |
| Onboarding labour, one-time, amortized | — | $9.70 | $6.59 |
| **Cost to serve per live location-month** | **$10.60** | **$19.47** | **$19.29** |
| Revenue per live location-month | $44.96 | $85.57 | $114.99 |
| **Fully loaded gross margin** | **76.4%** | **77.2%** | **83.2%** |

Three honest notes. First, the **software** gross margin is ~95%; the fully loaded number is lower because support and onboarding are real people. We report the fully loaded number because it is the one that pays salaries. Second, 2027 carries no onboarding labour cost only because the founders do it unpaid — that is a cash margin, not an economic one. Third, 2027 gross margin is **76%**, not 83%, because a $2,500/month support contractor is on payroll from October while the showcase cohort is still at 20% off and four groups pay nothing. That is the real cost of the first year. The margin recovers to 83% in 2029 as the cohort pays list, support is spread across 1,288 locations, and onboarding is templated. If it does not pass 85% by 2030, the business is a services company with a software veneer.

### 10.1a Per-group economics — the unit that actually gets sold

The plan sells a group, not a location. At 14 locations and the 2028 blended ARPU of $98, one group looks like this:

| Per group, 14 locations | Amount | Basis |
|---|---|---|
| Monthly revenue | $1,372 | 14 × $98 |
| Recurring gross profit (89%) | $1,221 | After infrastructure, payments, and allocated support; onboarding excluded |
| CAC, fully loaded | $1,590 | 18 selling hours × $55 + $600 travel |
| Onboarding labour | $1,680 | 14 locations × 2h × $60 |
| Less setup fee | −$1,500 | Charged to the group |
| Net onboarding cost | $180 | $1,680 − $1,500 |
| **Upfront investment** | **$1,770** | CAC + net onboarding |
| **Payback** | **1.45 months** | $1,770 ÷ $1,221 |
| Average life at 1.5% monthly churn | 67 months | 1 ÷ 0.015 |
| **LTV** | **$81,405** | $1,221 × 67 |
| **LTV : CAC** | **51.2x** | $81,405 ÷ $1,590 |

This is the correction to the earlier table. The old 4.8x was a category error: it divided a **per-location** LTV by a **per-group** CAC. A group is 14 locations, so its monthly gross profit is 14× the per-location figure while its CAC is paid once. The arithmetic was also wrong — 18 hours at $55 plus $600 is $1,590, not $1,200.

The 51x is arithmetically correct and strategically misleading, in one direction: it makes the business look too easy. CAC is mostly founder time, the 1.5% churn is an assumption, and the 14-location average is the top of the target range. The stress cases below are the ones to manage to:

| Case | Monthly gross profit | CAC | Upfront | Payback | LTV | LTV:CAC |
|---|---|---|---|---|---|---|
| **Base: 14 locations, 1-in-4 close, 1.5% churn** | **$1,221** | **$1,590** | **$1,770** | **1.45 mo** | **$81,405** | **51.2x** |
| 10-location group | $872 | $1,590 | $1,290 | 1.48 mo | $58,147 | 36.6x |
| 1-in-6 close rate (24 selling hours) | $1,221 | $1,920 | $2,100 | 1.72 mo | $81,405 | 42.4x |
| 2.5% monthly churn | $1,221 | $1,590 | $1,770 | 1.45 mo | $48,843 | 30.7x |
| **Combined: 10 locations, 1-in-6, 2.5% churn, $45 core** | **$748** | **$1,920** | **$1,620** | **2.17 mo** | **$29,904** | **15.6x** |

The combined stress still pays back in 2.2 months and returns 15.6x CAC. **Unit economics are not the constraint on this business. Cash timing and founder hours are.** That is the sentence to carry into the fundraise conversation.

### 10.1b Founder hours — the real capacity constraint

The plan says the founders work unpaid in 2027. It does not say they work part-time without consequence. The 2027 budget, rebuilt from its inputs:

| Activity | Hours | Basis |
|---|---|---|
| Build | 400 | 10 weeks × 40h/week total (the midpoint of the 8–12 week estimate) |
| Selling | 270 | 60 qualified conversations × 3h (180) + 15 pilots × 6h (90) |
| Onboarding | 420 | 15 groups × 14 locations × 2h |
| Support | 60 | ~1h/day from October, when live locations pass 150 |
| Admin | 260 | 5h/week × 52 |
| **Total** | **1,410** | **13.6 hours/week each across two founders** |

Split 60/40 on the build, 30/70 on sales, 50/50 elsewhere:

| Quarter | Founder A (build lead) | Founder B (sales lead) | Part-time capacity |
|---|---|---|---|
| Q1 2027 | 17.6 h/week | 14.7 h/week | 20 h/week each |
| Q2 2027 | 15.4 h/week | 16.4 h/week | 20 h/week each |
| Q3 2027 | 8.0 h/week | 9.7 h/week | 20 h/week each |
| Q4 2027 | 12.0 h/week | 14.6 h/week | 20 h/week each |
| **2027 average** | **13.3 h/week** | **13.8 h/week** | |

**The 16-hour peak was wrong.** The real peak is 17.6 h/week for the build lead in Q1 — 88% of a 20-hour part-time week, with no slack for slippage. At the high end of the build estimate (12 weeks, 480 hours) the Q1 peak is 20.3 h/week, at the ceiling. And if one founder owns the build alone — which is what “product/engineering” as a single function in §12 implies — that founder carries 26.8 h/week in Q1, which is full-time, not part-time. The plan must say which it is: a 10-week, two-founder build at ~18 h/week each, or a 10-week full-time build lead. It cannot claim both the 16-hour peak and a June go-live.

**The setup fee is not a profit centre, and barely a cost centre.** Onboarding runs about two hours per location at $60/hour = $120 per location. A 14-location group costs ~$1,680 to onboard against a $1,500 setup fee: −$180 per group. At three hours per location it is −$1,020; at four hours, −$1,860. Two rules follow: cap onboarding at two hours per location, or raise setup to $2,500. The model holds $1,500 and the two-hour cap. Raising setup to $2,500 adds $31K of revenue in 2028 and $46K in 2029 without changing a single other assumption.

**Break-even at list price — the arithmetic.** Contribution per location is $61.00 − $1.70 infrastructure − $1.77 payment fees = **$57.53/month**. Divide fixed monthly cost by that:

| Fixed monthly cost | Amount | Break-even locations |
|---|---|---|
| Founders unpaid, no support contractor | $1,150 | 1,150 ÷ 57.53 = **20** |
| Plus support contractor ($2,500) | $3,650 | 3,650 ÷ 57.53 = **64** |
| Plus both founders at $75K each ($12,500/mo) | $16,150 | 16,150 ÷ 57.53 = **281** |

At the actual 2027 blended price of $44.96, contribution is $41.96 and the same three break-evens are 27, 87 and 385 locations. The list-price numbers are the steady-state case; the actual-price numbers are what 2027 looks like. Both are shown because a plan that quotes only the first is selling itself a story.

### 10.2 Base case — 2027, month by month

The year-end number is the flattering one. The month that matters is April, and the counts are groups, not a smooth ramp. The per-group schedule below drives the revenue line: six showcase groups live April–June at 20% off, four design partners live July–September at zero, five full-price groups live October–December.

| Month | Live locations | Paying locations | Revenue | COGS | Gross profit | Operating costs | Net | Cash |
|---|---|---|---|---|---|---|---|---|
| Jan | 0 | 0 | $0 | $0 | $0 | $4,617 | −$4,617 | $15,383 |
| Feb | 0 | 0 | $0 | $0 | $0 | $5,617 | −$5,617 | $9,766 |
| Mar | 0 | 0 | $0 | $0 | $0 | $2,916 | −$2,916 | $6,850 |
| **Apr** | **14** | **14** | **$344** | **$22** | **$323** | **$1,250** | **−$927** | **$5,923** |
| May | 42 | 42 | $1,378 | $88 | $1,290 | $1,250 | $40 | $5,963 |
| Jun | 84 | 84 | $3,100 | $197 | $2,903 | $1,400 | $1,503 | $7,465 |
| Jul | 112 | 84 | $4,133 | $286 | $3,846 | $1,250 | $2,596 | $10,062 |
| Aug | 126 | 84 | $4,133 | $322 | $3,811 | $750 | $3,061 | $13,122 |
| Sep | 140 | 84 | $4,133 | $346 | $3,787 | $4,950 | −$1,163 | $11,959 |
| Oct | 168 | 112 | $7,987 | $2,993 | $4,994 | $750 | $4,243 | $16,202 |
| Nov | 196 | 140 | $9,695 | $3,091 | $6,604 | $1,950 | $4,654 | $20,857 |
| Dec | 210 | 154 | $9,476 | $3,120 | $6,356 | $750 | $5,606 | $26,463 |

**Per-group revenue schedule.** List price is $61 per location ($59 core + $2 of boards at 5% attach). The six showcase groups pay $49.20 (20% off core). The four design partners pay nothing until month 13. The five full-price groups pay $61 plus $1,500 setup.

| Group | Type | Locations | Live | Price / loc / mo | Setup | 2027 revenue |
|---|---|---|---|---|---|---|
| S1 | Showcase (20% off) | 14 | Apr | $49.20 | — | $5,855 |
| S2 | Showcase (20% off) | 14 | May | $49.20 | — | $5,166 |
| S3 | Showcase (20% off) | 14 | May | $49.20 | — | $5,166 |
| S4 | Showcase (20% off) | 14 | Jun | $49.20 | — | $4,477 |
| S5 | Showcase (20% off) | 14 | Jun | $49.20 | — | $4,477 |
| S6 | Showcase (20% off) | 14 | Jun | $49.20 | — | $4,477 |
| D1 | Design partner (free) | 14 | Jul | $0.00 | — | $0 |
| D2 | Design partner (free) | 14 | Jul | $0.00 | — | $0 |
| D3 | Design partner (free) | 14 | Aug | $0.00 | — | $0 |
| D4 | Design partner (free) | 14 | Sep | $0.00 | — | $0 |
| F1 | Full price | 14 | Oct | $61.00 | $1,500 | $3,635 |
| F2 | Full price | 14 | Oct | $61.00 | $1,500 | $3,635 |
| F3 | Full price | 14 | Nov | $61.00 | $1,500 | $2,781 |
| F4 | Full price | 14 | Nov | $61.00 | $1,500 | $2,781 |
| F5 | Full price | 14 | Dec | $61.00 | $1,500 | $1,927 |
| **Total** | | **210** | | | **$7,500** | **$44,377** |

That table reconciles to the monthly line in one step: showcase subscription $29,618 + full-price subscription $7,259 + setup $7,500 + design partners $0 = **$44,377**. Nothing is hiding in a blended ARPU.

**What this table actually says.**

1. **You never spend $20,000 in 2027. You spend $14,077 of it by April, and revenue covers costs from May.** The trough is the number that decides whether the company exists; the year-end cash of $26,463 is a consequence, not an achievement.
2. **The trough is caused by front-loaded spend, not by a slow sales ramp.** Design ($5,000 across three milestone payments), legal ($2,500), insurance ($1,500) and brand work ($2,000) all land before the first invoice clears. That is why design is paid in three milestone installments and why the $3,000 Toast certification is a Q3 event. Each trim exists to hold the April floor above $5,000.
3. **First month with revenue above costs: May 2027, by $40. Capital back above $20,000: November 2027.** Both are model outputs, not aspirations, and both are gates in §11.
4. **October's jump is a setup-fee month, not a step change in subscriptions.** Any month with new paying brands will look like that. Do not annualise it.
5. **The showcase program is visible in the location count.** December shows 210 locations live but only 154 paying. Reporting only the first number is how plans flatter themselves; both are in every table from here.

**The rule that makes $20,000 work:** a $5,000 cash floor. If cash falls below $5,000 before recurring revenue passes $3,000/month (roughly 50 locations), stop spending, stop building, and sell — in that order. The model's low point is $5,923 — $923 of headroom. §10.7 shows what happens when the first go-live slips, and why the 15 March checkpoint exists.

### 10.3 2028–2029 — when the hires land, and what gates them

| Quarter | Live locations | Paying locations | Revenue | Costs | Net | Cash | Headcount |
|---|---|---|---|---|---|---|---|
| 2028 Q1 | 336 | 280 | $52,698 | $30,941 | $21,758 | $48,220 | 2 founders + contractors |
| 2028 Q2 | 462 | 406 | $89,010 | $39,136 | $49,874 | $98,094 | 2 founders + contractors |
| 2028 Q3 | 560 | 560 | $137,883 | $88,789 | $49,094 | $147,188 | + engineer (July) |
| 2028 Q4 | 644 | 644 | $179,822 | $112,265 | $67,557 | $214,745 | + growth hire (October) |
| 2029 Q1 | 812 | 812 | $235,857 | $206,960 | $28,898 | $243,642 | founders on salary, + 2nd engineer |
| 2029 Q2 | 980 | 980 | $300,823 | $209,700 | $91,123 | $334,765 | 5 people + support |
| 2029 Q3 | 1,148 | 1,148 | $371,317 | $212,602 | $158,715 | $493,481 | 5 people + support |
| 2029 Q4 | 1,288 | 1,288 | $441,048 | $212,073 | $228,975 | $722,455 | 5 people + support |

**Why costs step from Q4 2027 to Q1 2028 — and why it is smaller than it looks.** Total costs go from $12,654 in Q4 2027 to $30,941 in Q1 2028, a **$18,287 step**, while revenue rises $25,540. Net therefore *rises* from $14,504 to $21,758. **None of the step is a hire; the first hire lands in July.** It is almost entirely the labour of onboarding 31 new groups, plus the fixed legal and tools lines, partly offset by marketing and travel that are now gated to MRR:

| Line | Q4 2027 | Q1 2028 | Change |
|---|---|---|---|
| Onboarding labour | $0 | $15,120 | +$15,120 |
| Legal / insurance / admin | $450 | $3,000 | +$2,550 |
| Tools & SaaS | $1,350 | $2,400 | +$1,050 |
| Payment fees | $788 | $1,528 | +$740 |
| Infrastructure | $916 | $1,393 | +$477 |
| Marketing & content | $450 | $0 | −$450 |
| Travel & demos | $1,200 | $0 | −$1,200 |
| Support contractor | $7,500 | $7,500 | $0 |
| Contract design | $0 | $0 | $0 |
| **Total** | **$12,654** | **$30,941** | **+$18,287** |

The 2028 marketing, travel and contract-design lines are **gated to MRR, not switched on at January 1**. Travel starts in April (the month after MRR crosses $15K), marketing in June (after $25K), and contract design in August (after $35K). That is why Q1 2028 carries $0 of growth marketing and $0 of travel, and why the Q4→Q1 step is $18K rather than $32K. If the gates are too tight and the pipeline needs paid support earlier, the plan should say so and move the gate, not quietly ungate the line.

**Hiring gates.** The model hires only when the revenue to carry the hire already exists — and the gate is written as a threshold, not a date:

- **Engineer:** $35K MRR. The model crosses that run-rate in August 2028 and books the hire from July — a month early, deliberately, because the Gen 2 build queue starts then. If you want the gate literal, move the hire to October and 2028 costs fall $27K.
- **Growth/partnerships:** $50K MRR. The model crosses it in October 2028 and hires that month.
- **Second engineer and founder salaries:** 2029, funded from operating cash, not from the $20,000.
- **Support:** contractor at ~150 live locations — October 2027 in the base case (168 live), at **$2,500/month**. That is the one support rate used everywhere in this plan.

The cash floor across 2028 and 2029 is **$30,502** and **$217,795** respectively. The 2028 floor lands in January, then cash rises every month. There is no month in the base case where the company is at risk after 2027 — and that is precisely why the 2027 discipline matters: it is the only period where the plan is fragile.

### 10.4 Three-year summary — base case

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Locations, end of year | 210 | 644 | 1,288 |
| Paying locations, end of year | 154 | 644 | 1,288 |
| Groups, end of year | 15 | 46 | 92 |
| Exit ARPU per paying location per month | $52 | $96 | $116 |
| Exit MRR | $7,976 | $61,633 | $149,424 |
| Exit ARR | $96K | $740K | $1.79M |
| Revenue recognized | $44,377 | $459,413 | $1,349,045 |
| COGS, including support and onboarding | $10,465 | $104,530 | $226,347 |
| Gross profit | $33,913 | $354,882 | $1,122,699 |
| Gross margin | 76.4% | 77.2% | 83.2% |
| Operating costs | $27,450 | $166,600 | $614,988 |
| **Operating result** | **+$6,463** | **+$188,282** | **+$507,711** |
| Year-end cash | $26,463 | $214,745 | $722,455 |
| Cash floor during year | $5,923 | $30,502 | $217,795 |

**Model notes.** Three conventions explain the shape. Revenue is recognized monthly on average live locations, not by applying an exit ARPU to the whole year. Gross margin includes support and onboarding labour. And 2027 revenue is net of the showcase program — six groups at 20% off, four at zero, setup waived for all ten — so the $61 list build in §10.1 is what a full-price location pays, while $44,377 is what the cohort actually pays.

Founder compensation is inside "operating costs": $0 in 2027, $6,000/month total from July 2028 ($36K for the year), $100K total in 2029. That is below market in every year. Anyone reading this plan should see that number and understand that the founders are the cheapest capital in the business.

### 10.5 Conservative case — with its own cost line

The conservative case is not a scaled-down base case. It is a different company: Gen 1 only, no ordering module, no app, no hires, founders doing support and onboarding themselves, and a sales motion that never compounds. It is the business you get if the showcase cohort converts slowly, Toast says no to ordering, and the agency channel never produces. It is also, deliberately, the case that a two-person team can run for a decade.

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Locations, end of year | 60 | 334 | 904 |
| Blended ARPU per location per month | $48 | $48 | $61 |
| Exit MRR | $2,880 | $16,032 | $55,144 |
| Exit ARR | $35K | $192K | $661K |
| Revenue recognized | $18,540 | $126,000 | $449,326 |
| COGS — support, infrastructure, payment fees | $3,437 | $31,692 | $80,549 |
| Gross margin | 81.5% | 74.9% | 82.1% |
| Founding team pay | $0 | $60,000 ($30K each) | $120,000 ($60K each) |
| Other operating costs | $15,000 | $20,400 | $28,800 |
| **Total costs** | **$18,437** | **$112,092** | **$229,349** |
| **Operating result** | **+$103** | **+$13,909** | **+$219,977** |
| Year-end cash | $20,103 | $34,011 | $253,988 |
| Cash floor during year | $8,678 | $7,841 | $36,847 |

**Read it plainly.** In the conservative case, 2027 is a wash: the company ends the year with the same $20,000 it started with, after paying for legal, design, insurance and a year of tools. 2028 pays each founder $30,000 and clears $14,000. 2029 is a real, if small, business: $449K of revenue, $120K of founder pay, $220K of profit, and $254K in the bank. Nobody gets rich, nobody goes broke, and the company never needs another dollar.

**The important contrast:** the conservative case has a *higher* cash floor ($7,841 vs $5,923) than the base case — but it arrives in early 2028, not 2027, and it arrives while both founders are drawing $2,500/month each. That is thinner than it looks: the flex in the conservative case is founder pay, not spending. If 2028 revenue lags by a quarter, the founders take nothing and the company survives; if it lags by two, they put money in. The base case is not riskier because it is ambitious; it is riskier because it front-loads spending on a designer, certification and travel in the first five months. That is a choice, and it is the right one only if the sales ramp in §9 actually happens. If the first six weeks of 2027 produce fewer than four serious group conversations, cut to the conservative cost line immediately — do not "give it another quarter."

**What the conservative case cannot do:** fund Gen 2. At $449K revenue and $220K profit, the ordering module is affordable from cash flow, but there is no capital for a sales team, an audit, or a bad legal year. The conservative case buys independence, not acceleration.

### 10.6 The $20,000, reconciled

The $20,000 is not spent. Total 2027 cash out is $37,915 and cash collected is $44,377, so the year is operating-cash-positive by $6,463 — and the company still runs $14,077 into its capital in April, because spending leads revenue by roughly three months. That gap, not the annual total, is what the capital is for, and it is why the annual summary alone would mislead a founder into thinking the money is safe.

| 2027 cash out | Amount | When |
|---|---|---|
| Entity, operating agreement, terms, IP assignment | $3,000 | Jan, Jul |
| Design, three milestone payments | $5,000 | Jan–Mar |
| Insurance — tech E&O and cyber | $1,500 | Feb |
| Brand, site, demo environment | $2,000 | Feb |
| Tools and SaaS | $4,500 | monthly |
| Travel, demos, group HQ visits | $5,600 | Mar–Jun, Sep, Nov |
| Toast certification | $3,000 | Sep |
| Marketing and content | $1,050 | Jun–Dec |
| Support contractor | $7,500 | Oct–Dec |
| Admin and miscellaneous | $1,800 | monthly |
| Infrastructure and payment fees | $2,965 | monthly |
| **Total 2027 cash out** | **$37,915** | |
| Cash collected in 2027 | $44,377 | |
| **Net operating cash for the year** | **+$6,463** | |
| **Peak capital deployed (April)** | **$14,077** | |
| **Capital returned** | **November 2027** | |

Capital deployed by month — this is the line to watch, not the budget: Jan $4,617 · Feb $10,234 · Mar $13,150 · Apr $14,077 (peak) · May $14,037 · Jun $12,535 · Jul $9,938 · Aug $6,878 · Sep $8,041 · Oct $3,798 · Nov capital fully recovered. From November the company is funding itself and adding cash every month.

**Six rules that protect the floor.**

1. **$5,000 cash floor, no exceptions.** Not a "buffer," a floor. If it is breached before $3,000/month of recurring revenue, the company stops and sells.
2. **No hire before the gate.** Gates are MRR thresholds in §10.3, not calendar dates. Founders work unpaid in 2027 by design.
3. **Design is paid on delivery.** Three payments against three milestones. Never up front, never on a promise.
4. **Setup fees are not discounted.** The fee covers onboarding at two hours per location and nothing more. Waiving it for the ten showcase groups is a marketing expense, not a pricing policy.
5. **Monthly close, single page.** Cash, MRR, locations, churn, onboarding hours per location, burn. If a number is not on that page, it does not get managed.
6. **Delay protocol.** One trigger: **15 March 2027**, if no showcase group is live. At that date the costs still unspent are April–June travel ($2,400) and the September Toast certification ($3,000). Freeze both. That raises the June trough by $2,400 and year-end cash by $5,400. It has to be pulled in March; by June the cash is already through the floor.

### 10.7 Sensitivities — what breaks it, and by how much

**Phasing, group size and close rate.** Group size 10 means 10 locations per group, not 14, with the same 15 groups by December. 1-in-6 means two showcase go-lives slip from June to July; the cash effect is small, but selling hours rise 50% (see §10.1b). "Slow" is 3 live by June instead of 6, with all 15 by December.

| Case | 2027 revenue | 2027 result | 2027 trough | 2028 cash floor | Verdict |
|---|---|---|---|---|---|
| **Base: 14 locations, 1-in-4, 6 live June** | **$44,377** | **+$6,463** | **$5,923 (Apr)** | **$30,502** | Funds the plan |
| Slower phasing (3 live June) | $35,451 | +$747 | $5,208 (Jun) | $24,787 | Survives by $208 |
| 1-in-6 close rate (4 live June) | $43,000 | +$5,244 | $5,923 (Apr) | $29,284 | Survives; cost is founder hours |
| Average group size 10 | $33,841 | +$1,711 | $5,502 (May) | $24,617 | Survives |
| **Group size 10 + slow phasing** | **$27,465** | **−$4,157** | **$3,815 (Sep)** | **$18,748** | **Fails — 2027 floor breach** |
| 1-in-6 + slow phasing | $32,286 | −$2,326 | $5,208 (Jun) | $20,103 | Survives by $208 |

The combined stress is the one to watch: **10-location groups and a slow ramp breach the $5,000 floor in September ($3,815).** Either condition alone is survivable; both together are not, on $20,000 of capital.

**Price and other sensitivities.**

| Change | Effect | Survives? |
|---|---|---|
| Core price $45 | 2027 result −$1,702; trough $5,582; 2028 floor $20,187; 2029 result $348,226 | Yes, thinner |
| Core price $35 | 2027 result −$7,534; trough $5,310; 2028 floor $12,819; 2029 result $234,308 | Marginal |
| Core price $25 | 2027 trough $2,715; 2028 floor $5,451; 2029 low −$694 | **No — floor breach in 2027, insolvent in 2029** |
| Group churn 2.5%/month | Per-group LTV $48,843; LTV:CAC 30.7x | Marginal, still investable |
| Setup fee raised to $2,500 | +$31K revenue in 2028, +$46K in 2029, no cost change | Improves |
| Toast denies ordering | 2028 revenue $407,887; 2029 revenue $1,079,933; 2029 result $246,402 | Yes — smaller, still profitable |
| Onboarding runs 4 hours/location | Setup is −$1,860 per group; 2028 onboarding labour nearly doubles and GM falls to ~65% | Tolerable, but it becomes an agency |
| Support tickets double after 150 locations | Support becomes a $5,500/month line; 2028 margin −8 points | Yes — normal scaling cost |

**Timing case — first go-live June, no revenue through May.** The schedule shifts two months: S1 goes live in June instead of April, and the last three full-price groups slip into 2028. Monthly cash, with and without the protocol:

| Month | Live | Paying | Revenue (no protocol) | Cash (no protocol) | Revenue (protocol) | Cash (protocol) |
|---|---|---|---|---|---|---|
| Jan 2027 | 0 | 0 | $0 | $15,383 | $0 | $15,383 |
| Feb | 0 | 0 | $0 | $9,766 | $0 | $9,766 |
| Mar | 0 | 0 | $0 | $6,850 | $0 | $6,850 |
| Apr | 0 | 0 | $0 | $5,600 | $0 | $6,400 |
| **May** | **0** | **0** | **$0** | **$4,350** | **$0** | **$5,950** |
| **Jun** | **14** | **14** | **$344** | **$3,273** | **$344** | **$5,673** |
| Jul | 42 | 42 | $1,378 | $3,313 | $1,378 | $5,713 |
| Aug | 84 | 84 | $3,100 | $5,465 | $3,100 | $7,865 |
| **Sep** | **112** | **84** | **$4,133** | **$4,362** | **$4,133** | **$9,762** |
| Oct | 126 | 84 | $4,133 | $7,422 | $4,133 | $12,822 |
| Nov | 140 | 84 | $4,133 | $9,259 | $4,133 | $14,659 |
| Dec | 168 | 112 | $7,987 | $13,502 | $7,987 | $18,902 |

Without the protocol, the floor is breached in May ($4,350), June ($3,273), July ($3,313) and September ($4,362). The low is $3,273 in June — $1,727 below the floor. With the 15 March protocol, the trough is **$5,673** (June) and year-end cash is **$18,902**. The protocol buys the trough with the April–June travel saving only; the September certification saving does not touch the trough, only the year-end.

But the protocol is not free. Moving the September 2027 certification into 2028 delays Gen 2 ordering by roughly six months. In the model, that cuts 2028 revenue from $426,056 to $391,066 (−$34,990) and 2028 operating result from $155,960 to $124,985. 2028 monthly cash, side by side:

| Month 2028 | Revenue (no protocol) | Cash (no protocol) | Revenue (protocol) | Cash (protocol) |
|---|---|---|---|---|
| Jan | $11,622 | $15,126 | $11,622 | $20,526 |
| Feb | $14,770 | $19,735 | $14,502 | $24,875 |
| Mar | $18,199 | $27,602 | $17,535 | $32,097 |
| Apr | $21,909 | $39,000 | $20,721 | $42,341 |
| May | $25,901 | $52,703 | $24,059 | $54,255 |
| Jun | $30,339 | $70,644 | $27,715 | $69,648 |
| Jul | $35,224 | $76,257 | $31,689 | $73,829 |
| Aug | $40,555 | $86,974 | $36,635 | $80,740 |
| Sep | $48,129 | $103,975 | $43,567 | $94,311 |
| Oct | $54,897 | $119,976 | $49,820 | $105,383 |
| Nov | $59,878 | $142,434 | $54,352 | $122,475 |
| Dec | $64,633 | $169,462 | $58,850 | $143,887 |

The protocol raises the 2028 floor (January, $20,526 vs $15,126) because the 2027 saving carries into the opening balance, but it lowers 2028 year-end cash by $25,575. **It is a 2027 survival tool with a 2028 cost.** If Toast can run certification in parallel without delaying Gen 2, the trade-off disappears; that is a question for the Toast representative, not a modelling assumption.

**Toast denies ordering — the v2.2 vs v2.4 reconciliation.** The two versions did not remove the same lines:

| Version | Core | Menu boards | Ordering | App | Setup | 2029 revenue | 2029 result |
|---|---|---|---|---|---|---|---|
| v2.2 sensitivity | Kept | **Removed (~$282K)** | **Removed (~$267K)** | **Removed (~$34K)** | Kept | $773K | −$40K |
| v2.4 sensitivity | Kept | Kept | **Removed (~$269K)** | Kept | Kept | $1.080M | +$246K |
| v2.4, app also removed | Kept | Kept | **Removed (~$269K)** | **Removed (~$34K)** | Kept | $1.046M | +$213K |

v2.2 removed menu boards, which are a Gen 1 surface and do not depend on Toast's Orders API. It also removed the Gen 3 app, which can run as a menu and merchandise channel without order injection, and it kept base-case costs that included the Gen 2 hires. That is why it landed at $773K and −$40K. **v2.4 removes only the revenue line that actually depends on the Ordering API.** If the app is removed as well, 2029 revenue falls another $34K and the result another $33K — the conclusion is unchanged. The honest statement is not "Toast denial kills the company"; it is "Toast denial turns a $1.35M plan into a $1.05–1.08M one, and the cost line has to follow."

### 10.8 What the model cannot tell you

It cannot tell you whether restaurant groups will pay $59 per location to fix a menu problem they have lived with for a decade. It cannot tell you whether Toast approves the partner application, or at what revenue share. It cannot price the value of the case studies the showcase cohort produces, and it cannot model the founder who quits in month fourteen. Those are the risks in §13, not spreadsheet cells.

What it can tell you is narrower and more useful: **at these prices, these costs, and this ramp, the company survives its own plan with $5,923 in the bank at the worst moment, and never needs another dollar to reach $1.35M of revenue and $1.79M of exit ARR.** If those assumptions are wrong by 10%, it still works. If they are wrong by half, the conservative case still works. If Toast says no to ordering, the company is smaller but profitable. If first go-live slips two months, the floor breaks unless the 15 March protocol is pulled — and the protocol itself costs 2028 growth. That is what "funded" means: not that the plan is right, but that being wrong is survivable, with the trade-offs written down.

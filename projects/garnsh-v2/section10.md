## 10. Financials

*Every figure in this section comes from a 36-month monthly model (`model.py`, cash basis, January 2027 – December 2029). The model is the source of truth, not this prose: change an assumption there and every table here — and the deck — moves with it. All figures are founder assumptions. Pricing is validated only by the Q1 2027 conversations; the ramp is a plan, not a forecast.*

### 10.1 Unit economics — the engine under everything

The price is $59 per location per month for publishing, plus $40 for menu boards. Blended revenue per location is that price stack multiplied by attach rates, nothing else.

| Revenue per location per month | 2027 | 2028 | 2029 |
|---|---|---|---|
| Core publishing — $59 × 100% | $59 | $59 | $59 |
| Menu boards — $40 × attach rate | $2 (5%) | $22 (55%) | $26 (65%) |
| Gen 2 ordering — $99 × attach rate | — | $17 (17%) | $28 (28%) |
| Gen 3 app — $149 × attach rate | — | — | $5 (3.5%) |
| **Blended ARPU** | **$61** | **$98** | **$118** |

Boards attach at almost nothing in 2027 because the first cohort is buying publishing to fix a specific problem, not screens. The ordering attach rate (17% of the installed base in Gen 2's first year) is deliberately conservative — it is the one number that depends on Toast, and it should not be load-bearing in year one.

Cost to serve, per location per month:

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Infrastructure, CDN, image processing | $1.70 | $1.70 | $1.70 |
| Payment processing (2.9% of revenue) | $1.77 | $2.84 | $3.42 |
| Support labour, allocated | $4.67 | $5.88 | $7.94 |
| Onboarding labour, one-time, amortized | — | $8.75 | $5.82 |
| **Fully loaded gross margin** | **86.8%** | **80.5%** | **83.9%** |

Two honest notes on that table. First, the **software** gross margin is ~95%; the fully loaded number is lower because support and onboarding are real people. We report the fully loaded number because it is the one that pays salaries. Second, 2027 carries no onboarding labour cost only because the founders do it unpaid — that is a cash margin, not an economic one. The margin dips in 2028 as contracted onboarding absorbs 31 new groups, then recovers as templated onboarding and self-serve replace hours. If it does not recover past 85% by 2030, the business is a services company with a software veneer, and it should be priced and staffed accordingly.

**Lifetime value and acquisition cost.** Recurring gross margin (excluding one-time onboarding) is 89%. That is the right basis for LTV, because onboarding does not recur.

| | Multi-unit group | Single location |
|---|---|---|
| ARPU per month | $98 (2028 blend) | $59 |
| Recurring gross margin | 89% | 89% |
| Monthly logo churn | 1.5% | 3.5% |
| Average life | ~67 months | ~29 months |
| **LTV** | **~$5,800** | **~$1,500** |
| CAC, fully loaded | $1,200 | $150 |
| Payback, including $120 onboarding per location | ~15 months | ~5 months |
| **LTV : CAC** | **~4.8x** | **~10x** |

CAC on a group is not a marketing line item; it is mostly founder time. The $1,200 assumes roughly 18 hours of selling and onboarding per closed group at $55/hour fully loaded, plus $600 of travel or event cost, at a one-in-four close rate on qualified conversations. If the close rate is one in six, CAC becomes $1,800 and LTV:CAC falls to 3.2x — still investable, but that is the number to watch, not the marketing budget.

**The setup fee is not a profit centre, and barely a cost centre.** Onboarding runs about two hours per location at $60/hour = $120 per location. A 12-location brand therefore costs ~$1,440 to onboard against a $1,500 setup fee: $60 of gross margin. At three hours per location it flips to −$660 per brand. Two rules follow: cap onboarding at two hours per location, or raise setup to $2,500. The model holds $1,500 and the two-hour cap. Raising setup to $2,500 adds $31K of revenue in 2028 and $46K in 2029 without changing a single other assumption — it is the cheapest improvement available, and it is a Q1 decision.

**Break-even is earlier than the plan previously claimed.** At $61 ARPU and 87% margin, running costs are covered at **22 paying locations** with founders unpaid and no support contractor, **70 locations** once a $2,750/month support contractor is on payroll, and **239 locations** if both founders pay themselves $75K. The last number is the one that matters for whether this becomes a business that outlives the founders' patience. The first number is why the $20,000 works.

### 10.2 Base case — 2027, month by month

The year-end number is the flattering one. The month that matters is May.

| Month | Locations | Revenue | COGS | Gross profit | Operating costs | Net | Cash |
|---|---|---|---|---|---|---|---|
| Jan | 0 | $0 | $0 | $0 | $4,617 | −$4,617 | $15,383 |
| Feb | 0 | $0 | $0 | $0 | $5,617 | −$5,617 | $9,766 |
| Mar | 6 | $0 | $5 | −$5 | $2,916 | −$2,921 | $6,845 |
| Apr | 14 | $480 | $31 | $449 | $1,250 | −$801 | $6,044 |
| **May** | **32** | **$1,150** | **$72** | **$1,078** | **$1,250** | **−$172** | **$5,872** |
| Jun | 58 | $2,340 | $144 | $2,196 | $1,400 | $796 | $6,667 |
| Jul | 82 | $3,850 | $231 | $3,619 | $1,250 | $2,369 | $9,037 |
| Aug | 104 | $5,301 | $312 | $4,989 | $750 | $4,239 | $13,276 |
| Sep | 126 | $10,015 | $486 | $9,529 | $4,950 | $4,579 | $17,855 |
| Oct | 152 | $8,479 | $1,982 | $6,497 | $750 | $5,747 | $23,602 |
| Nov | 180 | $14,626 | $2,206 | $12,420 | $1,950 | $10,470 | $34,071 |
| Dec | 210 | $11,895 | $2,176 | $9,719 | $750 | $8,969 | $43,040 |

**What this table actually says.**

1. **You never spend $20,000 in 2027. You spend $14,128 of it by May, and revenue takes over from June.** The trough is the number that decides whether the company exists; the year-end cash of $43K is a consequence, not an achievement.
2. **The trough is caused by front-loaded spend, not by a slow sales ramp.** Design ($6,000), legal ($2,500), insurance ($1,500) and brand work ($2,000) all land before the first invoice clears. That is why design is paid in three milestone installments, why the $3,000 Toast certification is a Q3 event, and why the brand spend is $2,000 rather than the $2,500 originally budgeted.
3. **Run the ramp 30% slower and the trough is $5,410, not zero.** Slower sales cost you time and growth, not survival. That is the correct shape for a plan this cheap — but only if the front-loaded spending stays disciplined.
4. **First month with revenue above costs: June 2027. Capital back above $20,000: October 2027.** Both are model outputs, not aspirations, and both are gates in §11.
5. **September's revenue spike is a setup-fee month, not a step change in subscriptions.** Any month with a new paying brand will look like that. Do not annualise it.

**The rule that makes $20,000 work:** a $5,000 cash floor. If cash falls below $5,000 before recurring revenue passes $3,000/month (roughly 50 locations), stop spending, stop building, and sell — in that order. The model never gets close; a plan that needs luck to avoid its own floor is not a plan.

### 10.3 2028–2029 — when the hires land, and what gates them

| Quarter | Locations | Revenue | Costs | Net | Cash | Headcount |
|---|---|---|---|---|---|---|
| 2028 Q1 | 318 | $71,241 | $40,972 | $30,269 | $73,308 | 2 founders + contractors |
| 2028 Q2 | 426 | $105,585 | $42,519 | $63,066 | $136,374 | 2 founders + contractors |
| 2028 Q3 | 534 | $142,809 | $89,149 | $53,660 | $190,034 | + engineer (July) |
| 2028 Q4 | 640 | $181,567 | $113,323 | $68,244 | $258,278 | + growth hire (October) |
| 2029 Q1 | 793 | $236,703 | $203,266 | $33,437 | $291,716 | founders on salary, + 2nd engineer |
| 2029 Q2 | 946 | $299,172 | $205,857 | $93,315 | $385,030 | 5 people + support |
| 2029 Q3 | 1,099 | $366,076 | $208,578 | $157,498 | $542,528 | 5 people + support |
| 2029 Q4 | 1,250 | $429,834 | $211,206 | $218,629 | $761,157 | 5 people + support |

**Hiring gates.** The model hires only when the revenue to carry the hire already exists — and the gate is written as a threshold, not a date:

- **Engineer:** hire at $35K MRR sustained for two months (model reaches it in Q2 2028; hire lands July).
- **Growth/partnerships:** hire at $50K MRR (model reaches it Q4 2028).
- **Second engineer and founder salaries:** 2029, funded from operating cash, not from the $20,000.
- **Support:** contractor at ~150 live locations (October 2027 in the model), which is exactly when support becomes a founder's whole day.

The cash floor across 2028 and 2029 is $49,835 and $263,101 respectively. There is no month in the base case where the company is at risk after mid-2027 — and that is precisely why the 2027 discipline matters: it is the only period where the plan is fragile.

### 10.4 Three-year summary — base case

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Locations, end of year | 210 | 640 | 1,250 |
| Groups, end of year | 15 | 46 | 92 |
| Blended ARPU per location per month | $61 | $98 | $118 |
| Exit MRR | $12,810 | $62,720 | $147,500 |
| Exit ARR | $154K | $753K | $1.77M |
| Revenue recognized | $58,136 | $501,202 | $1,331,785 |
| COGS, including support and onboarding | $7,646 | $97,864 | $213,918 |
| Gross profit | $50,490 | $403,338 | $1,117,867 |
| Gross margin | 86.8% | 80.5% | 83.9% |
| Operating costs | $27,450 | $188,100 | $614,988 |
| **Operating result** | **+$23,040** | **+$215,238** | **+$502,879** |
| Year-end cash | $43,040 | $258,278 | $761,157 |
| Cash floor during year | $5,872 | $49,835 | $263,101 |

**Why these numbers differ from the previous draft.** Two corrections, both arithmetic:

1. **Revenue is ramp-adjusted.** The earlier draft applied each year's exit ARPU to the whole year, which inflates revenue by 4–6%. 2029 revenue is $1.33M, not $1.42M; exit ARR is $1.77M, which is the more meaningful figure anyway. Nothing about the business changed — the table got honest.
2. **Gross margin includes support and onboarding labour.** Reporting 88% while paying contractors to onboard is how plans lie to their own founders. The fully loaded number is 80.5% in 2028, recovering to 83.9% in 2029. That is a good margin for a product with this much human contact, and a bad margin for a company that tells itself it is pure software.

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
| COGS, including support and onboarding | $3,584 | $31,798 | $80,875 |
| Gross margin | 80.7% | 74.8% | 82.0% |
| Founder pay | $0 | $60,000 ($30K each) | $120,000 ($60K each) |
| Support and contractors | $6,319 | $24,000 | $55,000 |
| Tools, travel, marketing, legal, admin | $8,534 | $56,294 | $73,474 |
| **Total costs** | **$18,437** | **$112,092** | **$229,349** |
| **Operating result** | **+$103** | **+$13,909** | **+$219,977** |
| Year-end cash | $20,103 | $34,011 | $253,988 |
| Cash floor during year | $8,678 | $20,000 | $34,000 |

**Read it plainly.** In the conservative case, 2027 is a wash: the company ends the year with the same $20,000 it started with, after paying for legal, design, insurance and a year of tools. 2028 pays each founder $30,000 and clears $14,000. 2029 is a real, if small, business: $449K of revenue, $120K of founder pay, $220K of profit, and $254K in the bank. Nobody gets rich, nobody goes broke, and the company never needs another dollar.

**The important contrast:** the conservative case has a *higher* cash floor ($8,678 vs $5,872) than the base case. Spending less is safer. The base case is not riskier because it is ambitious; it is riskier because it front-loads spending on a designer, certification and travel in the first five months. That is a choice, and it is the right one only if the sales ramp in §9 actually happens. If the first six weeks of 2027 produce fewer than four serious group conversations, cut to the conservative cost line immediately — do not "give it another quarter."

**What the conservative case cannot do:** fund Gen 2. At $449K revenue and $220K profit, the ordering module is affordable from cash flow, but there is no capital for a sales team, an audit, or a bad legal year. The conservative case buys independence, not acceleration.

### 10.6 The $20,000, reconciled

The earlier draft listed a use-of-funds table that added to $20,000 and implied the capital was spent in full. It is not: total 2027 cash spend is $35,150, revenue funds $23,040 of it, and the capital funds the gap — but the gap is $12,110 while the peak drawdown is $14,128, because spending leads revenue by about two months. That two-month lag is the entire reason to model monthly.

| 2027 cash out | Amount | When |
|---|---|---|
| Entity, operating agreement, terms, IP assignment | $3,000 | Jan, Jul |
| Design, three milestone payments | $6,000 | Jan–Mar |
| Insurance — tech E&O and cyber | $1,500 | Feb |
| Brand, site, demo environment | $2,000 | Feb |
| Tools and SaaS | $4,500 | monthly |
| Travel, demos, group HQ visits | $5,600 | Mar–Jun, Sep, Nov |
| Toast certification | $3,000 | Sep |
| Marketing and content | $1,050 | Jun–Dec |
| Support contractor | $4,500 | Oct–Dec |
| Admin and miscellaneous | $1,800 | monthly |
| Infrastructure and payment fees | $2,200 | monthly |
| **Total 2027 cash out** | **$35,150** | |
| Funded by revenue | −$23,040 | |
| **Funded by capital** | **$12,110** | |
| **Peak capital deployed (May)** | **$14,128** | |

Capital deployed by month — this is the line to watch, not the budget: Jan $4,617 · Feb $10,234 · Mar $13,155 · Apr $13,956 · **May $14,128 (peak)** · Jun $13,333 · Jul $10,963 · Aug $6,724 · Sep $2,145 · Oct capital fully recovered. From November the company is funding itself and adding cash every month.

**Five rules that protect the floor.**

1. **$5,000 cash floor, no exceptions.** Not a "buffer," a floor. If it is breached before $3,000/month of recurring revenue, the company stops and sells.
2. **No hire before the gate.** Gates are MRR thresholds in §10.3, not calendar dates. Founders work unpaid in 2027 by design.
3. **Design is paid on delivery.** Three payments against three milestones. Never up front, never on a promise.
4. **Setup fees are not discounted.** The fee covers onboarding at two hours per location and nothing more. Waiving it for the ten showcase groups is a marketing expense, not a pricing policy.
5. **Monthly close, single page.** Cash, MRR, locations, churn, onboarding hours per location, burn. If a number is not on that page, it does not get managed.

### 10.7 Sensitivities — what breaks it, and by how much

| Change | Effect | Survives? |
|---|---|---|
| 2027 ramp 30% slower (147 locations, not 210) | 2027 revenue $42,904; operating result +$8,689; trough $5,410 | Yes, comfortably. Slower growth, same floor. |
| Blended ARPU 10% lower everywhere | 2029 revenue $1.21M (−$127K); operating result $380K | Yes. The model is not ARPU-fragile at these prices. |
| Group churn 2.5%/month instead of 1.5% | LTV falls to ~$3,500; LTV:CAC ~2.9x; 2029 locations materially lower | Marginal. Still investable, but the growth story weakens and CAC discipline becomes the whole game. |
| Setup fee raised to $2,500 | +$31K revenue in 2028, +$46K in 2029, no cost change | Improves. Do it unless the first ten conversations say otherwise. |
| Toast denies ordering access entirely | 2028 revenue $363K, 2029 revenue $773K, 2029 operating result −$40K at base-case cost structure | **No — at base-case costs.** The fix is immediate: fall back to the conservative cost line. This is why that case is printed with its own numbers. |
| Onboarding runs 4 hours/location | Setup fee is −$1,140 per brand; 2028 gross margin falls ~4 points | Tolerable, but it converts a software business into an agency. Automate it or cap it. |
| Support tickets double after 150 locations | Support contractor becomes a $5,500/month line; 2028 margin −3 points | Yes. This is normal SaaS scaling cost, not a crisis. |

The asymmetry is worth stating: the base case can absorb slower sales and lower prices. It cannot absorb **Toast denying ordering access while spending at base-case levels** — because the 2028–29 cost line assumes ordering revenue exists. That single dependency is why §7 is the critical path and why the conservative cost line is a switch to flip, not a scenario to admire.

### 10.8 What the model cannot tell you

It cannot tell you whether restaurant groups will pay $59 per location to fix a menu problem they have lived with for a decade. It cannot tell you whether Toast approves the partner application, or at what revenue share. It cannot price the value of the case studies the showcase cohort produces, and it cannot model the founder who quits in month fourteen. Those are the risks in §13, not spreadsheet cells.

What it can tell you is narrower and more useful: **at these prices, these costs, and this ramp, the company survives its own plan with $5,900 in the bank at the worst moment, and never needs another dollar to reach $1.3M of revenue.** If those assumptions are wrong by 10%, it still works. If they are wrong by half, the conservative case still works. If Toast says no, you cut costs and the conservative case works. That is what "funded" means: not that the plan is right, but that being wrong is survivable.

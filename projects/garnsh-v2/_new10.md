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
| Payment processing (2.9% of revenue) | $1.23 | $2.49 | $3.33 |
| Support labour, allocated | $4.56 | $5.87 | $7.94 |
| Onboarding labour, one-time, amortized | — | $10.14 | $6.45 |
| **Cost to serve per live location-month** | **$7.49** | **$20.20** | **$19.42** |
| Revenue per live location-month | $44.96 | $85.72 | $114.90 |
| **Fully loaded gross margin** | **83.3%** | **76.4%** | **83.1%** |

Three honest notes. First, the **software** gross margin is ~95%; the fully loaded number is lower because support and onboarding are real people. We report the fully loaded number because it is the one that pays salaries. Second, 2027 carries no onboarding labour cost only because the founders do it unpaid — that is a cash margin, not an economic one. Third, the gap between the $61 list build and the $44.96 actual in 2027 is the showcase program: six groups at 20% off, four at zero, and 56 free locations in the cost denominator. That is a deliberate marketing spend, and §9 prices it at ~$40,700 of foregone revenue. The margin recovers to 83% in 2029 as the cohort pays list and onboarding is templated. If it does not pass 85% by 2030, the business is a services company with a software veneer, and it should be priced and staffed accordingly.

**Lifetime value and acquisition cost.** Recurring gross margin (excluding one-time onboarding) is ~88%. That is the right basis for LTV, because onboarding does not recur.

| | Multi-unit group | Single location |
|---|---|---|
| ARPU per month | $98 (2028 blend) | $59 |
| Recurring gross margin | 88% | 88% |
| Monthly logo churn | 1.5% | 3.5% |
| Average life | ~67 months | ~29 months |
| **LTV** | **~$5,770** | **~$1,480** |
| CAC, fully loaded | $1,200 | $150 |
| Payback, including $120 onboarding per location | ~15 months | ~5 months |
| **LTV : CAC** | **~4.8x** | **~9.9x** |

The per-location LTV above is not a group-level payback. A group is 14 locations, so its monthly gross profit is 14× the per-location figure while its CAC is paid once; the per-group rebuild, including the combined stress case, is the subject of Issue 4 and will replace this table. Do not use the 4.8x ratio to size a sales budget until that rebuild lands.

**The setup fee is not a profit centre, and barely a cost centre.** Onboarding runs about two hours per location at $60/hour = $120 per location. A 12-location brand therefore costs ~$1,440 to onboard against a $1,500 setup fee: $60 of gross margin. At three hours per location it flips to −$660 per brand; at four hours, −$1,860. Two rules follow: cap onboarding at two hours per location, or raise setup to $2,500. The model holds $1,500 and the two-hour cap. Raising setup to $2,500 adds $31K of revenue in 2028 and $46K in 2029 without changing a single other assumption — it is the cheapest improvement available, and it is a Q1 decision.

**Break-even at list price.** At $61 ARPU and 83% fully loaded margin, running costs are covered at **22 paying locations** with founders unpaid and no support contractor, **74 locations** once a $2,750/month support contractor is on payroll, and **309 locations** if both founders pay themselves $75K. The last number is the one that matters for whether this becomes a business that outlives the founders' patience. The first number is why the $20,000 works.

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
| Oct | 168 | 112 | $7,987 | $1,993 | $5,993 | $750 | $5,243 | $17,202 |
| Nov | 196 | 140 | $9,695 | $2,091 | $7,604 | $1,950 | $5,654 | $22,857 |
| Dec | 210 | 154 | $9,476 | $2,120 | $7,356 | $750 | $6,606 | $29,463 |

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

1. **You never spend $20,000 in 2027. You spend $14,077 of it by April, and revenue covers costs from May.** The trough is the number that decides whether the company exists; the year-end cash of $29,463 is a consequence, not an achievement.
2. **The trough is caused by front-loaded spend, not by a slow sales ramp.** Design ($5,000 across three milestone payments), legal ($2,500), insurance ($1,500) and brand work ($2,000) all land before the first invoice clears. That is why design is paid in three milestone installments, why the $3,000 Toast certification is a Q3 event, and why the brand and design budgets were trimmed. Each of those trims exists to hold the April floor above $5,000.
3. **First month with revenue above costs: May 2027, by $40. Capital back above $20,000: November 2027.** Both are model outputs, not aspirations, and both are gates in §11.
4. **October's jump is a setup-fee month, not a step change in subscriptions.** Any month with new paying brands will look like that. Do not annualise it.
5. **The showcase program is visible in the location count.** December shows 210 locations live but only 154 paying. Reporting only the first number is how plans flatter themselves; both are in every table from here.

**The rule that makes $20,000 work:** a $5,000 cash floor. If cash falls below $5,000 before recurring revenue passes $3,000/month (roughly 50 locations), stop spending, stop building, and sell — in that order. The model's low point is $5,923 — $923 of headroom, which is thin rather than comfortable. §10.7 shows what happens when the first go-live slips.

### 10.3 2028–2029 — when the hires land, and what gates them

| Quarter | Live locations | Paying locations | Revenue | Costs | Net | Cash | Headcount |
|---|---|---|---|---|---|---|---|
| 2028 Q1 | 318 | 262 | $48,992 | $42,127 | $6,865 | $36,328 | 2 founders + contractors |
| 2028 Q2 | 426 | 370 | $81,015 | $43,607 | $37,409 | $73,736 | 2 founders + contractors |
| 2028 Q3 | 534 | 534 | $129,950 | $90,577 | $39,373 | $113,109 | + engineer (July) |
| 2028 Q4 | 640 | 640 | $178,166 | $114,784 | $63,382 | $176,492 | + growth hire (October) |
| 2029 Q1 | 793 | 793 | $230,794 | $204,955 | $25,839 | $202,331 | founders on salary, + 2nd engineer |
| 2029 Q2 | 946 | 946 | $290,839 | $207,476 | $83,364 | $285,694 | 5 people + support |
| 2029 Q3 | 1,099 | 1,099 | $355,919 | $210,143 | $145,775 | $431,470 | 5 people + support |
| 2029 Q4 | 1,250 | 1,250 | $425,699 | $212,706 | $212,994 | $644,463 | 5 people + support |

**Why costs step from Q4 2027 to Q1 2028.** Total costs go from $9,654 in Q4 2027 to $42,127 in Q1 2028 — a $32,473 step — while revenue rises $21,834. Net therefore falls from $17,504 to $6,865 despite 80% revenue growth. **None of the step is a hire; the first hire lands in July.** It is the 2028 operating plan switching on at 1 January, plus the labour of onboarding 31 new groups:

| Line | Q4 2027 | Q1 2028 | Change |
|---|---|---|---|
| Onboarding labour | $0 | $12,960 | +$12,960 |
| Support contractor | $4,500 | $7,500 | +$3,000 |
| Marketing & content | $450 | $6,000 | +$5,550 |
| Travel & demos | $1,200 | $4,500 | +$3,300 |
| Contract design | $0 | $3,000 | +$3,000 |
| Legal / insurance / admin | $450 | $3,000 | +$2,550 |
| Tools & SaaS | $1,350 | $2,400 | +$1,050 |
| Payment fees | $788 | $1,420 | +$632 |
| Infrastructure | $916 | $1,347 | +$431 |
| **Total** | **$9,654** | **$42,127** | **+$32,473** |

The marketing, travel, legal and contract-design lines are calendar-driven, not revenue-driven: they start on 1 January at their annual run-rate. The onboarding line is variable but paid before the subscription ramps. That is a legitimate choice for a year in which 430 locations are added, but it should be visible, not buried in an annual total. The 2029 Q1 step — operating costs from $86,400 to $153,747 a quarter — *is* a hire step: founders go on salary and the second engineer starts.

**Hiring gates.** The model hires only when the revenue to carry the hire already exists — and the gate is written as a threshold, not a date:

- **Engineer:** $35K MRR. The model crosses that run-rate in August 2028 and books the hire from July — a month early, deliberately, because the Gen 2 build queue starts then. If you want the gate literal, move the hire to October and 2028 costs fall $27K.
- **Growth/partnerships:** $50K MRR. The model crosses it in October 2028 and hires that month.
- **Second engineer and founder salaries:** 2029, funded from operating cash, not from the $20,000.
- **Support:** contractor at ~150 live locations — October 2027 in the base case (168 live), which is exactly when support becomes a founder's whole day.

The cash floor across 2028 and 2029 is **$28,926** and **$179,015** respectively. The 2028 floor lands in January, before the year's revenue has built; it is the only month in 2028 that burns cash. There is no month in the base case where the company is at risk after 2027 — and that is precisely why the 2027 discipline matters: it is the only period where the plan is fragile.

### 10.4 Three-year summary — base case

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Locations, end of year | 210 | 640 | 1,250 |
| Paying locations, end of year | 154 | 640 | 1,250 |
| Groups, end of year | 15 | 46 | 92 |
| Exit ARPU per paying location per month | $52 | $95 | $116 |
| Exit MRR | $7,976 | $60,948 | $144,529 |
| Exit ARR | $96K | $731K | $1.73M |
| Revenue recognized | $44,377 | $438,123 | $1,303,251 |
| COGS, including support and onboarding | $7,465 | $102,994 | $220,291 |
| Gross profit | $36,913 | $335,129 | $1,082,960 |
| Gross margin | 83.2% | 76.5% | 83.1% |
| Operating costs | $27,450 | $188,100 | $614,988 |
| **Operating result** | **+$9,463** | **+$147,029** | **+$467,972** |
| Year-end cash | $29,463 | $176,492 | $644,463 |
| Cash floor during year | $5,923 | $28,926 | $179,015 |

**Model notes.** Three conventions explain the shape. Revenue is recognized monthly on average live locations, not by applying an exit ARPU to the whole year. Gross margin includes support and onboarding labour. And 2027 revenue is net of the showcase program — six groups at 20% off, four at zero, setup waived for all ten — so the $61 list build in §10.1 is what a full-price location pays, while $44,377 is what the cohort actually pays. The difference is the price of the case studies, and §9 shows it.

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

The $20,000 is not spent. Total 2027 cash out is $34,915 and cash collected is $44,377, so the year is operating-cash-positive by $9,463 — and the company still runs $14,077 into its capital in April, because spending leads revenue by roughly three months. That gap, not the annual total, is what the capital is for, and it is why the annual summary alone would mislead a founder into thinking the money is safe.

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
| Support contractor | $4,500 | Oct–Dec |
| Admin and miscellaneous | $1,800 | monthly |
| Infrastructure and payment fees | $2,965 | monthly |
| **Total 2027 cash out** | **$34,915** | |
| Cash collected in 2027 | $44,377 | |
| **Net operating cash for the year** | **+$9,463** | |
| **Peak capital deployed (April)** | **$14,077** | |
| **Capital returned** | **November 2027** | |

Capital deployed by month — this is the line to watch, not the budget: Jan $4,617 · Feb $10,234 · Mar $13,150 · Apr $14,077 (peak) · May $14,037 · Jun $12,535 · Jul $9,938 · Aug $6,878 · Sep $8,041 · Oct $2,798 · Nov capital fully recovered. From November the company is funding itself and adding cash every month.

**Six rules that protect the floor.**

1. **$5,000 cash floor, no exceptions.** Not a "buffer," a floor. If it is breached before $3,000/month of recurring revenue, the company stops and sells.
2. **No hire before the gate.** Gates are MRR thresholds in §10.3, not calendar dates. Founders work unpaid in 2027 by design.
3. **Design is paid on delivery.** Three payments against three milestones. Never up front, never on a promise.
4. **Setup fees are not discounted.** The fee covers onboarding at two hours per location and nothing more. Waiving it for the ten showcase groups is a marketing expense, not a pricing policy.
5. **Monthly close, single page.** Cash, MRR, locations, churn, onboarding hours per location, burn. If a number is not on that page, it does not get managed.
6. **Delay protocol.** If no group is live by 1 May 2027, freeze travel and demos, move Toast certification to 2028, and hold marketing at zero. That is worth ~$6,200 and it is the difference between a $3,273 low and a $6,473 one (§10.7). The protocol has to be pulled in April; by June the cash is already through the floor.

### 10.7 Sensitivities — what breaks it, and by how much

| Change | Effect | Survives? |
|---|---|---|
| **First go-live slips to June** (no revenue through May; schedule shifts two months) | 2027 revenue $25,207; operating result −$5,498; trough $3,273 (June); year-end cash $14,502; capital not returned in 2027 | **No.** Floor breached in May, June, July and September |
| Same delay **plus the delay protocol** (freeze travel Mar–Jun, move certification) | 2027 revenue $25,207; operating result +$702; trough $6,473; year-end cash $20,702; capital returned December | Yes — barely, and only if pulled in April |
| **Slower phasing** (3 live by June instead of 6; all 15 by December) | 2027 revenue $35,451; operating result +$2,747; trough $5,208 (June); year-end cash $22,747 | Yes — $208 above the floor |
| Core price $45 (boards and modules unchanged) | 2027 revenue $35,969; 2027 result +$1,298; trough $5,582; 2029 result $313,666 (−$154K) | Yes, thinner. §8 has the full table |
| Core price $35 | 2027 revenue $29,963; 2027 result −$4,534; trough $5,310; 2028 cash floor $8,964 | Marginal. One bad month from a top-up |
| Core price $25 | 2027 trough $2,715; 2028 cash floor −$4,557 | **No.** 2027 floor breach, insolvent in 2028 |
| Group churn 2.5%/month instead of 1.5% | LTV falls to ~$3,460; LTV:CAC ~2.9x; 2029 locations materially lower | Marginal. Still investable, but the growth story weakens and CAC discipline becomes the whole game |
| Setup fee raised to $2,500 | +$31K revenue in 2028, +$46K in 2029, no cost change | Improves. Do it unless the first ten conversations say otherwise |
| Toast denies ordering access entirely | 2028 revenue −$52,678 ($385,445); 2029 revenue −$266,847 ($1,036,404); 2029 operating result ~$209K | Yes, but the company is a $1M niche, not a $1.3M platform. Fall back to the conservative cost line and do not hire for Gen 2 |
| Onboarding runs 4 hours/location | Setup is −$1,860 per brand; 2028 onboarding labour doubles and gross margin falls ~12 points to ~65% | Tolerable, but it converts a software business into an agency. Automate it or cap it |
| Support tickets double after 150 locations | Support contractor becomes a $5,500/month line; 2028 margin −8 points | Yes. This is normal SaaS scaling cost, not a crisis |

The asymmetry is worth stating: the base case can absorb lower prices, slower sales and losing Gen 2. It cannot absorb **a two-month delay in first go-live without the delay protocol**, because the front-loaded design, legal, insurance and brand spend lands before any revenue. That is the single most likely failure mode, and it is a timing failure, not a demand failure.

**Timing case — first go-live June, no revenue through May.** The schedule shifts two months: S1 goes live in June instead of April, the showcase cohort follows, and the last three full-price groups slip into 2028. Monthly cash:

| Month | Live | Paying | Revenue | Costs | Net | Cash |
|---|---|---|---|---|---|---|
| Jan | 0 | 0 | $0 | $4,617 | −$4,617 | $15,383 |
| Feb | 0 | 0 | $0 | $5,617 | −$5,617 | $9,766 |
| Mar | 0 | 0 | $0 | $2,916 | −$2,916 | $6,850 |
| Apr | 0 | 0 | $0 | $1,250 | −$1,250 | $5,600 |
| **May** | **0** | **0** | **$0** | **$1,250** | **−$1,250** | **$4,350** |
| **Jun** | **14** | **14** | **$344** | **$1,422** | **−$1,078** | **$3,273** |
| Jul | 42 | 42 | $1,378 | $1,338 | $40 | $3,313 |
| Aug | 84 | 84 | $3,100 | $947 | $2,153 | $5,465 |
| **Sep** | **112** | **84** | **$4,133** | **$5,236** | **−$1,104** | **$4,362** |
| Oct | 126 | 84 | $4,133 | $1,072 | $3,061 | $7,422 |
| Nov | 140 | 84 | $4,133 | $2,296 | $1,837 | $9,259 |
| Dec | 168 | 112 | $7,987 | $2,744 | $5,243 | $14,502 |

The floor is breached in May ($4,350), June ($3,273), July ($3,313) and again in September ($4,362). The low is **$3,273 in June — $1,727 below the floor.** The plan as capitalised does not survive a two-month delay. With the delay protocol — no travel or demos March–June, certification moved to 2028 — the trough is **$6,473** and year-end cash is **$20,702**; the protocol is worth $3,200 of cash in 2027 and avoids the second September dip. That is the contingency, and it is cheap. It only works if it is pulled in April.

The old "ramp 30% slower" case has been removed. It assumed a revenue shape with no operational cause; a go-live delay is the risk the company actually faces.

### 10.8 What the model cannot tell you

It cannot tell you whether restaurant groups will pay $59 per location to fix a menu problem they have lived with for a decade. It cannot tell you whether Toast approves the partner application, or at what revenue share. It cannot price the value of the case studies the showcase cohort produces, and it cannot model the founder who quits in month fourteen. Those are the risks in §13, not spreadsheet cells.

What it can tell you is narrower and more useful: **at these prices, these costs, and this ramp, the company survives its own plan with $5,923 in the bank at the worst moment, and never needs another dollar to reach $1.30M of revenue and $1.73M of exit ARR.** If those assumptions are wrong by 10%, it still works. If they are wrong by half, the conservative case still works. If Toast says no to ordering, the company is smaller but profitable. If first go-live slips two months, the floor breaks unless the delay protocol is pulled — which is why that protocol is written down and not left to judgement. That is what "funded" means: not that the plan is right, but that being wrong is survivable.

# Garnsh — Assumptions and Evidence Register

**Version 3.0** · 11 November 2026

This register separates what is verified from what is modeled and what still needs evidence. A claim is not investor-grade because it appears in a deck; it is investor-grade when the evidence behind it is named.

**Classification key**

- **VERIFIED** — supported by a primary source or direct observation.
- **MODELED** — a planning assumption or forecast. It may be reasonable, but it is not evidence.
- **UNVERIFIED** — requires external confirmation, customer validation, legal review or a third-party quote.

| # | Claim | Class | Evidence / basis | Owner | Next action / deadline |
|---|---|---|---|---|---|
| 1 | Toast had ~189,000 locations at Q3 2026, up 21% year over year | VERIFIED | Toast Q3 2026 results, 3 Nov 2026 | Founders | Re-check at each Toast earnings release |
| 2 | Toast annualized recurring revenue was ~$2.5B at Q3 2026 | VERIFIED | Toast Q3 2026 results | Founders | Re-check quarterly |
| 3 | Toast added ~8,500 net new locations in Q3 2026 | VERIFIED | Toast Q3 2026 results | Founders | Re-check quarterly |
| 4 | 10–20% of Toast locations sit in groups of 10+ | MODELED | No public breakdown by group size; assumption | Founders | Validate with Toast partner rep or industry data |
| 5 | The Gen 1 SAM is $13.8M–$27.7M ARR | MODELED | 18,900–37,800 locations × $61 × 12 | Founders | Recalculate after pricing interviews |
| 6 | Garnsh has 0 signed design partners, 0 live locations and 0 paying customers | VERIFIED | Internal status, 11 Nov 2026 | Founders | Update monthly |
| 7 | The current build is a demo, not a production service | VERIFIED | Internal review | Founders | Production readiness review before first paid go-live |
| 8 | Toast Menus API production credentials are partner-gated | VERIFIED | Toast developer documentation, 2026 | Founders | Keep current |
| 9 | Toast standard API access is read-only, per-location, Menus V2, reporting-oriented | VERIFIED | Toast developer documentation, 2026 | Founders | Keep current |
| 10 | Customer-supplied credentials may lawfully power a public-facing website | UNVERIFIED | No written Toast position; terms are ambiguous | Counsel + Toast rep | Written opinion before first public use; 15 Jan 2027 |
| 11 | Toast partner fees and ordering revenue share | UNVERIFIED | Fees unpublished; ~30% ordering share is 2019 reporting, not current | Toast rep | Written terms before Gen 2 pricing; 31 Mar 2027 |
| 12 | Toast certification timeline for Gen 2 | UNVERIFIED | Process is gated; no dated commitment | Toast rep | Written timeline by day 120 |
| 13 | Toast Websites is view-only; Online Ordering and Local menus cannot differ | VERIFIED | Toast support documentation, 2026 | Founders | Keep current |
| 14 | Toast's US restaurant base is ~20% of US eating and drinking establishments | VERIFIED | Toast Q3 2026 commentary; industry counts 700,000+ | Founders | Keep current |
| 15 | Core price of $59 per location per month is achievable | UNVERIFIED | Founder hypothesis; no invoices | Founders | 10 pricing interviews; 31 Jan 2027 |
| 16 | Menu boards attach at 5% (2027), 55% (2028), 65% (2029) | MODELED | Founder assumption; no customer data | Founders | Measure first 10 groups |
| 17 | Gen 2 ordering attaches at 17% (2028), 28% (2029) | MODELED | Founder assumption; depends on Toast approval | Founders | Reassess after certification |
| 18 | Blended ARPU is $61 (2027), $98 (2028), $118 (2029) | MODELED | Price stack × attach assumptions | Founders | Rebuild after pricing interviews |
| 19 | Setup fee is $1,500 per brand | MODELED | Founder hypothesis | Founders | Test in first 10 sales conversations |
| 20 | Onboarding takes 2 hours per location at $60/hour | MODELED | Founder estimate | Founders | Time first 20 locations |
| 21 | Setup fee loses $180 per 14-location group at 2h/location | VERIFIED (arithmetic) | $1,680 cost − $1,500 fee | Founders | Raise fee to $2,500 or cap hours |
| 22 | Group logo churn is 1.5%/month; location churn 0.5%/month | MODELED | Comparable SaaS assumption; no Garnsh data | Founders | Measure from first cohort; Q4 2027 |
| 23 | Downside churn is 2.5% group / 1.0% location | MODELED | Stress assumption | Founders | Re-run after 6 months of data |
| 24 | CAC is $1,590 per group (18 selling hours × $55 + $600) | MODELED | Founder time and travel estimate | Founders | Track actual hours and travel per close |
| 25 | Close rate is 1-in-4 on qualified conversations | MODELED | Founder assumption; no pipeline yet | Founders | Measure first 40 conversations |
| 26 | 2027 plan: 15 gross groups, 14 net, 193 live, 142 paying | MODELED | Cohort model | Founders | Update monthly |
| 27 | 2028 plan: 46 net groups; 2029: 90 net groups | MODELED | Cohort model with churn and gross adds | Founders | Reforecast after 2027 |
| 28 | 2027 revenue is $42,195; 2028 $440,883; 2029 $1,287,970 | MODELED | Cohort model, `model_v3.py` | Founders | Re-run quarterly |
| 29 | 2027 economic result is −$20,558 after $25,200 imputed founder onboarding | MODELED | Cohort model | Founders | Decide whether founders absorb or capitalize onboarding |
| 30 | Paid 2027 onboarding exhausts the $20,000 | VERIFIED (model arithmetic) | Cash trough −$6,386 in Oct 2027 | Founders | Do not pay for 2027 onboarding without new capital |
| 31 | The base case returns capital in December 2027 | MODELED | Cash model; trough $5,923, YE $23,892 | Founders | Track monthly |
| 32 | Downside 2029 is insolvent at the planned cost base | MODELED | Revenue $694K, COGS $173K, opex $615K | Founders | Pre-commit the lean 2029 cost response |
| 33 | Setup fee at 10 locations is +$300; at 12 locations +$60 | VERIFIED (arithmetic) | 2h/location at $60 | Founders | Use group-size pricing where needed |
| 34 | A 14-location group pays $826/month core, $1,386 with boards | VERIFIED (arithmetic) | 14 × $59; 14 × $99 | Founders | Include in sales sheet |
| 35 | Toast plan may add ~$50/location/month if the group is not on Essentials | UNVERIFIED | No Toast quote | Toast rep | Get three written quotes; 31 Jan 2027 |
| 36 | Competitor prices: ChowNow $229–$449; Popmenu $159–$499; Owner.com $249 + 5%; Lunchbox $300–$499 | PARTLY VERIFIED | Published roundups, Oct 2026; some are reported, not published | Founders | Verify each vendor's current public price |
| 37 | Marqii and BentoBox pricing | UNVERIFIED | Not published | Founders | Request quotes; 31 Jan 2027 |
| 38 | A 30-day paid pilot converts to annual at list | UNVERIFIED | Proposed sales motion; no pilot run | Founders | Run first 4 pilots; Jun 2027 |
| 39 | The 12-month design-partner program produces case studies and references | UNVERIFIED | Proposed; no commitments | Founders | Sign 10 partners; Jun 2027 |
| 40 | The team can build Gen 1 in 8–12 weeks | MODELED | Founder estimate; current demo | Founders | Re-estimate after technical review; 15 Jan 2027 |
| 41 | Founder capacity is 1,410 hours in 2027, peak 17.6h/week each | MODELED | Activity budget in §8.2 | Founders | Track weekly; flag >20h/week |
| 42 | Support contractor costs $2,500/month from 150 locations | MODELED | Market rate assumption | Founders | Get two quotes; Q3 2027 |
| 43 | 2028 marketing, travel and design can be MRR-gated | MODELED | Management policy | Founders | Enforce in monthly close |
| 44 | Gen 2 card handling stays with Toast under the Orders API | UNVERIFIED | Assumed; determines PCI scope | Toast rep + counsel | Written confirmation before Gen 2 build |
| 45 | The company can reach $1.29M revenue by 2029 without outside capital | MODELED | Cohort model; requires founder onboarding, churn and price assumptions to hold | Founders | Reforecast after 2027 |

## What cannot be resolved without founder input

1. **Who performs 2027 onboarding.** If the founders do it, cash works and the economics do not. If a contractor does it, the company needs roughly $25,000 more capital.
2. **The final price.** $59 is a hypothesis. Ten interviews decide whether the $39/$69/$45 ladder is needed.
3. **Toast legal position.** Whether customer credentials may power a public website is a binary legal question.
4. **Founder role split and equity.** The plan assumes two equal partners; the operating agreement must say who owns which function.
5. **Design-partner commitments.** Zero are signed. The 2027 plan depends on 10.

*Anything not listed as VERIFIED above should be treated as a planning assumption, not a fact.*

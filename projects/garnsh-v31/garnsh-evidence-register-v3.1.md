# Garnsh — Evidence and Assumptions Register v3.1

**11 November 2026** · Companion to Business Plan v3.1 and Investor Deck v3.1

Classification key: **VERIFIED** — supported by an identifiable, relevant source. **MODELED** — produced by the financial model or management assumptions. **UNVERIFIED** — not yet established. **TARGET** — intended future milestone. **ACTUAL** — demonstrably achieved by Garnsh.

> A claim is not VERIFIED because it appears in an earlier Garnsh document. Primary sources only. Where only a secondary source exists, it is labelled and the limitation is stated.

---

## 1. Company status

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Garnsh has signed customers | 0 | ACTUAL | Founders | 11 Nov 2026 | No contract, LOI or pilot agreement exists |
| Garnsh has live locations | 0 | ACTUAL | Founders | 11 Nov 2026 | No menu is published for a customer |
| Garnsh has paying customers | 0 | ACTUAL | Founders | 11 Nov 2026 | Pre-revenue |
| Garnsh has completed customer interviews | 0 | ACTUAL | Founders | 11 Nov 2026 | The 60-conversation figure is a target |
| Founder capital committed | $20,000 | ACTUAL | Founders | 11 Nov 2026 | $10,000 each, per plan; bank evidence not sighted |
| Founders' names, backgrounds, time commitment | Not documented | UNVERIFIED | — | — | Placeholders in plan §8.1; must be completed before external circulation |
| Product stage | Interactive demo | ACTUAL | Demo reviewed | 11 Nov 2026 | Not a production service |
| Toast approval, certification, production credentials | None | UNVERIFIED | — | — | No application outcome exists at this date |
| Toast marketplace listing | None | UNVERIFIED | — | — | Requires partner approval |

## 2. Market

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Toast restaurant locations | ~189,000 | VERIFIED | Toast Q3 2026 results, investors.toasttab.com; Business Wire | 3 Nov 2026 | Up 21% year over year; ~8,500 net adds in Q3 |
| Toast ARR | $2.5B | VERIFIED | Same | 3 Nov 2026 | Up 24% |
| Share of Toast locations in groups of 10+ | 10–20% | MODELED | Management estimate | 11 Nov 2026 | Toast does not disclose the breakdown. Not survey data |
| Serviceable locations | 18,900–37,800 | MODELED | 189,000 × 10–20% | 11 Nov 2026 | Arithmetic on a modeled input |
| Gen 1 revenue per location | $61/month | MODELED | $59 core + $2 boards at 2027 attach | 11 Nov 2026 | Uses the lowest board attach year |
| Gen 1 serviceable market | $13.8M–$27.7M ARR | MODELED | 18,900–37,800 × $61 × 12 | 11 Nov 2026 | Excludes ordering, apps, payments |
| 2029 locations in the plan | 1,182 | MODELED | Model v3.1 | 11 Nov 2026 | Net of churn |
| Share of serviceable market in 2029 | 3.1%–6.3% | MODELED | 1,182 ÷ 18,900–37,800 | 11 Nov 2026 | Niche outcome, stated as such |
| US eating and drinking establishments | 700,000+ | VERIFIED | Industry reporting | 2024–2026 | Context only; not used in sizing |

## 3. Problem and product

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Groups maintain menus on four or more surfaces | 4 surfaces | UNVERIFIED | Founder research | 11 Nov 2026 | Not measured across a sample; should be tested in the first ten interviews |
| Menu errors cause comps, reviews or legal risk | Qualitative | UNVERIFIED | Founder research | 11 Nov 2026 | Plausible; no incident data collected |
| Preview, publish, version history, rollback | Demonstrated in demo | ACTUAL | Demo | 11 Nov 2026 | Production hardening required |
| Per-location mapping and overrides | Demonstrated in demo | ACTUAL | Demo | 11 Nov 2026 | — |
| Last-known-good serving | Designed only | UNVERIFIED | Architecture note | 11 Nov 2026 | Not built |
| CSV/Sheets import and manual editor | Not built | TARGET | Plan §3.3 | Q1 2027 | Build item |
| Production readiness | 10–12 weeks of work | MODELED | Founder estimate | 11 Nov 2026 | Not estimated by an outside engineer |
| WCAG 2.1 AA accessibility | Not assessed | UNVERIFIED | — | 11 Nov 2026 | Ship gate |
| Gen 1 is not ordering, payments, inventory, loyalty or real-time sync | Boundary | ACTUAL | Product definition | 11 Nov 2026 | Enforced in plan, deck, contract |

## 4. Toast integration

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Standard API access is read-only | Read-only, no write access | VERIFIED | *Standard API access overview*, doc.toasttab.com/doc/devguide/devApiAccessUserGuide.html | 11 Nov 2026 | Document states write access and sandbox are not included |
| Standard access is location-specific | One request per location | VERIFIED | Same | 11 Nov 2026 | Explicit in the document |
| Standard access includes sandbox | No | VERIFIED | Same | 11 Nov 2026 | Listed as not included |
| Menus API `GET` is supported for standard, partner and custom integrations | Yes | VERIFIED | *API overview*, doc.toasttab.com/doc/devguide/apiOverview.html | 11 Nov 2026 | — |
| Partner access requires application and certification | Yes | VERIFIED | *Partner integration overview*, doc.toasttab.com/doc/devguide/apiPartnerIntegrationOverview.html | 11 Nov 2026 | Scoped read/write on behalf of customers who share data with Toast |
| Customer credentials may power a public-facing commercial product | Not established | UNVERIFIED | — | 11 Nov 2026 | Contract/legal question. Blocks paid public publishing until answered in writing |
| Partner fees and revenue share | Unknown | UNVERIFIED | — | 11 Nov 2026 | Not assumed in the model |
| Certification timeline | Unknown | UNVERIFIED | — | 11 Nov 2026 | Day-120 gate requires a written timeline |
| Toast plan needed to enable API access, and its cost | Unknown | UNVERIFIED | — | 11 Nov 2026 | Interview question; excluded from model |

## 5. Competition

Prices are published list prices captured on 11 November 2026. They are not like-for-like.

| Competitor | Price | Basis | Class | Source | Date |
|---|---|---|---|---|---|
| Toast native (Websites, Online Ordering, Delphi) | Not publicly disclosed; bundled | Per location, plan-dependent | VERIFIED (not disclosed) | toasttab.com; ressto.co (secondary, ~$75/mo) | 11 Nov 2026 |
| Marqii | $90 / $145 / $180 / $250 per month | Per location, annual contract | VERIFIED | marqii.com/pricing | 11 Nov 2026 |
| Popmenu | $179 / $299 / $499 per month | Per location; additional locations ~$300/mo (secondary) | VERIFIED (base); secondary (add-on) | get.popmenu.com/pricing; restolabs.com | 11 Nov 2026 |
| BentoBox | ~$119 / $279 / $479 website tiers; ordering ~$49/mo + $0.99/order | Per location, tiered | UNVERIFIED — secondary only | orderitto.com; getsauce.com | 2026 |
| Owner.com | $249/mo + 5% of orders, or $499/mo flat | Per restaurant | VERIFIED | owner.com/pricing | 11 Nov 2026 |
| ChowNow | From $229/mo annual ($249 monthly); setup $119–$499 | Per restaurant | VERIFIED | get.chownow.com/pricing | 11 Nov 2026 |
| Lunchbox | Quote-based | Enterprise contract | VERIFIED (not disclosed) | lunchbox.io | 11 Nov 2026 |
| Web agencies | Quote-based | Project + retainer | VERIFIED (not disclosed) | — | 11 Nov 2026 |
| Marqii is an adjacent competitor, not merely a partner | Yes | — | MODELED | Product comparison | 11 Nov 2026 | It sells menu management and distribution |
| BentoBox is Clover-only in 2026 | Claimed | — | UNVERIFIED — secondary only | servestack.ai comparison | Oct 2026 | Not confirmed on BentoBox's own site |

## 6. Pricing and unit economics

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Core publishing price | $59/location/month | MODELED | Founder assumption | 11 Nov 2026 | Untested; ten interviews before fixing |
| Menu boards add-on | $40/location/month | MODELED | Founder assumption | 11 Nov 2026 | Untested |
| Onboarding fee | $120/location, $1,500 minimum | MODELED | Cost-recovery at 2h × $60 | 11 Nov 2026 | v3.1 change from flat $1,500 |
| Onboarding labor rate | $60/hour | MODELED | Founder estimate | 11 Nov 2026 | No contractor quote |
| Onboarding hours | 2h/location | MODELED | Founder estimate | 11 Nov 2026 | Downside 4h |
| 14-location monthly revenue | $1,372 | MODELED | 14 × $98 blended ARPU | 11 Nov 2026 | 2028 ARPU including boards |
| Recurring gross profit | $1,221 (89%) | MODELED | After infrastructure, payment fees, support | 11 Nov 2026 | Excludes onboarding |
| CAC | $1,590 | MODELED | 18 selling hours × $55 + $600 | 11 Nov 2026 | No measured cohort |
| Upfront investment | $1,590 | MODELED | CAC + net onboarding ($0) | 11 Nov 2026 | — |
| Payback | 1.3 months | MODELED | 1,590 ÷ 1,221 | 11 Nov 2026 | — |
| Monthly revenue churn | 2.0% | MODELED | 1.5% group + 0.5% location | 11 Nov 2026 | No cohort data |
| LTV | $61,054 | MODELED | $1,221 × 50 months | 11 Nov 2026 | Upper bound, not a benchmark |
| LTV:CAC | 38.4x | MODELED | 61,054 ÷ 1,590 | 11 Nov 2026 | Downside churn: 21.9x |
| Customer's incremental Toast plan cost | Unknown | UNVERIFIED | — | 11 Nov 2026 | Could add $25–50/location/month; excluded |

## 7. Go-to-market and funnel

| Claim or assumption | Value | Class | Source | Date | Notes |
|---|---|---|---|---|---|
| Qualified conversations 2027 | 60 | TARGET | Plan §6.1 | 11 Nov 2026 | 40 in H1, 20 in H2 |
| Pilot-to-conversation rate | 40% | MODELED | Founder assumption | 11 Nov 2026 | Untested |
| Pilot-to-paid conversion | 62.5% | MODELED | Founder assumption | 11 Nov 2026 | Untested; high for a first cohort |
| Gross groups 2027 | 15 | TARGET | Plan §6.1 | 11 Nov 2026 | 4 free, 6 discounted, 5 full price |
| Group logo churn 2027 | 1.5%/month | MODELED | Founder assumption | 11 Nov 2026 | ~0.9 groups lost in 2027 |
| Net groups at 31 Dec 2027 | 14.0 | MODELED | Model v3.1 | 11 Nov 2026 | — |
| Paying locations at 31 Dec 2027 | 192 | MODELED | Model v3.1 | 11 Nov 2026 | Free partners converted after 90 days |
| Design-partner program cost | $30,595 | MODELED | Plan §6.3 arithmetic | 11 Nov 2026 | v3.0 twelve-month offer: $91,286 |
| Public case studies from design partners | 4 | TARGET | Program terms | 11 Nov 2026 | Contractual obligation, not a guaranteed outcome |
| Agency revenue share | 25% | MODELED | Founder proposal | 11 Nov 2026 | Not negotiated with any agency |
| Paid acquisition viable at this price | No | MODELED | Cash arithmetic | 11 Nov 2026 | $10–15K per group vs $20K capital |

## 8. Financial model

All figures below are MODELED outputs of `model_v31.py` and reconcile to the workbook and plan.

| Metric | 2027 | 2028 | 2029 | Class |
|---|---|---|---|---|
| Revenue | $45,946 | $361,320 | $918,657 | MODELED |
| Cost of revenue excl. onboarding | $10,491 | $49,011 | $120,590 | MODELED |
| Onboarding labor (cash) | $0 | $62,160 | $94,080 | MODELED |
| Gross margin | 77.2% | 69.2% | 76.6% | MODELED |
| Operating expenses | $27,451 | $168,100 | $471,000 | MODELED |
| Economic result after founder labor | −$17,197 | +$82,049 | +$232,987 | MODELED |
| Cash from operations | +$25,643 | +$142,529 | +$326,227 | MODELED |
| Year-end cash | $45,643 | $188,172 | $514,399 | MODELED |
| Minimum cash in year | $6,750 | $50,990 | $193,782 | MODELED |
| Exit ARR | $130,278 | $577,049 | $1,177,318 | MODELED |
| Net groups | 14.0 | 45.7 | 89.5 | MODELED |
| Live / paying locations | 192 | 615 | 1,182 | MODELED |
| Founder onboarding imputed (2027) | $25,200 | — | — | MODELED |
| Base-case cash trough | $6,750 (April 2027) | — | — | MODELED |
| Combined stress trough | −$16,194 (May 2027) | — | — | MODELED |
| Combined stress + response trough | $7,085 (June 2027) | — | — | MODELED |
| Expansion contribution | $0 | −$65,212 | +$136,376 | MODELED |
| Cash reserve floor | $5,000 | — | — | MODELED — management policy |

## 9. Open questions and owners

| Question | Why it matters | Owner | Needed by |
|---|---|---|---|
| May customer-supplied Toast credentials power a public-facing menu in a commercial product? | Legal exposure and product design | Founders + counsel | Before the first paid public page; day 120 at the latest |
| Will Toast grant partner access, on what terms and when? | Gen 2 viability and scalable ingestion | Founder A | Day 120 |
| What is the customer's incremental Toast plan cost? | May raise the real price by 40–85% | Founder B | First ten interviews |
| Will groups pay $59 per location? | Base case revenue | Founder B | Ten interviews, Q1 2027 |
| What are real churn, CAC and conversion? | LTV, payback and growth | Both | First cohort, six months |
| Can 90 days produce a publishable case study? | Design-partner program design | Both | First two partners |
| Will any partner accept a 25% agency revenue share? | Channel economics | Founder B | First agency conversation |
| Who are the founders, and what is the equity split? | External credibility | Both | Before any external circulation |
| Is the 10–20% multi-unit share defensible? | Market size | Both | Before a raise; $5–15K dataset decision |
| Does the company need a $25–30K bridge? | Survival under stress | Both | Before launch if onboarding is outsourced |

---

*Register compiled 11 November 2026. Source URLs were accessed that day. Where a source is secondary, the row says so.*

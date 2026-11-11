# Garnsh

## Menu publishing and control for multi-location restaurant groups

**Business Plan v3.1** · 11 November 2026

Confidential. Prepared for the founders, advisers and prospective investors.

> **Status:** pre-revenue. Garnsh has a working product demo, no signed customers and no live locations. Toast access and the right to use customer credentials for public-facing menus are unverified. Every financial figure is modeled, not achieved. Targets are labelled as targets.

---

## 1. Executive Summary

Garnsh is a menu publishing and control platform for restaurant groups running 10 or more locations on Toast. It gives a group one place to prepare a menu, map it to each location, preview every guest-facing surface, publish deliberately, and roll back if something is wrong.

A group maintains one menu in Toast but presents it on four surfaces: its website, a hosted page, QR codes and in-store boards. Each is updated by hand. Prices drift, discontinued items linger, one location's prices appear at another, and a bad publish can leave a blank board during service. Nobody owns the problem end to end.

Gen 1 is the business: centralized menu management, per-location mapping and overrides, branded hosted menus and website embeds, QR menus, digital menu boards, preview and deliberate publishing, version history and rollback. It is not an ordering platform, a payment processor, a live inventory system, a loyalty product or a real-time sync engine. Ordering (Gen 2) and branded apps (Gen 3) are optional expansions, excluded from the base case.

The customer is a regional fast-casual or casual-dining group with 10–50 locations, all on Toast, with a brand worth protecting and a named owner for menu presentation. The buyer is the VP of Marketing, the Director of Operations or the founder-operator. Garnsh is sold on control, not on being the cheapest menu page.

Pricing is $59 per location per month for core publishing, $40 for menu boards, and a cost-recovery setup fee of $120 per location with a $1,500 minimum. The setup fee is a v3.1 change: a flat $1,500 loses money above 12 locations and badly at the top of the target range.

**2027 objective.** Sign 15 groups from 60 qualified conversations and 24 paid pilots: four free design partners for 90 days, six discounted showcase partners and five full-price customers. Reach 14 net groups and 192 live locations by December.

**Financial headline — Scenario A, Gen 1 only, modeled.**

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Revenue | $45,946 | $361,320 | $918,657 |
| Gross margin | 77.2% | 69.2% | 76.6% |
| Operating expenses | $27,451 | $168,100 | $471,000 |
| Economic result after founder labor | −$17,197 | +$82,049 | +$232,987 |
| Cash from operations | +$25,643 | +$142,529 | +$326,227 |
| Year-end cash | $45,643 | $188,172 | $514,399 |
| Net groups | 14.0 | 45.7 | 89.5 |
| Live locations | 192 | 615 | 1,182 |
| Exit ARR | $130,278 | $577,049 | $1,177,318 |

Two facts matter more than the headline. 2027 is cash-positive only because the founders perform onboarding unpaid; valuing that time at $60 per hour turns +$25,643 of operating cash into a **−$17,197 economic result**. And the plan survives its base case with **$6,750** at the April trough, $1,750 above the $5,000 floor. Paying a contractor for 2027 onboarding pushes the trough to **−$1,878** and breaches the reserve; it needs about $7,000 of additional capital, not a large round.

The company is capitalized with $20,000 from the two founders and is not raising now. The milestones that justify a round are ten paying groups, six months of measured churn, a clear Toast position and a measured CAC.

**What this plan does not claim.** No signed customers, no live locations, no Toast approval, no certification, no measured churn, CAC or conversion. The product is a demo, not a production service. The first business test is whether multi-location groups will pay for menu publishing alone. Section 10 sets out the gates that decide whether to continue.

---

## 2. Problem and Customer

### 2.1 The operational problem

Each surface is maintained separately, usually by someone whose real job is running restaurants. The failures repeat:

- **Price drift.** Toast says $16.25; the website says $14.50. The guest who notices is a comp, a bad review and, in some jurisdictions, a consumer-protection risk.
- **Dead items and stale pages.** A discontinued item stays on the QR page for weeks, and the website menu is two cycles old, because removing either means editing every surface.
- **Wrong-location menus.** One location's prices appear at another.
- **No safety net.** A broken import or a bad publish leaves a blank board during service.

For a 10-location group this is a stream of small public errors multiplied by every surface, with no single person able to fix them at the source.

### 2.2 Why existing answers do not fit

**Toast's native tools** get an operator online; they are not built to give a brand team publishing control across an estate. The menu channel on Toast Websites is view-only, and Online Ordering runs on Toast's pages with limited customization. Garnsh does not claim Toast cannot display a menu; it claims Toast does not provide versioned, per-location publishing across surfaces it does not host.

**Agencies** build the site and maintain the menu by hand. They are the real incumbent: slow, expensive and the reason menus go stale — and a potential reseller channel.

**Suites** — Marqii, Popmenu, BentoBox, Owner.com, Lunchbox, ChowNow — solve listings, websites, ordering or marketing. Menu control is a feature inside a larger product, priced around ordering or marketing economics (Section 4.2).

**The API wall.** Toast's Menus API is real but gated. Standard access is read-only and location-specific; partner access requires an application and certification. Whether a customer's own credentials may lawfully power a public-facing commercial product is **unverified** (Section 7).

### 2.3 The initial customer

**Ideal customer:** a regional fast-casual or casual-dining group with 10–50 locations, all on Toast, with a brand worth protecting and a named owner for menu presentation. Multi-unit franchisees in that band fit the same profile.

Below 10 locations the pain is real but the budget and brand risk are small. Above 50 the security review and sales cycle exceed a two-person company's capacity. The plan starts in the middle.

**Buyer:** VP of Marketing, Director of Operations, or the founder-operator. **Triggers:** a price change that appears in one place and not another, a rebrand, a new location, a menu cycle change, or an agency handover. These are the moments when manual updating becomes visible and budget appears.

---

## 3. Product and Solution

### 3.1 What Gen 1 does

1. **Menu documents.** Ingest from Toast (when approved access exists), a CSV/Google Sheets import, or the manual editor.
2. **Per-location mapping.** Assign menus, prices and overrides to each location and surface, with a group view.
3. **Branded surfaces.** Website embed on the group's own domain, a Garnsh-hosted page per location, a QR phone view, and in-store digital boards.
4. **Preview and publish.** See every surface before publishing; publish selected locations deliberately rather than syncing silently.
5. **Recovery.** Version history, one-click rollback, and last-known-good serving if an upstream source fails.

The workflow is ingest → normalize → map → preview → publish → serve. The architecture is deliberately boring: an ingestion service, a publishing and versioning layer, and four renderers. The hard engineering is menu-data hygiene and publishing safety, not rendering.

### 3.2 What Gen 1 does not do

Gen 1 does not read or display 86 status, live stock or table availability. It is not real-time: a change reaches guests only when someone previews and publishes it. It does not take orders, process payments, run loyalty or provide a branded app, and it does not replace Toast as the system of record. These are product boundaries, not gaps for the next sprint.

### 3.3 What exists today

The current build is an interactive demo. It demonstrates per-location menu rendering, the preview and publish flow, version history and rollback. It is not a production service.

To be sellable it needs a production ingestion path and the CSV/Sheets bridge, tenant authentication and isolation, per-location asset management, board scheduling, an accessibility pass to WCAG 2.1 AA, and bulk publish with an unpublished-change alert. Without the last two, a 14-location group repeats the same click fourteen times and "deliberate publish" becomes a tidy name for silent drift. The estimate is 10–12 weeks of focused work for two founders; the 2027 plan is sized to it.

| Capability | Today | At launch |
|---|---|---|
| Per-location rendering, preview, publish, version history, rollback | Demonstrated in demo | Production |
| Last-known-good serving | Architecture only | Production build required |
| Toast ingestion | Not built; access unverified | Conditional on Section 7 |
| CSV/Sheets import, tenant isolation, audit log | Not built | Ship gate |
| WCAG 2.1 AA accessibility | Not assessed | Ship gate |

### 3.4 Roadmap

- **Gen 1 (2027):** menu publishing. The only product in the base case.
- **Gen 2 (2028, gated):** ordering on the group's own site, writing orders into Toast through the certified Orders API. Requires certification and a commercial agreement. Not pre-sold.
- **Gen 3 (2029, optional):** branded mobile app and merchandise commerce for 25+ location groups, funded from revenue.

Gen 2 and Gen 3 are options, not the justification for the company.

---

## 4. Market and Competitive Position

### 4.1 Market sizing

The market is sized bottom-up from Toast's disclosed location count, not from a top-down software forecast.

| Input | Value | Classification |
|---|---|---|
| Toast locations, Q3 2026 | ~189,000, +21% YoY | VERIFIED — Toast Q3 2026 results, 3 Nov 2026 |
| Share in groups of 10+ | 10–20% | MODELED — no public breakdown |
| Serviceable locations | 18,900–37,800 | MODELED |
| Gen 1 revenue per location | $61/month | MODELED — $59 core + $2 boards |
| **Gen 1 serviceable market** | **$13.8M–$27.7M ARR** | MODELED |
| 2029 locations in the plan | 1,182 | MODELED |
| **Share of serviceable market** | **3.1%–6.3%** | MODELED |

The 10–20% band is a management estimate. Toast does not disclose how many locations belong to groups of ten or more; its enterprise push implies a rising share, the long tail of independents a low one. Better data exists in Toast's 10-K segment disclosure, franchise disclosure documents and paid datasets (Technomic, Datassential); buying it is a $5–15K decision the company has not made. The Gen 1 market excludes ordering, apps and payments. A 3–6% share of a $14–28M market is a credible niche, not a venture-scale outcome on its own.

**Why now.** Search engines and AI answer engines reward current, structured menu pages, and a PDF is invisible to them. Signage hardware is cheap, so the bottleneck is software. Labor turnover keeps recreating the "person who knew how to update it" failure. Toast adds roughly 8,500 net locations a quarter without Garnsh spending a dollar.

### 4.2 Competition

Prices are published list prices captured on 11 November 2026. They are not like-for-like: some are per location, some per brand, some per restaurant, and some bundle ordering Garnsh does not sell. The basis column is part of the comparison.

| Player | Category and target | Menu capability | Price | Basis | Source |
|---|---|---|---|---|---|
| Toast native (Websites, Online Ordering, Delphi) | POS-bundled website, ordering, boards; Toast operators | Menu syncs from POS; website menu is view-only | Not disclosed; bundled | Per location, plan-dependent | toasttab.com; ressto.co (secondary) |
| Marqii | Menu management and listings distribution; multi-unit | Menu sync to Google, Yelp, Apple, Facebook; review tools | $90 / $145 / $180 / $250 per month | Per location, annual contract | marqii.com/pricing |
| Popmenu | Website, menu, marketing; independents and small groups | Dynamic menu, website, ordering add-on | $179 / $299 / $499 per month | Per location | get.popmenu.com/pricing |
| BentoBox | Restaurant websites and ordering; Clover-aligned in 2026 | Website menu and ordering | ~$119 / $279 / $479 website tiers; ordering ~$49/mo + $0.99/order | Per location, tiered; secondary | orderitto.com, getsauce.com |
| Owner.com | Website, ordering, apps, marketing; independents | Website menu tied to ordering | $249/mo + 5% of orders, or $499/mo flat | Per restaurant | owner.com/pricing |
| ChowNow | Commission-free ordering and websites | Menu tied to ordering | From $229/mo annual; setup $119–$499 | Per restaurant | get.chownow.com/pricing |
| Lunchbox | Enterprise ordering and apps | Menu inside ordering stack | Quote-based | Enterprise contract | lunchbox.io |
| Web agencies | Custom sites, manual menu updates | Whatever they build, maintained by hand | Project fee + retainer | Quote-based | — |

**What the table shows.** Garnsh is not cheaper than every competitor. Marqii starts at $90 per location and already owns distribution to the listings that drive discovery. Popmenu bundles a website and marketing for $179. BentoBox sells design. Owner.com and ChowNow sell ordering economics and can treat the menu as free.

**Where Garnsh fits.** None of them sells publishing control as the product: per-location mapping, preview before publish, version history, rollback and last-known-good serving, on a website the group already owns. Marqii is the closest adjacent competitor and should be treated as one; it could compete down into rendering or partner on distribution. Toast native is the default, not the enemy.

**Why a group would buy, and why it might not.** The alternative is an agency retainer, a marketing suite it does not need, or a coordinator editing four surfaces by hand; Garnsh costs $59 per location and removes a recurring public-error problem without changing POS, website or ordering vendor. But the problem may not be urgent enough for a separate product, Toast may ship enough, $59 may be too high for the value, or the integration may not be permitted. Those are the four tests in Section 6.

### 4.3 Differentiation, honestly stated

There is no technical moat in reading a menu API. Defensibility, if it develops, comes from switching cost once every location is mapped, from case studies in a narrow segment, from Toast partner status, and from a second POS adapter. None is strong on day one.

| Claim | Status |
|---|---|
| Preview, publish, version history, rollback, per-location mapping | Demonstrated in the demo; production hardening required |
| Last-known-good serving | Designed, not built |
| Keeps the group's existing website, POS and ordering vendor | True by architecture |
| Toast ingestion | Not built; access unverified |
| Multi-POS (Square, Clover) | Not built; month-18 plan |

---

## 5. Business Model and Pricing

### 5.1 Price

| Item | Price | Basis | Status |
|---|---|---|---|
| Core publishing (hosted page, embed, QR) | $59 per location per month | Per location | MODELED — untested |
| Menu boards add-on | +$40 per location per month | Per location with screens | MODELED — untested |
| Onboarding | $120 per location, $1,500 minimum | 2h per location at $60/h | MODELED — v3.1 revision |
| Multi-location management | Included at 10+ locations | — | — |
| Gen 2 ordering | +$99 per location per month | Per location | MODELED — conditional |
| Gen 3 branded app | $5,000 build + $149 per location per month | Per brand + per location | MODELED — conditional |
| Enterprise (25+ locations) | ~$119 per location per month all-in | Annual contract, SLA | MODELED — untested |

Every price is a founder assumption. None has been tested against an invoice.

### 5.2 What a customer actually pays

| Line | 14-location group |
|---|---|
| Core publishing | $826 per month; $9,912 per year |
| Core plus boards at every location | $1,386 per month; $16,632 per year |
| Onboarding, one-time | $1,680 |
| Toast plan upgrade, if required | +$T per location per month — **UNVERIFIED** |

If the group already runs a Toast plan that includes API access, the incremental cost is zero; if not, it may have to upgrade every location. At $50 per location a 14-location group pays $700 more per month — a 51% uplift on core plus boards and 85% on core alone. The first ten interviews must price this. The model excludes it; if it applies, the value story changes.

### 5.3 Setup economics

Onboarding is two hours per location at $60 per hour, or $120 per location. A flat $1,500 fee breaks even at 12.5 locations and loses money above that — at the 14-location average and badly at 40 locations.

| Group size | Onboarding cost | Flat $1,500 | Margin | Cost-recovery fee | Margin |
|---|---|---|---|---|---|
| 10 | $1,200 | $1,500 | +$300 | $1,500 | +$300 |
| 14 | $1,680 | $1,500 | −$180 | $1,680 | $0 |
| 25 | $3,000 | $1,500 | −$1,500 | $3,000 | $0 |
| 40 | $4,800 | $1,500 | −$3,300 | $4,800 | $0 |

**Options considered.** (1) Retain $1,500 and cap onboarding at two hours: simple, but the cap is not credible for a 25-location group and the loss grows with the customer. (2) Raise the flat fee to $2,500: covers groups to 20 locations but still loses $2,300 at 40, and an unscoped flat fee is hard to defend in procurement. (3) Waive the fee as acquisition cost: better conversion, but adds $1,680 to every group's upfront cash on a $20,000 budget. (4) **Cost-recovery at $120 per location with a $1,500 minimum: breaks even at every size and does not tax the smallest customers. Recommended and adopted.**

The change adds $1,980 of 2027 revenue, $6,660 in 2028 and $10,080 in 2029 against the flat fee, and removes a structural loss on larger groups. The fee now scales with the work.

### 5.4 Pricing rules

No discount on the per-location price. Discount implementation instead: waive setup, add months, add a pilot location. A discounted rate compounds for the life of the account. The design-partner program is a capped, dated exception, approved by both founders in writing and recorded as marketing spend.

**Validation triggers.** Ten interviews, not three, before the price is fixed:

| Trigger | Threshold | Action |
|---|---|---|
| Median acceptable price | below $45 per location | move to a $39/$69/$45 ladder and cut the cost base |
| Credential friction | 3+ of 10 cannot supply Toast credentials | make CSV/Sheets the primary path |
| Pilot commitment | fewer than 4 of 10 accept a paid pilot | the segment or the pain is wrong; re-interview |
| 86 status | top pain in more than 3 of 10 | revisit the Gen 1 promise |
| Toast plan cost | +$25 per location for half the sample | the real price is $84+; retest the value story |

---

## 6. Go-to-Market and Customer Validation

### 6.1 Validation status and funnel

Zero signed design partners, zero live locations, zero paying customers and zero interviews as of 11 November 2026. The funnel is a target, not a result, and every downstream number — revenue, founder hours, cash — depends on it. v3.0 used four sets of customer numbers that did not reconcile; v3.1 uses one classification and one funnel:

| Stage | Count | Conversion | Note |
|---|---|---|---|
| Qualified conversations | 60 | — | 40 in H1, 20 in H2 |
| 30-day paid pilots started | 24 | 40% of conversations | Three locations each, $59/location |
| Pilots converted to annual | 15 | 62.5% of pilots | Includes design partners |
| — Free design partners | 4 | — | 90 days free, then list |
| — Discounted showcase partners | 6 | — | 20% off core for six months, then list |
| — Full-price customers | 5 | — | List price |
| Gross groups acquired | 15 | 25% of conversations | Model input |
| Churned groups | 1.0 | 1.5%/month | Model output |
| **Net groups at 31 December** | **14.0** | — | Model output |
| **Live and paying locations** | **192** | — | 13.7 average per group |

The 15-group forecast requires 60 qualified conversations at 25%, not 40 at 25%. The v3.0 claim that 40 conversations produce 15 customers was arithmetically wrong and has been removed. At a 1-in-6 close rate the same 15 groups need 90 conversations and roughly 50% more selling time: a capacity risk, not a cash risk. Design partners and showcase partners are one program with two tiers, not separate pools, and no customer is counted twice.

### 6.2 Pilot and design-partner terms

| Element | 30-day paid pilot | 90-day design partner |
|---|---|---|
| Eligibility | 10+ locations on Toast, one brand owner, menu access and feedback | 10+ locations, brand team, willing to sign reference obligations |
| Scope | Three locations, one embed, one QR view, one board | All locations |
| Price | $59 per location per month; setup waived during pilot, charged on conversion | Free for 90 days; setup waived; list price thereafter |
| Deliverables and conversion | Menu audit, three surfaces, training, written results; annual contract at list price | Case study, two reference calls, feedback; automatic annual contract at list unless 30 days' notice |

Showcase partners: six groups at 20% off core for six months, then list price. Setup is charged.

### 6.3 What the v3.0 program would have cost

The original offer — four groups free for twelve months, six at 20% for twelve months, setup waived for all ten — is generous in a way the balance sheet cannot support.

| Cost | v3.0 offer (12 months) | v3.1 program (90 days / 6 months) |
|---|---|---|
| Free subscriptions foregone | $40,992 | $10,248 |
| Discount foregone | $11,894 | $5,947 |
| Setup fees waived | $16,800 | $6,720 |
| Onboarding labor at $60/h | $16,800 | $6,720 |
| Reference and case-study time | $4,800 | $960 |
| **Total economic cost** | **$91,286** | **$30,595** |

The revised program costs about a third as much and still produces four case studies, and it keeps the company inside its cash floor. The trade-off is real: 90 days may be too short to produce a publishable case study. If the first two partners cannot, extend those two by 30 days rather than reintroducing a twelve-month free tier. Reference rights are contractual requirements; the model does not assume every customer agrees, and a partner who refuses the case-study clause is a full-price customer instead.

### 6.4 Channels and founder capacity

1. **Founder network.** The founders operate in the Afro Deli franchise system: a source of introductions, not a customer commitment.
2. **Agencies.** They update menus constantly and dislike it. Offer a 25% recurring revenue share and a white-label option.
3. **Toast Partner Connect.** Only after approval; not in the 2027 plan.
4. **No paid acquisition.** A paid channel at $10–15K per group cannot be funded from $20,000 (Section 9.5).

Founder hours for 2027 total **1,464**, or 14.1 per week each on average:

| Activity | Hours | Basis |
|---|---|---|
| Build | 400 | 10 weeks × 40 hours total |
| Selling | 324 | 60 conversations × 3h + 24 pilots × 6h |
| Onboarding | 420 | 15 groups × 14 locations × 2h |
| Support | 60 | ~1 hour/day from October |
| Admin | 260 | 5 hours/week |
| **Total** | **1,464** | **14.1 hours/week each** |

| Quarter | Founder A | Founder B | Note |
|---|---|---|---|
| Q1 | 9.9 h/week | 10.6 h/week | Build and first interviews |
| Q2 | 11.9 h/week | 14.4 h/week | 196 onboarding hours; 84 in June alone |
| Q3 | 7.6 h/week | 10.1 h/week | Post-build, selling |
| Q4 | 11.5 h/week | 14.0 h/week | 140 onboarding hours plus support |

The average understates the peak. In June three groups go live in one month: 84 hours of onboarding, 19.4 hours per week on that activity alone. The plan is feasible at part-time hours only if onboarding is capped at two groups per month.

### 6.5 Retention

Retention comes from switching cost: once every location is mapped and opening procedures reference Garnsh, replacing it means re-mapping the estate. The plan assumes 1.5% monthly group churn and 0.5% monthly location churn — assumptions, not measurements, which the first ten groups exist to replace with data.

---

## 7. Technology and Toast Integration

### 7.1 What works without Toast

The CSV/Google Sheets import and the manual editor can go live without Toast approval. They are not a temporary hack: they let the first groups pay before certification lands and remove the largest dependency from the first revenue dollar. The product is "menu document in, surfaces out"; Toast is an adapter, not the architecture.

### 7.2 Three kinds of Toast access

| Route | What Toast documents | What it implies |
|---|---|---|
| **Standard API access** | Credentials are **read-only**, scoped to specific restaurants, **location-specific** (a separate request per location), with **no sandbox**. Menus `GET` is supported. | Enough to read a menu. Does not authorize commercial public-facing use on its own; that is a contract question, not a technical one. |
| **Partner integration** | Access is granted through the Toast Partner Integrations program, including a formal application and certification. Approved partners get scoped read/write access on behalf of customers who share data with Toast. | The only route that plausibly supports public publishing at scale and any Gen 2 ordering. Grants depend on the agreement and approval. |
| **Custom integration** | Menus `GET` is supported for custom integrations. | A per-customer build. Not a scalable product, but a possible pilot route with one design partner. |

Sources, accessed 11 November 2026: *Standard API access overview* (doc.toasttab.com/doc/devguide/devApiAccessUserGuide.html); *Partner integration overview* (…/apiPartnerIntegrationOverview.html); *API overview* (…/apiOverview.html); *Menus API overview* (…/apiGettingMenuInformationFromTheMenusAPI.html).

### 7.3 The unverified question

A customer holding standard credentials can read its own menu. That does **not** establish that the customer may authorize Garnsh to use those credentials to power a public-facing menu inside a commercial SaaS product. That is a question of Toast's terms, the customer's agreement and possibly law. It is **unverified**, and no sale may depend on it until Toast or qualified counsel confirms it in writing. The same applies to partner fees, revenue share, certification timing and marketplace listing; none is assumed in the model.

### 7.4 The day-120 gate

By day 120 (May 2027), Garnsh must have all four:

1. a named Toast partner contact and a written application status;
2. a written timeline with dates for certification;
3. a sandbox credential, or a written reason none has been issued;
4. a written position — from Toast or counsel — on whether customer-supplied credentials may power public-facing menus.

If all four exist and (4) is yes, proceed on the partner route. If (4) is no, publish through CSV/Sheets and the manual editor only and start the Square adapter. If none exist by day 120, stop the Toast route and re-plan around import-first. "In progress" is not a status and does not pass the gate. The founders record the decision in writing.

### 7.5 Fallback and technical risk

Import-first is a complete product for a group willing to export a menu or maintain it manually, and the base case's safety net. A second POS adapter (Square, then Clover) by month 18 reduces single-platform risk. Menu-data hygiene — modifiers, price tiers, location variants — is the hard engineering. Tenant isolation and accessibility are ship gates: a failed accessibility audit is both an enterprise blocker and a legal exposure.

---

## 8. Operations and Founding Team

### 8.1 Team

Two founding partners. Names, backgrounds and the role split are **not yet documented** and must be completed before this plan goes to any external party. The table is deliberately blank rather than invented.

| Item | Founder A | Founder B |
|---|---|---|
| Name | [FOUNDER INPUT REQUIRED] | [FOUNDER INPUT REQUIRED] |
| Professional background | [FOUNDER INPUT REQUIRED] | [FOUNDER INPUT REQUIRED] |
| Restaurant or restaurant-technology experience | [FOUNDER INPUT REQUIRED] | [FOUNDER INPUT REQUIRED] |
| Product and engineering | Build lead: architecture, ingestion, publishing layer | Review, testing, accessibility and QA |
| Toast integration and certification | Partner application and technical contact | Fallback import path |
| Sales and partnerships | Agency channel | Sales lead: pipeline, pilots, close |
| Onboarding and support | Back-up | Primary owner |
| Weekly time commitment | [FOUNDER INPUT REQUIRED] | [FOUNDER INPUT REQUIRED] |
| Decision rights | Product and architecture | Commercial, pricing exceptions, hiring |

Four functions need a named owner from day one: product and engineering, Toast integration and certification, sales and operator relationships, and onboarding and support. With two people each owns two; "we both do sales" means nobody does support during a Friday dinner rush. Before external circulation the founders must also supply employment history, restaurant operating experience, conflicts of interest and the equity split — not cosmetic gaps, because investors price them.

### 8.2 Support and hiring

Support becomes a founder's full day at roughly 150 live locations. The model budgets a part-time support contractor at **$2,500 per month** from that point, funded from revenue, which occurs in October 2027. Hiring gates are thresholds, not dates:

| Hire | Gate | Model timing |
|---|---|---|
| Support contractor | 150 live locations | October 2027 |
| Engineer | $35K MRR | July 2028 |
| Growth / account management | $50K MRR | October 2028 |
| Second engineer, founder salaries | 2029, from operating cash | January 2029 |
| Founder pay | $0 in 2027; $6,000/month total from July 2028; $100K in 2029 | July 2028 |

### 8.3 Legal and operating checklist

Before the $20,000 is spent: operating agreement with decision rights and a deadlock clause; four-year vesting with a one-year cliff; IP assignment from both partners, including the pre-entity demo; buy-sell and right of first refusal with a valuation formula; trademark search and filing for "Garnsh" (USPTO classes 9 and 42); separate bank account and books; tech E&O and cyber insurance; contractor agreements with IP assignment.

---

## 9. Financial Plan

### 9.1 Model basis

The model is a 36-month cohort model. It tracks groups, locations, revenue, collections, onboarding labor, churn and cash, and separates cash from revenue recognition. It is a planning model, not a forecast. **Scenario A contains no Gen 2 or Gen 3 revenue.** v3.0's 2028–29 projections included 17%/28% ordering attach and 3.5% app attach, so they were not Gen 1 numbers; they are removed and modelled separately in Section 9.8.

| Assumption | Base | Downside | Classification |
|---|---|---|---|
| Average group size | 14 locations | 10 locations | MODELED |
| Group logo churn | 1.5%/month | 2.5%/month | MODELED — no cohort data |
| Location churn | 0.5%/month | 1.0%/month | MODELED — no cohort data |
| Subscription collection | Same month (card on file) | 30-day lag | MODELED |
| Setup collection | 50% at go-live, 50% next month | Same | MODELED |
| Onboarding labor | 2h/location at $60/h | 4h/location | MODELED |
| 2027 onboarding funding | Founders unpaid | Paid contractor | MODELED |
| Support contractor | $2,500/month from 150 locations | Same | MODELED |
| Price | $59 core, $40 boards | $59 core | MODELED |
| Toast plan cost to customer | Excluded | Excluded | UNVERIFIED |

### 9.2 2027 by quarter

| Quarter | Revenue | Cash from operations | Economic result | Cash at quarter-end |
|---|---|---|---|---|
| Q1 | $0 | −$13,151 | −$13,151 | $6,849 |
| Q2 | $8,085 | +$3,033 | −$7,887 | $9,882 |
| Q3 | $19,487 | +$11,535 | +$6,495 | $21,417 |
| Q4 | $36,854 | +$24,226 | +$15,826 | **$45,643** |

The trough is **$6,750 in April**, $1,750 above the floor. Peak capital deployed is $13,250; capital is returned by June. Monthly detail is in Appendix A.

### 9.3 The 2027 onboarding constraint

The 2027 cohort adds 210 live locations. At two hours per location and $60 per hour that is **$25,200 of labor**.

- **Founders perform it:** cash cost $0, economic cost $25,200, economic result **−$17,197**; the April trough is **$6,750**.
- **A contractor performs all of it:** the trough is **−$1,878 in June** and year-end cash is $20,443. The company survives the year but breaches the $5,000 reserve by about $6,900 and runs negative for part of Q2–Q3.
- **A contractor performs only the first cohort** (28 locations, $3,360): the April trough is **$3,390**, below the floor.

This is the binding constraint. The $20,000 works only if the founders perform 2027 onboarding, or if the company raises roughly **$7,000** to cover a contracted onboarding ramp. A $25,000–$30,000 requirement belongs to the combined stress case in Section 9.7, not to onboarding alone. That is a founder decision, not a modeling choice.

### 9.4 Three-year summary — Scenario A, Gen 1 only

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Revenue | $45,946 | $361,320 | $918,657 |
| Cost of revenue, excluding onboarding | $10,491 | $49,011 | $120,590 |
| Onboarding labor (cash) | $0 | $62,160 | $94,080 |
| Gross profit | $35,454 | $250,149 | $703,987 |
| Gross margin | 77.2% | 69.2% | 76.6% |
| Recurring gross margin before onboarding | 77.2% | 86.4% | 86.9% |
| Operating expenses | $27,451 | $168,100 | $471,000 |
| Economic result after founder labor | −$17,197 | +$82,049 | +$232,987 |
| Cash from operations | +$25,643 | +$142,529 | +$326,227 |
| Year-end cash | $45,643 | $188,172 | $514,399 |
| Minimum cash during year | $6,750 | $50,990 | $193,782 |
| Exit MRR | $10,857 | $48,087 | $98,110 |
| Exit ARR | $130,278 | $577,049 | $1,177,318 |
| Gross group additions | 15 | 37 | 56 |
| Churned groups | 1.0 | 5.3 | 12.2 |
| Net groups | 14.0 | 45.7 | 89.5 |
| Live and paying locations | 192 | 615 | 1,182 |

The 2028 gross margin falls because onboarding labor becomes cash and sits in cost of revenue; recurring gross margin rises to 86%. The 2029 cost base is sized to Gen 1: $471K of operating expense, one engineer, one growth hire and a support team. The model adds 37 gross groups in 2028 and 56 in 2029 to finish with 46 and 90 net; a gross-add-only plan would overstate profit.

### 9.5 Unit economics per group

Definitions are stated because v3.0 mixed them. **CAC** is sales and marketing cost to acquire one group; **onboarding cost** is the direct cost of implementing it; **upfront investment** is CAC plus unrecovered onboarding; **payback** is months to recover the upfront investment from recurring gross profit; **LTV:CAC** divides LTV by CAC, not by upfront investment.

| Line | Amount |
|---|---|
| Monthly revenue (14 locations × $98 blended ARPU) | $1,372 |
| Recurring gross profit (89%) | $1,221 |
| CAC (18 selling hours × $55 + $600) | $1,590 |
| Onboarding labor (14 × 2h × $60) | $1,680 |
| Less setup fee (cost-recovery) | −$1,680 |
| Net onboarding cost | $0 |
| **Upfront investment** | **$1,590** |
| Payback | 1.3 months |
| Average life at 2.0% monthly revenue churn | 50 months |
| LTV | $61,054 |
| **LTV : CAC** | **38.4x** |
| LTV : CAC at 3.5% monthly churn | 21.9x |

**Read this with suspicion.** A 38x LTV:CAC is not a benchmark; it is the output of assuming 2% monthly churn, 89% gross margin and no support cost growth, with no cohort to test any of it. The honest use is directional: at these prices the economics work if churn behaves, and the constraint on growth is cash and founder time, not unit profitability.

**Reconciling the v3.0 contradiction.** v3.0 claimed on page 6 that CAC exceeds LTV and on page 13 that LTV:CAC was 38.4x. Both cannot be true. The intended point was about paid acquisition: a paid channel at $10–15K per group cannot be funded from $20,000. At a hypothetical $15,900 CAC, LTV:CAC would still be 3.8x — mathematically acceptable, operationally impossible. The claim has been rewritten to say that, and the "CAC exceeds LTV" sentence removed.

### 9.6 Cash, working capital and the reserve

The base case assumes card-on-file collection in the same month and setup fees 50% at go-live, 50% the following month; receivables are $840 at the end of 2027 and $2,520 at the end of 2028. A 30-day subscription lag lowers the 2027 trough to **$5,570** — still above the floor, with $570 of headroom — and cuts 2029 year-end cash by about $40K. The plan should not assume same-month collection for enterprise accounts without confirming terms. The $5,000 reserve is a hard floor, not a buffer: below it, before recurring revenue passes $3,000 per month, the company stops discretionary spending, stops building and sells what exists.

### 9.7 Combined downside

v3.0 tested variables one at a time. v3.1 adds a combined stress case with simultaneous, correlated problems: 10-location groups, a 1-in-6 close rate (10 groups), launch delayed to June, 2.5% group and 1.0% location churn, 30-day collection, four hours of onboarding per location, and paid contractor onboarding.

| Case | 2027 revenue | 2027 economic result | 2027 minimum cash | 2029 year-end cash |
|---|---|---|---|---|
| Base | $45,946 | −$17,197 | $6,750 | $514,399 |
| Downside (moderate) | $31,167 | −$16,328 | $6,325 | −$9,354 |
| Downside + cost response | $31,167 | −$10,838 | $9,205 | $587,337 |
| Combined stress | $16,741 | −$35,894 | −$16,194 | −$292,456 |
| Combined stress + response | $16,741 | −$30,403 | $7,085 | $360,134 |

**The combined stress is not survivable on $20,000.** Cash goes negative in May 2027 and the company is insolvent before year-end. No cost cut fixes a business whose first customer arrives in June while a contractor is paid $4,000 per group to onboard.

**The response.** Founders perform all onboarding, including 2028, at four hours per location (cash saving $24,000 in 2027 and $52,800 in 2028); every hire is frozen, with no engineer, no growth hire and no founder draws through 2028; travel and marketing fall to $400/month each, contract design to zero, certification is deferred until the gate passes; the 2028 plan is capped at 22 gross groups; the support contractor is kept only from 150 locations. With those actions the trough is **$7,085** and 2029 ends with $360K — a smaller, slower, still-viable business, not the plan, at a cost of roughly two years of growth. The moderate downside breaches the reserve only in 2029 at the full cost base, and the same freeze restores it to $587K. If the founders will not run the freeze, the plan needs a bridge of **$25,000–$30,000** before launch.

### 9.8 Scenario B — conditional expansion

Expansion is modelled separately and never merged into Scenario A. Gen 2 launches July 2028 after a six-month build and certification; Gen 3 launches July 2029. Both depend on Toast partner approval and a commercial agreement.

| Incremental line | 2027 | 2028 | 2029 |
|---|---|---|---|
| Gen 2 ordering revenue ($99/location) | $0 | $25,528 | $225,097 |
| Gen 3 app subscriptions ($149/location) | $0 | $0 | $19,956 |
| Gen 3 build fees ($5,000/brand) | $0 | $0 | $13,429 |
| **Incremental revenue** | **$0** | **$25,528** | **$258,483** |
| Development and certification | $0 | $75,000 | $70,000 |
| Incremental support | $0 | $15,000 | $45,000 |
| Payment fees | $0 | $740 | $7,107 |
| **Incremental contribution** | **$0** | **−$65,212** | **+$136,376** |

Assumptions: ordering attach rises from 4% at launch to 22% of locations by December 2029; app attach from 1% to 3.5%; $10K per month of build for six months each; certification, security review and legal of $15K (Gen 2) and $10K (Gen 3). Adoption is modeled, not evidenced. Cumulative contribution by the end of 2029 is **+$71,164** — after $65K of investment in 2028 that the base case can fund and a smaller company could not.

No expansion revenue may be recognised before the product is built, certified and commercially permitted. If Toast denies partner access, Scenario B is worth zero and Scenario A is unaffected. That is the point of separating them.

---

## 10. Risks, Milestones and Funding

### 10.1 Principal risks

| Risk | Impact | Mitigation | Residual |
|---|---|---|---|
| Toast denies or delays access | No scalable feed; Gen 2 impossible | Apply in week one; day-120 gate; import-first; second POS by month 18 | High |
| Public-facing use of customer credentials not permitted | Legal exposure; redesign | Written position from Toast or counsel before the first paid public page | High |
| No demand at $59 | Revenue does not cover the cost base | Ten interviews before pricing; 60 conversations; paid pilots | Medium |
| Founder capacity | Build, sales and onboarding collide | 1,464-hour budget; two groups per month onboarding cap | Medium |
| Onboarding paid by contractor | Reserve breached in Q2 2027 | Founders perform it; otherwise raise ~$7K or halve the launch | High |
| Churn above 1.5%/month | LTV and growth fall | Annual contracts, quarterly reviews, measure from cohort one | Medium |
| Collection lag | Trough breaches floor | Card on file; setup at signing; deposits for enterprise terms | Low |
| Toast ships a native equivalent | Differentiation erodes | Publishing craft, multi-surface, agency channel; no moat claimed | Medium |
| Accessibility or legal exposure | Enterprise blocker; ADA claim | WCAG 2.1 AA ship gate; E&O insurance; contract terms | Low |

### 10.2 2027 milestones

| When | Milestone |
|---|---|
| Week 1 | Entity formed; $20,000 paid in; operating agreement, vesting and IP assignment signed; Toast partner application submitted |
| Jan–Mar | Build Gen 1; ship CSV/Sheets bridge; 40-group target list; pricing interviews; legal checkpoint on credentials |
| 15 Mar | First design partner signed. If not, freeze travel and demos, defer certification, cut launch scope |
| Mar–Jun | Ten groups live; pilots running; first case study drafted |
| Day 120 (~May) | Toast gate: all four tests documented |
| Day 180 | Sales gate: at least 4 design partners signed and 3 paying, or the ICP, price or motion is wrong |
| H2 2027 | Remaining five groups; six showcase partners; agency referrals |
| Dec 2027 | 14 net groups, 192 live locations, $45,946 revenue, $6,750 trough, $45,643 cash |

### 10.3 Gates and kill criteria

- **Day 120 Toast gate:** all four tests, documented. Fail means import-first and a re-plan, not "in progress".
- **Day 180 sales gate:** fewer than 4 design partners signed, or fewer than 3 paying, means the ICP, price or motion is wrong. Do not add features; re-interview.
- **Cash floor:** below $5,000 before $3,000/month recurring revenue means stop and sell.
- **Gross margin:** below 75% recurring at 100 live locations for two consecutive months means the unit economics are broken. At 100 locations and 2h/location the model shows 77.9%; at 4h, 61.5%.
- **Churn:** above 3% monthly group churn after 25 groups means the product is not embedded; stop marketing and fix onboarding.

### 10.4 Funding strategy

The company is not raising now. The milestones that justify a round are ten paying groups and roughly 140 paying locations; at least six months of measured churn; a clear Toast status; a CAC and payback measured from real cohorts; and one 20+ location group on an annual contract. A round at that point funds engineering, certification and the first sales hire. It does not fund survival.

If the founders cannot perform 2027 onboarding, the bridge requirement is about **$7,000**. If the combined stress case materialises before the first raise, it is **$25,000–$30,000**. Either way the right instrument is a small convertible note or founder loan, not a priced round.

---

## 11. Conclusion

Garnsh is a narrow, credible Gen 1 business: menu publishing and control for multi-location Toast groups. The problem is real, the product boundary is honest, and the unit economics work if the price holds and churn behaves. The risks are Toast access, demand and founder capacity — not the arithmetic.

The plan is deliberately small. It does not assume ordering, payments or a branded app. It does not assume customers it does not have. It assumes two founders can build a useful product, sell fifteen groups, and learn whether the market will pay $59 per location before spending money the company does not have.

That is the right test. If it passes, Garnsh has a business worth scaling. If it fails, it fails cheaply, with the evidence written down.

---

## Appendix A — 2027 monthly schedule (Scenario A)

| Month | Live loc | Paying loc | Revenue | Cash from ops | Economic result | Cash |
|---|---|---|---|---|---|---|
| Jan | 0 | 0 | $0 | −$4,617 | −$4,617 | $15,383 |
| Feb | 0 | 0 | $0 | −$5,617 | −$5,617 | $9,766 |
| Mar | 0 | 0 | $0 | −$2,917 | −$2,917 | $6,849 |
| Apr | 28 | 14 | $2,024 | −$99 | −$2,619 | $6,750 |
| May | 55 | 28 | $2,699 | $1,349 | −$2,011 | $8,099 |
| Jun | 96 | 41 | $3,361 | $1,783 | −$3,257 | $9,882 |
| Jul | 108 | 68 | $4,814 | $3,299 | $1,619 | $13,181 |
| Aug | 120 | 93 | $6,237 | $5,160 | $3,480 | $18,341 |
| Sep | 132 | 132 | $8,436 | $3,076 | $1,396 | $21,417 |
| Oct | 157 | 157 | $11,319 | $6,753 | $4,233 | $28,170 |
| Nov | 182 | 182 | $12,998 | $7,980 | $4,620 | $36,150 |
| Dec | 192 | 192 | $12,537 | $9,493 | $6,973 | $45,643 |

Paying locations reach live locations in September because every free design partner has passed its 90-day period. Revenue includes $18,480 of setup fees, collected 50% at go-live and 50% the following month, which is why December revenue is below November despite more paying locations.

## Appendix B — Sensitivities

| Case | 2027 revenue | 2027 economic result | Lowest cash | Month |
|---|---|---|---|---|
| Base | $45,946 | −$17,197 | $6,750 | Apr |
| Group size 10 | $32,818 | −$14,769 | $6,571 | Apr |
| Close 1 in 6 (10 groups) | $24,457 | −$21,510 | $4,100 | Jun |
| Launch delayed to June | $25,451 | −$26,450 | $4,100 | Jun |
| Churn 2.5% / 1.0% | $43,634 | −$16,879 | $6,750 | Apr |
| 30-day collection lag | $45,946 | −$17,197 | $6,405 | Apr |
| Paid 2027 onboarding | $45,946 | −$17,197 | −$1,878 | Jun |
| Onboarding 4h/location | $45,946 | −$42,397 | $6,750 | Apr |
| Core price $45 | $35,437 | −$27,400 | $6,673 | Apr |
| Setup flat $1,500 | $45,946 | −$17,197 | $6,660 | Apr |
| Setup $2,500 | $45,946 | −$17,197 | $6,849 | Mar |

## Appendix C — Evidence register (summary)

The full register is a separate deliverable. Claims are classified VERIFIED, MODELED, UNVERIFIED, TARGET or ACTUAL.

**VERIFIED.** Toast had ~189,000 locations at 30 September 2026, +21% year over year, ARR $2.5B and ~8,500 net adds in Q3 2026 (Toast Q3 2026 results, 3 November 2026). Standard API access is read-only, location-specific, and excludes write access and sandbox. Partner access requires a formal application and certification, with scoped read/write access. Menus `GET` is supported for partner, custom and standard integrations (Toast developer guide, accessed 11 November 2026). Published competitor prices in Section 4.2, as at 11 November 2026.

**MODELED.** 10–20% of Toast locations in groups of 10+; serviceable market $13.8M–$27.7M; all pricing, attach rates, churn, CAC, onboarding hours, conversion and financial results; founder hours and the 2027 funnel.

**UNVERIFIED.** Whether customer-supplied Toast credentials may power public-facing menus in a commercial product; partner fees, revenue share and certification timeline; the customer's incremental Toast plan cost; demand at $59; churn; CAC; pilot conversion; competitor prices where only secondary sources exist (BentoBox, Popmenu add-ons, Lunchbox).

**TARGET.** 15 gross groups, 14 net groups, 192 live locations and 60 conversations in 2027; Gen 2 launch July 2028; Gen 3 launch July 2029.

**ACTUAL.** Two founders, $20,000 committed capital, a working demo. Nothing else.

## Appendix D — Sources

1. Toast, Inc., *Toast Announces Third Quarter 2026 Financial Results*, 3 November 2026 — investors.toasttab.com; businesswire.com.
2. Toast developer guide, *Standard API access overview* — https://doc.toasttab.com/doc/devguide/devApiAccessUserGuide.html (accessed 11 November 2026).
3. Toast developer guide, *Partner integration overview* — https://doc.toasttab.com/doc/devguide/apiPartnerIntegrationOverview.html (accessed 11 November 2026).
4. Toast developer guide, *API overview* — https://doc.toasttab.com/doc/devguide/apiOverview.html (accessed 11 November 2026).
5. Toast developer guide, *Menus API overview* — https://doc.toasttab.com/doc/devguide/apiGettingMenuInformationFromTheMenusAPI.html (accessed 11 November 2026).
6. Marqii, *Pricing* — https://marqii.com/pricing (accessed 11 November 2026).
7. Popmenu, *Pricing* — https://get.popmenu.com/pricing (accessed 11 November 2026).
8. Owner.com, *Pricing* — https://www.owner.com/pricing (accessed 11 November 2026).
9. ChowNow, *Plans and pricing* — https://get.chownow.com/pricing (accessed 11 November 2026).
10. BentoBox pricing summaries — orderitto.com; getsauce.com (secondary, 2026).
11. Founders' working notes and the Garnsh demo, November 2026.

Where a claim is not sourced above, it is an assumption and is labelled MODELED or UNVERIFIED in the register.

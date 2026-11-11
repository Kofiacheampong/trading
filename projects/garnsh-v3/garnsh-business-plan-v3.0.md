# Garnsh

## Menu publishing for multi-location restaurant groups

**Business Plan v3.0** · 11 November 2026

Confidential. Prepared for the founders, advisors and prospective investors.

> **Status:** pre-revenue. Garnsh has a working demo, no signed customers and no live locations. Any customer, pilot or partnership mentioned in this plan is a target or a proposed program unless it is explicitly labeled as signed. Financial figures are planning estimates, not actuals.

---

## 1. Executive Summary

Garnsh is a software-as-a-service (SaaS) menu publishing platform for restaurant groups that operate 10 or more locations on Toast. It gives a group one controlled place to prepare a menu, map it to each location, preview every guest-facing surface, publish it, and roll back if something is wrong.

The problem is operational, not cosmetic. A multi-location group maintains one menu in Toast but presents it on at least four surfaces: its website, a hosted menu page, QR menus and in-store digital boards. Each surface is usually updated by hand. Prices drift, discontinued items linger, one location's prices appear at another, and a bad publish can leave a blank board during service. The group usually has no single owner for the problem.

Garnsh Gen 1 solves menu accuracy and publishing control. It is deliberately not an ordering system, a payments product, a live inventory system or a real-time sync engine. It does not show 86 status. It does not claim that a Toast change reaches guests until someone previews and publishes it. Those boundaries are central to the product and to the credibility of the plan.

The initial customer is a regional fast-casual or casual-dining group with 10–50 locations, all on Toast, and a brand team or operations leader who owns menu presentation. The buyer is usually the VP of Marketing, the Director of Operations, or the founder-operator in a smaller group. The product is sold on control, not on being the cheapest menu page.

The business model is a per-location subscription: $59 per location per month for core publishing, $40 per location per month for menu boards, and a $1,500 setup fee per brand. Optional Gen 2 ordering ($99 per location per month) and Gen 3 branded app ($149 per location per month) are expansion products, not part of the Gen 1 base case.

**Stage and 2027 objective.** Garnsh is pre-revenue. In 2027 the plan is to sign 10 design partners, of which six pay a discounted subscription and four are free for 12 months in exchange for feedback and case-study rights. The target is 14 net groups, 193 live locations and 142 paying locations by December 2027. The 10 design partners are a target, not traction.

**Financial headline (base case, modeled).**

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Revenue | $42,195 | $440,883 | $1,287,970 |
| Cash from operations | +$3,892 | +$163,901 | +$437,277 |
| Economic result after founder labor | −$20,558 | +$165,401 | +$435,027 |
| Year-end cash | $23,892 | $187,794 | $625,070 |
| Net groups | 14.1 | 45.8 | 89.6 |
| Exit ARR | $88K | $698K | $1.63M |

The 2027 cash result is positive only because the founders perform onboarding unpaid. Imputing that time at $60 per hour turns the year into a **−$20.6K economic result**. If a contractor performs the 2027 onboarding, the company runs out of cash. That is the most important financial fact in this plan, and it drives the operating rules in §9.

**Capital and fundraising.** The company is capitalized with $20,000 from the two founders. It is not raising now. The plan is to reach 10 paying groups, approximately 140 paying locations, a measured churn rate and a clear Toast status before opening a round. A raise at that point would fund engineering, Toast certification and the first sales hire, not basic survival.

**The main risks** are Toast access, demand for a menu-only product, founder capacity and the possibility that the $59 price is too high for the value delivered. Each is treated in §10. The plan is designed to survive being wrong about some of them, not to assume it is right about all of them.

---

## 2. Problem and Market Opportunity

### 2.1 The operational problem

A restaurant group runs one operational menu in Toast. Guests see a different set of surfaces:

- the group's website, often a PDF or a page maintained by an agency;
- a hosted menu page;
- QR codes at the table;
- digital menu boards in each location;
- printed menus and inserts.

Each surface is maintained separately, usually by someone whose real job is running restaurants. The failure modes are predictable:

- **Price drift.** Toast says $16.25; the website says $14.50. A guest who sees one price and is charged another is a comp, a bad review and, in some jurisdictions, a consumer-protection risk.
- **Dead items.** A discontinued item stays on the QR page and the board for weeks because removing it means editing every surface.
- **Wrong-location menus.** One location's prices or items appear at another.
- **Stale PDFs.** The website menu is two cycles old because updating it means calling the web person.
- **No safety net.** A broken integration or a bad publish leaves a blank board during service.

For a 10-location group, this is a steady stream of small public errors multiplied by every surface, with no single person able to fix them at the source.

### 2.2 Why existing answers do not fit

**Toast's native tools.** Toast Websites is a template site builder aimed at operators who need a website, not groups with brand teams, agencies and existing web properties. Its menu channel is "Websites View-Only": the menu appears on a Toast Website, view only, and is not orderable. Toast Online Ordering runs on Toast's pages, in Toast's frame, with limited customization. Neither gives a group a branded, per-location menu on its own domain.

**Agencies and freelancers.** They build the site and then maintain the menu by hand. They are the real incumbent. They are slow, expensive and the reason menus go stale. They are also a potential reseller channel.

**Ordering and marketing suites.** Lunchbox, ChowNow, Owner.com, Popmenu and BentoBox sell ordering, websites or marketing. Menu display is plumbing inside a larger product. Their pricing is built around ordering economics, not menu control.

**The API wall.** Toast's Menus API is real but partner-gated. The documentation is public; production credentials are issued only to accepted partners after vetting, a signed agreement and certification. Toast's standard API access is read-only, per-location, limited to the older Menus V2, and positioned for reporting and internal use. It cannot write orders. Whether a customer's own credentials can lawfully power a public-facing website is **unverified** and is a pre-sale legal checkpoint (§6).

### 2.3 The initial customer

**Ideal customer profile:** a regional fast-casual or casual-dining group with 10–50 locations, all on Toast, with a brand worth protecting and a marketing or operations owner for menu presentation. Multi-unit franchisees and growing concepts in the 10–50 location band fit the same profile.

Below 10 locations, the pain is real but the budget and brand risk are small. Above 50 locations, the sales cycle and security requirements exceed a two-person company's capacity. The plan deliberately starts in the middle.

**Buyer:** VP of Marketing, Director of Operations, or the founder-operator. The pitch is operational: your menus are wrong in public, and fixing them consumes hours every week. Garnsh gives you one controlled publishing process and a rollback when someone gets it wrong.

### 2.4 Market sizing

The market is sized bottom-up from Toast's disclosed location count, not from a top-down restaurant-software forecast.

| Input | Value | Status |
|---|---|---|
| Toast locations, Q3 2026 | ~189,000, up 21% year over year | VERIFIED — Toast Q3 2026 results |
| Share in groups of 10+ | 10–20% | MODELED — no public breakdown |
| Serviceable locations | 18,900–37,800 | MODELED |
| Gen 1 revenue per location | $61/month | MODELED — $59 core + $2 boards |
| **Gen 1 SAM** | **$13.8M–$27.7M ARR** | MODELED |
| 2029 base-case locations | 1,183 | MODELED |
| **Share of SAM** | **3.1%–6.3%** | MODELED |

The Gen 1 SAM excludes ordering, apps and payments. Including those products would raise the ceiling, but they are not in the base case and should not be used to justify the first round. A 3–6% share of the Gen 1 SAM is a credible niche, not a venture-scale outcome on its own.

**Why now.** Menu data is becoming a discovery asset: search engines and AI answer engines reward current, structured menu pages, and a PDF is invisible to them. Digital signage hardware is cheap, so the bottleneck is software. Restaurant labor turnover keeps recreating the "person who knew how to update it" failure. And Toast's base compounds by roughly 8,500 net new locations a quarter without Garnsh spending a dollar.

---

## 3. Product and Solution

### 3.1 What Gen 1 does

Garnsh Gen 1 is a publishing system for menus. It has five capability groups:

1. **Custom menus.** The Toast menu, or an imported menu file, rendered on the group's own website (embed) or on a Garnsh-hosted page per location, styled to the brand.
2. **Order-ready menu boards.** Designed displays for in-store screens, fed from the same source menu.
3. **Location picker.** Each surface is mapped to the correct location's menu and prices, with per-location overrides.
4. **QR menus.** A per-location phone view opened by a printed code.
5. **Publishing controls.** Preview every surface before publishing, deliberate publish rather than silent auto-sync, full version history, one-click rollback, and last-known-good serving if an upstream source breaks.

### 3.2 How it works

The workflow is deliberately simple:

1. **Ingest.** A menu arrives from Toast (when approved access exists), a CSV/Google Sheets import, or the manual editor. The import bridge is a shipped part of the product, not a temporary hack.
2. **Normalize.** Items, modifiers, prices and location variants are cleaned into one menu document.
3. **Map.** The operator assigns the menu to locations, surfaces and overrides.
4. **Preview.** The operator sees every surface before publishing.
5. **Publish.** One action publishes the selected locations and surfaces, with a version record.
6. **Serve.** The hosted page, website embed, QR view and board display read from the published version. If anything breaks, the last-known-good version is served.

The architecture is intentionally boring: an ingestion service, a publishing/versioning layer, and four renderers. The hard engineering is menu-data hygiene and publishing safety, not rendering.

### 3.3 What Gen 1 does not do

- It does not read or display 86 status, live stock or table availability.
- It is not real-time. A change reaches guests only when someone previews and publishes it.
- It does not take orders, process payments, run a loyalty program or provide a branded mobile app.
- It does not replace Toast as the system of record.

These are product boundaries, not temporary gaps. The site, deck, contract and sales script must state them consistently.

### 3.4 Current stage and product debt

The current build is a demo with real interaction design, not a production service. To be sellable it needs:

- a production ingestion path and the CSV/Sheets import bridge;
- tenant authentication and isolation;
- per-location asset management;
- an upload pipeline for logos and fonts;
- board scheduling;
- an accessibility pass to WCAG 2.1 AA;
- bulk publish across locations and an unpublished-change alert. Without these two, a 14-location group repeats the same click fourteen times and "deliberate publish" becomes a tidy name for silent drift.

The estimate is 8–12 weeks of focused work. It is a quarter, not a weekend, and the 2027 plan is sized to it. These two requirements are **ASSUMPTION** until the build confirms them.

### 3.5 Roadmap and gates

- **Gen 1 (2027):** menu publishing. The only product in the base case.
- **Gen 2 (2028, gated):** branded online ordering on the group's own site, with orders written into Toast through the certified Orders API. It requires Toast ordering-partner certification and a signed commercial agreement. It is not pre-sold.
- **Gen 3 (2029, optional):** branded mobile app and merchandise e-commerce for 25+ location groups. Funded from revenue, not from the initial capital.

Gen 2 and Gen 3 are options. The company is viable as a Gen 1 business; that is the test the plan is built to pass.

---

## 4. Target Customers and Go-to-Market

### 4.1 Customer and buyer

The initial segment is 10–50 location groups on Toast with a brand team, an existing website and a recurring menu-update problem. The economic buyer is the VP of Marketing or Director of Operations. The day-to-day user is a marketing coordinator, an operations manager or an agency.

The trigger events are concrete: a price change that appears in one place and not another, a rebrand, a new location opening, a menu cycle change, or an agency handover. These are the moments when the cost of manual updating becomes visible.

### 4.2 Validation status

Garnsh has **zero signed design partners, zero live locations and zero paying customers** as of 11 November 2026. The 10 design partners in this plan are a target. The company has not yet run the 40 qualified conversations that would validate the segment, the price or the pilot terms.

That is not a weakness to hide. It changes what the plan can claim. It cannot claim product-market fit, a conversion rate or a churn rate. It can claim a defined customer, a defined problem, a demo and a testable sales motion.

### 4.3 One coherent pilot strategy

A 30-day pilot and a 12-month design-partner program are different instruments and should be described that way.

**Standard sales motion: 30-day paid pilot.**

| Element | Terms |
|---|---|
| Eligibility | 10+ locations on Toast, one brand owner, willingness to provide menu access and feedback |
| Duration | 30 days |
| Scope | 3 locations, one website embed, one QR view, one board |
| Price | Setup waived; $59 per location per month during the pilot |
| Deliverables | Menu audit, three published surfaces, operator training, written results |
| Success measures | Menu accuracy on audit, admin time per week, publish time, operator sign-off |
| Conversion | Annual contract at list price within 30 days; setup waived on conversion |

**Showcase program: 12-month design partners.**

| Element | Terms |
|---|---|
| Eligibility | 10+ locations, brand team, willingness to be a public reference |
| Duration | 12 months from go-live |
| Scope | All locations in the group |
| Price | Six groups at 20% off core; four groups free for 12 months; setup waived for all ten |
| Deliverables | Logo rights, written case study, one reference call per quarter, product feedback |
| Success measures | Case study published, reference completed, renewal at list |
| Conversion | List price at month 13; no renewal at the discounted rate |

A prospect can start with the 30-day pilot and convert to either an annual contract or a design-partner slot. The pilot is the sales motion; the design-partner program is a capped marketing program.

### 4.4 Sales and channels

The first 10 groups will be sold founder-led. The target is 40 qualified conversations in the first half of 2027, a 1-in-4 close rate and a 21–30 day cycle. At a 1-in-6 close rate, the same 10 signatures require 60 conversations and roughly 50% more selling time; that is a capacity risk, not a cash risk (§8).

Channels, in order:

1. **Founder network and warm introductions.** The founding team operates in the Afro Deli franchise system; that is a source of introductions, not a customer commitment.
2. **Agencies.** Web-design agencies serving restaurants are asked to update menus constantly, dislike the work and can white-label Garnsh. Offer a 25% recurring revenue share.
3. **Toast Partner Connect (later).** A marketplace listing becomes available only after partner approval. It is not part of the 2027 plan.
4. **No paid search, no cold outbound at scale.** At these price points, CAC exceeds LTV.

### 4.5 Onboarding and retention

Onboarding is the product's first real test. The standard is two hours per location: brand template, location mapping, surface setup, training. The setup fee covers that scope and no more (§5).

Retention comes from switching cost: once every location is mapped and opening procedures reference Garnsh, replacing it means re-mapping the estate. The plan assumes 1.5% monthly group churn and 0.5% monthly location churn. Those are assumptions, not measurements. The first 10 groups exist to replace them with data.

---

## 5. Business Model and Pricing

### 5.1 Price

| Item | Proposed price | Notes |
|---|---|---|
| Core publishing (hosted page, embed, QR) | $59 / location / month | Entry product |
| Menu boards add-on | +$40 / location / month | Per location with screens |
| Onboarding / setup | $1,500 / brand | Two hours per location; waived for showcase groups |
| Multi-location management | Included at 10+ locations | Location picker, overrides, group dashboard |
| Gen 2 ordering (2028) | +$99 / location / month | Gated on Toast certification |
| Gen 3 branded app (2029) | $5,000 build + $149 / location / month | 25+ location groups |
| Enterprise (25+ locations) | ~$119 / location / month all-in | Annual contract, SLA |

Every price is a founder assumption. None has been tested against a real invoice. The Q1 2027 interviews are the test.

### 5.2 What the customer actually pays

| Line | 14-location group |
|---|---|
| Core publishing | $826 / month; $9,912 / year |
| Core + boards at every location | $1,386 / month; $16,632 / year |
| Setup | $1,500 one-time |
| Toast plan, if not already carried | +$T / location / month — **UNVERIFIED** |

If the group already runs Toast's Restaurant Management Suite Essentials, the plan that includes API access, the incremental Toast cost is zero. If not, it may have to upgrade every location. At $50 per location, a 14-location group pays an extra $700 per month, a 51% uplift on the core-plus-boards invoice and 85% on core alone. The first ten interviews must price this; the plan does not assume it away.

### 5.3 Setup-fee economics

Onboarding is two hours per location at $60 per hour, or $120 per location.

| Group size | Onboarding cost | Setup fee | Margin | Break-even hours per location |
|---|---|---|---|---|
| 10 locations | $1,200 | $1,500 | +$300 | 2.50 |
| 12 locations | $1,440 | $1,500 | +$60 | 2.08 |
| 14 locations | $1,680 | $1,500 | −$180 | 1.79 |
| 16 locations | $1,920 | $1,500 | −$420 | 1.56 |

The setup fee is not a profit center. For the planned 14-location average it loses $180 per group at the two-hour cap; at three hours it loses $1,020. The options are to cap onboarding at two hours, raise setup to $2,500, or accept the loss as a customer-acquisition cost. The plan holds $1,500 and the two-hour cap; raising to $2,500 adds $37K of 2028 revenue and $56K of 2029 revenue without changing any other assumption.

### 5.4 Pricing rules and validation

**Rule one:** no standard discount on the per-location price. Discount implementation instead: waive setup, add months, add a pilot location. A discounted rate compounds for the life of the account.

**Rule two:** the showcase program is a capped exception. Ten groups maximum, 20% off core for 12 months, automatic expiry to list, no renewal at the discounted rate. It is approved by both founders in writing and recorded as marketing spend.

**Validation triggers.** Ten interviews, not three, before the price is fixed:

| Trigger | Threshold | Action |
|---|---|---|
| Median acceptable price | below $45 (24% below list) | adopt the $39/$69/$45 ladder and cut the cost base |
| Credential friction | 3+ of 10 cannot supply Toast credentials | make the CSV/Sheets bridge the primary path |
| Pilot commitment | fewer than 4 of 10 agree to a 30-day pilot | the segment or the pain is wrong; re-interview |
| 86 status | top pain in more than 3 of 10 | revisit the Gen 1 promise |
| Toast plan cost | +$25/location or more for half the group | the real price is $84+; retest the value story |

---

## 6. Technology and Integration Strategy

### 6.1 What works today

The current demo renders menus and interaction flows. The CSV/Google Sheets import bridge and manual editor are the parts that can go live without Toast approval once built. They are not a temporary workaround; they are the fallback that lets the first groups pay before certification lands.

### 6.2 Toast access: the four-way distinction

| Category | Status |
|---|---|
| **Works without Toast approval (planned production scope)** | CSV/Sheets import, manual editor, Garnsh-hosted pages, QR views, board rendering |
| **Demonstrated in the demo** | Per-location menu rendering, preview/publish interaction, version history, rollback |
| **Requires Toast approval or certification** | Production Menus API access, Partner Connect listing, Gen 2 Orders API |
| **Unverified** | Whether a customer's own read-only credentials may lawfully power a public-facing website; partner fees and revenue share; certification timeline |

The plan must not describe the Toast integration as approved, production-ready or commercially permitted. It is not. The partner application is submitted in week one because it is the longest-lead item in the company.

### 6.3 The day-120 gate

The original gate ("approval in hand or clearly in process") is subjective. Replace it with four objective tests. By day 120, Garnsh must have:

1. a named Toast partner contact;
2. a written timeline for the application;
3. a sandbox credential or a written reason it has not been issued;
4. a written position on whether customer-supplied credentials may be used for public-facing menu publishing.

If all four are absent, redirect effort to the import bridge and the multi-POS path, or stop. "In process" is not a status.

### 6.4 Fallback and architecture

The internal model is "menu document in, surfaces out." Toast is an adapter, not the architecture. That costs about a week now and saves the company later. The fallback is:

- CSV/Sheets import plus manual editor for the first groups;
- a second POS adapter (Square, then Clover) by month 18;
- no dependency on Gen 2 ordering for the Gen 1 business case.

### 6.5 Technical risks

- **API terms.** The legal right to use customer credentials for a public website is unverified.
- **Certification delay.** Gen 2 revenue depends on a process Toast controls.
- **Menu-data hygiene.** Modifiers, pricing tiers and location variants are the hard engineering, not rendering.
- **Tenant isolation and accessibility.** Both are ship gates, not later fixes.

---

## 7. Competition and Differentiation

| Competitor | What they sell | Price signal | Garnsh's opening |
|---|---|---|---|
| Toast native (Websites, Online Ordering, Delphi boards) | Website, ordering and boards inside Toast | Bundled with POS plans | Generic templates; menus on Toast properties; publishing discipline is not the product |
| Agencies / freelancers | Hand-built sites and manual menu updates | Project fee + retainer | The real incumbent; slow and manual. Also a reseller channel |
| Marqii | Menu sync to Google, Yelp, Apple, Facebook | Mid-market, unpublished | Distribution, not rendering; a partner or acquirer, not a direct rival |
| Popmenu | Website, menu and marketing | $159–$499 / location / month | Marketing suite first; menu accuracy is not the core claim |
| BentoBox | Restaurant websites and ordering | Unpublished; Clover-only in 2026 | Its Clover move leaves the Toast-side gap open |
| Owner.com | Website, ordering and marketing | $249/month + 5% of orders, or $499 flat | Aimed at independents; per-order fees |
| Lunchbox / ChowNow | Enterprise ordering and apps | $229–$499 / location / month | Ordering-first and expensive; Gen 2 is where they collide |

**Advantages.** Publishing craft — versioning, rollback, last-known-good, per-location mapping — done better than the alternatives; no requirement to change POS, website or ordering vendor; a design-led product in a category where incumbents look dated; and a switching cost once every location is mapped.

**Disadvantages.** No technical moat in reading a menu API; Toast dependency; a two-person team; and a price that must be validated. The plan should not pretend otherwise.

**Defensibility over time.** Switching cost, showcase case studies, Toast partner certification/marketplace presence, and a multi-POS adapter. None is strong on day one; all compound.

---

## 8. Operations and Management

### 8.1 Team

Two founding partners. Names and role split are to be completed in the operating agreement. Four functions must each have a named owner from day one: product/engineering, Toast integration and certification, sales/operator relationships, and onboarding/support. With two people, each owns two. "We both do sales" means nobody does support during a Friday dinner rush.

### 8.2 Founder hours

The 2027 budget is 1,410 hours:

| Activity | Hours | Basis |
|---|---|---|
| Build | 400 | 10 weeks × 40 hours total |
| Selling | 270 | 60 conversations × 3 hours + 15 pilots × 6 hours |
| Onboarding | 420 | 15 groups × 14 locations × 2 hours |
| Support | 60 | ~1 hour/day from October |
| Admin | 260 | 5 hours/week × 52 |
| **Total** | **1,410** | **13.6 hours/week each** |

Split 60/40 on the build, 30/70 on sales, 50/50 elsewhere:

| Quarter | Founder A (build lead) | Founder B (sales lead) | Part-time capacity |
|---|---|---|---|
| Q1 2027 | 17.6 h/week | 14.7 h/week | 20 h/week each |
| Q2 2027 | 15.4 h/week | 16.4 h/week | 20 h/week each |
| Q3 2027 | 8.0 h/week | 9.7 h/week | 20 h/week each |
| Q4 2027 | 12.0 h/week | 14.6 h/week | 20 h/week each |

The real peak is 17.6 hours/week for the build lead in Q1, 88% of a 20-hour part-time week with no slack. At a 12-week build it is 20.3 hours/week, at the ceiling. If one founder builds alone, that founder carries 26.8 hours/week, which is full-time. The plan must choose: a 10-week two-founder build at ~18 hours/week each, or a 10-week full-time build lead.

### 8.3 Support and hiring

Support becomes a founder's full day at roughly 150 live locations. Budget a part-time support contractor at **$2,500/month** from that point, funded from revenue. The model puts that in October 2027.

Hiring gates are thresholds, not dates:

- **Engineer:** $35K MRR. The model crosses it in August 2028 and books the hire from July; move to October if the gate must be literal.
- **Growth/partnerships:** $50K MRR, reached in October 2028.
- **Second engineer and founder salaries:** 2029, funded from operating cash.
- **Founder pay:** $0 in 2027, $6,000/month total from July 2028, $100K total in 2029.

### 8.4 Legal and operating checklist

Before the $10,000 moves: operating agreement with decision rights and a deadlock clause; four-year vesting with a one-year cliff for both founders; IP assignment from both partners to the entity, including the pre-entity demo and site; buy-sell/right of first refusal with a valuation formula; trademark search and filing for "Garnsh" (USPTO classes 9 and 42); separate bank account and books; tech E&O and cyber insurance; contractor agreements with IP assignment.

---

## 9. Financial Plan

### 9.1 Model basis

The financials come from a 36-month cohort model. It tracks groups, locations, revenue, cash collection, onboarding labor, churn and cash. It is a planning model, not a forecast.

Key assumptions:

| Assumption | Base | Downside | Status |
|---|---|---|---|
| Average group size | 14 locations | 10 locations | MODELED |
| Group logo churn | 1.5%/month | 2.5%/month | MODELED — no data |
| Location churn | 0.5%/month | 1.0%/month | MODELED — no data |
| Subscription collection | Same month (card on file) | 30-day lag | MODELED |
| Setup collection | 50% at go-live, 50% next month | Same | MODELED |
| Onboarding labor | 2h/location at $60/h | 4h/location | MODELED |
| 2027 onboarding funding | Founders unpaid | Paid contractor | MODELED |
| Support contractor | $2,500/month from 150 locations | Same | MODELED |
| Price | $59 core, $40 boards | $59 | MODELED |
| Toast plan cost | Excluded | Excluded | UNVERIFIED |

### 9.2 2027 by quarter

| Quarter | Revenue | Cash from operations | Economic result | Cash at quarter-end |
|---|---|---|---|---|
| Q1 | $0 | −$13,150 | −$13,150 | $6,850 |
| Q2 | $4,753 | $550 | −$9,530 | $7,400 |
| Q3 | $11,753 | $3,888 | −$2,832 | $11,288 |
| Q4 | $25,689 | $12,604 | $4,954 | **$23,892** |

The trough is **$5,923 in April**, $923 above the $5,000 floor. Peak capital deployed is $14,077; capital is returned in December. The cash result is positive because the founders perform onboarding unpaid. Monthly detail is in Appendix A.

### 9.3 The 2027 onboarding problem

The 2027 cohort adds 210 live locations. At two hours per location and $60 per hour, that is **$25,200 of labor**.

- **If the founders do it:** cash cost is $0; economic cost is $25,200; the year's economic result is **−$20,558**.
- **If the first 14-location cohort is paid:** April cash falls from $5,923 to **$4,243**, breaching the $5,000 floor.
- **If all 2027 onboarding is paid:** the cash trough is **−$6,386 in October** and year-end cash is **−$1,308**. The company runs out of money.

This is the single most important operating constraint. The $20,000 capitalization only works if the founders perform 2027 onboarding. If they cannot, the company needs roughly $25,000 of additional capital or a much slower launch.

### 9.4 Three-year summary

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Revenue | $42,195 | $440,883 | $1,287,970 |
| COGS (cash) | $10,103 | $111,882 | $237,955 |
| Gross profit (cash) | $32,093 | $329,001 | $1,050,015 |
| Gross margin (cash) | 76.1% | 74.6% | 81.5% |
| Operating costs | $27,450 | $163,600 | $614,988 |
| Cash from operations | +$3,892 | +$163,901 | +$437,277 |
| Economic result | −$20,558 | +$165,401 | +$435,027 |
| Year-end cash | $23,892 | $187,794 | $625,070 |
| Net groups | 14.1 | 45.8 | 89.6 |
| Live locations | 193 | 615 | 1,183 |
| Exit ARR | $88K | $698K | $1.63M |
| Cash floor during year | $5,923 | $25,315 | $186,155 |

The 2028 and 2029 figures include churn and the gross adds required to replace it. The model adds 37 gross groups in 2028 and 56 in 2029 to end with 46 and 90 net groups. The extra onboarding and setup cost is visible in the model; a gross-add-only plan would overstate profit.

### 9.5 Unit economics per group

At 14 locations and the 2028 blended ARPU of $98:

| Line | Amount |
|---|---|
| Monthly revenue | $1,372 |
| Recurring gross profit (89%) | $1,221 |
| CAC (18 selling hours × $55 + $600) | $1,590 |
| Onboarding labor (14 × 2h × $60) | $1,680 |
| Less setup fee | −$1,500 |
| Net onboarding cost | $180 |
| Upfront investment | $1,770 |
| Payback | 1.45 months |
| Average life at 2.0% revenue churn | 50 months |
| LTV | $61,054 |
| LTV:CAC | 38.4x |

The 2.0% revenue churn is 1.5% group churn plus 0.5% location churn. At the downside 3.5%, LTV is $24,920 and LTV:CAC is 13.0x. Both are attractive; the constraint is cash and founder time, not unit economics.

### 9.6 Cash flow, working capital and reserve

The base case assumes card-on-file subscription collection in the same month and setup fees collected 50% at go-live and 50% the following month. That produces $750 of accounts receivable at the end of 2027 and $2,250 at the end of 2028.

A 30-day subscription lag is a realistic downside for larger groups. It lowers the 2027 trough to **$4,355 in June**, below the floor, and 2028 year-end cash to $123K. The plan should not assume same-month collection for enterprise accounts without confirming the billing terms.

The $5,000 reserve is a hard floor, not a buffer. If cash falls below $5,000 before recurring revenue passes $3,000 per month, the company stops spending, stops building and sells what exists.

### 9.7 Downside

The downside combines 10-location groups, a 1-in-6 close rate (four live by June), 2.5% group churn, 1.0% location churn and a 30-day collection lag.

| | 2027 | 2028 | 2029 |
|---|---|---|---|
| Revenue | $30,398 | $276,518 | $694,112 |
| Cash from operations | −$4,474 | +$18,971 | −$129,486 |
| Economic result | −$16,743 | +$46,810 | −$94,132 |
| Year-end cash | $15,526 | $34,497 | −$94,989 |
| Net groups | 13.6 | 36.7 | 67.1 |

The downside breaches the 2027 floor in September ($3,171) and is insolvent in 2029 at the planned cost base. The response is not to hope: freeze the 2029 hires, run one engineer and a support contractor, and hold operating costs near $395K. At that cost level, 2029 revenue of $694K and COGS of $173K produce roughly **$126K of operating result** and positive cash. The downside is survivable only with that cost response.

### 9.8 Sensitivities

The cases that matter are group size, close rate, launch timing, churn, collection timing, onboarding funding, onboarding hours and price. Group size 10 cuts 2027 revenue to $32,282 and leaves the trough at $5,492. A 1-in-6 close rate leaves revenue at $40,974 and the trough unchanged at $5,923; its cost is 50% more selling time. A slow launch (three live by June) lowers revenue to $33,984 and the trough to $5,169. A 30-day collection lag takes the trough to $4,355, below the floor. Paying for 2027 onboarding takes it to −$6,386. Onboarding at four hours per location cuts the 2027 economic result to −$45,758. A $45 core price leaves revenue at $34,284 and the trough at $5,572. The full table is in Appendix A.2.

### 9.9 What the model cannot tell you

It cannot tell you whether groups will pay $59, whether Toast will approve the partner application, what the revenue share will be, or whether the first 10 design partners will convert. It cannot price the case studies or model a founder quitting. Those are the risks in §10, not spreadsheet cells.

What it can tell you is narrower: at these prices, costs and churn assumptions, the company survives its own base case with $5,923 at the worst moment, provided the founders absorb 2027 onboarding. It does not survive paid onboarding on $20,000. That is the boundary of the plan.

---

## 10. Risks, Milestones and Execution

### 10.1 Principal risks

| Risk | Impact | Mitigation |
|---|---|---|
| Toast denies or delays access | No clean menu feed at scale; Gen 2 impossible | Apply week one; objective day-120 gate; import bridge; multi-POS by month 18 |
| No demand at $59 | Revenue does not cover the cost base | 10 interviews before pricing; 40 conversations; design partners; cut to conservative cost line |
| Founder capacity | Build, sales and onboarding collide | 1,410-hour budget; 15 March checkpoint; hire/contract only at gates |
| Setup fee loses money | Each 14-location group costs $180 to onboard | Cap at 2h/location or raise setup to $2,500 |
| 2027 onboarding paid | Cash exhausted | Founders perform it; otherwise raise ~$25K or slow the launch |
| Churn higher than 1.5% | LTV and growth fall | Annual contracts; QBRs; measure from first cohort |
| Collection lag | Trough breaches floor | Card-on-file; deposit; 50% setup at signing |
| API terms unverified | Legal/ToS exposure | Pre-sale legal checkpoint; no public-facing use until confirmed |
| Competition | Toast ships natively or agencies bundle | Publishing craft; multi-surface; agency channel; certification |
| Accessibility/legal | ADA exposure; enterprise blocker | WCAG 2.1 AA ship gate; E&O insurance; contract terms |

### 10.2 2027 milestones

| When | Milestone |
|---|---|
| Jan 2027, week 1 | Entity formed; $20,000 paid in; operating agreement, vesting and IP assignment signed; Toast partner application submitted |
| Jan–Mar | Build Gen 1; ship CSV/Sheets bridge; 40-group target list; pricing interviews; legal checkpoint on Toast credentials |
| 15 Mar | First design partner signed. If not, run the delay case: freeze travel and demos, move certification, cut launch scope |
| Mar–Jun | 10 design partners signed; six live and paying by June (about 84 locations) |
| Day 120 (~May) | Toast gate: named contact, written timeline, sandbox credential, written position on customer credentials |
| H2 2027 | Four design partners live; five full-price groups; case studies; agency channel first groups |
| Dec 2027 | 14 net groups, 193 live locations, 142 paying; $42K revenue; cash floor $5.9K; capital returned December |

### 10.3 Gates and kill criteria

- **Day 120 Toast gate:** if the four objective tests are not met, pivot to import + multi-POS or stop.
- **Day 180 sales gate:** fewer than 4 of 10 design partners signed, or fewer than 3 live and paying, means the ICP, price or sales motion is wrong. Do not add features; re-interview.
- **Cash floor:** below $5,000 before $3,000/month recurring revenue means stop and sell.
- **Gross margin:** below 75% at 100 live locations for two consecutive months, including onboarding labor at $60/hour, means the unit economics are broken. At 100 locations and 2h/location, gross margin is 77.9%; at 4h/location it is 61.5%.
- **Churn:** above 3% monthly group churn after 25 groups means the product is not embedded; stop marketing and fix onboarding.

### 10.4 Fundraising

The company is not raising now. The milestones that justify a round are:

- 10 paying groups and approximately 140 paying locations;
- at least six months of measured churn;
- a clear Toast status: approved, rejected or a named path with a date;
- a CAC and payback measured from real cohorts, not founder estimates;
- one 20+ location group on an annual contract.

A round at that point would fund engineering, certification and the first sales hire. It would not fund survival; the $20,000 and revenue must do that.

---

## 11. Conclusion

Garnsh is a narrow, credible Gen 1 business: menu publishing for multi-location Toast groups. The problem is real, the product boundary is honest, and the unit economics work if the price holds. The risks are Toast access, demand and founder capacity, not the arithmetic.

The plan is deliberately small. It does not assume ordering, payments or a branded app. It does not assume customers it does not have. It assumes two founders can build a useful product, sell ten design partners and learn whether the market will pay $59 per location before spending money the company does not have.

That is the right test. If it passes, Garnsh has a business worth scaling. If it fails, it fails cheaply and in public, with the evidence written down.

---

## Appendix A — Financial model assumptions

**Revenue.** Per-location subscription, recognized monthly. Lists: $59 core, $40 boards, $99 ordering (2028+), $149 app (2029). Attach rates: boards 5% (2027), ramping to 55% (2028) and 65% (2029); ordering 0% (2027), 17% (2028), 28% (2029); app 0% (2027–28), 3.5% (2029). Setup $1,500 per group, recognized at go-live.

**Cohorts.** 2027: 15 gross groups (6 showcase, 4 design partners, 5 full-price). 2028: 37 gross groups. 2029: 56 gross groups. Net of churn: 14.1, 45.8, 89.6 groups.

**Churn.** Group logo churn 1.5%/month; location churn 0.5%/month. Downside 2.5% and 1.0%. Churn is applied monthly to active groups and locations.

**Onboarding.** 2h/location at $60/hour. 2027: founders perform it; cash $0, economic cost $25,200. 2028–29: contractor, cash cost. Downside 4h/location.

**Cash.** Subscription collected same month in the base, 30-day lag in the downside. Setup 50% at go-live, 50% next month. Expenses paid in month incurred. AR tracked.

**Costs.** Infrastructure $1.70/location/month. Payment fees 2.9% of revenue. Support $2,500/month from 150 live locations; 2029 support team $7,500/month. 2028 marketing/travel/design MRR-gated: travel at $15K MRR, marketing at $25K, design at $35K. 2029 fixed operating costs $614,988.

**Capital.** $20,000 paid-in January 2027. No debt, grants or outside equity in the base case.

### A.1 2027 monthly cash

| Month | Live locations | Paying locations | Revenue | Cash from operations | Economic result | Cash |
|---|---|---|---|---|---|---|
| Jan | 0 | 0 | $0 | −$4,617 | −$4,617 | $15,383 |
| Feb | 0 | 0 | $0 | −$5,617 | −$5,617 | $9,766 |
| Mar | 0 | 0 | $0 | −$2,916 | −$2,916 | $6,850 |
| Apr | 14 | 14 | $344 | −$927 | −$2,607 | $5,923 |
| May | 42 | 42 | $1,364 | $27 | −$3,333 | $5,949 |
| Jun | 83 | 83 | $3,045 | $1,451 | −$3,589 | $7,400 |
| Jul | 109 | 81 | $3,997 | $2,468 | −$892 | $9,868 |
| Aug | 121 | 80 | $3,917 | $2,858 | $1,178 | $12,726 |
| Sep | 133 | 78 | $3,839 | −$1,438 | −$3,118 | $11,288 |
| Oct | 158 | 104 | $7,617 | $2,486 | $626 | $13,774 |
| Nov | 183 | 130 | $9,216 | $4,296 | $936 | $18,070 |
| Dec | 193 | 142 | $8,856 | $5,823 | $3,393 | $23,892 |

### A.2 Sensitivities

| Case | 2027 revenue | 2027 economic result | 2027 trough | 2028 cash floor |
|---|---|---|---|---|
| Base | $42,195 | −$20,558 | $5,923 | $25,315 |
| Group size 10 | $32,282 | −$15,027 | $5,492 | $23,082 |
| 1-in-6 close | $40,974 | −$21,635 | $5,923 | $24,259 |
| Slow launch (3 live June) | $33,984 | −$25,611 | $5,169 | $20,412 |
| 2.5% group churn | $40,672 | −$21,979 | $5,923 | $23,406 |
| 30-day collection lag | $42,195 | −$20,558 | $4,355 | $15,979 |
| 2027 onboarding paid | $42,195 | −$20,558 | −$6,386 | $115 |
| Onboarding 4h/location | $42,195 | −$45,758 | $5,923 | $18,595 |
| Core price $45 | $34,284 | −$28,239 | $5,572 | $15,559 |
| Toast denies ordering | $42,195 | −$20,558 | $5,923 | $25,315 |
| Toast denies ordering + app | $42,195 | −$20,558 | $5,923 | $25,315 |

## Appendix B — Evidence register

The full register is a separate deliverable. The main classifications:

- **VERIFIED:** Toast Q3 2026 location count (189,000), ARR ($2.5B), net adds (~8,500); Toast standard API is read-only, per-location, Menus V2; Toast partner process is gated; Toast Websites is view-only.
- **MODELED:** market share of 10+ groups (10–20%), pricing, attach rates, churn, CAC, onboarding hours, conversion, 2027–29 financials, SOM share.
- **UNVERIFIED:** whether customer credentials may power a public website; partner fees/revenue share; certification timeline; Toast plan cost per location; competitor prices not published; demand at $59.

## Appendix C — Sources

- Toast Q3 2026 results (investor relations / Business Wire, 3 November 2026): ~189,000 locations, +21% YoY, ARR $2.5B, ~8,500 net new locations.
- Toast developer documentation (2026): partner program, Menus API, standard API access, Orders API.
- Toast support documentation (2026): Websites View-Only, Online Ordering menu constraints.
- Published competitor pricing roundups (October 2026): ChowNow, Popmenu, Owner.com, Lunchbox, BentoBox.
- US restaurant counts: industry reporting, 700,000+ eating and drinking establishments (2024–2026).
- Founders' working notes and the Garnsh demo site, November 2026.

*Where a claim is not sourced above, it is an assumption and is labeled MODELED or UNVERIFIED in the register.*

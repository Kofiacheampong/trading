# Garnsh — Business Plan

*v2.4 · 10 November 2026 · financials rebuilt on a 36-month cohort-level cash model (§10)*

Prepared 7 November 2026 · revised 10 November 2026 · Status: Draft v2.4. Every number that is an assumption is labelled as one. Verified market facts are sourced at the end. The provenance of the two source drafts is recorded in the Sources section.

## 1. Executive summary

Garnsh is a software-as-a-service (SaaS) product for restaurant groups that run Toast point of sale (POS). It is built on one observation about enterprise restaurant groups: they keep their digital sales channel in their own hands, not Toast’s. They run Toast gladly as the system of record — POS, payments, kitchen, reporting — but they want their own website, their own ordering experience, and their own guest relationship. Toast offers them templates inside Toast’s properties instead, and offers no open application programming interface (API) to connect a Toast menu to a website of their own. So the connection gets built by hand, and the menu guests see drifts away from the menu in Toast: prices change and the website keeps the old PDF; a discontinued item stays on the QR page and the board until someone remembers to edit both; the airport location’s prices end up on the flagship’s menu board.

Garnsh is the layer that closes that gap. It takes the menu the team already maintains in Toast and publishes branded, per-location versions of it everywhere guests read it: the group’s own website (embed) or a hosted page, QR menus, and in-store menu boards — with preview-before-publish, version history, rollback, and a last-known-good fallback so a bad sync never leaves a blank board during service. The wedge is menu release discipline: Garnsh treats a menu the way engineering treats a deploy — draft, preview, publish, rollback, with an audit trail.

Generation 1 is deliberately not real-time. A change made in Toast reaches guests when someone previews and publishes it, and publish-time control is only worth paying for if the operator can see what is waiting to be published. Without that visibility, a publish step does not fix drift; it moves the stale-menu problem one step earlier. The argument that groups want to own the ordering experience belongs to Generation 2. Generation 1 has to earn its price on menu accuracy and consistency alone, and the plan is now written that way.

The plan in one paragraph: Two partners capitalize the company with $10,000 each ($20,000 paid-in, January 2027). Generation 1.0 (2027) ships menu publishing — custom menus, order-ready menu boards, custom location picker — and signs 10 showcase restaurant groups (10+ locations each) by June: six live and paying, four free design partners, 15 groups and 210 locations live by December, of which 154 pay. The Toast partner application is submitted in week one, because Generation 2.0 (2028) — custom online ordering on the group’s own website — requires full Toast partner certification, and that clock is the company’s critical path. Generation 3.0 (2029) adds a custom branded mobile app and e-commerce. Base-case scenario: ~15 groups / ~210 locations by end of 2027, ~46 groups / ~644 locations by end of 2028, ~92 groups / ~1,288 locations by end of 2029; $1.35M of revenue and $1.79M of exit annual recurring revenue (ARR) in 2029. A conservative case (slower signings, no app revenue) is modeled in §10 alongside it — roughly $661K exit ARR by year three. On either case the business is cash-lean and founder-built; the conservative case is still a profitable niche business, not a failure. The 2027 plan is deliberately thin: the cash floor is $5,923, and a two-month slip in first go-live breaches it; the 15 March protocol lifts the trough only to $5,673, which is $673 of headroom.

The single biggest risk is not competition — it is Toast itself: partner approval, marketplace economics, and Toast shipping this natively. Section 7 treats that dependency as the critical path, with a hard decision gate at day 120. Section 14 sets kill criteria in advance, in writing.

## 2. The problem

The problem is control. A restaurant group’s digital front door — its website, its online ordering, and the guest relationship that flows through both — is the most valuable sales channel it owns. Enterprise groups know this, and most of them keep that channel in their own hands, not Toast’s. They run Toast because it is an excellent system of record: POS, payments, kitchen, reporting. They do not want Toast’s templates as their brand’s public face, Toast’s modules as their ordering experience, or their guest relationship living inside Toast’s properties instead of their own. Toast is the engine. They want to own the storefront.

That choice creates a structural gap, because Toast’s architecture assumes the opposite — that the guest-facing layer also lives inside Toast:

### Why Toast’s own answer doesn’t fit enterprise groups

Toast Websites is a template site builder aimed at operators who need a website, not groups with brand teams, agencies, and existing web properties. Its menu channel is literally called “Websites View-Only” — the menu appears on your Toast Website, view only, not orderable (Toast’s own support documentation). A group with its own site gets nothing from this.

Toast Online Ordering runs on Toast’s pages, in Toast’s frame, with limited customization — and the menu cannot even differ between Toast Online Ordering and the Toast Local app (Toast support documentation). The guest experience, the checkout flow, and the customer relationship belong to the platform, not the brand.

So enterprise groups do what the platform doesn’t plan for: they keep their own websites and their own ordering ambitions, and the connection between Toast and those properties has to be built by someone else — or maintained by hand.

### The API wall (verified against public sources)

The obvious fix — “just connect the Toast menu to our website with an API” — does not exist as an open option:

Toast’s Menus API is real but partner-gated. The documentation is public; the credentials are not. Production API access is issued only to vendors accepted into Toast’s partner program after vetting, a signed agreement, and certification. As one 2026 industry guide puts it: “Anyone can read the docs. Almost no one can call the API.” There is no self-serve public API that a restaurant or its web developer can use to publish the Toast menu to the group’s own website.

The one self-serve door is not a website door. Toast’s “standard API access” lets a restaurant pull its own data, read-only (GET requests only, and only the older Menus V2), and Toast positions it for reporting and internal use. It requires a Restaurant Management Suite Essentials subscription per location, every request targets a single location, and it can never write anything — no orders, ever. It is a reporting tool for a group’s own analysts, not a supported way to power a public website, and it does not work as a publishing pipeline across dozens of locations.

Writing is fully locked. Anything that creates data in Toast — above all, injecting online orders from a group’s own ordering front-end — is reserved to certified partners. A group that wants its own ordering experience flowing into Toast can only get there through a partner’s product, or by becoming one.

The practical result: the menu on a group’s own website gets maintained manually, by export, by scraping workarounds, or on an agency retainer — and the group’s ordering ambitions wait on a short list of expensive enterprise platforms (see §6).

### What guests actually see

Meanwhile the group runs one operational menu (in Toast) and presents it in at least four places: their website, third-party and QR menus, in-store boards/screens, and printed pieces. Each surface is maintained separately, usually by hand, usually by someone whose real job is running restaurants.

The failure modes are constant and visible to guests:

Price drift — Toast says $16.25, the website PDF says $14.50. A guest who sees $16 on the QR menu and is charged $18 is a comp, a bad review, and in some jurisdictions a consumer-protection exposure.

Dead items — discontinued items and last season’s menu linger on the website, the QR page and the boards for weeks, because removing them means editing every surface separately.

Wrong-location menus — one location’s pricing or items shown at another.

Stale PDFs — the website menu is a PDF from two menu cycles ago because updating it means calling the web person — and when that person quits, the knowledge leaves with them.

No safety net — a broken integration or a bad publish leaves a blank board or an error page during service.

### What Generation 1 does — and does not — fix

Generation 1 fixes accuracy at the moment of publish. A price, item or location change is captured when the operator reviews the draft and publishes a new version, and is consistent across every surface from that moment on. It is not immediate: nothing reaches guests until a person publishes, and a change typed into Toast during service is not on the website until someone publishes it.

Three consequences are stated plainly, because the product’s credibility depends on them:

- **86 status and live stock are out of scope for Generation 1.** Garnsh does not track availability and does not claim to. An item marked 86 in Toast stays on the published menu until the menu is republished without it.
- **“Real-time” is not a claim Garnsh makes.** The site’s FAQ already says this: no live stock, no 86 status, no guaranteed sync timing. The plan uses the same words rather than implying otherwise.
- **The control thesis is a Generation 2 argument.** Owning the guest relationship — ordering on the group’s own domain — is what Generation 2 sells. Generation 1 sells a smaller, verifiable thing: the same menu, everywhere, without drift, with a rollback when someone gets it wrong.

For a 10+ location group this is not a cosmetic issue: it is a steady stream of small guest-facing errors, multiplied by every surface, with no single person able to fix them at the source.

## 3. The product

Positioning line (from the live site): “Your menu, everywhere. Get more from the menu you already run in Toast.”

### Generation 1.0 — 2027: Menu publishing

Custom menus — the Toast menu rendered on the group’s own website (embed) or on a Garnsh-hosted page per location, styled to the brand.

Custom order-ready menu boards — designed displays for in-store screens, fed from the same source menu.

Custom location picker — each surface mapped to the correct location’s menu and prices.

QR menus — per-location phone view opened by a printed code.

Publishing controls — preview every surface before publishing, deliberate publish (not silent auto-sync), full version history, one-click rollback, and last-known-good serving if anything upstream breaks.

Generation 1 is a publish-time system, not a live-sync system. It does not read or display 86 status, stock levels or table availability, and it makes no real-time claim (see §2). Publish-time control is only valuable if unpublished changes are visible, so two requirements follow — both **ASSUMPTION**, product scope, not yet built:

- **Bulk publish across locations (ASSUMPTION).** One review, one publish action, every selected location. Without it a 14-location group repeats the same click fourteen times, and the product recreates the labour it replaces.
- **Unpublished-change alert (ASSUMPTION).** When the Toast source has changed since the last publish, the dashboard says so, per location. Without it, "deliberate publish" becomes a tidy name for silent drift.

Neither is in the current demo. Together they are the difference between a publishing tool and a menu that is actually right. They are assumed inside the 8–12 week build estimate in "Honest product debt"; if they are not, that estimate is wrong and Q1 scope has to be re-cut.

A non-API bridge, shipped on purpose — CSV/Google Sheets import plus a manual editor, so the first groups can go live and pay before any Toast approval lands (see §7). It is a bridge, not the product.

### Generation 2.0 — 2028: Custom online ordering

A branded ordering front-end on the group’s own website — their domain, their design, their guest relationship — with orders written into Toast through the certified partner Orders API. This is the product enterprise groups actually ask for (see §2), and it is the plan’s prize: it is also where the money and the platform risk both concentrate, so it is gated on ordering-partner certification (see §7).

Scope guardrail: Gen 2 is built on Toast’s partner ordering rails wherever the certification allows, so card handling stays with Toast. Owning checkout outright — Garnsh’s own cart, payments, refunds, sales-tax and tip logic — is a separate, later decision (2029 at the earliest, and only under a signed partnership that makes it safe), because it changes the company’s regulatory identity (PCI DSS scope, chargeback handling, support measured in minutes) and puts Garnsh head-on against Toast’s core revenue. The distinction matters: order injection by certified partners is a sanctioned Toast category — ChowNow, Lunchbox, and Olo do it for a living. It is gated and expensive, not forbidden.

### Generation 3.0 — 2029: Owned guest channels

Custom branded mobile app per group.

Custom e-commerce — merchandise, gift products, packaged goods under the group’s brand.

Kept as vision funded from revenue, not as a dated commitment: branded-app install rates collapse below ~25 locations, so Gen 3 sells only to the top of the base.

### What Garnsh is not

Not a POS, not a delivery network, not a marketplace.

Not a live inventory, 86-status or real-time sync system. Generation 1 publishes versions; it does not mirror kitchen availability.

Not affiliated with or endorsed by Toast (the site already states this correctly — keep that disclaimer everywhere).

### Scope decision — 86 status

86 and live availability are an explicit non-goal for Generation 1 and are not sold, quoted or implied. It is not a roadmap item, and nothing public — site, deck, contract or sales script — may imply a future 86 feature. Internally, the founders will revisit on two triggers only: 86 appears as the top pain in more than three of the ten Q1 2027 pricing interviews, and a check of what Toast's API actually permits for availability data. Even then, the outcome is a decision to evaluate, not a commitment. Owner: both founders. Date to be set by the founders.

### Honest product debt

The current build is a strong demo with real interaction design. To be sellable it needs: a real ingestion path (§7), tenant authentication and isolation, per-location asset management, an upload pipeline for logos/fonts, board scheduling, and an accessibility pass to WCAG 2.1 AA (Web Content Accessibility Guidelines). Budget roughly 8–12 weeks of focused work — it is a quarter, not a weekend, and the Q1 2027 plan is sized to it.

## 4. Target customer

Ideal customer profile (ICP): restaurant groups with 10+ locations, all on Toast, with a brand worth protecting — regional fast-casual and casual-dining groups, multi-unit franchisees, and growing concepts in the 10–50 location band. The roadmap evolves the target to 25+ location groups as the ordering and app generations land.

Why this segment:

- Below 10 locations, the pain is real but the budget and the brand risk are small; a single-location operator tolerates a stale PDF.
- At 10+ locations, menu inconsistency is a brand and revenue problem with an owner — usually a small marketing/ops team that currently copy-pastes menus for a living.
- Groups standardize on one POS, so one integration (Toast) covers the whole estate in a single sale. One signature = 10–50 locations of recurring revenue.
- Multi-unit accounts churn at roughly 1–1.5% per month versus 4%+ for independents, because switching means re-mapping every location.

Buyer: VP of Marketing, Director of Operations, or the founder-operator in smaller groups. The pitch is operational — your menus are wrong in public, and your ordering runs on someone else’s pages; Garnsh fixes the menu first — not technical.

**Positioning must match the ICP.** The product is sold to multi-unit groups, and every surface that recruits customers must lead with them. Site copy that opens with "restaurants using Toast" and a single-location demo recruits the segment this plan deliberately does not serve: one operator, one menu, and a support cost that exceeds the subscription. The site's hero, demo and FAQ should lead with groups, per-location pricing and location mapping; a single-location visitor can be served through the guided pilot, but is not the audience the copy is written for. Canonical domain: addgarnsh.com.

An open strategic question, stated honestly (see §15): the review draft argued the opposite growth direction — that growth comes from adding POS platforms (Square, Clover, Lightspeed) and moving down into 3–9 location groups once onboarding is self-serve, because chasing ever-bigger accounts brings enterprise incumbents and 6–9 month cycles a two-person company cannot service. This plan keeps the founders’ 10+ → 25+ direction for 2027 (it matches where the control pain and the budgets are), adopts multi-POS as a year-two hedge (§7), and leaves the down-market question to be decided with real churn and sales-cycle data in hand — not by assertion in either draft.

## 5. Market

Verified facts (Toast’s own reporting, Q3 2026):

- Toast runs approximately 189,000 locations, up 21% year over year, with annualized recurring revenue of $2.5 billion as of September 30, 2026.
- It added ~8,500 net new locations in Q3 2026 alone, including enterprise wins like an 800-location bagel group — evidence Toast is pushing upmarket into exactly Garnsh’s target segment.
- Toast itself estimates its US restaurant locations are about 20% of the US restaurant market, and the US has well over 700,000 eating and drinking establishments.

Sizing (assumption-driven — no public source breaks out Toast locations by group size):

- **Assumption:** 10–20% of Toast’s 189,000 locations sit in groups of 10+. That is a serviceable addressable market (SAM) of roughly 19,000–38,000 locations.
- At a blended $89 per location per month, that SAM is worth roughly $20M–$40M in annual recurring revenue for the menu-publishing layer alone, before ordering and app revenue.
- Conservative cross-check (from the review draft): at 8–12% of the base in 10+ groups (15,000–23,000 locations) and $48–$61 blended, the same slice is worth $8M–$17M ARR. The truth is inside that range and cannot be resolved from public data — plan capital against the conservative end and sell against the optimistic one.
- Serviceable obtainable market (SOM) for this plan: ~1,288 locations by end of 2029 in the base case (~900 in the conservative case) — roughly 3–6% of the assumed SAM. Ambitious but not fantasy, if the showcase cohort converts (see §9).

Why now: menu data is becoming a discovery asset (search engines and AI answer engines reward current, structured, machine-readable menu pages; a PDF is invisible to them); digital signage hardware is cheap, so the bottleneck is software; restaurant labor turnover keeps recreating the “person who knew how to update it” failure; and Toast’s base compounds by ~8,500 locations a quarter without Garnsh spending a dollar.

## 6. Competition

| Competitor | What they sell | Price signals (published, Oct 2026) | Garnsh’s opening |
|---|---|---|---|
| Toast native (Websites, Online Ordering, Delphi boards) | Bundled website + ordering inside Toast; Delphi digital menu boards on Toast’s hardware track | Bundled with POS plans | Generic templates, limited brand fidelity; menus shown on Toast properties, not the group’s; publishing discipline (versioning, rollback, per-location control) is not the product’s focus |
| Lunchbox | Enterprise direct ordering, apps, loyalty | ~$300–$499/mo per location per product (enterprise) | Ordering-first and expensive; menu display treated as plumbing. Garnsh Gen 1 undercuts on price and wins on publishing craft — Gen 2 is where they collide |
| ChowNow | Commission-free ordering for independents | $229–$449/mo per location + setup | Built for single/few-location independents; weak multi-location central management |
| Popmenu | Website + marketing + ordering add-on | $159–$499/mo per location | Marketing suite first; menu accuracy/publishing controls are not the core claim |
| Owner.com | Website + ordering + marketing bundle | $249/mo + 5% per order, or $499 flat | Aimed at independents; per-order fees groups dislike |
| Marqii | Menu sync out to Google/Yelp/Apple/Facebook | Mid-market, unpublished | Distribution, not rendering. A natural partner (and plausible acquirer), not a direct rival |
| BentoBox | Restaurant websites + ordering | Not published; now Clover-only | Its move under Clover leaves the Toast-side website/menu gap open — a real opening for Garnsh |
| Agencies / freelancers | Hand-built sites, manual menu updates | Project fees + retainers | The actual incumbent. Slow, manual, and the reason menus go stale — Garnsh sells the automation they can’t; also a reseller channel (§9) |



Moat, honestly stated: there is no deep technical moat in reading a menu API — this is a well-executed product with good design taste, and the plan should not pretend otherwise. The defensible assets are (1) publishing craft — versioning, rollback, last-known-good, per-location mapping done better than anyone; (2) switching cost once every location is mapped and opening procedures reference Garnsh; (3) showcase-group logos and case studies in a relationship-driven industry; (4) Toast partner certification and marketplace presence (Gen 2), a real barrier because the process is slow; and (5) the multi-POS adapter layer once built. None of these is strong on day one. All of them compound. Speed and distribution matter more than features.

## 7. Technology and the Toast dependency (critical path)

This is the section the whole plan hinges on. Toast runs a closed partner ecosystem: documentation is public, but production credentials for multi-restaurant access are issued only to accepted partners. The published partner path has roughly eight stages — application, vetting, signed partnership agreement, build against sandbox, certification review, alpha at one restaurant, beta at three to five locations for several weeks, then listing in Toast Partner Connect (the marketplace inside Toast). Partner fees are not published; trade reporting from 2019 put Toast’s revenue share for ordering partners around 30% — dated, and must be re-verified with Toast directly before Gen 2 pricing is finalized. If a revenue share anywhere near that level applies to Garnsh’s tiers, it compresses margin rather than killing viability — but it changes pricing, so it must be known before scaling, not after.

The access ladder, matched to the roadmap:

Week one, January 2027 — apply. The partner application is the longest-lead item in the company and it is absent from the founders’ original timeline. Submit it in the first week, before the product is finished; the application is about business case, not code. Every week of delay is a week added to Gen 2.

2027 (Gen 1 — read-only): Menu display needs menu reads, not order writes. Toast’s standard API access (included with its Restaurant Management Suite Essentials plan) gives a restaurant read-only credentials to its own data. For pilots and showcase groups, Garnsh connects per-group with the group’s own credentials — no partner program required to start selling. The CSV/Sheets import bridge (§3) covers groups where even that is slow. This is the fastest legal path to revenue.

Day-120 gate (~May 2027): if partner approval is not in hand or clearly in process with a named path by day 120, redirect effort to the multi-POS + import path (item 5) or stop. Do not spend a year building a Toast-dependent company without Toast’s blessing. (Kill criteria, §14.)

2028 (Gen 2 — ordering): Order injection requires ordering-partner certification. Gen 2’s launch date is therefore not fully in Garnsh’s control; certification is a 2027 workstream with a 2028 launch target, the alpha/beta stages map naturally onto the showcase cohort (1 alpha location, then 3–5 beta locations), and Gen 1 revenue must be able to carry the company if certification slips. Never pre-sell an ordering date.

The hedge — POS-agnostic by construction: the internal model is “menu document in, surfaces out.” Toast is an adapter, not the architecture. That costs about a week now and saves the company later. Target a second POS adapter (Square first, then Clover) by around month 18, so a Toast reversal degrades the business instead of ending it.

Architecture implications: Garnsh’s own stack is deliberately boring — a menu ingestion/sync service, a publishing/versioning layer, and four renderers (hosted page, website embed, QR view, board display). The hard engineering is not rendering; it is menu-data hygiene (modifiers, pricing tiers, location variants) and publishing safety. Budget accordingly.

## 8. Pricing (proposed — to be validated in Q1 2027)

The founders’ notes leave pricing open (“finalize pricing” is a Q1 2027 task). This is a proposal built from competitor benchmarks — per-location SaaS in this category runs $119–$499/month, with ordering platforms at the top. Garnsh Gen 1 is a narrower product, so it prices under them and expands wallet share as Gen 2/3 land.

The pricing argument has three parts. First, $59 must be benchmarked against the menu-display and QR tools a group would otherwise buy, not against ordering suites; the comparison set is split below. Second, the sensitivity that matters is a set of absolute prices ($25, $35, $45), not a 10% shave of a blended ARPU; those cases run through all three years and the cash floor. Third, the customer may have to buy a Toast plan to supply API credentials; that cost is a line in the all-in cost, marked for verification.

| Item | Proposed price | Notes |
|---|---|---|
| Onboarding / setup | $1,500 per brand | Brand template build, location mapping, screen setup — covers ~2 hours per location, which is break-even (§10.1). Waived for the 10 showcase groups in exchange for logo use, case study, and testimonial |
| Core publishing (hosted page, embed, QR) | $59 / location / month | The entry product |
| Menu boards add-on | +$40 / location / month | Per location running boards |
| Multi-location management | Included at 10+ locations | Location picker, per-location overrides, group dashboard |
| Gen 2 ordering module (2028) | +$99 / location / month | Deliberately under Lunchbox’s $300–499 enterprise benchmark for the same control; revisit after Toast partner terms (any revenue share) are known |
| Gen 3 branded app (2029) | $5,000 build + $149 / location / month | Premium tier for 25+ groups |
| Enterprise (25+ locations) | Custom, ~$119 / location / month all-in | Annual contract, SLA, priority support |

Every price and attach rate in this table is a founder assumption. None of it has been tested against a real invoice. The Q1 2027 interviews are the test.

### What the customer actually pays

The per-location price is not the invoice. A group also pays setup, may pay for boards, and may have to buy a Toast plan to supply credentials. The all-in number is what the first ten interviews have to test:

| Line | Price | Notes |
|---|---|---|
| Garnsh core publishing | $59 / location / month | List price |
| Menu boards | +$40 / location / month | Only locations with screens |
| Setup | $1,500 / brand | Waived for the showcase cohort |
| Toast plan, if not already carried | +$T / location / month | **NEEDS VERIFICATION — Toast rep.** $0 incremental if the group already runs Restaurant Management Suite Essentials, the plan that includes API access |
| **14-location group, core only** | **$826 / month** | $9,912 / year, plus $1,500 setup |
| **14-location group, core + boards everywhere** | **$1,386 / month** | $16,632 / year, plus setup |
| **Same, if the Toast plan adds $50/loc** | **+$700 / month** | +$8,400 / year — a 51% uplift on the core+boards invoice ($16,632), or 85% on core alone ($9,912) |

The Toast line is the one that can break the value story. A 14-location group already on Essentials pays nothing extra; a group on a cheaper Toast plan may have to upgrade every location. Do not quote an all-in price until this is verified per deal. At $50/location the customer is paying $109–$149 all-in, and the comparison shifts from menu-display tools to website-and-ordering bundles.

### Benchmarks that matter

Two different markets are easy to conflate. Garnsh Gen 1 is not competing with Lunchbox or ChowNow; it is competing with the menu page, the QR code and the manual update. Price against that, and treat the ordering suites as the ceiling for Gen 2.

| Category | Products to price | What to compare | Status |
|---|---|---|---|
| Menu display / QR | UpMenu, MenuTiger, Flowcode, GloriaFood, Marqii | Per-location monthly, menu count, QR, publishing controls | **NEEDS RESEARCH — founders, before the first interview (15 Jan 2027)** |
| Website + menu | Toast Websites (View-Only), BentoBox, Popmenu | Whether the menu is editable per location; whether publishing is versioned | Partly sourced (§6); BentoBox unpublished |
| Ordering suites (Gen 2 ceiling) | Lunchbox, ChowNow, Owner.com | $/location and revenue share | Sourced (§6) |
| The real incumbent | Agency / freelancer retainer | Project fee + monthly retainer + turnaround | **NEEDS RESEARCH — get three live quotes by 15 Jan 2027** |

The point is not to find a lower number to match. It is to establish what a group pays today for a worse outcome. If two menu-display tools do 80% of Gen 1 for $20/location, $59 is a design-taste premium and the plan must say so. If they charge $40–$80 for a menu that still has to be updated by hand, $59 is cheap.

### Price scenarios through the model

The same cohort schedule, costs and cash floor, with only the core price changed. Boards ($40 × attach) and the Gen 2/3 modules are held constant:

| Core price | 2027 revenue | 2027 operating result | 2027 trough | 2028 operating result | 2028 cash floor | 2029 revenue | 2029 operating result | Verdict |
|---|---|---|---|---|---|---|---|---|
| **$59 (base)** | **$44,377** | **+$6,463** | **$5,923** | **+$188,282** | **$30,502** | **$1,349,045** | **+$507,711** | Funds the plan |
| $45 | $35,969 | −$1,702 | $5,582 | +$127,924 | $20,187 | $1,184,797 | +$348,226 | Works, thinner — $159K less 2029 profit |
| $35 | $29,963 | −$7,534 | $5,310 | +$83,669 | $12,819 | $1,067,477 | +$234,308 | Marginal — 2028 runs on $13K |
| $25 | $23,957 | −$13,366 | $2,715 | +$40,413 | $5,451 | $950,157 | +$120,390 | **Fails — 2027 floor breach, insolvent in 2029** |

**Read it plainly.** $59 is the only price that funds the plan as written. $45 works but gives up $159K of 2029 operating result and cuts the 2028 cash floor to $20K. $35 survives 2027 by $310 and then runs the company on $13K of cash in 2028 — one bad month from a founder top-up. $25 breaches the 2027 floor in September, runs 2028 on $5K, and is insolvent in 2029. The pricing question is therefore not “what will they pay?” in the abstract; it is “can we hold $59?” If the interviews say no, the answer is not to cut price and keep the cost base — it is to cut the cost base with it (§10.5).

### The discount rule, resolved

The plan cannot say both “never discount the per-location price” and “discounted year-one pricing.” The resolution:

1. **Standard deals: list price, no exceptions.** The per-location price is the revenue model; a discounted rate compounds for the life of the account. Discount implementation instead — waive setup, add months, add a pilot location.
2. **The showcase program is a capped exception, not a policy.** Ten groups maximum; 20% off core for 12 months from go-live; setup waived; automatic expiry to list at month 13; no renewal at the discounted rate. It is available to nobody else, approved by both founders in writing, and recorded as marketing spend (§9 prices it).
3. **The four design partners are free for 12 months and pay list from month 13.** They are not a discount; they are product-development customers. Their logos, case studies and feedback are the payment.

That is the only version of “discounted year-one pricing” that survives the rule. If the founders are not willing to enforce the expiry, remove the discount and rely on waived setup alone.

**Alternative considered.** The review draft proposed lower tiers ($39 Solo / $69 Growth / $45 Multi at 3+ locations). This plan holds $59 because the product is sold on control and publishing discipline to 10+ groups, not on being the cheapest menu page — but the ladder is the fallback, and the $35 and $25 rows above are the shadow it casts on the model. If the median acceptable price is below $45 — 24% below the $59 list — the ladder wins and the cost base has to move with it.

### Validation triggers (set before the first call)

From the companion interview script, with the model consequence attached:

| Trigger | Threshold | Action |
|---|---|---|
| Median acceptable price | below $45 (24% below $59) | Adopt the $39/$69/$45 ladder, re-run §10, and cut the cost base to the conservative line |
| Credential friction | 3+ of 10 cannot or will not supply Toast credentials | Make the CSV/Sheets bridge the primary path; re-price onboarding (no API setup) |
| Pilot commitment | fewer than 4 of 10 agree to a 30-day pilot | The ICP or the pain is wrong — do not add features; re-interview the 20 who said no |
| 86 status | top pain in more than 3 of 10 | Revisit what Gen 1 promises (§3) |
| Toast plan cost | +$25/location/month or more for more than half the group | The real price is $84+, and the value story must be re-tested at that number |

No price is final until at least 10 interviews are complete. The model keeps $59 as the base because it is the only price that funds the plan; the interviews decide whether the plan is fundable at all.

## 9. Go-to-market

Phase 1 — Showcase cohort (Mar–Jun 2027). Sign 10 groups at 10+ locations. Six are live and paying by June (about 84 locations); the other four go live July–September as design partners, free for 12 months from go-live, converting to list price at month 13. Signing and go-live are separate events, and the model is built on the per-group schedule in §10.2, not on ten simultaneous launches.

The deal is the same for all ten on everything except the invoice:

- **Six paying showcase groups:** 20% off core for 12 months from go-live, setup waived, list price from month 13. In exchange: logo rights, a written case study, one reference call per quarter, and product feedback access.
- **Four design partners:** no subscription for 12 months, setup waived, same logo and case-study rights, list price from month 13. They are product-development customers, not discounts.
- **Nothing else is discounted.** No per-location rate below the showcase rate, no permanent “founding customer” pricing, no free service beyond the terms above.

**Can the sales and build timeline carry six live by June?** The arithmetic says yes, with two conditions. The workload is the binding constraint, not cash:

| Constraint | Requirement | Capacity | Verdict |
|---|---|---|---|
| Build | 8–12 weeks of focused work from 4 January | 10 weeks puts it at mid-March | Tight but feasible. If it slips past 31 March, the June-go-live case applies (§10.7) |
| First go-live | S1 signed and onboarded by late April | Signed as a pre-build design partner in Feb–Mar; live 3–4 weeks after build | Requires selling on the demo before the product ships. This is the condition most likely to fail |
| Sales | 6 signatures by end-May at a 1-in-4 close | ~24 qualified conversations by end-April, ~6/week from January | Feasible with the founders’ network; the 40-conversation list must exist by week two |
| Onboarding | 168 hours in Q2 (6 groups × 28 hours) | ~13 hours/week each across two founders | Feasible part-time; Q2 is the peak quarter |
| Founder hours | Build 400h + selling 270h + onboarding 420h + support 60h + admin 260h = 1,410h | ~13.6h/week each average; peak **17.6h/week** for the build lead in Q1 (20.3h at a 12-week build; 26.8h if one founder builds alone) | **The real constraint.** Q1 leaves 12% of a 20-hour part-time week as slack; the 16-hour claim is withdrawn (§10.1b) |

The phasing is therefore kept, not reverted. But it is conditional on a 15 March checkpoint: if S1 is not signed by then, the first go-live moves to June and the plan enters the timing case in §10.7, which breaches the $5,000 floor in May. That is the trigger for the delay protocol — freeze travel and demos, move Toast certification — not a reason to hope.

**What the cohort costs.** The showcase program is the marketing budget, and it is much larger than the $2,000 brand line in §10. At list price, the ten groups would have paid about **$40,700** in 2027:

| Foregone revenue | Arithmetic | Amount |
|---|---|---|
| Showcase discount (6 groups) | 658 location-months × $11.80 (20% of $59) | $7,764 |
| Setup waived (10 groups) | 10 × $1,500 | $15,000 |
| Design partners free (4 groups) | 294 location-months × $61 | $17,934 |
| **Total** | | **$40,698** |

Judge the program on whether the case studies and logos produce more than $40,700 of pipeline. If they do not, the next cohort should be three paying groups, not ten.

These groups are the sales force — restaurant operators buy what peer operators show them. Target pipeline math: at a realistic 1-in-4 close rate on qualified conversations, 10 signatures require ~40 serious group conversations starting January 2027. Build that list in Q1 (Toast-heavy regional groups, franchise expos, operator communities, warm intros through the founders’ restaurant networks — including the Afro Deli franchise system the founding team already operates in).

Phase 2 — Proof to pipeline (H2 2027). Publish the showcase results (menu-error reduction, update time saved, before/after brand screenshots). Convert the showcase and design-partner groups to list price at month 13; the first conversions land April–October 2028. Run certification alpha/beta inside the showcase base.

Phase 2b — Agency and reseller channel (from month ~2). Web-design agencies serving restaurants are the highest-leverage channel available: they get asked “can you also update our menu?” constantly, they hate doing it, and they can white-label Garnsh. Offer ~25% recurring revenue share. Twenty active agency partners beat 2,000 organic visitors. POS resellers and state restaurant associations are slower but similarly CAC-efficient (customer acquisition cost). Explicitly not doing: paid search ads (CAC exceeds lifetime value at these price points), cold outbound at scale, trade-show booths.

Phase 3 — Marketplace and ordering (2028). Partner Connect listing becomes a distribution channel Toast itself surfaces to its 189,000 locations. Gen 2 ordering launches to the installed base first (land-and-expand: publishing customers buy ordering at a far higher rate than cold prospects).

Phase 4 — Enterprise (2029). 25+ location groups, branded apps, annual enterprise contracts, presence at the industry shows where those groups buy (National Restaurant Association Show, MURTEC, franchise conventions).

Sales motion, all phases: the deal is won on a live pilot on two locations — a 20-minute demo with the operator’s own menu, a 30-day pilot, then conversion on annual terms. Keep the cycle to 21–30 days; if it runs longer, the account is too big for the current product.

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

A per-location LTV divided by a per-group CAC would be a category error: a group is 14 locations, so its monthly gross profit is 14× the per-location figure while its CAC is paid once. The CAC inputs also did not reconcile: 18 hours at $55 plus $600 is $1,590, not $1,200.

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

**The real peak is 17.6 h/week** for the build lead in Q1 — 88% of a 20-hour part-time week, with no slack for slippage. At the high end of the build estimate (12 weeks, 480 hours) the Q1 peak is 20.3 h/week, at the ceiling. And if one founder owns the build alone — which is what “product/engineering” as a single function in §12 implies — that founder carries 26.8 h/week in Q1, which is full-time, not part-time. The plan must say which it is: a 10-week, two-founder build at ~18 h/week each, or a 10-week full-time build lead. It cannot claim both the 16-hour peak and a June go-live.

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
2. **The trough is caused by front-loaded spend, not by a slow sales ramp.** Design ($5,000 across three milestone payments), legal ($2,500), insurance ($1,500) and brand work ($2,000) all land before the first invoice clears. That is why design is paid in three milestone installments and why the $3,000 Toast certification is a Q3 event. Each of those choices holds the April floor above $5,000.
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

## 11. Timeline and milestones

| When | Milestone |
|---|---|
| Jan 2027, week 1 | Toast partner application submitted. Entity formed; $20,000 paid in; operating agreement, vesting, and IP assignment signed before the money moves (§15) |
| Jan–Mar 2027 | Finalize product vision, this business plan, pitch deck, and pricing; publish pricing publicly in month 1; build the 40-group target list; ship the CSV/Sheets import bridge; WCAG and price-accuracy terms specced before the first customer |
| 15 Mar 2027 | Checkpoint: first showcase group signed as a pre-build design partner. If not, the June-go-live case and the delay protocol apply (§9, §10.7) |
| Mar–Jun 2027 | Sign 10 showcase groups (Gen 1.0 live: custom menus, order-ready boards, location picker). Six live and paying by June (about 84 locations); the four design partners live by September (§9) |
| ~May 2027 (day 120) | Go/no-go gate: Toast partner approval in hand or clearly in process — otherwise redirect to multi-POS + import path or stop (§7, §14) |
| May–Nov 2027 | Cash gates: revenue covers costs from May; capital fully recovered by November (§10.2). If cash falls below $5,000 before recurring revenue passes $3,000/month, stop and sell |
| H2 2027 | Case studies published; 5 additional full-price groups (15 groups / 210 locations / 154 paying by December); partner certification alpha/beta; agency channel producing its first groups |
| Oct–Dec 2027 | Multi-unit sales push: 2–3 groups at 10+ locations on annual terms — this is what proves the actual thesis |
| 2028 | Gen 2.0 — custom online ordering launches (gated on Toast ordering-partner certification); Partner Connect listing live; second POS adapter (Square) by ~month 18. Base case: 644 locations, $459K revenue, $740K exit ARR. Engineer hired at $35K MRR, growth hire at $50K MRR (§10.3) |
| 2029 | Gen 3.0 — custom branded mobile app and e-commerce; enterprise push at 25+ location groups. Base case: 1,288 locations, $1.35M revenue, $1.79M exit ARR, $508K operating result (§10.4). Decision point: raise to accelerate, or run as a profitable business |



## 12. Team and operations

Two founding partners (names and role split to be completed in the operating agreement — the plan deliberately does not assume them). The work splits into four functions that must each have a named owner from day one: product/engineering, Toast integration and certification, sales/operator relationships, and onboarding/support. With two people, each owns two — write down which, because “we both do sales” means nobody does support during a Friday dinner rush when a board goes wrong.

Operating posture: remote-first, asynchronous, built to be run from anywhere — including across time zones — with support coverage matched to US restaurant service hours (lunch and dinner peaks, Eastern through Pacific). Support trigger: at roughly 150 live locations, support becomes a founder’s whole day — budget a part-time support contractor (~$2,500/mo) from that point, funded from revenue.

Metrics that matter (monthly): locations live · net new locations · revenue per location · group logo churn · gross margin per location · CAC by channel · onboarding hours per location · publish success rate · last-known-good activations (a leading indicator of upstream fragility) · support tickets per 100 locations.

## 13. Risks and mitigations

Toast denies partner access (fatal if unmanaged). No partner status means no clean, stable menu feed at scale, and workarounds (scraping the Toast admin, weekly CSV exports) are fragile and likely a terms-of-service problem. Mitigation: apply in week one; day-120 go/no-go gate (§7); POS-agnostic architecture; the import bridge keeps early revenue possible without betting the company on the gate.

Marketplace economics. If a ~30%-style revenue share applies, margin compresses materially. Mitigation: get the actual terms before scaling; price for the share from day one; keep the direct-sold mix above 50% of revenue.

Toast ships it natively. Toast already bundles websites and ordering and sells Delphi boards; a free “brand kit + menu publishing” release would compress Garnsh’s pricing. Mitigation: win on publishing discipline and multi-surface reach; be multi-POS by month ~18; own channels Toast doesn’t control (operator-language search, agencies).

Certification timeline slips. Gen 2 revenue depends on a process Toast controls. Mitigation: Gen 1 must be a real business on its own (it is, at ~70 locations); never pre-sell ordering dates to customers.

Group churn is lumpy. Losing one 40-location group is losing 40 locations in a day. Mitigation: annual contracts at 10+ locations, quarterly business reviews, and a hard rule that no single group exceeds 15% of revenue by 2028.

Liability for what Garnsh renders. A wrong price or an allergen claim on a published menu is a legal exposure, not a typo. Mitigation: contract makes Toast the system of record; every surface shows an “as of” freshness timestamp; Garnsh never renders nutrition or allergen claims; tech E&O insurance from month one.

Accessibility (ADA/WCAG) exposure. Public menu pages are exactly the kind of surface plaintiffs’ firms scan. Mitigation: WCAG 2.1 AA as a ship gate for all four surfaces, plus a published accessibility statement.

Sales cycle length. Restaurant groups buy slowly and seasonally (nobody signs during December or during an opening). Mitigation: the 40-conversation pipeline math in §9, the two-location pilot motion, and showcase pricing that removes the budget objection for the first cohort.

Thin capitalization. $20,000 leaves no room for a paid engineer, a SOC 2 audit if a big group demands one, or a legal fight. Mitigation: the monthly cash model and the $5,000 floor protect a certification reserve; the delay protocol in §10.7 is the buffer, and it only works if it is pulled in April. Gen 2/enterprise security requirements are scoped only after revenue exists to fund them.

Founder concentration. Two people, one of whom likely holds the whole codebase. Mitigation: contract designer early, document everything, no single-person deployment path.

## 14. Kill criteria

Decided in advance, in writing, so the decision is not made emotionally at month nine:

No Toast partner approval (or clear in-process path) by day 120 → pivot all effort to the multi-POS + agency-channel path, or stop.

Fewer than 4 of the 10 showcase groups signed, or fewer than 3 live and paying, by day 180 (end June 2027, when the plan has 6 live and 84 paying locations) → the ICP, the price or the sales motion is wrong. Do not add features; re-interview the 20 people who said no.

Multi-unit logo churn above 3% per month once past 25 multi-unit locations → the product is not embedded in their workflow. Stop marketing spend and fix onboarding.

CAC payback above 18 months on any channel after $5,000 spent on it → kill that channel, permanently.

Fully loaded gross margin, including onboarding labour at $60/hour even when founders do it unpaid, below 75% at 100 live locations for two consecutive months → unit economics are broken; re-price or automate onboarding before growing. The arithmetic: 100 locations × $61 × 12 = $73,200 of annual revenue. At 2h/location, onboarding is $12,000; COGS (infra $2,040 + payments $2,123 + onboarding $12,000) is $16,163; GM is 77.9%. At 4h/location, onboarding is $24,000, COGS is $28,163, and GM is 61.5% — below the line.

Cash below $5,000 before recurring revenue passes $3,000/month → stop. Not "cut back" — stop building, stop spending, and sell what exists (§10.2). The model's floor is $5,923 — $923 of headroom. A two-month slip takes it to $3,273; the 15 March protocol raises the trough to $5,673, only $673 above the floor, and capital is recovered in November. A plan that needs luck to clear its own floor is not a plan.

## 15. Founder decisions and the partnership checklist

### Decisions still needed

Partner names, equity split, and who owns which of the four functions in §12.

Entity type and state of formation (the notes say “legalize through partner” — clarify what that means: whose name, which state). Recommendation from the review draft, adopted as the default: an LLC taxed as a partnership at this scale — cheap, flexible, no double taxation; elect S-corp treatment later when there is profit worth optimizing, or convert to a Delaware C-corp if outside capital is ever raised.

Confirm the Mar–Jun 2027 signing window is realistic against whoever is building Gen 1, and accept the 15 March checkpoint in §11: if the first group is not signed by then, the plan runs the June-go-live case.

Validate §8 pricing with at least ten operators, using the companion interview script and the triggers in §8, before the pitch deck locks it in.

Confirm the Toast strategy in §7 explicitly: application in week one, day-120 gate, in parallel with showcase sales.

Decide the growth-direction question in §4 (up to 25+ groups vs. down to 3–9 + multi-POS first) — scheduled for the H2 2027 review, with data.

Confirm whether the current demo site’s scope (publishing only, no ordering) is the official Gen 1 promise to customers. The notes’ Gen 1 list and the site agree — keep them that way.

### Before the $10,000 moves (checklist)

A 50/50 two-person company funded with $10,000 each is the most common structure in software and the most common structure to fail. All of the following are cheap in January 2027 and unaffordable later:

Operating agreement, signed — decision rights (who owns product, who owns sales), expense policy, and a deadlock clause (mediation, then buy-sell). A deadlock clause is not pessimism; it is the difference between a resolved disagreement and a dissolved company.

Vesting, even for founders — four-year vest, one-year cliff, applied to both partners. Without it, a partner who leaves in month four keeps half the company forever.

IP assignment from both partners to the entity — critical and routinely missed. Any code, design, or copy written before the entity existed belongs personally to whoever wrote it unless assigned. The current demo and site need an explicit assignment.

Buy-sell / right of first refusal with a valuation formula agreed while everyone is friendly.

Trademark — search and file “Garnsh” (USPTO, roughly $250–$350 per class; classes 9 and 42) before spending further on brand assets.

Separate books from day one — business bank account, accounting software, no commingling. It matters at tax time and in any future diligence.

Insurance in month one — tech errors-and-omissions + cyber (~$1,500–$3,000/yr at this stage).

Contractor agreements with IP assignment for any designer or engineer who touches the product.

## Sources and verification notes

Toast Q3 2026 results (Toast investor relations / Business Wire, Nov 3, 2026): ~189,000 total locations (+21% YoY), ARR $2.5B, ~8,500 net new locations in the quarter.

Toast partner program structure (Toast developer documentation and 2026 partner-API reporting): closed ecosystem, ~eight-stage process (application → vetting → agreement → sandbox build → certification → alpha at 1 location → beta at 3–5 locations → Partner Connect listing); partner fees unpublished; ~30% ordering revenue share is from 2019 reporting and is not treated as current.

Toast standard API access (Toast developer guide, 2026): read-only, per-restaurant credentials included with Restaurant Management Suite Essentials for US customers.

Toast menu-to-website access (verified Nov 7, 2026): Toast’s own support documentation shows the website menu channel is “Websites View-Only” — the menu displays on a Toast Website only, view only, not orderable — and that Toast Online Ordering and Toast Local menus cannot differ. Third-party 2026 guides confirm the Menus API’s production credentials are issued only to accepted partner-program vendors (“Anyone can read the docs. Almost no one can call the API”), and that standard API access is GET-only, per-location, Menus V2, and positioned for reporting rather than ordering or website publishing. A WordPress Toast-menu plugin’s own FAQ confirms even it requires the account to have Partner API access enabled, arranged through a Toast representative.

Competitor pricing: published-price roundups, October 2026 (ChowNow $229–$449/mo + setup; Popmenu $159–$499/mo; Owner.com $249/mo + 5% or $499 flat; Lunchbox enterprise ~$300–$499/mo per location per product; BentoBox pricing unpublished and Clover-only as of 2026). Popmenu setup (~$1,300) and UpMenu ranges cited in the review draft are reported, not published, and are not used in this plan’s tables.

US restaurant counts: industry reporting citing 700,000+ US eating and drinking establishments (2024–2026).

Product scope, roadmap, timeline, capitalization, and target market: founders’ plan v1 (working notes shared November 7, 2026) and garnsh.vercel.app as read the same day.

Independent review draft (“v1.1,” November 7, 2026): source of the day-120 gate, kill criteria, partnership checklist, conservative financial case, agency-channel and showcase-payment amendments, and the alternative pricing ladder and growth-direction argument — each adopted, adapted, or explicitly deferred where noted in the text.

# Garnsh — Business Plan

**The menu publishing layer for Toast restaurants.**
Prepared for Kofi · 7 November 2026 · v1.1 — incorporates the founders' January 2027 timeline and the Generation 1.0 / 2.0 / 3.0 roadmap

---

## 1. Executive summary

Garnsh is a publishing layer that sits on top of a restaurant's Toast POS. The operator keeps running the menu in Toast — the single source of truth — and Garnsh renders that menu correctly on every guest-facing surface: a hosted menu page per location, an embed for the existing website, a QR view, and a designed digital menu board. It adds the things a POS was never built to do: preview before publish, version history, rollback, per-location mapping, and a last-known-good fallback when the upstream feed breaks.

**The wedge is not "menus." It is menu *release discipline*.** Every surface a guest sees is someone's draft that got shipped by accident. Garnsh treats a menu the way engineering treats a deploy: draft → preview → publish → rollback, with an audit trail.

**The strategic call in this plan: do not sell to single-location independents.** That market is owned by Owner.com and Popmenu at $249–$500/month with ordering, marketing and websites bundled — you cannot win a feature fight against a bundle, and a $39/month independent churns 40%+ a year. Garnsh's real customer is the **multi-unit Toast operator (3–200 locations)**, where the menu-per-location problem is acute, the buying process is rational, churn is 3–4x lower, and the same product sells for 3–6x the price.

**Bottom line:** this is a real, profitable, defensible niche business — roughly **$35–70M of addressable spend inside the Toast base alone** — not a venture-scale outcome on its own. Base case is ~$670K ARR by year three at ~70%+ EBITDA margins on a bootstrap budget. The venture version requires expanding off Toast to Square/Clover/Lightspeed and selling to 20+ location groups; that path supports a $250K raise and a $3–6M ARR outcome. Both are worth doing; only one is worth raising money for.

**The single biggest risk is not competition — it is Toast itself**: API access, marketplace economics, and Toast shipping this natively. Section 8 treats that as the critical path, not a footnote.

---

## 2. The problem

A restaurant's menu exists in five or six places at once, and they disagree.

- The POS has the *real* menu — items, prices, modifiers, availability.
- The website has a PDF or a hand-built page that was accurate in March.
- The QR code points at a third copy, often a Google Drive file.
- The in-store screens run off a USB stick or a vendor CMS that only the owner knows how to log into.
- Delivery marketplaces and Google/Yelp each hold their own version.
- Multi-location groups have all of the above, multiplied, with different prices per location — airport, stadium, and flagship pricing on the same item.

The cost of this is not aesthetic. It is:

1. **Price mismatch at the table.** Guest sees $16 on the QR code, is charged $18. That is a service recovery, a comp, a bad review, and in some jurisdictions a consumer-protection exposure.
2. **Labor cost of manual sync.** Someone — usually the GM — retypes the menu into Canva and a website builder every time a price changes. In a 6-location group that is hours per month, done badly.
3. **Menu drift after turnover.** The person who knew how to update the PDF quit. Now nobody does.
4. **Broken screens during service.** Upstream tool fails, board goes blank, guests stare at a black rectangle at the counter.
5. **Lost discovery.** PDFs and image menus are poorly parsed by search and AI answer engines. As guests increasingly ask an assistant "what's on the menu at X," a machine-readable, current menu page becomes a discovery asset.

Existing tools solve adjacent problems. Website builders solve the site, not the menu. Menu-sync tools (Marqii and similar) push menus *out* to Google/Yelp/Apple — a distribution problem, not a rendering problem. Digital signage vendors sell screens and a CMS. Nobody sells the operator a clean, reliable, per-location *publishing* pipeline that treats the POS as source of truth and everything else as a build target.

---

## 3. Product

### What Garnsh does

| Surface | What it is | Who it is for |
|---|---|---|
| **Hosted page** | A public menu page per location, server-rendered, phone-first, branded | Fast setup; the default landing surface |
| **Website embed** | An iframe/JS embed that drops the same menu into the operator's existing site | Restaurants with a site they like and don't want to rebuild |
| **QR menu** | A phone view opened from a printed code, one per location | Tables, patios, counters |
| **Menu board** | A designed display for in-store screens, 16:9 and 3-panel landscape | Lines and counters; replaces the USB stick |

### The features that actually differentiate

- **Preview → publish → rollback.** Draft v15 is never visible to guests while v14 is live. Every published version is retained. This is the feature nobody in restaurant tech has, and it is the entire pitch to an operator who has been burned.
- **Last-known-good fallback.** If the upstream feed is unavailable, public surfaces keep serving the most recent version that published correctly. No blank boards, no error pages at the table.
- **Location mapping.** Each surface is bound to one location's menu context, so the airport price never appears on the flagship board. This is the multi-unit unlock.
- **Freshness readout.** "Source last read 6 minutes ago" — an honest operational signal, not a fake "real-time" claim.
- **Brand at the center.** Typography, color, logo per brand, with per-location overrides.

### What Garnsh deliberately is not

No cart, no checkout, no payments, no ordering, no delivery, no 86/stock status, no promise of real-time sync. This is a strategic choice, not a limitation:

- It keeps Garnsh **out of Toast's revenue path** — the single most dangerous place for a dependent partner to stand.
- It keeps the company **out of PCI scope** entirely.
- It makes the product **easy to say yes to** — it does not threaten the operator's existing ordering vendor.
- It focuses the engineering effort on the thing that is genuinely hard: correct, versioned, per-location rendering.

### Generation roadmap — assessed

The founders' roadmap sequences the product across three generations. Gen 1.0 is correct and should consume all of 2027. Gen 2.0 is where the company's risk concentrates.

| Generation | Year | Founders' scope | Recommendation |
|---|---|---|---|
| **Gen 1.0** | 2027 | Custom menus, order-ready menu boards, location picker | **Ship as scoped.** This is the entire company for 18 months. Do not add surfaces. |
| **Gen 2.0** | 2028 | Custom online ordering | **Build a branded ordering front-end that hands off to Toast Online Ordering — not your own cart and checkout.** See below. |
| **Gen 3.0** | 2029 | Branded mobile app, custom e-commerce | **Keep as vision, not as plan.** Fund from revenue. Restaurant-branded apps have collapsing install rates below ~25 locations. |

**Why Gen 2.0 must not be "your own online ordering" by default:**

1. **It puts you in direct competition with your own platform.** Toast Online Ordering is one of Toast's core products and a major payments-adjacent revenue line. A partner that intercepts those orders is the first partner Toast restricts. Certification is discretionary and revocable.
2. **It changes the company's regulatory identity.** Owning checkout means PCI DSS scope, chargeback and refund handling, sales-tax and tip-compliance logic, gift cards, and a support model measured in minutes not hours. That is a different company with different insurance and a different hiring plan.
3. **It changes the competitive set completely.** You go from competing with website builders to competing with Owner.com (venture-funded, $249/mo + 5% of orders), Olo, Chowly, Lunchbox and Toast itself.

The middle path gets ~80% of the value at ~20% of the risk: **a branded ordering experience that submits into the operator's existing Toast Online Ordering.** The guest sees the restaurant's brand and domain; Toast still processes the order and the payment; Garnsh never touches a card. That is a product Toast can tolerate — arguably one it wants, because it makes their ordering look better — and it preserves the partner relationship you cannot operate without.

Revisit owning checkout in 2029, and only if there is a signed partnership that makes it safe.

### Honest product debt

The current build is a strong demo with real interaction design (three sample restaurants, four surfaces, publish/rollback simulation). To be sellable it needs: a real ingestion path (see §8), tenant auth and isolation, per-location asset management, an upload pipeline for logos/fonts, board scheduling, and an accessibility pass to WCAG 2.1 AA. That is roughly 8–12 weeks of focused work, not a weekend.

---

## 4. Market

### Bottom-up sizing

Toast reported approximately **189,000 locations** at Q3 2026, up 21% year over year, adding ~8,500 net locations per quarter. That is the beachhead, and it is growing faster than the restaurant industry.

| Layer | Estimate | Basis |
|---|---|---|
| Toast locations (global) | ~189,000 | Toast Q3 2026 disclosure |
| US share of Toast base | ~150,000 (est.) | Toast is US-weighted; treat as estimate |
| Locations that plausibly need a public menu surface | ~120,000 (est.) | Most, but not all, have a web presence |
| Multi-unit groups, 3+ locations | ~35,000–50,000 locations (est.) | ~25% of the base |
| **Founders' target: groups with 10+ locations** | **~15,000–23,000 locations (est.)** | ~8–12% of the base |
| Blended price per location per month | $45–$62 | See §6 |
| SAM — whole multi-unit segment (3+) | $19M–$37M ARR | 35–50k × $45–62 × 12 |
| **SAM — 10+ locations only (founders' focus)** | **$8M–$17M ARR** | 15–23k × $45–62 × 12 |
| TAM if single-unit independents included | $65M–$90M ARR | Whole Toast base, lower ARPU |
| **Expansion TAM: all POS platforms** | **$250M–$400M ARR (est.)** | Square, Clover, Lightspeed, SpotOn add roughly 3–4x the location count |

**Note on the 10+ focus:** concentrating on 10+ location groups is the right call for 2027 — longer contracts, real budgets, fewer support tickets per dollar. But understand what it costs: it roughly halves the addressable base versus targeting 3+. The stated evolution from 10+ to **25+** shrinks it further, and that is the wrong direction to grow. Growth comes from **more POS platforms** (Square, Clover, Lightspeed) and from **moving down into 3–9 location groups** once onboarding is self-serve — not from chasing bigger accounts, which brings enterprise CMS incumbents, 6–9 month cycles, and RFPs that a two-person company cannot service.

**Read this honestly:** the Toast-only opportunity is a genuine but small market. A 10% share of the multi-unit segment is ~$3M ARR — an excellent business for a small team, a disappointing one for a VC. The expansion to other POS platforms is what turns it into a venture story, and that is a year-two decision, not a year-one one.

### Why now

- **Menu data is becoming a discovery asset.** AI answer engines and Google's summaries reward current, structured, machine-readable menu pages. A PDF is invisible to them.
- **Digital signage hardware got cheap.** A 43" commercial display is a few hundred dollars; the bottleneck is software and content, not hardware.
- **Restaurant labor turnover** makes "the person who knew how to update it" a recurring failure mode — which makes a self-serve, guarded publishing pipeline more valuable every year.
- **Toast's installed base compounds at ~8,500 locations a quarter.** Every quarter the addressable base grows without Garnsh spending a dollar.
- **Consolidation in restaurant marketing** (website builders bundling more, POS platforms bundling more) means the window for a focused, independent layer is open now and may not stay open.

---

## 5. Customers and segmentation

### Primary ICP: the multi-unit operator, 3–200 locations

- **Who:** franchisee groups, local chains, hospitality groups with 4–40 units, airport/stadium concessionaires with per-location pricing.
- **Where they feel pain:** per-location price differences, brand consistency, every new opening requiring a manual site build, boards that break during service.
- **Who signs:** Director of Operations, Marketing Manager, or the owner-operator in smaller groups. Not IT.
- **Budget:** they already pay for a website, a signage tool, and someone's time. $45–$70 per location per month is inside existing line items.
- **Why they churn less:** switching means re-mapping every location; the product becomes part of opening procedures. Expect 1–1.5% monthly logo churn versus 4%+ for independents.

### Secondary ICP: the single-location independent with screens

Only worth serving **product-led** — self-serve signup, no sales calls, no onboarding calls. At $39/month with 4% monthly churn, the LTV supports roughly a $250 CAC. That means SEO and the Toast marketplace only; never paid acquisition, never outbound.

### Deliberately excluded

- **Enterprise chains (500+ locations).** Long sales cycles, RFP processes, custom integrations, and they already have internal menu systems or an enterprise CMS. Revisit at $2M ARR, not before.
- **Restaurants without a POS-managed menu.** Garbage in, garbage out.
- **Ghost kitchens and delivery-only brands** with no guest-facing surface.

---

## 6. Pricing and packaging

| Plan | Price | Includes |
|---|---|---|
| **Solo** | $39/mo per location | Hosted page, embed, QR, 1 board screen |
| **Growth** | $69/mo per location | Everything in Solo, unlimited board screens, custom domain, brand kit |
| **Multi** | $45/mo per location, min. 3 locations ($135/mo floor) | Everything in Growth, location mapping, shared brand kit, per-location overrides |
| **Group** | $35/mo per location, annual contract, 26+ locations | Everything in Multi, onboarding, priority support, invoicing |
| **Setup** | $199 one-time (waived on annual) | Brand import, first location live, QR assets |

**Pricing logic.** The reference points are: UpMenu at $49–$169 per location for menu modules, Popmenu at a reported ~$500/month plus ~$1,300 setup, Owner.com at $249–$499/month. Garnsh must sit clearly *below* the bundled website+ordering players so it reads as an obvious add-on rather than a replacement, and clearly *above* a $17/month commodity menu builder so it doesn't read as a toy. $39–$69 per location threads that needle.

**Two pricing rules to hold:**

1. **Never discount the per-location price.** Discount implementation (waive setup, extra months) instead. Per-location price is the entire revenue model.
2. **Charge per location, not per surface.** Surface-count pricing invites the operator to turn things off. Location pricing aligns with how they think about their business and grows automatically when they open a new unit.

**Expansion revenue** (year two, only after the core is stable): $5/screen/month beyond the included allowance for groups running 6+ screens; a $19/month "menu analytics" add-on (which surfaces get scanned, which items get viewed); a $99/month per-brand custom design service.

---

## 7. Unit economics

Assumptions: blended ARPU $52/location/month, gross margin 88% (below SaaS-typical 90% because of per-location rendering, image CDN, and support), multi-unit logo churn 1.2%/month, single-unit 4.0%/month.

| Metric | Multi-unit | Single-unit |
|---|---|---|
| ARPU/month | $52 | $39 |
| Gross margin | 88% | 88% |
| Direct cost per location/month | ~$2.10 (hosting, CDN, image processing) | ~$1.60 |
| Support cost per location/month | ~$4.20 (amortized) | ~$2.80 |
| Monthly logo churn | 1.2% | 4.0% |
| Average lifetime | ~83 months | ~25 months |
| **LTV** | **~$3,800** | **~$860** |
| Target CAC | $600–$900 | $200–$280 |
| **LTV:CAC** | **4.2–6.3x** | **3.1–4.3x** |
| CAC payback | 13–20 months | 6–8 months |

**The tension to plan around:** multi-unit accounts have a slower payback (sales cycle plus onboarding) but 4.4x the LTV and a far more durable revenue base. Single-unit accounts pay back fast but bleed. The correct strategy is a **product-led single-unit funnel feeding a sales-assisted multi-unit pipeline** — the same product, two motions, and the multi-unit motion is where the company's value actually accrues.

**Gross margin risk:** onboarding is the hidden cost. Budget 2–4 hours of human time per location in year one. At $52/month, a 4-hour onboarding is a 4–6 month payback before gross profit — which is why setup fees should not be discounted casually, and why self-serve onboarding must become good by year two.

---

## 8. The Toast dependency (critical path)

This section is the plan's most important. Everything else is executable; this is the thing that can end the company.

### The situation

- Toast's **Menus API** exists and returns a fully resolved menu for a location. It is available to **Partner integrations**, **Custom integrations**, and **Standard API access**.
- **Partner** status requires a formal application, vetting, and an eight-stage process ending in certification, with approval from Toast legal, compliance, privacy and security. Toast explicitly states it cannot integrate with all applicants.
- **Fees are not published.** Reporting from 2019 indicated a ~30% revenue share; current terms are unknown. Rate limit is documented at 20 requests/second.
- **Custom integrations** serve a single merchant and are not a route to a product.

### The risk, stated plainly

1. **Application rejection.** No partner status means no clean, stable menu feed at scale — and any workaround (screen-scraping the Toast admin, asking customers to export CSVs weekly) is fragile, high-effort, and likely a terms-of-service problem. A business built on a workaround is not investable and is one enforcement action from zero.
2. **Marketplace economics.** If a 30%-style revenue share applies, a $52 ARPU becomes ~$36 and the multi-unit CAC payback stretches past 24 months. That changes the pricing, not the viability — but it must be known before scaling.
3. **Toast ships it natively.** Toast already sells **Delphi digital menu boards** and has every incentive to bundle hosted menus into its marketing suite. When a platform owner moves into your feature, the independent vendor's only defenses are (a) being multi-surface and multi-POS, (b) being genuinely better at the operator's workflow, and (c) owning distribution outside the marketplace.

### Mitigations — do these in this order

1. **Apply for Toast partner status in week one.** It is the longest-lead item in the company. Apply before the product is finished; the application is about business case, not code.
2. **Build a POS-agnostic ingestion layer from day one.** The internal model should be "menu document in, surfaces out." Toast is an adapter, not the architecture. This costs a week now and saves the company later.
3. **Ship a non-API path for early customers**: CSV/Google Sheets import and a manual editor. Not because it is the future, but because it lets you take money before partner approval lands — and it proves willingness-to-pay without betting the company on a gate you don't control.
4. **Get to 3+ POS platforms by month 18** (Square, then Clover). This is the actual strategic hedge and the thing that converts this from a Toast feature into a company.
5. **Own a channel Toast doesn't control.** SEO on the operator's own problem language ("toast menu on our website," "digital menu board for toast"), plus web-design agencies who serve restaurants. If the marketplace closes, the business survives.

**Go/no-go gate:** if partner approval has not landed by **day 120**, redirect all effort to the multi-POS + agency-channel path or stop. Do not spend a year building a Toast-dependent company without Toast's blessing.

---

## 9. Competition

| Player | What they do | Price | How Garnsh differs |
|---|---|---|---|
| **Toast (native)** | POS, own marketing suite, Delphi digital menu boards | Bundled / hardware | Garnsh is brand-first, per-location, versioned, and works on screens the operator already owns. Toast's boards are Toast's hardware. |
| **Owner.com** | Website + ordering + marketing, AI-assisted | $249/mo + 5% of orders, or $499/mo flat | Doesn't publish to screens; requires the operator to move their site onto Owner. Garnsh layers on top of what exists. |
| **Popmenu** | Website + menu + marketing, restaurant-focused | ~$500/mo + ~$1,300 setup (reported, unpublished) | Same — it's a website replacement, sold with a long contract. Garnsh is cheap, narrow, and removable. |
| **Marqii** | Menu sync out to Google, Yelp, Apple, Facebook | Mid-market, unpublished | Distribution, not rendering. Natural partner, plausible acquirer. |
| **BentoBox / Squarespace** | Restaurant websites | Bundled | Site hosting, not a per-location publishing pipeline. |
| **UpMenu, MenuTiger and regional menu builders** | Menu pages + ordering modules | $17–$169/location | Weaker on versioning, rollback and multi-location mapping — but they are cheap and they are already there. |
| **Wallboard, 42 Digital Signage** | Digital signage with Toast integration | Signage-tier pricing | Screen-first, not menu-first. No hosted page or embed story. |

**Where Garnsh actually wins:** multi-location pricing integrity, the preview/publish/rollback workflow, last-known-good reliability, and the fact that it does not require the operator to change their website, their POS, or their ordering vendor.

**Where Garnsh actually loses:** anyone who wants one vendor for everything, anyone who wants ordering, and anyone who will not pay for a second tool for a problem they have decided to live with.

**Moat assessment — be honest.** There is no technical moat here. This is a well-executed CRUD app with good design taste. The durable advantages available are: (1) **switching cost** once every location is mapped and opening procedures reference it; (2) **distribution** via marketplace listing plus SEO; (3) **brand/design quality** in a category where the incumbents look like 2014; (4) **the multi-POS adapter layer** once built. None of these are strong on day one. All of them compound. Plan accordingly: speed and distribution matter more than features.

---

## 10. Go-to-market

### Channel sequence

**Months 0–3 — design partners, not marketing.**
Sign 5–8 paying design partners, ideally 2–3 multi-unit groups, at a discount in exchange for weekly feedback and a case study. Do this through direct outreach to restaurant groups in one metro and through hospitality web-design agencies. Target: product that survives a real service day.

**Months 2–6 — agency and reseller channel.**
Web design agencies serving restaurants are the highest-leverage channel: they get asked "can you also update our menu?" constantly, they hate doing it, and they can white-label. Offer 25% recurring revenue share. Twenty active agency partners beats 2,000 organic visitors.

**Months 3–9 — SEO on the operator's language.**
The site's existing resource pages are the right instinct. Build 30–50 pieces targeting the exact queries operators type: "toast menu on website," "update menu on toast," "digital menu board for restaurant toast," "qr menu per location," "toast menu export." This is slow, cheap, and compounding — and it is the only channel that survives losing marketplace access.

**Months 6+ — Toast Integration Marketplace.**
Highest-intent, lowest-CAC channel available, once certified. Being listed is worth more than any ad budget at this price point.

**Continuous — POS resellers and restaurant associations.**
Resellers sell Toast all day and get asked adjacent questions. State restaurant associations run vendor programs and newsletters. Both are relationship-slow and CAC-efficient.

**Explicitly not doing:** paid Google Ads (CAC will exceed LTV at $39–$69 ARPU), cold outbound at scale (sales cost per location too high under 10 locations), trade show booths (cost per lead is brutal for a sub-$100 ACV), and channel partnerships with delivery marketplaces (misaligned incentives).

### Sales motion for multi-unit

The deal is won or lost on a **live pilot on two locations**. Process: 20-minute demo with the operator's own menu, not a demo restaurant → free 30-day pilot on 2 locations → convert at Multi pricing with annual terms. Keep the sales cycle to 21–30 days; if it runs longer, the account is too big for the current product.

### Positioning and message

> **Your team already runs the menu in Toast. Garnsh makes every guest-facing version match it — per location, with preview, rollback, and a menu that never goes dark.**

Three objections to pre-empt, every time:

- *"Can't my website guy do this?"* — Yes, once. Not every price change, not per location, and not with a rollback.
- *"Is this official Toast?"* — No, and that is disclosed plainly. It reads the menu, it never touches payments or orders.
- *"What if we switch POS?"* — The hosted pages, QR codes and boards keep working.

---

## 11. Operating plan

### Team

| Phase | Headcount | Notes |
|---|---|---|
| Months 0–6 | Founder (product + eng), contract designer | Design quality is a core differentiator; do not skimp on it |
| Months 6–18 | + part-time support/CS (contract, ~$2,500/mo) | At ~150 locations, support becomes the founder's whole day otherwise |
| Months 18–36 | + 1 engineer, + 1 growth/partnerships | Only after the multi-unit motion is proven |

### Milestones

**Days 1–90**
- Toast partner application submitted (day 5)
- POS-agnostic ingestion model + CSV/Sheets import shipped
- 3 paying design partners live on real menus
- WCAG 2.1 AA pass on all four surfaces
- Pricing page, docs, onboarding flow, terms of service, DPA

**Days 91–180**
- 10–15 paying locations; first multi-unit account signed
- 5 active agency partners
- 10 SEO pieces published; first organic signups
- Toast approval status resolved (go/no-go gate at day 120)

**Months 7–12**
- 40–60 locations live; 3+ multi-unit accounts
- Marketplace listing live (if approved)
- Self-serve onboarding under 20 minutes
- $30K+ ARR run-rate; gross margin measured, not assumed

**Year 2**
- 250–350 locations; $180K–$250K ARR
- Second POS adapter (Square) shipped
- First 20+ location group closed
- Support hire; founder out of day-to-day support

**Year 3**
- 800–1,000 locations; $600K–$700K ARR
- 3 POS platforms; agency channel producing 40%+ of new logos
- Decision point: raise to accelerate, or run as a profitable $700K-ARR business

### Metrics that matter (monthly)

Locations live · net new locations · ARPU · logo churn (split single vs multi) · gross margin per location · CAC by channel · onboarding hours per location · publish success rate · last-known-good activations (a leading indicator of upstream fragility) · support tickets per 100 locations.

---

## 12. Financial plan

### Base case

| | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Ending locations | 60 | 320 | 900 |
| Blended ARPU/location/mo | $48 | $56 | $62 |
| Exit ARR | $34.6K | $215K | $670K |
| Revenue recognized | $18K | $105K | $400K |
| Gross margin | 80% | 86% | 88% |
| Gross profit | $14K | $90K | $352K |
| People & contractors | $0 | $45K | $150K |
| Tools, infra, marketing | $6K | $18K | $48K |
| Legal, insurance, admin | $3K | $7K | $12K |
| **Operating result** | **+$5K** | **+$20K** | **+$142K** |
| Operating margin | 28% | 19% | 36% |

*Founder salary excluded in years 1–2; $90K assumed inside "people" from year 3.*

### Scenarios at year 3

| Scenario | Locations | ARR | Character |
|---|---|---|---|
| **Bear** | 150 | $81K | Side project. Something is wrong with channel or churn — stop and reassess. |
| **Base** | 900 | $670K | Profitable niche business, ~$140K/yr to the owner. Good outcome for bootstrapping. |
| **Bull** | 1,800 | $1.5M | Multi-POS + agency channel working. Now a fundable company. |
| **Venture** | 4,500+ | $3.5M+ | Requires $250K–$500K raised, 2 sales reps, and 4 POS platforms. Only attempt after base case is proven. |

### Capital requirement

**The founders' plan: $20,000 initial paid-in capital, two partners at $10,000 each, funded January 2027.** That is enough — narrowly — for Gen 1.0, and it is not close to enough for Gen 2.0. Plan the two separately.

| Use of the $20,000 | Amount |
|---|---|
| Entity formation, operating agreement, trademark filing | $1,500 |
| Tech E&O + cyber insurance, year one | $2,000 |
| Contract design (the core differentiator — do not cut this) | $6,000 |
| Infrastructure and tooling, 12 months | $3,600 |
| Toast partner application (no published fee at application stage) | $0 |
| Buffer | $6,900 |
| **Founder salaries** | **$0 — both partners work unpaid through 2027** |

**The rule that makes $20K work:** Gen 1.0 must be cash-positive by month 9 (i.e. by September 2027) or the capital is gone and the company is a hobby. That means revenue from paying customers by month 5–6, not "showcase" customers who pay nothing.

**What $20K does not fund:** Gen 2.0 ordering work ($150K–$400K), paid acquisition, a support hire, or a second engineer. Gen 2.0 is funded from revenue at ~$250K ARR or from a raise at proof — not from the initial capital.

- **Bootstrap path (recommended, and what $20K buys): $20K.** Covers infrastructure, legal, insurance, and a designer. The business is cash-generative from month 9–12 at this cost structure.
- **Accelerated path: $250K–$350K.** Two salespeople, one engineer, 18 months of runway, target $1.5M ARR in 24 months. Only raise after: 50+ locations live, churn measured under 2%, Toast status known, and one 20+ location group signed. Raising before those four facts exist is how this category eats founders.

---

## 13. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Toast denies partner access** | Medium | Fatal | Apply day 5; POS-agnostic architecture; non-API import path; day-120 go/no-go gate |
| **Toast ships this natively** | High (2–3 yrs) | Severe | Multi-POS by month 18; own SEO + agency channel; win the multi-location workflow where Toast is weak |
| **Marketplace revenue share compresses margin** | Medium | Moderate | Price for it from day one; keep direct-sold mix above 50% |
| **Restaurant SMB churn** (3–5%/mo industry norm) | High | Moderate | Weight the book toward multi-unit; annual contracts; setup fees |
| **Thin moat / fast copycat** | High | Moderate | Speed, design quality, distribution, and switching cost via location mapping |
| **Liability for a wrong price or allergen on a rendered menu** | Low–Medium | Severe | Contract makes Toast the system of record; show "as of" timestamps; never render nutrition or allergen claims; E&O insurance from month one |
| **ADA/WCAG exposure on public menu pages** | Medium | Moderate | WCAG 2.1 AA as a ship gate; accessibility statement; note that restaurant sites are heavily targeted by plaintiffs and courts have held operators cannot simply push liability onto their website vendor |
| **Founder concentration / solo build risk** | High | Severe | Contractor designer early; document everything; no single-person deployment path |
| **Data/security incident** | Low | Severe | Tenant isolation, least-privilege API scopes, SOC 2 readiness by year 2 if selling 20+ location groups (they will ask) |

**Legal and compliance baseline:** terms of service with a clear "POS is the system of record" clause and an indemnity carve-out for menu content accuracy; a data processing agreement; privacy policy; trademark non-affiliation disclaimer (already handled well on the site — keep it prominent, never imply Toast endorsement); business insurance including tech E&O and cyber ($1.5K–$3K/yr at this stage).

---

## 14. Kill criteria

Decide these in advance, in writing, so the decision is not made emotionally at month nine:

1. **No Toast partner approval by day 120** → pivot to multi-POS + agency channel, or stop.
2. **Fewer than 10 paying locations by day 180** → the ICP or the price is wrong. Do not add features; re-interview the 20 people who said no.
3. **Multi-unit logo churn above 3%/month after 25 multi-unit locations** → the product is not embedded in their workflow. Stop marketing spend and fix onboarding.
4. **CAC payback above 18 months on any channel after $5K spent** → kill that channel, permanently.
5. **Gross margin below 75% at 100 locations** → the unit economics are broken by support cost; re-price or automate onboarding before growing.

---

## 14b. Calendar plan — founders' timeline, with the gaps closed

The founders' document sets the shape. Three things are missing from it, and one is fatal if unaddressed.

| When | Founders' plan | Add this |
|---|---|---|
| **Jan 2027** | Form entity, $10K each in | **Toast partner application submitted in week 1** (8-stage certification, months of lead time — this is the longest pole and is absent from the timeline). Also: operating agreement signed *before* money moves (§17). |
| **Jan–Mar 2027** | Finalize vision, plan, pitch, pricing | **Publish pricing publicly in month 1.** Also spec WCAG 2.1 AA and the price-accuracy terms before the first customer, not after. |
| **Mar–Jun 2027** | 10 showcase customers | **Make at least 6 of the 10 paying** — even $50/month. A free showcase customer is a favour, not validation, and cannot be used to prove willingness-to-pay. Trade the discount for a public case study and a logo. |
| **Jul–Sep 2027** | *(unstated)* | **Cash-positive gate.** If not revenue-positive by September 2027, stop and reassess rather than spending the buffer. |
| **Oct–Dec 2027** | *(unstated)* | Multi-unit sales motion: 2–3 groups at 10+ locations on annual terms. This is what proves the actual thesis. |
| **Day-120 gate (May 2027)** | *(unstated)* | Toast partner approval status resolved, or pivot to multi-POS import path. |

The stated note "March–June 2026" is a typo for 2027 — worth fixing before this document goes to a partner or an advisor, because a timeline that appears to start in the past reads as unserious.

---

## 15. What I would do in the next 14 days

1. **Submit the Toast partner application.** Today. Everything downstream depends on it, and it is free to start.
2. **Talk to 10 multi-unit operators** (4–40 locations) and ask one question: "Walk me through what happens when you change a price." Do not pitch. Count how many describe a manual process involving Canva, a web person, or a spreadsheet. That number is the business.
3. **Talk to 5 restaurant web-design agencies** and ask what they charge for menu updates and whether they would resell. This validates the highest-leverage channel before a line of code is written.
4. **Ship the CSV/Sheets import path** so the first customer can pay you without Toast's blessing.
5. **Set the price and publish it.** $39 Solo / $69 Growth / $45-per-location Multi. Public pricing filters out the wrong customers and shortens every sales cycle.
6. **Write the WCAG and price-accuracy clauses into the terms** before the first invoice, not after the first complaint.

---

## 16. Verdict

Garnsh is solving a real, unglamorous, recurring problem with unusually good design instincts, in a market where the incumbents are either too big (Toast), too bundled (Owner.com, Popmenu), or solving a different problem (Marqii, signage vendors). The product as designed — preview, publish, rollback, last-known-good, per-location — is genuinely better than what multi-unit operators have today, and the site already communicates it more clearly than most seed-stage companies manage.

The honest constraints: the Toast-only market is ~$20–37M of addressable ARR, the moat is distribution and switching cost rather than technology, and the entire company sits downstream of a partner gate controlled by a publicly traded company that also sells a competing product.

**So the plan is: land 5 design partners on the strength of the product, win the multi-location segment on the strength of location mapping and release discipline, get the Toast relationship settled inside 120 days, and treat multi-POS expansion in year two as the thing that turns a $700K business into a $3M+ one.** Bootstrap it. It can be profitable by month twelve. Do not raise money until the four facts in §12 exist.

---

---

## 17. Partnership and entity checklist

A 50/50 two-person company funded with $10,000 each is the most common structure in software and the most common structure to fail. All of the following are cheap in January 2027 and unaffordable later.

**Before the $10,000 moves:**

1. **Operating agreement, signed.** 50/50 is fine, but it must specify decision rights (who owns product, who owns sales), the expense policy, and what happens when the two of you disagree. A deadlock clause with mediation followed by a buy-sell is not pessimism — it is the difference between a resolved disagreement and a dissolved company.
2. **Vesting, even for founders.** Four-year vest with a one-year cliff, applied to both partners' equity. Without it, a partner who leaves in month four keeps half the company forever.
3. **IP assignment from both partners to the entity.** Critical and routinely missed. Any code, design or copy written *before* the entity existed belongs personally to whoever wrote it unless assigned. The current demo and site need an explicit assignment.
4. **Buy-sell / right of first refusal** with a valuation formula agreed while everyone is friendly.
5. **Entity choice.** LLC taxed as a partnership is correct at $20K — cheap, flexible, no double taxation. Elect S-corp later when there is profit worth optimizing, or convert to a Delaware C-corp if you raise.
6. **Trademark.** Search and file "Garnsh" (USPTO, roughly $250–$350 per class; classes 9 and 42). Do it before spending on brand and domain assets.
7. **Separate books from day one.** Business bank account, accounting software, no commingling. It matters at tax time and it matters in any future diligence.

**Ongoing:** tech E&O and cyber insurance in month one; a written contractor agreement with IP assignment for the designer; and documented security practices, because a 20+ location group will ask for a security questionnaire and eventually SOC 2.

---

*Sources: Garnsh public site (product, positioning, disclaimers); Toast Q3 2026 results and investor materials (189,000 locations, +21% YoY, ~8,500 net adds); Toast developer documentation (Menus API availability, partner integration process, 20 req/sec limit); Toast support documentation (Delphi digital menu boards); Owner.com published pricing; reported Popmenu and UpMenu pricing; Marqii product pages; SaaS churn benchmarks for SMB segments; accessibility litigation commentary (Level Access). Market sizing figures marked "est." are this plan's own bottom-up estimates and should be re-derived before any external use.*

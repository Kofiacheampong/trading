# Garnsh — Change Log

**v3.0** · 11 November 2026 · From Business Plan v2.4 and 19-slide deck to v3.0 and 15-slide deck

## 1. What was removed

- **Length and repetition.** The plan was 29 pages and repeated the same problem, product boundary and pricing arguments in three or four places. The new plan is 15 pages of main body plus 3 pages of appendices.
- **Changelog language.** References to "the earlier draft," "v2.2," "the old 30% slower case" and "will replace this table" were removed. The plan now reads as a standalone document.
- **Per-location LTV divided by per-group CAC.** The 4.8x ratio was a category error. It has been replaced with a per-group LTV:CAC calculation.
- **Unverified real-time and 86 claims.** The plan no longer implies live stock, 86 status or real-time sync. Gen 1 is explicitly a publish-time system.
- **"10 showcase customers" framing.** The plan now says zero signed, zero live and zero paying. The 10 design partners are a target.
- **The 19-slide deck.** Replaced with 15 slides, each carrying one message.
- **The old "30% slower" sensitivity.** Replaced with explicit group-size, close-rate, churn, collection-lag and onboarding-funding cases.
- **The $20–40M market claim.** Replaced with a bottom-up $14–28M Gen 1 SAM.

## 2. What was rewritten

- **Executive summary.** Now states the stage, the zero-customer position, the 2027 economic loss and the capital constraint in the first two pages.
- **Problem and market.** Separates the operational problem from the Toast API wall and gives a transparent bottom-up market calculation.
- **Product.** Separates what exists (demo), what is planned (production build), what requires Toast approval (API, Gen 2) and what is out of scope (86, live stock, ordering).
- **Go-to-market.** Replaces the mixed 30-day pilot and 12-month design-partner language with two defined instruments and one coherent conversion path.
- **Pricing.** Corrects the setup-fee economics, adds the customer's all-in cost and sets pricing triggers relative to $59.
- **Technology.** Adds the four-way Toast status table and an objective day-120 gate.
- **Operations.** Rebuilds the founder-hours budget; the real peak is 17.6 hours/week, not 16.
- **Financial plan.** Rebuilt on a cohort model with churn, onboarding labor, cash collection timing and a downside.
- **Risks and milestones.** Now tied to specific gates and kill criteria.

## 3. What was added

- **Validation status.** A clear statement that Garnsh is pre-revenue, with 0 signed design partners, 0 live locations and 0 paying customers.
- **2027 onboarding finding.** The 2027 cohort needs 210 location-onboardings, or $25,200 at $60/hour. If the founders do it, cash works and the economic result is −$20.6K. If it is paid, the company runs out of cash.
- **Churn.** Group logo churn (1.5%/month) and location churn (0.5%/month) are modeled, with a 2.5%/1.0% downside.
- **Cash-flow reconciliation.** Subscription collection timing, setup-fee collection, accounts receivable and the $5,000 reserve are explicit.
- **Downside case.** 10-location groups, 1-in-6 close, 2.5% churn, 1.0% location churn and a 30-day collection lag.
- **Sensitivity analysis.** Group size, close rate, launch timing, churn, collection lag, onboarding funding, onboarding hours, price and Toast denial.
- **Assumptions and Evidence Register.** A separate 45-item register classifying claims as VERIFIED, MODELED or UNVERIFIED.
- **Deck v3.0.** 15 slides with a single argument per slide, including a validation slide that states the zero-customer position.

## 4. Financial assumptions that changed

| Item | v2.4 | v3.0 | Why |
|---|---|---|---|
| 2027 revenue | $44,377 | $42,195 | Churn reduces live locations to 193 and paying locations to 142 |
| 2027 cash from operations | +$6,463 | +$3,892 | Churn and setup-collection timing |
| 2027 economic result | +$6,463 | −$20,558 | $25,200 of imputed founder onboarding at $60/hour |
| 2027 year-end cash | $26,463 | $23,892 | Lower revenue and churn |
| 2027 trough | $5,923 | $5,923 | April remains the low point |
| 2028 revenue | $459,413 | $440,883 | Churn; 615 live locations vs 644 |
| 2028 operating result | $188,282 | $165,401 | Lower revenue, churn, onboarding |
| 2029 revenue | $1,349,045 | $1,287,970 | Churn; 1,183 live locations vs 1,288 |
| 2029 operating result | $507,711 | $435,027 | Lower revenue and gross adds |
| 2029 exit ARR | $1.79M | $1.63M | 1,183 locations × $115 |
| Net groups 2027/28/29 | 15 / 46 / 92 | 14.1 / 45.8 / 89.6 | Churn applied; gross adds calibrated |
| Setup fee at 14 locations | −$180 | −$180 | Arithmetic confirmed; break-even 1.79h/location |
| CAC | $1,200 | $1,590 | 18 hours × $55 + $600 = $1,590 |
| LTV:CAC | 4.8x (per location vs per group) | 38.4x (per group, 2% revenue churn) | Correct denominator |
| Gen 1 SAM | $20–40M | $14–28M | $61 Gen 1 ARPU, not $89 blended |

## 5. Inconsistencies corrected

1. **Setup fee.** The deck said it breaks even at two hours. At 14 locations and two hours, it loses $180. Break-even is 1.79 hours per location.
2. **CAC.** The old $1,200 did not match its own inputs. Corrected to $1,590.
3. **LTV:CAC.** The old 4.8x divided a per-location LTV by a per-group CAC. Corrected to 38.4x per group, with 13.0x in the downside.
4. **2027 onboarding.** The model omitted it. It is now $25,200 imputed; paid onboarding breaks the $5,000 floor.
5. **Churn.** The old model had no churn. It now has group and location churn.
6. **Cash flow.** The old model treated revenue as cash. It now separates collections, AR and setup timing.
7. **Market size.** The old $20–40M used a blended ARPU that included Gen 2/3. The Gen 1 SAM is $14–28M.
8. **Customer counts.** The old plan could be read as having 10 showcase customers. It has zero. The plan now says so.
9. **Pilot strategy.** The 30-day pilot and 12-month design partner are now two defined instruments, not competing claims.
10. **Toast status.** The old plan called customer-credential access the "fastest legal path." It is now UNVERIFIED and gated by a legal checkpoint.
11. **2029 ARR.** Corrected from $1.79M to $1.63M after churn and 1,183 locations.
12. **Deck and plan reconciliation.** Both use the same model outputs, rounded consistently.

## 6. What still requires founder input

1. **2027 onboarding funding.** Founders perform it (cash works, economics do not) or raise ~$25K to pay for it.
2. **Final pricing.** $59 is a hypothesis; ten interviews decide.
3. **Toast legal position.** Whether customer credentials may power a public website.
4. **Founder roles and equity.** Who owns product, sales, onboarding and support.
5. **Design-partner commitments.** Zero signed; the 2027 plan assumes 10.
6. **Entity and jurisdiction.** LLC vs. corporation; state of formation.
7. **Hiring timing.** Engineer July vs. October 2028; growth October 2028.
8. **Board attach and churn.** No data; measure from the first cohort.

## 7. Deliverables produced

1. `garnsh-business-plan-v3.0.md` / `.pdf` / `.docx` — 15 pages of main body plus appendices.
2. `garnsh-pitch-deck.pptx` / `deck.pdf` — 15 slides.
3. `model_v3.py` / `model_v3.json` — corrected executable model with churn, onboarding and cash timing.
4. `assumptions-evidence-register.md` / `.pdf` — 45-item evidence register.
5. `change-log.md` / `.pdf` — this document.

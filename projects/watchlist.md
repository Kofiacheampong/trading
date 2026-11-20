# 📊 Active Watchlist — updated Nov 20, 2026

## Thesis: Data Center Power Infrastructure / Analog Semi Supercycle

> Analog content per rack: $36K (<160kW) → $291K (600kW+) → $917K (1MW)
> AI analog TAM: $5.2B (CY25) → $15.9B (CY30)
> SiC TAM: 63% CAGR → $2.1B (CY30)
> GaN TAM: 69% CAGR → $1.6B (CY30)

---

## 📌 Read me first

- **Live levels → the table below.** The per-name sections further down are *thesis history*; their old trigger prices are superseded.
- One monitor job replaces the 17 per-ticker alert crons (Nov 20, 2026). It only speaks when a level actually crosses.
- AI-power, drone and the June `WATCHLIST.md` are consolidated here; originals in `projects/archive/`.

---

### 🎯 Live Levels — single source of truth

> Machine-readable: `projects/watchlist-levels.json` · rendered by `trading_sim/monitor.py`
> (edge-triggered: fires once per cross, re-arms only after a 1.5% move back through the level).
> Live board with prices: `projects/watchlist-board.md` · Job: cron "Stock monitor — edge-triggered" (10:15 AM + 3:50 PM ET).
> **▼ = dip/stop trigger · ▲ = reclaim / base-confirmation trigger.**

**DC Power / Analog (entry plan)**

| Ticker | Live levels | Note |
|---|---|---|
| **TXN** | ▼ $266 · ▼ $250 · ▲ $299 | Only analog name still above its 200-SMA (266). In $260-275 All-In band. |
| **ADI** | ▼ $350 · ▼ $330 · ▲ $378 | Slipped below 200-SMA (378); sitting on the $360 All-In floor. |
| **VRT** | ▼ $148 · ▲ $205 | Watch-only. Stop ($240) blown months ago; no entry framework left. |
| **INTC** | ▼ $52 · ▲ $65 | Holding + thesis broken. Entry framework void; only a reclaim matters. |
| **NVTS** | ▼ $6 · ▲ $8.55 | Watch-only. At a new 52-wk low ($6.47); stop ($10) blown. |
| **ON** | ▼ $60 · ▲ $70 | Watch-only / exit-review. Stop ($80) blown. |

**AI Power (quality + story tier)**

| Ticker | Live levels | Note |
|---|---|---|
| **CEG** | ▼ $228.63 · ▲ $262 | Quality tier. Below 200-SMA ($278); watching for a base, not a dip-buy. |
| **VST** | ▼ $110 · ▲ $132 | Quality tier, RSI 40, near 52-wk low ($110.89). |
| **GEV** | ▼ $700 · ▲ $819 | Quality tier. Broke 200-SMA ($952) decisively — uptrend over. |
| **CCJ** | ▼ $59 · ▲ $72 | Uranium. RSI 28.6 — most washed out in the group. |
| **BWXT** | ▼ $112 · ▲ $125 | Reactor components. Falling knife, −36% under 200-SMA. |
| **OKLO** | ▼ $18.5 · ▲ $24 | Story tier — spec size only, defined risk. −82% from high. |
| **SMR** | ▼ $3.4 · ▲ $4.92 | Story tier, lottery only. −85% from high. |
| **FCEL** | ▼ $5.71 · ▲ $10.1 | Fuel cells, −81% from high, below 200-SMA now too. |

**Drone/UAS (thesis broken — reclaims only)**

| Ticker | Live levels | Note |
|---|---|---|
| **AVAV** | ▼ $92 · ▲ $117 | Drone thesis broken (−77% from high, under 200-SMA). Reclaim-only. |
| **KTOS** | ▼ $28 · ▲ $36.2 | Best quality of the four, but −79% from high. Reclaim-only. |
| **ONDS** | ▼ $3.9 · ▲ $5.45 | Position closed Aug 13 (+15.8%). Re-entry watch only; at a new low. |
| **RCAT** | ▼ $1.8 · ▲ $3.85 | Microcap lottery, −90% from high. Reclaim-only, 1-2% sizing max. |

**Turnarounds / Specials**

| Ticker | Live levels | Note |
|---|---|---|
| **HNST** | ▼ $4.5 · ▼ $4 · ▼ $3.5 | Only watchlist name ABOVE its 200-SMA (+15%). Best-in-class setup on the board. |
| **NBIS** | ▼ $73.5 · ▲ $135 | AI neocloud, −70% from high. Entry (was ≤$230) retired — blown. |
| **IREN** | ▼ $12.5 · ▲ $20.7 | AI cloud/bitcoin, −82% from high, at a new low. Reclaim-only. |
| **WOLF** | ▼ $13.48 · ▲ $23.7 | Post-bankruptcy SiC. RSI 47, but −36% under 200-SMA. |
| **USAR** | ▼ $6.5 · ▲ $8.3 | Rare earths spec, −80% from high. Entry (≤$17) retired. |
| **CRCL** | ▼ $49.9 · ▲ $67.5 | Stablecoin. RSI 18.2 — deeply oversold, at the 52-wk low. |
| **CLF** | ▼ $10.5 · ▼ $9 | Only name holding its 200-SMA (−2%). The one well-calibrated trigger. |
| **CIEN** | ▼ $225 · ▼ $210 · ▲ $288 | Optical/AI interconnect, −62% from high. Plan stop $225. |
| **NVO** | ▼ $36 · ▲ $41 | GLP-1 incumbent. Waiting on the $41 reclaim; floor $36. |
| **HIMS** | ▼ $13.74 · ▲ $22.8 | Entry (≤$25) retired — blown. −62% from high. |

**Macro hedges**

| Ticker | Live levels | Note |
|---|---|---|
| **GLD** | ▼ $315 · ▲ $360 | Gold ETF at a fresh 52-wk low (323.5), RSI 27.8. Original ≤$378 trigger long gone. |
| **GDX** | ▼ $68 · ▲ $81 | Miners at the 52-wk low. |

**Holdings (stop / trim levels)**

| Ticker | Sh | Avg | Live levels | Note |
|---|---|---|---|---|
| **DRAM** | 15.5176 | $64.35 | — | Biggest position and biggest loser (−45%). Memory bust; −16% today. |
| **AMPG** | 1 | $8.72 | — | 1 share, −79%. Token position; no thesis left. |
| **MP** | 5.9683 | $67.35 | — | Rare earths. −33% under 200-SMA; breakeven is +90% away. |
| **INTC** | 1.6867 | $104.34 | ▼ $52 · ▲ $65 | IBKR cleanup lot (+ 11 sh at Fidelity). Thesis broken. |

**Retired**

- **TE** — Ex-FREYR solar, −90.6% from high, $1.18. Thesis dead — removed from alerts 2026-11-20.
- **PUSA** — Golf-course shell w/ drone unit, never had an entry level. Removed 2026-11-20 (track-only ended).
- **MDB** — Sold Aug 3 to fund ONDS. Removed from portfolio check-in 2026-11-20.

*Re-based 2026-11-20: the market is in a broad downtrend (SPY below its 200-day, VIX 28.4), so entry-below levels were replaced with reclaim-above levels for every name already past its old zone. Old below-levels only survive where they are still in front of price (CLF, HNST, NVO, CIEN, GLD/GDX).*

### 📝 Notes (last 4 checks — older notes archived)
- **Nov 20 manual retry check (15:05 UTC / 10:05 AM ET, live intraday — cron lane was dead on deepseek billing cooldown Aug–Nov, so this was run by hand):** ✅ **TXN $280.20 (−1.9%, +1.2% off the $280 floor — back INSIDE the $280–300 Best Zone after a week above it; <$290 start-building HIT; $275 All-In −1.9% away; $240 stop +16.8% clear) 🔔 THE ENTRY**, **ADI $369.46 (−2.1%, fell from $397.97 on 11/16 → −7.2% in four sessions, now INSIDE the $360–380 All-In Zone: +2.6% over the $360 floor, −2.8% under the $380 Best floor; <$380 full-position trigger HIT, <$400 start-building HIT; $330 stop +12.0% clear) 🔔**, **VRT $175.98 (−4.9%, −29.6% under the $250 All-In floor and −26.6% UNDER the $240 stop; −37% below Best Zone floor) 🔔**, **INTC $55.98 (+0.5%, still −41.6% under the $95 All-In floor and −37.8% UNDER the $90 stop; framework void — thesis-break review, NOT an add) 🔔🔔**, **NVTS $6.77 (−5.6%, −43.6% under the $12 All-In floor, −32.3% UNDER the $10 stop, only +2.9% above the $6.58 52-wk low) 🔔**, **ON $64.64 (−1.6%, −28.2% under the $90 All-In floor, −19.2% UNDER the $80 stop; plan = exit/review) 🔔**.** Net: **two buyables — TXN reclaimed its Best Zone floor and ADI dropped into All-In** (the first time both analog names are in-zone at once since Nov 10). Tape behind it is ugly: SPY 715.91 below its 200-day (733) — momentum scanner is REGIME BLOCKED — and VIX 28.4 (+64% in a month). Buy small into a broken tape, not full-size.
- **Nov 20 check (3:00 PM UTC / 10:00 AM ET, market OPEN — live intraday quotes, vs Thu Nov 19 close $285.75/$377.44/$184.99/$55.72/$7.17/$65.72 — Thursday was red across five of six):** the four-day slide finally delivered the plan's entry — **TXN $280.16 (−1.96%, slid back from $295.86 Tue → $292.43 → $285.75 → $280.16 and is sitting ON the $280 Best-Zone floor (+0.1% above it, −6.6% under the $300 ceiling); <$290 start-building HIT; <$270 full-position only −3.6% away; $240 stop +16.7% clear) 🔔 THE ENTRY**, **ADI $368.91 (−2.26%, cracked the $380 Best floor and dropped INTO the $360–380 All-In Zone, +2.5% over the $360 floor; <$380 full-position trigger HIT; $330 stop +11.8% clear) 🔔**, **VRT $175.98 (−4.87%❗, −29.6% under the $250 All-In floor, −26.7% UNDER the $240 stop; −37.1% below Best Zone floor) 🔔**, **INTC $56.00 (+0.50%, the ONLY green name in the group, still −41.1% under the $95 All-In floor, −37.8% UNDER the $90 stop, −49.1% under the $110 Best floor; framework invalid, thesis-break review, NOT an add) 🔔🔔**, **NVTS $6.77 (−5.58%❗ worst in group for the second straight check, −43.6% under the $12 All-In floor and −32.3% UNDER the $10 stop, breach widening toward the 52-wk low; −57.7% below Best Zone floor) 🔔**, **ON $64.53 (−1.81%, −28.3% under the $90 All-In floor, −19.3% UNDER the $80 stop; −35.5% below Best Zone floor; plan = exit/review) 🔔**. Net: **TWO entries live — TXN is back in its Best Zone at the $280 floor and ADI has pulled into All-In below $380**, the first time the plan has offered both analog levels together since Nov 10; everything power/auto kept sliding (VRT −4.9%, NVTS −5.6% re-widening under $10) with only INTC green on a +0.5% dead-cat tick. Size the analog pair per plan, don't add to the four stop-breached names.
- **Nov 16 check (2:00 PM UTC / 9:00 AM ET pre-market; no live pre-market print yet — quotes = Fri Nov 13 close, vs Thu Nov 12 close $312.48/$409.29/$209.64/$61.20/$9.56/$73.73 — Friday was red across all six, −2.5% to −6.4%):** the pullback finally did something useful — **ADI $397.97 (−2.77%, dropped back INSIDE the $380–400 Best Zone after one session above it: −0.5% under the $400 ceiling, +4.7% over the $380 floor; <$400 start-building HIT; <$380 full-position only −4.5% away; $330 stop +20.6% clear) 🔔 THE ENTRY**, **TXN $303.60 (−2.84%, came back to only +1.2% OVER the $300 ceiling, +8.4% over the floor — nearest it's been to the zone in a week but still no-buy; <$290 start-building OFF, −4.5% away; $240 stop +26.5% clear) ⚠️**, **VRT $202.07 (−3.61%, −19.2% under the $250 All-In floor, −15.8% UNDER the $240 stop; −27.8% below Best Zone floor) 🔔**, **INTC $59.66 (−2.52%, −37.2% under the $95 All-In floor, −33.7% UNDER the $90 stop, −45.8% under the $110 Best floor; framework invalid, thesis-break review, NOT an add) 🔔🔔**, **NVTS $8.95 (−6.38%❗ worst in group, −25.4% under the $12 All-In floor and −10.5% UNDER the $10 stop, breach widening again; −44.1% below Best Zone floor) 🔔**, **ON $71.06 (−3.62%, −21.0% under the $90 All-In floor, −11.2% UNDER the $80 stop; −28.9% below Best Zone floor; plan = exit/review) 🔔**. Net: **one entry triggered — ADI is back in its Best Zone** ($397.97, −0.5% under the $400 ceiling) on Friday's −2.8% fade, the first live buy signal since Nov 10; TXN is knocking on the door at +1.2% over $300 (needs ≤$290 to start, −4.5% away); the power/auto four stayed stop-breached and got worse — NVTS −6.4% re-widening under $10, INTC still deepest at −37.2% below All-In.
- **Nov 13 check (2:00 PM UTC / 9:00 AM ET pre-market; no live pre-market print yet — quotes = Thu Nov 12 close, vs Wed Nov 11 close $309.81/$409.08/$206.51/$62.50/$10.07/$73.62 — Thursday split the group: analog flat, NVTS/INTC red):** the two-day rally stalled at the top — **TXN $312.48 (+0.86%, still +4.2% OVER the $300 Best-Zone ceiling, +11.6% over the floor; <$290 start-building OFF; <$270 full-position OFF (−13.6% away); $240 stop +30.2% clear — extended, no chase) ⚠️**, **ADI $409.29 (+0.05%, dead flat, +2.3% over the $400 ceiling, +7.7% over the $380 floor; <$400 start-building OFF; <$380 full-position OFF (−7.1% away); $330 stop +24.0% clear — not a buy) ⚠️**, **VRT $209.64 (+1.52%, −16.1% under the $250 All-In floor, −12.6% UNDER the $240 stop; −34.5% below Best Zone floor) 🔔**, **INTC $61.20 (−2.03%, gave back Wednesday's +7.5%❗ — −35.6% under the $95 All-In floor, −32.0% UNDER the $90 stop, −44.4% under the $110 Best floor; framework void, thesis-break review, NOT an add) 🔔🔔**, **NVTS $9.56 (−5.07%❗ worst in group, lost the $10 stop reclaim after one session — −20.3% under the $12 All-In floor, now −4.4% UNDER the $10 stop again; −40.3% below Best Zone floor) 🔔**, **ON $73.73 (+0.15%, −18.1% under the $90 All-In floor, −7.8% UNDER the $80 stop; −26.3% below Best Zone floor; plan = exit/review) 🔔**. Net: **zero entries triggered** — the analog pair is still parked above its ceilings (TXN +4.2% over $300, ADI +2.3% over $400), so the plan's only buy levels remain OFF on the upside; the power/auto four reversed Thursday (NVTS −5.1%, INTC −2.0%) and all four are stop-breached again, NVTS re-breaking $10 and INTC deepest at −32.0%. Nothing to do: wait for TXN ≤$290 or ADI ≤$400, and treat VRT/INTC/NVTS/ON as thesis-break reviews, not adds.

---


## 🛟 Turnaround / Special Situations — added Aug 6, 2026

> Thesis: consumer brand at a proven inflection — GAAP-profitable, record margins,
> organic growth accelerating, clean balance sheet. Small-cap volatility = spec sizing.

### HNST — The Honest Company (Jessica Alba's clean baby/personal care brand)

- **The event:** Q2 2026 (reported Aug 5): revenue $83.3M (−10.9% reported, **Organic +6.7%**),
  gross margin **48.4% (+800 bps)**, GAAP net income **$10.7M**, adj. EBITDA margin 9.8%,
  cash $105.9M. **Raised FY26 guidance.** Stock +41% on Aug 6 (3.85 → 5.42, 52w high $5.84).
- **Why it's a watch, not a buy today:** +162% off 52w low ($2.07). Post-earnings pops
  typically pull back 10–20% before the next leg. **Do NOT chase at $5.40+.**
- **Entry zones:** Best Zone **$4.50–5.00** (consolidation pullback) · All-In **$4.00–4.50**
  (deep pullback toward the $3.65–3.90 pre-pop base)
- **Stop:** $3.50 (below the pre-earnings base = rally failed)
- **Targets (1yr/3yr):** $7.50 / $10 — 2–3% spec position max (small-cap turnaround, diapers still declining)
- **Bear risks:** reported revenue still shrinking (−11%), diaper category declining,
  brutal CPG competition (Coterie, Hello Bello, P&G/Kimberly), consumer spending pressure.

### 🚨 HNST Triggers
- HNST < $5.00: Start small (1% spec)
- HNST < $4.50: Add to 2%
- HNST < $4.00: Full spec position (3%)
- HNST < $3.50: Stop — thesis failed, exit

---

## 🚀 AI Neocloud / Infra Momentum — added Aug 12, 2026

> Thesis: AI capacity demand growing "exponentially" (CEO); neoclouds convert demand into
> contracted, prepaid growth. NBIS differs from CRWV: customers prepay 50–60% of capex,
> so the build-out is customer-funded, not debt-funded. Momentum/spec bucket — NOT Tier-1 quality.

### NBIS — Nebius Group (AI cloud, Nvidia-backed)

- **The event:** Q2 2026 (reported Aug 12 pre-market): revenue **$582M (+454% YoY)** vs $574M est;
  EPS -$0.68 vs -$0.70 est. 4 deals >$1B TCV each (Reflection, Cohere, US AI lab, US quant fund).
  Avg yield >$20M/MW, prices heading to $40–50M/MW (first deal at that level already signed).
  70% of deals prepaid 50–60% of capex. Contracted power raised to 5 GW by YE26 (was 4+ GW).
  Stock +29% intraday on the print; +131% YTD. Backlog: Meta $27B/5yr; Nvidia $2B stake.
- **Why it's a watch, not a buy at $250:** earnings spike +29% in a day — buying here is buying
  the top of a spike. RSI blowing out. **Do NOT chase.** Wait for digestion (10–15% pullback).
- **Entry zones:** Best Zone **$215–230** (first pullback toward the gap) · All-In **$190–205**
  (gap fill toward pre-earnings close $193.23)
- **Stop:** $175 (below the pre-earnings base = spike failed)
- **Targets (1yr/3yr):** $300 (52w high retest) / $410 (Northland street-high) —
  **2–3% spec position max** (momentum name, no earnings moat proven yet)
- **Bear risks:** revenue recognition mostly 2027 — paying today for tomorrow's numbers;
  hyperscaler competition (MSFT/GOOG/AMZN renting their own capacity);
  capex arms race ($20–25B/yr guidance); stock still -17% off 52w high ($299.86).

### 🚨 NBIS Triggers
- NBIS ≤ $230: Start small (1% spec)
- NBIS ≤ $205: Add to 2%
- NBIS ≤ $190: Full spec position (3%)
- NBIS < $175: Stop — thesis failed, exit
- NBIS ≤ $230: daily 11 AM ET alert active (entry zone watch)

### IREN — Iren Limited (AI cloud + bitcoin, Microsoft/Nvidia-backed) — added Aug 13, 2026

- **The event:** Aug 13, 2026: delivered **first 50MW Microsoft AI cloud deployment at Childress** (Horizon 1) + **NVIDIA "Exemplar Cloud" status for GB300 deployment at Microsoft's Houston** facility. Stock +11% to $48.46 on the print (intraday $45.38–$49.19).
- **Context:** 52wk range $17.22–$76.87; 3mo range $29.31–$67.84. Jul 29 washout low $29.31 → now $48 (+65% in 3 weeks). SMA20 $38.87, SMA50 $45.39 — price extended above both after today's spike.
- **Why it's a watch, not a buy at $48:** +11% single-session spike after a 3-week run = chasing risk. Real catalyst (Microsoft/NVIDIA validation) but momentum/spec bucket, NOT Tier-1 quality.
- **Entry zones:** Best Zone **$40–42** (retest of breakout / SMA20 confluence) · All-In **$35–38** (July base)
- **Stop:** $32 (below July consolidation — thesis failed)
- **Targets (1yr/3yr):** $60 (near-term supply) / $77 (52w high retest) — **2–3% spec position max**
- **Bear risks:** bitcoin-mining legacy drag; hyperscaler competition; stock still -37% off 52w high — paying up for momentum after a spike

### 🚨 IREN Triggers
- IREN ≤ $42: Start small (1% spec)
- IREN ≤ $38: Add to 2%
- IREN ≤ $35: Full spec position (3%)
- IREN < $32: Stop — thesis failed, exit
- IREN ≤ $42: daily 11 AM ET alert active (entry zone watch)

---

## ⚡ Post-Earnings Turnaround / AI-Power Spec — added Aug 17, 2026

> Thesis: post-bankruptcy SiC chipmaker repricing from "EV bust" to "AI datacenter power".
> Real narrative (TOLT packaging, LITEON 800V hyperscale partnership, Amperesand SST deal),
> but fundamentals still negative (gross margin -27%, FQ4 guide $140-160M, June dilution overhang,
> avg analyst PT ~$25). Momentum/spec bucket — NOT Tier-1 quality.

### WOLF — Wolfspeed (silicon carbide power, NYSE)

- **The event (Aug 17):** $33.44 (+5.2%), tagged $34.09 early then faded. AI-datacenter power
  narrative: next-gen TOLT portfolio (Gen 4 MOSFET, 650V AI racks), LITEON partnership to
  qualify SiC for 800V hyperscale power, Amperesand $13B SST-market deal. It's a 10%-a-day
  yoyo: +14.8% Jun 17, +17.7% Jul 30, +14.1% Aug 6 — with -10%+ drops between. 52wk $8–$81.
- **Technical snapshot (Aug 17):** RSI 71.6 (overbought by our scanner math), +17.7% above
  200-day MA ($28.41), SMA50 $36.71 (resistance overhead), 1y range $14.80–$73.50.
- **Why it's a watch, not a buy at $33:** RSI 72 + +5% day + earnings in 2 days = coin flip.
  Your own rules exclude it: momentum scanner has a no-calls-straddling-earnings rule, and
  fade logic says don't fight RSI 72 into a binary event. **Do NOT chase.**
- **The catalyst to wait for: fiscal Q4 earnings Wed Aug 19.** If the print is OK and the
  stock pulls back toward the 200-day MA, that's the real entry with the AI-power story intact.
  If it gaps, we dodged a coin flip.
- **Entry zones:** Best Zone **$28–30** (200-day MA confluence + early-Aug base) ·
  All-In **$24–26** (July consolidation / gap zone)
- **Stop:** $22 (below July base = rally failed)
- **Targets (1yr/2yr):** $40 (recent supply / simplywall.st noted ~$40 trading) / $50 —
  **1–2% spec position max** (post-bankruptcy, negative margins, dilution overhang)
- **Bear risks:** earnings Aug 19 is binary (could gap down on weak guide); negative gross
  margins; Chinese SiC competition + oversupply; dilution from June secondary; analysts
  cautious (Susquehanna cut to $30, avg PT ~$25).

### 🚨 WOLF Triggers
- WOLF ≤ $30: Start small (1% spec) — **only after Aug 19 earnings print**
- WOLF ≤ $26: Add to 2%
- WOLF < $22: Stop — thesis failed, exit
- WOLF ≤ $30: daily 11 AM ET alert active (entry zone watch; reminder: post-earnings only)

---

## 🧲 Rare Earths / Critical Minerals Spec — added Aug 17, 2026

> Thesis: US critical-minerals supply chain buildout — CHIPS funding, possible government
> price-floor policy (would lift USAR + MP + UAMY). Momentum/spec bucket — NOT Tier-1 quality.

### USAR — USA Rare Earth (Nasdaq)

- **The setup:** $19.05 (-4.75% Aug 17) after a +50% 3-week run ($13 → $20). Q2 (Aug 10)
  missed on both lines (rev $5.8M vs $8.0M est, EPS -$0.15 vs -$0.13) — story stock + miss = fade.
  52w range $11.45–$43.98.
- **The catalyst:** **Serra Verde merger ($2.83B) closing by end of August** (offtake-agreement
  condition). That's the real event — buy the post-close reaction, not the pre-close guess.
  Also: CHIPS funding secured, Carester stake, price-floor policy talk.
- **Why it's a watch, not a buy at $19:** +50% run + earnings miss + pending binary merger = wait.
  Street positive (Cantor Overweight, avg PT ~$35.83) but that's story coverage.
- **Entry zones:** Best Zone **$15–17** (SMA20 ~$16.70 confluence, ~15% below Aug 17 close) ·
  All-In **$13–14** (July base / pre-run consolidation)
- **Stop:** $11 (below 52w low $11.45 = thesis broken)
- **Targets (1yr/2yr):** $28 / $40 (52w high retest) — **1–2% spec position max** (no revenue,
  merger-dependent, dilution risk)
- **Bear risks:** SVRE merger falls through (offtake condition); continued cash burn; rare earth
  prices stay soft; another dilution; policy talk stays talk.

### 🚨 USAR Triggers
- USAR ≤ $17: Start small (1% spec) — toe-dip zone
- USAR ≤ $14: Add to 2%
- USAR < $11: Stop — thesis failed, exit
- USAR ≤ $17: daily 11 AM ET alert active (entry zone watch)

---

## 🪙 CRCL — Circle Internet Group (crypto/stablecoin tilt) — added Aug 19, 2026

> Thesis: USDC issuer, biggest direct beneficiary of stablecoin legislation (GENIUS Act
> signed Jul 2025; CLARITY Act advancing — would ban stablecoin yield, making USDC the
> compliant option). OCC national trust charter approved Aug 19, 2026 → federal trust bank.
> High-beta crypto proxy — binary-ish around CLARITY Act timing. Watch, not buy now (just
> popped +9.6% on OCC news).

- **The setup:** $78.59 (Aug 19, +9.6% on OCC charter). IPO Jun 2025 @ $31 → $164 high →
  halved in Oct 2025 crypto meltdown → recovered ~150% off Feb lows. Still ~52% below 52w high.
- **Fundamentals (Q2, Aug 6):** USDC circulation $73.3B (+19% YoY), $14.8T onchain volume.
- **Street:** Bernstein $190 target (+129%); "Nvidia of crypto" chatter.
- **Entry zones (pullback, no chase):** Best **$68–72** (pre-OCC base, alert set ≤$70) ·
  All-In **$60–65** (deeper fill / CLARITY-act stumble)
- **Stop:** $52 (below Feb-recovery trend = thesis broken)
- **Targets (1yr/2yr):** $100 / $150 (KuCoin CLARITY thesis) — **1–2% position max** (crypto
  beta, legislation binary risk, no dividend, high vol)
- **Bear risks:** CLARITY Act stalls or weakens; stablecoin yield competition; crypto
  deleverage again; OCC charter path hits friction.
- **Alert cron active:** CRCL ≤ $70 weekdays 11 AM ET (silent unless triggered).

### 🚨 CRCL Triggers
- CRCL ≤ $70: Start small (1% spec) — best-zone top
- CRCL ≤ $65: Add to 2% — all-in zone
- CRCL < $52: Stop — thesis failed, exit

---

## 🏗️ CLF — Cleveland-Cliffs (transformer-steel / GOES bottleneck) — added Aug 20, 2026

> Thesis: SOLE US domestic producer of grain-oriented electrical steel (GOES) — the
> specialty steel in transformer cores. AI data centers are bottlenecked on power
> transformers (2-4yr lead times; ~half of 2026 US AI DCs delayed/canceled). CLF = toll
> booth on the grid buildout. Watch, don't chase — financials still recovering.

- **The setup:** $11.17 (-5.98% Aug 19, steel sold off with chips). Market cap $6.37B,
  EV $14.03B. 52wk +5.6%. Beta 2.12, RSI 45.8 (neutral).
- **Q2 2026 (Jul 23):** Rev $5.2B; returned to positive FCF; adj EBITDA tripled
  sequentially; guidance stronger Q3/Q4 (contract resets, cost cuts, asset sales).
- **The ugly TTM numbers:** net -$876M (EPS -$1.60), gross margin -1.1%, FCF -$857M,
  total debt $7.72B vs cash $70M (net debt -$7.65B), Debt/EBITDA 10.3x, interest
  coverage -0.9x, Altman Z 1.26 (distress zone), shares +12.35% YoY (dilution).
- **Electrical steel segment:** only ~$1.86B of $19.2B TTM revenue (~10%) — the GOES
  moat is real but small; transformer-steel upside is optionality, not current P&L.
- **Analysts:** PT $11.80 (+5.6%), Hold, 13 covering. Short interest 14.1% of float.
- **Entry zones (pullback, no chase):** Best **$9.50–10.50** (alert set ≤$10.50) ·
  All-In **$8.00–9.00** (2026 lows / deep-cycle bottom)
- **Stop:** $7.50 (below cycle support = thesis broken)
- **Targets:** $15 / $20 (1yr/2yr) — **1–2% spec position max** (cyclical, levered,
  losing money TTM; GOES premium not yet in earnings)
- **Peers (quality comparison):** NUE $248.74 (PE 19.9, fwd 11.6, ROIC 12%, debt/EBITDA
  1.2x, dividend) · STLD $231.01 (PE 21, fwd 11.4, ROIC 12.4%, dividend) — profitable,
  clean balance sheets, but less pure AI/GOES exposure and pricier.
- **Alert cron active:** CLF ≤ $10.50 weekdays 11 AM ET (silent unless triggered).

### 🚨 CLF Triggers
- CLF ≤ $10.50: Start small (1% spec) — best-zone top
- CLF ≤ $9.00: Add to 2% — all-in zone
- CLF < $7.50: Stop — thesis failed, exit

---

## 📡 CIEN — Ciena (optical transport / AI interconnect) — added Sep 10, 2026

> Thesis: Ciena is the optical-networking/interconnect layer between AI compute and the data
> center (WaveLogic 6 Extreme coherent, 800ZR pluggables, Hyper-Rail, DCOM). Demand is not
> the problem — capacity to convert it is. Watch, don't chase: priced for perfection
> (~7.7x sales, ~50x FY26 adj EPS) and the chart is broken after a −46% drawdown from $627.

- **The event (Sep 3, 2026 — fiscal Q3):** record quarter. Rev **$1.671B (+37% YoY, top of
  guide)**, adj EPS **$2.11 (+215%)** vs ~$1.73 est (+21% beat), record adj op margin **22.5%**,
  GM 46.4%, FCF **$116M**, cash **$2.8B**. Backlog **$8.5B** (+$800M QoQ), guided to exit FY26
  **>$10B** — vast majority customer-requested for **2027**. Direct cloud revenue **+80%**;
  in-and-around-DC revenue quadrupled YTD. FY26 guide raised to **$6.42B (+35%)**; FY27 baseline
  **≥30% ($8.3–8.4B)** with "supply-driven upside."
- **Why it fell anyway (−11% on the print):** management said component supply constraints keep
  supply/demand out of balance **into 2028** — they can't convert backlog fast enough, so revenue
  recognition is capped. Plus valuation. Street kept mostly Buys but cut targets (TD Cowen
  $675→$575; Stifel Buy $615; Rosenblatt/Barclays/Evercore/B.Riley trims; street low $270).
- **Technical snapshot (Sep 9 close):** $338.00, **−46% from the $627 high**, −22% in 30 days.
  Below SMA20 $384.95 / SMA50 $399.16 / SMA200 $378.68 — broken chart, no base. RSI(14) 39.4
  (cooling, not washed). 52wk range $123.65–$637.51.
- **Why it's a watch, not a buy at $338:** best-in-class AI-infra business ≠ buy here. The
  selloff driver (supply timing) is exactly what the market punishes until it shows in reported
  numbers, and at ~50x with two customers >10% of revenue, any AI-capex wobble hits it hard.
- **Entry zones:** Best Zone **$280–305** (deeper flush, RSI <30) · All-In **$240–265**
  (AI-capex derating / broad semi washout)
- **Reclaim path (alternative):** start 1% only if it holds/reclaims **>$385 (20-SMA)** and
  builds a base — stop under **$317** (Sep 3 post-earnings low) on that path.
- **Stop (zone entries):** $225 (below the wash zone = thesis broken). Do **not** anchor to the
  $123 52wk low.
- **Targets (1yr/2yr):** $450 (backlog conversion / PT cuts settle) / $600 (52wk high retest) —
  **1–2% spec position max** (high-beta AI-capex proxy, customer concentration).
- **Bear risks:** component supply stays tight into 2028 (revenue recognition capped); AI capex
  slows and a ~50x multiple compresses hard; two customers >10% of revenue (concentration);
  backlog ≠ booked revenue; direct cloud/DC revenue is lumpy quarter to quarter.
- **Alert cron active:** CIEN ≤ $305 weekdays 11 AM ET (silent unless triggered).

### 🚨 CIEN Triggers
- CIEN ≤ $305: Start small (1% spec) — best-zone top
- CIEN ≤ $265: Add to 2% — all-in zone
- CIEN < $225: Stop — thesis failed, exit
- CIEN > $385 (reclaim): optional 1% momentum starter, stop under $317

---

## 💊 NVO — Novo Nordisk (GLP-1 incumbent on a dated clock) — added Sep 22, 2026

> Thesis check: looks like a textbook quality-on-discount name on the screen (PE ~9.8,
> ROIC ~39%), but the discount is NOT sentiment — it's measurable deterioration: Lilly
> winning the GLP-1 duopoly + a hard semaglutide patent cliff the company itself dates
> (US LOE 2032). Closest analogue in our book is the FAILED screen bucket (NKE/CRM/NOW/UNH
> — "deteriorating business"), just with better ROIC. **Watch, do not catch the knife.**

- **The event (Sep 21, 2026):** Capital Markets Day in London laid out 2030 ambitions
  (5+ multi-blockbuster drugs by 2030, >DKK 150B risk-adjusted pipeline sales by 2035,
  60M patients, "grow in line with peers"). Investors wanted a decisive turnaround and
  didn't get one — the ADR gapped **$43.24 → $39.80 (−8.0%)** the same session on
  **49.3M shares vs ~10M typical** (institutional distribution, not a dip-buy flush).
  Sep 22 followed through to **$39.40 (−1.0%)**, after-hours $39.34.
- **The numbers (Sep 22, 2026 close):** $39.40 · market cap $175B · **−38.4% from the
  $64.16 52-wk high** · 52-wk low **$35.12** · RSI(14) **30** · SMA20 $44.46 / SMA50 $46.51
  (below both) · trailing PE **9.84** / forward PE **12.24** / PB 5.18 / EV/EBITDA 7.15 /
  P/FCF 15.1 · **ROIC 39.2%, ROE 59.8%** · Debt/Equity 0.63.
- **Why it's a watch, not a buy at $39.40:** three structural, dated problems —
  1) **Lilly is winning the race** (LLY +52% vs NVO −27% over the trailing year);
  2) **Forward PE (12.2) ABOVE trailing PE (9.8)** = the market is explicitly modeling
  *earnings decline* into the 2032 US semaglutide LOE — the CEO called it "the elephant
  in the room";
  3) the plan leans **volume over price** ("10x capacity for oral GLP-1"), which is
  margin-thin growth.
  A 9.8x PE on falling E can get cheaper. That's the value-trap signature.
- **Entry zones (no chase, confirmation only):** **Confirmation $41–42** (reclaim + 2 closes
  above the post-CMD shelf = sellers exhausted) · **Floor $35–36** (hard hold of the $35.12
  52-wk low — deeper value entry, not a guess at the bottom).
- **Stop:** **closing break below $33** (under the 52-wk low = thesis failed, exit). Do not
  average down through it.
- **Targets:** $52 (1yr, if stabilization confirms) / $70 (3yr, only if pipeline diversification
  actually lands) — **1–2% spec position max**.
- **Catalyst to wait for:** **Q3 earnings Wed Nov 4, 2026, pre-market** (confirmed). First real
  checkpoint — buying before it is paying to find out.
- **Venue:** IBKR for anything structural; Fidelity (Tier 1) can only do **long calls** here
  (no spreads). NVO options are liquid.
- **Bear risks:** GLP-1 share loss compounds; US pricing pressure; 2032 LOE arrives with the
  market already discounting it; "diversification" stays a slide deck; further guidance cuts.
- **Alert cron active:** NVO ≤ $41 weekdays 11 AM ET (silent unless triggered).

### 🚨 NVO Triggers
- NVO ≥ $41 (reclaim, 2 closes): Start small (1% spec) — confirmation path
- NVO ≤ $36 (hard hold of 52-wk low): Add to 2% — floor path
- NVO < $33 (closing break): Stop — thesis failed, exit
- NVO before Nov 4 earnings: no new entries (binary checkpoint)

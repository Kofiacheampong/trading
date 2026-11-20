# 🔍 Stock Monitoring Audit — Nov 20, 2026

*Review of every file and cron job that watches stocks. Evidence pulled live from cron run history (Sep 11 → Nov 19, 2026), Yahoo quotes 10:05 AM ET Nov 20, and the files themselves.*

---

## 1. What exists

### Watchlist / thesis files (6)
| File | Size | Last real update | Names covered |
|---|---|---|---|
| `projects/watchlist.md` | 95 KB / 422 lines | Nov 20 (cron writes daily) | TXN, ADI, VRT, INTC, NVTS, ON + HNST, NBIS, IREN, WOLF, USAR, CRCL, CLF, CIEN, NVO |
| `projects/ai-power-watchlist.md` | 2.7 KB | **Aug 16** (3 months) | CEG, VST, GEV, CCJ, BWXT, OKLO, SMR, FCEL, TE |
| `projects/drone-watchlist.md` | 3.4 KB | **Sep 17** (2 months) | AVAV, KTOS, ONDS, RCAT, PUSA |
| `WATCHLIST.md` (workspace root) | 3 KB | **Jun 23** (5 months) | HIMS, USAR, INTC, IONQ/QBTS/RGTI/QUBT, nuclear basket, CCL/SOFI/MARA |
| `projects/regime-change-playbook.md` | — | Aug 13 | regime signals (VIX, breadth) |
| `projects/earnings-cheatsheet.md` | — | Aug 12 | reference only, no tickers |
| `TRADING-SYSTEM.md` | 5.3 KB | Aug 16 | rules of engagement (spreads, stops, sizing) |

### Monitoring code (21 scripts)
- **Live / wired to cron (6):** `trading_sim/momentum_calls.py`, `trading_sim/sim.py`, `trading_sim/breadth.py`, `trading_sim/opportunity.py`, `scripts/budget_dips.py`, `scripts/protect.sh`
- **Used inside sims (6):** `options_data.py`, `mes_sim.py`, `mes_intraday.py`, `covered_calls.py`, `fade_flags.py`, `data_health.py`
- **Dead weight — zero references anywhere (7):** `scripts/200wma_screen.py`, `scripts/200wma_screen2.py`, `scripts/200wma_budget.py`, `scripts/weeklies_scan.py`, `scripts/weeklies_scan2.py`, `scripts/options_screen.py`, `trading_sim/lottery_demo.py`
- **Manual utility (1):** `scripts/legcheck.py`
- **Shared state:** `trading_sim/state.json` — 130 KB (214 opportunities, 191 cc_skips, 53 puts, 23 MES-intraday trades) + 3 stale backups totalling 140 KB

### Cron jobs (33)
17 level-alert jobs · 4 momentum sweeps · 2 ONDS squeeze trackers · 2 sim (daily/report) · 2 betting · 5 weekly/periodic reports · 1 backup.

---

## 2. Headline numbers (the problem in one line)

**383 alert messages delivered in 69 days (~5.5/day) from 17 jobs — 3 of which were "triggered" on literally every single run.**

| Job | Runs | Delivered | Signal |
|---|---|---|---|
| MP ≤ $55 | 47 | **47** | MP $37.24 — triggered 100% of runs |
| AI-power basket (9 names) | 46 | **46** | all 9 below entry since ~Aug 20 |
| Drone basket (4 names) | 45 | **45** | all 4 below entry since Aug 15 |
| USAR ≤ $17 | 45 | **45** | USAR $7.02 — 100% |
| WOLF ≤ $30 | 45 | 39 | WOLF $20.22 |
| IREN ≤ $42 | 45 | 33 | IREN $13.45 |
| NBIS ≤ $230 | 45 | 33 | NBIS $91.34 |
| INTC ≤ $100 | 47 | 24 | INTC $56.00 |
| Gold GLD ≤ $378 | 46 | 21 | GLD $327.46 |
| ONDS squeeze AM/PM | 47/44 | 5/11 | position closed in August |
| HNST / HIMS / CRCL / CIEN | 47/47/45/45 | 9/7/7/9 | intermittent |
| NVO $41 reclaim | 38 | 2 | at $38.93, waiting on reclaim |
| CLF ≤ $10.50 | 45 | **0** | never triggered — the one well-calibrated alert |

**Why this matters beyond noise:** every one of those jobs is a full LLM turn — ~25 model calls every weekday, each reading a large prompt. That is the real reason DeepSeek credits drained to zero and every job died with a billing error in mid-November. The monitoring suite costs more than it reports.

**Root cause (design, not bug):** alerts are *level-triggered* with no state. Once a name sits below its trigger, the job re-fires forever. Nothing knows "I already told him."

---

## 3. Findings, ranked

### 🔴 1. No trigger-state memory → 383 redundant alerts
Every alert job re-alerts daily forever. The only job that stayed quiet (CLF, 0 deliveries) is quiet by luck, not design.
**Fix:** one script, one state file: alert only on *transitions* (armed → triggered), and again on a material change (>2% move) or a reset back above the level.

### 🔴 2. Levels are stale by months and unre-baselined
Current vs trigger:
- AI-power: CEG 246.7 vs ≤270 · VST 121.3 vs ≤140 · GEV 734.9 vs ≤1010 · CCJ 61.25 vs ≤92 · BWXT 115.5 vs ≤168 · OKLO 21.35 vs ≤41 · SMR 3.68 vs ≤8.5 · FCEL 7.33 vs ≤20 · TE 1.23 vs ≤4.2 → **all 9 blown through, average −38% below trigger**
- Drone: AVAV 96.22 vs ≤166 · KTOS 29.04 vs ≤53 · ONDS 4.12 vs ≤8.35 · RCAT 1.92 vs ≤8.60 → **−42% to −78% below trigger**
- These aren't buy zones any more, they're "the thesis broke" markers. Waiting for a bounce back *up* to them is backwards.
- Both files' status logs stop in Aug/Sep — the daily alert never wrote anything back to the file.

### 🔴 3. Three competing watchlists, one source of truth missing
`projects/watchlist.md` (Nov 20, 15 names), `projects/ai-power-watchlist.md` (Aug 16, 9 names), `WATCHLIST.md` root (Jun 23, ~15 names), plus 13 per-ticker cron prompts holding *their own* copies of levels. Levels now live in 4 places and disagree:
- HNST: watchlist.md says add at $4.50 / full at $4.00; the cron alerts at **≤$4.80**. Different plan.
- USAR, INTC, HIMS appear in both root WATCHLIST.md (June prices) and the current files.
- Root `WATCHLIST.md` is 5 months old, still quotes HIMS ~$35.25 (now $15.83) — actively misleading if anything ever reads it.

### 🟠 4. `projects/watchlist.md` is a 95 KB append-only log
422 lines, individual note lines up to **1,885 characters**. Every daily check appends a mega-paragraph; nothing is ever archived. The table's "Status" cells are also paragraph-length, so the file is unreadable as a table and expensive to load. Notes for Oct 26 → Nov 20 all still sit at the top of the file.
**Fix:** keep table + last 7 days of notes in the file; move older notes to `memory/watchlist-archive-2026.md`.

### 🟠 5. Zero coverage of what he actually owns
Holdings: **DRAM 15.5 sh, AMPG 1 sh, MP 5.97 sh, INTC 1.69 sh (IBKR) + 11 sh INTC (Fidelity)**.
- **DRAM — no watchlist, no alert, nothing.** It's the biggest dollar loser (−$108 at the Aug snapshot) and no system watches it.
- **AMPG — nothing**, despite −32% on a single day in August.
- MP/INTC have *entry* alerts (≤$55, ≤$100) but nothing for stop-loss or trim decisions on the position held.
- The Weekly Portfolio Check-In still asks about **MDB**, sold in August to fund ONDS.

### 🟡 6. Momentum sweeps run into a blocked regime 4×/day
`momentum_calls.py --alert` today: `REGIME BLOCKED (SPY 716 < SMA200 733)` → NO_ALERTS. The scanner cannot flag anything until SPY reclaims its 200-day, but 4 cron jobs/day × 1 LLM turn each still spin up to read "NO_ALERTS". VIX is 28.4 (+64% in a month) — regime gate is doing its job; the schedule isn't adapting.
**Fix:** have the script itself gate on regime and write a state flag; skip the model call entirely (or collapse 4 sweeps → 2) while blocked.

### 🟡 7. Dead scripts and state bloat
7 unreferenced scripts (two generations of the 200-WMA screen, two of the weeklies scanner, `options_screen.py`, `lottery_demo.py`). `state.json` has no pruning policy and 3 redundant backups.

### 🟡 8. Two betting agents, both failing
EPL (daily) and CL (Tue–Thu) — separate domain, fine, but both sit in error state with the same billing root cause and neither has produced a bet log since the outage.

---

## 4. What I'd build instead (target architecture)

1. **One `monitor.py` + `monitor_state.json`.** All tickers, all levels in one table, edge-triggered. Replaces 17 cron jobs with 1 job (1 script run, 0 model calls unless something actually changes). ~90% of the credit burn disappears.
2. **Re-base the dead levels** — either to current structure (drone: is the thesis still alive at AVAV $96?) or retire the name. Decision per ticker, not a blanket rewrite.
3. **Consolidate to `projects/watchlist.md` as the single source of truth**; move ai-power + drone + root WATCHLIST.md into it (or archive them with a pointer), and have cron read *from* the file instead of carrying levels inside prompts.
4. **Add holdings monitoring** — DRAM and AMPG at minimum; stop/trim levels, not just entry levels.
5. **Fix the Weekly Portfolio Check-In ticker list** (drop MDB).
6. **Archive notes older than 7 days** out of watchlist.md.
7. **Delete/archive the 7 dead scripts**, prune state.json backups to one.

---

## 5. Decisions needed from Kofi

1. Re-base or retire the drone and AI-power watchlists? (all levels are 40–80% off; the theses may be dead, not cheap)
2. Approve collapsing the 17 alert crons into one edge-triggered job? (biggest credit + noise win)
3. Which holdings get stop/trim alerts — DRAM, AMPG, MP, INTC?
4. Root `WATCHLIST.md` (June) and the Aug ai-power file — archive into `projects/watchlist.md`, or keep separate?

*Audit run Nov 20, 2026 15:30 UTC. Quotes: Yahoo v8 chart API, live intraday.*

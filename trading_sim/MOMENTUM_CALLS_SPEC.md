# Momentum Call Scanner — Build Plan

**Goal:** Replicate the friend's momentum-call alert system on our own stack.
Scan for overbought momentum names, confirm with volume + market regime, pick a
15-DTE call, score confidence, alert to Telegram intraday, and paper-trade the
alerts in the sim until the hit rate earns real money.

**Reference (friend's alerts, 8/6/26):** TOST $35C (conf 0.57), PRGO $12.50C
(conf 0.76), FSLY $26C (conf 0.55). All RSI 76, Z +2.7σ to +8.3σ, 2.0–2.9× vol,
15 DTE, TP +100% / SL −50% / time stop 7 DTE.

---

## 1. Data Layer — `trading_sim/options_data.py` (new)

Reuse proven pieces from `sim.py` (crumb + Yahoo v7 options API already work for
puts). Generalize and add:

- `get_crumb()` — move from `sim.py`, share via import.
- `fetch_chain(sym, expiry_ts, crumb)` — returns calls list: strike, bid, ask,
  last, IV, open interest, volume, delta. (Same endpoint as `fetch_put_quote`,
  read `calls` instead of `puts`.)
- `pick_expiry(sym, crumb, target_dte=15, min_dte=10, max_dte=21)` — nearest
  listed weekly expiry in range (Yahoo expirations are Thursdays/Fridays).
- `spread_pct(bid, ask)` → `(ask-bid)/mid * 100`.
- `fetch_quote(sym)` — reuse `fetch_history` from `opportunity.py` (1d bars give
  today's live print as last close).
- `fetch_regime()` — SPY close + 200-day SMA (via `fetch_history("SPY")`),
  VIX close (via `fetch_history("^VIX")`). Cached per run.

## 2. Scanner — `trading_sim/momentum_calls.py` (new)

### Entry filters (ALL must pass)
- RSI(14) ≥ 70
- Z-score vs 20-day avg ≥ +2.5σ  → add `zscore(closes, 20)` helper
- Volume ≥ 2.0× 20-day average
- Uptrend intact: px > SMA50 > SMA200 (continuation, not first pop)
- Regime: SPY > SMA200 **and** VIX < 20

### Contract selection
- Expiry: 10–21 DTE, prefer 15
- Strike: ATM or one strike ITM (delta 0.45–0.65)
- Liquidity gate: OI ≥ 500 · bid > 0 · spread < 15% to trade
  (15–30% = flag "use limit near mid, not market"; >30% = reject)
- IV sanity: < 150%

### Confidence score (0–1, mirrors friend's)
| Signal | Points |
|---|---|
| RSI ≥ 75 / 70–75 | 0.20 / 0.10 |
| Z ≥ 3σ / 2.5–3σ | 0.20 / 0.10 |
| RelVol ≥ 2.5× / 2–2.5× | 0.20 / 0.10 |
| Spread < 10% / 10–15% | 0.20 / 0.10 |
| Regime VIX < 18 / 18–20 | 0.10 / 0.05 |
| Trend px > SMA50 > SMA200 | 0.10 |

**Trade threshold: 0.60.** (Validation: friend's PRGO = 0.76 → alert; TOST 0.57,
FSLY 0.55 → correctly skipped. Our filter would have only fired PRGO.)

### Output per candidate
Ticker · spot · strike · expiry (DTE) · mid premium · break-even (+% vs spot) ·
cost/contract · RSI · Z · relvol · spread% · IV · delta · confidence · exit plan
(TP +100%, SL −50%, time stop 7 DTE).

## 3. Alerting — cron, silent unless triggered

- `momentum_calls.py --alert`: runs scan; skips tickers already alerted today
  (dedupe key = ticker+strike+expiry+date in state.json `call_flags`);
  prints formatted alert(s) or `NO_ALERTS`.
- Cron (isolated agentTurn → Telegram, like Weeklies Scanner): Mon–Fri at
  **9:35, 10:05, 10:35, 11:05 AM ET** (friend's fired ~10:37–10:42 AM).
  Prompt: run `python3 momentum_calls.py --alert`; if `NO_ALERTS`, reply nothing.
- No new entries after Thursday 11 AM (no weekend holds).

## 4. Sim Integration — `sim.py` edits + weekly report

- `--step` logs each alert into `state["call_flags"]` (ticker, date, spot,
  strike, expiry, premium, break-even, confidence).
- Daily resolution (in `--step`, reuse chain fetch): fetch that call's mid;
  apply **TP +100% / SL −50% / time stop 7 DTE** — same rules as the plan.
- Weekly report section:
  `CALL FLAGS: N resolved | win rate X% | avg return Y%` + per-ticker splits.
- **LEVER 3 (go-live gate):** once ≥ 10 flags resolved, if win rate ≥ 55% **and**
  avg win / avg loss ≥ 1.5 → trade for real in IBKR, $100–150 max risk/trade,
  1–2 trades/wk (already fits the weekly options system).

## 5. Files & Phases

| Phase | Work | Effort | Status |
|---|---|---|---|
| 1 | `options_data.py` (chain fetch, expiry, regime, zscore) | half day | ✅ done 8/6 |
| 2 | `momentum_calls.py` scanner + confidence score; backtest vs TOST/PRGO/FSLY | half day | ✅ done 8/6 |
| 3 | `--alert` mode + Telegram cron + dedupe | half day | ✅ done 8/6 (4 sweeps 9:35/10:05/10:35/11:05 Mon–Fri; Thu cutoff 11 AM; dedupe in state.json call_flags) |
| 4 | sim call-flag logging + daily resolution + report section | half day | ✅ done 8/6 (step() resolves flags daily 4:15 PM via TP +100% / SL −50% / time stop 7 DTE / expired=intrinsic; report has CALL FLAGS section + LEVER 3 gate; also fixed latent missing `statistics` import in report) |
| 5 | Paper trade ≥ 10 flags (≈2–3 weeks), measure, then decide live | 2–3 wks | |

## 8. Phase 2 findings (8/6) — the friend's feed is STALE

Backtests revealed the friend's alerts quote **yesterday's close as "spot"** and fire
next morning (10:37–10:42 AM) on EOD signals:

- FSLY alert said spot $26.03 (8/5 close); the stock **gapped to $22.68** on 8/6 and
  was trading ~$23.20 when he bought the $26C at $0.91. That call is now ~$0.65–0.82
  (bid/mid), deep OTM, illiquid (OI 60 — our MIN_OI 500 gate rejects that strike).
- PRGO said spot $13.27 (8/5 close); stock faded 13.20 → 12.70. Call ~flat.
- TOST said spot $34.80 (8/5 close); stock held ~$35. Call ~flat.

Our EOD 8/5 backtest reproduces his feed (FSLY RSI 77 / Z +2.8σ / vol 2.5× — his: 76 / 4.0 / 2.9×;
confidence 0.60 with wide-spread warning). But our **live** scan at 10:42 on 8/6 fired nothing:
live RSI/Z/volume had already decayed (FSLY RSI 59, PRGO fading, today's volume a fraction of
8/5's). Conclusion: signal core matches; freshness is the difference. We trade live intraday
sweeps, never EOD-stale prices. Trend gate (px > SMA50 > SMA200) rejected TOST/PRGO (below
200-day MAs — bounce-off-lows, not continuations); FSLY passed and still gap-risked — overnight
gap risk is inherent to momentum, another reason for the 2-3% spec sizing.

Volume metric: our time-of-day-corrected relvol matches his at EOD (frac=1.0) but is stricter
intraday (his feed uses a burst/rate metric). Threshold 1.5× corrected; confidence carries the rest.

## 6. Risk Rules (baked in)
- Max 2 alerts/day, max 2 open sim call flags
- Naked long call = max loss is full premium — always defined risk
- Stops non-negotiable: SL −50%, time stop 7 DTE, no weekend holds
- Wide spread → limit order near mid or skip
- Live sizing: $100–150 risk, spec only, until LEVER 3 clears

## 7. Honest caveats
- Buying at RSI 70+ / Z +2.5σ+ is chasing; win rate is the only thing that
  justifies it. The PRGO fade (13.27 → 12.72 same day) is the base case, not
  the exception.
- Yahoo intraday chain data can lag; treat alerts as candidates, confirm the
  spread on the broker screen before paying.
- Backtest on the friend's 3 alerts is illustrative, not proof — Phase 5 is
  the real test.

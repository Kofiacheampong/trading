# COVERED CALLS (Buy-Write) PAPER SIM — LEVER 5

Status: **LIVE Aug 15, 2026** (Kofi greenlit after Corey Holiday video transcript review)
Spec: `trading_sim/covered_calls.py` — runs inside the daily 4:15 PM sim step + Saturday report.

## Why
Kofi can't write covered calls today (all real positions < 100 shares; cash $744).
This paper track tests *whether* buy-writes earn their keep BEFORE any share
rounding-up or new capital: does selling ~8% OTM monthly calls with the video's
filters beat plain hold, or is it capped growth?

## Universe (synthetic 100-share lots, paper only)
`MP, DRAM` (real holdings he'd round up) + `LULU, KMB, ZTS, PYPL, PAYC` (budget basket).

## Entry rules (every weekday step, one open cycle per ticker)
1. **Regime filter (Holiday lesson 4):** SKIP if SMA20 > SMA50 (confirmed uptrend).
   Sell calls only in flat/down regimes — never into the strongest upside periods.
2. **Premium floor:** SKIP if the ~8% OTM call yields < 1.0% of spot/month
   (not worth capping upside for pennies).
3. **Liquidity:** strike must have real bid+ask on the Yahoo chain.
4. Expiry: nearest listed with 21–45 DTE (target 30), strike = first liquid
   strike ≥ spot × 1.08.

## Settlement (at expiry, 100 sh)
- spot ≥ strike → `assigned`: P&L = (strike − entry) + premium, per share
- spot < strike → `kept`: P&L = (spot − entry) + premium
- Benchmark per cycle: plain 100-sh hold return over the same window.

## Gate (LEVER 5)
≥20 resolved cycles AND win rate ≥70% AND avg premium yield ≥1.0%/mo AND
sum(cycle ret) ≥ 0.8 × sum(hold ret) — the filter must dodge the big upside
months, otherwise covered calls are just capped growth.
Real-money application ONLY on names owned at 100+ shares.

## Known data issues (as of 8/15)
- MP: Yahoo chain fetch returns nothing (expiry/chain rows = 0) — retried daily;
  if persistent, MP won't qualify until data improves (which is itself a finding:
  no liquid chain = can't actually sell the call).
- TEAM/ABNB/ABCL stale flags (time-stops 8/13 passed, still open): Yahoo v7
  options endpoint is returning empty on weekends/rate-limit — they resolve on
  the next step with data, or settle at intrinsic on expiry. No code bug.

## First dry-run (8/15, real quotes)
Filter already working: LULU, KMB, PYPL, PAYC SKIPPED (SMA20>50 uptrend).
DRAM $62C exp 9/11 @ $2.49 (4.34%/mo) and ZTS $80C exp 9/18 @ $1.13 (1.52%/mo)
would open Monday. DRAM is the live test of the video's own warning: the ETF is
in a strong rally but SMA20 hasn't crossed SMA50 yet — the filter lets it through.

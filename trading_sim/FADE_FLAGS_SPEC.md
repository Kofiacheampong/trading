# FADE-THE-FLAG PAPER SIM — LEVER 3C

Status: **LIVE Aug 16, 2026** (Kofi greenlit after NetPicks 8-Minute Options Cookbook review)
Spec: `trading_sim/fade_flags.py` — runs inside the daily 4:15 PM sim step + Saturday report.

## Why
The momentum scanner flags stocks at overbought extremes (RSI>=70, Z>=2.5 sigma)
and paper-trades LONG calls (momentum following). The NetPicks cookbook argues
the opposite: extremes are mean-reverting, so sell CALL CREDIT SPREADS into them.
This track puts BOTH sides of the same signal in the sim — same trigger, opposite
trade — and one gate decides which philosophy wins in the current regime.
(OR-fade backtest 8/11 already hints fades win: shorts 85% WR vs longs 53%.)

## Trigger
Every momentum call flag dated >= 2026-08-16 (no retro data — existing 8/11 TEAM
and 8/13 DRAM flags are excluded by design). Fade opens automatically for the
flag's ticker with the SAME expiry and SAME time-stop as the flag — a fair
same-window fight.

## Trade construction (paper)
- Short strike: first liquid strike >= flag spot x 1.05 (5% OTM)
- Long strike: next listed strike above the short strike
- Credit = short mid - long mid; must be > 0
- Expiry + time-stop: identical to the momentum flag's

## Exits (mirror momentum flag lifecycle)
- TP: buy back when spread cost <= 50% of collected credit (keep >=50% of max profit)
- SL: cut when cost >= 2x credit
- Time stop: exit at market on flag's time-stop date
- Expired: settle at intrinsic (max(spot-k_short,0) - max(spot-k_long,0))
- ret = (credit - cost) / credit * 100

## Gate (LEVER 3C)
>=10 resolved fades AND win rate >=55% AND avg win / avg loss >= 1.5.
Report shows head-to-head: fade ret vs momentum ret on matched flags.

## Verified (8/16)
- Module imports clean; sim.py wired (step + report).
- Spread-pick tested on live ZTS chain: 80/85C, credit $0.675 (vs covered-call
  sim's ZTS $80C 9/18 @ $1.13 — same chain, different legs; no conflict).
- Existing flags (pre-8/16) correctly get NO fades. First fades open when a new
  scanner flag lands (Monday 9:35 AM sweep or later).

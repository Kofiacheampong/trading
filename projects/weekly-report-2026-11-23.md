# Weeklies Report — Week of Nov 23, 2026

Account: $400 IBKR | Strategy: bull call spreads
Data: Fri 11/20/2026 close | Built: Sun 11/22/2026 23:00 UTC

## Market context
Broad risk-off washout Friday — high-beta sub-$50 names got hit hard:
SOFI -7.4%, RIOT -7.7%, HIMS -8.3%, RIVN -8.3%, LI -7.2%, SYM -7.3%, CLSK -15.7%, BILI -5.1%, TCOM -3.5%.
**Thanksgiving week**: Thu 11/26 closed, Fri 11/27 half-day (1pm ET). Only ~3.5 trading days on the 11/27 expiry.

## Picks

### TOP — HPQ $27.96 | ER Tue 11/24 BMO
11/27 30/33C. Long ask 0.71 (OI 3429), short bid 0.08 (OI 3106).
Cost $63 | Max $237 (+276%) | B/E 30.63 (+9.5%) | full max at 33 (+18.0%)
Only true earnings catalyst in the window with a tradeable weekly chain. IV 93-97%, options pricing ±7-8% move. Lottery-shaped but defined risk.

### RUNNER-UP — SOFI $12.48 | no dated catalyst
11/27 12/14C. Long ask 0.53 (OI 326, vol 2236), short bid 0.12 (OI 659).
Cost $41 | Max $159 (+288%) | B/E 12.41 (-0.6%, BELOW spot) | max at 14 (+12.2%)
Best structure on the board — breakeven under current price, tightest chain (6% wide long leg). Profits on a flat tape.

### WILDCARD — MARA $5.09 | BTC proxy
12/04 5/6.5C. Long ask 0.58 (OI 674), short bid 0.11 (OI 1800).
Cost $47 | Max $103 (+119%) | B/E 5.47 (+7.5%) | max at 6.5 (+27.7%)
2% bid/ask on the 5C — cleanest fills of anything scanned. 12/04 avoids Thanksgiving decay.

## Full scan
```
HPQ    $27.96  11/27 30/33C   $63  -> $237   276%  B/E 30.63  need +9.5%   ER 11/24
SOFI   $12.48  11/27 12/14C   $41  -> $159   288%  B/E 12.41  need -0.6%   no catalyst
MARA   $ 5.09  12/04 5/6.5C   $47  -> $103   119%  B/E  5.47  need +7.5%   BTC
RIOT   $16.23  11/27 16/18C   $61  -> $139   128%  B/E 16.96  need +4.5%   no ER
HIMS   $14.60  11/27 15/17C   $53  -> $147   177%  B/E 15.53  need +6.4%   no ER
RIVN   $10.33  12/04 11/13C   $33  -> $167   406%  B/E 11.33  need +9.7%   thin long leg
CHWY   $19.50  12/04 20/21.5C $68  -> $ 82   121%  B/E 20.68  need +6.1%   no ER this wk
```

## Excluded (liquidity kills the trade)
- **KSS** $22.25, ER 11/24, IV 145-165% — 40-60% bid/ask on every strike. Unfillable.
- **SYM** $31.10, ER 11/23 — 50-70% wide. Chain is a ghost town (OI 0-30 at the money).
- **TCOM** $40.52, ER 11/23 — Dec 18 only, no weeklies. $140 for $160 max.
- **LI** $10.39, ER 11/25 — near-money strikes have OI 0-1.
- **BILI** $10.60, ER 11/24 — Dec 18 only, OI under 80.
- **KSS/AMTM/CMBT/AEXA/VIPS/BZ** — no tradeable two-sided market.

## Notes / rule decisions
- SOXS now far above the $50 cap (was $52 in Oct). Dropped from scans.
- Sub-$50 small caps with weeklies almost always have 15-40% bid/ask spreads. Paying ask / selling bid (what this scan does) is the honest number; the "mid" fill would look 20-50% better and is not realistic.

Script: `projects/weeklies-scan.py`, `projects/scan2.py`

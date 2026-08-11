# Trading Sim — Kofi's paper-trading bot

Forward-testing simulator for the budget watchlist (LULU, KMB, ZTS, PYPL, PAYC)
plus a quality-extras opportunity scanner (QCOM, ADBE, IT, PNR).

## Strategies
1. **Dip-buy**: buys ~$120 notional when price ≤ threshold (LULU 112 / KMB 103 / ZTS 73 / PYPL 53 / PAYC 152).
   Exits: +6% take profit, -6% stop, or 15 trading days.
2. **Weekly put sim**: sells a ~10% OTM put at the next listed expiry (real credit from Yahoo options API,
   fallback 1.2% of strike). Resolves on expiry day vs close. This is the "lever for weeklys" — win rate
   per ticker after a month tells us which names to actually sell weeklies on.
3. **Opportunity scanner** (`opportunity.py`): the "intuitive" eye. Every daily step it scores the universe
   on technicals — % below 200-day MA, RSI(14), distance from 52-week low, RSI reversal, volume surges,
   breakouts — weighted by each name's ROIC (a cheap 27% ROIC business is an opportunity; a cheap 9% one
   is a trap). Flags score ≥ 40 get logged with price/date. Flags are judged after 3+ days:
   +5% = bounce (good flag), -8% = dud (bad flag).

## Usage
- `python3 sim.py --step`   — daily step (buy/sell/resolve/scan). Cron: weekdays 16:15 ET.
- `python3 sim.py --report` — weekly stats incl. scanner scorecard. Cron: Saturday 10:00 ET.
- `python3 opportunity.py`  — standalone: just show today's top setups.
- `python3 lottery_demo.py` — **standalone experiment** (does NOT touch sim logic): opens ONE cheap
  OTM weekly call at real ask prices (stored under `state.json["lottery"]`, ignored by sim.py) and
  values it each run. Purpose: show what a "lottery-ticket" earnings/momentum call actually does
  before real money is on the line. `--reset` deletes the demo position.

## State
- `state.json` — cash ($1,500 start), open positions, closed trades, put log, opportunity flags.
- Trades are logged with real market closes; no API key needed. Prices: Yahoo v8 chart. Options:
  **Cboe delayed quotes** (cdn.cboe.com, official exchange, free, no key) primary for the lottery demo,
  and used as the put-credit fallback in sim.py when the Yahoo options endpoint is throttled or a
  strike interval doesn't match (ZTS/KMB have $5 strikes; the sim rounds to $2.5).

## Lever rules (from report)
- Put win rate > 75% on a ticker → real weekly put selling has empirical backing.
- < 60% → skip or widen strike.
- **Lever 2:** if a ticker's opportunity flags bounce ≥ 70% of the time, its oversold
  flags are a green light to sell puts that week (bot intuition → real trade).

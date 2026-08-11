# Episode 01 — "I Backtested 60 Days of S&P Futures. Breakouts Lost. Fading Won."

**Length:** ~9 min · **Format:** faceless VO + charts + screen recordings
**Tone:** direct, curious, honest — no guru energy, numbers do the talking

---

## HOOK (0:00-0:35)

[VISUAL: Split screen. Left: big red "-$4,162 BREAKOUT". Right: big green "+$3,429 FADE".
Both on a simple candlestick background. VO starts over the numbers.]

Every trading video on this platform will tell you to trade breakouts.
Buy the breakout, ride the trend, that's where the money is.

So I did the opposite of trusting them. I took 60 days of real S&P 500 futures data —
thirteen thousand five-minute bars, fifty trading days — and I backtested the most
popular strategy on YouTube: the opening range breakout.

It lost. In every variation. Between thirteen hundred and four thousand dollars.

Then I flipped it. I faded the opening range instead — bought the breakdowns, shorted
the breakouts. Same data, same 60 days. Forty-five trades, seventy-one percent win rate,
plus three thousand four hundred dollars.

And here's the part that changed how I think about the market forever:
the short side carried the entire edge. Eighty-five percent win rate shorting strength.
Fifty-three percent buying weakness. Almost break-even.

The strategy everyone sells you — losing. The trade everyone's afraid of — the only
thing working. That's today's video. I'm going to show you the exact data, the exact
rules, and the exact mistakes I made before I trusted any of it.

[VISUAL: Channel intro card — just text: "SMALL ACCOUNT SYSTEMS" + subscribe CTA.]

---

## WHAT THE OPENING RANGE IS (0:35-1:45)

[VISUAL: ES 5-min chart, draw the 9:30-10:00 box — high and low lines, shaded box.]

First, the setup. The opening range is simple: the first thirty minutes of the US
session — 9:30 to 10:00 AM Eastern — mark a high and a low. That box is the market
telling you where it thinks fair value is for the day.

The breakout trade: when price closes above the top of that box, you go long.
It breaks below, you go short. The idea is momentum — the market picking a direction
and running with it. It's the single most recommended intraday strategy on the internet.

Here's what most people never check: does it actually work? Not in a good year.
Not in a trending month. Right now, in this market.

[VISUAL: The regime stats: median opening range 31.6 points, ~0.4% of the index.
SPX at record highs, big daily ranges.]

Because context matters. I ran this in mid-2026 — the index is at record highs,
daily ranges are fat, the median opening range over those sixty days was thirty-one
points. That's a wild tape. Breakouts in a wild, range-bound tape get chopped.

But I didn't want to guess. I wanted the receipts.

---

## THE METHOD (1:45-3:15)

[VISUAL: Screen recording of the actual backtest script running. Terminal output scrolling.
Keep it fast, 15 seconds of footage.]

Here's the method, and I'll show you the code because hiding your methodology is how
you lie to yourself. Sixty days of five-minute bars from the front-month E-mini
contract. Fifty trading days with a complete opening range.

Rule one: no lookahead. The entry decision only uses bars up to that second — the
replay is chronological. Rule two: I test everything on the micro contract, MES —
five dollars per point — because that's what a small account can actually trade.
Rule three: every trade has a hard stop and a hard target. This isn't a "trust me,
I'll manage it" strategy. It's mechanical.

Breakout version: first close above the range high, go long. First close below the
range low, go short. Entry window ten to eleven-thirty AM. Stop and target at fixed
points, flat by 3:50 PM every day. No overnight risk, ever.

Then the fade version: the exact mirror. First close below the range low — that's the
breakdown — you fade it, you go long. First close above the range high — the breakout —
you fade it, you short. Same stop, same target, same flat-by-close rule.

Same data. Same risk. Opposite direction. That's the whole experiment.

---

## THE RESULTS (3:15-5:15)

[VISUAL: Results table builds on screen. Breakout row red, fade row green.]

Here's what fifty trading days said.

Opening range breakout, four different parameter sets: win rate between ten and
twenty-seven percent. Net result: negative thirteen hundred to negative forty-one
hundred dollars. Three take-profits hit. Thirty-seven stops. Breakout trades got
run over, almost every time. This market does not let you buy the pop and keep it.

Now flip it. The fade. Forty-five trades — almost one per day. Seventy-one percent
win rate. Thirty-one take-profits against thirteen stops and one time exit.
Net: plus three thousand four hundred twenty-nine dollars. Max drawdown, eight
point one percent.

[VISUAL: Pie/bar split: LONG bucket 19 trades 53% WR vs SHORT bucket 26 trades 85% WR.
Make this the big visual — it's the money shot.]

But here's where I almost made the classic mistake. I almost looked at the combined
seventy-one percent and called it a day. Then I split the trades into two buckets —
longs and shorts — because I wanted to know which half was actually earning.

The longs: nineteen trades, fifty-three percent win rate. Basically a coin flip.
The shorts: twenty-six trades, eighty-five percent win rate. That's not luck.
That's a market telling you something.

Fading strength worked. Fading weakness barely did. In this tape, the crowd buys
the breakout — and the crowd is the exit liquidity.

---

## THE HONEST PART (5:15-7:00)

[VISUAL: Text card: "60 days ≠ proof". Then the caveat list.]

Now the part every guru skips, because it costs them the fantasy.

Sixty days is one regime. This worked in a market that chops. Put this same strategy
in a straight-line trending market and the fade gets run over — you'd be shorting
every breakout that keeps going. The win rate you just saw is not a permanent law.

Second: fills are close-based, not tick-based. I modeled entries on bar closes.
Real execution has slippage — on the micro contract that's maybe one or two ticks,
not nothing, but not fatal.

Third, and this one's subtle: the risk-reward is razor-thin. Average win was a hundred
forty-eight dollars, average loss exactly a hundred. That's a one-point-four-eight
ratio — and my own gate requires one-point-five. The strategy passed by the skin
of its teeth, and only because time-exits didn't drag it below.

So what do you do with a backtest that's good but not bulletproof?

[VISUAL: The gate graphic — a simple checklist.]

You don't deposit money. You paper-trade it forward. Same rules, real-time data,
and you let the win rate and the drawdown prove themselves over forty-plus trades
before a single real dollar touches it. That's the system I run everything through:
backtest, paper, gate, live. In that order. Skipping steps is how small accounts
die.

---

## THE LESSON (7:00-8:15)

[VISUAL: Simple text slides as each point lands.]

Three things this experiment taught me that I'd pay for again.

One: trade the market you're in, not the market you wish existed. Every course you've
ever seen was built in some other tape. The data from the last sixty days is the
only data that pays you.

Two: track your sides separately. If I'd looked at the combined number I'd have
thought "great strategy, seventy-one percent." I'd have gone live and let the
fifty-three-percent long side bleed the book while the shorts quietly carried it.
One side can hide the other. Always split the ledger.

Three: the contrarian side is where the edge lives. In a market where everyone's
conditioned to buy breakouts — retail, algorithms, all of it — the short side of
the same move is the orphan trade. And orphans are underpriced.

That last one's uncomfortable. It means your edge is usually on the side of the
trade your gut hates. Get comfortable with it.

---

## OUTRO (8:15-9:00)

[VISUAL: The sim report header. Subscribe + bell.]

I'm now paper-trading this fade strategy forward with the exact rules you just saw —
and I publish the results weekly, wins and losses, no cherry-picking. If the edge
dies in live paper trading, you'll see it die right here in the data.

If you want to see whether the fade holds up — or whether the market regime flips
and kills it — subscribe. The report drops every Saturday.

Next episode: I'm breaking down why the same principle — fade the crowd — is why I
don't buy momentum call alerts, even when they're right. See you in the data.

---

## Production notes

**Title options:**
- "I Backtested 60 Days of S&P Futures. Breakouts Lost $4,000. Fading Won $3,400."
- "The Opening Range Strategy Everyone Gets Wrong (60 Days of Data)"
- "Shorts Carried the Edge: 60 Days of Intraday S&P Futures Data"

**Thumbnail:** split-screen red/green — "BREAKOUT −$4,162" vs "FADE +$3,429", ES chart behind,
3-4 words max.

**Visuals needed:** ES 5-min chart with opening-range box (TradingView), terminal recording
of `mes_intraday.py --backtest`, results table, long/short bucket split, gate checklist.

**VO:** own voice or ElevenLabs. If AI voice: warm, measured, no sing-song — the numbers
carry it.

**Description:** the method summary + "data from /trading_sim/mes_intraday.py, 60 days,
13,729 5-min bars" + weekly sim report teaser + subscribe CTA.

**Tags:** s&p futures, opening range, ORB, day trading data, mean reversion, MES,
small account, paper trading, trading backtest

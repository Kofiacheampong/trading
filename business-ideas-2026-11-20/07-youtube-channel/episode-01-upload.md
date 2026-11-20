# Episode 01 — Upload Package (ready to publish)

## 📋 TITLE (pick one)
1. "I Backtested 60 Days of S&P Futures. Breakouts Lost $4,000. Fading Won $3,400."
2. "The Opening Range Strategy Everyone Gets Wrong (60 Days of Data)"
3. "Shorts Carried the Edge: 60 Days of Intraday S&P Futures Data"

## 🖼️ THUMBNAIL
- 1280x720, high contrast. Split screen: left half red "BREAKOUT −$4,162", right half green "FADE +$3,429"
- Background: ES candlestick chart (screenshot from TradingView, dark theme)
- Max 4 words total besides the numbers. Big bold font (Canva free: Montserrat/Bebas Neue)

## 📝 DESCRIPTION (paste as-is)

I backtested 60 days of S&P 500 futures data — 13,729 five-minute bars — to test the most popular intraday strategy on YouTube: the opening range breakout. It lost in every variation. Then I flipped it and faded the range instead: 45 trades, 71% win rate, +$3,429. And the short side carried the entire edge.

⏱️ CHAPTERS
0:00 The numbers that started this
0:35 What the opening range is
1:45 The method (code included)
3:15 The results
5:15 The honest caveats
7:00 Three lessons
8:15 What happens next

📊 THE DATA
- 60 days, 13,729 five-minute bars, 50 trading days (front-month E-mini S&P 500)
- Opening range breakout (ORB), 4 variants: 10–27% win rate, −$1,300 to −$4,162
- Range fade (mean reversion): 45 trades, 71% WR, +$3,429, max drawdown 8.1%
- Longs: 19 trades, 53% WR | Shorts: 26 trades, 85% WR ← the whole story
- Exits: 31 take-profits, 13 stops, 1 time exit
- Micro E-mini (MES), $5/point, TP +30 pts / SL −20 pts, flat by 3:50 PM daily
- No lookahead — entries use only bars up to the decision point
- Backtest: python3 mes_intraday.py --backtest

⚠️ NOT FINANCIAL ADVICE. I'm tracking this strategy forward in a paper sim and publishing the results weekly — wins and losses, no cherry-picking. 60 days is one regime; it can and may fail when the market changes.

🔔 Subscribe — sim report every Saturday.

## 🏷️ TAGS
s&p futures, opening range, ORB, day trading, futures trading, mean reversion, MES, micro e-mini, trading backtest, paper trading, small account, intraday strategy, trading data, es futures, fade the breakout

## ⚙️ UPLOAD CHECKLIST (in order)
1. [ ] Upload video (1080p, MP4). Title from list above. Thumbnail attached.
2. [ ] Paste description. Category: Education. Language: English. Not "made for kids."
3. [ ] Tags pasted. Add "sp500", "trading" to the 500-char limit.
4. [ ] Chapters: description timestamps auto-detect — verify chapter markers show.
5. [ ] End screen (last 5-20s): Subscribe button + Next Video placeholder.
6. [ ] Card (optional): link to the sim repo on GitHub (private — skip or use public blog later).
7. [ ] Visibility: Schedule for Tuesday or Thursday, 8–9 AM ET (finance audience morning scroll). First video: schedule is fine — gives you time to fix issues.
8. [ ] Allow embedding ON, notify subscribers ON, comments ON.
9. [ ] Upload as UNLISTED first (if paranoid): review yourself, then flip to public at the scheduled time.

## 🚀 FIRST 48 HOURS
- [ ] Pin a comment: "Data from my paper sim — full report drops every Saturday. Questions welcome."
- [ ] Reply to every comment for the first 48h (algorithm + community).
- [ ] Share once, in 1-2 places max (not spam): one trading community you're genuinely active in.
- [ ] Watch CTR (aim >4-5%) and retention (aim >40-45% at the 1-min mark). If CTR low → thumbnail/title swap. If retention dies early → hook or pacing.
- [ ] Don't buy ads, don't buy subs. Ever.

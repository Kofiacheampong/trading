# 📊 TradingView Chart Setup — Episode 01 (copy-paste)

## Chart settings (set once, save as layout)

| Setting | Value |
|---|---|
| Symbol | **ES1!** (continuous E-mini S&P 500 futures) |
| Timeframe | **5-minute** |
| Timezone | **America/New_York** (exchange time — the 9:30-10:00 box MUST be ET) |
| Session | **RTH / Regular** — hide overnight Globex bars so the video is clean |
| Theme | Dark |
| Candles | Default green/red (or your preference — keep high contrast) |
| Volume pane | On, below the chart (subtle, small height) |

How to hide overnight: Chart settings (gear icon) → Trading session → "Regular" (RTH), or the clock icon in the toolbar → choose session. If your plan limits it, just zoom the chart to 9:30–16:00 ET and let the box tell the story.

## The one drawing you need

- **Rectangle tool** (toolbar, or hotkey: press R)
- Draw from **9:30** to **10:00** ET horizontally; vertically from the session's high to low in that window
- Style: fill OFF (or very faint), border 2px, white/yellow — it must read on camera
- This box IS the strategy. Show it on every day you record.

## Which days to record (from the actual backtest log — all within the last 2 weeks)

| Purpose | Date | What happened | Script section |
|---|---|---|---|
| Fade works (short) | **Thu Jul 30** | Short @ 7440 → +$150 TP | Results / money shot |
| Fade works (long) | **Fri Jul 31** | Long @ 7454 → +$150 TP | Results |
| Fade works (short) | **Thu Aug 6** | Short @ 7765 → +$150 TP | Results |
| Fade FAILS (honesty) | **Wed Aug 5** | Long @ 7791 → −$100 SL (trend day) | Caveats — shows it's not magic |
| Grind / time exit | **Mon Aug 10** | Short @ 7787 → +$78 time exit | Method / exit rules |

For each day: scroll so 9:00–12:00 ET fills the frame, draw the box, narrate later (VO), keep the mouse still while the chart tells the story.

## Recording flow per day (OBS)

1. Frame the chart (9:00–12:00 ET), clean browser, no notifications.
2. Draw the 9:30–10:00 rectangle slowly (it's a teachable moment).
3. Press play on the chart animation (or slowly drag through) to show price leaving the range.
4. 20–40 seconds per day. 3-4 days total. Done.

## Optional extra (strong visual)

- Terminal: `cd ~/clawd/trading_sim && python3 mes_intraday.py --backtest`
- OBS-record the scrolling output 15-30s — the "transparency" moment.
- Canva: results table + long/short split graphic (export PNG).

## Notes

- TradingView menu names may vary slightly by version — core tools (rectangle, session, timezone) are stable.
- Free plan intraday history covers ~2 months at 5m — all the dates above are within range.
- If a date doesn't load, any day from the trade log works; the story is the same.

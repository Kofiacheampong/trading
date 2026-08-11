# 🎙️ Recording Guide — Episode 01 (faceless)

**The one principle that saves you hours:** AUDIO FIRST, VISUALS SECOND.
Record the voiceover reading the script, then lay visuals on top of the audio track.
Matching video to existing audio is 10x easier than the reverse.

## Step 1 — Voiceover (45-60 min)

- **Option A (recommended): your own voice.** Quiet room. Phone with earbuds, or a $30-50 USB mic. Read the script naturally — 2-3 takes per section, pick the best. Don't perform; talk like you're explaining to a friend.
- **Option B: AI voice.** ElevenLabs free tier (~10 min/mo = one video). Pick a natural voice. MUST disclose "altered/synthetic content" in YouTube upload settings (their AI policy).
- Record each script section as its own file: hook / explainer / method / results / caveats / lessons / outro. Makes editing painless.
- Script is ~1,400 words ≈ 9 min at 150 wpm. On pace.

## Step 2 — Screen recordings (30-45 min)

Use OBS Studio (free): 1080p, 30 fps is fine.

Segments needed for ep01:
1. **TradingView** (free account) — ES 5-min chart, dark theme:
   - Draw the 9:30-10:00 AM opening range box (rectangle tool) — 20-40s
   - Show a day where a breakout got chopped (range box + price slicing through) — 20-40s
   - Show a day where the fade worked — 20-40s
   - Clean mouse movement, no frantic cursor, no notifications
2. **Terminal** — run `python3 mes_intraday.py --backtest` in `/home/kofi/clawd/trading_sim` — the scrolling output IS the money shot. 15-30s.
3. **Canva slides** — results table, long/short split (the money shot), gate checklist. Export as PNG, animate in CapCut.

## Step 3 — Edit (2-4 hrs first time)

- **CapCut** (free). Import VO track FIRST. Cut visuals to the audio sections.
- Big text overlays for the numbers (most viewers watch muted at first).
- Subtle zoom on charts; background music from YouTube Audio Library at -25dB ("minimal/corporate" search).
- Auto-captions, styled large.
- Export 1080p MP4 → follow `episode-01-upload.md` checklist.

## Step 4 — Thumbnail + upload

Canva per the thumbnail spec in the upload package. Then the upload checklist. Done.

## 🚫 What NOT to record

- Your face, your real name, your **real broker account**, real money positions. NEVER.
- Sim data = fine (it's paper). Real IBKR account = privacy risk, and it exposes live strategy details.
- No "guaranteed returns" / financial-advice language — the script's disclaimer covers the legal basics.
- AI voice must be disclosed in upload settings if you go that route.

## ⏱️ Time budget

- First video: 6-10 hrs total (script + upload package are already done — the hard part's behind you)
- Subsequent videos: 4-6 hrs once you have templates

## 📁 File plan

```
youtube/ep01/
  vo/        (voiceover sections)
  screens/   (OBS recordings)
  slides/    (Canva exports)
  export/    (final MP4)
```

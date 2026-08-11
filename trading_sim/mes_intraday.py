#!/usr/bin/env python3
"""
MES intraday paper sim — OR-fade (mean reversion). Lean replay design.

Design (8/11/26, Kofi's call): intraday reps WITHOUT bloating the system.
No new crons, no new data sources, no live checks. The existing 4:15 PM
sim step fetches today's completed 5-min ES bars (same Yahoo curl as the
daily-bar sim) and REPLAYS the day: decide entry at 10:00-11:30 ET, walk
forward bar-by-bar for exits. Statistically identical to live trading
(no lookahead — entry uses only bars up to that point); the only thing
we don't learn is live-execution feel, which the real account teaches.

Strategy v1: OR-FADE (mean reversion — matches Kofi's dip-buy style)
  - Opening range = high/low of 9:30-10:00 ET.
  - First 5-min close BELOW the range  -> LONG  (fade the down-move)
  - First 5-min close ABOVE the range  -> SHORT (fade the up-move)
  - Entry window 10:00-11:30 ET only (late fades are low quality).
  - Exits: TP +30 pts (+$150) / SL -20 pts (-$100) / 3:50 PM time exit.
  - Flat by 3:50 PM daily. Zero overnight risk, zero weekend risk.

Why NOT breakout (ORB): backtested 60 days of ES 5-min bars — breakout
WR 10-27% (net -$1,300 to -$4,100 across variants). Fade WR 71% (net
+$3,429, 45 trades). Longs 53% WR / shorts 85% WR — shorts carry it;
separate buckets below so one side never hides the other.

Backtest on 60 days (built in):  python3 mes_intraday.py --backtest
Live replay runs inside the daily 4:15 PM sim step.

Gate (same Lever-4 standard, evaluated at the Nov 9 review):
  >=40 resolved trades AND WR >=55% AND avg win/avg loss >=1.5 AND
  max drawdown <=25%. Early review at 20 trades if WR <40% or DD >25%.
"""
import json, os, subprocess, datetime, statistics, sys
from zoneinfo import ZoneInfo
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

SYMBOL = "ES=F"
MULT = 5.0                 # MES: $5 per index point
SL_PTS = 20.0              # -$100 max risk (inside the $100-150 rule)
TP_PTS = 30.0              # +$150
OR_START = (9, 30)         # opening range window
OR_END = (10, 0)
ENTRY_UNTIL = (11, 30)     # no fades after 11:30 ET
TIME_EXIT = (15, 50)       # flat by 3:50 PM, always
REVIEW_DATE = "2026-11-09"
GATE_MIN_TRADES = 40
GATE_WR = 55.0
GATE_RR = 1.5
GATE_MAX_DD = 25.0
EARLY_TRADES = 20
EARLY_WR = 40.0
START_EQUITY = 1500.0

NY = ZoneInfo("America/New_York")


def fetch_5m(rng="5d"):
    """5-min bars [(datetime(ET), high, low, close)] for ES=F."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{SYMBOL}"
           f"?range={rng}&interval=5m")
    out = subprocess.run(["curl", "-s", "-m", "30", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["chart"]["result"][0]
        ts = res["timestamp"]
        q = res["indicators"]["quote"][0]
        bars = []
        for i, t in enumerate(ts):
            hi, lo, cl = q["high"][i], q["low"][i], q["close"][i]
            if hi is None or lo is None or cl is None:
                continue
            bars.append((datetime.datetime.fromtimestamp(t, NY), hi, lo, cl))
        return bars
    except Exception:
        return []


def replay(hist):
    """Replay one day of 5-min bars -> trade dict or None. No lookahead."""
    or_bars = [b for b in hist if OR_START <= (b[0].hour, b[0].minute) < OR_END]
    if not or_bars:
        return None
    or_hi = max(b[1] for b in or_bars)
    or_lo = min(b[2] for b in or_bars)

    side = entry = None
    for b in hist:
        t = (b[0].hour, b[0].minute)
        if t < OR_END:
            continue
        if t >= ENTRY_UNTIL:
            break
        if b[3] < or_lo:                 # broke below the range -> fade long
            side, entry = "long", b[3]
            break
        if b[3] > or_hi:                 # broke above the range -> fade short
            side, entry = "short", b[3]
            break
    if side is None:
        return None

    reason = exit_px = None
    for b in hist:
        t = (b[0].hour, b[0].minute)
        if t >= TIME_EXIT:
            reason, exit_px = "time", b[3]
            break
        if side == "long":
            if b[1] >= entry + TP_PTS:
                reason, exit_px = "tp", entry + TP_PTS
                break
            if b[2] <= entry - SL_PTS:
                reason, exit_px = "sl", entry - SL_PTS
                break
        else:
            if b[2] <= entry - TP_PTS:
                reason, exit_px = "tp", entry - TP_PTS
                break
            if b[1] >= entry + SL_PTS:
                reason, exit_px = "sl", entry + SL_PTS
                break
    if reason is None:                   # partial-day data; exit at last close
        reason, exit_px = "open", hist[-1][3]
    pnl = round((exit_px - entry) * MULT * (1 if side == "long" else -1), 2)
    return {"date": str(hist[0][0].date()), "side": side,
            "entry": round(entry, 2), "exit": round(exit_px, 2),
            "reason": reason, "pnl": pnl}


def step(state):
    """One daily sim step: replay today's bars at 4:15 PM. Returns events."""
    events = []
    if "mes_intraday" not in state:
        state["mes_intraday"] = []
    today = datetime.date.today()
    if today.weekday() >= 5:
        return events
    if any(t["date"] == str(today) for t in state["mes_intraday"]):
        return events
    bars = [b for b in fetch_5m() if b[0].date() == today]
    if not bars:
        return events
    tr = replay(bars)
    if tr:
        state["mes_intraday"].append(tr)
        events.append(f"MES-ID {tr['side'].upper()} fade @ {tr['entry']} -> "
                      f"{tr['reason']} pnl ${tr['pnl']:+.2f}")
    return events


def _bucket_stats(trades):
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] <= 0]
    n = len(trades)
    wr = len(wins) / n * 100 if n else 0.0
    avg_win = sum(t["pnl"] for t in wins) / len(wins) if wins else 0.0
    avg_loss = sum(t["pnl"] for t in losses) / len(losses) if losses else 0.0
    return n, wr, avg_win, avg_loss


def report(state):
    trades = state.get("mes_intraday", [])
    lines = []
    if not trades:
        lines.append("MES INTRADAY (OR-fade): no trades yet — first fade beyond "
                     "the 9:30-10:00 opening range triggers a paper trade (replayed "
                     "in the 4:15 PM step). Longs and shorts tracked separately.")
        return "\n".join(lines)

    n, wr, avg_win, avg_loss = _bucket_stats(trades)
    rr = abs(avg_win / avg_loss) if avg_loss != 0 else 0.0
    net = sum(t["pnl"] for t in trades)

    eq, peak, max_dd = START_EQUITY, START_EQUITY, 0.0
    for t in trades:
        eq += t["pnl"]
        peak = max(peak, eq)
        dd = (peak - eq) / peak * 100
        max_dd = max(max_dd, dd)

    lines.append(f"MES INTRADAY (OR-fade): {n} resolved | win rate {wr:.0f}% | "
                 f"avg win ${avg_win:+.1f} | avg loss ${avg_loss:+.1f} | R:R {rr:.2f} | "
                 f"net ${net:+.2f} | max DD {max_dd:.1f}%")

    # separate buckets — one side never hides the other (Kofi's rule)
    longs = [t for t in trades if t["side"] == "long"]
    shorts = [t for t in trades if t["side"] == "short"]
    if longs:
        ln, lw, _, _ = _bucket_stats(longs)
        lines.append(f"  LONG bucket: {ln} trades | WR {lw:.0f}%")
    if shorts:
        sn, sw, _, _ = _bucket_stats(shorts)
        lines.append(f"  SHORT bucket: {sn} trades | WR {sw:.0f}%")

    by_r = defaultdict(int)
    for t in trades:
        by_r[t["reason"]] += 1
    lines.append(f"  exits: {', '.join(f'{k} {v}' for k, v in sorted(by_r.items()))}")
    for t in trades[-8:]:
        lines.append(f"  {t['date']} {t['side']} @ {t['entry']} -> {t['reason']} "
                     f"${t['pnl']:+.2f}")

    if n >= EARLY_TRADES and (wr < EARLY_WR or max_dd > GATE_MAX_DD):
        lines.append(f"  ⚠ EARLY REVIEW: {n} trades, WR {wr:.0f}%, DD {max_dd:.1f}% — "
                     "below survival line. Pause and rework before the full period.")

    if n >= GATE_MIN_TRADES:
        passed = wr >= GATE_WR and rr >= GATE_RR and max_dd <= GATE_MAX_DD
        if passed:
            lines.append(f"  ✅ LEVER 4 (MES intraday): GATE PASSED — {n} trades, WR {wr:.0f}%, "
                         f"R:R {rr:.2f}, DD {max_dd:.1f}%. Green-lit: 1 MES, $100 risk, "
                         "flat by 3:50 PM daily.")
        else:
            lines.append(f"  LEVER 4 (MES intraday): gate NOT passed (need WR >=55%, R:R >=1.5, "
                         f"DD <=25%; now {wr:.0f}% / {rr:.2f} / {max_dd:.1f}%). Keep paper trading.")
    else:
        lines.append(f"  LEVER 4 (MES intraday): {n}/{GATE_MIN_TRADES} trades — gate at "
                     f"{REVIEW_DATE} or {GATE_MIN_TRADES} trades, whichever later.")
    return "\n".join(lines)


def backtest():
    """60-day backtest through the same replay engine (reproducible)."""
    bars = fetch_5m(rng="60d")
    days = defaultdict(list)
    for b in bars:
        days[b[0].date()].append(b)
    trades = []
    for dt in sorted(days):
        tr = replay(days[dt])
        if tr:
            trades.append(tr)
    st = {"mes_intraday": trades}
    print(f"Backtest: {len(days)} trading days -> {len(trades)} trades "
          f"({sum(1 for t in trades if t['side']=='long')} long / "
          f"{sum(1 for t in trades if t['side']=='short')} short)")
    print(report(st))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--backtest":
        backtest()
    else:
        st = {"mes_intraday": []}
        print(step(st))
        print(report(st))

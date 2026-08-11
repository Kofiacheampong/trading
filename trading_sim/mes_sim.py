#!/usr/bin/env python3
"""
MES (Micro E-mini S&P 500) paper-trading module — extended paper period.

Strategy v1 (default): LONG-ONLY MEAN REVERSION on daily bars.
  - Buy 1 MES when ES (front-month) closes >=2% below its 20-day SMA
    AND RSI(14) < 40.  (Mirrors Kofi's "buy quality on discount" style.)
  - Exit: +30 pts (+$150) take profit / -25 pts (-$125) stop loss /
          10 trading-day time stop / Friday close (no weekend holds,
          matches the core "no gap risk" rule).
  - Position = 1 MES contract, $5 per index point. Max risk per trade
    ($125) stays inside the $100-150 rule from the options system.

EXTENDED PAPER PERIOD (Kofi, 8/11/26): the MES gate is NOT evaluated
until BOTH (a) 2026-11-09 (3 full months of paper trading) AND (b)
>=40 resolved trades. That is deliberately longer than the momentum
gate (10 flags) because futures are pure leverage with no theta.

Go-live gate (Lever 4) once period + sample are met:
  win rate >=55% AND avg win / avg loss >=1.5 AND max drawdown <=25%.

Early-review trigger (don't waste 3 months on a broken strategy):
  >=20 resolved trades with win rate <40% OR drawdown >25%.

Toggles (edit at top of file):
  NO_WEEKEND_HOLD  : exit Friday close; no entries on Friday (default ON)
  LONG_ONLY        : True = mean-reversion dips; False (future) = add shorts
"""
import json, os, subprocess, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

SYMBOL = "ES=F"           # Yahoo continuous front-month E-mini S&P 500
MULT = 5.0                # MES: $5 per index point
TP_PTS = 30.0             # +$150 per trade
SL_PTS = 25.0             # -$125 per trade (inside $100-150 risk rule)
MAX_HOLD = 10             # trading days
DIP_PCT = 0.02            # entry: >=2% below 20-day SMA
RSI_MAX = 40.0            # entry: RSI(14) below this
NO_WEEKEND_HOLD = True    # no entries Friday, exit Friday close
LONG_ONLY = True

REVIEW_DATE = "2026-11-09"   # 3-month extended paper period end
GATE_MIN_TRADES = 40
GATE_WR = 55.0
GATE_RR = 1.5
GATE_MAX_DD = 25.0
EARLY_TRADES = 20
EARLY_WR = 40.0

START_EQUITY = 1500.0     # paper equity anchor (mirrors sim cash)


def fetch_history(sym=SYMBOL, rng="3mo"):
    """Daily closes [(date, close), ...] for the continuous front-month."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d"
    out = subprocess.run(["curl", "-s", "-m", "15", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        d = json.loads(out.stdout)
        res = d["chart"]["result"][0]
        closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
        ts = res["timestamp"]
        dates = [datetime.date.fromtimestamp(t) for t in ts]
        return list(zip(dates, closes))
    except Exception:
        return []


def rsi14(closes):
    if len(closes) < 15:
        return None
    gains = losses = 0.0
    for i in range(len(closes) - 14, len(closes)):
        ch = closes[i] - closes[i - 1]
        if ch >= 0:
            gains += ch
        else:
            losses -= ch
    if losses == 0:
        return 100.0
    rs = (gains / 14) / (losses / 14)
    return 100.0 - 100.0 / (1.0 + rs)


def sma(closes, n):
    if len(closes) < n:
        return None
    return sum(closes[-n:]) / n


def step(state):
    """One daily sim step for MES. Mutates state; returns event strings."""
    events = []
    if "mes" not in state:
        state["mes"] = None
    if "mes_trades" not in state:
        state["mes_trades"] = []

    today = datetime.date.today()
    if today.weekday() >= 5:      # weekend runs: no new data, no actions
        return events

    hist = fetch_history()
    if len(hist) < 25:            # need SMA20 + RSI buffer
        return events

    last_date, last_close = hist[-1]
    closes = [c for _, c in hist]
    pos = state["mes"]

    # --- exits ---
    if pos:
        entry_date = datetime.date.fromisoformat(pos["entry_date"])
        held = sum(1 for d, _ in hist if d > entry_date)
        reason = None
        px = last_close
        if px >= pos["tp"]:
            reason = "tp"
        elif px <= pos["sl"]:
            reason = "sl"
        elif held >= MAX_HOLD:
            reason = "time"
        elif NO_WEEKEND_HOLD and today.weekday() == 4 and held >= 1:
            reason = "weekend"
        if reason:
            if reason == "sl" and px < pos["sl"]:
                px = pos["sl"]    # paper: assume fill at stop (real gaps can be worse)
            pnl = round((px - pos["entry"]) * MULT, 2)
            rec = {"entry": round(pos["entry"], 2), "exit": round(px, 2),
                   "entry_date": pos["entry_date"], "exit_date": str(today),
                   "reason": reason, "pnl": pnl, "hold_days": held}
            state["mes_trades"].append(rec)
            state["mes"] = None
            events.append(f"MES CLOSED {reason} entry {rec['entry']} exit {rec['exit']} pnl ${pnl:+.2f}")

    # --- entry (long-only mean reversion) ---
    if state["mes"] is None and LONG_ONLY:
        if NO_WEEKEND_HOLD and today.weekday() == 4:
            pass  # no Friday entries (weekend gap risk)
        else:
            s20 = sma(closes, 20)
            r = rsi14(closes)
            if s20 and r is not None and last_close <= s20 * (1 - DIP_PCT) and r < RSI_MAX:
                state["mes"] = {"entry": round(last_close, 2), "entry_date": str(last_date),
                                "sl": round(last_close - SL_PTS, 2),
                                "tp": round(last_close + TP_PTS, 2)}
                events.append(f"MES BUY 1 @ {last_close:.2f} (sma20 {s20:.0f}, rsi {r:.0f}) "
                              f"sl {last_close - SL_PTS:.0f} tp {last_close + TP_PTS:.0f}")
    return events


def report(state):
    """Saturday-report section for MES paper trading."""
    trades = state.get("mes_trades", [])
    pos = state.get("mes")
    lines = []
    if not trades and not pos:
        lines.append("MES PAPER (futures): no trades yet — waiting for a dip signal "
                     "(ES >=2% below 20-SMA with RSI<40). Extended paper period runs "
                     f"through {REVIEW_DATE}; gate needs >=40 trades + 3 months.")
        return "\n".join(lines)

    if trades:
        wins = [t for t in trades if t["pnl"] > 0]
        losses = [t for t in trades if t["pnl"] <= 0]
        n = len(trades)
        wr = len(wins) / n * 100
        avg_win = sum(t["pnl"] for t in wins) / len(wins) if wins else 0.0
        avg_loss = sum(t["pnl"] for t in losses) / len(losses) if losses else 0.0
        net = sum(t["pnl"] for t in trades)
        rr = abs(avg_win / avg_loss) if avg_loss != 0 else 0.0

        # equity curve + max drawdown (paper equity anchored at $1,500)
        eq, peak, max_dd = START_EQUITY, START_EQUITY, 0.0
        for t in trades:
            eq += t["pnl"]
            peak = max(peak, eq)
            dd = (peak - eq) / peak * 100
            max_dd = max(max_dd, dd)

        lines.append(f"MES PAPER (futures): {n} resolved | win rate {wr:.0f}% | "
                     f"avg win ${avg_win:+.1f} | avg loss ${avg_loss:+.1f} | R:R {rr:.2f} | "
                     f"net ${net:+.2f} | max drawdown {max_dd:.1f}%")
        by_r = {}
        for t in trades:
            by_r[t["reason"]] = by_r.get(t["reason"], 0) + 1
        lines.append(f"  exits: {', '.join(f'{k} {v}' for k, v in sorted(by_r.items()))}")
        for t in trades[-8:]:
            lines.append(f"  {t['exit_date']} {t['reason']} entry {t['entry']} exit {t['exit']} "
                         f"${t['pnl']:+.2f} ({t['hold_days']}d)")

        # early review trigger
        if n >= EARLY_TRADES and (wr < EARLY_WR or max_dd > GATE_MAX_DD):
            lines.append(f"  ⚠ EARLY REVIEW: {n} trades with WR {wr:.0f}% / DD {max_dd:.1f}% — "
                         "below survival line. Pause and rework the strategy instead of waiting "
                         "for the full period.")

        # extended-period gate (only after BOTH 3 months AND 40 trades)
        if n >= GATE_MIN_TRADES:
            passed = wr >= GATE_WR and rr >= GATE_RR and max_dd <= GATE_MAX_DD
            if passed:
                lines.append(f"  ✅ LEVER 4 (MES): GATE PASSED — {n} trades, WR {wr:.0f}%, "
                             f"R:R {rr:.2f}, DD {max_dd:.1f}%. Futures are green-lit: "
                             "1 MES, $125 risk, same discipline as options.")
            else:
                lines.append(f"  LEVER 4 (MES): gate NOT passed (need WR >=55%, R:R >=1.5, "
                             f"DD <=25%; now {wr:.0f}% / {rr:.2f} / {max_dd:.1f}%). Keep paper trading.")
        else:
            lines.append(f"  LEVER 4 (MES): {n}/{GATE_MIN_TRADES} trades — gate evaluates at "
                         f"{REVIEW_DATE} or {GATE_MIN_TRADES} trades, whichever comes LATER "
                         "(extended paper period).")
    if pos:
        lines.append(f"  Open: 1 MES @ {pos['entry']} (sl {pos['sl']}, tp {pos['tp']}) since {pos['entry_date']}")
    return "\n".join(lines)


if __name__ == "__main__":
    # quick manual test
    import sys
    st = {"mes": None, "mes_trades": []}
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        print(report(st))
    else:
        print(step(st))
        print(report(st))

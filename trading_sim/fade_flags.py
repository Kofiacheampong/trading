#!/usr/bin/env python3
"""
Fade-the-flag paper sim — the NetPicks cookbook side of the momentum flags.

Idea (Kofi greenlit 8/16/26): every momentum call flag is a "buy strength"
signal (RSI>=70, Z>=2.5 sigma). This track takes the OPPOSITE side of the SAME
signal — sell a short call credit spread (fade the overbought extreme) on the
same ticker, same expiry, same window. One gate decides which philosophy
survives in the current regime (the OR-fade backtest says fades win).

Rules (mirror the momentum flag lifecycle for a fair same-window fight):
- Created automatically for every call flag dated >= 2026-08-16 (no retro data).
- Short strike: first liquid strike >= flag spot * 1.05 (5% OTM).
- Long strike: the next listed strike above the short strike.
- Expiry + time-stop: identical to the momentum flag's.
- Exit: buy back when spread cost <= 50% of credit (keep >=50% of max profit),
        or cost >= 2x credit (cut), or time-stop, or expiry (settle at intrinsic).
- ret measured as % of max profit (credit): (credit - cost) / credit * 100.

Gate (LEVER 3C): >=10 resolved fades, WR >=55%, avg win / avg loss >= 1.5.
Report also shows the head-to-head: fade ret vs momentum ret on matched flags.
"""
import json, os, sys, datetime, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import options_data as od

BASE = os.path.dirname(os.path.abspath(__file__))
FEATURE_DATE = datetime.date(2026, 8, 16)   # only flag dates >= this get fades
OTM_PCT = 1.05
TP_FACTOR = 0.50    # buy back at 50% of collected credit
SL_FACTOR = 2.00    # cut when cost reaches 2x credit


def _spread_at(chain, spot, flag):
    """Pick (short_strike, long_strike) from a chain: first liquid strike >=
    spot*1.05, then the next strike above it. Returns (k_short, k_long, short_mid,
    long_mid, credit) or None."""
    rows = [c for c in chain if c.get("strike")
            and (c.get("bid") or 0) > 0 and (c.get("ask") or 0) > 0]
    rows.sort(key=lambda c: c["strike"])
    target = spot * OTM_PCT
    shorts = [c for c in rows if c["strike"] >= target]
    if not shorts:
        return None
    s = shorts[0]
    longs = [c for c in rows if c["strike"] > s["strike"]]
    if not longs:
        return None
    l = longs[0]
    short_mid, long_mid = s["mid"], l["mid"]
    credit = short_mid - long_mid
    if credit <= 0:
        return None
    return s["strike"], l["strike"], short_mid, long_mid, credit


def _expiry_ts(sym, expiry, crumb):
    for e in od.expirations(sym, crumb):
        if datetime.date.fromtimestamp(e) == expiry:
            return e
    return None


def step(state, crumb=None):
    """Open fades for eligible momentum flags; resolve open fades. Returns []."""
    if crumb is None:
        crumb = od.get_crumb()
    today = datetime.date.today()
    fades = state.setdefault("fade_flags", [])
    flags = state.get("call_flags", [])

    # --- open fades for eligible flags (no retro data) ---
    for f in flags:
        if f.get("date", "") < str(FEATURE_DATE):
            continue
        if any(x.get("flag_date") == f["date"] and x["ticker"] == f["ticker"]
               for x in fades):
            continue
        sym = f["ticker"]
        expiry = datetime.date.fromisoformat(f["expiry"])
        if expiry < today:
            continue
        ts = _expiry_ts(sym, expiry, crumb)
        if not ts:
            continue  # no chain data yet; retry next step
        chain = od.fetch_best_chain(sym, ts, crumb)
        if not chain:
            continue
        got = _spread_at(chain, f.get("spot") or 0, f)
        if not got:
            continue
        k_short, k_long, sm, lm, credit = got
        fades.append({
            "ticker": sym, "flag_date": f["date"], "expiry": f["expiry"],
            "time_stop": f.get("time_stop", f["expiry"]),
            "spot": round(f.get("spot") or 0, 2),
            "k_short": k_short, "k_long": k_long,
            "width": round(k_long - k_short, 2),
            "credit": round(credit, 2),
            "ret": None, "outcome": None, "resolved_date": None,
            "source": "fade-the-flag (NetPicks side)",
        })
        print(f"EVENT FADEFLAG {sym} OPEN {k_short:.2f}/{k_long:.2f}C exp {f['expiry']} "
              f"credit ${credit:.2f} (width ${k_long - k_short:.2f})")

    # --- resolve open fades ---
    resolved = []
    for x in fades:
        if x.get("outcome") is not None:
            continue
        sym, k_short, k_long, credit = x["ticker"], x["k_short"], x["k_long"], x["credit"]
        expiry = datetime.date.fromisoformat(x["expiry"])
        time_stop = datetime.date.fromisoformat(x["time_stop"])
        if credit <= 0:
            continue

        # expired -> settle at intrinsic value
        if today > expiry:
            ts = _expiry_ts(sym, expiry, crumb)
            px = od.fetch_quote(sym)
            if ts is None or px is None:
                continue
            cost = max(px - k_short, 0) - max(px - k_long, 0)
            cost = max(cost, 0)
            x["outcome"] = "expired"
            x["ret"] = round((credit - cost) / credit * 100, 1)
            x["resolved_date"] = str(today)
            resolved.append(x)
            continue

        ts = _expiry_ts(sym, expiry, crumb)
        if ts is None:
            continue
        chain = od.fetch_best_chain(sym, ts, crumb)
        if not chain:
            continue
        short_mid = long_mid = None
        for c in chain:
            if abs(c.get("strike", -1) - k_short) < 1e-6:
                short_mid = c["mid"]
            if abs(c.get("strike", -1) - k_long) < 1e-6:
                long_mid = c["mid"]
        if short_mid is None or long_mid is None:
            continue
        cost = max(short_mid - long_mid, 0)

        if today >= time_stop:
            x["outcome"] = "time"
            x["ret"] = round((credit - cost) / credit * 100, 1)
            x["resolved_date"] = str(today)
            resolved.append(x)
        elif cost <= credit * TP_FACTOR:
            x["outcome"] = "win"
            x["ret"] = round((credit - cost) / credit * 100, 1)
            x["resolved_date"] = str(today)
            resolved.append(x)
        elif cost >= credit * SL_FACTOR:
            x["outcome"] = "loss"
            x["ret"] = round((credit - cost) / credit * 100, 1)
            x["resolved_date"] = str(today)
            resolved.append(x)
    return resolved


def report(state):
    """Return the fade-the-flag section of the weekly sim report (a string)."""
    fades = state.get("fade_flags", [])
    resolved = [x for x in fades if x.get("outcome")]
    flags = {f["date"] + f["ticker"]: f for f in state.get("call_flags", [])}
    lines = ["\nFADE-THE-FLAG (short call spreads vs momentum flags, paper):"]
    if not resolved:
        lines.append("  none resolved yet (first fades mirror flags dated >= 8/16/26)")
    else:
        rets = [x["ret"] for x in resolved]
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        wr = len(wins) / len(rets) * 100
        avg_ret = sum(rets) / len(rets)
        avg_w = sum(wins) / len(wins) if wins else 0.0
        avg_l = sum(losses) / len(losses) if losses else 0.0
        rr = abs(avg_w / avg_l) if avg_l < 0 else 0.0
        credits = sum(x["credit"] for x in resolved)
        lines.append(f"  {len(resolved)} resolved | win rate {wr:.0f}% | "
                     f"avg ret {avg_ret:+.1f}% | avg win {avg_w:+.1f}% | avg loss {avg_l:+.1f}% | "
                     f"credit collected ${credits:.2f}")
        # head-to-head vs momentum flags
        paired = []
        for x in resolved:
            f = flags.get(x["flag_date"] + x["ticker"])
            if f and f.get("ret") is not None:
                paired.append((x, f))
        if paired:
            fade_wins = sum(1 for x, f in paired if x["ret"] > f["ret"])
            lines.append(f"  HEAD-TO-HEAD vs momentum (matched flags): fade won "
                         f"{fade_wins}/{len(paired)}")
            for x, f in paired[-6:]:
                lines.append(f"    {x['resolved_date']} {x['ticker']} fade {x['ret']:+.1f}% "
                             f"vs mom {f['ret']:+.1f}% ({x['outcome']})")
        for x in resolved[-6:]:
            lines.append(f"  {x.get('resolved_date','?')} {x['ticker']} {x['k_short']:.2f}/"
                         f"{x['k_long']:.2f}C {x['outcome']} ret {x['ret']:+.1f}% "
                         f"(credit ${x['credit']:.2f}, flag {x['flag_date']})")
        if len(resolved) >= 10:
            if wr >= 55.0 and rr >= 1.5:
                lines.append("  LEVER 3C: FADE-THE-FLAG GATE PASSED — fading momentum extremes "
                             "has empirical backing (>=10, >=55% WR, R:R >=1.5).")
            else:
                lines.append(f"  LEVER 3C: {len(resolved)} resolved — gate NOT passed "
                             f"(need >=55% WR + R:R >=1.5; now {wr:.0f}% / {rr:.1f}). "
                             f"Keep paper trading.")
        else:
            lines.append(f"  LEVER 3C: {len(resolved)}/10 fades resolved — keep paper trading.")
    open_fades = [x for x in fades if x.get("outcome") is None]
    if open_fades:
        lines.append(f"  Open fades: {len(open_fades)}")
        for x in open_fades:
            lines.append(f"    {x['flag_date']} {x['ticker']} {x['k_short']:.2f}/{x['k_long']:.2f}C "
                         f"exp {x['expiry']} credit ${x['credit']:.2f} time-stop {x['time_stop']}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sim as _sim
    st = _sim.load()
    step(st)
    print(report(st))

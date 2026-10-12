#!/usr/bin/env python3
"""Lightweight data-fetch health signal (added 2026-10-12).

Problem (systems review 2026-10-12): every data fetch fails *silently* — a
Yahoo/Cboe outage returns the same empty result as "no setups today", so a
broken feed looks identical to a quiet market.

This module records the last N attempts per source into state["fetch_health"]
and lets reports shout when a source has been failing repeatedly.

Usage:
    import data_health as dh
    dh.record(state, "yahoo_chain", ok)     # after a fetch
    print(dh.warn(state))                    # report line(s) or ""
"""
import datetime

KEEP = 12          # how many recent attempts per source to remember
FAIL_ALERT = 3     # consecutive failures before we shout


def record(state, source, ok, note=""):
    """Log one fetch attempt for `source` into state['fetch_health']."""
    h = state.setdefault("fetch_health", {})
    e = h.setdefault(source, {"last_ok": None, "last_try": None,
                              "streak_fail": 0, "attempts": []})
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    e["last_try"] = stamp
    if ok:
        e["last_ok"] = stamp
        e["streak_fail"] = 0
    else:
        e["streak_fail"] = int(e.get("streak_fail", 0)) + 1
    e["attempts"].append({"ts": stamp, "ok": bool(ok), "note": note})
    e["attempts"] = e["attempts"][-KEEP:]


def warn(state):
    """Return a report-ready warning block, or "" if every source is healthy."""
    h = state.get("fetch_health") or {}
    bad = [(s, e) for s, e in h.items() if e.get("streak_fail", 0) >= FAIL_ALERT]
    if not bad:
        return ""
    lines = ["\nDATA HEALTH ⚠ (a failing feed looks like 'no setups'):"]
    for s, e in sorted(bad, key=lambda kv: -kv[1]["streak_fail"]):
        lines.append(f"  {s}: {e['streak_fail']} consecutive failures "
                     f"(last ok: {e.get('last_ok') or 'never'})")
    return "\n".join(lines)

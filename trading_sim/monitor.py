#!/usr/bin/env python3
"""Edge-triggered stock monitor — replaces the 17 per-ticker alert crons.

Levels live in projects/watchlist-levels.json (single source of truth).
Fires ONCE when a level is crossed, then stays quiet until either:
  - price re-arms past the level by HYST (1.5%), or
  - price moves >= MATERIAL (3%) further in the triggered direction (max 1/day).

Usage:
  monitor.py            # alerts only; prints nothing when quiet
  monitor.py --status   # full board (always prints)
  monitor.py --init     # arm current state without alerting
  monitor.py --dry      # evaluate + print what WOULD fire, don't save state
"""
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEVELS = os.environ.get("MONITOR_LEVELS") or os.path.join(BASE, "projects", "watchlist-levels.json")
STATE = os.environ.get("MONITOR_STATE") or os.path.join(BASE, "trading_sim", "monitor_state.json")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
HYST = 0.015      # re-arm distance
MATERIAL = 0.03   # re-notify on continued move
MAX_NOTIFY_PER_DAY = 2


def quote(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=5d&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode())
    res = d["chart"]["result"][0]
    m = res["meta"]
    closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
    px = m.get("regularMarketPrice") or (closes[-1] if closes else None)
    # NOTE: chartPreviousClose is the close *before the 5d window* — wrong for day %.
    # Use the second-to-last daily bar (yesterday's close) instead.
    prev = closes[-2] if len(closes) > 1 else (m.get("chartPreviousClose") or px)
    return {"px": px, "prev": prev, "chg": (px - prev) / prev * 100 if prev else 0.0}


def load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def save(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
    os.replace(tmp, path)


def all_tickers(cfg):
    seen = []
    for th in cfg.get("themes", {}).values():
        for t in th.get("tickers", []):
            if t not in seen:
                seen.append(t)
    for t in list(cfg.get("tickers", {}).keys()) + list(cfg.get("holdings", {}).keys()):
        if t not in seen:
            seen.append(t)
    return seen


def nearest(px, ticker_cfg):
    """Distance in % to the nearest untriggered level, for --status."""
    cands = []
    for direction in ("below", "above"):
        for lv in ticker_cfg.get(direction, []):
            d = (lv["px"] / px - 1) * 100
            cands.append((abs(d), direction, lv["px"], d))
    if not cands:
        return None
    return min(cands)


def main():
    status = "--status" in sys.argv
    board = None
    for i, a in enumerate(sys.argv):
        if a == "--board" and i + 1 < len(sys.argv):
            board = sys.argv[i + 1]
    init = "--init" in sys.argv
    dry = "--dry" in sys.argv

    cfg = load(LEVELS, None)
    if not cfg:
        print(f"monitor: cannot read {LEVELS}")
        return 2
    st = load(STATE, {"levels": {}, "meta": {}})
    st.setdefault("levels", {})
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    quotes, errors = {}, []
    for t in all_tickers(cfg):
        try:
            quotes[t] = quote(t)
        except Exception as e:
            errors.append(f"{t}:{type(e).__name__}")
        time.sleep(0.12)

    fired = []
    for ticker, tcfg in list(cfg.get("tickers", {}).items()) + list(cfg.get("holdings", {}).items()):
        q = quotes.get(ticker)
        if not q or not q["px"]:
            continue
        px = q["px"]
        for direction in ("below", "above"):
            for lv in tcfg.get(direction, []):
                key = f"{ticker}:{direction}:{lv['px']}"
                rec = st["levels"].get(key) or {"state": None}
                lvl = lv["px"]

                if rec["state"] is None:
                    if init:
                        # --init: silently mark already-crossed levels as fired so the
                        # first live run doesn't dump 30 historical triggers.
                        past = (px <= lvl) if direction == "below" else (px >= lvl)
                        rec = {"state": "fired" if past else "armed",
                               "since": today, "last_px": px, "last_notify": None}
                    else:
                        # first sight without --init: always arm, so a level that is
                        # already crossed gets reported once on the following run.
                        rec = {"state": "armed", "since": None,
                               "last_px": px, "last_notify": None}
                    st["levels"][key] = rec
                    continue

                if rec["state"] == "armed":
                    hit = (px <= lvl) if direction == "below" else (px >= lvl)
                    if hit and not dry:
                        rec.update(state="fired", since=today, last_px=px,
                                   last_notify=today)
                        fired.append((ticker, direction, lvl, lv["why"], q, "new"))
                    elif hit and dry:
                        fired.append((ticker, direction, lvl, lv["why"], q, "new"))
                    elif not hit:
                        rec["last_px"] = px
                else:  # fired -> look for re-arm or material follow-through
                    rearm = (px >= lvl * (1 + HYST)) if direction == "below" else (px <= lvl * (1 - HYST))
                    if rearm and not dry:
                        rec.update(state="armed", last_px=px)
                        continue
                    moved = abs(px / (rec.get("last_px") or px) - 1)
                    if moved >= MATERIAL and rec.get("last_notify") != today:
                        if not dry:
                            rec.update(last_px=px, last_notify=today)
                        fired.append((ticker, direction, lvl, lv["why"], q, "follow"))
                st["levels"][key] = rec

    if not dry:
        st["meta"]["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        save(STATE, st)

    ts = datetime.now(timezone.utc).strftime("%H:%M UTC")

    if status or board:
        out = [f"📊 MONITOR BOARD — {ts}", ""]
        for th_key, th in cfg.get("themes", {}).items():
            out.append(f"— {th['label']}")
            for t in th["tickers"]:
                q = quotes.get(t)
                if not q:
                    out.append(f"  {t:6} no data")
                    continue
                n = nearest(q["px"], cfg["tickers"].get(t, {}))
                extra = f" · nearest {n[1]} ${n[2]:g} ({n[3]:+.1f}%)" if n else ""
                out.append(f"  {t:6} ${q['px']:<9.2f} {q['chg']:+5.1f}%{extra}")
            out.append("")
        if cfg.get("holdings"):
            out.append("— HOLDINGS")
            tot = 0.0
            for t, h in cfg["holdings"].items():
                q = quotes.get(t)
                if not q:
                    continue
                pl = (q["px"] - h["avg"]) * h["sh"]
                tot += pl
                out.append(f"  {t:6} ${q['px']:<9.2f} {q['chg']:+5.1f}% · {h['sh']:g} sh @ ${h['avg']:g} → {pl:+.0f} usd ({(q['px']/h['avg']-1)*100:+.1f}%)")
            out.append(f"  TOTAL unrealised: {tot:+.0f} usd")
        if errors:
            out.append(f"\n⚠️ data errors: {', '.join(errors)}")
        text = "\n".join(out)
        if board:
            with open(board, "w") as f:
                f.write(text + "\n")
        if status:
            print(text)
        if status:
            return 0
        return 0

    if not fired:
        return 0  # silence

    lines = [f"🔔 MONITOR — {ts}"]
    for ticker, direction, lvl, why, q, kind in fired:
        arrow = "▼" if direction == "below" else "▲"
        tag = "" if kind == "new" else " (still)"
        hold = ""
        if ticker in cfg.get("holdings", {}):
            h = cfg["holdings"][ticker]
            hold = f" · HOLDING {(q['px']/h['avg']-1)*100:+.1f}% vs ${h['avg']:g}"
        lines.append(f"{arrow} {ticker} ${q['px']:.2f} ({q['chg']:+.1f}%){tag} — ${lvl:g}: {why}{hold}")
    if errors:
        lines.append(f"⚠️ no data: {', '.join(errors)}")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())

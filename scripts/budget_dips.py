#!/usr/bin/env python3
"""Budget watchlist dip alert — LULU, KMB, ZTS, PYPL, PAYC.

WHY THIS EXISTS
---------------
The original cron prompt compared live prices to hard-coded "Friday Jul 31"
baselines (LULU 118.87, KMB 109.31, ZTS 77.29, PYPL 57.21, PAYC 163.96) and used
absolute thresholds (LULU<112, KMB<103, ...). By Sep 2026 every name except PAYC
sat permanently below its threshold, so the job fired every weekday reporting a
fake "7-17% below Friday" dip. It could never un-trigger and the % was computed
against a 7-week-old price. Fixed 2026-09-21.

NEW RULE (self-normalising — no stale constants)
-----------------------------------------------
  * DIP_ZONE  : last price <= 95% of the 20-day SMA
                (same rule the dip-buy sim uses, see trading_sim/sim.py)
  * FRESH DIP : day change <= -3.0% vs the previous close
  * alert a ticker when FRESH DIP, or (in DIP_ZONE and down on the day)
  * max one alert per ticker per calendar day (state file, no repeat spam)
  * refuse to alert on stale or implausible data

OUTPUT
------
  * "NO_REPLY" when nothing triggered (cron turns that into silence)
  * otherwise a short Telegram-ready digest
"""
import json
import os
import subprocess
import datetime
from statistics import mean

UNIVERSE = ["LULU", "KMB", "ZTS", "PYPL", "PAYC"]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
SMA_WINDOW = 20
ZONE_MULT = 0.95        # <= 5% below the 20-day SMA = in the dip zone
FRESH_DIP_PCT = -3.0    # day move that counts as a fresh dip
MAX_STALE_DAYS = 4      # refuse to alert on bars older than this
# Reference levels only — informational, never a trigger (PAYC has run well
# above the original <=$170 budget-basket cap; it is kept for visibility).
OLD_THRESHOLDS = {"LULU": 112.0, "KMB": 103.0, "ZTS": 73.0, "PYPL": 53.0, "PAYC": 152.0}

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, ".budget_dips_state.json")


def fetch(sym):
    """Return (last, prev, sma20, bar_date) or None."""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           f"?range=3mo&interval=1d")
    out = subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        res = json.loads(out.stdout)["chart"]["result"][0]
        q = res["indicators"]["quote"][0]["close"]
        rows = [(t, c) for t, c in zip(res["timestamp"], q) if c is not None]
        if len(rows) < SMA_WINDOW + 1:
            return None
        last = res["meta"].get("regularMarketPrice") or rows[-1][1]
        prev = rows[-2][1]
        sma = mean(c for _, c in rows[-SMA_WINDOW:])
        prior_low = min(c for _, c in rows[-SMA_WINDOW:-1])
        bar_date = datetime.date.fromtimestamp(rows[-1][0])
        return last, prev, sma, prior_low, bar_date
    except Exception:
        return None


def load_state():
    if os.path.exists(STATE):
        try:
            with open(STATE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"alerted": {}}


def save_state(st):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(st, f, indent=1)
    os.replace(tmp, STATE)


def main():
    today = datetime.date.today()
    st = load_state()
    alerted = st.setdefault("alerted", {})
    # prune anything older than 7 days
    cutoff = str(today - datetime.timedelta(days=7))
    st["alerted"] = {k: v for k, v in alerted.items() if v >= cutoff}
    alerted = st["alerted"]

    hits, stale = [], []
    for sym in UNIVERSE:
        d = fetch(sym)
        if not d:
            continue
        last, prev, sma, prior_low, bar_date = d
        if (today - bar_date).days > MAX_STALE_DAYS or prev <= 0:
            stale.append(sym)
            continue
        day_pct = (last / prev - 1) * 100
        vs_sma = (last / sma - 1) * 100
        in_zone = last <= sma * ZONE_MULT
        new_low = last < prior_low
        # a fresh −3% day, or a new 20-day low on a meaningfully red day
        if day_pct <= FRESH_DIP_PCT or (new_low and in_zone and day_pct <= -1.5):
            key = f"{sym}:{today}"
            if alerted.get(key):
                continue
            hits.append({"sym": sym, "last": last, "day": day_pct,
                         "vs_sma": vs_sma, "zone": in_zone,
                         "new_low": new_low})

    if hits:
        for h in hits:
            alerted[f"{h['sym']}:{today}"] = str(today)
        save_state(st)

    if not hits:
        print("NO_REPLY")
        return

    lines = [f"📉 *Budget basket dip* — {today}"]
    for h in hits:
        if h["day"] <= FRESH_DIP_PCT:
            tag = "FRESH DIP"
        elif h["new_low"]:
            tag = "new 20-day low"
        else:
            tag = "dip zone"
        z = "" if h["zone"] else " (above dip zone — thin signal)"
        lines.append(
            f"• *{h['sym']}* ${h['last']:.2f} — {h['day']:+.2f}% on the day, "
            f"{h['vs_sma']:+.1f}% vs 20d SMA · {tag}{z}")
    if stale:
        lines.append(f"⚠️ no data (stale feed): {', '.join(stale)}")
    lines.append("Rule: dip zone = ≤95% of 20-day SMA. No entry signal on a "
                 "green day; a −3% day inside the zone is the buy trigger.")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

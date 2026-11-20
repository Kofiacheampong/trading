#!/usr/bin/env python3
"""Render the live-levels section of projects/watchlist.md from watchlist-levels.json.

Single source of truth = the JSON. Run after every level change:
    python3 scripts/render_watchlist.py
"""
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(BASE, "projects", "watchlist-levels.json")
MD_PATH = os.path.join(BASE, "projects", "watchlist.md")
BEGIN = "<!-- LEVELS:BEGIN -->"
END = "<!-- LEVELS:END -->"


def fmt_levels(entry):
    bits = []
    for d, sym in (("below", "▼"), ("above", "▲")):
        for lv in entry.get(d, []):
            s = f"{sym} ${lv['px']:g}"
            if lv.get("close_only"):
                s += " (close)"
            bits.append(s)
    return " · ".join(bits) if bits else "—"


def fmt_zone(entry):
    z = entry.get("zone")
    if not z:
        return ""
    return f" · zone ${z['low']:g}–{z['high']:g}"


def render(cfg):
    out = [BEGIN]
    out.append("### 🎯 Live Levels — single source of truth\n")
    out.append("> Machine-readable: `projects/watchlist-levels.json` (edit this, then run "
               "`python3 scripts/render_watchlist.py`).")
    out.append("> Engine: `trading_sim/monitor.py` — edge-triggered, fires once per crossing, "
               "re-arms after a 1.5% move back, re-notifies on a 3% follow-through.")
    out.append("> Board: `projects/watchlist-board.md` · Cron: *Stock monitor — edge-triggered* "
               "10:15 AM + 3:50 PM ET (command payload, zero LLM calls).\n")
    out.append("**▼ = dip/stop trigger · ▲ = reclaim / base-confirmation trigger · "
               "zone = buy band shown on the board, never alerts**\n")

    for th in cfg["themes"].values():
        out.append(f"**{th['label']}**\n")
        out.append("| Ticker | Live levels | Note |")
        out.append("|---|---|---|")
        for t in th["tickers"]:
            e = cfg["tickers"].get(t, {})
            out.append(f"| **{t}** | {fmt_levels(e)} | {e.get('note','')} |")
        out.append("")

    out.append("**Holdings (stop / trim levels)**\n")
    out.append("| Ticker | Sh | Avg | Live levels | Note |")
    out.append("|---|---|---|---|---|")
    for t, h in cfg["holdings"].items():
        out.append(f"| **{t}** | {h['sh']:g} | ${h['avg']:g} | {fmt_levels(h)} | {h.get('note','')} |")
    out.append("")

    if cfg.get("retired"):
        out.append("**Retired**\n")
        for t, why in cfg["retired"].items():
            out.append(f"- **{t}** — {why}")
        out.append("")

    out.append(f"*Re-based {cfg.get('rebalanced','')}. Reasoning in `projects/monitoring-audit-2026-11-20.md`.*")
    out.append(END)
    return "\n".join(out)


def main():
    cfg = json.load(open(JSON_PATH))
    md = open(MD_PATH).read()
    block = render(cfg)

    if BEGIN in md and END in md:
        md = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, md, flags=re.S)
    else:
        # first run: replace the generated section that starts at the header and ends at
        # the "Re-based ..." paragraph
        start = md.index("### 🎯 Live Levels")
        m = re.search(r"\*Re-based [^\n]*\n", md[start:])
        if not m:
            raise SystemExit("cannot locate levels section")
        end = start + m.end()
        md = md[:start] + block + "\n" + md[end:]

    open(MD_PATH, "w").write(md)
    print(f"rendered {len(block)} bytes into watchlist.md")


if __name__ == "__main__":
    main()

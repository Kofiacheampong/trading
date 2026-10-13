#!/usr/bin/env python3
"""Breadth line — index move vs. Kofi's basket, and % of the universe above its 20-SMA.

Added 2026-10-12: the headline index and Kofi's actual screen often disagree
(a "flat market, red basket" dispersion day reads as "the whole market is red"
when you're small-cap/thematic heavy). This makes that divergence explicit.

Usage:
    python3 breadth.py            # print the BREADTH block
    (also called from sim.py's report())
"""
import subprocess, json, statistics

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
INDICES = {"S&P 500": "^GSPC", "Nasdaq": "^IXIC", "Dow": "^DJI", "Russell 2000": "^RUT"}
# Kofi's holdings + the names he actually watches (drone / DC-power / rare-earth /
# quantum + live watchlist). Keep this list in sync with the watchlists.
BASKET = ["DRAM", "MP", "INTC", "AMPG", "MDB", "IONQ", "AVAV", "KTOS", "ONDS", "RCAT",
          "UMAC", "TXN", "ADI", "VRT", "NVTS", "ON", "HNST", "USAR", "HIMS", "CIEN",
          "CLF", "WOLF", "NBIS", "IREN", "CRCL"]


def _closes(sym, rng="6mo"):
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
           f"?range={rng}&interval=1d")
    out = subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    try:
        q = json.loads(out.stdout)["chart"]["result"][0]["indicators"]["quote"][0]
        return [c for c in q["close"] if c is not None]
    except Exception:
        return []


def _day(closes):
    return (closes[-1] - closes[-2]) / closes[-2] * 100 if len(closes) >= 2 else None


def _above20(closes):
    return len(closes) >= 20 and closes[-1] > sum(closes[-20:]) / 20


def report(state=None):
    idx = {}
    for name, sym in INDICES.items():
        c = _closes(sym, "5d")
        d = _day(c) if c else None
        if d is not None:
            idx[name] = d
    days, above, tot = {}, 0, 0
    for s in BASKET:
        c = _closes(s)
        if not c:
            continue
        d = _day(c)
        if d is not None:
            days[s] = d
        if _above20(c):
            above += 1
        tot += 1

    lines = ["BREADTH — index vs your basket:"]
    lines.append("  " + " | ".join(f"{k} {v:+.2f}%" for k, v in idx.items()))
    if days:
        avg = statistics.mean(days.values())
        spx = idx.get("S&P 500", 0.0)
        red = sum(1 for v in days.values() if v < 0)
        lines.append(f"  basket: avg {avg:+.2f}% | {red}/{len(days)} red | vs S&P {spy_delta(avg, spx)}")
        lines.append(f"  20-SMA breadth: {above}/{tot} above ({above / tot * 100:.0f}%)")
        if spx > -0.3 and avg < -1.5:
            lines.append("  ⚠ DIVERGENCE: index flat/green but your basket is red — "
                         "risk-off is concentrated in small caps.")
        if tot and above / tot < 0.25:
            lines.append("  ⚠ WEAK BREADTH: <25% of your universe above its 20-SMA — "
                         "defensive regime; size down, wait for trend confirmation.")
    return "\n".join(lines)


def spy_delta(avg, spx):
    d = avg - spx
    return f"{d:+.2f}pp {'under' if d < 0 else 'out'}performing"


if __name__ == "__main__":
    print(report())

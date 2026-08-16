#!/usr/bin/env python3
"""
Covered-call (buy-write) paper sim — LEVER 5. Corey Holiday's rules, gate-tested.

Paper-tracks selling ~8% OTM monthly covered calls on synthetic 100-share lots
for the names Kofi would actually own in size: his real holdings (MP, DRAM)
plus the budget basket (LULU, KMB, ZTS, PYPL, PAYC).

Entry filters (video lessons 4 + quality floor):
  1. Regime filter: SKIP when SMA20 > SMA50 (confirmed uptrend). Do not sell
     calls into the strongest upside periods — that is exactly where the cap
     bites (opportunity cost). Sell only in flat/down regimes.
  2. Premium floor: SKIP when the ~8% OTM monthly call yields < 1.0% of spot.
     Not worth capping upside for pennies.
  3. Liquidity: strike must have a real bid/ask on the Yahoo chain.

Settlement at expiry (paper, 100 sh):
  - spot >= strike -> "assigned": P&L = (strike - entry) + premium per share
  - spot <  strike -> "kept":    P&L = (spot  - entry) + premium per share
  Per-cycle benchmark: plain 100-share hold return over the same window.

Gate (LEVER 5): >=20 resolved AND win rate >=70% AND avg premium yield >=1.0%
AND sum(cycle ret) >= 0.8 * sum(hold ret) — the filter must dodge the big
upside months, otherwise the strategy is just capped growth.

Real-money application: ONLY on names where Kofi owns 100+ shares (he owns
none today — this is readiness + ticker-qualification testing).
"""
import json, os, sys, datetime, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import options_data as od

BASE = os.path.dirname(os.path.abspath(__file__))
CC_UNIVERSE = ["MP", "DRAM", "LULU", "KMB", "ZTS", "PYPL", "PAYC"]
OTM_PCT = 1.08          # ~8% OTM strike
MIN_YIELD = 0.01        # 1.0% of spot per month minimum
TARGET_DTE, MIN_DTE, MAX_DTE = 30, 21, 45   # monthly-ish expiry
SHARES = 100
MAX_SKIPS = 300


def sma20_50(sym):
    """(sma20, sma50) from 1y daily closes; (None, None) if not enough data."""
    ts, closes, _ = od.fetch_history(sym, rng="1y")
    if not closes or len(closes) < 50:
        return None, None
    return (sum(closes[-20:]) / 20, sum(closes[-50:]) / 50)


def call_mid(sym, strike, expiry_ts, crumb):
    """Mid of one call (strike/expiry) — real bid/ask only, no last-price junk."""
    chain = od.fetch_best_chain(sym, expiry_ts, crumb)
    for c in chain:
        if c.get("strike") is not None and abs(c["strike"] - strike) < 1e-6:
            bid, ask = c.get("bid") or 0, c.get("ask") or 0
            if bid > 0 and ask > 0:
                return (bid + ask) / 2
    return None


def pick_strike(sym, expiry_ts, spot, crumb):
    """First liquid strike >= spot * OTM_PCT; None if none exists."""
    chain = od.fetch_best_chain(sym, expiry_ts, crumb)
    rows = [c for c in chain if c.get("strike")
            and (c.get("bid") or 0) > 0 and (c.get("ask") or 0) > 0]
    cands = [c["strike"] for c in rows if c["strike"] >= spot * OTM_PCT]
    if not cands:
        return None
    return min(cands)


def step(state, crumb=None):
    """Resolve expired cycles, then open new ones (Mon-Fri only)."""
    if crumb is None:
        crumb = od.get_crumb()
    today = datetime.date.today()
    cycles = state.setdefault("cc", [])
    skips = state.setdefault("cc_skips", [])

    # --- resolve open cycles at expiry ---
    for c in cycles:
        if c.get("outcome") is not None:
            continue
        if today < datetime.date.fromisoformat(c["expiry"]):
            continue
        px = od.fetch_quote(c["ticker"])
        if px is None:
            continue  # retry next step
        entry, strike, prem = c["spot"], c["strike"], c["premium"]
        if px >= strike:
            pnl = (strike - entry + prem) * SHARES
            outcome = "assigned"
        else:
            pnl = (px - entry + prem) * SHARES
            outcome = "kept"
        c["outcome"] = outcome
        c["settle"] = round(px, 2)
        c["pnl_usd"] = round(pnl, 2)
        c["ret_pct"] = round(pnl / (entry * SHARES) * 100, 2)
        c["hold_pct"] = round((px / entry - 1) * 100, 2)
        c["resolved_date"] = str(today)
        print(f"EVENT CC {c['ticker']} {outcome.upper()} ret {c['ret_pct']:+.2f}% "
              f"(yield {c['yield_pct']:.2f}%, vs hold {c['hold_pct']:+.2f}%)")

    # --- open new cycles (Mon-Fri; weekend steps only resolve) ---
    if today.weekday() >= 5:
        return
    for sym in CC_UNIVERSE:
        if any(c["ticker"] == sym and c.get("outcome") is None for c in cycles):
            continue
        s20, s50 = sma20_50(sym)
        if s20 is None:
            skips.append({"date": str(today), "ticker": sym, "reason": "no history"})
        elif s20 > s50:
            skips.append({"date": str(today), "ticker": sym, "reason": "sma20>sma50 uptrend",
                          "s20": round(s20, 2), "s50": round(s50, 2)})
            continue
        ts, dte = od.pick_expiry(sym, crumb, target_dte=TARGET_DTE,
                                 min_dte=MIN_DTE, max_dte=MAX_DTE)
        if not ts:
            skips.append({"date": str(today), "ticker": sym, "reason": "no expiry"})
            continue
        spot = od.fetch_quote(sym)
        if not spot:
            continue
        strike = pick_strike(sym, ts, spot, crumb)
        if not strike:
            skips.append({"date": str(today), "ticker": sym, "reason": "no liquid strike"})
            continue
        prem = call_mid(sym, strike, ts, crumb)
        if prem is None:
            continue
        yield_pct = prem / spot
        if yield_pct < MIN_YIELD:
            skips.append({"date": str(today), "ticker": sym, "reason": "low premium",
                          "yield": round(yield_pct * 100, 2)})
            continue
        exp = datetime.date.fromtimestamp(ts)
        cycles.append({"ticker": sym, "date": str(today), "spot": round(spot, 2),
                       "strike": strike, "expiry": str(exp), "dte": dte,
                       "premium": round(prem, 2), "yield_pct": round(yield_pct * 100, 2),
                       "s20": round(s20, 2), "s50": round(s50, 2), "outcome": None})
        print(f"EVENT CC {sym} OPEN {strike}C exp {exp} prem ${prem:.2f} "
              f"yield {yield_pct * 100:.2f}% (s20 {s20:.1f} s50 {s50:.1f})")

    if len(skips) > MAX_SKIPS:
        del skips[:len(skips) - MAX_SKIPS]


def report(state):
    """Return the covered-call section of the weekly sim report (a string)."""
    cycles = state.get("cc", [])
    resolved = [c for c in cycles if c.get("outcome")]
    lines = ["\nCOVERED CALLS (buy-write, synthetic 100-sh lots, paper):"]
    if not resolved:
        lines.append("  none resolved yet (first monthly expiries settle in Sept)")
    else:
        wins = [c for c in resolved if c["pnl_usd"] > 0]
        assigned = [c for c in resolved if c["outcome"] == "assigned"]
        wr = len(wins) / len(resolved) * 100
        avg_yield = statistics.mean(c["yield_pct"] for c in resolved)
        tot_ret = sum(c["ret_pct"] for c in resolved)
        tot_hold = sum(c["hold_pct"] for c in resolved)
        net = sum(c["pnl_usd"] for c in resolved)
        lines.append(f"  {len(resolved)} resolved | win rate {wr:.0f}% | "
                     f"avg yield {avg_yield:.2f}%/mo | assigned {len(assigned)} | "
                     f"net ${net:+.2f} | cum ret {tot_ret:+.1f}% vs hold {tot_hold:+.1f}%")
        for c in resolved[-8:]:
            lines.append(f"  {c.get('resolved_date','?')} {c['ticker']} {c['strike']:.2f}C "
                         f"{c['outcome']} ret {c['ret_pct']:+.2f}% "
                         f"(yield {c['yield_pct']:.2f}%, hold {c['hold_pct']:+.2f}%)")
        if len(resolved) >= 20:
            rr = tot_ret >= 0.8 * tot_hold
            if wr >= 70.0 and avg_yield >= 1.0 and rr:
                lines.append("  LEVER 5: COVERED-CALL GATE PASSED — buy-writes have empirical "
                             "backing (>=20, >=70% WR, >=1.0%/mo yield, >=80% of hold return). "
                             "Applies only to names owned at 100+ shares.")
            else:
                lines.append(f"  LEVER 5: {len(resolved)} resolved — gate NOT passed "
                             f"(need >=70% WR, >=1.0%/mo yield, >=80% of hold; "
                             f"now {wr:.0f}% / {avg_yield:.2f}% / {rr}). Keep paper trading.")
        else:
            lines.append(f"  LEVER 5: {len(resolved)}/20 cycles resolved — keep paper trading.")
    open_cycles = [c for c in cycles if c.get("outcome") is None]
    if open_cycles:
        lines.append(f"  Open cycles: {len(open_cycles)}")
        for c in open_cycles:
            lines.append(f"    {c['date']} {c['ticker']} {c['strike']:.2f}C exp {c['expiry']} "
                         f"prem ${c['premium']:.2f} ({c['yield_pct']:.2f}%/mo)")
    skips = state.get("cc_skips", [])
    if skips:
        counts = {}
        for s in skips:
            counts[s["reason"]] = counts.get(s["reason"], 0) + 1
        summ = ", ".join(f"{k} {v}x" for k, v in sorted(counts.items(),
                                                        key=lambda x: -x[1]))
        lines.append(f"  Filter skips (since start): {summ}")
    return "\n".join(lines)


if __name__ == "__main__":
    # Standalone dry-run on a throwaway state (no save) — for testing.
    import sim as _sim  # only for state loading in manual runs
    st = _sim.load()
    step(st)
    print(report(st))

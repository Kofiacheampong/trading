#!/usr/bin/env python3
"""Weeklies Scanner — find cheap bull call spreads for small accounts."""
import json, sys, time, warnings
import requests
import yfinance as yf

warnings.filterwarnings("ignore")

H = {
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Accept": "application/json",
}

DATES = ["2026-11-23", "2026-11-24", "2026-11-25", "2026-11-27"]


def earnings_week():
    out = []
    for d in DATES:
        try:
            r = requests.get(
                f"https://api.nasdaq.com/api/calendar/earnings?date={d}", headers=H, timeout=25
            )
            rows = r.json()["data"]["rows"] or []
        except Exception as e:
            print(f"# cal fail {d}: {e}", file=sys.stderr)
            continue
        for row in rows:
            row["date"] = d
            out.append(row)
    return out


def parse_cap(s):
    try:
        return float(str(s).replace("$", "").replace(",", ""))
    except Exception:
        return 0.0


def main():
    rows = earnings_week()
    print(f"# total reporters: {len(rows)}", file=sys.stderr)

    seen = {}
    for r in rows:
        sym = r.get("symbol", "").strip().upper()
        if not sym or "^" in sym or "/" in sym:
            continue
        cap = parse_cap(r.get("marketCap", "0"))
        # keep small/mid caps — big caps are usually > $50/share
        if cap > 60e9:
            continue
        seen[sym] = {
            "sym": sym,
            "name": r.get("name", ""),
            "date": r["date"],
            "time": r.get("time", ""),
            "cap": cap,
            "eps": r.get("epsForecast", ""),
        }

    cands = list(seen.values())
    print(f"# candidates after cap filter: {len(cands)}", file=sys.stderr)

    results = []
    for i, c in enumerate(cands):
        try:
            t = yf.Ticker(c["sym"])
            fi = t.fast_info
            px = fi.get("lastPrice") or fi.get("last_price")
            if not px:
                continue
            px = float(px)
            if px < 3 or px > 50:      # scan window
                continue
            c["px"] = px
            c["avgvol"] = float(fi.get("lastVolume") or 0)

            exps = t.options
            if not exps:
                continue
            # nearest expiry at least 4 days out
            import datetime as dt
            today = dt.date(2026, 11, 22)
            good = []
            for e in exps:
                try:
                    ed = dt.datetime.strptime(e, "%Y-%m-%d").date()
                except Exception:
                    continue
                if 3 <= (ed - today).days <= 45:
                    good.append((ed, e))
            if not good:
                continue
            good.sort()
            exp_date, exp = good[0]
            c["exp"] = exp

            ch = t.option_chain(exp)
            calls = ch.calls
            if calls is None or len(calls) == 0:
                continue
            calls = calls[(calls["volume"].fillna(0) > 0) | (calls["openInterest"].fillna(0) > 20)]
            if len(calls) < 3:
                continue

            best = None
            cl = calls.sort_values("strike").reset_index(drop=True)
            for a in range(len(cl)):
                for b in range(a + 1, len(cl)):
                    ka = float(cl.loc[a, "strike"])
                    kb = float(cl.loc[b, "strike"])
                    width = kb - ka
                    if width <= 0 or width > 3.01:
                        continue
                    # must be OTM-ish / near money
                    if ka < px * 0.90 or ka > px * 1.35:
                        continue
                    ask = float(cl.loc[a, "ask"] or 0)
                    bid = float(cl.loc[b, "bid"] or 0)
                    if ask <= 0 or bid < 0:
                        continue
                    debit = ask - bid
                    if debit <= 0:
                        continue
                    cost = debit * 100
                    if not (35 <= cost <= 160):
                        continue
                    maxp = (width - debit) * 100
                    if maxp <= 0:
                        continue
                    rr = maxp / cost
                    be = ka + debit
                    move = (be - px) / px * 100
                    if rr < 0.4 or move > 22:
                        continue
                    score = rr * 100 - move * 3
                    # liquidity
                    oi = float(cl.loc[a, "openInterest"] or 0) + float(cl.loc[b, "openInterest"] or 0)
                    if oi < 30:
                        continue
                    if best is None or score > best["score"]:
                        best = {
                            "score": score,
                            "long": ka, "short": kb, "cost": cost,
                            "maxp": maxp, "rr": rr, "be": be, "move": move,
                            "oi": oi,
                            "vol": float(cl.loc[a, "volume"] or 0) + float(cl.loc[b, "volume"] or 0),
                        }
            if best:
                c.update(best)
                results.append(c)
        except Exception:
            pass
        if i % 20 == 0:
            print(f"# ..{i}/{len(cands)}", file=sys.stderr)

    results.sort(key=lambda x: -x["score"])
    json.dump(results, open("/home/kofi/clawd/projects/weeklies-out.json", "w"), indent=1)
    for r in results[:30]:
        print(
            f"{r['sym']:6s} ${r['px']:>=6.2f} {r['exp']} {r['long']:.0f}/{r['short']:.0f}C "
            f"cost=${r['cost']:.0f} max=${r['maxp']:.0f} rr={r['rr']:.2f} be={r['be']:.2f} "
            f"need={r['move']:.1f}% oi={r['oi']:.0f} ER={r['date']} cap={r['cap']/1e9:.1f}B"
        )
    print(f"# results: {len(results)}", file=sys.stderr)


if __name__ == "__main__":
    main()

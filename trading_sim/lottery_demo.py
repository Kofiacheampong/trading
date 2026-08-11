#!/usr/bin/env python3
"""
Lottery-ticket call demo for the paper sim.

Opens ONE cheap OTM call using REAL option prices (Cboe delayed quotes — official
exchange data, free, no API key) and stores it under state.json["lottery"].
The main sim (sim.py) ignores this key — it is a standalone experiment.

Usage:
  python3 lottery_demo.py          # opens a position if none open, else values it
  python3 lottery_demo.py --reset  # delete the demo position
"""
import json, os, re, subprocess, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
OPT_PAT = re.compile(r"^([A-Z]+)(\d{6})([CP])(\d{8})$")


def curl(url):
    return subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {UA}", url],
                          capture_output=True, text=True).stdout


def spot(sym):
    d = json.loads(curl(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1mo&interval=1d"))
    q = d["chart"]["result"][0]["indicators"]["quote"][0]
    closes = [c for c in q["close"] if c]
    return closes[-1]


def cboe_chain(sym):
    """Full option chain from Cboe delayed quotes. Decodes strike/expiry from the symbol."""
    d = json.loads(curl(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json"))
    out = []
    for o in d["data"]["options"]:
        m = OPT_PAT.match(o["option"])
        if not m:
            continue
        _, yymmdd, typ, strike = m.groups()
        exp = datetime.date(2000 + int(yymmdd[:2]), int(yymmdd[2:4]), int(yymmdd[4:6]))
        out.append({"exp": exp, "type": typ, "strike": int(strike) / 1000.0,
                    "bid": o.get("bid") or 0, "ask": o.get("ask") or 0,
                    "last": o.get("last_trade_price") or 0,
                    "delta": o.get("delta"), "iv": o.get("iv"), "theo": o.get("theo")})
    return out


def mid(o):
    if o["bid"] > 0 and o["ask"] > 0:
        return (o["bid"] + o["ask"]) / 2
    if o["last"] > 0:
        return o["last"]
    return o.get("theo") or 0


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return None


def save_state(state):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=1)
    os.replace(tmp, STATE)


def open_position(sym="ZTS", otm=0.10, min_days=7):
    px = spot(sym)
    target = px * (1 + otm)
    today = datetime.date.today()
    chain = cboe_chain(sym)
    cs = [c for c in chain if c["type"] == "C" and (c["exp"] - today).days >= min_days]
    if not cs:
        print("OPEN_FAILED (no calls)")
        return None
    exp = min(c["exp"] for c in cs)
    exp_calls = [c for c in cs if c["exp"] == exp]
    above = [c for c in exp_calls if c["strike"] >= target]
    o = min(above, key=lambda c: c["strike"]) if above else max(exp_calls, key=lambda c: c["strike"])
    cost = o["ask"] if o["ask"] > 0 else mid(o)
    return {
        "sym": sym, "strike": o["strike"], "expiry": o["exp"].isoformat(),
        "cost": round(cost, 2), "bid": o["bid"], "ask": o["ask"],
        "spot": round(px, 2), "date": str(today),
        "delta": round(o["delta"], 3) if o["delta"] is not None else None,
        "iv": round(o["iv"] * 100, 1) if o["iv"] else None,
        "label": "DEMO lottery ticket (paper)"
    }


def value_position(entry):
    chain = cboe_chain(entry["sym"])
    today = datetime.date.today()
    stored = datetime.date.fromisoformat(entry["expiry"])
    cands = [c for c in chain if c["type"] == "C"
             and abs(c["strike"] - entry["strike"]) < 1e-6 and c["exp"] >= today]
    if not cands:
        return None
    o = min(cands, key=lambda c: abs((c["exp"] - stored).days))
    return {"bid": o["bid"], "ask": o["ask"], "mid": mid(o),
            "spot": spot(entry["sym"]), "exp": o["exp"], "delta": o["delta"]}


def main():
    if "--reset" in sys.argv:
        st = load_state()
        if st and "lottery" in st:
            del st["lottery"]
            save_state(st)
            print("LOTTERY_RESET")
        return

    st = load_state()
    if st is None:
        print("NO_STATE")
        return

    if "lottery" not in st:
        entry = open_position()
        if entry is None:
            return
        st["lottery"] = entry
        save_state(st)
        print("DEMO LOTTERY TICKET OPENED (paper)")
        print(f"  {entry['sym']} ${entry['strike']} call exp {entry['expiry']}")
        print(f"  Bought 1 contract at ${entry['cost']} (ask) = ${entry['cost']*100:.0f} risked")
        print(f"  Spot ${entry['spot']:.2f} -> strike is {max(0,(entry['strike']/entry['spot']-1)*100):.0f}% OTM")
        if entry["delta"] is not None:
            print(f"  Market-implied chance of expiring ITM: ~{entry['delta']*100:.0f}%")
            print(f"  => ~{100-entry['delta']*100:.0f}% chance this goes to $0. This is the lottery.")
        if entry["iv"]:
            print(f"  IV {entry['iv']}% — that's the price of the dream.")
    else:
        e = st["lottery"]
        v = value_position(e)
        today = datetime.date.today()
        exp = v["exp"] if v else datetime.date.fromisoformat(e["expiry"])
        days = (exp - today).days
        if v is None:
            print("VALUE_FAILED (no matching contract)")
            return
        pnl = (v["mid"] - e["cost"]) * 100
        pct = (v["mid"] / e["cost"] - 1) * 100 if e["cost"] else 0
        print("LOTTERY VALUE (paper)")
        print(f"  {e['sym']} ${e['strike']} call exp {exp.isoformat()}  ({days}d left)")
        print(f"  Entry ${e['cost']} | now mid ${v['mid']:.2f} (bid {v['bid']:.2f}/ask {v['ask']:.2f})")
        print(f"  Spot ${v['spot']:.2f} | P&L {pnl:+.2f} ({pct:+.1f}%) | value ${v['mid']*100:.0f} vs ${e['cost']*100:.0f} risked")
        if v["delta"] is not None:
            print(f"  Market-implied chance of expiring ITM now: ~{v['delta']*100:.0f}%")
        if v["mid"] <= 0.01:
            print("  -> effectively ZERO. This is the ~80% outcome.")
        elif v["mid"] < e["cost"]:
            print("  -> bleeding. Theta is eating it. Most likely path: $0 at expiry.")
        else:
            print("  -> green. The 1-in-5 version.")


if __name__ == "__main__":
    main()

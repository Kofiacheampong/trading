#!/usr/bin/env python3
"""ATM straddle -> implied move, plus leg quotes for specific spreads.
Usage: legcheck.py EXP TICKER... ; legcheck.py --spread EXP T:S1:S2 ...
"""
import json, re, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
PAT = re.compile(r"^([A-Z0-9\.]+?)(\d{6})([CP])(\d{8})$")


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode())


def load(t):
    d = fetch(f"https://cdn.cboe.com/api/global/delayed_quotes/options/{t}.json")["data"]
    return d.get("close"), d["options"]


def legs(t, exp, s1, s2):
    close, opts = load(t)
    out = []
    for o in opts:
        m = PAT.match(o["option"])
        if not m or m.group(2) != exp or m.group(3) != "C":
            continue
        k = int(m.group(4)) / 1000.0
        if k in (s1, s2):
            out.append((k, o))
    if len(out) != 2:
        print(f"{t} missing legs"); return
    out.sort()
    (k1, o1), (k2, o2) = out
    cost = o1["ask"] - o2["bid"]
    print(f"{t} spot={close} exp={exp} {k1:.2f}C bid{o1['bid']}/ask{o1['ask']} (OI {o1['open_interest']:.0f}, vol {o1['volume']:.0f}, IV {o1['iv']:.2f})")
    print(f"          {k2:.2f}C bid{o2['bid']}/ask{o2['ask']} (OI {o2['open_interest']:.0f}, vol {o2['volume']:.0f}, IV {o2['iv']:.2f})")
    print(f"  debit ${cost*100:.0f}  max ${(k2-k1-cost)*100:.0f}  roi {(k2-k1-cost)/cost*100:.0f}%  b/e {k1+cost:.2f}  need {(k1+cost-close)/close*100:+.1f}%")


def straddle(t, exp):
    close, opts = load(t)
    calls, puts = {}, {}
    for o in opts:
        m = PAT.match(o["option"])
        if not m or m.group(2) != exp:
            continue
        k = int(m.group(4)) / 1000.0
        (calls if m.group(3) == "C" else puts).setdefault(k, o)
    if close is None:
        print(f"{t}: no close"); return
    ks = sorted(set(calls) & set(puts))
    if not ks:
        print(f"{t}: no matching strikes"); return
    atm = min(ks, key=lambda k: abs(k - close))
    c, p = calls[atm], puts[atm]
    paid = (c["ask"] or 0) + (p["ask"] or 0)
    mid = ((c["bid"] or 0) + (c["ask"] or 0)) / 2 + ((p["bid"] or 0) + (p["ask"] or 0)) / 2
    print(f"{t} spot={close} exp={exp} ATM={atm} straddle mid ${mid:.2f} = +/-{mid/close*100:.1f}%  (paid {paid:.2f} = +/-{paid/close*100:.1f}%)")


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "--spread":
        exp = sys.argv[2]
        for spec in sys.argv[3:]:
            t, s1, s2 = spec.split(":")
            legs(t.upper(), exp, float(s1), float(s2))
    else:
        exp = sys.argv[1]
        for t in sys.argv[2:]:
            straddle(t.upper(), exp)

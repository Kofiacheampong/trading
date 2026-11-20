#!/usr/bin/env python3
"""Technicals snapshot for watchlist re-basing. Usage: technicals.py TICK..."""
import json, sys, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}


def bars(t):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode())
    res = d["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    closes = [c for c in q["close"] if c is not None]
    vols = [v for v in q["volume"] if v is not None]
    return res["meta"], closes, vols


def sma(xs, n):
    return sum(xs[-n:]) / n if len(xs) >= n else None


def rsi(xs, n=14):
    if len(xs) < n + 1:
        return None
    gains = losses = 0.0
    for i in range(-n, 0):
        ch = xs[i] - xs[i - 1]
        gains += max(ch, 0)
        losses += max(-ch, 0)
    ag, al = gains / n, losses / n
    if al == 0:
        return 100.0
    return 100 - 100 / (1 + ag / al)


def main(tickers):
    print(f"{'TICK':6}{'PX':>9}{'d%':>7}{'SMA20':>9}{'SMA50':>9}{'SMA200':>9}{'vs20':>8}{'vs200':>8}{'RSI':>6}{'52wLo':>9}{'52wHi':>9}{'offHi':>8}")
    for t in tickers:
        try:
            m, c, v = bars(t.upper())
            px = m.get("regularMarketPrice") or c[-1]
            prev = c[-2] if len(c) > 1 else px
            s20, s50, s200 = sma(c, 20), sma(c, 50), sma(c, 200)
            r = rsi(c)
            lo, hi = m.get("fiftyTwoWeekLow"), m.get("fiftyTwoWeekHigh")
            f = lambda x: f"{x:9.2f}" if x else "        -"
            print(f"{t.upper():6}{px:9.2f}{(px-prev)/prev*100:+6.1f}%"
                  f"{f(s20)}{f(s50)}{f(s200)}"
                  f"{(px/s20-1)*100:+7.1f}%{(px/s200-1)*100:+7.1f}%"
                  f"{r:6.1f}{f(lo)}{f(hi)}{((px/hi-1)*100 if hi else 0):+7.1f}%")
        except Exception as e:
            print(f"{t.upper():6}ERR {type(e).__name__}: {e}")


if __name__ == "__main__":
    main(sys.argv[1:])

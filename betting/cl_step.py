#!/usr/bin/env python3
"""
UEFA Champions League betting agent — daily step (CL paper lane #2).

Mirror of step.py (EPL lane) pointed at soccer_uefa_champs_league, with its
OWN paper book (book_cl.json) and the SAME gate: >=200 settled bets + avg CLV
>=2% + ROI >=5% before any real money.

Ratings:
  - EPL teams: live values from ratings.json (updated by EPL results only)
  - CL teams: ratings_cl.json, seeded from verified 2025-26 domestic stats
    calibrated by UEFA country coefficients (see seed_cl_calibrate.py) and
    updated ONLY from CL results, so the two lanes never cross-contaminate.
"""
import json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import odds, model, book as bookmod
from step import _deduped, _add_bet, _void_stale_open_bets, HORIZON_DAYS

SPORT = "soccer_uefa_champs_league"
BOOK_PATH = os.path.join(BASE, "book_cl.json")
RATS_EPL = os.path.join(BASE, "ratings.json")
RATS_CL = os.path.join(BASE, "ratings_cl.json")


def load_ratings():
    """Merged view: CL teams (evolving) + EPL teams (live, refreshed daily)."""
    cl = {}
    if os.path.exists(RATS_CL):
        with open(RATS_CL) as f:
            cl = json.load(f)
    epl = {}
    if os.path.exists(RATS_EPL):
        with open(RATS_EPL) as f:
            epl = json.load(f)
    rats = dict(cl)
    rats.update(epl)   # EPL live ratings win on any overlap
    return rats, set(cl.keys())


def save_cl_ratings(rats, cl_keys):
    """Persist only CL-lane teams; EPL teams re-sync from ratings.json daily."""
    out = {t: rats[t] for t in cl_keys if t in rats}
    tmp = RATS_CL + ".tmp"
    with open(tmp, "w") as f:
        json.dump(out, f, indent=1)
    os.replace(tmp, RATS_CL)


def main():
    api_key = odds.get_key()
    bk = bookmod.load(BOOK_PATH)
    rats, cl_keys = load_ratings()
    events = []

    # --- settle + CL rating updates from results ---
    if api_key:
        scores = odds.fetch_scores(api_key, days=3, sport=SPORT)
        for sc in scores:
            if not sc.get("completed"):
                continue
            home, away = odds.norm(sc["home_team"]), odds.norm(sc["away_team"])
            sm = {s["name"]: s["score"] for s in sc.get("scores", [])}
            gh, ga = sm.get(home), sm.get(away)
            if gh is None or ga is None:
                continue
            gh, ga = int(gh), int(ga)
            for b in bk["bets"]:
                if b.get("result") is None and b["home"] == home and b["away"] == away:
                    pnl = bookmod.settle(b, gh, ga)
                    b["clv"] = bookmod.clv_pct(b["odds"], b.get("closing_odds"))
                    bk["bankroll"] = round(bk["bankroll"] + pnl, 2)
                    events.append(f"SETTLE {home} {gh}-{ga} {away} [{b['market']}] "
                                  f"{b['result']} {pnl:+.1f}u")
            if home in rats and away in rats:
                model.update_ratings(rats, home, away, gh, ga)
        save_cl_ratings(rats, cl_keys)
        _void_stale_open_bets(bk, events)

    # --- value scan vs FanDuel (UCL) ---
    if api_key:
        fixtures = odds.parse_fixtures(odds.fetch_odds(api_key, sport=SPORT))
        now = datetime.datetime.now(datetime.timezone.utc)
        for f in fixtures:
            if f["home"] not in rats or f["away"] not in rats:
                continue
            try:
                kick = datetime.datetime.fromisoformat(f["commence"].replace("Z", "+00:00"))
            except Exception:
                continue
            if kick <= now + datetime.timedelta(minutes=30):
                continue
            if kick > now + datetime.timedelta(days=HORIZON_DAYS):
                continue
            lh, la = model.expected_goals(f["home"], f["away"], rats)
            mp = model.match_probs(lh, la)

            h2h = {k: v for k, v in f["h2h"].items() if v}
            if len(h2h) == 3:
                mprobs = {"home": mp["home"], "draw": mp["draw"], "away": mp["away"]}
                for side, price, pmod, edge in bookmod.find_value(mprobs, h2h):
                    mkt = f"h2h_{side}"
                    if _deduped(bk, f["id"], mkt):
                        continue
                    stake = _add_bet(bk, f, side, price, pmod, edge, mkt)
                    events.append(f"BET {f['home']} vs {f['away']} [{mkt}] @ {price:.2f} "
                                  f"(model {pmod:.3f}, edge {edge*100:.1f}%) stake {stake}u")

            tots = {k: v for k, v in f["totals"].items() if v}
            if len(tots) == 2:
                mprobs = {"over25": mp["over25"], "under25": mp["under25"]}
                for side, price, pmod, edge in bookmod.find_value(mprobs, tots):
                    if _deduped(bk, f["id"], side):
                        continue
                    stake = _add_bet(bk, f, side, price, pmod, edge, side)
                    events.append(f"BET {f['home']} vs {f['away']} [{side}] @ {price:.2f} "
                                  f"(model {pmod:.3f}, edge {edge*100:.1f}%) stake {stake}u")

        bookmod.save(bk, BOOK_PATH)

    for ev in events:
        print("EVENT", ev)
    if not events:
        print("NO_EVENTS")
    print("DONE")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        bk = bookmod.load(BOOK_PATH)
        print("⚽ UCL PAPER BOOK (CL lane):\n" + bookmod.report(bk))
    else:
        main()

#!/usr/bin/env python3
"""
EPL betting agent — daily step.

Architecture (mirrors the trading sim):
  scores -> settle paper book + update Poisson ratings
        -> value scan vs FanDuel (model edge >= 4% after vig removal)
        -> quarter-Kelly staking, 0.5-2 units, CLV tracked on every bet
        -> gate: >=200 settled bets + avg CLV >=2% + ROI >=5% before real money

Run daily (cron 10 AM ET). --report for the weekly book summary.
Without ODDS_API_KEY it runs model-only (prints fixture probabilities).
"""
import json, os, sys, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import model, odds, book as bookmod

RATINGS_PATH = os.path.join(BASE, "ratings.json")


def load_ratings():
    if os.path.exists(RATINGS_PATH):
        with open(RATINGS_PATH) as f:
            return json.load(f)
    rats = model.initial_ratings(model.load_seed())
    with open(RATINGS_PATH, "w") as f:
        json.dump(rats, f, indent=1)
    return rats


def save_ratings(rats):
    with open(RATINGS_PATH, "w") as f:
        json.dump(rats, f, indent=1)


def _deduped(bk, event_id, market):
    return any(b.get("event_id") == event_id and b["market"] == market
               and b.get("result") is None for b in bk["bets"])


def _add_bet(bk, f, side, price, p_model, edge, kind):
    stake = bookmod.stake_for(p_model, price, bk["bankroll"])
    bk["bets"].append({
        "event_id": f["id"], "home": f["home"], "away": f["away"],
        "commence": f["commence"], "market": kind, "odds": price,
        "model_prob": p_model, "edge": edge, "stake": stake,
        "entered": str(datetime.date.today()),
        "closing_odds": price, "result": None, "pnl": None,
    })
    return stake


def update_closing(bk, fixtures):
    """Refresh closing odds on open bets from the latest book snapshot."""
    by_id = {f["id"]: f for f in fixtures}
    for b in bk["bets"]:
        if b.get("result") is not None or b["event_id"] not in by_id:
            continue
        f = by_id[b["event_id"]]
        pool = f["h2h"] if b["market"].startswith("h2h") else f["totals"]
        side = b["market"].split("_", 1)[1] if b["market"].startswith("h2h") else b["market"]
        if side in pool and pool[side]:
            b["closing_odds"] = pool[side]


def main():
    api_key = odds.get_key()
    bk = bookmod.load()
    rats = load_ratings()
    events = []

    # --- settle + rating updates from results ---
    if api_key:
        scores = odds.fetch_scores(api_key)
        for sc in scores:
            if not sc.get("completed"):
                continue
            home, away = odds.norm(sc["home_team"]), odds.norm(sc["away_team"])
            sm = {s["name"]: s["score"] for s in sc.get("scores", [])}
            gh, ga = sm.get(home), sm.get(away)
            if gh is None or ga is None:
                continue
            gh, ga = int(gh), int(ga)   # Odds API returns scores as strings
            for b in bk["bets"]:
                if b.get("result") is None and b["home"] == home and b["away"] == away:
                    pnl = bookmod.settle(b, gh, ga)
                    b["clv"] = bookmod.clv_pct(b["odds"], b.get("closing_odds"))
                    bk["bankroll"] = round(bk["bankroll"] + pnl, 2)
                    events.append(f"SETTLE {home} {gh}-{ga} {away} [{b['market']}] "
                                  f"{b['result']} {pnl:+.1f}u")
            if home in rats and away in rats:
                model.update_ratings(rats, home, away, gh, ga)

    # --- value scan vs FanDuel ---
    if api_key:
        fixtures = odds.parse_fixtures(odds.fetch_odds(api_key))
        for f in fixtures:
            if f["home"] not in rats or f["away"] not in rats:
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

        update_closing(bk, fixtures)
        save_ratings(rats)
        bookmod.save(bk)
    else:
        # model-only mode: keep the cron quiet until the odds key lands
        print("MODEL_ONLY — add ODDS_API_KEY to betting/.env to activate the value scan")

    for ev in events:
        print("EVENT", ev)
    if not events:
        print("NO_EVENTS")
    print("DONE")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--report":
        bk = bookmod.load()
        print(bookmod.report(bk))
    else:
        main()

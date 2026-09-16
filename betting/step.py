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

# Never bet fixtures more than this many days out (early FanDuel lines are wide
# and ruin the CLV gate metric). Also guards against betting phantom listings.
HORIZON_DAYS = 7


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


def _iso(dtstr):
    return datetime.datetime.fromisoformat(dtstr.replace("Z", "+00:00"))


def _flag_unresolved(bk, events):
    """Shout about open bets whose fixture kicked off but has no result yet.

    Added 2026-09-16 after the void audit (see _void_stale_open_bets). The old
    code stayed silent for 5 days and then refunded real losses; from now on a
    missing result is visible on the FIRST run after kickoff, so it can be
    verified against a primary source (UEFA.com / ESPN) while it still matters.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    for b in bk["bets"]:
        if b.get("result") is not None:
            continue
        try:
            kick = _iso(b["commence"])
        except Exception:
            continue
        if kick >= now:
            continue
        age = (now - kick).days
        events.append(
            f"UNRESOLVED {b['home']} vs {b['away']} [{b['market']}] — "
            f"kickoff {b['commence']}, no result from the scores feed after "
            f"{age}d. VERIFY vs UEFA/ESPN/BBC before accepting any void.")


def _void_stale_open_bets(bk, events, horizon_days=5):
    """LAST-RESORT void for open bets whose fixture never published a result.

    The Odds API scores endpoint only looks back 3 days, so a bet on a match
    whose result the feed silently dropped would hang open forever otherwise.
    Refund the stake (pnl 0) and mark it void — but NEVER silently.

    2026-09-16 audit: this refunded real matches the feed dropped (Liverpool
    2-1 Atlético, Sporting 3-1 Galatasaray, PSG 6-1 Slovan Bratislava, Chelsea
    4-3 Brighton) — laundering ~5.3u of real losses into 'refunds' and
    inflating both books toward their gates. Every void is now flagged as
    UNVERIFIED and must be checked against a primary source.
    """
    now = datetime.datetime.now(datetime.timezone.utc)
    for b in bk["bets"]:
        if b.get("result") is not None:
            continue
        try:
            kick = _iso(b["commence"])
        except Exception:
            continue
        if (now - kick).days > horizon_days:
            b["result"] = "void"
            b["pnl"] = 0.0
            b["settled"] = str(datetime.date.today())
            b["note"] = ("no result within %dd of kickoff — voided UNVERIFIED "
                         "(feed gap, match may have been played)" % horizon_days)
            events.append(f"⚠️ VOID {b['home']} vs {b['away']} [{b['market']}] "
                          f"(no result — stake refunded) — UNVERIFIED: confirm "
                          f"the fixture was not played before trusting this.")


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
                # score entries may carry unnormalized names — retry via NAME_MAP
                sm = {odds.norm(k): v for k, v in sm.items()}
                gh, ga = sm.get(home), sm.get(away)
            if gh is None or ga is None:
                # Never skip silently: if we hold an open bet on this exact
                # fixture, a score-parse failure is a bug, not a non-event.
                stuck = [b for b in bk["bets"] if b.get("result") is None and
                         (b.get("event_id") == sc.get("id") or
                          (b["home"] == home and b["away"] == away))]
                if stuck:
                    events.append(
                        f"WARN completed fixture {home} vs {away} has no readable "
                        f"score (payload names: {list(sm)}; {len(stuck)} open bet(s)) "
                        f"— result NOT settled, needs a look.")
                continue
            gh, ga = int(gh), int(ga)   # Odds API returns scores as strings
            for b in bk["bets"]:
                if b.get("result") is not None:
                    continue
                # match by event id first (immune to feed name drift), name second
                if not (b.get("event_id") == sc.get("id") or
                        (b["home"] == home and b["away"] == away)):
                    continue
                pnl = bookmod.settle(b, gh, ga)
                b["clv"] = bookmod.clv_pct(b["odds"], b.get("closing_odds"))
                bk["bankroll"] = round(bk["bankroll"] + pnl, 2)
                events.append(f"SETTLE {home} {gh}-{ga} {away} [{b['market']}] "
                              f"{b['result']} {pnl:+.1f}u")
            if home in rats and away in rats:
                model.update_ratings(rats, home, away, gh, ga)
        _flag_unresolved(bk, events)
        _void_stale_open_bets(bk, events)

    # --- value scan vs FanDuel ---
    if api_key:
        fixtures = odds.parse_fixtures(odds.fetch_odds(api_key))
        now = datetime.datetime.now(datetime.timezone.utc)
        for f in fixtures:
            if f["home"] not in rats or f["away"] not in rats:
                continue
            # never bet a fixture already kicked off, or one >HORIZON_DAYS out
            # (wide early lines wreck the CLV gate metric)
            try:
                kick = _iso(f["commence"])
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

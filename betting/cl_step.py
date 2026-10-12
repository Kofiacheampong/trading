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
from step import (_deduped, _add_bet, _void_stale_open_bets, _flag_unresolved,
                  update_closing, HORIZON_DAYS)

# The CL job runs Tue/Wed/Thu at 10:05 ET (cron "5 10 * * 2-4"). The Odds API
# scores endpoint only looks back 3 days, so a fixture whose result cannot be
# picked up by the NEXT run is unsettleable: it would hang open and then get
# voided (see the 2026-09-16 audit). Thursday-slate CL fixtures are exactly
# that case. Keep RUN_DAYS in sync with the cron expression.
RUN_DAYS = {1, 2, 3}            # Mon=0 — Tue/Wed/Thu
SCORES_LOOKBACK_DAYS = 3


def _next_run_after(kick):
    for i in range(1, 8):
        cand = kick.date() + datetime.timedelta(days=i)
        if cand.weekday() in RUN_DAYS:
            return cand
    return None


def _settleable(kick):
    """Can the next scheduled run still see this fixture's result?"""
    nxt = _next_run_after(kick)
    return True if nxt is None else (nxt - kick.date()).days <= SCORES_LOOKBACK_DAYS

SPORT = "soccer_uefa_champs_league"
BOOK_PATH = os.path.join(BASE, "book_cl.json")
RATS_EPL = os.path.join(BASE, "ratings.json")
RATS_CL = os.path.join(BASE, "ratings_cl.json")

# --- CL model v2 (rebuilt 2026-10-12 after the -89.5% ROI audit) -------------
# The crude CL seed (domestic stats squashed by UEFA coefficient ^0.35) was
# massively overconfident on longshots: it priced Porto to beat Man City at 43%
# (market ~19%), Stuttgart away at 11.0 as 29%, and a 51.0 no-hoper at 7%. Every
# longshot got bet and almost all lost. Three guards now bound the damage:
#   SHRINK       : pull CL-only ratings toward the mean so extreme seeds stop
#                  dominating (applied at load time, live updates preserved).
#   MARKET_BLEND : shrink model probs toward vig-free market probs before betting
#                  (weight on the model; 0.5 = half-model/half-market).
#   MAX_EDGE     : reject implausible edges — a "20% edge" from a crude model is
#                  model error, not value.
SHRINK = 0.65
MARKET_BLEND = 0.50
MAX_EDGE = 0.10


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
    # CL-only ratings: shrink toward league mean (EPL live ratings left as-is)
    for t in cl:
        rats[t] = {"attack": round(1 + SHRINK * (cl[t]["attack"] - 1), 3),
                   "defense": round(1 + SHRINK * (cl[t]["defense"] - 1), 3)}
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
                # score entries may carry unnormalized names — retry via NAME_MAP
                sm = {odds.norm(k): v for k, v in sm.items()}
                gh, ga = sm.get(home), sm.get(away)
            if gh is None or ga is None:
                # never skip silently (2026-09-16 audit: this hid real results)
                stuck = [b for b in bk["bets"] if b.get("result") is None and
                         (b.get("event_id") == sc.get("id") or
                          (b["home"] == home and b["away"] == away))]
                if stuck:
                    events.append(
                        f"WARN completed fixture {home} vs {away} has no readable "
                        f"score (payload names: {list(sm)}; {len(stuck)} open bet(s)) "
                        f"— result NOT settled, needs a look.")
                continue
            gh, ga = int(gh), int(ga)
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
        save_cl_ratings(rats, cl_keys)
        _flag_unresolved(bk, events)
        _void_stale_open_bets(bk, events)

    # --- value scan vs FanDuel (UCL) ---
    if api_key:
        fixtures = odds.parse_fixtures(odds.fetch_odds(api_key, sport=SPORT))
        now = datetime.datetime.now(datetime.timezone.utc)
        skipped_unsettleable = []
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
            if not _settleable(kick):
                # Don't open bets we can't settle: the result would age out of
                # the 3-day scores window before the next run (silent void).
                skipped_unsettleable.append(f"{f['home']} vs {f['away']} ({kick.date()})")
                continue
            lh, la = model.expected_goals(f["home"], f["away"], rats)
            mp = model.match_probs(lh, la)

            h2h = {k: v for k, v in f["h2h"].items() if v}
            if len(h2h) == 3:
                mprobs = {"home": mp["home"], "draw": mp["draw"], "away": mp["away"]}
                mprobs = bookmod.blend_with_market(mprobs, h2h, MARKET_BLEND)
                for side, price, pmod, edge in bookmod.find_value(mprobs, h2h, max_edge=MAX_EDGE):
                    mkt = f"h2h_{side}"
                    if _deduped(bk, f["id"], mkt):
                        continue
                    stake = _add_bet(bk, f, side, price, pmod, edge, mkt)
                    events.append(f"BET {f['home']} vs {f['away']} [{mkt}] @ {price:.2f} "
                                  f"(model {pmod:.3f}, edge {edge*100:.1f}%) stake {stake}u")

            tots = {k: v for k, v in f["totals"].items() if v}
            if len(tots) == 2:
                mprobs = {"over25": mp["over25"], "under25": mp["under25"]}
                mprobs = bookmod.blend_with_market(mprobs, tots, MARKET_BLEND)
                for side, price, pmod, edge in bookmod.find_value(mprobs, tots, max_edge=MAX_EDGE):
                    if _deduped(bk, f["id"], side):
                        continue
                    stake = _add_bet(bk, f, side, price, pmod, edge, side)
                    events.append(f"BET {f['home']} vs {f['away']} [{side}] @ {price:.2f} "
                                  f"(model {pmod:.3f}, edge {edge*100:.1f}%) stake {stake}u")

        update_closing(bk, fixtures)
        bookmod.save(bk, BOOK_PATH)
        if skipped_unsettleable:
            events.append("SKIP would-void (result can't be caught by next run): "
                          + "; ".join(skipped_unsettleable))

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

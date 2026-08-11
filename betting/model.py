#!/usr/bin/env python3
"""
Poisson goal model for the Premier League betting agent.
- Team attack/defense ratings from (seed) last-season table, updated live from results.
- Match scoreline matrix -> fair probabilities for h2h and over/under 2.5.
- v1 = plain Poisson (Dixon-Coles low-score correction = future upgrade).
"""
import json, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
LEAGUE_AVG = 1.375          # goals per team per match (2.75/match total)
HOME_SHARE = 0.54           # ~54% of goals scored at home
HOME_AVG = LEAGUE_AVG * 2 * HOME_SHARE
AWAY_AVG = LEAGUE_AVG * 2 * (1 - HOME_SHARE)
DECAY = 0.92                # per-match memory decay for in-season rating updates
ADJ_K = 0.08                # how fast ratings react to results
PROMOTED_ATT, PROMOTED_DEF = 0.90, 1.10   # promoted teams start ~10% below average


def load_seed():
    with open(os.path.join(BASE, "seed.json")) as f:
        return json.load(f)


def initial_ratings(seed):
    """attack/defense ratings from last season's GF/GA (league-mean normalized)."""
    rats = {}
    for team, r in seed["teams"].items():
        if r.get("promoted"):
            rats[team] = {"attack": PROMOTED_ATT, "defense": PROMOTED_DEF}
            continue
        games = r["w"] + r["d"] + r["l"]
        att = (r["gf"] / games) / LEAGUE_AVG
        deff = (r["ga"] / games) / LEAGUE_AVG
        rats[team] = {"attack": round(att, 3), "defense": round(deff, 3)}
    return rats


def expected_goals(home, away, rats):
    """(lambda_home, lambda_away) for a fixture."""
    lh = HOME_AVG * rats[home]["attack"] * rats[away]["defense"]
    la = AWAY_AVG * rats[away]["attack"] * rats[home]["defense"]
    return lh, la


def _pois(l, k):
    return math.exp(-l) * l ** k / math.factorial(k)


def match_probs(lh, la, max_goals=8):
    """Scoreline matrix -> {home, draw, away, over25, under25} probabilities."""
    p = [[_pois(lh, i) * _pois(la, j) for j in range(max_goals + 1)]
         for i in range(max_goals + 1)]
    home = draw = away = over = 0.0
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            if i > j: home += p[i][j]
            elif i == j: draw += p[i][j]
            else: away += p[i][j]
            if i + j > 2: over += p[i][j]
    tot = home + draw + away
    return {"home": home / tot, "draw": draw / tot, "away": away / tot,
            "over25": over / tot, "under25": 1 - over / tot}


def update_ratings(rats, home, away, gh, ga):
    """Bayes-ish rating update after a result (gentle, decayed)."""
    lh, la = expected_goals(home, away, rats)
    # ratio of actual to expected, damped
    fa_h = (gh / lh) if lh > 0 else 1.0
    fa_a = (ga / la) if la > 0 else 1.0
    fd_h = (ga / la) if la > 0 else 1.0   # defense = goals CONCEDED vs expected conceded
    fd_a = (gh / lh) if lh > 0 else 1.0
    r = rats[home]; ra = rats[away]
    r["attack"] = DECAY * r["attack"] + (1 - DECAY) * r["attack"] * (fa_h ** ADJ_K)
    ra["attack"] = DECAY * ra["attack"] + (1 - DECAY) * ra["attack"] * (fa_a ** ADJ_K)
    r["defense"] = DECAY * r["defense"] + (1 - DECAY) * r["defense"] * (fd_h ** ADJ_K)
    ra["defense"] = DECAY * ra["defense"] + (1 - DECAY) * ra["defense"] * (fd_a ** ADJ_K)
    # renormalize to league mean of 1.0
    _norm(rats)
    return rats


def _norm(rats):
    n = len(rats)
    ma = sum(v["attack"] for v in rats.values()) / n
    md = sum(v["defense"] for v in rats.values()) / n
    for v in rats.values():
        v["attack"] = round(v["attack"] / ma, 3)
        v["defense"] = round(v["defense"] / md, 3)


if __name__ == "__main__":
    seed = load_seed()
    rats = initial_ratings(seed)
    for t, v in sorted(rats.items(), key=lambda kv: -kv[1]["attack"]):
        print(f"{t:24s} att {v['attack']:.2f} def {v['defense']:.2f}")
    print("\n--- sample: Arsenal vs Ipswich Town (home) ---")
    lh, la = expected_goals("Arsenal", "Ipswich Town", rats)
    mp = match_probs(lh, la)
    print(f"lambda {lh:.2f}/{la:.2f} | H {mp['home']:.2f} D {mp['draw']:.2f} A {mp['away']:.2f} "
          f"| O2.5 {mp['over25']:.2f} U2.5 {mp['under25']:.2f}")

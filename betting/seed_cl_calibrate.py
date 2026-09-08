#!/usr/bin/env python3
"""
League-strength calibration for the CL ratings seed.

Raw seed_cl ratings normalize each team within its own league (mean 1.0),
which wrongly treats a Norwegian champion as equal to a La Liga champion.
Fix: scale each league by its UEFA 5-year country coefficient relative to
England (squashed with ^0.35 so the spread isn't exaggerated):

    attack_adj  = attack_raw  * S(league)
    defense_adj = defense_raw / S(league)      # lower defense = better

EPL teams keep their live ratings.json numbers (England is the S=1.0 anchor).

Usage: python3 seed_cl_calibrate.py
"""
import json, os, math

BASE = os.path.dirname(os.path.abspath(__file__))
RATS_CL = os.path.join(BASE, "ratings_cl.json")
OUT = os.path.join(BASE, "ratings_cl.json")

# UEFA 5-year association coefficients (2022-23..2026-27, as of 27 Aug 2026)
# Source: en.wikipedia.org/wiki/UEFA_coefficient
COEFF = {
    "England": 102.019, "Italy": 87.874, "Spain": 82.493, "Germany": 80.402,
    "France": 68.153, "Portugal": 64.550, "Belgium": 59.050,
    "Netherlands": 52.395, "Turkey": 49.675, "Greece": 43.812,
    "Norway": 38.612, "Austria": 27.650, "Slovakia": 22.375,
}

# league (as used in seed_cl.json) -> country coeff key
LEAGUE_COUNTRY = {
    "La Liga": "Spain", "Serie A": "Italy", "Ligue 1": "France",
    "Bundesliga": "Germany", "Eredivisie": "Netherlands",
    "Primeira Liga": "Portugal", "Belgian Pro League": "Belgium",
    "Super League Greece": "Greece", "Austrian Bundesliga": "Austria",
    "Eliteserien": "Norway", "Super Lig": "Turkey", "Fortuna Liga": "Slovakia",
}

SEED = json.load(open(os.path.join(BASE, "seed_cl.json")))
LEAGUES = SEED["leagues"]
TEAMS = SEED["teams"]

EXP = 0.35
eng = COEFF["England"]
STRENGTH = {c: (COEFF[c] / eng) ** EXP for c in COEFF}
STRENGTH["England"] = 1.0
for c in STRENGTH:
    print(f"  strength {c:12s} {STRENGTH[c]:.3f}")

out = {}
for league, ldata in LEAGUES.items():
    country = LEAGUE_COUNTRY[league]
    s = STRENGTH[country]
    avg = ldata["avg_goals_per_team"]
    for team, r in TEAMS.get(league, {}).items():
        games = r["w"] + r["d"] + r["l"]
        if games == 0:
            continue
        att_raw = (r["gf"] / games) / avg
        def_raw = (r["ga"] / games) / avg
        out[team] = {
            "attack": round(att_raw * s, 3),
            "defense": round(def_raw / s, 3),
        }

with open(OUT, "w") as f:
    json.dump(out, f, indent=1)
print(f"Wrote {len(out)} calibrated teams to ratings_cl.json")
for t, v in sorted(out.items(), key=lambda kv: -kv[1]["attack"]):
    print(f"  {t:26s} att {v['attack']:.2f} def {v['defense']:.2f}")

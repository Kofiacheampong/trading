#!/usr/bin/env python3
"""
Build CL seed ratings for the UCL betting lane.

Merges:
  1. EPL ratings (ratings.json — in-season, already decayed/updated)
  2. CL teams from seed_cl.json (last-season domestic stats, normalized
     within each team's own league so league quality is treated as ~equal —
     a v1 assumption; CL results will self-correct the ratings over time).

Writes ratings_cl.json = {team: {attack, defense}} for CL opponents NOT in
the EPL set (EPL teams keep their live ratings.json numbers).

Usage: python3 seed_cl_build.py [seed_cl.json]
"""
import json, os, sys, math

BASE = os.path.dirname(os.path.abspath(__file__))
SEED_CL = os.path.join(BASE, sys.argv[1] if len(sys.argv) > 1 else "seed_cl.json")
OUT = os.path.join(BASE, "ratings_cl.json")

# League-quality flattening: ratings normalized to league mean 1.0 (see header)
def initial_ratings_for(seed, league):
    rats = {}
    avg = seed["leagues"][league]["avg_goals_per_team"]
    for team, r in seed["teams"].get(league, {}).items():
        games = r["w"] + r["d"] + r["l"]
        if games == 0:
            continue
        rats[team] = {
            "attack": round((r["gf"] / games) / avg, 3),
            "defense": round((r["ga"] / games) / avg, 3),
        }
    return rats


def main():
    with open(SEED_CL) as f:
        seed = json.load(f)
    epl = {}
    if os.path.exists(os.path.join(BASE, "ratings.json")):
        with open(os.path.join(BASE, "ratings.json")) as f:
            epl = json.load(f)

    out = {}
    for league in seed["leagues"]:
        out.update(initial_ratings_for(seed, league))

    # EPL teams keep their LIVE ratings (they are in ratings.json) — don't
    # overwrite them with stale seed data.
    for t in list(out.keys()):
        if t in epl:
            out[t] = epl[t]

    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"Wrote {len(out)} teams to ratings_cl.json")
    for t, v in sorted(out.items(), key=lambda kv: -kv[1]["attack"]):
        print(f"  {t:26s} att {v['attack']:.2f} def {v['defense']:.2f}")


if __name__ == "__main__":
    main()

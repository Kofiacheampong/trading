#!/usr/bin/env python3
"""
The Odds API wrapper — one free key covers everything:
- FanDuel odds for upcoming EPL fixtures (h2h + totals = O/U 2.5)
- Closing lines (re-fetch before kickoff) for CLV tracking
- Match scores (settles the paper book + feeds the model)

Free tier: 500 requests/month. EPL needs ~15-20/month at 2-3 fetches/fixture-day.
Key: ODDS_API_KEY env var or betting/.env  (signup: the-odds-api.com)
"""
import json, os, subprocess, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SPORT = "soccer_epl"
REGIONS = "us"
BOOK = "fanduel"
MARKETS = "h2h,totals"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

# Odds API team names -> seed names
NAME_MAP = {
    "Brighton and Hove Albion": "Brighton & Hove Albion",
    "Brighton & Hove Albion": "Brighton & Hove Albion",
    "Brighton": "Brighton & Hove Albion",
    "Manchester United": "Manchester United",
    "Man United": "Manchester United",
    "Man Utd": "Manchester United",
    "Man City": "Manchester City",
    "Newcastle": "Newcastle United",
    "Nottingham Forest": "Nottingham Forest",
    "Nott'm Forest": "Nottingham Forest",
    "Tottenham": "Tottenham Hotspur",
    "Spurs": "Tottenham Hotspur",
    "Wolverhampton": "Wolverhampton Wanderers",
    "Wolves": "Wolverhampton Wanderers",
    "Sheffield United": "Sheffield United",
    # CL lane name normalizations (Odds API feed -> seed keys)
    "Atlético Madrid": "Atletico Madrid",
    "Atletico": "Atletico Madrid",
    "Paris Saint Germain": "Paris Saint-Germain",
    "ŠK Slovan Bratislava": "Slovan Bratislava",
    "Sporting Lisbon": "Sporting CP",
    "Sporting": "Sporting CP",
    "Inter": "Inter Milan",
    "PSG": "Paris Saint-Germain",
    "Barcelona": "Barcelona",
}


def get_key():
    k = os.environ.get("ODDS_API_KEY")
    if not k:
        env = os.path.join(BASE, ".env")
        if os.path.exists(env):
            for line in open(env):
                if line.startswith("ODDS_API_KEY="):
                    k = line.strip().split("=", 1)[1]
    return k or None


def norm(name):
    return NAME_MAP.get(name, name)


def _curl(url):
    out = subprocess.run(["curl", "-s", "-m", "20", "-H", f"User-Agent: {UA}", url],
                         capture_output=True, text=True)
    return out.stdout


def fetch_odds(api_key, sport=SPORT):
    """Upcoming events with FanDuel h2h + totals. [] if no key / failure."""
    if not api_key:
        return []
    url = (f"https://api.the-odds-api.com/v4/sports/{sport}/odds/"
           f"?apiKey={api_key}&regions={REGIONS}&markets={MARKETS}"
           f"&bookmakers={BOOK}&oddsFormat=decimal")
    try:
        return json.loads(_curl(url))
    except Exception:
        return []


def fetch_scores(api_key, days=3, sport=SPORT):
    """Completed/recent match results. [] if no key / failure."""
    if not api_key:
        return []
    url = (f"https://api.the-odds-api.com/v4/sports/{sport}/scores/"
           f"?apiKey={api_key}&daysFrom={days}")
    try:
        return json.loads(_curl(url))
    except Exception:
        return []


def parse_fixtures(events):
    """Events -> [{id, commence, home, away, h2h:{home,draw,away}, totals:{over25,under25}}]

    Outcome names from the bookmaker are mapped to canonical sides by comparing
    against the event's home/away teams (anything else = draw), and O/U 2.5
    totals are keyed over25/under25. This fixes the old bug where raw outcome
    names ("chelsea", "over") were stored as keys and never matched the
    home/draw/away or over25/under25 lookups in step.py — the bot could only
    ever bet h2h draws before.
    """
    out = []
    for e in events:
        home, away = norm(e["home_team"]), norm(e["away_team"])
        rec = {"id": e["id"], "commence": e["commence_time"],
               "home": home, "away": away,
               "h2h": {}, "totals": {}}
        for bm in e.get("bookmakers", []):
            if bm.get("key") != BOOK:
                continue
            for m in bm.get("markets", []):
                if m["key"] == "h2h":
                    for o in m["outcomes"]:
                        nm = norm(o["name"])
                        if nm == home:
                            rec["h2h"]["home"] = o["price"]
                        elif nm == away:
                            rec["h2h"]["away"] = o["price"]
                        else:
                            rec["h2h"]["draw"] = o["price"]
                elif m["key"] == "totals":
                    for o in m["outcomes"]:
                        pt = o.get("point") or 2.5
                        if abs(pt - 2.5) < 0.01:
                            key = "over25" if o["name"].lower().startswith("over") else "under25"
                            rec["totals"][key] = o["price"]
        out.append(rec)
    return out


if __name__ == "__main__":
    k = get_key()
    if not k:
        print("NO_KEY — set ODDS_API_KEY in betting/.env (free: the-odds-api.com)")
    else:
        fx = parse_fixtures(fetch_odds(k))
        print(f"fixtures: {len(fx)}")
        for f in fx[:5]:
            print(f"  {f['home']} vs {f['away']} | h2h {f['h2h']} | totals {f['totals']}")

#!/usr/bin/env python3
"""
Paper betting book — the gate before any real money.
- Tracks every bet: entry odds, closing odds (CLV), stake, result, P&L.
- Staking: quarter-Kelly, capped 0.5-2 units. 1 unit = $10 default (Kofi: $5-20).
- Gate (real money): >=200 settled bets AND avg CLV >= 2% AND ROI >= 5%.
- State: betting/book.json
"""
import json, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "book.json")
START_UNITS = 100.0
MAX_UNITS_PER_BET = 2.0
MIN_UNITS_PER_BET = 0.5
KELLY_FRAC = 0.25
MIN_EDGE = 0.04          # only bet when model edge >= 4% after removing vig
GATE_BETS = 200
GATE_CLV = 2.0           # %
GATE_ROI = 5.0           # %


def load():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {"bankroll": START_UNITS, "bets": [], "started": str(datetime.date.today())}


def save(book):
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(book, f, indent=1)
    os.replace(tmp, STATE)


def fair_odds(probs):
    """Decimal fair odds from model probabilities (pre-margin)."""
    return {k: round(1.0 / p, 2) for k, p in probs.items() if p > 0}


def remove_vig(book_odds):
    """Normalize book implied probabilities so they sum to 1."""
    keys = list(book_odds.keys())
    imp = {k: 1.0 / v for k, v in book_odds.items()}
    s = sum(imp.values())
    return {k: imp[k] / s for k in keys}


def find_value(model_probs, book_odds, min_edge=MIN_EDGE):
    """Return [(side, book_price, model_prob, edge)] where model beats the book."""
    fair = remove_vig(book_odds)
    out = []
    for side, p_model in model_probs.items():
        if side not in book_odds:
            continue
        edge = p_model - fair[side]
        if edge >= min_edge:
            out.append((side, book_odds[side], round(p_model, 3), round(edge, 3)))
    return out


def stake_for(p_model, odds, bankroll):
    """Quarter-Kelly, capped 0.5-2 units."""
    b = odds - 1.0
    f = KELLY_FRAC * (b * p_model - 1.0) / b if b > 0 else 0.0
    units = f * bankroll
    return round(min(MAX_UNITS_PER_BET, max(MIN_UNITS_PER_BET, units)), 2)


def settle(bet, home_score, away_score):
    """Resolve one bet -> pnl in units. Mutates bet dict."""
    if bet.get("result") is not None:
        return 0.0
    if bet["market"] == "h2h_home": won = home_score > away_score
    elif bet["market"] == "h2h_draw": won = home_score == away_score
    elif bet["market"] == "h2h_away": won = home_score < away_score
    elif bet["market"] == "over25": won = (home_score + away_score) > 2
    elif bet["market"] == "under25": won = (home_score + away_score) <= 2
    else: won = False
    stake = bet["stake"]
    pnl = round(stake * (bet["odds"] - 1.0), 2) if won else -stake
    bet["result"] = "win" if won else "loss"
    bet["pnl"] = pnl
    bet["settled"] = str(datetime.date.today())
    return pnl


def clv_pct(entry_odds, closing_odds):
    """Positive = you beat the close (got a better price than the market settled on)."""
    if not closing_odds:
        return None
    return round((entry_odds - closing_odds) / closing_odds * 100, 2)


def report(book):
    bets = book["bets"]
    settled = [b for b in bets if b.get("result")]
    lines = [f"⚽ EPL PAPER BOOK — {len(settled)} settled / {len(bets)} total | "
             f"bankroll {book['bankroll']:.1f} units (start {START_UNITS:.0f})"]
    if settled:
        wins = [b for b in settled if b["result"] == "win"]
        wr = len(wins) / len(settled) * 100
        pnl = sum(b["pnl"] for b in settled)
        roi = pnl / (sum(b["stake"] for b in settled)) * 100
        clvs = [b["clv"] for b in settled if b.get("clv") is not None]
        avg_clv = sum(clvs) / len(clvs) if clvs else 0.0
        lines.append(f"  win rate {wr:.0f}% | P&L {pnl:+.1f}u | ROI {roi:+.1f}% | avg CLV {avg_clv:+.2f}%")
        for b in settled[-6:]:
            lines.append(f"  {b['settled']} {b['home']} {b['home_score']}-{b['away_score']} {b['away']} "
                         f"[{b['market']}] {b['result']} {b['pnl']:+.1f}u (odds {b['odds']:.2f})")
        if len(settled) >= GATE_BETS:
            ok = avg_clv >= GATE_CLV and roi >= GATE_ROI
            lines.append(f"  GATE ({GATE_BETS} bets): {'✅ PASSED — real money eligible' if ok else
                         f'NOT passed (need CLV ≥{GATE_CLV}% + ROI ≥{GATE_ROI}%; now {avg_clv:.2f}%/{roi:.1f}%)'}")
        else:
            lines.append(f"  GATE: {len(settled)}/{GATE_BETS} settled — paper season continues")
    else:
        lines.append("  no settled bets yet — first matchday will feed the book")
    return "\n".join(lines)

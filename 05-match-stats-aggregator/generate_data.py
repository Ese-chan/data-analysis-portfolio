"""Generate a synthetic single-match event log (JSON) for Project 05.

Stdlib only. Output: data/match_events.json
"""
import json
import random
from pathlib import Path

random.seed(99)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

TEAMS = {
    "Riverside FC": ["K. Adeyemi", "J. Novak", "T. Silva", "M. Okafor",
                     "L. Bennett", "R. Castellanos", "D. Kimura"],
    "Harbor United": ["A. Petrov", "S. Mensah", "C. Dubois", "F. Haddad",
                      "G. Lindqvist", "P. Alvarez", "N. Ito"],
}

# Each player gets a personality so the summary tells a story.
PERSONAS = {
    "K. Adeyemi": dict(pass_weight=4.0, shot_weight=2.5, goal_weight=1.6),
    "J. Novak": dict(pass_weight=5.0, shot_weight=0.4, goal_weight=0.2),
    "T. Silva": dict(pass_weight=3.0, shot_weight=0.8, goal_weight=0.5),
    "M. Okafor": dict(pass_weight=2.0, shot_weight=3.0, goal_weight=1.4),
    "L. Bennett": dict(pass_weight=2.5, shot_weight=0.5, goal_weight=0.1),
    "R. Castellanos": dict(pass_weight=3.5, shot_weight=1.5, goal_weight=0.9),
    "D. Kimura": dict(pass_weight=4.5, shot_weight=0.3, goal_weight=0.1),
    "A. Petrov": dict(pass_weight=4.5, shot_weight=1.0, goal_weight=0.6),
    "S. Mensah": dict(pass_weight=2.0, shot_weight=3.2, goal_weight=1.7),
    "C. Dubois": dict(pass_weight=3.2, shot_weight=0.6, goal_weight=0.3),
    "F. Haddad": dict(pass_weight=5.0, shot_weight=0.5, goal_weight=0.2),
    "G. Lindqvist": dict(pass_weight=2.2, shot_weight=2.8, goal_weight=1.2),
    "P. Alvarez": dict(pass_weight=3.8, shot_weight=1.2, goal_weight=0.8),
    "N. Ito": dict(pass_weight=4.8, shot_weight=0.4, goal_weight=0.1),
}

events = []
minute = 0
while len(events) < 300:
    team = random.choice(list(TEAMS))
    player = random.choice(TEAMS[team])
    persona = PERSONAS[player]
    r = random.random()
    if r < 0.55:
        etype, outcome = "pass", random.choices(["complete", "incomplete"], [0.8, 0.2])[0]
    elif r < 0.70:
        etype, outcome = "tackle", random.choices(["won", "lost"], [0.6, 0.4])[0]
    elif r < 0.80:
        etype, outcome = "shot", random.choices(["on_target", "off_target"], [0.4, 0.6])[0]
    elif r < 0.88:
        etype, outcome = "foul", None
    elif r < 0.96:
        etype, outcome = "corner", None
    elif r < 0.99:
        etype, outcome = "save", "made"
    else:
        etype, outcome = "goal", None
    events.append({
        "minute": minute,
        "team": team,
        "player": player,
        "event_type": etype,
        "detail": {"outcome": outcome} if outcome else {},
    })
    # a few events share the same minute, like a real match feed
    minute = min(90, minute + random.choices([0, 1], [5, 3])[0])

match = {
    "match_id": "FR-2025-091",
    "date": "2025-09-14",
    "competition": "Friendly",
    "home_team": "Riverside FC",
    "away_team": "Harbor United",
    "events": events,
}

out = DATA_DIR / "match_events.json"
out.write_text(json.dumps(match, indent=2), encoding="utf-8")
print(f"Wrote {len(events)} events to {out}")

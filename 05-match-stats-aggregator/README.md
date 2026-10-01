# Project 05 — Single-Match Player Stat Sheet Aggregator

**Domain:** Sports · **Focus:** Parsing JSON and aggregating event counts

## Goal

Parse a raw JSON file of match events and compile an **automated post-match
summary report** (passes, tackles, shots, goals) per player and per team.

## Skills shown

- Handling a non-relational format (nested JSON)
- Aggregating event counts accurately with Pandas
- Turning raw events into a human-readable report

## Data

Run `python generate_data.py` to create `data/match_events.json` — one friendly
match, ~300 events with nested structure:

```json
{
  "match_id": "FR-2025-091",
  "competition": "Friendly",
  "home_team": "Riverside FC",
  "away_team": "Harbor United",
  "events": [
    {"minute": 3, "team": "Riverside FC", "player": "K. Adeyemi",
     "event_type": "pass", "detail": {"outcome": "complete"}}
  ]
}
```

Event types: `pass`, `tackle`, `shot`, `goal`, `save`, `foul`, `corner`.

## Tasks

- [x] Load the JSON (stdlib `json` or `pandas.read_json`) and flatten `events` into a DataFrame
- [x] Event counts per player per type (pivot table)
- [x] Per team: total shots, total goals, pass completion rate (from `detail.outcome`)
- [x] Answer in code: top scorer, most passes, most tackles
- [x] Export `data/match_summary_players.csv` and print a short text report
- [x] Stretch: add minutes played per player (first/last event minute as an approximation)

## Hints

```python
import json
with open("data/match_events.json", encoding="utf-8") as f:
    match = json.load(f)
events = pd.DataFrame(match["events"])
events.groupby(["team", "player", "event_type"]).size().unstack(fill_value=0)
```

## Results

From 300 raw events, **Riverside FC beat Harbor United 2–0** (goals from D. Kimura and K. Adeyemi) — but the shot count tells a different story: Harbor out-shot Riverside **15–10** (8 on target vs 5) and simply didn't convert. The real difference was ball retention: Riverside completed **81.7%** of their 93 passes against Harbor's 69.3% of 75, and won the tackle battle 24–15.

Standouts: **K. Adeyemi** was Riverside's engine — 1 goal, 13 passes at 76.9%, and a match-high 5 tackles; **L. Bennett** led all passers (18, 88.9% complete); **N. Ito** was Harbor's cleanest distributor (90% completion) while **S. Mensah** did most of their shooting (4 shots) without reward. Full per-player sheet with minutes, event counts, and pass completion: `data/match_summary_players.csv`.

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

- [ ] Load the JSON (stdlib `json` or `pandas.read_json`) and flatten `events` into a DataFrame
- [ ] Event counts per player per type (pivot table)
- [ ] Per team: total shots, total goals, pass completion rate (from `detail.outcome`)
- [ ] Answer in code: top scorer, most passes, most tackles
- [ ] Export `data/match_summary_players.csv` and print a short text report
- [ ] Stretch: add minutes played per player (first/last event minute as an approximation)

## Hints

```python
import json
with open("data/match_events.json", encoding="utf-8") as f:
    match = json.load(f)
events = pd.DataFrame(match["events"])
events.groupby(["team", "player", "event_type"]).size().unstack(fill_value=0)
```

## Results

(your findings here)

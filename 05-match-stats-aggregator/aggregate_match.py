"""Project 05 — Compile a post-match stat sheet from raw JSON events.

Loads data/match_events.json, flattens the nested event list, builds a
player × event-type pivot, computes per-team totals (shots, goals, pass
completion), finds the top scorer / passer / tackler, and writes the player
summary to CSV plus a human-readable text report.

Outputs:
    data/match_summary_players.csv
    (console) the text report
"""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).parent

with (BASE / "data" / "match_events.json").open(encoding="utf-8") as f:
    match = json.load(f)

events = pd.json_normalize(match["events"])          # detail.outcome -> column
events["outcome"] = events["detail.outcome"].fillna("")

# ------------------------------------------------- player x event_type pivot
pivot = (
    events.groupby(["team", "player", "event_type"]).size()
    .unstack("event_type", fill_value=0)
)
for col in ["pass", "tackle", "shot", "goal", "save", "foul", "corner"]:
    if col not in pivot.columns:
        pivot[col] = 0
pivot = pivot[["pass", "tackle", "shot", "goal", "save", "foul", "corner"]]

# ------------------------------------------------- minutes played (stretch:
# first/last event minute as an approximation)
mins = events.groupby("player")["minute"].agg(first_min="min", last_min="max")

passes = events[(events["event_type"] == "pass")]
pass_total = passes.groupby("player").size()
pass_complete = passes[passes["outcome"] == "complete"].groupby("player").size()

players = pivot.reset_index().merge(mins, on="player")
players["pass_completion_pct"] = (
    (pass_complete / pass_total * 100).round(1).reindex(players["player"]).fillna(0).values
)
players["minutes_played"] = players["last_min"] + 1
players = players.sort_values(["team", "goal", "shot"], ascending=[True, False, False])

out_cols = ["player", "team", "minutes_played", "pass", "tackle", "shot", "goal",
            "save", "foul", "corner", "pass_completion_pct"]
players[out_cols].to_csv(BASE / "data" / "match_summary_players.csv", index=False)

# ------------------------------------------------- team totals
teams = {}
for team in [match["home_team"], match["away_team"]]:
    t = events[events["team"] == team]
    tp = t[t["event_type"] == "pass"]
    teams[team] = {
        "goals": int((t["event_type"] == "goal").sum()),
        "shots": int((t["event_type"] == "shot").sum()),
        "shots_on_target": int(((t["event_type"] == "shot") & (t["outcome"] == "on_target")).sum()),
        "passes": len(tp),
        "pass_pct": round((tp["outcome"] == "complete").mean() * 100, 1),
        "tackles": int((t["event_type"] == "tackle").sum()),
        "fouls": int((t["event_type"] == "foul").sum()),
    }

# ------------------------------------------------- leaders
def leader(stat, df=events):
    top = df[df["event_type"] == stat].groupby(["team", "player"]).size()
    (team, player), n = top.idxmax(), top.max()
    return player, team, n

top_scorer = leader("goal")
top_passer = leader("pass")
top_tackler = leader("tackle")

# ------------------------------------------------- text report
h, a = teams[match["home_team"]], teams[match["away_team"]]
print(f"MATCH REPORT — {match['match_id']} ({match['competition']}, {match['date']})")
print(f"{match['home_team']} vs {match['away_team']}")
print(f"  events parsed: {len(events)}\n")
print(f"{'':16} {match['home_team']:>14} {match['away_team']:>14}")
print(f"{'goals':16} {h['goals']:>14} {a['goals']:>14}")
print(f"{'shots':16} {h['shots']:>10} ({h['shots_on_target']} on tgt)"
      f" {a['shots']:>4} ({a['shots_on_target']} on tgt)"[:60])
print(f"{'passes':16} {h['passes']:>14} {a['passes']:>14}")
print(f"{'pass completion':16} {h['pass_pct']:>13}% {a['pass_pct']:>13}%")
print(f"{'tackles':16} {h['tackles']:>14} {a['tackles']:>14}")
print(f"{'fouls':16} {h['fouls']:>14} {a['fouls']:>14}\n")
print(f"Top scorer : {top_scorer[0]} ({top_scorer[1]}) — {top_scorer[2]} goals")
print(f"Most passes: {top_passer[0]} ({top_passer[1]}) — {top_passer[2]} passes")
print(f"Most tackles: {top_tackler[0]} ({top_tackler[1]}) — {top_tackler[2]} tackles")
print("\nPlayer stat sheet:")
print(players[out_cols].to_string(index=False))
print(f"\nSaved {BASE / 'data' / 'match_summary_players.csv'}")

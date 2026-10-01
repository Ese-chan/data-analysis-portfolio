# Project 06 — Basic Player Distance & Sprint Visualizer

**Domain:** Sports · **Focus:** First 2D spatial chart from raw coordinates

## Goal

Plot raw GPS snapshots of one player on a football pitch with Matplotlib to
show **pitch coverage**, and compute total distance covered.

## Skills shown

- Generating 2D spatial charts from raw coordinate data
- Working with a coordinate system (pitch dimensions, axes, limits)
- Turning scatter points into an insight (where did the player actually run?)

## Data

Run `python generate_data.py` to create `data/gps_track.csv` — 10 minutes of
1-second GPS snapshots for a single player on a standard pitch
(**105 m × 68 m**), including standing phases, jogging, and two sprints.

| column | meaning |
|--------|---------|
| `timestamp` | second-by-second snapshot |
| `player_id` | one tracked player |
| `x_m` / `y_m` | position on pitch (origin at corner) |

## Tasks

- [x] Load the CSV and sanity-check that x is within 0–105 and y within 0–68
- [x] Scatter plot of all positions, colored by time (add a colorbar)
- [x] Set axis limits to the pitch and give it sensible labels/title
- [x] Save the chart as `pitch_coverage.png`
- [x] Compute total distance covered: sum of point-to-point distances
- [x] Stretch: draw the pitch lines (outer rectangle, halfway line, center circle) under the scatter
- [x] Stretch: color points by speed instead of time — `pitch_coverage_speed.png`

## Hints

```python
import numpy as np
dist = np.hypot(np.diff(df["x_m"]), np.diff(df["y_m"])).sum()
plt.scatter(df["x_m"], df["y_m"], c=range(len(df)), s=8, cmap="viridis")
plt.colorbar(label="snapshot #")
```

## Results

Player P07 covered **1,463 m in 10 minutes** (mean speed 2.4 m/s, peak 9.1 m/s), of which **471 m was sprinting** — two sprints of ~230 m and ~240 m at snapshots **181–208 and 421–448** (minutes ~3 and ~7), visible as the bright streaks in the speed-colored chart. The time-colored chart shows the player starting near midfield, drifting toward the right flank, and settling into a stand around snapshots 500–560; by speed, everything else is walking/jogging (dark/purple) with the sprints popping instantly. One honest data note: after the second sprint the track hugs the right touchline — the snapshots clamp at x = 104.5, so the player "bounces" against the boundary rather than turning back.

*Distance uses `numpy.hypot` over consecutive points (1 s apart, so m ≈ m/s). Built by `plot_gps_track.py`.*

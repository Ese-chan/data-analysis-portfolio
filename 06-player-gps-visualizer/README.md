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

- [ ] Load the CSV and sanity-check that x is within 0–105 and y within 0–68
- [ ] Scatter plot of all positions, colored by time (add a colorbar)
- [ ] Set axis limits to the pitch and give it sensible labels/title
- [ ] Save the chart as `pitch_coverage.png`
- [ ] Compute total distance covered: sum of point-to-point distances
- [ ] Stretch: draw the pitch lines (outer rectangle, halfway line, center circle) under the scatter
- [ ] Stretch: color points by speed instead of time — can you spot the two sprints?

## Hints

```python
import numpy as np
dist = np.hypot(np.diff(df["x_m"]), np.diff(df["y_m"])).sum()
plt.scatter(df["x_m"], df["y_m"], c=range(len(df)), s=8, cmap="viridis")
plt.colorbar(label="snapshot #")
```

## Results

(your findings here — total distance, sprint moments, what the chart shows)

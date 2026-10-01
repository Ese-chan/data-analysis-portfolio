"""Project 06 — Plot one player's GPS track on a football pitch.

Loads data/gps_track.csv (600 one-second snapshots), sanity-checks the pitch
bounds, draws the positions as a scatter with pitch markings underneath, and
computes total distance covered from point-to-point distances.

Outputs:
    pitch_coverage.png        (positions colored by snapshot #)
    pitch_coverage_speed.png  (stretch: positions colored by speed -> sprints pop out)
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).parent
PITCH_W, PITCH_H = 105.0, 68.0
SPRINT_SPEED = 7.0          # m/s threshold that counts as a sprint

df = pd.read_csv(BASE / "data" / "gps_track.csv")

# ------------------------------------------------------------- sanity check
assert df["x_m"].between(0, PITCH_W).all(), "x out of pitch bounds!"
assert df["y_m"].between(0, PITCH_H).all(), "y out of pitch bounds!"
print(f"Sanity check OK: {len(df)} snapshots, x within [0, {PITCH_W}], y within [0, {PITCH_H}]")

# ------------------------------------------------------------- distance
step_dist = np.hypot(np.diff(df["x_m"]), np.diff(df["y_m"]))
total_m = step_dist.sum()
speed = np.concatenate([[0.0], step_dist])            # m/s (1 s between snapshots)
df["speed"] = speed
print(f"Total distance covered: {total_m:.0f} m  ({total_m / 1000:.2f} km)")
print(f"Mean speed: {speed.mean():.1f} m/s, peak speed: {speed.max():.1f} m/s")

# sprint windows = contiguous runs above the threshold (3 s smoothing)
smooth = pd.Series(speed).rolling(3, center=True).mean()
sprint_bool = smooth > SPRINT_SPEED                 # boolean mask for indexing
sprint_id = sprint_bool.astype(int).diff().fillna(0).abs().cumsum()
windows = []
for _, grp in df[sprint_bool].groupby(sprint_id[sprint_bool]):
    windows.append((grp.index[0], grp.index[-1]))
sprint_m = float(step_dist[sprint_bool.values[: len(step_dist)]].sum())
print("Sprint windows (snapshot #): "
      + ", ".join(f"{a}-{b}" for a, b in windows)
      + f"  -> {sprint_m:.0f} m of sprinting")


# ------------------------------------------------------------- pitch drawing
def draw_pitch(ax):
    """Outer rectangle, halfway line, center circle + spot."""
    ax.plot([0, PITCH_W, PITCH_W, 0, 0], [0, 0, PITCH_H, PITCH_H, 0],
            color="white", lw=1.5, zorder=1)
    ax.plot([PITCH_W / 2, PITCH_W / 2], [0, PITCH_H], color="white", lw=1.5, zorder=1)
    center = plt.Circle((PITCH_W / 2, PITCH_H / 2), 9.15, color="white",
                        fill=False, lw=1.5, zorder=1)
    ax.add_patch(center)
    ax.plot(PITCH_W / 2, PITCH_H / 2, "o", color="white", ms=4, zorder=1)


def pitch_axes(ax, title):
    ax.set_xlim(0, PITCH_W)
    ax.set_ylim(0, PITCH_H)
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(title, fontsize=13, pad=12)
    ax.set_facecolor("#2e7d32")          # grass green so white lines read like a pitch
    ax.tick_params(colors="white")
    for spine in ax.spines.values():
        spine.set_color("white")


# ------------------------------------------------------------- chart 1: time
fig, ax = plt.subplots(figsize=(12, 8))
sc = ax.scatter(df["x_m"], df["y_m"], c=np.arange(len(df)), s=10,
                cmap="viridis", zorder=2)
draw_pitch(ax)
pitch_axes(ax, f"Player {df['player_id'][0]} pitch coverage — 10 min, "
               f"{total_m:.0f} m covered (color = snapshot #)")
cbar = fig.colorbar(sc, ax=ax, shrink=0.8)
cbar.set_label("snapshot # (0 = kick-off)")
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "pitch_coverage.png", dpi=150, facecolor="white")
plt.close(fig)

# ------------------------------------------------------------- chart 2: speed
fig, ax = plt.subplots(figsize=(12, 8))
sc = ax.scatter(df["x_m"], df["y_m"], c=df["speed"], s=10,
                cmap="plasma", vmin=0, vmax=9, zorder=2)
draw_pitch(ax)
pitch_axes(ax, f"Same track colored by speed — the two sprints are unmistakable "
               f"(>{SPRINT_SPEED} m/s)")
cbar = fig.colorbar(sc, ax=ax, shrink=0.8)
cbar.set_label("speed (m/s)")
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "pitch_coverage_speed.png", dpi=150, facecolor="white")
plt.close(fig)

print(f"Saved pitch_coverage.png and pitch_coverage_speed.png")

"""Project 07 — Python chart: steel yield vs concrete compressive strength.

Plots one bar per material, colored by type (steel navy, concrete gray), with
MPa values labeled, and saves material_strength.png next to the workbook.
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

BASE = Path(__file__).parent
COLORS = {"steel": "#1B2A4A", "concrete": "#8C8A84"}   # design tokens

df = pd.read_csv(BASE / "data" / "materials.csv")
df["label"] = df["material"] + "\n(" + df["strength_kind"] + ")"

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(df["label"], df["strength_mpa"],
              color=[COLORS[t] for t in df["type"]])
ax.bar_label(bars, fmt="%d", padding=2, fontsize=10)

ax.set_title("Steel yield strength vs concrete compressive strength",
             fontsize=14, pad=15)
ax.set_ylabel("Strength (MPa)")
ax.set_ylim(0, df["strength_mpa"].max() * 1.15)
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(handles=[Patch(color=COLORS["steel"], label="Steel (yield strength)"),
                   Patch(color=COLORS["concrete"], label="Concrete (compressive strength)")],
          loc="upper left")
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "material_strength.png", dpi=150, facecolor="white")
plt.close(fig)
print("Saved material_strength.png")

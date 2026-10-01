"""Project 02 — Hourly parking occupancy rates per lot (Pandas).

Reads data/parking_entries.csv, computes the occupancy rate for every
snapshot, aggregates it per lot per hour of day, finds the busiest hour
across all lots, and exports a tidy summary plus a chart.

Outputs:
    data/hourly_occupancy_summary.csv
    hourly_occupancy.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE = Path(__file__).parent

df = pd.read_csv(BASE / "data" / "parking_entries.csv", parse_dates=["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["occupancy_rate"] = (df["occupied_spaces"] / df["total_spaces"]).round(3)

# Tidy summary: mean occupancy rate per lot per hour of day (0-23)
summary = (
    df.groupby(["hour", "lot_id"])["occupancy_rate"]
    .mean()
    .round(3)
    .unstack("lot_id")
)
summary["all_lots"] = summary.mean(axis=1).round(3)
summary.index.name = "hour_of_day"
summary.to_csv(BASE / "data" / "hourly_occupancy_summary.csv")

# Busiest single hour across all lots (mean rate over the whole period)
busiest_hour = summary["all_lots"].idxmax()
busiest_rate = summary["all_lots"].max()

print(f"Rows: {len(df):,} snapshots, {df['timestamp'].max() - df['timestamp'].min()}")
print("\nMean occupancy rate by hour of day:")
print(summary.to_string())
print(f"\nBusiest hour across all lots: {busiest_hour:02d}:00 (mean rate {busiest_rate:.1%})")
for lot in summary.columns.drop("all_lots"):
    peak = summary[lot].idxmax()
    print(f"  lot {lot}: peak at {peak:02d}:00 ({summary.loc[peak, lot]:.1%}), "
          f"14-day mean {df[df['lot_id'] == lot]['occupancy_rate'].mean():.1%}")

# One line per lot, hour vs occupancy rate
fig, ax = plt.subplots(figsize=(10, 6))
for lot in summary.columns.drop("all_lots"):
    ax.plot(summary.index, summary[lot], marker="o", markersize=4, label=f"Lot {lot}")
ax.plot(summary.index, summary["all_lots"], "--", color="gray", linewidth=1.5,
        label="All lots")
ax.set_title("Average hourly parking occupancy by lot (Sep 1–14, 2025)", fontsize=14, pad=15)
ax.set_xlabel("Hour of day")
ax.set_ylabel("Mean occupancy rate")
ax.set_xticks(range(0, 24, 2))
ax.set_ylim(0, 1)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper left")
fig.tight_layout(pad=2.0)
fig.savefig(BASE / "hourly_occupancy.png", dpi=150, facecolor="white")
plt.close(fig)
print(f"\nSaved {BASE / 'data' / 'hourly_occupancy_summary.csv'} and hourly_occupancy.png")

"""Generate material property and beam load tables for Project 07.

Stdlib only. Outputs: data/materials.csv, data/beams.csv
"""
import csv
import random
from pathlib import Path

random.seed(3)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# material, type, strength_mpa, strength_kind, density_kg_m3, cost_per_m3
MATERIALS = [
    ["Steel A36",        "steel",    250, "yield",        7850, 1250],
    ["Steel S355",       "steel",    355, "yield",        7850, 1420],
    ["Steel S460",       "steel",    460, "yield",        7850, 1680],
    ["Concrete C25/30",  "concrete",  25, "compressive",  2400,  180],
    ["Concrete C40/50",  "concrete",  40, "compressive",  2400,  240],
    ["Concrete C60/75",  "concrete",  60, "compressive",  2400,  310],
]

out = DATA_DIR / "materials.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["material", "type", "strength_mpa", "strength_kind",
                     "density_kg_m3", "cost_per_m3"])
    writer.writerows(MATERIALS)
print(f"Wrote {out}")

# 10 beams with applied loads chosen to make some beams overstressed.
out = DATA_DIR / "beams.csv"
with out.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["beam_id", "material", "section_factor_kn", "applied_load_kn", "span_m"])
    for i in range(1, 11):
        material = random.choice(MATERIALS)[0]
        section = random.choice([40, 60, 80, 100])          # kN the section can carry per MPa
        allowable = section * dict((m[0], m[2]) for m in MATERIALS)[material] / 1000
        applied = round(allowable * random.uniform(0.5, 1.35), 1)
        writer.writerow([f"B-{i:03d}", material, section, applied, random.choice([4, 6, 8])])
print(f"Wrote {out}")

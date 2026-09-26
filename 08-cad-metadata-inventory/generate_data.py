"""Create a dummy CAD folder to inventory for Project 08.

Stdlib only. Output: sample_cad_files/ (18 dummy binary files)

Files are small random bytes; modification dates are spread across 2024-2025
so the inventory has something interesting to report.
"""
import os
import random
import time
from datetime import datetime, timedelta
from pathlib import Path

random.seed(77)

BASE = Path(__file__).parent / "sample_cad_files"
BASE.mkdir(exist_ok=True)

PREFIXES = ["BRG", "TUN", "WTP", "PLT"]      # bridge, tunnel, water treatment plant, plant layout
TYPES = ["DRW", "MDL", "PLN"]
DESCRIPTIONS = ["site_plan", "deck_section", "elevation", "piping_layout",
                "foundation_detail", "general_arrangement", "rebar_schedule"]
EXTENSIONS = [".dwg", ".dxf", ".rvt", ".pdf"]

made = 0
for i in range(1, 19):
    project = random.choice(PREFIXES)
    ftype = random.choice(TYPES)
    desc = random.choice(DESCRIPTIONS)
    ext = random.choice(EXTENSIONS)
    name = f"{project}-{ftype}-{i:03d}_{desc}{ext}"
    path = BASE / name
    size = random.randint(12_000, 90_000)     # 12-90 KB of dummy bytes
    path.write_bytes(random.randbytes(size))
    # spread modification times over 2024-2025
    mtime = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 600))).timestamp()
    os.utime(path, (mtime, mtime))
    made += 1

print(f"Created {made} dummy files in {BASE}")

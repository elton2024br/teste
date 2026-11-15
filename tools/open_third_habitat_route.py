"""Open the short provisional trail out of Campo Cerrado.

Route 2 still uses inherited scenery with a one-way ledge. Until its final
redesign, these three blocks lead around the agent to the Caatinga trigger.
"""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/Route2/map.bin"
WIDTH = 24
HEIGHT = 80
# 0x30D4 is the ordinary walkable ground already used by Route 2's path.
WALKABLE_GROUND = 0x30D4
TRAIL_X = 10
TRAIL_Y = range(69, 72)


blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
for y in TRAIL_Y:
    blocks[y * WIDTH + TRAIL_X] = WALKABLE_GROUND
MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
print("Opened the Campo Cerrado trail to the Caatinga transition.")

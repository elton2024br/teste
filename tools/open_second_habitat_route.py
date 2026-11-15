"""Open the two-tile north exit from the first habitat.

The route uses the existing walkable forest ground metatile and preserves the
elevation bits already used by the interior path. The script is intentionally
small and idempotent so the binary layout change can be reproduced.
"""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/ViridianForest/map.bin"
WIDTH = 24
HEIGHT = 20
WALKABLE_GROUND = 0x3011
EXIT_CELLS = ((11, 0), (12, 0))


blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
for x, y in EXIT_CELLS:
    index = y * WIDTH + x
    assert blocks[index] in (0x341C, WALKABLE_GROUND), (x, y, blocks[index])
    blocks[index] = WALKABLE_GROUND
MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
print("Opened the first habitat north exit at (11,0) and (12,0).")

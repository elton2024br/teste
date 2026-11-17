"""Replace the inherited water-looking final corridor with dry rare-land ground."""

from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/CeruleanCity/map.bin"
WIDTH = 48
HEIGHT = 40
GROUND_METATILE = 0x0D9
CELLS = {(x, y) for x in range(4, 7) for y in range(5, 12)}
EXPECTED_OLD = {0x128, 0x12A, 0x12B, 0x12C, GROUND_METATILE}

blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
for x, y in sorted(CELLS):
    index = y * WIDTH + x
    old_metatile = blocks[index] & 0x3FF
    assert old_metatile in EXPECTED_OLD, (x, y, hex(blocks[index]))
    blocks[index] = (blocks[index] & 0xFC00) | GROUND_METATILE

MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
print(f"Installed dry metatile {GROUND_METATILE:#x} in {len(CELLS)} rare-land cells; attributes preserved.")

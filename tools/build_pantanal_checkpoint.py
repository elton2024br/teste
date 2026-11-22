"""Install a small flooded Pantanal checkpoint without moving campaign cells."""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/Route4/map.bin"
WIDTH = 108
HEIGHT = 20

GRASS_METATILE = 0x008
WATER_METATILE = 0x12B
ISLAND_CELLS = {(x, y) for x in range(4, 8) for y in range(8, 11)}
WATER_CELLS = ({(3, y) for y in range(8, 11)}
               | {(8, y) for y in range(8, 11)})
CAMPAIGN_CELLS = {(5, 8), (5, 9), (6, 9)}
EXPECTED_OLD = {0x0D9, 0x0B7, 0x00D, 0x0D1, GRASS_METATILE, WATER_METATILE}


def main():
    blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
    assert CAMPAIGN_CELLS <= ISLAND_CELLS
    for x, y in sorted(ISLAND_CELLS | WATER_CELLS):
        index = y * WIDTH + x
        old_metatile = blocks[index] & 0x3FF
        assert old_metatile in EXPECTED_OLD, (x, y, hex(blocks[index]))
        new_metatile = GRASS_METATILE if (x, y) in ISLAND_CELLS else WATER_METATILE
        blocks[index] = (blocks[index] & 0xFC00) | new_metatile
    MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
    print("Installed 12 grass and 6 calm-water Pantanal checkpoint cells; attributes preserved.")


if __name__ == "__main__":
    main()

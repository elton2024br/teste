"""Install a dry Caatinga clearing around the third mission.

The campaign still reuses Pewter City's wider layout.  This localized patch
replaces only the inherited plaza beneath the mission agent and its approach
with the walkable dry-ground metatile already used by the campaign trail.
Object positions, the eastbound trigger and the layout attributes stay intact.
"""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/PewterCity/map.bin"
WIDTH = 48
HEIGHT = 40

DRY_GROUND_METATILE = 0x0D4
# Four flowering cells remain as small islands of drought-resistant growth.
BLOOM_CELLS = {(29, 8), (31, 8), (28, 9), (30, 9)}
CLEARING_CELLS = ({(x, y) for x in range(20, 32) for y in range(8, 12)}
                  - BLOOM_CELLS)
CAMPAIGN_CELLS = {(23, 8), (23, 9), (24, 9)}
EXPECTED_OLD = {
    0x001, 0x008, 0x009, 0x1B9, 0x1BA, 0x1C1, 0x1C2, 0x1C3, 0x1C9,
    DRY_GROUND_METATILE,
}


def main():
    blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
    assert CAMPAIGN_CELLS <= CLEARING_CELLS
    for x, y in sorted(CLEARING_CELLS):
        index = y * WIDTH + x
        old_metatile = blocks[index] & 0x3FF
        assert old_metatile in EXPECTED_OLD, (x, y, hex(blocks[index]))
        blocks[index] = (blocks[index] & 0xFC00) | DRY_GROUND_METATILE
    MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
    print("Installed 44 dry-ground Caatinga clearing cells; four blooms preserved.")


if __name__ == "__main__":
    main()

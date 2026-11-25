"""Install a small dry Caatinga clearing around the third mission.

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
CLEARING_CELLS = {
    (20, 8), (21, 8), (22, 8), (23, 8), (24, 8),
    (20, 9), (21, 9), (22, 9), (23, 9), (24, 9),
    (20, 10), (21, 10), (22, 10), (23, 10), (24, 10),
    (20, 11), (21, 11), (22, 11), (23, 11), (24, 11),
}
CAMPAIGN_CELLS = {(23, 8), (23, 9), (24, 9)}
EXPECTED_OLD = {
    0x1B9, 0x1BA, 0x1C1, 0x1C2, 0x1C3, 0x1C9, DRY_GROUND_METATILE
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
    print("Installed 20 dry-ground Caatinga clearing cells; attributes preserved.")


if __name__ == "__main__":
    main()

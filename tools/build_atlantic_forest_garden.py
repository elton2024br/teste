"""Add a small flowering patch beside the Mata Atlântica mission.

The flowers sit east of the Pantanal transition trigger, outside the campaign
corridor.  The converter keeps the existing elevation/collision attributes and
does not move the agent, player entry or trigger cells.
"""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/Route3/map.bin"
WIDTH = 84
HEIGHT = 20

FLOWER_METATILE = 0x004
FLOWER_CELLS = {(8, 8), (11, 8), (9, 10), (12, 10)}
CAMPAIGN_CELLS = {(5, 8), (5, 9), (6, 9)}
EXPECTED_OLD = {0x008, 0x010, FLOWER_METATILE}


def main():
    blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
    assert FLOWER_CELLS.isdisjoint(CAMPAIGN_CELLS)
    for x, y in sorted(FLOWER_CELLS):
        index = y * WIDTH + x
        old_metatile = blocks[index] & 0x3FF
        assert old_metatile in EXPECTED_OLD, (x, y, hex(blocks[index]))
        blocks[index] = (blocks[index] & 0xFC00) | FLOWER_METATILE
    MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
    print("Installed four flowering Mata Atlântica cells; attributes preserved.")


if __name__ == "__main__":
    main()

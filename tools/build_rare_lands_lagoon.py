"""Replace the inherited gym beside the final circle with a calm lagoon."""

from pathlib import Path
import struct


ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "pokefirered/data/layouts/CeruleanCity/map.bin"
WIDTH = 48
HEIGHT = 40
WATER = 0x12B
WATER_RIGHT_EDGE = 0x12C
CELLS = {
    (x, y): WATER_RIGHT_EDGE if x == 20 else WATER
    for y in range(5, 12)
    for x in range(8, 21)
}
EXPECTED_OLD = {
    0x001, 0x004, 0x005, 0x008, 0x009,
    0x0D3, 0x0D4, 0x0D5, 0x0DF,
    0x12B, 0x12C,
    0x290, 0x298,
    0x2A7, 0x2A8, 0x2A9, 0x2AA, 0x2AB, 0x2AC, 0x2AD, 0x2AE, 0x2AF,
    0x2B0, 0x2B1, 0x2B2, 0x2B6, 0x2B7, 0x2B8, 0x2BA,
    0x2BD, 0x2BF, 0x2C1, 0x2C2, 0x2C3, 0x2C4,
}


def main():
    blocks = list(struct.unpack(f"<{WIDTH * HEIGHT}H", MAP.read_bytes()))
    for (x, y), replacement in sorted(CELLS.items()):
        index = y * WIDTH + x
        old_metatile = blocks[index] & 0x3FF
        assert old_metatile in EXPECTED_OLD, (x, y, hex(blocks[index]))
        blocks[index] = (blocks[index] & 0xFC00) | replacement
    MAP.write_bytes(struct.pack(f"<{WIDTH * HEIGHT}H", *blocks))
    print(
        f"Installed calm lagoon in {len(CELLS)} cells beside the rare-land circle; "
        "attributes preserved."
    )


if __name__ == "__main__":
    main()

"""Install the small village service clearing; safe to rerun on this version."""
from pathlib import Path
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TILESET = ROOT / 'pokefirered/data/tilesets/secondary/pallet_town'
METATILE = 0x2F3
FIRST_TILE = 208
CELLS = {(x, y) for x in range(10, 15) for y in range(15, 18)} | {(11, 13), (11, 14)}

colors = [tuple(map(int, line.split())) for line in (TILESET / 'palettes/07.pal').read_text().splitlines()[3:19]]
art = Image.open(ROOT / 'assets/amazon/village-ground/dirt-source.png').convert('RGB')
art = art.resize((16, 16), Image.Resampling.NEAREST)
pixels = art.tobytes()
# Existing house palette: tan, ochre and brown only; no shared palette edit.
allowed = [1, 3, 6, 10]
indices = [min(allowed, key=lambda i: sum((a-b)**2 for a, b in zip(pixels[p:p+3], colors[i])))
           for p in range(0, len(pixels), 3)]
old = Image.open(TILESET / 'tiles.png')
assert old.size in ((128, 104), (128, 112)), 'Unexpected tileset; inspect before updating.'
canvas = Image.new('P', (128, 112))
canvas.putpalette(old.getpalette())
canvas.paste(old, (0, 0))
for y in range(16):
    for x in range(16):
        tile = FIRST_TILE + (y // 8) * 2 + x // 8
        canvas.putpixel(((tile % 16)*8 + x % 8, (tile // 16)*8 + y % 8), indices[y*16+x])
canvas.save(TILESET / 'tiles.png')
mt = TILESET / 'metatiles.bin'
attrs = TILESET / 'metatile_attributes.bin'
local = METATILE - 640
assert mt.stat().st_size in (local*16, (local+1)*16)
assert attrs.stat().st_size in (local*4, (local+1)*4)
entry = struct.pack('<8H', *[(640+FIRST_TILE+i) | (7 << 12) for i in range(4)], 0, 0, 0, 0)
mt.write_bytes(mt.read_bytes()[:local*16] + entry)
attrs.write_bytes(attrs.read_bytes()[:local*4] + bytes(4))
path = ROOT / 'pokefirered/data/layouts/PalletTown/map.bin'
blocks = list(struct.unpack('<480H', path.read_bytes()))
for x, y in sorted(CELLS):
    index = y*24+x
    assert blocks[index] & 0x3FF in (0x11, METATILE), (x, y, blocks[index])
    blocks[index] = (blocks[index] & 0xFC00) | METATILE
path.write_bytes(struct.pack('<480H', *blocks))
print(f'Installed metatile {METATILE:#x} in {len(CELLS)} cells; collision/elevation bits preserved.')

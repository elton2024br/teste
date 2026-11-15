"""Convert the original terminal artwork to the native NPC green palette.

Run from any directory with Python 3 and Pillow. Index zero is transparent;
no shared palette is modified. Nearest-neighbor scaling preserves hard pixels.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'assets/amazon/storage/terminal-source.png'
target = ROOT / 'pokefirered/graphics/object_events/pics/misc/amazon_storage_terminal.png'
palette_path = ROOT / 'pokefirered/graphics/object_events/palettes/npc_green.pal'
colors = [tuple(map(int, line.split())) for line in palette_path.read_text().splitlines()[3:19]]
art = Image.open(source).convert('RGBA')
art = art.crop(art.getchannel('A').getbbox())
art.thumbnail((16, 16), Image.Resampling.NEAREST)
canvas = Image.new('RGBA', (16, 16))
canvas.paste(art, ((16-art.width)//2, 16-art.height))
# Skin/wood, green, white and black only: unused pink entries stay available
# in the shared palette but are excluded from this asset's color matching.
allowed = list(range(1, 11)) + [14, 15]
indices = []
pixels = canvas.tobytes()
for offset in range(0, len(pixels), 4):
    r, g, b, alpha = pixels[offset:offset + 4]
    indices.append(0 if alpha < 128 else min(allowed, key=lambda i: sum((a-c)**2 for a,c in zip((r,g,b), colors[i]))))
out = Image.new('P', (16, 16))
out.putpalette([c for color in colors for c in color] + [0] * (768-48))
out.putdata(indices)
out.save(target, bits=4, transparency=0)
print(target.relative_to(ROOT))

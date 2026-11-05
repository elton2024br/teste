"""Convert the original intro artwork to the formats consumed by the GBA engine."""
from pathlib import Path
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'pokefirered'
SOURCE = ROOT / 'assets/amazon/intro'


def magenta(color):
    return color[0] > 180 and color[1] < 100 and color[2] > 150


def convert():
    title = Image.open(SOURCE / 'title-source.png').convert('RGB')
    assert title.width * 2 == title.height * 3, 'Title source must be 3:2'
    title = title.resize((240, 160), Image.Resampling.NEAREST)
    data = [r >> 3 | (g >> 3) << 5 | (b >> 3) << 10 for r, g, b in title.get_flattened_data()]
    target = GAME / 'graphics/amazon_intro/title.rgb555'
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(struct.pack('<38400H', *data))
    sheet = Image.open(SOURCE / 'characters-source.png').convert('RGB')
    for column, name in enumerate(['oak', 'rival']):
        image = sheet.crop((column * sheet.width // 2, 0, (column + 1) * sheet.width // 2, sheet.height))
        image = image.resize((64, 96), Image.Resampling.NEAREST)
        colors = [c for c in image.get_flattened_data() if not magenta(c)]
        strip = Image.new('RGB', (len(colors), 1))
        strip.putdata(colors)
        raw = strip.quantize(colors=31, method=Image.Quantize.MEDIANCUT).getpalette()[:93]
        palette = [(115, 197, 164)] + [tuple(v >> 3 << 3 for v in raw[i:i+3]) for i in range(0, 93, 3)]
        indexed = Image.new('P', (64, 96))
        rgb = [0] * 768
        for i, color in enumerate(palette, 96):
            rgb[i*3:i*3+3] = color
        indexed.putpalette(rgb)
        indexed.putdata([0 if magenta(c) else 96 + min(range(1,32), key=lambda i: sum((a-b)**2 for a,b in zip(c,palette[i]))) for c in image.get_flattened_data()])
        folder = GAME / 'graphics/oak_speech' / name
        indexed.save(folder / 'pic.png')
        (folder / 'pal.pal').write_text('JASC-PAL\n0100\n32\n' + '\n'.join(' '.join(map(str, c)) for c in palette) + '\n')
    print('Converted 240x160 title and two 64x96 intro portraits.')


if __name__ == '__main__':
    convert()

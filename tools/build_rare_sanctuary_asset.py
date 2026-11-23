"""Build the original five-stone sanctuary object with a native NPC palette."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "pokefirered/graphics/object_events/palettes/npc_green.pal"
SOURCE = ROOT / "assets/amazon/rare-sanctuary/sanctuary-source.png"
TARGET = ROOT / "pokefirered/graphics/object_events/pics/misc/amazon_rare_sanctuary.png"


def main():
    colors = [tuple(map(int, line.split()))
              for line in PALETTE.read_text().splitlines()[3:19]]
    art = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(art)

    # Five distinct stones arc above a living green core.
    gems = [(3, 5, 5), (5, 3, 8), (8, 2, 14), (11, 3, 11), (13, 5, 2)]
    for x, y, palette_index in gems:
        color = (*colors[palette_index], 255)
        draw.point((x, y - 1), fill=color)
        draw.line((x - 1, y, x + 1, y), fill=color)
        draw.point((x, y + 1), fill=(*colors[15], 255))

    # Leaf-shaped energy and a carved stone pedestal.
    draw.polygon([(8, 4), (5, 7), (8, 11), (11, 7)],
                 fill=(*colors[9], 255), outline=(*colors[10], 255))
    draw.line((8, 5, 8, 10), fill=(*colors[14], 255))
    draw.polygon([(5, 9), (11, 9), (13, 12), (12, 15), (4, 15), (3, 12)],
                 fill=(*colors[4], 255), outline=(*colors[15], 255))
    draw.rectangle((5, 10, 11, 13), fill=(*colors[6], 255))
    draw.line((6, 11, 10, 11), fill=(*colors[5], 255))
    draw.line((4, 14, 12, 14), fill=(*colors[7], 255))

    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    art.save(SOURCE)

    indices = []
    pixels = art.tobytes()
    for offset in range(0, len(pixels), 4):
        r, g, b, alpha = pixels[offset:offset + 4]
        if alpha < 128:
            indices.append(0)
        else:
            indices.append(min(range(1, 16),
                               key=lambda i: sum((a - c) ** 2
                                                 for a, c in zip((r, g, b), colors[i]))))
    out = Image.new("P", art.size)
    out.putpalette([channel for color in colors for channel in color]
                   + [0] * (768 - 48))
    out.putdata(indices)
    out.save(TARGET, bits=4, transparency=0)
    print(SOURCE.relative_to(ROOT))
    print(TARGET.relative_to(ROOT))


if __name__ == "__main__":
    main()

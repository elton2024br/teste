"""Build four original 16x16 stone markers using the native green NPC palette."""

from pathlib import Path
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
PALETTE = ROOT / "pokefirered/graphics/object_events/palettes/npc_green.pal"
ASSETS = ROOT / "assets/amazon/rare-stone-markers"
TARGETS = ROOT / "pokefirered/graphics/object_events/pics/misc"


def indexed(art, colors):
    indices = []
    pixels = art.load()
    for y in range(art.height):
        for x in range(art.width):
            r, g, b, alpha = pixels[x, y]
            if alpha < 128:
                indices.append(0)
            else:
                indices.append(min(range(1, 16), key=lambda i: sum(
                    (actual - candidate) ** 2
                    for actual, candidate in zip((r, g, b), colors[i])
                )))
    output = Image.new("P", art.size)
    output.putpalette([channel for color in colors for channel in color]
                      + [0] * (768 - 48))
    output.putdata(indices)
    output.info["transparency"] = 0
    return output


def draw_marker(kind, gem_index, colors):
    art = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(art)

    # Carved pedestal, shared silhouette but distinct central glyph.
    draw.polygon([(4, 6), (6, 3), (10, 3), (12, 6), (11, 12),
                  (13, 14), (3, 14), (5, 12)],
                 fill=(*colors[4], 255), outline=(*colors[15], 255))
    draw.rectangle((5, 7, 11, 11), fill=(*colors[6], 255))
    draw.line((4, 13, 12, 13), fill=(*colors[7], 255))
    gem = (*colors[gem_index], 255)
    light = (*colors[14], 255)

    if kind == "water":
        draw.polygon([(8, 4), (6, 8), (8, 10), (10, 8)], fill=gem)
        draw.point((7, 7), fill=light)
    elif kind == "roots":
        draw.line((8, 4, 8, 10), fill=gem, width=2)
        draw.line((8, 7, 5, 10), fill=gem)
        draw.line((8, 7, 11, 10), fill=gem)
        draw.point((7, 4), fill=light)
    elif kind == "drought":
        draw.ellipse((5, 4, 10, 9), fill=gem)
        for end in ((8, 2), (8, 11), (4, 6), (12, 6)):
            draw.line((8, 6, *end), fill=gem)
        draw.point((7, 5), fill=light)
    elif kind == "forest":
        draw.polygon([(8, 3), (5, 7), (8, 10), (11, 6)], fill=gem)
        draw.line((8, 5, 8, 10), fill=(*colors[15], 255))
        draw.point((7, 5), fill=light)
    else:
        raise ValueError(kind)
    return art


def main():
    colors = [tuple(map(int, line.split()))
              for line in PALETTE.read_text().splitlines()[3:19]]
    ASSETS.mkdir(parents=True, exist_ok=True)
    definitions = {
        "water": 5,
        "roots": 8,
        "drought": 14,
        "forest": 11,
    }
    for kind, gem_index in definitions.items():
        art = draw_marker(kind, gem_index, colors)
        source = ASSETS / f"{kind}-source.png"
        target = TARGETS / f"amazon_stone_{kind}.png"
        art.save(source)
        indexed(art, colors).save(target, bits=4, transparency=0)
        print(source.relative_to(ROOT))
        print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()

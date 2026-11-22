"""Build original Onca-pintada battle, icon and footprint assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "pokefirered/graphics/pokemon/spinarak"
SOURCE = ROOT / "assets/amazon/creatures/oncapinta-source.png"

BATTLE_COLORS = [
    (205, 205, 172),
    (24, 16, 16), (57, 32, 16), (98, 49, 16), (148, 74, 16),
    (205, 115, 24), (238, 164, 49), (255, 205, 98), (255, 238, 172),
    (246, 246, 222), (139, 98, 57), (90, 65, 41), (57, 49, 41),
    (197, 139, 82), (115, 164, 205), (0, 0, 0),
]


def canvas(size):
    image = Image.new("P", size, 0)
    image.putpalette([v for color in BATTLE_COLORS for v in color]
                     + [0] * (768 - len(BATTLE_COLORS) * 3))
    return image


def add_spots(draw, points):
    for x, y in points:
        draw.rectangle((x, y, x + 2, y + 1), fill=1)
        draw.point((x + 1, y), fill=7)


def draw_front():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.arc((3, 26, 27, 52), 70, 300, fill=1, width=5)
    draw.arc((5, 28, 25, 49), 70, 292, fill=6, width=3)
    draw.ellipse((15, 27, 46, 46), fill=1)
    draw.ellipse((17, 28, 45, 44), fill=6)
    draw.ellipse((38, 18, 55, 35), fill=1)
    draw.ellipse((40, 20, 54, 33), fill=6)
    draw.ellipse((39, 16, 45, 22), fill=1)
    draw.ellipse((50, 16, 56, 22), fill=1)
    draw.polygon([(48, 27), (59, 29), (53, 35), (44, 32)], fill=7)
    draw.rectangle((56, 29, 59, 31), fill=1)
    draw.point((45, 23), fill=15)
    draw.point((51, 23), fill=15)
    draw.polygon([(19, 42), (26, 42), (24, 57), (18, 57)], fill=3)
    draw.polygon([(36, 42), (43, 41), (46, 56), (40, 57)], fill=3)
    draw.rectangle((17, 55, 27, 58), fill=1)
    draw.rectangle((39, 55, 49, 58), fill=1)
    add_spots(draw, [(20, 31), (29, 29), (37, 32), (24, 37), (34, 39),
                     (43, 25), (49, 28)])
    return image


def draw_back():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.arc((3, 25, 28, 53), 70, 300, fill=1, width=5)
    draw.arc((5, 27, 26, 50), 70, 292, fill=6, width=3)
    draw.ellipse((16, 27, 47, 46), fill=1)
    draw.ellipse((18, 28, 45, 44), fill=6)
    draw.ellipse((28, 17, 46, 35), fill=1)
    draw.ellipse((30, 19, 44, 33), fill=6)
    draw.ellipse((28, 15, 34, 22), fill=1)
    draw.ellipse((41, 15, 47, 22), fill=1)
    draw.polygon([(20, 42), (27, 42), (25, 57), (19, 57)], fill=3)
    draw.polygon([(37, 42), (44, 41), (47, 56), (41, 57)], fill=3)
    draw.rectangle((18, 55, 28, 58), fill=1)
    draw.rectangle((40, 55, 50, 58), fill=1)
    add_spots(draw, [(21, 31), (30, 29), (39, 32), (25, 37), (35, 39),
                     (32, 22), (40, 25)])
    return image


def palette_text(colors):
    return "JASC-PAL\n0100\n16\n" + "\n".join(
        " ".join(map(str, color)) for color in colors
    ) + "\n"


def icon_colors():
    path = ROOT / "pokefirered/graphics/pokemon/icon_palettes/icon_palette_0.pal"
    return [tuple(map(int, line.split())) for line in path.read_text().splitlines()[3:19]]


def remap(image, colors):
    rgba = image.convert("RGBA")
    out = Image.new("P", image.size, 0)
    out.putpalette([v for color in colors for v in color]
                   + [0] * (768 - len(colors) * 3))
    pixels = []
    for index, color in zip(image.get_flattened_data(), rgba.get_flattened_data()):
        if index == 0:
            pixels.append(0)
        else:
            pixels.append(min(range(1, len(colors)), key=lambda candidate: sum(
                (color[channel] - colors[candidate][channel]) ** 2 for channel in range(3)
            )))
    out.putdata(pixels)
    return out


def main():
    TARGET.mkdir(parents=True, exist_ok=True)
    SOURCE.parent.mkdir(parents=True, exist_ok=True)
    front, back = draw_front(), draw_back()
    front.save(TARGET / "front.png")
    back.save(TARGET / "back.png")
    pal = palette_text(BATTLE_COLORS)
    (TARGET / "normal.pal").write_text(pal)
    (TARGET / "shiny.pal").write_text(pal)

    crop = front.crop(front.getbbox()).resize((28, 28), Image.Resampling.NEAREST)
    frame = remap(crop, icon_colors())
    icon = Image.new("P", (32, 64), 0)
    icon.putpalette(frame.getpalette())
    icon.paste(frame, (2, 2))
    icon.paste(frame, (2, 34))
    icon.save(TARGET / "icon.png")

    footprint = Image.new("1", (16, 16), 1)
    feet = ImageDraw.Draw(footprint)
    for x, y in ((4, 5), (11, 5), (5, 11), (10, 11)):
        feet.ellipse((x - 2, y - 2, x + 1, y + 1), fill=0)
        feet.point((x - 2, y - 3), fill=0)
        feet.point((x + 1, y - 3), fill=0)
    footprint.save(TARGET / "footprint.png")

    preview = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    for offset, sprite in ((0, front), (64, back)):
        rgba = sprite.convert("RGBA")
        mask = Image.new("L", sprite.size)
        mask.putdata([0 if value == 0 else 255 for value in sprite.get_flattened_data()])
        rgba.putalpha(mask)
        preview.alpha_composite(rgba, (offset, 0))
    preview.save(SOURCE)
    print("Installed original Onca-pintada battle sprites, icon, footprint and palettes.")


if __name__ == "__main__":
    main()

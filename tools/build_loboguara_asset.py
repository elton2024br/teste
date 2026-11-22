"""Build original Lobo-guara battle, icon and footprint assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "pokefirered/graphics/pokemon/caterpie"
SOURCE = ROOT / "assets/amazon/creatures/loboguara-source.png"

BATTLE_COLORS = [
    (205, 205, 172),  # transparent index used by the battle renderer
    (32, 24, 24),
    (57, 41, 32),
    (98, 49, 32),
    (180, 74, 32),
    (230, 115, 49),
    (246, 164, 82),
    (255, 222, 164),
    (246, 246, 222),
    (238, 197, 49),
    (139, 49, 41),
    (106, 82, 65),
    (148, 107, 74),
    (197, 148, 98),
    (82, 65, 49),
    (16, 16, 16),
]


def indexed_canvas(size):
    image = Image.new("P", size, 0)
    image.putpalette([value for color in BATTLE_COLORS for value in color]
                     + [0] * (768 - len(BATTLE_COLORS) * 3))
    return image


def draw_front():
    image = indexed_canvas((64, 64))
    draw = ImageDraw.Draw(image)
    # Long pale-tipped tail, orange body and the dark mane of a maned wolf.
    draw.polygon([(19, 35), (9, 26), (3, 24), (8, 31), (4, 35), (14, 40)], fill=1)
    draw.polygon([(18, 34), (9, 28), (5, 27), (10, 34), (7, 36), (16, 39)], fill=6)
    draw.ellipse((15, 27, 45, 43), fill=1)
    draw.ellipse((17, 28, 44, 41), fill=5)
    draw.polygon([(38, 35), (39, 22), (47, 17), (53, 22), (50, 37)], fill=1)
    draw.polygon([(40, 34), (41, 23), (47, 19), (51, 23), (48, 36)], fill=4)
    draw.polygon([(42, 21), (41, 9), (47, 17)], fill=1)
    draw.polygon([(49, 18), (55, 8), (54, 22)], fill=1)
    draw.polygon([(43, 18), (43, 12), (46, 17)], fill=6)
    draw.polygon([(50, 17), (54, 11), (53, 20)], fill=6)
    draw.polygon([(46, 21), (57, 24), (55, 30), (47, 31)], fill=5)
    draw.polygon([(49, 25), (58, 26), (55, 31), (48, 30)], fill=7)
    draw.rectangle((56, 26, 59, 28), fill=1)
    draw.point((50, 23), fill=15)
    draw.point((51, 23), fill=9)
    draw.polygon([(21, 39), (27, 39), (25, 57), (20, 57)], fill=1)
    draw.polygon([(34, 39), (40, 39), (43, 57), (38, 57)], fill=1)
    draw.rectangle((20, 55, 27, 58), fill=15)
    draw.rectangle((38, 55, 45, 58), fill=15)
    draw.polygon([(36, 27), (43, 24), (44, 37), (38, 41)], fill=2)
    return image


def draw_back():
    image = indexed_canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.polygon([(20, 35), (8, 27), (3, 28), (10, 35), (5, 38), (18, 42)], fill=1)
    draw.polygon([(19, 36), (9, 30), (6, 30), (12, 36), (8, 38), (18, 40)], fill=6)
    draw.ellipse((17, 28, 46, 44), fill=1)
    draw.ellipse((19, 29, 44, 42), fill=5)
    draw.polygon([(28, 31), (27, 18), (32, 13), (38, 18), (39, 34)], fill=1)
    draw.polygon([(29, 30), (29, 19), (33, 15), (37, 19), (37, 33)], fill=4)
    draw.polygon([(28, 18), (27, 7), (32, 15)], fill=1)
    draw.polygon([(36, 16), (41, 7), (40, 20)], fill=1)
    draw.polygon([(29, 15), (29, 10), (31, 15)], fill=6)
    draw.polygon([(37, 15), (40, 10), (39, 18)], fill=6)
    draw.polygon([(22, 40), (28, 40), (26, 58), (20, 58)], fill=1)
    draw.polygon([(36, 40), (42, 40), (44, 58), (38, 58)], fill=1)
    draw.rectangle((20, 56, 27, 59), fill=15)
    draw.rectangle((38, 56, 45, 59), fill=15)
    draw.polygon([(28, 27), (38, 27), (40, 40), (33, 44), (26, 39)], fill=2)
    return image


def palette_text(colors):
    return "JASC-PAL\n0100\n16\n" + "\n".join(
        " ".join(map(str, color)) for color in colors
    ) + "\n"


def icon_palette():
    path = ROOT / "pokefirered/graphics/pokemon/icon_palettes/icon_palette_0.pal"
    lines = path.read_text().splitlines()[3:19]
    return [tuple(map(int, line.split())) for line in lines]


def remap(image, colors):
    rgba = image.convert("RGBA")
    out = Image.new("P", image.size, 0)
    out.putpalette([value for color in colors for value in color]
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
    front = draw_front()
    back = draw_back()
    front.save(TARGET / "front.png")
    back.save(TARGET / "back.png")
    pal = palette_text(BATTLE_COLORS)
    (TARGET / "normal.pal").write_text(pal)
    (TARGET / "shiny.pal").write_text(pal)

    crop = front.crop(front.getbbox()).resize((28, 28), Image.Resampling.NEAREST)
    icon_frame = remap(crop, icon_palette())
    icon = Image.new("P", (32, 64), 0)
    icon.putpalette(icon_frame.getpalette())
    icon.paste(icon_frame, (2, 2))
    icon.paste(icon_frame, (2, 34))
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
    print("Installed original Lobo-guara battle sprites, icon, footprint and palettes.")


if __name__ == "__main__":
    main()

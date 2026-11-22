"""Build original Mico-leao battle, icon and footprint assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "pokefirered/graphics/pokemon/hoothoot"
SOURCE = ROOT / "assets/amazon/creatures/micoleao-source.png"

BATTLE_COLORS = [
    (205, 205, 172),
    (32, 24, 16), (65, 41, 24), (106, 57, 24), (156, 74, 16),
    (205, 98, 16), (238, 139, 24), (255, 181, 49), (255, 222, 123),
    (246, 238, 197), (139, 90, 49), (90, 57, 41), (57, 41, 32),
    (222, 115, 65), (255, 197, 139), (8, 8, 8),
]


def canvas(size):
    image = Image.new("P", size, 0)
    image.putpalette([v for color in BATTLE_COLORS for v in color]
                     + [0] * (768 - len(BATTLE_COLORS) * 3))
    return image


def draw_front():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    # Long curled tail, small orange body and the golden mane of a lion tamarin.
    draw.arc((4, 24, 32, 55), 65, 290, fill=2, width=5)
    draw.arc((7, 27, 29, 51), 65, 280, fill=6, width=3)
    draw.ellipse((20, 29, 44, 48), fill=2)
    draw.ellipse((22, 30, 43, 46), fill=6)
    draw.ellipse((35, 13, 56, 35), fill=3)
    draw.ellipse((37, 15, 54, 33), fill=7)
    draw.polygon([(37, 18), (34, 9), (43, 15)], fill=5)
    draw.polygon([(51, 17), (57, 9), (56, 22)], fill=5)
    draw.ellipse((40, 18, 53, 30), fill=14)
    draw.ellipse((43, 20, 54, 30), fill=8)
    draw.point((45, 21), fill=15)
    draw.point((50, 21), fill=15)
    draw.rectangle((48, 26, 50, 27), fill=1)
    draw.line((37, 17, 34, 31), fill=7, width=3)
    draw.line((53, 16, 57, 30), fill=7, width=3)
    draw.polygon([(23, 44), (29, 44), (27, 56), (21, 56)], fill=3)
    draw.polygon([(36, 44), (42, 43), (45, 55), (39, 56)], fill=3)
    draw.rectangle((20, 55, 28, 58), fill=1)
    draw.rectangle((39, 54, 47, 57), fill=1)
    return image


def draw_back():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.arc((5, 23, 34, 56), 65, 292, fill=2, width=5)
    draw.arc((8, 26, 31, 52), 65, 282, fill=6, width=3)
    draw.ellipse((21, 29, 46, 48), fill=2)
    draw.ellipse((23, 30, 44, 46), fill=6)
    draw.ellipse((29, 12, 51, 35), fill=3)
    draw.ellipse((31, 14, 49, 33), fill=7)
    draw.polygon([(31, 17), (28, 8), (37, 15)], fill=5)
    draw.polygon([(46, 16), (53, 8), (51, 22)], fill=5)
    draw.line((31, 16, 28, 31), fill=7, width=3)
    draw.line((48, 15, 53, 30), fill=7, width=3)
    draw.ellipse((34, 19, 46, 31), fill=6)
    draw.polygon([(24, 44), (30, 44), (28, 56), (22, 56)], fill=3)
    draw.polygon([(37, 44), (43, 43), (46, 55), (40, 56)], fill=3)
    draw.rectangle((21, 55, 29, 58), fill=1)
    draw.rectangle((40, 54, 48, 57), fill=1)
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
    for x, y in ((5, 5), (11, 5), (5, 11), (11, 11)):
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
    print("Installed original Mico-leao battle sprites, icon, footprint and palettes.")


if __name__ == "__main__":
    main()

"""Build original Tuiuiu battle, icon and footprint assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "pokefirered/graphics/pokemon/ledyba"
SOURCE = ROOT / "assets/amazon/creatures/tuiuiu-source.png"

BATTLE_COLORS = [
    (205, 205, 172),
    (16, 16, 24), (41, 41, 49), (74, 74, 82), (115, 115, 123),
    (164, 164, 164), (205, 205, 197), (238, 238, 222), (255, 255, 246),
    (123, 32, 32), (180, 41, 41), (230, 74, 57), (106, 74, 49),
    (197, 148, 82), (106, 164, 205), (0, 0, 0),
]


def canvas(size):
    image = Image.new("P", size, 0)
    image.putpalette([v for color in BATTLE_COLORS for v in color]
                     + [0] * (768 - len(BATTLE_COLORS) * 3))
    return image


def draw_front():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    # Tall white jabiru with black head/neck, red collar and long dark legs.
    draw.ellipse((17, 29, 45, 48), fill=2)
    draw.ellipse((19, 29, 44, 46), fill=8)
    draw.polygon([(34, 35), (46, 32), (43, 45), (31, 47)], fill=3)
    draw.line((39, 32, 37, 17), fill=1, width=7)
    draw.ellipse((34, 10, 47, 22), fill=1)
    draw.polygon([(44, 13), (59, 16), (45, 19)], fill=2)
    draw.point((41, 14), fill=8)
    draw.rectangle((35, 22, 42, 27), fill=10)
    draw.rectangle((36, 26, 42, 31), fill=7)
    draw.line((24, 45, 22, 58), fill=1, width=2)
    draw.line((35, 46, 37, 58), fill=1, width=2)
    draw.line((18, 58, 25, 58), fill=1, width=2)
    draw.line((34, 58, 41, 58), fill=1, width=2)
    draw.polygon([(18, 33), (7, 27), (12, 38), (20, 41)], fill=6)
    draw.line((9, 29, 17, 37), fill=3, width=2)
    return image


def draw_back():
    image = canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.ellipse((18, 29, 46, 48), fill=2)
    draw.ellipse((20, 29, 44, 46), fill=8)
    draw.polygon([(19, 32), (44, 31), (42, 45), (22, 47)], fill=3)
    draw.line((31, 32, 32, 16), fill=1, width=7)
    draw.ellipse((27, 9, 40, 21), fill=1)
    draw.polygon([(28, 13), (14, 16), (28, 19)], fill=2)
    draw.rectangle((28, 21, 35, 26), fill=10)
    draw.rectangle((29, 25, 35, 31), fill=7)
    draw.line((25, 45, 23, 58), fill=1, width=2)
    draw.line((36, 46, 38, 58), fill=1, width=2)
    draw.line((19, 58, 26, 58), fill=1, width=2)
    draw.line((35, 58, 42, 58), fill=1, width=2)
    draw.polygon([(20, 33), (8, 28), (13, 39), (22, 42)], fill=6)
    draw.line((10, 30, 19, 38), fill=3, width=2)
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
    feet.line((4, 3, 6, 12), fill=0, width=2)
    feet.line((11, 3, 9, 12), fill=0, width=2)
    feet.line((2, 12, 7, 12), fill=0)
    feet.line((8, 12, 13, 12), fill=0)
    footprint.save(TARGET / "footprint.png")

    preview = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    for offset, sprite in ((0, front), (64, back)):
        rgba = sprite.convert("RGBA")
        mask = Image.new("L", sprite.size)
        mask.putdata([0 if value == 0 else 255 for value in sprite.get_flattened_data()])
        rgba.putalpha(mask)
        preview.alpha_composite(rgba, (offset, 0))
    preview.save(SOURCE)
    print("Installed original Tuiuiu battle sprites, icon, footprint and palettes.")


if __name__ == "__main__":
    main()

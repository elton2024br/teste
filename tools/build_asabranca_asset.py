"""Build original Asa-branca battle, icon and footprint assets."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "pokefirered/graphics/pokemon/pidgey"
SOURCE = ROOT / "assets/amazon/creatures/asabranca-source.png"

BATTLE_COLORS = [
    (205, 205, 172),  # transparent index used by the battle renderer
    (24, 24, 32),
    (49, 49, 57),
    (82, 82, 90),
    (123, 123, 131),
    (172, 172, 172),
    (213, 213, 205),
    (246, 246, 230),
    (246, 205, 74),
    (197, 139, 49),
    (139, 82, 41),
    (98, 57, 32),
    (222, 115, 65),
    (115, 164, 213),
    (255, 255, 255),
    (8, 8, 16),
]


def indexed_canvas(size):
    image = Image.new("P", size, 0)
    image.putpalette([value for color in BATTLE_COLORS for value in color]
                     + [0] * (768 - len(BATTLE_COLORS) * 3))
    return image


def draw_front():
    image = indexed_canvas((64, 64))
    draw = ImageDraw.Draw(image)
    # White dove seen from the side, with the characteristic dark wing bars.
    draw.polygon([(17, 35), (5, 29), (10, 38), (4, 43), (20, 42)], fill=1)
    draw.polygon([(18, 34), (8, 31), (13, 38), (8, 41), (21, 40)], fill=6)
    draw.ellipse((17, 25, 47, 47), fill=2)
    draw.ellipse((19, 26, 45, 45), fill=7)
    draw.ellipse((38, 17, 53, 32), fill=2)
    draw.ellipse((40, 18, 52, 30), fill=7)
    draw.polygon([(51, 23), (60, 26), (51, 29)], fill=9)
    draw.point((47, 22), fill=15)
    draw.point((48, 22), fill=13)
    draw.polygon([(21, 29), (42, 32), (37, 45), (18, 42)], fill=4)
    draw.polygon([(23, 30), (40, 33), (36, 42), (20, 40)], fill=6)
    draw.line((23, 34, 38, 37), fill=1, width=2)
    draw.line((21, 38, 36, 41), fill=2, width=2)
    draw.polygon([(25, 44), (29, 44), (28, 53), (24, 53)], fill=9)
    draw.polygon([(35, 44), (39, 43), (41, 52), (37, 53)], fill=9)
    draw.line((21, 53, 30, 53), fill=1, width=2)
    draw.line((35, 53, 44, 53), fill=1, width=2)
    return image


def draw_back():
    image = indexed_canvas((64, 64))
    draw = ImageDraw.Draw(image)
    draw.polygon([(17, 35), (5, 29), (11, 38), (5, 43), (21, 43)], fill=1)
    draw.polygon([(18, 35), (8, 32), (13, 38), (9, 41), (21, 40)], fill=6)
    draw.ellipse((17, 25, 47, 47), fill=2)
    draw.ellipse((19, 26, 45, 45), fill=7)
    draw.ellipse((27, 15, 43, 31), fill=2)
    draw.ellipse((29, 17, 41, 29), fill=7)
    draw.polygon([(20, 29), (43, 30), (42, 45), (19, 43)], fill=4)
    draw.polygon([(22, 30), (41, 31), (39, 42), (21, 41)], fill=6)
    draw.line((22, 34, 40, 35), fill=1, width=2)
    draw.line((21, 38, 39, 40), fill=2, width=2)
    draw.polygon([(24, 43), (28, 44), (27, 53), (23, 53)], fill=9)
    draw.polygon([(35, 44), (39, 43), (41, 52), (37, 53)], fill=9)
    draw.line((20, 53, 29, 53), fill=1, width=2)
    draw.line((35, 53, 44, 53), fill=1, width=2)
    return image


def palette_text(colors):
    return "JASC-PAL\n0100\n16\n" + "\n".join(
        " ".join(map(str, color)) for color in colors
    ) + "\n"


def icon_palette():
    path = ROOT / "pokefirered/graphics/pokemon/icon_palettes/icon_palette_0.pal"
    return [tuple(map(int, line.split())) for line in path.read_text().splitlines()[3:19]]


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
    feet.line((3, 4, 6, 12), fill=0, width=2)
    feet.line((12, 4, 9, 12), fill=0, width=2)
    feet.line((3, 12, 7, 12), fill=0)
    feet.line((9, 12, 13, 12), fill=0)
    footprint.save(TARGET / "footprint.png")

    preview = Image.new("RGBA", (128, 64), (0, 0, 0, 0))
    for offset, sprite in ((0, front), (64, back)):
        rgba = sprite.convert("RGBA")
        mask = Image.new("L", sprite.size)
        mask.putdata([0 if value == 0 else 255 for value in sprite.get_flattened_data()])
        rgba.putalpha(mask)
        preview.alpha_composite(rgba, (offset, 0))
    preview.save(SOURCE)
    print("Installed original Asa-branca battle sprites, icon, footprint and palettes.")


if __name__ == "__main__":
    main()

from math import cos, pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH, HEIGHT, FRAME_COUNT = 1000, 300, 30
ASSET_PATH = Path(__file__).parent / "assets" / "profile-banner.gif"

start = (11, 16, 33)
end = (17, 43, 53)
background = Image.new("RGB", (WIDTH, HEIGHT))
pixels = background.load()
for x in range(WIDTH):
    ratio = x / (WIDTH - 1)
    for y in range(HEIGHT):
        vertical = y / (HEIGHT - 1)
        pixels[x, y] = tuple(
            int(start[channel] * (1 - ratio) + end[channel] * ratio + (4 if channel == 2 else 0) * vertical)
            for channel in range(3)
        )

FONTS = Path(r"C:\Windows\Fonts")


def load_font(candidates: list[Path], size: int) -> ImageFont.FreeTypeFont:
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    raise FileNotFoundError("Install a supported Segoe UI, Arial, or DejaVu Sans font.")


title_font = load_font(
    [
        FONTS / "segoeuib.ttf",
        FONTS / "arialbd.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ],
    46,
)
subtitle_font = load_font(
    [
        FONTS / "segoeui.ttf",
        FONTS / "arial.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
    ],
    21,
)
label_font = load_font(
    [
        FONTS / "segoeuib.ttf",
        FONTS / "arialbd.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ],
    13,
)

frames = []
for frame_index in range(FRAME_COUNT):
    phase = 2 * pi * frame_index / FRAME_COUNT
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_x = int(WIDTH * (0.25 + 0.62 * (0.5 + 0.5 * sin(phase))))
    glow_y = int(HEIGHT * (0.25 + 0.18 * cos(phase)))
    glow_draw.ellipse(
        (glow_x - 180, glow_y - 140, glow_x + 180, glow_y + 140),
        fill=(33, 215, 187, 38),
    )
    glow_draw.ellipse(
        (WIDTH - glow_x - 130, HEIGHT - glow_y - 90, WIDTH - glow_x + 130, HEIGHT - glow_y + 90),
        fill=(133, 87, 255, 22),
    )
    glow = glow.filter(ImageFilter.GaussianBlur(65))
    frame = Image.alpha_composite(background.convert("RGBA"), glow)
    draw = ImageDraw.Draw(frame)

    for point in range(22):
        x = (point * 89 + frame_index * (2 + point % 3)) % WIDTH
        y = (point * 47 + int(6 * sin(phase + point))) % HEIGHT
        color = (61, 110, 125) if point % 3 else (81, 158, 151)
        draw.ellipse((x, y, x + 2, y + 2), fill=color)

    draw.rounded_rectangle((62, 54, 67, 78), radius=3, fill=(74, 231, 195))
    draw.text((82, 54), "BUILDING INTELLIGENT DIGITAL SYSTEMS", font=label_font, fill=(116, 225, 209))
    draw.text((62, 105), "SYLVESTER EDEM DUGO", font=title_font, fill=(242, 248, 255))
    draw.text(
        (66, 174),
        "Python  /  AI/ML  /  Data Science  /  Secure Software",
        font=subtitle_font,
        fill=(184, 203, 220),
    )
    draw.rounded_rectangle((66, 230, 226, 263), radius=16, outline=(73, 158, 151), width=1)
    draw.text((82, 239), "CURIOUS BY DESIGN", font=label_font, fill=(151, 211, 202))
    frames.append(frame.convert("RGB").quantize(colors=128))

ASSET_PATH.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(
    ASSET_PATH,
    save_all=True,
    append_images=frames[1:],
    duration=100,
    loop=0,
    optimize=True,
    disposal=2,
)
print(f"Wrote {ASSET_PATH} ({ASSET_PATH.stat().st_size:,} bytes)")

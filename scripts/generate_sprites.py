"""Generate Claymorphism-style pet sprites with soft 3D effects."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math


def add_edge_feather(img: Image.Image, radius: int = 3) -> Image.Image:
    """Add feather effect to edges for smooth transparency."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")

    alpha = img.split()[3]
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=radius))
    img.putalpha(blurred_alpha)
    return img


def create_shadow(color: tuple, offset: int = 3, blur: int = 5) -> Image.Image:
    """Create a soft shadow image."""
    size = 128 + blur * 2
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)

    shadow_color = (30, 20, 10, 80)
    for i in range(offset, size - offset):
        for j in range(offset, size - offset):
            dx = i - size // 2
            dy = j - size // 2
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 50:
                alpha = int(80 * (1 - dist / 50))
                shadow.putpixel((i, j), (*shadow_color[:3], alpha))

    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=blur))
    return shadow


def draw_claymorphism_body(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    radius: int,
    main_color: tuple,
    highlight_color: tuple,
    shadow_color: tuple,
) -> None:
    """Draw a claymorphism-style body with soft shadows and highlights."""
    outer_shadow = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    outer_draw = ImageDraw.Draw(outer_shadow)

    for i in range(140):
        for j in range(140):
            dx = i - 70
            dy = j - 70
            dist = math.sqrt(dx * dx + dy * dy)
            if 45 < dist < 55:
                alpha = int(60 * (1 - abs(dist - 50) / 5))
                outer_draw.ellipse([i - 1, j - 1, i + 1, j + 1], fill=(20, 15, 10, alpha))

    outer_shadow = outer_shadow.filter(ImageFilter.GaussianBlur(radius=8))

    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius], fill=shadow_color, outline=None
    )

    offset = 4
    draw.ellipse(
        [cx - radius + offset, cy - radius + offset, cx + radius - offset, cy + radius - offset],
        fill=main_color,
        outline=None,
    )

    highlight_r = radius - 10
    highlight_points = []
    for angle in range(180, 360):
        rad = math.radians(angle)
        x = int(cx + math.cos(rad) * highlight_r)
        y = int(cy + math.sin(rad) * highlight_r)
        highlight_points.append((x, y))

    if len(highlight_points) > 2:
        for i in range(len(highlight_points) - 1):
            p1, p2 = highlight_points[i], highlight_points[i + 1]
            mid_x = (p1[0] + p2[0]) // 2
            mid_y = (p1[1] + p2[1]) // 2
            draw.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=highlight_color)


def draw_cat_face(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    frame: int,
    total_frames: int,
    main_color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw anime-style cat face with claymorphism effect."""
    bounce = int(math.sin(frame / total_frames * math.pi * 2) * 4)

    ear_color = main_color
    inner_ear = (255, 180, 160, 255)

    ear1 = [(cx - 35, cy - 25 + bounce), (cx - 25, cy - 45 + bounce), (cx - 15, cy - 25 + bounce)]
    ear2 = [(cx + 15, cy - 25 + bounce), (cx + 25, cy - 45 + bounce), (cx + 35, cy - 25 + bounce)]
    draw.polygon(ear1, fill=ear_color)
    draw.polygon(ear2, fill=ear_color)
    draw.polygon(
        [(cx - 32, cy - 25 + bounce), (cx - 25, cy - 38 + bounce), (cx - 18, cy - 25 + bounce)],
        fill=inner_ear,
    )
    draw.polygon(
        [(cx + 18, cy - 25 + bounce), (cx + 25, cy - 38 + bounce), (cx + 32, cy - 25 + bounce)],
        fill=inner_ear,
    )

    if is_sleeping:
        draw.arc(
            [cx - 15, cy - 5 + bounce, cx + 15, cy + 10 + bounce],
            0,
            180,
            fill=(50, 40, 30),
            width=3,
        )
        draw.line(
            [cx - 25, cy + 15 + bounce, cx - 15, cy + 15 + bounce], fill=(50, 40, 30), width=2
        )
        draw.line(
            [cx + 15, cy + 15 + bounce, cx + 25, cy + 15 + bounce], fill=(50, 40, 30), width=2
        )
    else:
        eye_blink = frame % max(total_frames // 2, 1) < 2
        eye_height = 6 if eye_blink else 18

        eye_y = cy - 8 + bounce
        draw.ellipse([cx - 22, eye_y, cx - 8, eye_y + eye_height], fill="white")
        draw.ellipse([cx + 8, eye_y, cx + 22, eye_y + eye_height], fill="white")

        if not eye_blink:
            pupil_offset = int(math.sin(frame / total_frames * math.pi * 4) * 2)
            draw.ellipse(
                [cx - 18 + pupil_offset, eye_y + 4, cx - 12 + pupil_offset, eye_y + 12],
                fill=(30, 20, 10),
            )
            draw.ellipse(
                [cx + 12 + pupil_offset, eye_y + 4, cx + 18 + pupil_offset, eye_y + 12],
                fill=(30, 20, 10),
            )
            draw.ellipse(
                [cx - 17 + pupil_offset, eye_y + 5, cx - 14 + pupil_offset, eye_y + 8], fill="white"
            )
            draw.ellipse(
                [cx + 13 + pupil_offset, eye_y + 5, cx + 16 + pupil_offset, eye_y + 8], fill="white"
            )

        nose_color = (255, 150, 150)
        draw.ellipse([cx - 4, cy + 8 + bounce, cx + 4, cy + 14 + bounce], fill=nose_color)

        mouth_open = int(abs(math.sin(frame / total_frames * math.pi * 6)) * 4)
        draw.arc(
            [cx - 10, cy + 14 + bounce, cx + 10, cy + 22 + bounce + mouth_open],
            0,
            180,
            fill=(50, 40, 30),
            width=2,
        )

        whisker_y = cy + 12 + bounce
        for offset in [-12, -8, -4]:
            draw.line(
                [cx - 15, whisker_y + offset, cx - 35, whisker_y + offset - 5],
                fill=(100, 80, 60),
                width=1,
            )
            draw.line(
                [cx + 15, whisker_y + offset, cx + 35, whisker_y + offset - 5],
                fill=(100, 80, 60),
                width=1,
            )

    tail_angle = math.sin(frame / total_frames * math.pi * 4) * 0.4
    tail_x = cx + 40
    tail_y = cy + 25 + bounce
    for i in range(6):
        t = i / 5
        x = tail_x + math.sin(t * math.pi + tail_angle * math.pi) * (10 + i * 4)
        y = tail_y + t * 30
        width = 8 - i
        draw.ellipse([x - width // 2, y - 2, x + width // 2, y + 2], fill=main_color)


def draw_dog_face(
    draw: ImageDraw.ImageDraw,
    cx: int,
    cy: int,
    frame: int,
    total_frames: int,
    main_color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw anime-style dog face with claymorphism effect."""
    bounce = int(math.sin(frame / total_frames * math.pi * 2) * 4)

    ear_color = main_color

    draw.ellipse([cx - 40, cy - 20 + bounce, cx - 15, cy + 15 + bounce], fill=ear_color)
    draw.ellipse([cx + 15, cy - 20 + bounce, cx + 40, cy + 15 + bounce], fill=ear_color)

    inner_ear = (200, 140, 120)
    draw.ellipse([cx - 35, cy - 15 + bounce, cx - 20, cy + 10 + bounce], fill=inner_ear)
    draw.ellipse([cx + 20, cy - 15 + bounce, cx + 35, cy + 10 + bounce], fill=inner_ear)

    if is_sleeping:
        draw.arc(
            [cx - 15, cy - 5 + bounce, cx + 15, cy + 10 + bounce],
            0,
            180,
            fill=(50, 40, 30),
            width=3,
        )
        draw.line(
            [cx - 25, cy + 15 + bounce, cx - 15, cy + 15 + bounce], fill=(50, 40, 30), width=2
        )
        draw.line(
            [cx + 15, cy + 15 + bounce, cx + 25, cy + 15 + bounce], fill=(50, 40, 30), width=2
        )
    else:
        eye_blink = frame % max(total_frames // 2, 1) < 2
        eye_height = 5 if eye_blink else 16

        eye_y = cy - 10 + bounce
        draw.ellipse([cx - 20, eye_y, cx - 5, eye_y + eye_height], fill="white")
        draw.ellipse([cx + 5, eye_y, cx + 20, eye_y + eye_height], fill="white")

        if not eye_blink:
            pupil_offset = int(math.sin(frame / total_frames * math.pi * 3) * 2)
            draw.ellipse(
                [cx - 15 + pupil_offset, eye_y + 3, cx - 8 + pupil_offset, eye_y + 11],
                fill=(30, 20, 10),
            )
            draw.ellipse(
                [cx + 8 + pupil_offset, eye_y + 3, cx + 15 + pupil_offset, eye_y + 11],
                fill=(30, 20, 10),
            )
            draw.ellipse(
                [cx - 14 + pupil_offset, eye_y + 4, cx - 11 + pupil_offset, eye_y + 7], fill="white"
            )
            draw.ellipse(
                [cx + 9 + pupil_offset, eye_y + 4, cx + 12 + pupil_offset, eye_y + 7], fill="white"
            )

        nose_color = (40, 30, 20)
        draw.ellipse([cx - 8, cy + 8 + bounce, cx + 8, cy + 18 + bounce], fill=nose_color)
        draw.ellipse([cx - 5, cy + 10 + bounce, cx, cy + 14 + bounce], fill=(80, 60, 50))

        tongue_out = (
            int(abs(math.sin(frame / total_frames * math.pi * 5)) * 8) if not is_sleeping else 0
        )
        if tongue_out > 2:
            draw.ellipse(
                [cx - 5, cy + 18 + bounce, cx + 5, cy + 18 + tongue_out + bounce],
                fill=(255, 120, 120),
            )

    tail_wag = math.sin(frame / total_frames * math.pi * 10) * 0.5
    side = 1 if frame % (total_frames * 2) < total_frames else -1
    tail_x = cx - 45 * side
    tail_y = cy + 10 + bounce
    for i in range(6):
        t = i / 5
        x = tail_x + math.sin(t * math.pi + tail_wag * math.pi) * (8 + i * 3) * side
        y = tail_y + t * 25
        width = 7 - i
        draw.ellipse([x - width // 2, y - 2, x + width // 2, y + 2], fill=main_color)


def draw_cat(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a claymorphism-style cat."""
    cx, cy = 64, 64

    highlight = tuple(min(c + 40, 255) for c in color[:3]) + (255,)
    shadow = tuple(max(c - 30, 0) for c in color[:3]) + (255,)

    draw_claymorphism_body(draw, cx, cy, 45, color, highlight, shadow)
    draw_cat_face(draw, cx, cy, frame, total_frames, color, is_sleeping)


def draw_dog(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a claymorphism-style dog."""
    cx, cy = 64, 64

    highlight = tuple(min(c + 40, 255) for c in color[:3]) + (255,)
    shadow = tuple(max(c - 30, 0) for c in color[:3]) + (255,)

    draw_claymorphism_body(draw, cx, cy, 45, color, highlight, shadow)
    draw_dog_face(draw, cx, cy, frame, total_frames, color, is_sleeping)


def create_pet_sprites(output_dir: Path, name: str, draw_func) -> None:
    """Create claymorphism-style sprites for a pet type."""
    output_dir.mkdir(parents=True, exist_ok=True)

    behaviors = {
        "idle": (12, False),
        "walk": (12, False),
        "sleep": (6, True),
        "eat": (12, False),
        "play": (12, False),
    }

    color_schemes = {
        "cat": {
            "idle": (255, 180, 120),
            "walk": (255, 180, 120),
            "sleep": (180, 180, 180),
            "eat": (255, 160, 100),
            "play": (255, 140, 80),
        },
        "dog": {
            "idle": (200, 160, 120),
            "walk": (200, 160, 120),
            "sleep": (160, 160, 160),
            "eat": (180, 140, 100),
            "play": (170, 120, 80),
        },
        "default": {
            "idle": (100, 160, 255),
            "walk": (100, 160, 255),
            "sleep": (160, 160, 180),
            "eat": (80, 140, 240),
            "play": (60, 120, 220),
        },
    }

    colors = color_schemes.get(name, color_schemes["default"])

    for behavior, (frame_count, is_sleeping) in behaviors.items():
        for frame in range(frame_count):
            img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            pet_color = colors.get(behavior, colors["idle"]) + (255,)
            draw_func(img, draw, frame, frame_count, pet_color, is_sleeping)
            img = add_edge_feather(img, radius=2)

            filename = f"{behavior}_{frame:02d}.png"
            img.save(output_dir / filename)

    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    draw_func(icon, icon_draw, 0, 1, colors["idle"] + (255,), False)

    icon_final = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    icon_final.paste(icon, (0, 0), icon)
    icon_final.save(output_dir.parent / "icon.png")

    print(f"Created {name} claymorphism sprites in {output_dir}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"

    create_pet_sprites(base_dir / "cat", "cat", draw_cat)
    create_pet_sprites(base_dir / "dog", "dog", draw_dog)
    create_pet_sprites(base_dir / "default", "default", draw_cat)

    print("All claymorphism-style pet sprites generated!")

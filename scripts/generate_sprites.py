"""Generate anime-style pet sprites with smooth animations."""

from pathlib import Path
from PIL import Image, ImageDraw
import math


def draw_cat(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw an anime-style cat."""
    cx, cy = 64, 64

    bounce = int(math.sin(frame / total_frames * math.pi * 2) * 3)

    if is_sleeping:
        draw.ellipse([20, 50, 108, 90], fill=color, outline="#333333", width=2)
        draw.ellipse([75, 55, 100, 80], fill=color, outline="#333333", width=2)
        draw.ellipse([85, 58, 95, 72], fill="white", outline="#333333", width=1)
        draw.line([88, 68, 92, 68], fill="#333333", width=2)
        draw.line([35, 35, 50, 45], fill=color, width=3)
        draw.line([75, 35, 60, 45], fill=color, width=3)
    else:
        draw.ellipse([20, 30 + bounce, 108, 100 + bounce], fill=color, outline="#333333", width=2)

        ear1 = [(25, 30 + bounce), (35, 10 + bounce), (45, 30 + bounce)]
        ear2 = [(83, 30 + bounce), (93, 10 + bounce), (103, 30 + bounce)]
        draw.polygon(ear1, fill=color, outline="#333333")
        draw.polygon(ear2, fill=color, outline="#333333")

        inner_ear1 = [(30, 28 + bounce), (35, 15 + bounce), (42, 28 + bounce)]
        inner_ear2 = [(86, 28 + bounce), (93, 15 + bounce), (98, 28 + bounce)]
        draw.polygon(inner_ear1, fill="#FFB6C1")
        draw.polygon(inner_ear2, fill="#FFB6C1")

        eye_offset = int(math.sin(frame / total_frames * math.pi * 4) * 2)
        draw.ellipse([35, 50 + bounce, 55, 70 + bounce], fill="white", outline="#333333", width=1)
        draw.ellipse([73, 50 + bounce, 93, 70 + bounce], fill="white", outline="#333333", width=1)
        draw.ellipse([40 + eye_offset, 55 + bounce, 50 + eye_offset, 65 + bounce], fill="#333333")
        draw.ellipse([78 + eye_offset, 55 + bounce, 88 + eye_offset, 65 + bounce], fill="#333333")

        draw.ellipse([43, 57 + bounce, 47, 61 + bounce], fill="white")
        draw.ellipse([81, 57 + bounce, 85, 61 + bounce], fill="white")

        draw.ellipse([58, 72 + bounce, 70, 80 + bounce], fill="#FFB6C1", outline="#333333", width=1)

        nose_y = 78 + bounce
        draw.polygon(
            [(64, nose_y), (60, nose_y + 5), (68, nose_y + 5)],
            fill="#FFB6C1",
            outline="#333333",
            width=1,
        )

        mouth_open = int(math.sin(frame / total_frames * math.pi * 6) * 3) if not is_sleeping else 0
        draw.arc([55, nose_y + 3, 73, nose_y + 12 + mouth_open], 0, 180, fill="#333333", width=1)

        tail_angle = math.sin(frame / total_frames * math.pi * 4) * 0.3
        tail_points = []
        for i in range(5):
            t = i / 4
            x = 105 + math.sin(t * math.pi + tail_angle * math.pi) * (15 + i * 3)
            y = 70 + bounce + i * 4
            tail_points.append((x, y))
        if len(tail_points) > 1:
            draw.line(tail_points, fill=color, width=8)
            draw.line(tail_points, fill=color, width=6)


def draw_dog(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw an anime-style dog."""
    cx, cy = 64, 64

    bounce = int(math.sin(frame / total_frames * math.pi * 2) * 3)

    if is_sleeping:
        draw.ellipse([20, 50, 108, 90], fill=color, outline="#333333", width=2)
        draw.ellipse([75, 55, 100, 80], fill=color, outline="#333333", width=2)
        draw.ellipse([85, 58, 95, 72], fill="white", outline="#333333", width=1)
        draw.line([88, 68, 92, 68], fill="#333333", width=2)
        draw.ellipse([15, 30, 40, 55], fill=color, outline="#333333", width=2)
        draw.ellipse([88, 30, 113, 55], fill=color, outline="#333333", width=2)
    else:
        draw.ellipse([20, 30 + bounce, 108, 100 + bounce], fill=color, outline="#333333", width=2)

        draw.ellipse([10, 25 + bounce, 45, 55 + bounce], fill=color, outline="#333333", width=2)
        draw.ellipse([83, 25 + bounce, 118, 55 + bounce], fill=color, outline="#333333", width=2)

        eye_blink = frame % max(total_frames // 2, 1) < 2
        eye_height = 4 if eye_blink else 15

        draw.ellipse(
            [35, 50 + bounce, 55, 50 + bounce + eye_height],
            fill="white",
            outline="#333333",
            width=1,
        )
        draw.ellipse(
            [73, 50 + bounce, 93, 50 + bounce + eye_height],
            fill="white",
            outline="#333333",
            width=1,
        )

        if not eye_blink:
            draw.ellipse([42, 53 + bounce, 50, 63 + bounce], fill="#333333")
            draw.ellipse([80, 53 + bounce, 88, 63 + bounce], fill="#333333")
            draw.ellipse([44, 55 + bounce, 47, 58 + bounce], fill="white")
            draw.ellipse([82, 55 + bounce, 85, 58 + bounce], fill="white")

        draw.ellipse([58, 70 + bounce, 70, 80 + bounce], fill="#333333", outline="#333333", width=1)

        nose_y = 75 + bounce
        draw.ellipse([58, nose_y, 70, nose_y + 10], fill="#333333")
        draw.ellipse([60, nose_y + 2, 64, nose_y + 6], fill="#666666")

        tongue_out = int(math.sin(frame / total_frames * math.pi * 6) * 5) if not is_sleeping else 0
        if tongue_out > 0:
            draw.ellipse([60, nose_y + 10, 68, nose_y + 10 + tongue_out], fill="#FF6B6B")

        tail_wag = math.sin(frame / total_frames * math.pi * 8) * 0.4
        tail_base_x = 15 if frame % (total_frames * 2) < total_frames else 113
        tail_points = []
        for i in range(5):
            t = i / 4
            x = tail_base_x + math.sin(t * math.pi + tail_wag * math.pi) * (10 + i * 2) * (
                -1 if tail_base_x < 64 else 1
            )
            y = 40 + bounce + i * 5
            tail_points.append((x, y))
        if len(tail_points) > 1:
            draw.line(tail_points, fill=color, width=8)
            draw.line(tail_points, fill=color, width=6)


def create_pet_sprites(output_dir: Path, name: str, color: str, draw_func) -> None:
    """Create sprites for a pet type."""
    output_dir.mkdir(parents=True, exist_ok=True)

    behaviors = {
        "idle": (8, False),
        "walk": (8, False),
        "sleep": (4, True),
        "eat": (8, False),
        "play": (8, False),
    }

    color_map = {
        "cat": {
            "idle": (255, 165, 79, 255),
            "walk": (255, 165, 79, 255),
            "sleep": (180, 180, 180, 255),
            "eat": (255, 165, 79, 255),
            "play": (255, 140, 0, 255),
        },
        "dog": {
            "idle": (139, 90, 43, 255),
            "walk": (139, 90, 43, 255),
            "sleep": (160, 160, 160, 255),
            "eat": (139, 90, 43, 255),
            "play": (160, 80, 30, 255),
        },
        "default": {
            "idle": (100, 149, 237, 255),
            "walk": (100, 149, 237, 255),
            "sleep": (180, 180, 180, 255),
            "eat": (100, 149, 237, 255),
            "play": (70, 130, 200, 255),
        },
    }

    pet_colors = color_map.get(name, color_map["default"])

    for behavior, (frame_count, is_sleeping) in behaviors.items():
        for frame in range(frame_count):
            img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            pet_color = pet_colors.get(behavior, pet_colors["idle"])
            draw_func(img, draw, frame, frame_count, pet_color, is_sleeping)

            filename = f"{behavior}_{frame:02d}.png"
            img.save(output_dir / filename)

    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    draw_func(icon, icon_draw, 0, 1, pet_colors["idle"], False)

    icon_small = icon.resize((32, 32), Image.Resampling.LANCZOS)
    icon_final = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    icon_final.paste(icon_small, (16, 16))
    icon_final.save(output_dir.parent / "icon.png")

    print(f"Created {name} sprites in {output_dir}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"

    create_pet_sprites(base_dir / "cat", "cat", "orange", draw_cat)
    create_pet_sprites(base_dir / "dog", "dog", "brown", draw_dog)
    create_pet_sprites(base_dir / "default", "default", "blue", draw_cat)

    print("All anime-style pet sprites generated!")

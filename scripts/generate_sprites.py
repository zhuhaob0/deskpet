"""Generate full-body pet sprites with four-legged walking animation."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import math


def add_edge_feather(img: Image.Image, radius: int = 2) -> Image.Image:
    """Add feather effect to edges for smooth transparency."""
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    alpha = img.split()[3]
    blurred_alpha = alpha.filter(ImageFilter.GaussianBlur(radius=radius))
    img.putalpha(blurred_alpha)
    return img


def draw_full_cat_walking(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a full cat body with four-legged walking animation."""
    cx, cy = view_width // 2, view_height // 2

    leg_cycle = math.sin(frame / total_frames * math.pi * 2) * 12
    body_bounce = abs(math.sin(frame / total_frames * math.pi * 2)) * 3

    body_y = cy - 10 + body_bounce

    draw.ellipse([cx - 40, body_y - 25, cx + 40, body_y + 25], fill=main_color)

    head_x, head_y = cx + 30, body_y - 15
    draw.ellipse([head_x - 20, head_y - 20, head_x + 15, head_y + 15], fill=main_color)

    ear1 = [(head_x - 15, head_y - 15), (head_x - 8, head_y - 30), (head_x, head_y - 15)]
    ear2 = [(head_x + 5, head_y - 15), (head_x + 12, head_y - 30), (head_x + 18, head_y - 15)]
    draw.polygon(ear1, fill=main_color)
    draw.polygon(ear2, fill=main_color)
    draw.polygon(
        [(head_x - 13, head_y - 15), (head_x - 8, head_y - 25), (head_x - 2, head_y - 15)],
        fill="#FFB6C1",
    )
    draw.polygon(
        [(head_x + 7, head_y - 15), (head_x + 12, head_y - 25), (head_x + 16, head_y - 15)],
        fill="#FFB6C1",
    )

    eye_offset = int(math.sin(frame / total_frames * math.pi * 4) * 2)
    draw.ellipse([head_x - 5, head_y - 8, head_x + 2, head_y + 2], fill="white")
    draw.ellipse([head_x + 5, head_y - 8, head_x + 12, head_y + 2], fill="white")
    draw.ellipse(
        [head_x - 2 + eye_offset, head_y - 5, head_x + eye_offset, head_y - 1], fill="#333"
    )
    draw.ellipse(
        [head_x + 8 + eye_offset, head_y - 5, head_x + 10 + eye_offset, head_y - 1], fill="#333"
    )

    draw.ellipse([head_x + 8, head_y + 3, head_x + 12, head_y + 8], fill="#FFB6C1")
    draw.arc([head_x - 5, head_y + 5, head_x + 8, head_y + 12], 0, 180, fill="#333", width=1)

    tail_start_x, tail_start_y = cx - 40, body_y
    tail_wave = math.sin(frame / total_frames * math.pi * 3) * 15
    tail_points = []
    for i in range(8):
        t = i / 7
        x = tail_start_x - t * 35
        y = tail_start_y + math.sin(t * math.pi + tail_wave * 0.1) * (8 + i * 2)
        tail_points.append((x, y))
    if len(tail_points) > 1:
        draw.line(tail_points, fill=main_color, width=8)
        draw.line(tail_points, fill=main_color, width=5)

    front_leg_offset = int(leg_cycle)
    back_leg_offset = int(-leg_cycle)

    draw.ellipse(
        [cx + 10, body_y + 15 + front_leg_offset, cx + 18, body_y + 45 + front_leg_offset],
        fill=main_color,
    )
    draw.ellipse(
        [cx - 18, body_y + 15 + back_leg_offset, cx - 10, body_y + 45 + back_leg_offset],
        fill=main_color,
    )
    draw.ellipse(
        [
            cx + 15,
            body_y + 10 + front_leg_offset // 2,
            cx + 22,
            body_y + 20 + front_leg_offset // 2,
        ],
        fill=main_color,
    )
    draw.ellipse(
        [cx - 22, body_y + 10 + back_leg_offset // 2, cx - 15, body_y + 20 + back_leg_offset // 2],
        fill=main_color,
    )


def draw_full_cat_idle(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a full cat in idle/sleeping pose."""
    cx, cy = view_width // 2, view_height // 2

    breathe = math.sin(frame / total_frames * math.pi * 2) * 2

    draw.ellipse([cx - 50 + breathe, cy - 20, cx + 50 - breathe, cy + 20], fill=main_color)

    head_x, head_y = cx + 35, cy - 10
    draw.ellipse([head_x - 22, head_y - 22, head_x + 18, head_y + 18], fill=main_color)

    ear1 = [(head_x - 18, head_y - 18), (head_x - 10, head_y - 38), (head_x - 2, head_y - 18)]
    ear2 = [(head_x + 2, head_y - 18), (head_x + 10, head_y - 38), (head_x + 18, head_y - 18)]
    draw.polygon(ear1, fill=main_color)
    draw.polygon(ear2, fill=main_color)
    draw.polygon(
        [(head_x - 15, head_y - 18), (head_x - 10, head_y - 32), (head_x - 5, head_y - 18)],
        fill="#FFB6C1",
    )
    draw.polygon(
        [(head_x + 5, head_y - 18), (head_x + 10, head_y - 32), (head_x + 15, head_y - 18)],
        fill="#FFB6C1",
    )

    draw.ellipse([head_x - 8, head_y - 8, head_x + 2, head_y + 4], fill="white")
    draw.ellipse([head_x + 6, head_y - 8, head_x + 16, head_y + 4], fill="white")
    draw.ellipse([head_x - 4, head_y - 4, head_x - 1, head_y - 1], fill="#333")
    draw.ellipse([head_x + 10, head_y - 4, head_x + 13, head_y - 1], fill="#333")

    draw.ellipse([head_x + 10, head_y + 6, head_x + 15, head_y + 12], fill="#FFB6C1")

    tail_x, tail_y = cx - 50, cy
    tail_curve = math.sin(frame / total_frames * math.pi * 2) * 10
    tail_points = [(tail_x, tail_y + i * 3) for i in range(6)]
    tail_curved = [
        (tail_x - i * 5 + (tail_curve if i > 2 else 0), tail_y + i * 4) for i in range(6)
    ]
    draw.line(tail_curved, fill=main_color, width=8)

    draw.ellipse([cx + 30, cy + 15, cx + 40, cy + 30], fill=main_color)
    draw.ellipse([cx - 40, cy + 15, cx - 30, cy + 30], fill=main_color)
    draw.ellipse([cx + 15, cy + 15, cx + 25, cy + 30], fill=main_color)
    draw.ellipse([cx - 25, cy + 15, cx - 15, cy + 30], fill=main_color)


def draw_full_cat_sleeping(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a sleeping cat curled up."""
    cx, cy = view_width // 2, view_height // 2

    draw.ellipse([cx - 50, cy - 25, cx + 50, cy + 25], fill=main_color)

    head_x, head_y = cx + 30, cy
    draw.ellipse([head_x - 25, head_y - 20, head_x + 20, head_y + 20], fill=main_color)

    ear1 = [(head_x - 20, head_y - 15), (head_x - 12, head_y - 32), (head_x - 5, head_y - 15)]
    ear2 = [(head_x + 5, head_y - 15), (head_x + 12, head_y - 32), (head_x + 20, head_y - 15)]
    draw.polygon(ear1, fill=main_color)
    draw.polygon(ear2, fill=main_color)

    zzz_y = cy - 40 + int(math.sin(frame / total_frames * math.pi * 4) * 5)
    draw.text((cx + 50, zzz_y), "Z", fill="#666")

    closed_eye = math.sin(frame / total_frames * math.pi * 2) > 0
    if closed_eye:
        draw.arc([head_x - 12, head_y - 5, head_x - 2, head_y + 5], 0, 180, fill="#333", width=2)
        draw.arc([head_x + 2, head_y - 5, head_x + 12, head_y + 5], 0, 180, fill="#333", width=2)
    else:
        draw.ellipse([head_x - 12, head_y - 5, head_x - 2, head_y + 5], fill="white")
        draw.ellipse([head_x + 2, head_y - 5, head_x + 12, head_y + 5], fill="white")

    draw.ellipse([head_x + 8, head_y + 8, head_x + 14, head_y + 14], fill="#FFB6C1")

    tail_x, tail_y = cx - 50, cy + 10
    tail_curled = [(tail_x - i * 4, tail_y + math.sin(i * 0.5) * 10) for i in range(10)]
    draw.line(tail_curled, fill=main_color, width=8)


def draw_full_cat_eating(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a cat eating."""
    cx, cy = view_width // 2, view_height // 2

    bob = int(abs(math.sin(frame / total_frames * math.pi * 4)) * 5)

    body_y = cy + bob
    draw.ellipse([cx - 40, body_y - 25, cx + 40, body_y + 25], fill=main_color)

    head_x, head_y = cx + 30, body_y - 20 + bob
    draw.ellipse([head_x - 20, head_y - 20, head_x + 15, head_y + 15], fill=main_color)

    ear1 = [(head_x - 15, head_y - 15), (head_x - 8, head_y - 30), (head_x, head_y - 15)]
    ear2 = [(head_x + 5, head_y - 15), (head_x + 12, head_y - 30), (head_x + 18, head_y - 15)]
    draw.polygon(ear1, fill=main_color)
    draw.polygon(ear2, fill=main_color)
    draw.polygon(
        [(head_x - 13, head_y - 15), (head_x - 8, head_y - 25), (head_x - 2, head_y - 15)],
        fill="#FFB6C1",
    )
    draw.polygon(
        [(head_x + 7, head_y - 15), (head_x + 12, head_y - 25), (head_x + 16, head_y - 15)],
        fill="#FFB6C1",
    )

    mouth_open = int(abs(math.sin(frame / total_frames * math.pi * 6)) * 8)
    draw.ellipse([head_x + 8, head_y + 5, head_x + 14, head_y + 10 + mouth_open], fill="#FF6B6B")

    draw.ellipse([head_x - 5, head_y - 8, head_x + 2, head_y + 2], fill="white")
    draw.ellipse([head_x + 5, head_y - 8, head_x + 12, head_y + 2], fill="white")
    draw.ellipse([head_x - 2, head_y - 5, head_x, head_y - 1], fill="#333")
    draw.ellipse([head_x + 8, head_y - 5, head_x + 10, head_y - 1], fill="#333")

    draw.ellipse([head_x + 5, head_y + 2, head_x + 9, head_y + 6], fill="#FFB6C1")

    tail_wave = math.sin(frame / total_frames * math.pi * 4) * 12
    tail_points = [
        (cx - 40 - i * 4 + (tail_wave if i > 3 else 0), cy - 5 + i * 2) for i in range(8)
    ]
    draw.line(tail_points, fill=main_color, width=7)

    draw.ellipse([cx + 15, body_y + 20, cx + 22, body_y + 40], fill=main_color)
    draw.ellipse([cx - 22, body_y + 20, cx - 15, body_y + 40], fill=main_color)
    draw.ellipse([cx + 8, body_y + 18, cx + 15, body_y + 32], fill=main_color)
    draw.ellipse([cx - 15, body_y + 18, cx - 8, body_y + 32], fill=main_color)


def draw_full_cat_playing(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a cat playing/jumping."""
    cx, cy = view_width // 2, view_height // 2

    jump = int(abs(math.sin(frame / total_frames * math.pi * 2)) * 15)
    rotation = math.sin(frame / total_frames * math.pi * 3) * 0.2

    body_y = cy - 20 - jump
    draw.ellipse([cx - 40, body_y - 25, cx + 40, body_y + 25], fill=main_color)

    head_x, head_y = cx + 30, body_y - 15
    draw.ellipse([head_x - 20, head_y - 20, head_x + 15, head_y + 15], fill=main_color)

    ear1 = [(head_x - 15, head_y - 15), (head_x - 8, head_y - 30), (head_x, head_y - 15)]
    ear2 = [(head_x + 5, head_y - 15), (head_x + 12, head_y - 30), (head_x + 18, head_y - 15)]
    draw.polygon(ear1, fill=main_color)
    draw.polygon(ear2, fill=main_color)
    draw.polygon(
        [(head_x - 13, head_y - 15), (head_x - 8, head_y - 25), (head_x - 2, head_y - 15)],
        fill="#FFB6C1",
    )
    draw.polygon(
        [(head_x + 7, head_y - 15), (head_x + 12, head_y - 25), (head_x + 16, head_y - 15)],
        fill="#FFB6C1",
    )

    excited = True
    draw.ellipse([head_x - 5, head_y - 10, head_x + 2, head_y - 2], fill="white")
    draw.ellipse([head_x + 5, head_y - 10, head_x + 12, head_y - 2], fill="white")
    draw.ellipse([head_x - 2, head_y - 7, head_x, head_y - 3], fill="#333")
    draw.ellipse([head_x + 8, head_y - 7, head_x + 10, head_y - 3], fill="#333")

    draw.ellipse([head_x + 8, head_y + 3, head_x + 12, head_y + 8], fill="#FFB6C1")
    draw.arc([head_x - 5, head_y + 5, head_x + 8, head_y + 12], 0, 180, fill="#333", width=2)

    tail_up = math.sin(frame / total_frames * math.pi * 4) * 20
    tail_points = [(cx - 40 - i * 3, body_y - 10 - i * 8 - tail_up * (i / 7)) for i in range(6)]
    draw.line(tail_points, fill=main_color, width=7)

    leg_extend = int(abs(math.sin(frame / total_frames * math.pi * 4)) * 10)
    draw.ellipse(
        [cx + 15, body_y + 20 - leg_extend, cx + 22, body_y + 45 - leg_extend], fill=main_color
    )
    draw.ellipse(
        [cx - 22, body_y + 20 + leg_extend, cx - 15, body_y + 45 + leg_extend], fill=main_color
    )


def draw_full_dog_walking(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a full dog body with four-legged walking animation."""
    cx, cy = view_width // 2, view_height // 2

    leg_cycle = math.sin(frame / total_frames * math.pi * 2) * 14
    body_bounce = abs(math.sin(frame / total_frames * math.pi * 2)) * 4

    body_y = cy - 5 + body_bounce

    draw.ellipse([cx - 45, body_y - 22, cx + 45, body_y + 22], fill=main_color)

    head_x, head_y = cx + 40, body_y - 20
    draw.ellipse([head_x - 25, head_y - 22, head_x + 20, head_y + 18], fill=main_color)

    draw.ellipse([head_x - 25, head_y - 25, head_x - 5, head_y + 5], fill=main_color)
    draw.ellipse([head_x + 5, head_y - 25, head_x + 25, head_y + 5], fill=main_color)
    draw.ellipse([head_x - 22, head_y - 18, head_x - 10, head_y], fill="#D4A574")
    draw.ellipse([head_x + 10, head_y - 18, head_x + 22, head_y], fill="#D4A574")

    eye_blink = frame % max(total_frames // 2, 1) < 2
    eye_h = 4 if eye_blink else 14
    draw.ellipse([head_x - 12, head_y - 10, head_x - 2, head_y - 10 + eye_h], fill="white")
    draw.ellipse([head_x + 2, head_y - 10, head_x + 12, head_y - 10 + eye_h], fill="white")
    if not eye_blink:
        draw.ellipse([head_x - 9, head_y - 6, head_x - 4, head_y + 2], fill="#333")
        draw.ellipse([head_x + 4, head_y - 6, head_x + 9, head_y + 2], fill="#333")

    nose_color = "#333"
    draw.ellipse([head_x + 10, head_y + 5, head_x + 18, head_y + 14], fill=nose_color)
    draw.ellipse([head_x + 12, head_y + 7, head_x + 15, head_y + 10], fill="#555")

    tongue = int(abs(math.sin(frame / total_frames * math.pi * 5)) * 8)
    if tongue > 2:
        draw.ellipse([head_x + 8, head_y + 14, head_x + 16, head_y + 14 + tongue], fill="#FF8080")

    tail_wag = math.sin(frame / total_frames * math.pi * 8) * 25
    tail_base_x = cx - 45
    tail_points = [
        (tail_base_x - i * 5, body_y - 15 - i * 5 + tail_wag * (i / 6)) for i in range(6)
    ]
    draw.line(tail_points, fill=main_color, width=10)
    draw.line(tail_points, fill=main_color, width=7)

    front_leg = int(leg_cycle)
    back_leg = int(-leg_cycle)
    draw.ellipse(
        [cx + 18, body_y + 18 + front_leg, cx + 28, body_y + 48 + front_leg], fill=main_color
    )
    draw.ellipse(
        [cx - 28, body_y + 18 + back_leg, cx - 18, body_y + 48 + back_leg], fill=main_color
    )
    draw.ellipse(
        [cx + 10, body_y + 15 + front_leg // 2, cx + 20, body_y + 30 + front_leg // 2],
        fill=main_color,
    )
    draw.ellipse(
        [cx - 20, body_y + 15 + back_leg // 2, cx - 10, body_y + 30 + back_leg // 2],
        fill=main_color,
    )


def draw_full_dog_idle(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a full dog in idle pose."""
    cx, cy = view_width // 2, view_height // 2

    breathe = math.sin(frame / total_frames * math.pi * 2) * 3

    body_y = cy + breathe
    draw.ellipse([cx - 50, body_y - 25, cx + 50, body_y + 25], fill=main_color)

    head_x, head_y = cx + 35, body_y - 15
    draw.ellipse([head_x - 28, head_y - 25, head_x + 22, head_y + 20], fill=main_color)

    draw.ellipse([head_x - 28, head_y - 28, head_x - 8, head_y + 8], fill=main_color)
    draw.ellipse([head_x + 8, head_y - 28, head_x + 28, head_y + 8], fill=main_color)
    draw.ellipse([head_x - 24, head_y - 20, head_x - 12, head_y - 2], fill="#D4A574")
    draw.ellipse([head_x + 12, head_y - 20, head_x + 24, head_y - 2], fill="#D4A574")

    eye_blink = frame % max(total_frames // 2, 1) < 2
    draw.ellipse(
        [head_x - 15, head_y - 12, head_x - 4, head_y - 12 + (4 if eye_blink else 14)], fill="white"
    )
    draw.ellipse(
        [head_x + 4, head_y - 12, head_x + 15, head_y - 12 + (4 if eye_blink else 14)], fill="white"
    )
    if not eye_blink:
        draw.ellipse([head_x - 12, head_y - 8, head_x - 7, head_y], fill="#333")
        draw.ellipse([head_x + 7, head_y - 8, head_x + 12, head_y], fill="#333")

    draw.ellipse([head_x + 12, head_y + 5, head_x + 22, head_y + 16], fill="#333")

    tail_wag = math.sin(frame / total_frames * math.pi * 3) * 15
    tail_points = [(cx - 50 - i * 4, body_y - 10 - i * 3 + tail_wag * (i / 5)) for i in range(5)]
    draw.line(tail_points, fill=main_color, width=10)

    draw.ellipse([cx + 30, body_y + 20, cx + 40, body_y + 42], fill=main_color)
    draw.ellipse([cx - 40, body_y + 20, cx - 30, body_y + 42], fill=main_color)
    draw.ellipse([cx + 15, body_y + 18, cx + 25, body_y + 35], fill=main_color)
    draw.ellipse([cx - 25, body_y + 18, cx - 15, body_y + 35], fill=main_color)


def draw_full_dog_sleeping(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a sleeping dog."""
    cx, cy = view_width // 2, view_height // 2

    draw.ellipse([cx - 55, cy - 20, cx + 55, cy + 30], fill=main_color)

    head_x, head_y = cx + 40, cy
    draw.ellipse([head_x - 30, head_y - 25, head_x + 25, head_y + 25], fill=main_color)

    draw.ellipse([head_x - 30, head_y - 28, head_x - 10, head_y + 10], fill=main_color)
    draw.ellipse([head_x + 10, head_y - 28, head_x + 30, head_y + 10], fill=main_color)

    draw.arc([head_x - 15, head_y - 8, head_x - 5, head_y + 4], 0, 180, fill="#333", width=2)
    draw.arc([head_x + 5, head_y - 8, head_x + 15, head_y + 4], 0, 180, fill="#333", width=2)

    draw.ellipse([head_x + 15, head_y + 8, head_x + 24, head_y + 18], fill="#333")

    zzz = "Z" * (1 + int(frame % 3))
    draw.text((cx + 60, cy - 50), zzz, fill="#666")

    tail_x, tail_y = cx - 55, cy + 10
    tail_points = [(tail_x - i * 5, tail_y + math.sin(i * 0.8) * 8) for i in range(7)]
    draw.line(tail_points, fill=main_color, width=9)


def draw_full_dog_eating(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a dog eating."""
    cx, cy = view_width // 2, view_height // 2

    bob = int(abs(math.sin(frame / total_frames * math.pi * 4)) * 8)

    body_y = cy + bob
    draw.ellipse([cx - 45, body_y - 22, cx + 45, body_y + 22], fill=main_color)

    head_x, head_y = cx + 40, body_y - 25 + bob
    draw.ellipse([head_x - 25, head_y - 22, head_x + 20, head_y + 18], fill=main_color)

    draw.ellipse([head_x - 25, head_y - 25, head_x - 5, head_y + 5], fill=main_color)
    draw.ellipse([head_x + 5, head_y - 25, head_x + 25, head_y + 5], fill=main_color)
    draw.ellipse([head_x - 22, head_y - 18, head_x - 10, head_y - 2], fill="#D4A574")
    draw.ellipse([head_x + 10, head_y - 18, head_x + 22, head_y - 2], fill="#D4A574")

    draw.ellipse([head_x - 12, head_y - 10, head_x - 2, head_y + 4], fill="white")
    draw.ellipse([head_x + 2, head_y - 10, head_x + 12, head_y + 4], fill="white")
    draw.ellipse([head_x - 9, head_y - 6, head_x - 4, head_y], fill="#333")
    draw.ellipse([head_x + 4, head_y - 6, head_y + 9, head_y], fill="#333")

    draw.ellipse([head_x + 10, head_y + 8, head_x + 18, head_y + 18], fill="#333")

    tongue = int(abs(math.sin(frame / total_frames * math.pi * 6)) * 12)
    draw.ellipse([head_x + 6, head_y + 18, head_x + 14, head_y + 18 + tongue], fill="#FF8080")

    draw.ellipse([cx + 20, body_y + 18, cx + 30, body_y + 48], fill=main_color)
    draw.ellipse([cx - 30, body_y + 18, cx - 20, body_y + 48], fill=main_color)


def draw_full_dog_playing(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 160,
    view_height: int = 128,
) -> None:
    """Draw a dog playing."""
    cx, cy = view_width // 2, view_height // 2

    jump = int(abs(math.sin(frame / total_frames * math.pi * 2)) * 18)

    body_y = cy - 15 - jump
    draw.ellipse([cx - 45, body_y - 25, cx + 45, body_y + 25], fill=main_color)

    head_x, head_y = cx + 40, body_y - 22
    draw.ellipse([head_x - 25, head_y - 25, head_x + 20, head_y + 20], fill=main_color)

    draw.ellipse([head_x - 25, head_y - 28, head_x - 5, head_y + 8], fill=main_color)
    draw.ellipse([head_x + 5, head_y - 28, head_x + 25, head_y + 8], fill=main_color)

    draw.ellipse([head_x - 12, head_y - 12, head_x - 2, head_y + 2], fill="white")
    draw.ellipse([head_x + 2, head_y - 12, head_x + 12, head_y + 2], fill="white")
    draw.ellipse([head_x - 9, head_y - 8, head_x - 4, head_y - 2], fill="#333")
    draw.ellipse([head_x + 4, head_y - 8, head_x + 9, head_y - 2], fill="#333")

    draw.ellipse([head_x + 10, head_y + 5, head_x + 18, head_y + 15], fill="#333")

    tongue = int(abs(math.sin(frame / total_frames * math.pi * 6)) * 10)
    draw.ellipse([head_x + 6, head_y + 15, head_x + 14, head_y + 15 + tongue], fill="#FF8080")

    tail_wag = math.sin(frame / total_frames * math.pi * 8) * 30
    tail_points = [(cx - 45 - i * 4, body_y - 15 - i * 5 + tail_wag * (i / 5)) for i in range(5)]
    draw.line(tail_points, fill=main_color, width=10)

    leg_extend = int(abs(math.sin(frame / total_frames * math.pi * 4)) * 12)
    draw.ellipse(
        [cx + 20, body_y + 22 - leg_extend, cx + 30, body_y + 52 - leg_extend], fill=main_color
    )
    draw.ellipse(
        [cx - 30, body_y + 22 + leg_extend, cx - 20, body_y + 52 + leg_extend], fill=main_color
    )


def draw_cat(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a cat based on behavior."""
    color_rgba = color if len(color) == 4 else (*color, 255)
    if is_sleeping or "sleep" in str(frame):
        draw_full_cat_sleeping(draw, frame, total_frames, color_rgba)
    elif total_frames == 12:
        if "eat" in str(frame) or frame >= 8:
            draw_full_cat_eating(draw, frame, total_frames, color_rgba)
        elif "play" in str(frame) or frame >= 6:
            draw_full_cat_playing(draw, frame, total_frames, color_rgba)
        else:
            draw_full_cat_walking(draw, frame, total_frames, color_rgba)
    else:
        draw_full_cat_idle(draw, frame, total_frames, color_rgba)


def draw_dog(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: int,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a dog based on behavior."""
    color_rgba = color if len(color) == 4 else (*color, 255)
    if is_sleeping or "sleep" in str(frame):
        draw_full_dog_sleeping(draw, frame, total_frames, color_rgba)
    elif total_frames == 12:
        if "eat" in str(frame) or frame >= 8:
            draw_full_dog_eating(draw, frame, total_frames, color_rgba)
        elif "play" in str(frame) or frame >= 6:
            draw_full_dog_playing(draw, frame, total_frames, color_rgba)
        else:
            draw_full_dog_walking(draw, frame, total_frames, color_rgba)
    else:
        draw_full_dog_idle(draw, frame, total_frames, color_rgba)


def create_pet_sprites(output_dir: Path, name: str, draw_func) -> None:
    """Create full-body sprites for a pet type."""
    output_dir.mkdir(parents=True, exist_ok=True)

    view_width, view_height = 160, 128

    behaviors = {
        "idle": (16, False),
        "walk": (16, False),
        "sleep": (8, True),
        "eat": (16, False),
        "play": (16, False),
    }

    color_schemes = {
        "cat": {
            "idle": (255, 180, 120),
            "walk": (255, 180, 120),
            "sleep": (180, 175, 170),
            "eat": (255, 160, 100),
            "play": (255, 140, 80),
        },
        "dog": {
            "idle": (180, 140, 100),
            "walk": (180, 140, 100),
            "sleep": (160, 155, 150),
            "eat": (170, 130, 90),
            "play": (160, 110, 70),
        },
        "default": {
            "idle": (100, 160, 255),
            "walk": (100, 160, 255),
            "sleep": (150, 150, 170),
            "eat": (80, 140, 240),
            "play": (60, 120, 220),
        },
    }

    colors = color_schemes.get(name, color_schemes["default"])

    for behavior, (frame_count, is_sleeping) in behaviors.items():
        for frame in range(frame_count):
            img = Image.new("RGBA", (view_width, view_height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            pet_color = colors.get(behavior, colors["idle"])
            if len(pet_color) == 3:
                pet_color = pet_color + (255,)
            draw_func(img, draw, frame, frame_count, pet_color, is_sleeping)
            img = add_edge_feather(img, radius=2)

            filename = f"{behavior}_{frame:02d}.png"
            img.save(output_dir / filename)

    icon_size = 64
    icon = Image.new("RGBA", (view_width, view_height), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    draw_func(
        icon,
        icon_draw,
        0,
        1,
        colors["idle"] + (255,) if len(colors["idle"]) == 3 else colors["idle"],
        False,
    )
    icon = add_edge_feather(icon, radius=1)
    icon_resized = icon.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
    icon_final = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    icon_final.paste(icon_resized, (0, 0), icon_resized)
    icon_final.save(output_dir.parent / "icon.png")

    print(f"Created {name} full-body sprites in {output_dir}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"

    create_pet_sprites(base_dir / "cat", "cat", draw_cat)
    create_pet_sprites(base_dir / "dog", "dog", draw_dog)
    create_pet_sprites(base_dir / "default", "default", draw_cat)

    print("All full-body pet sprites generated!")

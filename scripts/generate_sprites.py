"""Generate detailed full-body pet sprites with clear limbs."""

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


def draw_detailed_limb(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    length: int,
    width: int,
    color: tuple,
    angle: float = 0,
) -> None:
    """Draw a detailed limb with rounded ends."""
    half_len = length // 2
    half_wid = width // 2

    points = []
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        rad = angle + math.pi * t
        x1 = x + math.sin(rad) * half_wid
        y1 = y + math.cos(rad) * half_wid
        points.append((x1, y1))

    draw.ellipse([x - half_wid, y - half_len, x + half_wid, y + half_len], fill=color, outline=None)

    draw.ellipse(
        [x - half_wid + 2, y - half_len + 2, x + half_wid - 2, y + half_len - 2],
        fill=color,
        outline=None,
    )


def draw_detailed_paw(draw: ImageDraw.ImageDraw, x: int, y: int, size: int, color: tuple) -> None:
    """Draw a detailed paw with toes."""
    draw.ellipse(
        [x - size // 2, y - size // 3, x + size // 2, y + size // 3], fill=color, outline=None
    )

    toe_size = size // 4
    draw.ellipse(
        [x - size // 2 + 2, y - size // 3 - 2, x - size // 4, y - 2], fill=color, outline=None
    )
    draw.ellipse([x - size // 6, y - size // 3 - 3, x + size // 6, y - 2], fill=color, outline=None)
    draw.ellipse(
        [x + size // 4, y - size // 3 - 2, x + size // 2 - 2, y - 2], fill=color, outline=None
    )


def draw_full_cat_walking(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 200,
    view_height: int = 160,
) -> None:
    """Draw a detailed walking cat with visible limbs."""
    cx, cy = view_width // 2, view_height // 2 + 10

    walk_cycle = frame / total_frames * math.pi * 2

    front_leg_angle = math.sin(walk_cycle) * 0.6
    back_leg_angle = math.sin(walk_cycle + math.pi) * 0.6

    body_bounce = abs(math.sin(walk_cycle)) * 4

    body_x, body_y = cx, cy + body_bounce

    tail_wag = math.sin(walk_cycle * 2) * 0.4
    tail_base_x, tail_base_y = body_x - 55, body_y - 15
    tail_length = 45
    for i in range(8):
        t = i / 7
        angle = math.pi + tail_wag * t * math.pi
        x = tail_base_x - math.cos(angle) * tail_length * t
        y = tail_base_y - math.sin(angle) * tail_length * t * 0.6
        width = int(10 - t * 6)
        draw.ellipse(
            [x - width // 2, y - width // 2, x + width // 2, y + width // 2],
            fill=main_color,
            outline=None,
        )

    dark_color = tuple(max(c - 30, 0) for c in main_color[:3]) + main_color[3:]

    draw.ellipse(
        [body_x - 50, body_y - 30, body_x + 50, body_y + 30], fill=main_color, outline=None
    )

    leg_length = 35
    leg_width = 12

    leg1_x, leg1_y = body_x + 20, body_y + 25
    leg1_offset = int(math.sin(walk_cycle) * 15)
    draw.ellipse(
        [
            leg1_x - leg_width // 2,
            leg1_y + leg1_offset,
            leg1_x + leg_width // 2,
            leg1_y + leg_length + leg1_offset,
        ],
        fill=dark_color,
        outline=None,
    )
    draw.ellipse(
        [
            leg1_x - leg_width // 2 + 2,
            leg1_y + leg_length + leg1_offset - 5,
            leg1_x + leg_width // 2 - 2,
            leg1_y + leg_length + leg1_offset + 8,
        ],
        fill=main_color,
        outline=None,
    )

    leg2_x, leg2_y = body_x - 20, body_y + 25
    leg2_offset = int(math.sin(walk_cycle + math.pi) * 15)
    draw.ellipse(
        [
            leg2_x - leg_width // 2,
            leg2_y + leg2_offset,
            leg2_x + leg_width // 2,
            leg2_y + leg_length + leg2_offset,
        ],
        fill=dark_color,
        outline=None,
    )
    draw.ellipse(
        [
            leg2_x - leg_width // 2 + 2,
            leg2_y + leg_length + leg2_offset - 5,
            leg2_x + leg_width // 2 - 2,
            leg2_y + leg_length + leg2_offset + 8,
        ],
        fill=main_color,
        outline=None,
    )

    leg3_x, leg3_y = body_x + 35, body_y + 20
    leg3_offset = int(math.sin(walk_cycle + math.pi) * 12)
    draw.ellipse(
        [
            leg3_x - leg_width // 2 + 2,
            leg3_y + leg3_offset,
            leg3_x + leg_width // 2 + 2,
            leg3_y + leg_length - 5 + leg3_offset,
        ],
        fill=dark_color,
        outline=None,
    )
    draw.ellipse(
        [
            leg3_x - leg_width // 2 + 4,
            leg3_y + leg_length - 8 + leg3_offset,
            leg3_x + leg_width // 2,
            leg3_y + leg_length + leg3_offset + 5,
        ],
        fill=main_color,
        outline=None,
    )

    leg4_x, leg4_y = body_x - 35, body_y + 20
    leg4_offset = int(math.sin(walk_cycle) * 12)
    draw.ellipse(
        [
            leg4_x - leg_width // 2 - 2,
            leg4_y + leg4_offset,
            leg4_x + leg_width // 2 - 2,
            leg4_y + leg_length - 5 + leg4_offset,
        ],
        fill=dark_color,
        outline=None,
    )
    draw.ellipse(
        [
            leg4_x - leg_width // 2,
            leg4_y + leg_length - 8 + leg4_offset,
            leg4_x + leg_width // 2 - 4,
            leg4_y + leg_length + leg4_offset + 5,
        ],
        fill=main_color,
        outline=None,
    )

    head_x, head_y = body_x + 45, body_y - 20

    ear_size = 18
    ear1 = [
        (head_x - 12, head_y - 8),
        (head_x - 5, head_y - ear_size - 5),
        (head_x + 3, head_y - 8),
    ]
    ear2 = [
        (head_x + 5, head_y - 8),
        (head_x + 13, head_y - ear_size - 5),
        (head_x + 18, head_y - 8),
    ]
    draw.polygon(ear1, fill=main_color, outline=None)
    draw.polygon(ear2, fill=main_color, outline=None)
    draw.polygon(
        [(head_x - 9, head_y - 8), (head_x - 5, head_y - ear_size), (head_x - 1, head_y - 8)],
        fill="#FFB6C1",
        outline=None,
    )
    draw.polygon(
        [(head_x + 8, head_y - 8), (head_x + 13, head_y - ear_size), (head_x + 16, head_y - 8)],
        fill="#FFB6C1",
        outline=None,
    )

    draw.ellipse(
        [head_x - 20, head_y - 18, head_x + 22, head_y + 18], fill=main_color, outline=None
    )

    eye_y = head_y - 5
    eye_size = 10

    eye_offset = int(math.sin(walk_cycle * 2) * 2)
    draw.ellipse([head_x - 12, eye_y, head_x - 2, eye_y + eye_size], fill="white", outline=None)
    draw.ellipse([head_x + 2, eye_y, head_x + 12, eye_y + eye_size], fill="white", outline=None)

    pupil_size = 5
    draw.ellipse(
        [head_x - 9 + eye_offset, eye_y + 2, head_x - 4 + eye_offset, eye_y + 7],
        fill="#222",
        outline=None,
    )
    draw.ellipse(
        [head_x + 5 + eye_offset, eye_y + 2, head_x + 10 + eye_offset, eye_y + 7],
        fill="#222",
        outline=None,
    )

    draw.ellipse(
        [head_x - 7 + eye_offset, eye_y + 3, head_x - 5 + eye_offset, eye_y + 5],
        fill="white",
        outline=None,
    )
    draw.ellipse(
        [head_x + 7 + eye_offset, eye_y + 3, head_x + 9 + eye_offset, eye_y + 5],
        fill="white",
        outline=None,
    )

    nose_size = 6
    draw.polygon(
        [
            (head_x, head_y + 4),
            (head_x - nose_size // 2, head_y + nose_size + 2),
            (head_x + nose_size // 2, head_y + nose_size + 2),
        ],
        fill="#FF8888",
        outline=None,
    )

    mouth_y = head_y + nose_size + 6
    draw.arc([head_x - 8, mouth_y, head_x + 8, mouth_y + 10], 0, 180, fill="#555", width=2)

    whisker_y = head_y + 8
    for offset in [-8, -4, 0, 4]:
        draw.line(
            [head_x - 18, whisker_y + offset, head_x - 35, whisker_y + offset - 3],
            fill="#AAA",
            width=1,
        )
        draw.line(
            [head_x + 18, whisker_y + offset, head_x + 35, whisker_y + offset - 3],
            fill="#AAA",
            width=1,
        )


def draw_full_cat_idle(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 200,
    view_height: int = 160,
) -> None:
    """Draw a detailed idle cat."""
    cx, cy = view_width // 2, view_height // 2 + 15

    breathe = math.sin(frame / total_frames * math.pi * 2) * 3
    body_x, body_y = cx, cy + breathe

    tail_wag = math.sin(frame / total_frames * math.pi * 3) * 0.3
    tail_base_x, tail_base_y = body_x - 55, body_y - 10
    for i in range(10):
        t = i / 9
        angle = math.pi + tail_wag * t * math.pi * 0.5
        x = tail_base_x - math.cos(angle) * 50 * t
        y = tail_base_y - math.sin(angle) * 20 * t
        width = int(12 - t * 8)
        draw.ellipse(
            [x - width // 2, y - width // 2, x + width // 2, y + width // 2],
            fill=main_color,
            outline=None,
        )

    draw.ellipse(
        [body_x - 55, body_y - 30, body_x + 55, body_y + 30], fill=main_color, outline=None
    )

    leg_width, leg_length = 14, 40
    for lx, ly in [
        (body_x + 25, body_y + 25),
        (body_x - 25, body_y + 25),
        (body_x + 40, body_y + 22),
        (body_x - 40, body_y + 22),
    ]:
        draw.ellipse(
            [lx - leg_width // 2, ly, lx + leg_width // 2, ly + leg_length],
            fill=main_color,
            outline=None,
        )
        draw.ellipse(
            [
                lx - leg_width // 2 + 2,
                ly + leg_length - 8,
                lx + leg_width // 2 - 2,
                ly + leg_length + 5,
            ],
            fill=main_color,
            outline=None,
        )

    head_x, head_y = body_x + 40, body_y - 15

    for angle_offset, x_offset in [(-0.3, -12), (0.3, 12)]:
        ear_x = head_x + x_offset
        ear_top = head_y - 35
        ear_base = head_y - 12
        ear_points = [(ear_x - 10, ear_base), (ear_x, ear_top), (ear_x + 10, ear_base)]
        draw.polygon(ear_points, fill=main_color, outline=None)
        inner_ear = [(ear_x - 5, ear_base - 3), (ear_x, ear_top + 5), (ear_x + 5, ear_base - 3)]
        draw.polygon(inner_ear, fill="#FFB6C1", outline=None)

    draw.ellipse(
        [head_x - 22, head_y - 20, head_x + 25, head_y + 20], fill=main_color, outline=None
    )

    eye_blink = frame % 4 < 1
    eye_h = 3 if eye_blink else 12
    draw.ellipse(
        [head_x - 12, head_y - 8, head_x - 2, head_y - 8 + eye_h], fill="white", outline=None
    )
    draw.ellipse(
        [head_x + 2, head_y - 8, head_x + 12, head_y - 8 + eye_h], fill="white", outline=None
    )

    if not eye_blink:
        draw.ellipse([head_x - 9, head_y - 5, head_x - 4, head_y + 1], fill="#222", outline=None)
        draw.ellipse([head_x + 5, head_y - 5, head_x + 10, head_y + 1], fill="#222", outline=None)
        draw.ellipse([head_x - 8, head_y - 4, head_x - 5, head_y - 2], fill="white", outline=None)
        draw.ellipse([head_x + 6, head_y - 4, head_x + 9, head_y - 2], fill="white", outline=None)

    draw.polygon(
        [(head_x, head_y + 3), (head_x - 4, head_y + 10), (head_x + 4, head_y + 10)],
        fill="#FF8888",
        outline=None,
    )

    for offset in [-6, -2, 2, 6]:
        draw.line(
            [head_x - 15, head_y + 8 + offset, head_x - 30, head_y + 6 + offset],
            fill="#AAA",
            width=1,
        )
        draw.line(
            [head_x + 15, head_y + 8 + offset, head_x + 30, head_y + 6 + offset],
            fill="#AAA",
            width=1,
        )


def draw_full_cat_sleeping(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 200,
    view_height: int = 160,
) -> None:
    """Draw a sleeping curled cat."""
    cx, cy = view_width // 2, view_height // 2 + 10

    draw.ellipse([cx - 70, cy - 25, cx + 70, cy + 35], fill=main_color, outline=None)

    head_x, head_y = cx + 50, cy + 5

    for angle_offset, x_offset in [(-0.4, -15), (0.4, 15)]:
        ear_x = head_x + x_offset
        ear_points = [(ear_x - 8, head_y), (ear_x, head_y - 20), (ear_x + 8, head_y)]
        draw.polygon(ear_points, fill=main_color, outline=None)

    draw.ellipse(
        [head_x - 18, head_y - 18, head_x + 20, head_y + 18], fill=main_color, outline=None
    )

    draw.arc([head_x - 10, head_y - 3, head_x, head_y + 7], 0, 180, fill="#444", width=2)
    draw.arc([head_x + 2, head_y - 3, head_x + 12, head_y + 7], 0, 180, fill="#444", width=2)

    draw.polygon(
        [(head_x, head_y + 8), (head_x - 3, head_y + 13), (head_x + 3, head_y + 13)],
        fill="#FF8888",
        outline=None,
    )

    for i in range(8):
        t = i / 7
        x = cx - 65 - i * 6 + math.sin(t * math.pi) * 10
        y = cy + 15 + t * 15
        width = int(10 - t * 6)
        draw.ellipse(
            [x - width // 2, y - width // 2, x + width // 2, y + width // 2],
            fill=main_color,
            outline=None,
        )

    zzz_y = cy - 45 + int(math.sin(frame / total_frames * math.pi * 3) * 5)
    draw.text((cx + 55, zzz_y), "Z z z", fill="#666")


def draw_full_cat_eating(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 200,
    view_height: int = 160,
) -> None:
    """Draw a cat eating with visible mouth."""
    cx, cy = view_width // 2, view_height // 2 + 10

    bob = int(abs(math.sin(frame / total_frames * math.pi * 5)) * 10)
    body_x, body_y = cx, cy + bob

    tail_wag = math.sin(frame / total_frames * math.pi * 3) * 0.3
    tail_base_x, tail_base_y = body_x - 55, body_y - 10
    for i in range(8):
        t = i / 7
        angle = math.pi + tail_wag * t * math.pi
        x = tail_base_x - math.cos(angle) * 40 * t
        y = tail_base_y - math.sin(angle) * 15 * t
        width = int(10 - t * 6)
        draw.ellipse(
            [x - width // 2, y - width // 2, x + width // 2, y + width // 2],
            fill=main_color,
            outline=None,
        )

    draw.ellipse(
        [body_x - 50, body_y - 28, body_x + 50, body_y + 28], fill=main_color, outline=None
    )

    leg_width, leg_length = 12, 35
    for lx, ly in [
        (body_x + 20, body_y + 23),
        (body_x - 20, body_y + 23),
        (body_x + 35, body_y + 20),
        (body_x - 35, body_y + 20),
    ]:
        draw.ellipse(
            [lx - leg_width // 2, ly, lx + leg_width // 2, ly + leg_length],
            fill=main_color,
            outline=None,
        )

    head_x, head_y = body_x + 45, body_y - 25 + bob

    for angle_offset, x_offset in [(-0.3, -10), (0.3, 10)]:
        ear_x = head_x + x_offset
        ear_points = [(ear_x - 8, head_y - 5), (ear_x, head_y - 28), (ear_x + 8, head_y - 5)]
        draw.polygon(ear_points, fill=main_color, outline=None)
        draw.polygon(
            [(ear_x - 4, head_y - 5), (ear_x, head_y - 22), (ear_x + 4, head_y - 5)],
            fill="#FFB6C1",
            outline=None,
        )

    draw.ellipse(
        [head_x - 18, head_y - 18, head_x + 20, head_y + 18], fill=main_color, outline=None
    )

    draw.ellipse([head_x - 10, head_y - 8, head_x - 2, head_y + 2], fill="white", outline=None)
    draw.ellipse([head_x + 2, head_y - 8, head_x + 10, head_y + 2], fill="white", outline=None)
    draw.ellipse([head_x - 7, head_y - 5, head_x - 3, head_y - 1], fill="#222", outline=None)
    draw.ellipse([head_x + 5, head_y - 5, head_x + 9, head_y - 1], fill="#222", outline=None)

    mouth_open = int(abs(math.sin(frame / total_frames * math.pi * 8)) * 8)
    draw.ellipse(
        [head_x - 6, head_y + 5, head_x + 6, head_y + 12 + mouth_open], fill="#FF6666", outline=None
    )
    draw.ellipse([head_x - 4, head_y + 7, head_x - 1, head_y + 10], fill="#CC4444", outline=None)
    draw.ellipse([head_x + 1, head_y + 7, head_x + 4, head_y + 10], fill="#CC4444", outline=None)


def draw_full_cat_playing(
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    main_color: tuple,
    view_width: int = 200,
    view_height: int = 160,
) -> None:
    """Draw an excited playing cat."""
    cx, cy = view_width // 2, view_height // 2

    jump = int(abs(math.sin(frame / total_frames * math.pi * 3)) * 20)
    body_x, body_y = cx, cy + jump

    tail_up = math.sin(frame / total_frames * math.pi * 4) * 0.5
    tail_base_x, tail_base_y = body_x - 55, body_y - 30
    for i in range(10):
        t = i / 9
        angle = math.pi * 0.7 + tail_up * t * math.pi
        x = tail_base_x - math.cos(angle) * 50 * t
        y = tail_base_y - math.sin(angle) * 50 * t
        width = int(12 - t * 8)
        draw.ellipse(
            [x - width // 2, y - width // 2, x + width // 2, y + width // 2],
            fill=main_color,
            outline=None,
        )

    draw.ellipse(
        [body_x - 50, body_y - 30, body_x + 50, body_y + 30], fill=main_color, outline=None
    )

    leg_extend = int(abs(math.sin(frame / total_frames * math.pi * 6)) * 15)
    leg_width, leg_length = 12, 35
    for lx, ly, offset in [
        (body_x + 20, body_y + 25, leg_extend),
        (body_x - 20, body_y + 25, -leg_extend),
        (body_x + 35, body_y + 20, -leg_extend),
        (body_x - 35, body_y + 20, leg_extend),
    ]:
        draw.ellipse(
            [lx - leg_width // 2, ly + offset, lx + leg_width // 2, ly + leg_length + offset],
            fill=main_color,
            outline=None,
        )

    head_x, head_y = body_x + 45, body_y - 20

    for angle_offset, x_offset in [(-0.3, -10), (0.3, 10)]:
        ear_x = head_x + x_offset
        ear_points = [(ear_x - 8, head_y - 5), (ear_x, head_y - 30), (ear_x + 8, head_y - 5)]
        draw.polygon(ear_points, fill=main_color, outline=None)

    draw.ellipse(
        [head_x - 18, head_y - 18, head_x + 20, head_y + 18], fill=main_color, outline=None
    )

    draw.ellipse([head_x - 10, head_y - 10, head_x - 2, head_y], fill="white", outline=None)
    draw.ellipse([head_x + 2, head_y - 10, head_x + 10, head_y], fill="white", outline=None)
    draw.ellipse([head_x - 7, head_y - 7, head_x - 3, head_y - 3], fill="#222", outline=None)
    draw.ellipse([head_x + 5, head_y - 7, head_x + 9, head_y - 3], fill="#222", outline=None)

    draw.arc([head_x - 8, head_y + 2, head_x + 8, head_y + 12], 0, 180, fill="#555", width=2)


def draw_cat(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a cat based on behavior."""
    color_rgba = color if len(color) == 4 else (*color, 255)
    if is_sleeping:
        draw_full_cat_sleeping(draw, frame, total_frames, color_rgba, img.width, img.height)
    elif total_frames >= 16:
        if frame >= 12:
            draw_full_cat_eating(draw, frame, total_frames, color_rgba, img.width, img.height)
        elif frame >= 8:
            draw_full_cat_playing(draw, frame, total_frames, color_rgba, img.width, img.height)
        else:
            draw_full_cat_walking(draw, frame, total_frames, color_rgba, img.width, img.height)
    elif total_frames >= 8:
        draw_full_cat_idle(draw, frame, total_frames, color_rgba, img.width, img.height)


def draw_dog(
    img: Image.Image,
    draw: ImageDraw.ImageDraw,
    frame: int,
    total_frames: float,
    color: tuple,
    is_sleeping: bool = False,
) -> None:
    """Draw a dog based on behavior."""
    color_rgba = color if len(color) == 4 else (*color, 255)
    if is_sleeping:
        draw_full_cat_sleeping(draw, frame, total_frames, color_rgba, img.width, img.height)
    elif total_frames >= 16:
        if frame >= 12:
            draw_full_cat_eating(draw, frame, total_frames, color_rgba, img.width, img.height)
        elif frame >= 8:
            draw_full_cat_playing(draw, frame, total_frames, color_rgba, img.width, img.height)
        else:
            draw_full_cat_walking(draw, frame, total_frames, color_rgba, img.width, img.height)
    elif total_frames >= 8:
        draw_full_cat_idle(draw, frame, total_frames, color_rgba, img.width, img.height)


def create_pet_sprites(output_dir: Path, name: str, draw_func) -> None:
    """Create detailed full-body sprites for a pet type."""
    output_dir.mkdir(parents=True, exist_ok=True)

    view_width, view_height = 200, 160

    behaviors = {
        "idle": (16, False),
        "walk": (20, False),
        "sleep": (8, True),
        "eat": (16, False),
        "play": (16, False),
    }

    color_schemes = {
        "cat": {
            "idle": (255, 180, 120),
            "walk": (255, 180, 120),
            "sleep": (200, 190, 185),
            "eat": (255, 160, 100),
            "play": (255, 140, 80),
        },
        "dog": {
            "idle": (180, 140, 100),
            "walk": (180, 140, 100),
            "sleep": (170, 165, 160),
            "eat": (170, 130, 90),
            "play": (160, 110, 70),
        },
        "default": {
            "idle": (100, 160, 255),
            "walk": (100, 160, 255),
            "sleep": (150, 150, 180),
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

    icon_size = 32
    icon = Image.new("RGBA", (view_width, view_height), (0, 0, 0, 0))
    icon_draw = ImageDraw.Draw(icon)
    idle_color = colors["idle"] + (255,) if len(colors["idle"]) == 3 else colors["idle"]
    draw_func(icon, icon_draw, 0, 1, idle_color, False)
    icon = add_edge_feather(icon, radius=1)

    aspect = view_width / view_height
    if aspect > 1:
        new_w, new_h = icon_size, int(icon_size / aspect)
    else:
        new_w, new_h = int(icon_size * aspect), icon_size

    icon_resized = icon.resize((new_w, new_h), Image.Resampling.LANCZOS)
    icon_final = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    offset_x = (icon_size - new_w) // 2
    offset_y = (icon_size - new_h) // 2
    icon_final.paste(icon_resized, (offset_x, offset_y), icon_resized)
    icon_final.save(output_dir.parent / "icon.png")

    print(f"Created {name} detailed sprites in {output_dir}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"

    create_pet_sprites(base_dir / "cat", "cat", draw_cat)
    create_pet_sprites(base_dir / "dog", "dog", draw_dog)
    create_pet_sprites(base_dir / "default", "default", draw_cat)

    print("All detailed pet sprites generated!")

"""Generate a logo for the pet project."""

from pathlib import Path
from PIL import Image, ImageDraw


def create_logo(output_path: Path) -> None:
    """Create a simple and cute pet logo."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    orange = (255, 165, 79)
    dark_orange = (200, 130, 60)
    white = (255, 255, 255)
    black = (50, 50, 50)
    pink = (255, 180, 180)

    # Background circle (soft orange)
    cx, cy = size // 2, size // 2
    draw.ellipse([4, 4, 60, 60], fill=orange)

    # Body
    draw.ellipse([12, 25, 52, 55], fill=dark_orange)

    # Head
    draw.ellipse([18, 12, 46, 38], fill=orange)

    # Ears
    ear1 = [(20, 14), (26, 4), (32, 14)]
    ear2 = [(32, 14), (38, 4), (44, 14)]
    draw.polygon(ear1, fill=orange)
    draw.polygon(ear2, fill=orange)
    draw.polygon([(22, 14), (26, 8), (30, 14)], fill=pink)
    draw.polygon([(34, 14), (38, 8), (42, 14)], fill=pink)

    # Eyes
    draw.ellipse([22, 18, 30, 26], fill=white)
    draw.ellipse([34, 18, 42, 26], fill=white)
    draw.ellipse([24, 20, 28, 24], fill=black)
    draw.ellipse([36, 20, 40, 24], fill=black)
    draw.ellipse([25, 21, 27, 23], fill=white)
    draw.ellipse([37, 21, 39, 23], fill=white)

    # Nose
    draw.ellipse([28, 28, 36, 33], fill=pink)

    # Mouth
    draw.arc([26, 32, 38, 40], 0, 180, fill=black, width=1)

    # Feet
    draw.ellipse([14, 50, 22, 58], fill=dark_orange)
    draw.ellipse([42, 50, 50, 58], fill=dark_orange)

    img.save(output_path)
    print(f"Created logo at {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"
    create_logo(base_dir / "icon.png")

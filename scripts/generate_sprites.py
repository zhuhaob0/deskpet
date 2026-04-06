"""Generate placeholder sprites for testing."""

from pathlib import Path
from PIL import Image, ImageDraw


def create_placeholder_sprites(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    colors = {
        "idle": "blue",
        "walk": "green",
        "sleep": "purple",
        "eat": "orange",
        "play": "red",
    }

    for behavior, color in colors.items():
        for frame in range(4):
            img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            offset = frame * 2
            draw.ellipse(
                [20 + offset, 30, 108 - offset, 100],
                fill=color,
                outline="black",
                width=2,
            )
            draw.ellipse(
                [40 + offset, 50, 60 + offset, 70],
                fill="white",
                outline="black",
            )
            draw.ellipse(
                [68 + offset, 50, 88 - offset, 70],
                fill="white",
                outline="black",
            )
            draw.ellipse(
                [50 + offset, 60, 55 + offset, 65],
                fill="black",
            )
            draw.ellipse(
                [73, 60, 78, 65],
                fill="black",
            )

            filename = f"{behavior}_{frame:02d}.png"
            img.save(output_dir / filename)

    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    draw.ellipse([8, 12, 56, 52], fill="blue", outline="black", width=2)
    icon.save(output_dir.parent / "icon.png")

    print(f"Created sprites in {output_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        output = Path(sys.argv[1])
    else:
        output = Path(__file__).parent.parent / "resources" / "pets" / "default"
    create_placeholder_sprites(output)

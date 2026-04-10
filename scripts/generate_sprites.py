"""Generate placeholder sprites for testing."""

from pathlib import Path
from PIL import Image, ImageDraw


def create_placeholder_sprites(output_dir: Path, color: str, name: str) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    behaviors = {
        "idle": color,
        "walk": color,
        "sleep": "gray",
        "eat": color,
        "play": color,
    }

    for behavior, fill_color in behaviors.items():
        for frame in range(4):
            img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            offset = frame * 2
            draw.ellipse(
                [20 + offset, 30, 108 - offset, 100],
                fill=fill_color,
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

            if name == "dog":
                draw.polygon(
                    [(30 + offset, 25), (45 + offset, 40), (50 + offset, 30)],
                    fill=fill_color,
                    outline="black",
                )
                draw.polygon(
                    [(78 - offset, 25), (88 - offset, 40), (98 - offset, 30)],
                    fill=fill_color,
                    outline="black",
                )
            elif name == "cat":
                draw.polygon(
                    [(35 + offset, 25), (45 + offset, 40), (50 + offset, 20)],
                    fill=fill_color,
                    outline="black",
                )
                draw.polygon(
                    [(78 - offset, 20), (88 - offset, 40), (93 - offset, 25)],
                    fill=fill_color,
                    outline="black",
                )

            filename = f"{behavior}_{frame:02d}.png"
            img.save(output_dir / filename)

    icon = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    draw.ellipse([8, 12, 56, 52], fill=color, outline="black", width=2)
    icon.save(output_dir.parent / "icon.png")

    print(f"Created sprites in {output_dir}")


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent / "resources" / "pets"

    create_placeholder_sprites(base_dir / "cat", "orange", "cat")
    create_placeholder_sprites(base_dir / "dog", "brown", "dog")
    create_placeholder_sprites(base_dir / "default", "blue", "default")

    print("All pet sprites generated!")

"""Sprite importer for GIF and video files."""

from __future__ import annotations

import logging
from pathlib import Path

import cv2
from PIL import Image

logger = logging.getLogger(__name__)


class SpriteImporter:
    TARGET_FPS = 30
    CROP_MARGIN = 2

    def __init__(self, resource_dir: Path):
        self.resource_dir = resource_dir

    def import_from_file(
        self,
        file_path: str,
        pet_name: str,
        action_name: str,
    ) -> tuple[bool, str]:
        path = Path(file_path)
        if not path.exists():
            return False, f"File not found: {file_path}"

        suffix = path.suffix.lower()
        if suffix == ".gif":
            return self._import_gif(path, pet_name, action_name)
        elif suffix in (".mp4", ".avi", ".mkv", ".mov", ".wmv"):
            return self._import_video(path, pet_name, action_name)
        else:
            return False, f"Unsupported file format: {suffix}. Use GIF or MP4."

    def _import_gif(self, gif_path: Path, pet_name: str, action_name: str) -> tuple[bool, str]:
        try:
            output_dir = self._prepare_output_dir(pet_name, action_name)

            with Image.open(gif_path) as gif:
                total_frames = getattr(gif, "n_frames", 1)
                duration_ms = gif.info.get("duration", 100)
                original_fps = 1000 / duration_ms if duration_ms > 0 else 10

                frame_interval = max(1, round(original_fps / self.TARGET_FPS))

                saved_count = 0
                for frame_idx in range(0, total_frames, frame_interval):
                    gif.seek(frame_idx)

                    frame_rgba = gif.convert("RGBA")
                    frame_cropped = self._crop_transparency(frame_rgba)
                    frame_path = output_dir / f"{action_name}_{saved_count:02d}.png"
                    frame_cropped.save(frame_path, "PNG")
                    saved_count += 1

                    logger.info(f"Extracted frame {saved_count}: {frame_path.name}")

            return True, f"Imported {saved_count} frames to {output_dir}"

        except Exception as e:
            logger.error(f"Failed to import GIF: {e}")
            return False, f"Failed to import GIF: {e}"

    def _import_video(self, video_path: Path, pet_name: str, action_name: str) -> tuple[bool, str]:
        try:
            output_dir = self._prepare_output_dir(pet_name, action_name)

            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                return False, f"Cannot open video: {video_path}"

            original_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = max(1, round(original_fps / self.TARGET_FPS))

            saved_count = 0
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_idx % frame_interval == 0:
                    frame_rgba = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    frame_pil = Image.fromarray(frame_rgba)
                    frame_cropped = self._crop_transparency(frame_pil)
                    frame_path = output_dir / f"{action_name}_{saved_count:02d}.png"
                    frame_cropped.save(frame_path, "PNG")
                    saved_count += 1

                    logger.info(f"Extracted frame {saved_count}: {frame_path.name}")

                frame_idx += 1

            cap.release()

            return True, f"Imported {saved_count} frames to {output_dir}"

        except Exception as e:
            logger.error(f"Failed to import video: {e}")
            return False, f"Failed to import video: {e}"

    def _crop_transparency(self, image: Image.Image) -> Image.Image:
        bbox = image.getbbox()
        if bbox is None:
            return image

        left, top, right, bottom = bbox
        margin = self.CROP_MARGIN
        left = max(0, left - margin)
        top = max(0, top - margin)
        right = min(image.width, right + margin)
        bottom = min(image.height, bottom + margin)

        return image.crop((left, top, right, bottom))

    def _prepare_output_dir(self, pet_name: str, action_name: str) -> Path:
        pet_name = pet_name.lower().strip().replace(" ", "_")
        action_name = action_name.lower().strip().replace(" ", "_")

        output_dir = self.resource_dir / pet_name / action_name
        output_dir.mkdir(parents=True, exist_ok=True)

        for f in output_dir.glob(f"{action_name}_*.png"):
            f.unlink()

        return output_dir

    def get_available_pets(self) -> list[str]:
        if not self.resource_dir.exists():
            return []
        return [d.name for d in self.resource_dir.iterdir() if d.is_dir() and d.name != "icon.png"]

    def get_available_actions(self, pet_name: str) -> list[str]:
        pet_dir = self.resource_dir / pet_name
        if not pet_dir.exists():
            return []
        return [d.name for d in pet_dir.iterdir() if d.is_dir()]

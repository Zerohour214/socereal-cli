"""Utilities for locating image files on disk."""

from pathlib import Path
from typing import Iterable, List

SUPPORTED_EXTENSIONS = (".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".gif")

def is_image_file(filename: str) -> bool:
    """Return ``True`` if ``filename`` has a supported image extension."""
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)

def collect_image_files(inputs: Iterable[str]) -> List[str]:
    """Collect all image file paths from given directories or files.

    This function accepts any iterable of input paths and handles Windows or
    POSIX-style paths transparently using :class:`pathlib.Path`.
    """

    image_files: List[str] = []
    for raw_path in inputs:
        p = Path(raw_path).expanduser()
        if p.is_dir():
            for child in p.iterdir():
                if child.is_file() and is_image_file(child.name):
                    image_files.append(str(child))
        elif p.is_file() and is_image_file(p.name):
            image_files.append(str(p))
        else:
            from logging import warning

            warning(f"Skipping unsupported input: {raw_path}")

    return image_files

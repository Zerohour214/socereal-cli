"""Utilities for locating image files on disk."""
import os
from typing import List

SUPPORTED_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.gif')

def is_image_file(filename: str) -> bool:
    """Return True if the filename has a supported image extension."""
    return filename.lower().endswith(SUPPORTED_EXTENSIONS)

def collect_image_files(inputs: List[str]) -> List[str]:
    """Collect all image file paths from given directories or files."""
    image_files = []
    for input_path in inputs:
        if os.path.isdir(input_path):
            for fname in os.listdir(input_path):
                fpath = os.path.join(input_path, fname)
                if os.path.isfile(fpath) and is_image_file(fname):
                    image_files.append(fpath)
        elif os.path.isfile(input_path) and is_image_file(input_path):
            image_files.append(input_path)
        else:
            from logging import warning
            warning(f"Skipping unsupported input: {input_path}")
    return image_files

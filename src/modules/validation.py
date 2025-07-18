import re
import logging
from typing import Optional

# List of characters/symbols considered "weird" (customize as needed)

SAFE_KEYBOARD_PATTERN = re.compile(
    r"[^a-zA-Z0-9 \t\n~!@#$%^&*()_+\-=\[\]{}\\|;:'\",.<>/?`]"
)

  # allow most printable

def has_abnormal_characters(text: str) -> bool:
    """Returns True if text contains any abnormal characters."""
    return bool(SAFE_KEYBOARD_PATTERN.search(text))

def find_abnormal_characters(text: str) -> str:
    """Returns a string of all unique abnormal characters found in the text."""
    return "".join(sorted(set(SAFE_KEYBOARD_PATTERN.findall(text))))

def validate_text(text: str) -> Optional[str]:
    """Validate OCR text. Returns a message if issues found, else None."""
    if not text or text.strip() == "":
        return "Empty or whitespace-only OCR result"
    if has_abnormal_characters(text):
        weirds = find_abnormal_characters(text)
        return f"Abnormal characters detected: {weirds}"
    return None

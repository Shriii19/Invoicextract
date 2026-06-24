"""
Miscellaneous helper utilities
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional


def clean_amount(value: str) -> Optional[float]:
    """Parse a currency string like '$1,234.56' into a float."""
    if not value:
        return None
    cleaned = re.sub(r"[^\d.]", "", value)
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_whitespace(text: str) -> str:
    """Collapse multiple spaces/tabs into a single space, strip lines."""
    lines = [" ".join(line.split()) for line in text.splitlines()]
    return "\n".join(lines)


def find_files(directory: Path, extensions: list[str]) -> list[Path]:
    """Return all files in *directory* (non-recursive) matching *extensions*."""
    directory = Path(directory)
    return [f for f in directory.iterdir() if f.is_file() and f.suffix.lower() in extensions]


def safe_filename(name: str) -> str:
    """Strip characters that are illegal in filenames."""
    return re.sub(r'[<>:"/\\|?*]', "_", name)

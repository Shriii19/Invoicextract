"""
PDF utility functions — page count, metadata, thumbnail generation
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def get_page_count(pdf_path: Path) -> int:
    """Return the number of pages in a PDF."""
    try:
        import fitz

        with fitz.open(str(pdf_path)) as doc:
            return len(doc)
    except Exception as e:
        logger.warning(f"Could not read page count for {pdf_path.name}: {e}")
        return 0


def get_pdf_metadata(pdf_path: Path) -> dict:
    """Return the PDF metadata dict (author, title, creator, etc.)."""
    try:
        import fitz

        with fitz.open(str(pdf_path)) as doc:
            return doc.metadata or {}
    except Exception as e:
        logger.warning(f"Could not read metadata for {pdf_path.name}: {e}")
        return {}


def is_scanned_pdf(pdf_path: Path, sample_pages: int = 3) -> bool:
    """
    Return True if the PDF appears to contain only images (scanned).
    Heuristic: fewer than 20 characters of selectable text per page.
    """
    try:
        import fitz

        with fitz.open(str(pdf_path)) as doc:
            pages = list(doc)[:sample_pages]
            total_chars = sum(len(p.get_text()) for p in pages)
            return total_chars < 20 * len(pages)
    except Exception as e:
        logger.warning(f"Could not determine if {pdf_path.name} is scanned: {e}")
        return False


def render_page_to_image(pdf_path: Path, page_number: int = 0, dpi: int = 150) -> Optional[bytes]:
    """Render a single PDF page to PNG bytes."""
    try:
        import fitz

        with fitz.open(str(pdf_path)) as doc:
            page = doc[page_number]
            mat = fitz.Matrix(dpi / 72, dpi / 72)
            pix = page.get_pixmap(matrix=mat)
            return pix.tobytes("png")
    except Exception as e:
        logger.error(f"Could not render page {page_number} of {pdf_path.name}: {e}")
        return None

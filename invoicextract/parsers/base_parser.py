"""
Abstract base class for all invoice parsers
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from invoicextract.models.invoice import Invoice


class BaseParser(ABC):
    """All parsers must implement parse(); can_parse() enables auto-selection."""

    @abstractmethod
    def parse(self, text: str, source_file: Optional[Path] = None) -> Invoice:
        """Parse raw text into an Invoice object."""
        ...

    def can_parse(self, text: str) -> bool:
        """Return True if this parser recognises the invoice format."""
        return True

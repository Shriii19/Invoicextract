"""
Abstract base class for all exporters
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Union

from invoicextract.models.invoice import Invoice


class BaseExporter(ABC):
    """All exporters must implement export()."""

    @abstractmethod
    def export(self, invoices: List[Invoice], output_path: Union[str, Path]) -> None:
        """Write invoices to the given output path."""
        ...

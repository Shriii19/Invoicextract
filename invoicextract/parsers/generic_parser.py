"""
Generic invoice parser using regex and pattern matching
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from invoicextract.models.invoice import Invoice, LineItem

logger = logging.getLogger(__name__)


class GenericParser:
    """
    Parses invoice text using generic patterns and heuristics
    """

    # Regex patterns for common invoice fields
    PATTERNS = {
        "invoice_number": [
            r"invoice[^\S\n]*#?[^\S\n]*:?[^\S\n]*([^\s]+)",
            r"inv[^\S\n]*#?[^\S\n]*:?[^\S\n]*([^\s]+)",
            r"invoice[^\S\n]+number[^\S\n]*:?[^\S\n]*([^\s]+)",
        ],
        "date": [
            r"invoice\s+date\s*:?\s*(\d{4}-\d{2}-\d{2})",
            r"date\s*:?\s*(\d{4}-\d{2}-\d{2})",
            r"(\d{1,2}/\d{1,2}/\d{4})",
        ],
        "total": [
            r"\btotal\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"amount\s+due\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"grand\s+total\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "subtotal": [
            r"subtotal\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"sub\s+total\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "tax": [
            r"tax\s*(?:\([^)]+\))?\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"sales\s+tax\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "currency": [
            r"(USD|EUR|GBP|CAD|AUD)\b",
            r"\$\s*[\d,]+\.?\d*\s+(USD|EUR|GBP)",
        ],
    }

    def __init__(self):
        logger.debug("GenericParser initialized")

    def parse(self, text: str, source_file: Optional[Path] = None) -> Invoice:
        """
        Parse invoice text into structured data

        Args:
            text: Raw text extracted from invoice
            source_file: Optional source file path

        Returns:
            Invoice object with extracted data
        """
        logger.debug("Starting generic parsing")

        # Normalize text
        text_lower = text.lower()

        # Extract fields using patterns
        invoice = Invoice(
            invoice_number=self._extract_field(text_lower, "invoice_number"),
            invoice_date=self._extract_date(text_lower),
            vendor_name=self._extract_vendor(text),
            total_amount=self._extract_amount(text_lower, "total"),
            subtotal=self._extract_amount(text_lower, "subtotal"),
            tax_amount=self._extract_amount(text_lower, "tax"),
            currency=self._extract_field(text_lower, "currency") or "USD",
            line_items=self._extract_line_items(text),
            raw_text=text[:500],  # Store first 500 chars
            source_file=str(source_file) if source_file else None,
        )

        logger.debug(f"Parsed invoice: {invoice.invoice_number}")
        return invoice

    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a field using regex patterns"""
        patterns = self.PATTERNS.get(field_name, [])

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                logger.debug(f"Extracted {field_name}: {value}")
                return value

        logger.debug(f"Could not extract {field_name}")
        return None

    def _extract_amount(self, text: str, field_name: str) -> Optional[float]:
        """Extract monetary amount"""
        value_str = self._extract_field(text, field_name)
        if not value_str:
            return None

        try:
            # Remove commas and convert to float
            amount = float(value_str.replace(",", ""))
            return amount
        except ValueError:
            logger.warning(f"Could not parse amount: {value_str}")
            return None

    def _extract_date(self, text: str) -> Optional[str]:
        """Extract and normalize date"""
        date_str = self._extract_field(text, "date")
        if not date_str:
            return None

        # Try to parse and normalize to ISO format
        date_formats = ["%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"]

        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # Return as-is if parsing failed
        return date_str

    def _extract_vendor(self, text: str) -> Optional[str]:
        """Extract vendor name (simple heuristic)"""
        # Look for "Vendor:" or company name patterns
        patterns = [
            r"vendor\s*:?\s*([^\n]+)",
            r"from\s*:?\s*([^\n]+)",
        ]

        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                # Get the original cased version
                start, end = match.span(1)
                # Find position in original text
                lines = text.split("\n")
                for line in lines:
                    if "vendor" in line.lower() or "from" in line.lower():
                        vendor = re.sub(r"vendor\s*:?\s*", "", line, flags=re.IGNORECASE)
                        vendor = re.sub(r"from\s*:?\s*", "", vendor, flags=re.IGNORECASE)
                        return vendor.strip()

        # Fallback: first line often contains vendor name
        first_line = text.split("\n")[0].strip()
        if first_line and len(first_line) > 3:
            return first_line

        return None

    def _extract_line_items(self, text: str) -> list[LineItem]:
        """Extract line items (placeholder implementation)"""
        # TODO: Implement proper line item extraction
        # For now, return empty list
        return []

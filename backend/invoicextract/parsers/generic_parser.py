"""
Generic invoice parser using regex and pattern matching
"""

from __future__ import annotations

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from invoicextract.models.invoice import Invoice, LineItem

logger = logging.getLogger(__name__)


class GenericParser:
    """
    Parses invoice text using generic patterns and heuristics.
    Works on any text-based invoice without vendor-specific templates.
    """

    PATTERNS: dict[str, list[str]] = {
        "invoice_number": [
            r"invoice\s+number\s*:?\s*([A-Z0-9][\w\-/]{2,20})",
            r"invoice\s+no\.?\s*:?\s*([A-Z0-9][\w\-/]{2,20})",
            r"invoice\s*[#:]\s*([A-Z0-9][\w\-/]{2,20})",
            r"inv\s*[#:]\s*([A-Z0-9][\w\-/]{2,20})",
            r"inv\s+no\.?\s*:?\s*([A-Z0-9][\w\-/]{2,20})",
            r"\b(inv[-/]\d[\w\-/]{1,15})\b",
        ],
        "date": [
            r"invoice\s+date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            r"invoice\s+date\s*:?\s*(\d{4}-\d{2}-\d{2})",
            r"(?<!\w)date\s*:?\s*(\d{4}-\d{2}-\d{2})",
            r"(?<!\w)date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            r"(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\.?\s+\d{4})",
        ],
        "due_date": [
            r"due\s+date\s*:?\s*(\d{4}-\d{2}-\d{2})",
            r"due\s+date\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
            r"payment\s+due\s*:?\s*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})",
        ],
        "total": [
            r"\btotal\s*(?:due|amount)?\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"grand\s+total\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"\bamount\s+due\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"\bbalance\s+due\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "subtotal": [
            r"sub[\s\-]?total\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "tax": [
            r"tax\s*(?:\([^)]*\))?\s*:?\s*\$?\s*([\d,]+\.?\d*)",
            r"(?:sales\s+tax|vat|gst)\s*(?:\d+%?)?\s*:?\s*\$?\s*([\d,]+\.?\d*)",
        ],
        "currency": [
            r"\b(USD|EUR|GBP|CAD|AUD|INR|JPY|CNY|CHF|SGD)\b",
        ],
        "payment_terms": [
            r"payment\s+terms?\s*:?\s*([^\n]{3,40})",
            r"terms?\s*:?\s*(net\s*\d+[^\n]{0,20})",
        ],
        "vendor_email": [
            r"([a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})",
        ],
        "vendor_phone": [
            r"(?:phone|tel|ph|mobile|fax)\s*[:\.]?\s*([\+\d][\d\s\-\(\)\.]{6,20})",
        ],
    }

    DATE_FORMATS = [
        "%Y-%m-%d",
        "%m/%d/%Y", "%d/%m/%Y",
        "%m-%d-%Y", "%d-%m-%Y",
        "%d.%m.%Y", "%m.%d.%Y",
        "%d %B %Y", "%d %b %Y",
        "%B %d, %Y", "%b %d, %Y",
        "%d %b. %Y",
    ]

    def __init__(self):
        logger.debug("GenericParser initialized")

    def parse(self, text: str, source_file: Optional[Path] = None) -> Invoice:
        logger.debug("Starting generic parsing")
        text_lower = text.lower()

        invoice = Invoice(
            invoice_number=self._extract_field(text, "invoice_number"),
            invoice_date=self._extract_date(text_lower, "date"),
            due_date=self._extract_date(text_lower, "due_date"),
            vendor_name=self._extract_vendor_name(text),
            vendor_address=self._extract_address_block(text, ["from", "vendor", "seller", "bill from"]),
            vendor_email=self._extract_field(text, "vendor_email"),
            vendor_phone=self._extract_field(text_lower, "vendor_phone"),
            customer_name=self._extract_customer_name(text),
            customer_address=self._extract_address_block(text, ["bill to", "ship to", "sold to"]),
            total_amount=self._extract_amount(text_lower, "total"),
            subtotal=self._extract_amount(text_lower, "subtotal"),
            tax_amount=self._extract_amount(text_lower, "tax"),
            currency=(self._extract_field(text, "currency") or "USD").upper(),
            payment_terms=self._extract_field(text, "payment_terms"),
            line_items=self._extract_line_items(text),
            raw_text=text[:500],
            source_file=str(source_file) if source_file else None,
        )

        logger.debug(f"Parsed invoice: {invoice.invoice_number}")
        return invoice

    # ------------------------------------------------------------------
    # Field extractors
    # ------------------------------------------------------------------

    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        for pattern in self.PATTERNS.get(field_name, []):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                logger.debug(f"Extracted {field_name}: {value}")
                return value
        return None

    def _extract_amount(self, text: str, field_name: str) -> Optional[float]:
        value_str = self._extract_field(text, field_name)
        if not value_str:
            return None
        try:
            return float(value_str.replace(",", ""))
        except ValueError:
            logger.warning(f"Could not parse amount: {value_str}")
            return None

    def _extract_date(self, text: str, field_name: str = "date") -> Optional[str]:
        date_str = self._extract_field(text, field_name)
        if not date_str:
            return None
        for fmt in self.DATE_FORMATS:
            try:
                return datetime.strptime(date_str.strip(), fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str

    def _extract_vendor_name(self, text: str) -> Optional[str]:
        patterns = [
            r"(?:from|vendor|seller|company|billed?\s+from)\s*:?\s*([^\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        # Fallback: first substantive line (not the word "INVOICE")
        for line in text.split("\n"):
            line = line.strip()
            if line and len(line) > 3 and not re.match(r"^invoice$", line, re.IGNORECASE):
                return line
        return None

    def _extract_customer_name(self, text: str) -> Optional[str]:
        patterns = [
            r"(?:bill\s+to|ship\s+to|sold\s+to|customer|client)\s*:?\s*([^\n]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if name and not name[0].isdigit():
                    return name
        return None

    def _extract_address_block(self, text: str, keywords: list[str]) -> Optional[str]:
        """Return up to 4 lines following a keyword as an address block."""
        for keyword in keywords:
            pattern = rf"(?:^|\n)\s*{re.escape(keyword)}\s*:?\s*\n?((?:[^\n]+\n?){{1,4}})"
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                lines = [l.strip() for l in match.group(1).split("\n") if l.strip()]
                return "\n".join(lines[:4])
        return None

    # ------------------------------------------------------------------
    # Line item extraction
    # ------------------------------------------------------------------

    def _extract_line_items(self, text: str) -> list[LineItem]:
        items = []

        # Isolate the items section (between the items header and the totals)
        section_text = self._isolate_items_section(text)

        # Try numbered list format:  "1. Product A - $100.00"
        items = self._parse_numbered_items(section_text)
        if items:
            return items

        # Try table format:  "Description   2   50.00   100.00"
        items = self._parse_table_items(section_text)
        if items:
            return items

        # Try inline format: "Product A .......... $100.00"
        items = self._parse_dotleader_items(section_text)
        return items

    def _isolate_items_section(self, text: str) -> str:
        header = re.search(
            r'\b(?:items?|description|services?|products?|details?)\b[^\n]*\n',
            text, re.IGNORECASE
        )
        start = header.end() if header else 0

        footer = re.search(
            r'\n\s*(?:sub[\s\-]?total|total)\s*[:\$]',
            text[start:], re.IGNORECASE
        )
        end = start + footer.start() if footer else len(text)
        return text[start:end]

    def _parse_numbered_items(self, section: str) -> list[LineItem]:
        """Matches:  1. Description - $100.00"""
        items = []
        pattern = re.compile(
            r'^\s*\d+[.)]\s+(.+?)\s*[-–]\s*\$?([\d,]+\.?\d*)\s*$',
            re.MULTILINE
        )
        for m in pattern.finditer(section):
            try:
                items.append(LineItem(
                    description=m.group(1).strip(),
                    amount=float(m.group(2).replace(",", "")),
                ))
            except ValueError:
                continue
        return items

    def _parse_table_items(self, section: str) -> list[LineItem]:
        """Matches table rows with 2-4 whitespace-separated columns."""
        items = []
        skip_words = {"description", "item", "service", "qty", "amount", "price", "total", "unit"}
        pattern = re.compile(
            r'^([A-Za-z][^\t\n$]{3,50}?)\s{2,}(\d+\.?\d*)?\s*\$?([\d,]+\.?\d*)\s+\$?([\d,]+\.?\d*)\s*$',
            re.MULTILINE
        )
        for m in pattern.finditer(section):
            description = m.group(1).strip()
            if any(w in description.lower() for w in skip_words):
                continue
            try:
                qty = float(m.group(2)) if m.group(2) else 1.0
                unit_price = float(m.group(3).replace(",", "")) if m.group(3) else None
                amount = float(m.group(4).replace(",", "")) if m.group(4) else None
                if description and amount:
                    items.append(LineItem(description=description, quantity=qty,
                                          unit_price=unit_price, amount=amount))
            except (ValueError, AttributeError):
                continue
        return items

    def _parse_dotleader_items(self, section: str) -> list[LineItem]:
        """Matches:  Product A ........ $100.00"""
        items = []
        pattern = re.compile(
            r'^([A-Za-z][^\n$]{3,50}?)\s*[.\s]{3,}\s*\$?([\d,]+\.?\d*)\s*$',
            re.MULTILINE
        )
        for m in pattern.finditer(section):
            try:
                items.append(LineItem(
                    description=m.group(1).strip(),
                    amount=float(m.group(2).replace(",", "")),
                ))
            except ValueError:
                continue
        return items

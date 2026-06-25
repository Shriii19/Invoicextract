"""
Validator for invoice data quality and completeness
"""

import logging
from dataclasses import dataclass
from typing import List

from invoicextract.models.invoice import Invoice

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of invoice validation"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]


class InvoiceValidator:
    """
    Validates extracted invoice data for completeness and accuracy
    """

    def __init__(self, strict: bool = False):
        """
        Initialize validator

        Args:
            strict: If True, warnings are treated as errors
        """
        self.strict = strict
        logger.debug(f"Validator initialized (strict={strict})")

    def validate(self, invoice: Invoice) -> ValidationResult:
        """
        Validate an invoice object

        Args:
            invoice: Invoice to validate

        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []

        # Required fields
        if not invoice.invoice_number:
            errors.append("Missing invoice number")

        if not invoice.vendor_name:
            errors.append("Missing vendor name")

        if invoice.total_amount is None:
            errors.append("Missing total amount")
        elif invoice.total_amount < 0:
            errors.append("Total amount cannot be negative")

        # Optional but recommended fields
        if not invoice.invoice_date:
            warnings.append("Missing invoice date")

        if not invoice.currency:
            warnings.append("Missing currency information")

        if not invoice.line_items or len(invoice.line_items) == 0:
            warnings.append("No line items found")

        # Business logic validations
        if invoice.subtotal and invoice.total_amount:
            if invoice.subtotal > invoice.total_amount:
                errors.append("Subtotal cannot exceed total amount")

        if invoice.tax_amount and invoice.tax_amount < 0:
            errors.append("Tax amount cannot be negative")

        # Determine validity
        all_issues = errors + (warnings if self.strict else [])
        is_valid = len(all_issues) == 0

        if errors:
            logger.warning(
                f"Validation failed for invoice {invoice.invoice_number}: {len(errors)} error(s)"
            )

        return ValidationResult(is_valid=is_valid, errors=errors, warnings=warnings)

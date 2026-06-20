"""
Unit tests for InvoiceXtract

Run with: pytest tests/
"""

from pathlib import Path

import pytest

from invoicextract.core.validator import InvoiceValidator, ValidationResult
from invoicextract.models.invoice import Invoice, LineItem
from invoicextract.parsers.generic_parser import GenericParser


class TestInvoiceModel:
    """Tests for Invoice data model"""

    def test_invoice_creation(self):
        """Test basic invoice creation"""
        invoice = Invoice(invoice_number="INV-001", vendor_name="Test Vendor", total_amount=100.00)

        assert invoice.invoice_number == "INV-001"
        assert invoice.vendor_name == "Test Vendor"
        assert invoice.total_amount == 100.00
        assert invoice.currency == "USD"

    def test_line_item_calculation(self):
        """Test line item amount calculation"""
        item = LineItem(description="Product A", quantity=2.0, unit_price=50.0)

        assert item.amount == 100.0

    def test_invoice_to_dict(self):
        """Test invoice dictionary conversion"""
        invoice = Invoice(invoice_number="INV-002", vendor_name="Vendor Inc", total_amount=250.00)

        data = invoice.to_dict()
        assert isinstance(data, dict)
        assert data["invoice_number"] == "INV-002"
        assert data["total_amount"] == 250.00


class TestValidator:
    """Tests for InvoiceValidator"""

    def test_valid_invoice(self):
        """Test validation of a valid invoice"""
        validator = InvoiceValidator()
        invoice = Invoice(
            invoice_number="INV-003",
            vendor_name="Valid Vendor",
            total_amount=100.00,
            invoice_date="2024-06-17",
            currency="USD",
        )

        result = validator.validate(invoice)
        assert result.is_valid
        assert len(result.errors) == 0

    def test_invalid_invoice_missing_required(self):
        """Test validation fails for missing required fields"""
        validator = InvoiceValidator()
        invoice = Invoice(
            invoice_number=None,  # Missing required field
            vendor_name="Vendor",
            total_amount=100.00,
        )

        result = validator.validate(invoice)
        assert not result.is_valid
        assert "Missing invoice number" in result.errors

    def test_negative_amount_validation(self):
        """Test validation catches negative amounts"""
        validator = InvoiceValidator()
        invoice = Invoice(
            invoice_number="INV-004",
            vendor_name="Vendor",
            total_amount=-50.00,  # Invalid negative amount
        )

        result = validator.validate(invoice)
        assert not result.is_valid
        assert any("negative" in error.lower() for error in result.errors)


class TestGenericParser:
    """Tests for GenericParser"""

    def test_parse_invoice_number(self):
        """Test parsing invoice number from text"""
        parser = GenericParser()
        text = """
        INVOICE
        Invoice #: INV-2024-001
        Total: $100.00
        """

        invoice = parser.parse(text)
        assert invoice.invoice_number == "inv-2024-001"

    def test_parse_amount(self):
        """Test parsing amounts from text"""
        parser = GenericParser()
        text = """
        Subtotal: $350.00
        Tax: $35.00
        Total: $385.00
        """

        invoice = parser.parse(text)
        assert invoice.total_amount == 385.00
        assert invoice.subtotal == 350.00
        assert invoice.tax_amount == 35.00

    def test_parse_with_commas(self):
        """Test parsing amounts with comma separators"""
        parser = GenericParser()
        text = "Total: $1,234.56"

        invoice = parser.parse(text)
        assert invoice.total_amount == 1234.56


# Fixtures
@pytest.fixture
def sample_invoice():
    """Fixture providing a sample invoice"""
    return Invoice(
        invoice_number="INV-SAMPLE-001",
        vendor_name="Sample Vendor Ltd",
        customer_name="Sample Customer Inc",
        invoice_date="2024-06-17",
        subtotal=500.00,
        tax_amount=50.00,
        total_amount=550.00,
        currency="USD",
        payment_terms="Net 30",
    )


@pytest.fixture
def sample_text():
    """Fixture providing sample invoice text"""
    return """
    INVOICE
    
    Invoice Number: INV-2024-999
    Date: 2024-06-17
    
    Vendor: Acme Corporation
    Total: $1,000.00 USD
    """


def test_with_fixture(sample_invoice):
    """Test using the sample invoice fixture"""
    assert sample_invoice.invoice_number == "INV-SAMPLE-001"
    assert sample_invoice.total_amount == 550.00

"""
Basic usage example for InvoiceXtract

This example demonstrates how to:
1. Extract data from a single invoice
2. Validate the extracted data
3. Export to different formats
"""

from pathlib import Path

from invoicextract import InvoiceExtractor
from invoicextract.exporters.csv_exporter import CSVExporter
from invoicextract.exporters.json_exporter import JSONExporter
from invoicextract.exporters.excel_exporter import ExcelExporter


def main():
    """Main example function"""
    
    print("=" * 60)
    print("InvoiceXtract - Basic Usage Example")
    print("=" * 60)
    
    # Initialize the extractor
    print("\n[1] Initializing InvoiceExtractor...")
    extractor = InvoiceExtractor()
    
    # Example 1: Extract from a single file (mock demonstration)
    print("\n[2] Extracting invoice data...")
    print("    Note: This example uses mock data for demonstration.")
    print("    In production, provide a real PDF path.")
    
    # Create a mock invoice for demonstration
    from invoicextract.models.invoice import Invoice, LineItem
    
    invoice = Invoice(
        invoice_number="INV-2024-001",
        vendor_name="Acme Corporation",
        customer_name="John Doe",
        invoice_date="2024-06-17",
        due_date="2024-07-17",
        subtotal=350.00,
        tax_amount=35.00,
        total_amount=385.00,
        currency="USD",
        payment_terms="Net 30",
        line_items=[
            LineItem(description="Product A", quantity=1, unit_price=100.00),
            LineItem(description="Product B", quantity=2, unit_price=125.00)
        ]
    )
    
    # Display extracted data
    print(f"\n    ✓ Extracted: {invoice}")
    print(f"      Vendor: {invoice.vendor_name}")
    print(f"      Total: {invoice.total_amount} {invoice.currency}")
    print(f"      Line Items: {len(invoice.line_items)}")
    print(f"      Valid: {'Yes' if invoice.is_valid else 'No'}")
    
    # Example 2: Export to CSV
    print("\n[3] Exporting to CSV...")
    csv_exporter = CSVExporter()
    csv_output = Path("output/invoices.csv")
    csv_exporter.export([invoice], csv_output)
    print(f"    ✓ Saved to: {csv_output}")
    
    # Example 3: Export to JSON
    print("\n[4] Exporting to JSON...")
    json_exporter = JSONExporter()
    json_output = Path("output/invoices.json")
    json_exporter.export([invoice], json_output, pretty=True)
    print(f"    ✓ Saved to: {json_output}")
    
    # Example 4: Export to Excel (if openpyxl is installed)
    print("\n[5] Exporting to Excel...")
    try:
        excel_exporter = ExcelExporter()
        excel_output = Path("output/invoices.xlsx")
        excel_exporter.export([invoice], excel_output)
        print(f"    ✓ Saved to: {excel_output}")
    except ImportError:
        print("    ⚠ Skipped: openpyxl not installed")
        print("      Install with: pip install openpyxl")
    
    print("\n" + "=" * 60)
    print("Example complete!")
    print("=" * 60)
    
    # Real usage example (commented out)
    print("\n# To extract from a real PDF file:")
    print("# invoice = extractor.extract('path/to/invoice.pdf')")
    print("# csv_exporter.export([invoice], 'output/results.csv')")


if __name__ == "__main__":
    main()

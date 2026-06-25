"""
CSV exporter for invoice data
"""

import csv
import logging
from pathlib import Path
from typing import List, Union

from invoicextract.models.invoice import Invoice

logger = logging.getLogger(__name__)


class CSVExporter:
    """
    Exports invoice data to CSV format
    """

    FIELDNAMES = [
        "invoice_number",
        "vendor_name",
        "customer_name",
        "invoice_date",
        "due_date",
        "subtotal",
        "tax_amount",
        "total_amount",
        "currency",
        "payment_terms",
        "is_valid",
        "source_file",
        "extracted_at",
    ]

    def export(
        self,
        invoices: List[Invoice],
        output_path: Union[str, Path],
        include_line_items: bool = False,
    ):
        """
        Export invoices to CSV file

        Args:
            invoices: List of Invoice objects to export
            output_path: Path to output CSV file
            include_line_items: If True, export line items separately
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Exporting {len(invoices)} invoices to CSV: {output_path}")

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.FIELDNAMES)
            writer.writeheader()

            for invoice in invoices:
                row = {
                    "invoice_number": invoice.invoice_number,
                    "vendor_name": invoice.vendor_name,
                    "customer_name": invoice.customer_name,
                    "invoice_date": invoice.invoice_date,
                    "due_date": invoice.due_date,
                    "subtotal": invoice.subtotal,
                    "tax_amount": invoice.tax_amount,
                    "total_amount": invoice.total_amount,
                    "currency": invoice.currency,
                    "payment_terms": invoice.payment_terms,
                    "is_valid": invoice.is_valid,
                    "source_file": invoice.source_file,
                    "extracted_at": invoice.extracted_at,
                }
                writer.writerow(row)

        logger.info(f"Successfully exported to {output_path}")

        # Export line items separately if requested
        if include_line_items and any(inv.line_items for inv in invoices):
            self._export_line_items(invoices, output_path)

    def _export_line_items(self, invoices: List[Invoice], base_path: Path):
        """Export line items to separate CSV"""
        line_items_path = base_path.parent / f"{base_path.stem}_line_items.csv"

        fieldnames = [
            "invoice_number",
            "line_number",
            "description",
            "quantity",
            "unit_price",
            "amount",
        ]

        with open(line_items_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for invoice in invoices:
                for idx, item in enumerate(invoice.line_items, 1):
                    writer.writerow(
                        {
                            "invoice_number": invoice.invoice_number,
                            "line_number": idx,
                            "description": item.description,
                            "quantity": item.quantity,
                            "unit_price": item.unit_price,
                            "amount": item.amount,
                        }
                    )

        logger.info(f"Exported line items to {line_items_path}")

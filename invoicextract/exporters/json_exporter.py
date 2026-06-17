"""
JSON exporter for invoice data
"""

import json
import logging
from pathlib import Path
from typing import List, Union

from invoicextract.models.invoice import Invoice

logger = logging.getLogger(__name__)


class JSONExporter:
    """
    Exports invoice data to JSON format
    """
    
    def export(
        self, 
        invoices: List[Invoice], 
        output_path: Union[str, Path],
        pretty: bool = True
    ):
        """
        Export invoices to JSON file
        
        Args:
            invoices: List of Invoice objects to export
            output_path: Path to output JSON file
            pretty: If True, format with indentation
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Exporting {len(invoices)} invoices to JSON: {output_path}")
        
        # Convert invoices to dictionaries
        data = {
            'invoices': [self._invoice_to_dict(inv) for inv in invoices],
            'count': len(invoices),
            'exported_at': invoices[0].extracted_at if invoices else None
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)
        
        logger.info(f"Successfully exported to {output_path}")
    
    def _invoice_to_dict(self, invoice: Invoice) -> dict:
        """Convert invoice to dictionary with all fields"""
        return {
            'invoice_number': invoice.invoice_number,
            'vendor': {
                'name': invoice.vendor_name,
                'address': invoice.vendor_address,
                'tax_id': invoice.vendor_tax_id,
                'email': invoice.vendor_email,
                'phone': invoice.vendor_phone
            },
            'customer': {
                'name': invoice.customer_name,
                'address': invoice.customer_address,
                'tax_id': invoice.customer_tax_id
            },
            'dates': {
                'invoice_date': invoice.invoice_date,
                'due_date': invoice.due_date
            },
            'amounts': {
                'subtotal': invoice.subtotal,
                'tax': invoice.tax_amount,
                'discount': invoice.discount_amount,
                'total': invoice.total_amount,
                'currency': invoice.currency
            },
            'line_items': [
                {
                    'description': item.description,
                    'quantity': item.quantity,
                    'unit_price': item.unit_price,
                    'amount': item.amount
                }
                for item in invoice.line_items
            ],
            'payment': {
                'terms': invoice.payment_terms,
                'method': invoice.payment_method
            },
            'metadata': {
                'source_file': invoice.source_file,
                'extracted_at': invoice.extracted_at,
                'is_valid': invoice.is_valid,
                'validation_errors': invoice.validation_errors
            }
        }

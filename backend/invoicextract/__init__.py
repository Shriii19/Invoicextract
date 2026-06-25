"""
InvoiceXtract - Automated invoice data extraction
"""

__version__ = "0.1.0"
__author__ = "InvoiceXtract Contributors"

from invoicextract.core.extractor import InvoiceExtractor
from invoicextract.models.invoice import Invoice

__all__ = ["InvoiceExtractor", "Invoice", "__version__"]

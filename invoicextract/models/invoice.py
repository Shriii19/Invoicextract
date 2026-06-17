"""
Data models for invoice representation
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class LineItem:
    """
    Represents a single line item in an invoice
    """
    description: str
    quantity: float = 1.0
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    
    def __post_init__(self):
        """Calculate amount if not provided"""
        if self.amount is None and self.unit_price is not None:
            self.amount = self.quantity * self.unit_price


@dataclass
class Invoice:
    """
    Represents a complete invoice with all extracted data
    """
    # Required fields
    invoice_number: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[float] = None
    
    # Date fields
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    
    # Financial details
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    discount_amount: Optional[float] = None
    currency: str = "USD"
    
    # Vendor details
    vendor_address: Optional[str] = None
    vendor_tax_id: Optional[str] = None
    vendor_email: Optional[str] = None
    vendor_phone: Optional[str] = None
    
    # Customer details
    customer_name: Optional[str] = None
    customer_address: Optional[str] = None
    customer_tax_id: Optional[str] = None
    
    # Line items
    line_items: List[LineItem] = field(default_factory=list)
    
    # Payment details
    payment_terms: Optional[str] = None
    payment_method: Optional[str] = None
    
    # Metadata
    source_file: Optional[str] = None
    extracted_at: str = field(default_factory=lambda: datetime.now().isoformat())
    raw_text: Optional[str] = None
    
    # Validation
    is_valid: bool = True
    validation_errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert invoice to dictionary"""
        return {
            'invoice_number': self.invoice_number,
            'vendor_name': self.vendor_name,
            'customer_name': self.customer_name,
            'invoice_date': self.invoice_date,
            'due_date': self.due_date,
            'subtotal': self.subtotal,
            'tax_amount': self.tax_amount,
            'discount_amount': self.discount_amount,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'payment_terms': self.payment_terms,
            'line_items_count': len(self.line_items),
            'is_valid': self.is_valid,
            'source_file': self.source_file,
            'extracted_at': self.extracted_at
        }
    
    def __str__(self) -> str:
        """String representation of invoice"""
        return (
            f"Invoice {self.invoice_number} | "
            f"{self.vendor_name} | "
            f"{self.total_amount} {self.currency}"
        )

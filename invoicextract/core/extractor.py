"""
Main invoice extraction orchestrator
"""

import logging
from pathlib import Path
from typing import Union, Optional

from invoicextract.core.ocr import OCREngine
from invoicextract.parsers.generic_parser import GenericParser
from invoicextract.core.validator import InvoiceValidator
from invoicextract.models.invoice import Invoice
from invoicextract.config import SUPPORTED_FORMATS, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)


class InvoiceExtractor:
    """
    Main class for extracting structured data from invoice files
    """
    
    def __init__(self, ocr_engine: Optional[OCREngine] = None):
        """
        Initialize the invoice extractor
        
        Args:
            ocr_engine: Optional custom OCR engine instance
        """
        self.ocr = ocr_engine or OCREngine()
        self.parser = GenericParser()
        self.validator = InvoiceValidator()
        logger.info("InvoiceExtractor initialized")
    
    def extract(self, file_path: Union[str, Path]) -> Invoice:
        """
        Extract structured data from an invoice file
        
        Args:
            file_path: Path to the invoice file (PDF, image, etc.)
        
        Returns:
            Invoice object with extracted data
        
        Raises:
            ValueError: If file format is not supported or file is too large
            FileNotFoundError: If file does not exist
        """
        file_path = Path(file_path)
        
        # Validate file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Validate file format
        if file_path.suffix.lower() not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {file_path.suffix}. "
                f"Supported: {', '.join(SUPPORTED_FORMATS)}"
            )
        
        # Validate file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File too large: {file_size_mb:.1f}MB "
                f"(max: {MAX_FILE_SIZE_MB}MB)"
            )
        
        logger.info(f"Extracting invoice from: {file_path.name}")
        
        # Step 1: OCR - Extract text from file
        raw_text = self.ocr.extract_text(file_path)
        logger.debug(f"Extracted {len(raw_text)} characters of text")
        
        # Step 2: Parse - Extract structured data
        invoice = self.parser.parse(raw_text, file_path)
        logger.debug(f"Parsed invoice #{invoice.invoice_number}")
        
        # Step 3: Validate - Check data quality
        validation_result = self.validator.validate(invoice)
        invoice.validation_errors = validation_result.errors
        invoice.is_valid = validation_result.is_valid
        
        if not invoice.is_valid:
            logger.warning(
                f"Validation warnings for {file_path.name}: "
                f"{len(validation_result.errors)} issue(s)"
            )
        
        logger.info(f"Successfully extracted invoice #{invoice.invoice_number}")
        return invoice
    
    def extract_batch(self, file_paths: list[Union[str, Path]]) -> list[Invoice]:
        """
        Extract data from multiple invoice files
        
        Args:
            file_paths: List of file paths
        
        Returns:
            List of Invoice objects
        """
        invoices = []
        for file_path in file_paths:
            try:
                invoice = self.extract(file_path)
                invoices.append(invoice)
            except Exception as e:
                logger.error(f"Failed to extract {file_path}: {e}")
        
        logger.info(f"Batch extraction complete: {len(invoices)}/{len(file_paths)} succeeded")
        return invoices

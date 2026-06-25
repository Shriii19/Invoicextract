"""
Configuration settings for InvoiceXtract
"""

import os
from pathlib import Path
from typing import Optional

# Base directories
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output"

# OCR settings
OCR_ENGINE = os.getenv("OCR_ENGINE", "tesseract")
OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "eng")
OCR_DPI = int(os.getenv("OCR_DPI", "300"))

# Processing settings
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "50"))
SUPPORTED_FORMATS = [".pdf", ".png", ".jpg", ".jpeg", ".tiff"]

# Export settings
DEFAULT_EXPORT_FORMAT = os.getenv("DEFAULT_EXPORT_FORMAT", "csv")
DECIMAL_PLACES = int(os.getenv("DECIMAL_PLACES", "2"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validation
STRICT_VALIDATION = os.getenv("STRICT_VALIDATION", "true").lower() == "true"

# Ensure directories exist
for directory in [DATA_DIR, LOGS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

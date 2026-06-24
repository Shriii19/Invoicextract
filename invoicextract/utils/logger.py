"""
Logging setup for InvoiceXtract
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from invoicextract.config import LOG_FORMAT, LOG_LEVEL, LOGS_DIR


def setup_logger(name: str, log_file: Optional[str] = None) -> logging.Logger:
    """
    Create and configure a named logger.

    Args:
        name: Logger name (usually __name__ of the calling module).
        log_file: Optional filename inside LOGS_DIR to write logs to.
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        formatter = logging.Formatter(LOG_FORMAT)

        # Console handler
        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        logger.addHandler(console)

        # File handler (optional)
        if log_file:
            file_path = LOGS_DIR / log_file
            file_path.parent.mkdir(parents=True, exist_ok=True)
            fh = logging.FileHandler(file_path, encoding="utf-8")
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger

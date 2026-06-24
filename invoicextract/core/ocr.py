"""
OCR (Optical Character Recognition) engine for text extraction
"""

import io
import logging
from pathlib import Path
from typing import Union

from invoicextract.config import OCR_DPI, OCR_ENGINE, OCR_LANGUAGE

logger = logging.getLogger(__name__)


class OCREngine:
    """
    Handles text extraction from PDF and image files.
    Strategy: pdfplumber → PyMuPDF → EasyOCR (for scanned pages).
    """

    def __init__(self, engine: str = OCR_ENGINE, language: str = OCR_LANGUAGE, dpi: int = OCR_DPI):
        self.engine = engine
        self.language = language
        self.dpi = dpi
        self._easyocr_reader = None
        logger.info(f"OCR engine initialized: {engine} (lang={language}, dpi={dpi})")

    def extract_text(self, file_path: Union[str, Path]) -> str:
        file_path = Path(file_path)
        logger.debug(f"Starting text extraction: {file_path.name}")

        try:
            if file_path.suffix.lower() == ".pdf":
                text = self._extract_from_pdf(file_path)
            else:
                text = self._extract_from_image(file_path)

            logger.debug(f"Extraction complete: {len(text)} characters")
            return text

        except Exception as e:
            logger.error(f"Extraction failed for {file_path.name}: {e}")
            raise

    # ------------------------------------------------------------------
    # PDF extraction
    # ------------------------------------------------------------------

    def _extract_from_pdf(self, pdf_path: Path) -> str:
        text = self._try_pdfplumber(pdf_path)
        if text.strip():
            logger.debug("Text extracted via pdfplumber")
            return text

        text = self._try_pymupdf(pdf_path)
        if text.strip():
            logger.debug("Text extracted via PyMuPDF")
            return text

        logger.info(f"No selectable text in {pdf_path.name}, falling back to OCR")
        return self._ocr_pdf_pages(pdf_path)

    def _try_pdfplumber(self, pdf_path: Path) -> str:
        try:
            import pdfplumber

            pages_text = []
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
            return "\n".join(pages_text)
        except Exception as e:
            logger.debug(f"pdfplumber failed: {e}")
            return ""

    def _try_pymupdf(self, pdf_path: Path) -> str:
        try:
            import fitz  # PyMuPDF

            pages_text = []
            with fitz.open(str(pdf_path)) as doc:
                for page in doc:
                    pages_text.append(page.get_text())
            return "\n".join(pages_text)
        except Exception as e:
            logger.debug(f"PyMuPDF failed: {e}")
            return ""

    def _ocr_pdf_pages(self, pdf_path: Path) -> str:
        """Render each PDF page to an image and run EasyOCR on it."""
        try:
            import fitz
            import numpy as np
            from PIL import Image

            reader = self._get_easyocr_reader()
            pages_text = []

            with fitz.open(str(pdf_path)) as doc:
                for page in doc:
                    mat = fitz.Matrix(self.dpi / 72, self.dpi / 72)
                    pix = page.get_pixmap(matrix=mat)
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    results = reader.readtext(np.array(img), detail=0, paragraph=True)
                    pages_text.append("\n".join(results))

            return "\n".join(pages_text)
        except Exception as e:
            logger.error(f"OCR fallback failed: {e}")
            return ""

    # ------------------------------------------------------------------
    # Image extraction
    # ------------------------------------------------------------------

    def _extract_from_image(self, image_path: Path) -> str:
        try:
            import numpy as np
            from PIL import Image

            reader = self._get_easyocr_reader()
            img = Image.open(image_path)
            results = reader.readtext(np.array(img), detail=0, paragraph=True)
            return "\n".join(results)
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            return ""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_easyocr_reader(self):
        """Lazy-load the EasyOCR reader (slow to initialise)."""
        if self._easyocr_reader is None:
            import easyocr

            lang = "en" if self.language in ("eng", "en") else self.language
            logger.info(f"Loading EasyOCR reader (lang={lang}) …")
            self._easyocr_reader = easyocr.Reader([lang], gpu=False)
        return self._easyocr_reader

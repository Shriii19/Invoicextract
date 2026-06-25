"""
FastAPI backend for InvoiceXtract
"""

import io
import logging
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from invoicextract import InvoiceExtractor
from invoicextract.exporters.csv_exporter import CSVExporter
from invoicextract.exporters.excel_exporter import ExcelExporter
from invoicextract.exporters.json_exporter import JSONExporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="InvoiceXtract API", version="0.1.0", description="Extract structured data from PDF invoices")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

extractor = InvoiceExtractor()

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".tiff"}


def _save_upload(file: UploadFile, content: bytes) -> Path:
    ext = Path(file.filename).suffix.lower()
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tmp.write(content)
    tmp.close()
    return Path(tmp.name)


@app.get("/")
async def root():
    return {"service": "InvoiceXtract API", "version": "0.1.0", "status": "ok"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/api/extract")
async def extract_invoice(file: UploadFile = File(...)):
    """Upload a PDF/image invoice and receive structured JSON data."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")

    content = await file.read()
    tmp_path = _save_upload(file, content)

    try:
        invoice = extractor.extract(tmp_path)
        return {
            "success": True,
            "filename": file.filename,
            "invoice": {
                "invoice_number": invoice.invoice_number,
                "vendor": {
                    "name": invoice.vendor_name,
                    "address": invoice.vendor_address,
                    "email": invoice.vendor_email,
                    "phone": invoice.vendor_phone,
                    "tax_id": invoice.vendor_tax_id,
                },
                "customer": {
                    "name": invoice.customer_name,
                    "address": invoice.customer_address,
                },
                "dates": {
                    "invoice_date": invoice.invoice_date,
                    "due_date": invoice.due_date,
                },
                "amounts": {
                    "subtotal": invoice.subtotal,
                    "tax": invoice.tax_amount,
                    "total": invoice.total_amount,
                    "currency": invoice.currency,
                },
                "line_items": [
                    {
                        "description": item.description,
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "amount": item.amount,
                    }
                    for item in invoice.line_items
                ],
                "payment_terms": invoice.payment_terms,
                "is_valid": invoice.is_valid,
                "validation_errors": invoice.validation_errors,
                "extracted_at": invoice.extracted_at,
            },
        }
    except FileNotFoundError as e:
        raise HTTPException(404, str(e))
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(500, f"Extraction failed: {e}")
    finally:
        tmp_path.unlink(missing_ok=True)


@app.post("/api/extract/download")
async def extract_and_download(
    file: UploadFile = File(...),
    format: str = Form("csv"),
):
    """Upload a PDF/image invoice and download as CSV, Excel, or JSON."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported file type '{ext}'")

    if format not in ("csv", "excel", "json"):
        raise HTTPException(400, "format must be csv, excel, or json")

    content = await file.read()
    tmp_path = _save_upload(file, content)
    out_dir = Path(tempfile.mkdtemp())

    try:
        invoice = extractor.extract(tmp_path)

        if format == "csv":
            out_path = out_dir / "invoice.csv"
            CSVExporter().export([invoice], out_path)
            media_type = "text/csv"
            dl_name = "invoice.csv"
        elif format == "excel":
            out_path = out_dir / "invoice.xlsx"
            ExcelExporter().export([invoice], out_path)
            media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            dl_name = "invoice.xlsx"
        else:
            out_path = out_dir / "invoice.json"
            JSONExporter().export([invoice], out_path)
            media_type = "application/json"
            dl_name = "invoice.json"

        file_bytes = out_path.read_bytes()
        return StreamingResponse(
            io.BytesIO(file_bytes),
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{dl_name}"'},
        )
    except Exception as e:
        logger.error(f"Export failed: {e}")
        raise HTTPException(500, str(e))
    finally:
        tmp_path.unlink(missing_ok=True)

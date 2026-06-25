"""
Start the InvoiceXtract FastAPI backend.
Run from the repo root:  python backend/run.py
Or from inside backend/:  python run.py
"""
import os
import sys

# Ensure the repo root is on sys.path so `invoicextract` package is importable
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "invoicextract.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[ROOT],
    )

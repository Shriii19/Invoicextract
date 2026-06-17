# InvoiceXtract

> **Stop typing invoices. Start extracting them.**

InvoiceXtract is an open-source Python application that automates the extraction of structured data from PDF invoices. It helps businesses, freelancers, accountants, and developers eliminate manual data entry by converting invoice information into machine-readable formats.

[![Tests](https://github.com/yourusername/InvoiceXtract/workflows/Tests/badge.svg)](https://github.com/yourusername/InvoiceXtract/actions)
[![Code Coverage](https://codecov.io/gh/yourusername/InvoiceXtract/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/InvoiceXtract)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/InvoiceXtract.git
cd InvoiceXtract

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from invoicextract import InvoiceExtractor
from invoicextract.exporters.csv_exporter import CSVExporter

# Initialize extractor
extractor = InvoiceExtractor()

# Extract from single invoice
invoice = extractor.extract("path/to/invoice.pdf")

print(f"Invoice #: {invoice.invoice_number}")
print(f"Vendor: {invoice.vendor_name}")
print(f"Total: {invoice.total_amount} {invoice.currency}")

# Export to CSV
exporter = CSVExporter()
exporter.export([invoice], "output/invoices.csv")
```

### CLI Usage

```bash
# Extract single invoice
python -m invoicextract.main extract invoice.pdf -o output.csv -f csv

# Batch process directory
python -m invoicextract.main batch ./invoices -o output/ -f excel

# Start API server
python -m invoicextract.main api --port 8000
```

---

## ✨ Features

- 📄 **PDF Text Extraction** - Fast text extraction from PDF invoices
- 🤖 **OCR Support** - Handle scanned PDFs with EasyOCR
- 📦 **Batch Processing** - Process multiple invoices at once
- 📊 **Multiple Export Formats** - CSV, Excel, JSON
- 🔍 **Smart Field Detection** - Extracts:
  - Invoice Number
  - Invoice Date
  - Vendor/Supplier Name
  - Customer Name
  - Tax/GST/VAT
  - Subtotal
  - Total Amount
  - Currency
  - Due Date
  - Addresses
- 💾 **Offline Processing** - Privacy-first, no data sent to servers
- 🧩 **Extensible** - Easy to add custom parsers for specific vendors
- 🔒 **Type-Safe** - Full type hints throughout codebase

---

## 📋 Requirements

- Python 3.8 or higher
- 2GB RAM minimum (4GB+ recommended for OCR)
- 500MB disk space

---

## 🛠️ Installation Options

### Option 1: From Source (Development)

```bash
git clone https://github.com/yourusername/InvoiceXtract.git
cd InvoiceXtract
pip install -r requirements-dev.txt
make setup
```

### Option 2: From PyPI (Coming Soon)

```bash
pip install invoicextract
```

### Option 3: Docker

```bash
docker build -t invoicextract .
docker run -v /path/to/invoices:/invoices invoicextract
```

---

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Usage Examples](docs/usage.md)
- [API Reference](docs/api_reference.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Architecture](docs/architecture.md)

---

## 🎯 Project Goals

- ✅ Reduce manual invoice processing time
- ✅ Improve extraction accuracy
- ✅ Support invoices from different vendors
- ✅ Provide free, open-source alternative to commercial tools
- ✅ Build developer-friendly platform for document processing

---

## 🏗️ Architecture

```
PDF Invoice
    ↓
PDF Text Extraction
    ↓
OCR (optional, for scanned PDFs)
    ↓
Field Detection Engine (Regex + Pattern Matching)
    ↓
Data Validation
    ↓
Export (CSV / Excel / JSON)
```

---

## 📁 Project Structure

```
InvoiceXtract/
├── invoicextract/          # Main package
│   ├── core/              # Core extraction logic
│   ├── parsers/           # Invoice parsers
│   ├── exporters/         # Export formats
│   ├── models/            # Data models
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example scripts
└── .github/              # GitHub configuration
```

---

## 📅 Roadmap

### Phase 1 (Current)
- [x] Basic project structure
- [x] PDF text extraction setup
- [x] Generic invoice parser
- [x] CSV export
- [x] Batch processing
- [ ] Complete PDF text extraction implementation

### Phase 2
- [ ] Excel export enhancements
- [ ] JSON export
- [ ] OCR full implementation
- [ ] Duplicate detection
- [ ] Template-based parsers

### Phase 3
- [ ] Web dashboard
- [ ] REST API
- [ ] User-defined templates
- [ ] Multi-language support
- [ ] Docker deployment

---

## 🤝 Contributing

We welcome contributions from everyone! Please see our [Contributing Guide](CONTRIBUTING.md) for:

- How to report bugs
- How to suggest features
- How to submit code changes
- Coding standards
- Testing guidelines

**Quick contribution steps:**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit changes (`git commit -m 'feat: add amazing feature'`)
6. Push to branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Areas Needing Help

- [x] PDF text extraction implementation
- [x] Additional invoice parsers
- [ ] OCR improvements
- [ ] Web UI development
- [ ] Documentation
- [ ] Testing

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 🌟 Acknowledgments

- Built with [PyMuPDF](https://pymupdf.readthedocs.io/) and [pdfplumber](https://github.com/jsvine/pdfplumber)
- OCR powered by [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- Data processing with [Pandas](https://pandas.pydata.org/)

---

## 📞 Support

- **Issues** - Use [GitHub Issues](https://github.com/yourusername/InvoiceXtract/issues)
- **Discussions** - Use [GitHub Discussions](https://github.com/yourusername/InvoiceXtract/discussions)
- **Email** - contact@invoicextract.dev

---

## 🎓 Learning Resources

- [Python Documentation](https://docs.python.org/3/)
- [PDF Processing in Python](https://realpython.com/pdf-python/)
- [Regular Expressions](https://docs.python.org/3/library/re.html)
- [Testing with Pytest](https://docs.pytest.org/)

---

**Made with ❤️ by the open-source community**

⭐ If you find this project helpful, please consider giving it a star!


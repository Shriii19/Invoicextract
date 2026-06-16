# InvoiceXtract

> **Stop typing invoices. Start extracting them.**

InvoiceXtract is an open-source Python application that automates the extraction of structured data from PDF invoices. It helps businesses, freelancers, accountants, and developers eliminate manual data entry by converting invoice information into machine-readable formats.

## 🚀 Overview

Processing invoices manually is slow, repetitive, and prone to errors. InvoiceXtract simplifies this process by extracting important fields from PDF invoices and exporting them into structured formats such as CSV, Excel, and JSON.

The project is designed to work **offline**, ensuring data privacy and making it suitable for organizations that cannot upload sensitive documents to third-party services.

---

## ✨ Features

- 📄 Extract data from PDF invoices
- 📦 Batch process multiple invoices
- 🔍 Extract key fields:
  - Invoice Number
  - Invoice Date
  - Vendor/Supplier Name
  - Customer Name (when available)
  - Tax/GST/VAT
  - Subtotal
  - Total Amount
  - Currency
- 📊 Export to CSV, Excel, and JSON
- 💾 Store extracted data locally
- 🔒 Privacy-first (offline processing)
- 🧩 Modular architecture for adding new invoice templates

---

## 🎯 Project Goals

- Reduce manual invoice processing time
- Improve extraction accuracy
- Support invoices from different vendors and layouts
- Provide a free and open-source alternative to commercial invoice extraction tools
- Build a developer-friendly platform for document processing

---

## 🏗️ Planned Architecture

```
PDF Invoice
      │
      ▼
PDF Text Extraction
      │
      ▼
OCR (for scanned PDFs)
      │
      ▼
Field Detection Engine
      │
      ▼
Data Validation
      │
      ▼
Export (CSV / Excel / JSON)
```

---

## 🛠️ Tech Stack

- Python
- FastAPI
- PyMuPDF / pdfplumber
- EasyOCR or Tesseract OCR
- Pandas
- SQLite / PostgreSQL

---

## 📅 Roadmap

### Phase 1
- [ ] PDF upload
- [ ] Text extraction
- [ ] Extract invoice number
- [ ] Extract invoice date
- [ ] Extract vendor name
- [ ] Extract total amount
- [ ] Export to CSV

### Phase 2
- [ ] Batch processing
- [ ] Excel export
- [ ] JSON export
- [ ] OCR support for scanned PDFs
- [ ] Duplicate invoice detection

### Phase 3
- [ ] Web dashboard
- [ ] REST API
- [ ] User-defined extraction templates
- [ ] Multi-language support
- [ ] Docker deployment

---

## 🤝 Contributing

Contributions are welcome!

You can help by:
- Adding support for new invoice formats
- Improving extraction accuracy
- Writing tests
- Fixing bugs
- Improving documentation
- Building new features

Please open an issue before working on large changes.

---

## 🌟 Vision

InvoiceXtract aims to become a powerful, privacy-focused, open-source document extraction platform that enables anyone to automate invoice processing without relying on expensive cloud services or proprietary software.

---

## 📄 License

This project is licensed under the MIT License.

---

Made with ❤️ by the open-source community.
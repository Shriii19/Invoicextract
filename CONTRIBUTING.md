# Contributing to InvoiceXtract

Thank you for your interest in contributing to InvoiceXtract! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## 📋 Code of Conduct

Please be respectful and constructive in all interactions. We're committed to providing a welcoming and inclusive environment.

---

## 🎯 How to Contribute

### 1. **Report Bugs**

Found a bug? Create an issue using the bug report template:
- Describe the problem clearly
- Include steps to reproduce
- Provide system information (OS, Python version)
- Attach sample PDFs (if possible)

### 2. **Suggest Features**

Have an idea? Create a feature request:
- Describe the feature and use case
- Explain why it would be useful
- Suggest implementation approaches

### 3. **Improve Documentation**

- Fix typos and unclear explanations
- Add examples and use cases
- Improve API documentation
- Create tutorials

### 4. **Submit Code Changes**

#### Prerequisites

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/InvoiceXtract.git
   cd InvoiceXtract
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

#### Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or for bug fixes:
   git checkout -b fix/bug-description
   ```

2. **Make your changes**
   - Follow the coding style (see below)
   - Write/update tests
   - Update documentation

3. **Run tests**
   ```bash
   pytest
   pytest --cov=invoicextract  # With coverage report
   ```

4. **Check code quality**
   ```bash
   black invoicextract tests
   flake8 invoicextract tests
   mypy invoicextract
   pylint invoicextract
   ```

5. **Commit your changes**
   ```bash
   git commit -m "feat: Add new feature description"
   # Use conventional commits:
   # feat: A new feature
   # fix: A bug fix
   # docs: Documentation changes
   # refactor: Code refactoring
   # test: Adding/updating tests
   # style: Formatting changes
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Use the PR template
   - Reference related issues
   - Provide clear description of changes
   - Include screenshots if UI-related

---

## 💻 Coding Standards

### Style Guide

- **Language**: Python 3.8+
- **Style**: [PEP 8](https://pep8.org/)
- **Formatter**: `black` (line length: 100)
- **Linter**: `flake8`
- **Type hints**: Use type hints for all functions

### Example Code Style

```python
"""
Module docstring explaining purpose
"""

from typing import List, Optional
from loguru import logger

class MyClass:
    """Class docstring"""
    
    def __init__(self, param: str) -> None:
        """Initialize the class"""
        self.param = param
    
    def process(self, data: List[str]) -> Optional[str]:
        """
        Process data and return result
        
        Args:
            data: List of strings to process
            
        Returns:
            Processed result or None
        """
        if not data:
            logger.warning("No data provided")
            return None
        
        result = " ".join(data)
        logger.info(f"Processed {len(data)} items")
        return result
```

### Directory Structure

- `invoicextract/` - Main package
  - `core/` - Core functionality
  - `parsers/` - Invoice parsers
  - `exporters/` - Export formats
  - `models/` - Data models
  - `utils/` - Utilities
- `tests/` - Test suite
- `docs/` - Documentation

---

## 🧪 Testing

### Writing Tests

- Place tests in `tests/` directory
- Use `pytest` framework
- Use descriptive test names: `test_<function>_<scenario>`
- Aim for >80% code coverage

### Example Test

```python
import pytest
from invoicextract.models.invoice import Invoice

def test_invoice_creation():
    """Test creating an invoice object"""
    invoice = Invoice(
        invoice_number="INV-001",
        vendor_name="Acme Corp",
        total_amount=100.0
    )
    
    assert invoice.invoice_number == "INV-001"
    assert invoice.vendor_name == "Acme Corp"
    assert invoice.total_amount == 100.0

def test_invoice_to_dict():
    """Test converting invoice to dictionary"""
    invoice = Invoice(invoice_number="INV-001")
    data = invoice.to_dict()
    
    assert isinstance(data, dict)
    assert data["invoice_number"] == "INV-001"
```

---

## 🎨 Areas for Contribution

### High Priority
- [ ] Implement PDF text extraction (pdfplumber/PyMuPDF)
- [ ] Complete OCR implementation
- [ ] Add more invoice templates/parsers
- [ ] Improve field extraction accuracy
- [ ] Add comprehensive tests

### Medium Priority
- [ ] Web UI dashboard
- [ ] REST API endpoints
- [ ] Database integration
- [ ] Docker deployment
- [ ] Performance optimization

### Community Contributions
- [ ] Translations
- [ ] Documentation improvements
- [ ] Bug reports
- [ ] Feature requests
- [ ] Integration examples

---

## 📝 Pull Request Process

1. **Update documentation** - If changing functionality
2. **Add tests** - All new features need tests
3. **Update CHANGELOG** - Document your changes
4. **Self-review** - Check your code before submitting
5. **Request review** - Ask maintainers to review

### PR Checklist

- [ ] Follows style guide
- [ ] Added/updated tests
- [ ] All tests pass
- [ ] Updated documentation
- [ ] No breaking changes (or documented)
- [ ] Conventional commit messages

---

## 🚀 Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and ideas
- **Email** - Contact maintainers
- **Documentation** - Check docs/ directory

---

## 📄 License

By contributing, you agree your code will be licensed under MIT License.

---

## 🌟 Recognition

Contributors will be recognized in:
- README.md
- GitHub contributors page
- Release notes

---

**Thank you for making InvoiceXtract better!** 🎉

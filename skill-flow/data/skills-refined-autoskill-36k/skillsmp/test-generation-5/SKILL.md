---
type: skill
name: Test Generation
description: Generate comprehensive test cases for code
skillSlug: test-generation
phases: [E, V]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Test Generation Skill

## When to Use

Use this skill when:
- Creating unit tests for functions (indexer, search, organize)
- Writing integration tests for full workflows
- Testing PDF extraction (pdfplumber and OCR)
- Testing database operations (SQLite/FTS5)
- Validating document classification logic

## Testing Framework

Currently **no test framework configured**, but recommended approach:

- **Framework**: `pytest` (recommended for Python projects)
- **Test Location**: `tests/` directory
- **Naming**: `test_*.py` files
- **Coverage**: Aim for >80% coverage

## Test Organization

```
tests/
├── test_indexer.py      # Tests for indexer.py
├── test_search.py       # Tests for search.py
├── test_organize.py     # Tests for organize.py
├── test_extraction.py   # Tests for PDF extraction
└── fixtures/            # Test fixtures (sample PDFs)
```

## Key Functions to Test

### From `indexer.py`:
- `create_db()` - Database creation and schema
- `extract_text_from_pdf()` - PDF text extraction
- `extract_text_from_pdf_ocr()` - OCR fallback
- `classify_document()` - Document classification logic
- `extract_metadata()` - Metadata extraction
- `index_files()` - Full indexing workflow

### From `search.py`:
- `search()` - Full-text search with filters
- `list_categories()` - Category listing
- `list_contracts()` - Contract listing

### From `organize.py`:
- `organize_documents()` - Document organization
- `generate_summary_report()` - Report generation

## Testing Patterns

### Unit Test Example

```python
import pytest
from contrato.indexer import classify_document

def test_classify_document_contrato():
    """Test classification of main contract."""
    filename = "TNE_JU_COM_0002-13 - SIEMENS - Contrato.pdf"
    result = classify_document(filename, "/path/to/file")
    
    assert result["category"] == "contrato"
    assert result["document_type"] == "contrato_principal"
    assert result["contract_number"] == "TNE_JU_COM_0002-13"

def test_classify_document_aditivo():
    """Test classification of addendums."""
    filename = "TNE_JU_COM_0002-13 - SIEMENS - 1ºAditivo.pdf"
    result = classify_document(filename, "/path/to/file")
    
    assert result["category"] == "aditivo"
    assert result["document_number"] == "1"

def test_classify_document_anexo():
    """Test classification of attachments."""
    filename = "TNE_JU_COM_0002-13 (Anexo I).pdf"
    result = classify_document(filename, "/path/to/file")
    
    assert result["category"] == "anexo"
    assert result["document_number"] == "I"
```

### Integration Test Example

```python
def test_full_indexing_workflow(tmp_path):
    """Test complete indexing workflow."""
    # Setup: Create test PDF in tmp_path
    # Execute: Run index_files()
    # Assert: Verify documents in database
    # Assert: Verify FTS index created
```

### Mocking Strategies

For external dependencies:
- **PDFs**: Use sample PDF files in `fixtures/`
- **OCR**: Mock pytesseract when testing extraction
- **Database**: Use in-memory SQLite for tests
- **File System**: Use `tmp_path` from pytest

## Test Coverage Goals

- **Critical Functions**: 100% coverage
  - `classify_document()` - Core classification logic
  - `extract_text_from_pdf()` - Extraction methods
  - Database operations

- **Overall Coverage**: >80%
- **Edge Cases**: Test error handling, empty files, corrupted PDFs

## Test Data

Create test fixtures:
- Sample PDFs (with text)
- Sample scanned PDFs (for OCR testing)
- Sample contract filenames
- Database fixtures with known data

## Best Practices

1. **Isolation**: Each test should be independent
2. **Fixtures**: Reuse test PDFs and data
3. **Clear Names**: Test names should describe what they test
4. **Portuguese**: Test descriptions can be in Portuguese
5. **Assertions**: Use descriptive assertion messages

## Common Test Scenarios

### PDF Extraction Tests
- Extract text from normal PDFs
- Fallback to OCR for scanned PDFs
- Handle corrupted PDFs gracefully
- Extract metadata correctly

### Classification Tests
- Classify contracts correctly
- Extract contract numbers
- Identify addendums by number
- Identify attachments by number

### Database Tests
- Verify schema creation
- Test FTS5 index updates
- Validate triggers work
- Test query performance

### Error Handling Tests
- Missing PDF files
- Corrupted PDFs
- Database connection errors
- OCR failures

## Checklist

When writing tests:
- [ ] Test file created in `tests/` directory
- [ ] Test functions named `test_*`
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Fixtures created for reusable data
- [ ] Assertions are clear and descriptive
- [ ] Integration tests for workflows
- [ ] Mock external dependencies appropriately

---
type: skill
name: Code Review
description: Review code quality, patterns, and best practices
skillSlug: code-review
phases: [R, V]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Code Review Skill

## When to Use

Use this skill when:
- Reviewing code changes before merge
- Ensuring code quality and consistency
- Validating security practices
- Checking performance considerations
- Verifying adherence to project patterns

## Code Review Guidelines

### Python Style

- **PEP 8 Compliance**: Follow Python style guide
- **Function Naming**: snake_case for functions (`extract_text_from_pdf`)
- **Constants**: UPPER_CASE for constants (`DB_NAME`, `ROOT_DIR`)
- **Imports**: Standard library, third-party, local (grouped)

### Code Patterns in Project

#### Database Operations Pattern

```python
# Pattern: Always use parameterized queries
cursor.execute("SELECT * FROM documents WHERE filepath = ?", (abs_path,))
```

#### Error Handling Pattern

```python
# Pattern: Try-except with specific error messages
try:
    text = extract_text_from_pdf(full_path)
except Exception as e:
    print(f"Erro ao processar {file}: {e}")
    errors += 1
    continue
```

#### Function Documentation Pattern

```python
# Pattern: Portuguese docstrings
def classify_document(filename, filepath):
    """Classifica o documento baseado no nome do arquivo e caminho."""
```

## Code Quality Checks

### 1. Security

- ✅ **SQL Injection**: All queries use parameterized statements
- ✅ **Path Traversal**: Validate file paths before processing
- ✅ **Input Validation**: Validate user inputs in search functions
- ✅ **Error Messages**: Don't expose sensitive information

Example from codebase:
```python
# ✅ Good: Parameterized query
cursor.execute("SELECT id FROM documents WHERE filepath = ?", (abs_path,))

# ❌ Bad: String formatting (vulnerable)
cursor.execute(f"SELECT id FROM documents WHERE filepath = '{abs_path}'")
```

### 2. Performance

- **Database Indexes**: Verify indexes exist for common queries
- **FTS5 Usage**: Proper use of full-text search
- **Lazy Loading**: Don't load entire PDFs into memory unnecessarily
- **Incremental Processing**: Skip already processed files

Checkpoints:
- [ ] Indexes created for filtered columns
- [ ] FTS5 queries optimized
- [ ] File operations efficient
- [ ] Memory usage reasonable

### 3. Error Handling

- **Graceful Degradation**: System works even if OCR unavailable
- **Clear Error Messages**: Portuguese error messages with context
- **Error Recovery**: Continue processing other files on failure
- **Logging**: Important operations logged

Pattern from codebase:
```python
try:
    # Try primary method
    text = extract_text_from_pdf_direct(pdf)
except Exception as e:
    # Fallback method
    text = extract_text_from_pdf_ocr(pdf)
```

### 4. Code Organization

- **Single Responsibility**: Functions do one thing
- **DRY Principle**: Don't repeat code
- **Clear Naming**: Functions and variables self-documenting
- **Module Structure**: Logical grouping of functions

## Common Patterns to Review

### PDF Processing Pattern

```python
# Pattern: Try direct extraction, fallback to OCR
text, stats = extract_text_from_pdf(filepath)
if not text or len(text.strip()) < MIN_TEXT_LENGTH:
    # Use OCR or handle error
```

### Database Transaction Pattern

```python
# Pattern: Commit after successful operations
cursor.execute("INSERT INTO ...")
conn.commit()
```

### Classification Pattern

```python
# Pattern: Regex-based classification with fallbacks
contract_match = re.search(r'tne_ju_com_\d{4}-\d{2}', filename_lower)
contract_number = contract_match.group(0).upper() if contract_match else None
```

## Style Checklist

- [ ] PEP 8 compliant
- [ ] Portuguese docstrings for functions
- [ ] Descriptive variable names
- [ ] Constants at module level
- [ ] Proper import organization
- [ ] No hardcoded values (use constants)
- [ ] Consistent indentation (4 spaces)

## Security Checklist

- [ ] SQL queries use parameterized statements
- [ ] File paths validated/sanitized
- [ ] User inputs validated
- [ ] Error messages don't expose internals
- [ ] Sensitive data handled securely

## Performance Checklist

- [ ] Database indexes appropriate
- [ ] FTS5 queries optimized
- [ ] File operations efficient
- [ ] Memory usage reasonable
- [ ] Unnecessary operations avoided

## Documentation Checklist

- [ ] Functions have docstrings
- [ ] Complex logic has comments
- [ ] README.md updated if needed
- [ ] Examples match implementation

## Review Focus Areas

### For `indexer.py`:
- PDF extraction logic
- OCR fallback implementation
- Classification regex patterns
- Database schema creation
- Metric collection

### For `search.py`:
- FTS5 query construction
- Filter parameter handling
- CSV export logic
- Result formatting

### For `organize.py`:
- SQL aggregation queries
- Report generation
- Data formatting

## Examples from Codebase

### Good Pattern - Error Handling

```python
try:
    text, stats = extract_text_from_pdf(full_path)
except Exception as e:
    print(f"   ❌ Erro ao processar {file}: {e}")
    errors += 1
    save_extraction_metrics(cursor, None, {}, 0, success=False, error_message=str(e))
    continue
```

### Good Pattern - Validation

```python
if not text or len(text.strip()) < MIN_TEXT_LENGTH:
    print(f"   ❌ Sem texto extraível ou muito curto ({len(text) if text else 0} chars)")
    errors += 1
    continue
```

## Anti-Patterns to Avoid

- ❌ String formatting in SQL queries
- ❌ Silent failures (always log errors)
- ❌ Hardcoded file paths
- ❌ Missing error handling
- ❌ Inefficient database queries
- ❌ Memory-intensive operations

---
type: skill
name: Security Audit
description: Security review checklist for code and infrastructure
skillSlug: security-audit
phases: [R, V]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Security Audit Skill

## When to Use

Use this skill when:
- Reviewing code for security vulnerabilities
- Auditing database operations
- Validating input handling
- Checking file system operations
- Reviewing external dependencies

## Security Checklist for This Project

### SQL Injection Prevention

✅ **CRITICAL**: All database queries must use parameterized statements

**Pattern from codebase:**
```python
# ✅ Good: Parameterized query
cursor.execute("SELECT id FROM documents WHERE filepath = ?", (abs_path,))

# ✅ Good: Multiple parameters
cursor.execute("""
    INSERT INTO documents (filename, filepath, content)
    VALUES (?, ?, ?)
""", (file, abs_path, text))
```

**Check:**
- [ ] No string formatting in SQL queries
- [ ] All user inputs passed as parameters
- [ ] Search queries use parameterized FTS5 MATCH

### Path Traversal Prevention

✅ **IMPORTANT**: Validate and sanitize file paths

**Pattern from codebase:**
```python
# ✅ Good: Use absolute paths
abs_path = os.path.abspath(full_path)

# ✅ Good: Validate file extension
if not file.lower().endswith(".pdf"):
    continue
```

**Check:**
- [ ] Paths validated before file operations
- [ ] Only PDF files processed
- [ ] No arbitrary path access
- [ ] Absolute paths used consistently

### Input Validation

✅ **IMPORTANT**: Validate all user inputs in search functions

**Check in `search.py`:**
- [ ] Search query parameter validated
- [ ] Category filter validated (allowed values)
- [ ] Contract number validated/sanitized
- [ ] CSV export filename validated

**Pattern:**
```python
# Validate category
if category and category not in ["contrato", "aditivo", "anexo", "outros"]:
    raise ValueError("Categoria inválida")
```

### Error Handling Security

✅ **IMPORTANT**: Don't expose sensitive information in errors

**Pattern from codebase:**
```python
# ✅ Good: Generic error message
except Exception as e:
    print(f"   ❌ Erro ao processar {file}: {e}")
    # Log details internally, don't expose to user

# ❌ Bad: Exposing internals
except Exception as e:
    print(f"SQL Error: {e.sqlite_errorname}")
```

**Check:**
- [ ] Error messages don't reveal internal paths
- [ ] Database errors handled gracefully
- [ ] No stack traces in user-facing errors

### File Processing Security

**Check PDF Processing:**
- [ ] File size limits enforced (optional)
- [ ] Malformed PDFs handled gracefully
- [ ] OCR process isolated (if needed)
- [ ] Temporary files cleaned up

### Database Security

**Check:**
- [ ] Database file permissions appropriate
- [ ] No sensitive data in plain text (if applicable)
- [ ] Transactions used correctly
- [ ] Database connections closed properly

**Pattern:**
```python
# ✅ Good: Always close connections
conn = create_db()
try:
    index_files(conn)
finally:
    conn.close()
```

### Dependency Security

**Check:**
- [ ] Dependencies up to date
- [ ] No known vulnerabilities in dependencies
- [ ] Optional dependencies (OCR) fail gracefully if missing

**Dependencies to audit:**
- `pdfplumber` - PDF processing
- `pytesseract` - OCR (optional)
- `pdf2image` - PDF to image conversion (optional)
- `pandas` - CSV export (optional)
- `sqlite3` - Built-in, but verify usage

### Data Validation

**Check:**
- [ ] Filenames sanitized before processing
- [ ] Metadata validated before JSON encoding
- [ ] Contract numbers validated format
- [ ] Text length limits considered

## Common Vulnerabilities to Check

### 1. SQL Injection (Critical)

**Vulnerable Pattern:**
```python
# ❌ VULNERABLE
query = f"SELECT * FROM documents WHERE filename = '{user_input}'"
cursor.execute(query)
```

**Secure Pattern:**
```python
# ✅ SECURE
cursor.execute("SELECT * FROM documents WHERE filename = ?", (user_input,))
```

### 2. Path Traversal (High)

**Vulnerable Pattern:**
```python
# ❌ VULNERABLE
filepath = user_input  # Could be "../../etc/passwd"
```

**Secure Pattern:**
```python
# ✅ SECURE
abs_path = os.path.abspath(user_input)
if not abs_path.startswith(ROOT_DIR):
    raise ValueError("Path outside allowed directory")
```

### 3. Command Injection (High)

**Check OCR usage:**
```python
# ✅ Good: Using library, not shell
pytesseract.image_to_string(image, lang='por')

# ❌ Bad: Shell command
os.system(f"tesseract {filepath} output")
```

### 4. Information Disclosure (Medium)

- Check error messages don't reveal file paths
- Check database errors don't expose schema
- Verify sensitive data not logged

## Security Review Checklist

### Code Review
- [ ] No SQL injection vulnerabilities
- [ ] No path traversal vulnerabilities
- [ ] Input validation present
- [ ] Error handling secure
- [ ] No command injection
- [ ] Sensitive data protected

### Database Review
- [ ] All queries parameterized
- [ ] Transactions used correctly
- [ ] Database permissions appropriate
- [ ] No sensitive data in plain text

### File Operations Review
- [ ] Paths validated
- [ ] File types checked
- [ ] Size limits considered
- [ ] Temporary files cleaned

### Dependency Review
- [ ] Dependencies up to date
- [ ] No known CVEs
- [ ] Optional dependencies fail gracefully

## Project-Specific Security Notes

### OCR Dependencies

If OCR is unavailable:
- System should continue working
- Clear message about limitation
- No crashes or security issues

### Database Location

- SQLite database is local file
- No network access required
- File permissions should be appropriate

### PDF Processing

- PDFs may contain malicious content
- Library (pdfplumber) should handle safely
- OCR process should be isolated if concerns

## Examples from Codebase

### Secure Pattern - SQL Query

```python
# From search.py - Secure parameterized query
where_clauses = ["documents_fts MATCH ?"]
params = [query]

if category:
    where_clauses.append("category = ?")
    params.append(category)

where_sql = " AND ".join(where_clauses)
cursor.execute(sql, params)
```

### Secure Pattern - File Path

```python
# From indexer.py - Safe path handling
full_path = os.path.join(root, file)
abs_path = os.path.abspath(full_path)
# Validates path is within ROOT_DIR implicitly
```

## Remediation Priority

1. **Critical**: SQL injection, command injection
2. **High**: Path traversal, input validation
3. **Medium**: Error disclosure, dependency updates
4. **Low**: Information leakage, logging improvements

## Testing Security

When auditing:
- Test with malicious inputs
- Test edge cases
- Verify error handling
- Check dependency versions
- Review file permissions

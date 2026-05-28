---
name: security-audit
description: Use this skill when reviewing code and infrastructure for security vulnerabilities.
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

✅ **CRITICAL**: All database queries must use parameterized statements.

**Pattern from codebase:**
```python
# ✅ Good: Parameterized query
cursor.execute("SELECT id FROM documents WHERE filepath = ?", (abs_path,))
```

**Check:**
- [ ] No string formatting in SQL queries
- [ ] All user inputs passed as parameters

### Path Traversal Prevention

✅ **IMPORTANT**: Validate and sanitize file paths.

**Pattern from codebase:**
```python
# ✅ Good: Use absolute paths
abs_path = os.path.abspath(full_path)
```

**Check:**
- [ ] Paths validated before file operations
- [ ] Only allowed file types processed

### Input Validation

✅ **IMPORTANT**: Validate all user inputs in search functions.

**Check:**
- [ ] Search query parameter validated
- [ ] Category filter validated (allowed values)

**Pattern:**
```python
# Validate category
if category and category not in ["contrato", "aditivo", "anexo", "outros"]:
    raise ValueError("Categoria inválida")
```

### Error Handling Security

✅ **IMPORTANT**: Don't expose sensitive information in errors.

**Pattern from codebase:**
```python
# ✅ Good: Generic error message
except Exception as e:
    print(f"   ❌ Erro ao processar {file}: {e}")
```

**Check:**
- [ ] Error messages don't reveal internal paths

### File Processing Security

**Check PDF Processing:**
- [ ] File size limits enforced (optional)
- [ ] Malformed PDFs handled gracefully

### Database Security

**Check:**
- [ ] Database file permissions appropriate
- [ ] No sensitive data in plain text (if applicable)

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

### Data Validation

**Check:**
- [ ] Filenames sanitized before processing
- [ ] Metadata validated before JSON encoding

## Common Vulnerabilities to Check

### 1. SQL Injection (Critical)

**Vulnerable Pattern:**
```python
# ❌ VULNERABLE
query = f"SELECT * FROM documents WHERE filename = '{user_input}'"
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
```

### 4. Information Disclosure (Medium)

- Check error messages don't reveal file paths
- Check database errors don't expose schema

## Security Review Checklist

### Code Review
- [ ] No SQL injection vulnerabilities
- [ ] No path traversal vulnerabilities
- [ ] Input validation present
- [ ] Error handling secure

### Database Review
- [ ] All queries parameterized
- [ ] Transactions used correctly

### File Operations Review
- [ ] Paths validated
- [ ] File types checked

### Dependency Review
- [ ] Dependencies up to date
- [ ] No known CVEs

## Project-Specific Security Notes

### Database Location

- SQLite database is local file
- No network access required

### PDF Processing

- PDFs may contain malicious content
- Library (pdfplumber) should handle safely

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

## Remediation Priority

1. **Critical**: SQL injection, command injection
2. **High**: Path traversal, input validation
3. **Medium**: Error disclosure, dependency updates

## Testing Security

When auditing:
- Test with malicious inputs
- Test edge cases
- Verify error handling
- Check dependency versions
- Review file permissions
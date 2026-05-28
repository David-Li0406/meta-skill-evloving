---
type: skill
name: Bug Investigation
description: Systematic bug investigation and root cause analysis
skillSlug: bug-investigation
phases: [E, V]
generated: 2026-01-20
status: filled
scaffoldVersion: "2.0.0"
---

# Bug Investigation Skill

## When to Use

Use this skill when:
- Debugging extraction failures
- Investigating classification errors
- Analyzing search performance issues
- Troubleshooting database problems

## Debugging Workflow

### 1. Reproduce the Issue

- Identify failing PDF or operation
- Reproduce in isolation
- Collect error messages

### 2. Check Extraction Metrics

Use `metrics.py` to check:
- Extraction success rate
- Methods used (pdfplumber vs OCR)
- Error patterns

### 3. Review Logs

- Error messages in console
- Database error logs
- Processing statistics

## Common Bug Patterns

### PDF Extraction Failures

**Symptoms:**
- "Sem texto extraível"
- Empty content in database
- OCR not triggered when needed

**Investigation:**
1. Check if PDF is scanned (images)
2. Verify OCR is installed and working
3. Test extraction manually
4. Check file permissions

### Classification Errors

**Symptoms:**
- Documents classified as "outros"
- Incorrect contract number extraction
- Missing document numbers

**Investigation:**
1. Check filename pattern
2. Test regex patterns
3. Verify classification logic
4. Review expected vs actual output

### Database Issues

**Symptoms:**
- Duplicate key errors
- FTS5 index not updating
- Missing data in results

**Investigation:**
1. Check filepath uniqueness
2. Verify triggers are working
3. Test queries directly
4. Check database schema

### Search Problems

**Symptoms:**
- No results found
- Incorrect results
- Performance issues

**Investigation:**
1. Verify FTS5 index exists
2. Test query syntax
3. Check content was indexed
4. Review filter logic

## Logging and Error Handling

### Error Logging Pattern

```python
try:
    text = extract_text_from_pdf(full_path)
except Exception as e:
    print(f"   ❌ Erro ao processar {file}: {e}")
    # Log error with context
    errors += 1
```

### Debugging Checklist

- [ ] Error message clear and helpful
- [ ] Context information logged
- [ ] Error doesn't crash entire process
- [ ] Metrics track failures

## Test Verification Steps

### For Extraction Bugs

1. Test with sample PDF
2. Verify extraction method used
3. Check text length
4. Validate OCR if used

### For Classification Bugs

1. Test classification function directly
2. Verify regex matches
3. Check fallback logic
4. Compare with expected result

## Bug Fix Examples

### Fix: OCR Not Triggering

**Root Cause:** OCR check happens after text validation

**Fix:** Move OCR check before validation failure

### Fix: Classification Fails

**Root Cause:** Regex doesn't match all patterns

**Fix:** Improve regex or add alternative patterns

# Advanced Patterns (Official Anthropic Guidelines)

## Feedback Loops Pattern

Run validator → fix errors → repeat. This pattern greatly improves output quality.

### Example: Style Guide Compliance (No Code)

```markdown
## Content review process

1. Draft content following STYLE_GUIDE.md
2. Review against checklist:
   - Check terminology consistency
   - Verify examples follow standard format
   - Confirm all required sections present
3. If issues found:
   - Note each issue with section reference
   - Revise content
   - Review checklist again
4. Only proceed when all requirements met
5. Finalize and save
```

### Example: Document Editing (With Code)

```markdown
## Document editing process

1. Make edits to `word/document.xml`
2. **Validate immediately**: `python scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review error message
   - Fix issues in XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

## Plan-Validate-Execute Pattern

For complex tasks, create a plan file, validate it, then execute.

### Why This Pattern Works
- **Catches errors early**: Validation finds problems before changes applied
- **Machine-verifiable**: Scripts provide objective verification
- **Reversible planning**: Iterate on plan without touching originals
- **Clear debugging**: Error messages point to specific problems

### When to Use
- Batch operations
- Destructive changes
- Complex validation rules
- High-stakes operations

### Example: Form Filling

```markdown
## Workflow

1. Analyze form: `python scripts/analyze_form.py input.pdf`
2. **Create plan file**: Generate `changes.json` with field mappings
3. **Validate plan**: `python scripts/validate_plan.py changes.json`
4. If validation fails, fix plan and re-validate
5. **Execute**: `python scripts/fill_form.py input.pdf changes.json output.pdf`
6. Verify output
```

## Template Pattern

Provide templates for output format. Match strictness to needs.

### Strict Template (API responses, data formats)

````markdown
## Report structure

ALWAYS use this exact template structure:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with data
- Finding 2 with data

## Recommendations
1. Specific recommendation
2. Specific recommendation
```
````

### Flexible Template (when adaptation useful)

````markdown
## Report structure

Sensible default format, adapt as needed:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on discovery]

## Recommendations
[Tailor to context]
```
````

## Conditional Workflow Pattern

Guide Claude through decision points:

```markdown
## Document modification workflow

1. Determine modification type:

   **Creating new content?** → Follow "Creation workflow"
   **Editing existing?** → Follow "Editing workflow"

2. Creation workflow:
   - Use docx-js library
   - Build from scratch
   - Export to .docx

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

## Workflow Checklists

For complex tasks, provide a checklist Claude can track:

````markdown
## Research synthesis workflow

Copy and track progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**
Review each document in `sources/`. Note main arguments.

**Step 2: Identify key themes**
Look for patterns. What themes repeat? Where do sources agree/disagree?

[Continue with detailed steps...]
````

## Multi-Model Testing

Test skills with all models you plan to use:

| Model | Consideration |
|-------|---------------|
| **Claude Haiku** | Does skill provide enough guidance? |
| **Claude Sonnet** | Is skill clear and efficient? |
| **Claude Opus** | Does skill avoid over-explaining? |

What works for Opus might need more detail for Haiku.

## Anti-Patterns to Avoid

### Windows-Style Paths
```markdown
# BAD
scripts\helper.py

# GOOD
scripts/helper.py
```

### Too Many Options
```markdown
# BAD - Confusing
"Use pypdf, or pdfplumber, or PyMuPDF, or pdf2image..."

# GOOD - Default with escape hatch
"Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
```

### Time-Sensitive Information
```markdown
# BAD - Will become wrong
"If before August 2025, use old API. After August 2025, use new API."

# GOOD - Use "old patterns" section
## Current method
Use v2 API: `api.example.com/v2/messages`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>
The v1 API used: `api.example.com/v1/messages`
</details>
```

### Voodoo Constants
```python
# BAD - Magic numbers
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?

# GOOD - Documented
# HTTP requests typically complete within 30s
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

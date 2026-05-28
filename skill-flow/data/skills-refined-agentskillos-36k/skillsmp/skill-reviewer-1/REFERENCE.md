# Skill Review Reference

Technical specifications and detailed requirements for reviewing Claude Code Skills.

## Official Quality Checklist

Complete 22-item checklist from Anthropic's official skill authoring best practices guide.

**Source**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices#checklist-for-effective-skills

### Core Quality (10 items)

- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does and when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

### Code and Scripts (8 items)

Only applicable if skill includes scripts or code.

- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values justified)
- [ ] Required packages listed in instructions and verified as available
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths (all forward slashes)
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks

### Testing (4 items)

- [ ] At least three evaluations created
- [ ] Tested with Haiku, Sonnet, and Opus
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated (if applicable)

**Total**: 22 items

## YAML Frontmatter Validation

### Name Field Requirements

**Constraints**:
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain XML tags
- Cannot contain reserved words: "anthropic", "claude"
- Must match directory name

**Recommended**: Use gerund form (verb + -ing)
- ✓ `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`
- ✓ Acceptable: `pdf-processing`, `spreadsheet-analysis`
- ✗ Avoid: `helper`, `utils`, `tools`

### Description Field Requirements

**Constraints**:
- Must be non-empty
- Maximum 1024 characters
- Cannot contain XML tags
- Must describe what the Skill does AND when to use it
- Must use third person voice

**Good Example**:
> "Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

**Why it's good**:
- Specific capabilities: extract, fill, merge
- File types named: PDF
- When clause: "Use when..."
- Third person: "Extract" not "I extract"
- Key discovery terms: PDF, text, tables, forms, documents

**Bad Example**:
> "Helps with documents"

**Why it's bad**:
- Too generic
- No when clause
- Vague verb "helps"
- No specific capabilities

### Allowed-Tools Field

Optional field that restricts tool access. List valid tool names if present.

## SKILL.md Length Guidelines

**Requirement**: Under 500 lines for optimal performance

**If over 500 lines**:
- Move examples to `examples.md`
- Move reference docs to `references/`
- Move detailed API docs to `references/api.md`
- Keep core workflow in SKILL.md
- Use progressive disclosure pattern

**Count command**:
```bash
wc -l SKILL.md
```

## Progressive Disclosure Pattern

**Pattern**: SKILL.md overview → separate files loaded as needed

**Good structure**:
```
skill-name/
├── SKILL.md (<500 lines, core workflow)
├── references/
│   ├── finance.md (loaded when needed)
│   ├── sales.md (loaded when needed)
│   └── api.md (loaded when needed)
├── scripts/
│   └── helper.py (executed, not loaded)
└── assets/
    └── template.md (used in output)
```

**File references must be one level deep**:
- ✓ Good: `SKILL.md` → `reference.md`
- ✗ Too deep: `SKILL.md` → `advanced.md` → `details.md`

**Why**: Claude may partially read nested files with `head -100`, resulting in incomplete information.

## Content Quality Standards

### Time-Sensitive Information

**Avoid**:
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Good approach** (use "old patterns" section):
```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

### Consistent Terminology

**Good - Consistent**:
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad - Inconsistent**:
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

### Concrete Examples

**Good**:
- Show actual code, commands, outputs
- Input → output pairs
- Real file paths and data

**Bad**:
- Abstract descriptions without examples
- "Process the file appropriately"
- "Handle the data as needed"

### Concise Writing

Challenge each paragraph:
- "Does Claude really need this explanation?"
- "Can I assume Claude knows this?"
- "Does this justify its token cost?"

## Workflow Requirements

**Good - Sequential with checklist**:
```markdown
Copy and track progress:
```
Task Progress:
- [ ] Step 1: Analyze form fields
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output
```

**Step 1: Analyze form fields**
Run: `python scripts/analyze.py input.pdf`

**Step 2**: ...
```

**Feedback loops** for quality:
- Run validator → fix errors → repeat
- Only proceed when validation passes

## Script Quality Standards

### Solve, Don't Punt

**Good** (handles errors):
```python
def process_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"File {path} not found, creating default")
        with open(path, 'w') as f:
            f.write('')
        return ''
```

**Bad** (punts to Claude):
```python
def process_file(path):
    return open(path).read()  # Just fails, Claude figures it out
```

### No Voodoo Constants

**Good** (justified):
```python
# HTTP requests typically complete within 30 seconds
REQUEST_TIMEOUT = 30

# Three retries balances reliability vs speed
MAX_RETRIES = 3
```

**Bad** (magic numbers):
```python
TIMEOUT = 47  # Why 47?
RETRIES = 5   # Why 5?
```

### Clear Execution Intent

Distinguish between execute vs read:
- "Run `analyze.py` to extract fields" (execute)
- "See `analyze.py` for algorithm" (read as reference)

### Package Dependencies

- List required packages
- Verify availability in code execution environment
- Include installation commands

## Path Conventions

**Forward slashes only**:
- ✓ `scripts/helper.py`, `references/guide.md`
- ✗ `scripts\helper.py`, `references\guide.md` (Windows-style)

Unix-style paths work everywhere. Windows-style breaks on Unix.

## Testing Requirements

### Evaluation Scenarios

**Requirement**: At least 3 evaluation scenarios

**Example structure**:
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads PDF using appropriate library",
    "Extracts text from all pages",
    "Saves to output.txt in readable format"
  ]
}
```

### Model Testing

**Test with all three**:
- **Haiku** (fast, economical): Enough guidance?
- **Sonnet** (balanced): Clear and efficient?
- **Opus** (powerful): Not over-explaining?

What works for Opus might need more detail for Haiku.

### Real Usage Scenarios

Test with:
- Actual user requests (not just test cases)
- Real files and data
- Complete workflows start to finish
- Edge cases and errors

Observe where Claude:
- Struggles or gets confused
- Misses important steps
- Makes unexpected choices
- Succeeds smoothly

### Team Feedback

If team skill:
- Share with teammates
- Observe their usage
- Ask: Activates when expected? Instructions clear? What's missing?
- Incorporate feedback

## Common Issues and Fixes

### SKILL.md Too Long

**Issue**: Over 500 lines
**Fix**:
- Move examples to separate file
- Move reference docs to `references/`
- Keep core workflow in SKILL.md

### Description Vague

**Issue**: Generic or missing key information
**Fix**:
- Add specific capabilities, file types, domains
- Include when clause
- Use third person
- Add key discovery terms

### References Too Deep

**Issue**: Nested references (SKILL.md → advanced.md → details.md)
**Fix**:
- Keep one level from SKILL.md
- Flatten nested references
- All references should link directly from SKILL.md

### Windows Paths

**Issue**: Backslashes in paths
**Fix**:
- Replace all backslashes with forward slashes
- Test paths work on Unix systems

## Anti-Patterns

### Too Many Options

- ✗ "Use pypdf, or pdfplumber, or PyMuPDF, or pdf2image..."
- ✓ "Use pdfplumber for text extraction. For scanned PDFs needing OCR, use pdf2image with pytesseract."

### Over-Explaining Basics

- ✗ "PDF (Portable Document Format) files are a common format..."
- ✓ "Use pdfplumber for text extraction" (assume Claude knows what PDFs are)

### Vague Workflow

- ✗ "Process the file appropriately"
- ✓ "Read CSV with comma delimiter, convert to JSON array"

### Scripts That Punt

- ✗ `def process(): return open(path).read()` (just fails)
- ✓ Handle FileNotFoundError with helpful message or create default

## MCP Tool References

If skill uses MCP tools, use fully qualified names:

**Format**: `ServerName:tool_name`

**Examples**:
- `BigQuery:bigquery_schema` (not just `bigquery_schema`)
- `GitHub:create_issue` (not just `create_issue`)

## Degree of Freedom

Match specificity to task fragility:

**High freedom** (text instructions): Code reviews, analysis
**Medium freedom** (pseudocode with parameters): Report generation
**Low freedom** (exact scripts): Database migrations, critical operations

## Official References

- Best Practices: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
- Skills Overview: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- Skills Quickstart: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart

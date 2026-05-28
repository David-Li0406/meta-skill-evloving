# Comprehensive Skill Review Checklist

Detailed criteria for reviewing agent skills against best practices.

## Table of Contents

- YAML Frontmatter
- Naming Conventions
- Description Quality
- SKILL.md Body
- Progressive Disclosure
- File Organization
- Reference Files
- Content Quality
- Workflows and Validation
- Anti-Patterns

## YAML Frontmatter

### Name Field

**Requirements**:
- [ ] Maximum 64 characters
- [ ] Lowercase letters, numbers, and hyphens only
- [ ] No XML tags
- [ ] No reserved words ("anthropic", "claude")

**Best Practices**:
- [ ] Uses gerund form (e.g., `processing-pdfs`)
- [ ] Specific and descriptive
- [ ] Not vague (`helper`, `utils`, `tools`)
- [ ] Consistent with other skills

**Examples**:
- ✓ `analyzing-spreadsheets`
- ✓ `managing-databases`
- ✓ `writing-documentation`
- ✗ `helper` (too vague)
- ✗ `anthropic-tools` (reserved word)
- ✗ `PDF_PROCESSOR` (uppercase)

### Description Field

**Requirements**:
- [ ] Non-empty
- [ ] Maximum 1024 characters
- [ ] No XML tags
- [ ] Written in third person (not "I" or "you")

**Best Practices**:
- [ ] Includes WHAT the skill does
- [ ] Includes WHEN to use it
- [ ] Specific with key terms
- [ ] Primary triggering mechanism is clear

**Examples**:

✓ **Good**:
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```
- Clear what it does
- Clear when to use it
- Specific key terms (PDF, forms, extract, merge)

✗ **Bad**:
```yaml
description: Helps with documents
```
- Too vague
- Missing "when to use"
- No specific key terms

✗ **Bad**:
```yaml
description: I can help you process PDF files
```
- Uses first person (should be third person)

## SKILL.md Body

### Size

**Target**:
- [ ] Target ~200 lines, maximum 500 lines
- [ ] If >500: needs refactoring

**When >500 is acceptable**:
- Complex domain with many essential workflows
- After already extracting details to references
- User explicitly requested comprehensive guide in SKILL.md

**When >500 is problematic**:
- Contains detailed examples that could be in references
- Contains comprehensive API docs that could be in references
- Contains multiple domain guides that could be split

### Structure

**Essential elements**:
- [ ] Quick start / basic usage
- [ ] Core workflows
- [ ] References to additional files (if any)

**Writing style**:
- [ ] Uses imperative form ("Run this", "Check that")
- [ ] Not first person ("I recommend")
- [ ] Not second person in instructions ("You should")

**Organization**:
- [ ] Clear section headings
- [ ] Logical flow
- [ ] Easy to scan

## Progressive Disclosure

### Three-Level Loading

**Level 1: Metadata (always loaded)**:
- [ ] Name and description only
- [ ] ~100 tokens or less
- [ ] Clear and specific

**Level 2: SKILL.md body (loaded when triggered)**:
- [ ] Under 5k tokens (roughly <500 lines)
- [ ] Essential instructions only
- [ ] Links to references for details

**Level 3: Resources (loaded as needed)**:
- [ ] Bundled reference files
- [ ] Scripts and assets
- [ ] Only loaded when accessed

### Implementation

**Check**:
- [ ] Detailed content in reference files, not SKILL.md
- [ ] SKILL.md links clearly to references
- [ ] No duplication between SKILL.md and references
- [ ] File organization supports on-demand loading

**Red flags**:
- SKILL.md contains comprehensive API documentation
- SKILL.md contains extensive examples
- SKILL.md contains multiple domain guides
- No reference files despite >400 lines

## File Organization

### Required

- [ ] SKILL.md exists
- [ ] SKILL.md has valid YAML frontmatter
- [ ] SKILL.md has body content

### Optional but Recommended

**references/**:
- [ ] Used for documentation loaded as needed
- [ ] Descriptive file names
- [ ] Table of contents for files >100 lines

**scripts/**:
- [ ] Used for executable code
- [ ] Tested and working
- [ ] Clear purpose

**assets/**:
- [ ] Used for output files (templates, images, fonts)
- [ ] Not loaded into context
- [ ] Properly referenced

### Optional Human-Facing Documentation

**README.md** (optional but recommended):
- [ ] If exists, contains installation instructions for humans
- [ ] Provides overview and usage guidance
- [ ] Clearly separated from SKILL.md (which is AI-facing)

**Should NOT Exist**:
- [ ] No INSTALLATION_GUIDE.md (use README.md instead)
- [ ] No CHANGELOG.md
- [ ] No redundant documentation

**Principle**: SKILL.md is for Claude; README.md is for humans. Avoid duplication.

## Reference Files

### Reference Depth

**One level deep** (from SKILL.md):
- [ ] All references link directly from SKILL.md
- [ ] No references from references

**Examples**:

✓ **Good** (one level):
```
SKILL.md
  → references/feature-a.md
  → references/feature-b.md
  → references/api-docs.md
```

✗ **Bad** (nested):
```
SKILL.md
  → references/advanced.md
    → references/details.md  (too deep!)
```

### File Organization

**Domain-specific**:
- [ ] Organized by domain/feature when appropriate
- [ ] Clear navigation in SKILL.md

**Example**:
```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    ├── product.md
    └── marketing.md
```

When user asks about sales, Claude only loads sales.md.

### File Quality

**For files >100 lines**:
- [ ] Has table of contents at top
- [ ] Clear section headings
- [ ] Easy to navigate

**Naming**:
- [ ] Descriptive (`database-schemas.md` not `doc1.md`)
- [ ] Consistent with content
- [ ] No generic names (`misc.md`, `stuff.md`)

## Content Quality

### Conciseness

**Principle**: Only add what Claude doesn't already know

**Check**:
- [ ] No obvious explanations (what PDFs are, how libraries work)
- [ ] No unnecessary context
- [ ] Each paragraph justifies its token cost

**Good example** (50 tokens):
````markdown
## Extract PDF text

Use pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**Bad example** (150 tokens):
````markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
````

### No Time-Sensitive Information

- [ ] No "before/after [date]" instructions
- [ ] Use "Old patterns" section for deprecated approaches

**Bad**:
```markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

**Good**:
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

**Check**:
- [ ] One term per concept throughout
- [ ] No mixing synonyms unnecessarily

**Good** (consistent):
- Always "API endpoint"
- Always "field"
- Always "extract"

**Bad** (inconsistent):
- Mix "API endpoint", "URL", "API route", "path"
- Mix "field", "box", "element", "control"
- Mix "extract", "pull", "get", "retrieve"

### Concrete Examples

- [ ] Examples are specific, not abstract
- [ ] Input/output pairs when appropriate
- [ ] Real-world scenarios

**Good**:
````markdown
**Example**: Analyzing a sales report
Input: sales_data.xlsx with columns: Date, Region, Revenue
Output: Summary showing total revenue by region
````

**Bad**:
````markdown
**Example**: Process some data and generate output
````

### Clear Workflows

**Multi-step processes**:
- [ ] Numbered steps
- [ ] Clear decision points
- [ ] Conditional logic explained

**Example**:
```markdown
## Workflow

1. Determine task type:
   **Creating new?** → Follow creation workflow
   **Editing existing?** → Follow editing workflow

2. Creation workflow:
   - Step 1
   - Step 2

3. Editing workflow:
   - Step 1
   - Step 2
```

## Anti-Patterns

### Path Format

- [ ] Uses forward slashes (`/`) not backslashes (`\`)
- [ ] Works cross-platform

**Good**: `scripts/helper.py`
**Bad**: `scripts\helper.py`

### Options Overload

- [ ] Provides default with escape hatch
- [ ] Not 5+ alternatives without recommendation

**Good**:
````markdown
Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
````

**Bad**:
```markdown
You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or camelot, or...
```

### Vague Instructions

- [ ] Every instruction is specific and actionable
- [ ] No ambiguous directions

**Good**: "Run `python validate.py input.json` to check field mappings"
**Bad**: "Validate the data somehow"

### Duplication

- [ ] No duplicate information between SKILL.md and references
- [ ] Information lives in one place

**Check**: If same content appears in both SKILL.md and a reference file, one copy should be removed.

### Deeply Nested References

- [ ] All references are one level from SKILL.md
- [ ] No reference-from-reference chains

### Generic File Names

- [ ] Reference files have descriptive names
- [ ] No `doc1.md`, `misc.md`, `stuff.md`

**Good**: `database-schemas.md`, `api-authentication.md`
**Bad**: `file1.md`, `other.md`

## Workflows and Validation

### Workflow Design

**Multi-step workflows**:
- [ ] Complex processes broken into clear sequential steps
- [ ] Each step is actionable and specific
- [ ] Decision points clearly indicated

**Workflow checklists**:
- [ ] Complex workflows (>3 steps) include copy-paste checklist
- [ ] Checklist items match workflow steps
- [ ] Makes progress tracking easy

**Example** (good workflow with checklist):
````markdown
Copy this checklist:
```
- [ ] Step 1: Analyze form
- [ ] Step 2: Create plan
- [ ] Step 3: Validate plan
- [ ] Step 4: Execute
```

**Step 1: Analyze form**
Run: `python scripts/analyze.py input.pdf`
````

### Validation Patterns

Check if skill implements validation appropriately for its task type:

**Plan-Validate-Execute pattern**:
- [ ] Used for batch operations or destructive changes (if applicable)
- [ ] Creates intermediate plan file (JSON/YAML/CSV)
- [ ] Validates plan before execution
- [ ] Clear workflow: analyze → create plan → validate → execute → verify

**Validate script pattern**:
- [ ] Used for structured data editing (if applicable)
- [ ] Validates after each significant change
- [ ] Clear instructions to not proceed if validation fails
- [ ] Validation runs before final output

**Feedback loop pattern**:
- [ ] Used for iterative quality improvement (if applicable)
- [ ] Clear loop: execute → validate → fix → repeat
- [ ] Exit criteria specified (when to stop iterating)

**When validation should be used**:
- Batch operations (>10 items)
- Destructive changes (deletes, overwrites)
- Structured data editing (XML, JSON, config files)
- Format compliance requirements
- High error cost operations

**Red flags** (missing validation when it should exist):
- Batch operations without plan file
- XML/JSON editing without validation step
- Database migrations without verification
- Complex workflows with no validation steps

### Validation Scripts

**If scripts/ directory exists**:
- [ ] Validation scripts named clearly (e.g., `validate.py`, `verify_output.py`)
- [ ] Scripts referenced in workflow at appropriate points
- [ ] Script usage explained with exact commands

**Script quality**:
- [ ] Error messages are specific and actionable
- [ ] Shows what's wrong and how to fix it
- [ ] Lists available options when field/value not found

**Good validation script output**:
```
VALIDATION FAILED:
  - Field 'signature_date' not found. Available fields: customer_name, order_total, signature_date_signed
  - Line 15: order_total must be numeric, got 'invalid'
```

**Bad validation script output**:
```
Error: validation failed
```

### Workflow Recovery

**Error handling**:
- [ ] Workflows explain what to do if validation fails
- [ ] Clear recovery steps provided
- [ ] Reference to troubleshooting guide (if complex)

**Example** (good recovery):
```markdown
If validation fails:
1. Read the error message carefully - it shows the exact problem
2. Edit the plan file to fix the issue
3. Run validation again
4. Repeat until validation passes
5. Only then proceed to next step
```

**Bad recovery**:
```markdown
If validation fails, fix it and try again.
```

### Validation Appropriateness

**Check if validation level matches task risk**:

**High-risk tasks** (should have validation):
- Database operations
- Batch file updates
- Production deployments
- Data migrations
- Document structure editing (OOXML, etc.)

**Medium-risk tasks** (consider validation):
- Report generation
- Code generation
- API integrations
- Configuration changes

**Low-risk tasks** (validation optional):
- Simple data queries
- Read-only operations
- Single file edits
- Exploratory analysis

**Red flags**:
- High-risk task with no validation
- Trivial task with complex validation (over-engineering)
- Validation exists but workflow doesn't enforce it

## Degrees of Freedom

### Appropriate for Task

**High freedom** (text-based guidance):
- Multiple approaches valid
- Context-dependent decisions
- Examples: code review, content writing

**Medium freedom** (templates + parameters):
- Preferred pattern exists
- Some variation acceptable
- Examples: report generation, API integration

**Low freedom** (exact scripts):
- Fragile operations
- Consistency critical
- Examples: database migrations, deployments

**Check**:
- [ ] Freedom level matches task characteristics
- [ ] Not too rigid for creative tasks
- [ ] Not too loose for critical operations

## Overall Assessment

After reviewing all criteria, provide:

**Strengths**:
- What does the skill do well?
- What best practices does it follow?

**Weaknesses**:
- What are the main issues?
- What best practices does it violate?

**Priority Actions**:
1. Most critical fix
2. Next critical fix
3. Important improvement

**Overall Rating**:
- ✓ **Good**: Follows best practices, minor issues only
- ⚠ **Needs Work**: Some significant issues, but functional
- ✗ **Major Issues**: Multiple critical problems, needs substantial revision

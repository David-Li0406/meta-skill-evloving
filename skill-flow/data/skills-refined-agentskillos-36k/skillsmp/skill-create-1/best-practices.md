# Skill Best Practices

Adapted from [Anthropic Skill Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).

## Core Principles

### Concise is Key

The context window is shared. Skills compete with system prompt, conversation history, other skills' metadata, and the user request.

**Default assumption:** Claude is already very smart. Only add context Claude doesn't have.

Challenge each piece of information:
- "Does Claude really need this explanation?"
- "Does this paragraph justify its token cost?"

**Good** (~50 tokens):
```markdown
## Extract PDF text
Use pdfplumber:
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

**Bad** (~150 tokens):
```markdown
## Extract PDF text
PDF files are a common format containing text and images.
To extract text, you'll need a library. We recommend pdfplumber
because it's easy to use. First install it with pip...
```

### Degrees of Freedom

Match specificity to task fragility:

| Level | When to Use | Example |
|-------|-------------|---------|
| **High** | Multiple valid approaches, context-dependent | Code review guidelines |
| **Medium** | Preferred pattern exists, some variation OK | Script with parameters |
| **Low** | Fragile operations, consistency critical | Exact migration command |

**Analogy:** Narrow bridge with cliffs = low freedom. Open field = high freedom.

### Test with Target Models

Skills effectiveness depends on the underlying model:

- **Haiku** (fast): Does the skill provide enough guidance?
- **Sonnet** (balanced): Is the skill clear and efficient?
- **Opus** (powerful): Does the skill avoid over-explaining?

---

## Structure

### Naming Conventions

**Pattern:** `<namespace>[-<subnamespace>]-<action>`

| Valid | Invalid |
|-------|---------|
| `code-debug` | `helper` (vague) |
| `spec-create` | `utils` (generic) |
| `git-worktree-use` | `claude-tools` (reserved) |

**Rules:**
- Lowercase letters, numbers, hyphens only
- Max 64 characters
- No reserved words: "anthropic", "claude"

### Writing Descriptions

The description enables skill discovery. Include what it does AND when to use it.

**Format:** Third person, max 1024 characters.

**Good:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**Bad:**
```yaml
description: Helps with documents
```

### Progressive Disclosure

Skills use three-level loading:

1. **Metadata** (name + description) - Always in context
2. **SKILL.md body** - When skill triggers
3. **Bundled resources** - As needed by Claude

**Keep SKILL.md under 500 lines.** Split content when approaching this limit.

**Pattern 1: High-level guide with references**
```markdown
# PDF Processing

## Quick start
[minimal example]

## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Pattern 3: Conditional details**
```markdown
## Creating documents
Use docx-js. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [REDLINING.md](REDLINING.md)
```

**Guidelines:**
- Keep references one level deep from SKILL.md
- Add table of contents to files over 100 lines

---

## Workflows and Feedback Loops

### Use Workflows for Complex Tasks

Break complex operations into clear, sequential steps with a checklist:

```markdown
## Form filling workflow

Task Progress:
- [ ] Step 1: Analyze form (run analyze_form.py)
- [ ] Step 2: Create field mapping
- [ ] Step 3: Validate mapping
- [ ] Step 4: Fill form
- [ ] Step 5: Verify output

**Step 1: Analyze the form**
Run: `python scripts/analyze_form.py input.pdf`
...
```

### Implement Feedback Loops

**Pattern:** Run validator → fix errors → repeat

```markdown
## Document editing

1. Make edits to document.xml
2. **Validate immediately**: `python scripts/validate.py`
3. If validation fails:
   - Review error message
   - Fix issues
   - Validate again
4. **Only proceed when validation passes**
5. Rebuild document
```

---

## Content Guidelines

### Avoid Time-Sensitive Information

**Bad:**
```markdown
If before August 2025, use old API. After, use new API.
```

**Good:**
```markdown
## Current method
Use v2 API endpoint.

## Old patterns
<details>
<summary>Legacy v1 API (deprecated)</summary>
...
</details>
```

### Use Consistent Terminology

Choose one term, use it throughout:

| Consistent | Inconsistent |
|------------|--------------|
| Always "API endpoint" | Mix "endpoint", "URL", "route" |
| Always "field" | Mix "field", "box", "element" |

---

## Common Patterns

### Template Pattern

Provide templates for output format:

**Strict requirements:**
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Flexible guidance:**
```markdown
## Report structure
Sensible default, adjust as needed:
...
```

### Examples Pattern

For quality-dependent output, provide input/output pairs:

```markdown
## Commit message format

**Example 1:**
Input: Added user authentication with JWT
Output:
feat(auth): implement JWT-based authentication
Add login endpoint and token validation middleware
```

### Conditional Workflow Pattern

Guide through decision points:

```markdown
## Document modification

1. Determine type:
   **Creating new?** → Follow creation workflow
   **Editing existing?** → Follow editing workflow

2. Creation workflow: ...
3. Editing workflow: ...
```

---

## Evaluation and Iteration

### Build Evaluations First

Create evaluations BEFORE writing extensive documentation. This ensures your skill solves real problems.

**Evaluation-driven development:**
1. **Identify gaps**: Run Claude on tasks without a skill. Document failures
2. **Create evaluations**: Build 3 scenarios testing these gaps
3. **Establish baseline**: Measure performance without the skill
4. **Write minimal instructions**: Just enough to pass evaluations
5. **Iterate**: Execute, compare, refine

**Evaluation structure:**
```json
{
  "skills": ["pdf-processing"],
  "query": "Extract text from this PDF and save to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Reads PDF using appropriate library",
    "Extracts text from all pages",
    "Saves to output.txt in readable format"
  ]
}
```

### Develop Iteratively with Claude

Use two Claude instances:
- **Claude A**: Creates and refines the skill
- **Claude B**: Tests the skill on real tasks

**Creating a new skill:**

1. **Complete task without skill**: Work through problem with Claude A. Notice what context you repeatedly provide
2. **Identify reusable pattern**: What would help similar future tasks?
3. **Ask Claude A to create skill**: "Create a skill capturing this pattern"
4. **Review for conciseness**: Remove unnecessary explanations
5. **Improve architecture**: Split into reference files as needed
6. **Test with Claude B**: Fresh instance with skill loaded
7. **Iterate**: If Claude B struggles, return to Claude A with specifics

**Iterating on existing skills:**

1. Use skill in real workflows with Claude B
2. Observe: Where does it struggle? Succeed? Make unexpected choices?
3. Return to Claude A: "Claude B forgot to filter test accounts. The skill mentions it but maybe not prominently enough?"
4. Apply refinements, test again
5. Repeat based on usage

### Observe How Claude Navigates

Watch for:
- **Unexpected exploration paths**: Structure may not be intuitive
- **Missed connections**: Links need to be more explicit
- **Overreliance on sections**: Content should be in SKILL.md instead
- **Ignored content**: File may be unnecessary or poorly signaled

The `name` and `description` are critical for triggering. Make sure they clearly describe what the skill does and when to use it.

---

## Scripts and Code

### Solve, Don't Punt

Handle errors explicitly:

**Good:**
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

**Bad:**
```python
def process_file(path):
    return open(path).read()  # Let Claude figure it out
```

### Provide Utility Scripts

Pre-made scripts offer:
- More reliable than generated code
- Save tokens (no code in context)
- Ensure consistency

**Document clearly:**
```markdown
## Utility scripts

**analyze_form.py**: Extract form fields
python scripts/analyze_form.py input.pdf > fields.json

**validate.py**: Check for conflicts
python scripts/validate.py fields.json
```

### Use Visual Analysis

When inputs can be rendered as images, have Claude analyze them:

```markdown
## Form layout analysis

1. Convert PDF to images:
   python scripts/pdf_to_images.py form.pdf

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
```

### Create Verifiable Intermediate Outputs

For complex tasks, use plan-validate-execute pattern:

1. **Analyze** → Create plan file (e.g., `changes.json`)
2. **Validate** → Run validation script on plan
3. **Execute** → Apply changes only after validation passes
4. **Verify** → Confirm results

**Benefits:**
- Catches errors before changes applied
- Machine-verifiable with scripts
- Reversible planning (iterate without touching originals)
- Clear debugging with specific error messages

**When to use:** Batch operations, destructive changes, complex validation, high-stakes operations.

### Package Dependencies

Platform-specific limitations:
- **claude.ai**: Can install from npm/PyPI, pull from GitHub
- **Anthropic API**: No network access, no runtime installation

List required packages in SKILL.md.

### MCP Tool References

Use fully qualified names: `ServerName:tool_name`

```markdown
Use BigQuery:bigquery_schema to retrieve schemas.
Use GitHub:create_issue to create issues.
```

### Avoid Assuming Tools Installed

**Bad:** "Use the pdf library to process the file."

**Good:**
```markdown
Install: `pip install pypdf`
Then:
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```

---

## Checklist

### Core Quality
- [ ] Description includes what AND when
- [ ] SKILL.md under 500 lines
- [ ] Additional details in separate files
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] References one level deep
- [ ] Clear workflow steps

### Code and Scripts
- [ ] Scripts handle errors explicitly
- [ ] No magic constants (all values justified)
- [ ] Required packages documented
- [ ] Forward slashes in paths (no Windows-style)
- [ ] Validation steps for critical operations
- [ ] Feedback loops for quality tasks

### Testing
- [ ] Tested with target models
- [ ] Tested with real usage scenarios

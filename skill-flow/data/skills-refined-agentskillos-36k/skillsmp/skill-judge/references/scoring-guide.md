# Scoring Guide

Detailed scoring guidance with examples and common pitfalls.

## Scoring Philosophy

### The Golden Rule

**Score based on VALUE, not VOLUME.**

A 43-line skill that provides pure expert knowledge deserves a higher score than a 500-line skill that's 80% redundant.

### Scoring Mindset

When scoring, ask yourself:
1. **What is the knowledge delta?** (How much does Claude NOT know?)
2. **Is this actionable?** (Can Agent use it immediately?)
3. **Is this tested?** (Will this actually work in practice?)
4. **Is this necessary?** (Or could Claude figure this out?)

### Common Scoring Biases to Avoid

| Bias | Why It's Wrong | Correct Approach |
|------|----------------|------------------|
| Length bias | Longer ≠ better | Score based on content quality, not word count |
| Formatting bias | Pretty ≠ valuable | Focus on substance, not presentation |
| Completeness bias | More ≠ better | Score based on necessity, not comprehensiveness |
| Generosity bias | "They tried hard" ≠ good | Score objectively against criteria |
| Harshness bias | Perfect ≠ only passing | Recognize good work, not just perfect work |

---

## Dimension-by-Dimension Scoring Guide

### D1: Knowledge Delta (20 points)

#### How to Score

1. Read through the skill section by section
2. For each section, mark as Expert (E), Activation (A), or Redundant (R)
3. Calculate ratio: E:A:R
4. Assign score based on ratio

#### Score Ranges

| Score | E:A:R Ratio | Characteristics |
|-------|-------------|-----------------|
| 0-5 | E < 40%, R > 30% | Mostly basics, tutorials, obvious content |
| 6-10 | E 40-70%, A high | Mixed value, diluted by obvious content |
| 11-15 | E > 70%, A < 20%, R < 10% | Mostly expert, minimal redundancy |
| 16-20 | E > 90%, R ≈ 0% | Pure knowledge delta, every paragraph earns tokens |

#### Scoring Examples

**Example 1: Score 3/20**

```markdown
## What is a PDF?

PDF (Portable Document Format) is a file format developed by Adobe in 1993.
It preserves document formatting across different platforms and devices...

## How to Read a PDF

Step 1: Open the file using a PDF reader
Step 2: Navigate to the desired page
Step 3: Read the content
Step 4: Extract text if needed using appropriate tools

## PDF Libraries

There are several libraries for working with PDFs:
- PyPDF2: A popular Python library
- pdfplumber: Good for extracting tables
- PyMuPDF: Fast and feature-rich
```

**Analysis**:
- E: 0% (nothing Claude doesn't know)
- A: 10% (library names)
- R: 90% (what is PDF, how to read, basic concepts)
- **Score: 3/20**

---

**Example 2: Score 18/20**

```markdown
## PDF Text Extraction Strategy

| Scenario | Primary Tool | Fallback | Why |
|----------|-------------|----------|-----|
| Standard PDF | pdftotext | PyMuPDF | pdftotext is 10x faster |
| Scanned PDF | OCR first | - | pdftotext returns blank |
| Encrypted PDF | PyMuPDF with password | - | pdftotext fails silently |

**CRITICAL**: Always check if PDF is scanned before extraction.
Scanned PDFs return empty text from pdftotext - this is NOT an error,
it's expected behavior. Use OCR instead.

## Table Extraction Trade-offs

| Library | Speed | Accuracy | Edge Cases |
|---------|-------|----------|------------|
| camelot-py | Slow | High | Fails on complex borders |
| tabula-py | Fast | Medium | Struggles with merged cells |
| pdfplumber | Medium | High | Good for complex layouts |

**Recommendation**: Start with camelot-py for accuracy. If it fails
(timeout or border issues), fall back to tabula-py.
```

**Analysis**:
- E: 90% (decision trees, trade-offs, critical warnings)
- A: 10% (library names)
- R: 0%
- **Score: 18/20**

---

### D2: Mindset + Procedures (15 points)

#### How to Score

1. Identify thinking patterns (guides decision-making)
2. Identify domain-specific procedures (Claude wouldn't know)
3. Identify generic procedures (Claude already knows)
4. Score based on balance and value

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-3 | Only generic procedures (open, read, write, save) |
| 4-7 | Has domain procedures but no thinking frameworks |
| 8-11 | Good balance of thinking + domain procedures |
| 12-15 | Expert-level thinking + procedures Claude wouldn't know |

#### Scoring Examples

**Example 1: Score 2/15**

```markdown
## How to Create a Document

1. Create a new file
2. Add content to the file
3. Save the file
4. Test that it works

## How to Edit a Document

1. Open the file
2. Find the section to edit
3. Make the changes
4. Save the file
```

**Analysis**:
- Thinking patterns: 0% (no guidance on what to think about)
- Domain procedures: 0% (all generic)
- Generic procedures: 100%
- **Score: 2/15**

---

**Example 2: Score 14/15**

```markdown
## Document Creation Philosophy

Before creating any document, ask:
- **Who is this for?** (audience determines tone and structure)
- **What's the core message?** (everything else supports this)
- **What format works best?** (report, memo, presentation, etc.)

## OOXML Document Workflow

**CRITICAL ORDER**: Follow this sequence exactly:
1. **Create structure** using docx-js (never start with blank file)
2. **Add content** in logical order (headers before paragraphs)
3. **Apply styles** (never use inline formatting)
4. **Validate** before saving (check for broken references)

**Why this order matters**: OOXML has hidden dependencies.
If you add content before structure, references break silently.
If you use inline formatting, styles won't cascade correctly.

## Validation Checklist

Before saving, verify:
- [ ] All styles are defined in styles.xml
- [ ] No inline formatting in document.xml
- [ ] All images have proper relationships
- [ ] Document.xml is well-formed XML
```

**Analysis**:
- Thinking patterns: 50% (philosophy questions)
- Domain procedures: 50% (OOXML workflow, validation)
- Generic procedures: 0%
- **Score: 14/15**

---

### D3: Anti-Pattern Quality (15 points)

#### How to Score

1. Look for NEVER lists or anti-patterns
2. Check if they're specific (not generic)
3. Check if they include WHY (reasoning)
4. Score based on specificity and reasoning

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY |

#### Scoring Examples

**Example 1: Score 2/15**

```markdown
## Common Mistakes

- Make sure to handle errors properly
- Don't forget to test your code
- Be careful with edge cases
- Consider performance
```

**Analysis**:
- Specific: 0% (all generic)
- Reasoning: 0% (no WHY)
- **Score: 2/15**

---

**Example 2: Score 14/15**

```markdown
## NEVER Do These

**Layout Mistakes**
- NEVER use purple gradients on white backgrounds — this is the #1 sign of AI-generated content
- NEVER use Inter, Roboto, or Arial as primary fonts — they're overused and generic
- NEVER apply border-radius to everything — it looks like default Tailwind

**Technical Mistakes**
- NEVER modify OOXML files directly without validation — one wrong byte corrupts the entire file
- NEVER skip the checksum step when packing PDFs — the file will appear valid but fail silently
- NEVER use inline formatting in documents — it breaks style cascading and makes maintenance impossible

**Why these matter**: These aren't just "bad practices" — they're
specific landmines that experts have learned to avoid through painful experience.
```

**Analysis**:
- Specific: 100% (very specific anti-patterns)
- Reasoning: 100% (includes WHY for each)
- **Score: 14/15**

---

### D4: Specification Compliance - Description (15 points)

#### How to Score

1. Check frontmatter exists and is valid
2. Evaluate description for WHAT, WHEN, KEYWORDS
3. Score based on completeness and specificity

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague/incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: WHAT + WHEN + KEYWORDS |

#### Scoring Examples

**Example 1: Score 4/15**

```yaml
---
name: my-skill
description: "处理文档相关功能"
---
```

**Analysis**:
- Frontmatter: Valid
- WHAT: Vague ("文档相关功能" - what specifically?)
- WHEN: Missing
- KEYWORDS: Missing
- **Score: 4/15**

---

**Example 2: Score 12/15**

```yaml
---
name: docx-processor
description: "Process and edit Microsoft Word documents (.docx files).
Supports creating, modifying, and analyzing documents with proper
formatting preservation."
---
```

**Analysis**:
- Frontmatter: Valid
- WHAT: Good (process, edit, create, modify, analyze)
- WHEN: Weak (no explicit "when to use")
- KEYWORDS: Good (.docx files, Microsoft Word)
- **Score: 12/15**

---

**Example 3: Score 15/15**

```yaml
---
name: docx-processor
description: "Comprehensive document creation, editing, and analysis with support
for tracked changes, comments, formatting preservation, and text extraction.
When Claude needs to work with professional documents (.docx files) for:
(1) Creating new documents, (2) Modifying or editing content,
(3) Working with tracked changes, (4) Adding comments, or any other document tasks"
---
```

**Analysis**:
- Frontmatter: Valid
- WHAT: Excellent (specific capabilities listed)
- WHEN: Excellent (explicit "When Claude needs to...")
- KEYWORDS: Excellent (.docx, tracked changes, professional documents)
- **Score: 15/15**

---

### D5: Progressive Disclosure (15 points)

#### How to Score

1. Check line count (should be <500 for SKILL.md)
2. Check if references directory exists
3. Check loading triggers (MANDATORY, Do NOT Load)
4. Score based on layering quality

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-5 | Everything in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load |
| 11-13 | Good layering with MANDATORY triggers |
| 14-15 | Perfect: decision trees + triggers + "Do NOT Load" |

#### Scoring Examples

**Example 1: Score 3/15**

```markdown
## References

- docx-js.md - for creating documents
- ooxml.md - for editing
- redlining.md - for tracking changes

[800 lines of content in SKILL.md]
```

**Analysis**:
- Line count: 800 (too long)
- References: Listed but no loading guidance
- Triggers: None
- **Score: 3/15**

---

**Example 2: Score 13/15**

```markdown
### Creating New Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`docx-js.md`](docx-js.md) (~500 lines) completely from start to finish.
**NEVER set any range limits when reading this file.**

**Do NOT load** `ooxml.md` or `redlining.md` for this task.

### Editing Existing Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`ooxml.md`](ooxml.md) (~400 lines) completely.

**Do NOT load** `docx-js.md` or `redlining.md` for this task.

[300 lines in SKILL.md]
```

**Analysis**:
- Line count: 300 (appropriate)
- References: Used properly
- Triggers: MANDATORY + "Do NOT Load"
- **Score: 13/15**

---

### D6: Freedom Calibration (15 points)

#### How to Score

1. Identify task type (creative, judgment, fragile)
2. Check if freedom level matches task type
3. Score based on appropriateness

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-5 | Severely mismatched (rigid for creative, vague for fragile) |
| 6-10 | Partially appropriate, some mismatches |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

#### Scoring Examples

**Example 1: Score 4/15**

```markdown
## Frontend Design

**MANDATORY**: Use exactly this HTML structure:
```html
<div class="container">
  <h1>Title</h1>
  <p>Content</p>
</div>
```

Do NOT modify the structure. Use exactly these colors:
- Primary: #3B82F6
- Secondary: #10B981
- Background: #FFFFFF
```

**Analysis**:
- Task type: Creative/design (should have high freedom)
- Freedom level: Low (rigid script)
- Mismatch: Severe
- **Score: 4/15**

---

**Example 2: Score 14/15**

```markdown
## Frontend Design Philosophy

Commit to a BOLD aesthetic direction. Pick an extreme:
- Brutally minimal (black and white, stark typography)
- Maximalist chaos (overlapping elements, vibrant colors)
- Retro-futuristic (neon, gradients, geometric shapes)
- Organic natural (earth tones, soft curves, nature imagery)

**Key principle**: Better to be polarizing than forgettable.
If half the users love it and half hate it, you've succeeded.
If everyone thinks it's "fine", you've failed.
```

**Analysis**:
- Task type: Creative/design (should have high freedom)
- Freedom level: High (guidance, not scripts)
- Match: Perfect
- **Score: 14/15**

---

**Example 3: Score 14/15**

```markdown
## OOXML File Editing

**MANDATORY**: Use exact script in `scripts/edit-docx.py`
Parameters: --file "path/to/file.docx" --operation "add-paragraph"
Do NOT modify the script or use manual editing.

**Why**: OOXML files are fragile. One wrong byte corrupts the entire file.
The script has been tested and validated. Manual editing has 90% failure rate.
```

**Analysis**:
- Task type: Fragile file operation (should have low freedom)
- Freedom level: Low (specific script)
- Match: Perfect
- **Score: 14/15**

---

### D7: Pattern Recognition (10 points)

#### How to Score

1. Identify which pattern the skill follows
2. Check if it matches the task type
3. Check for deviations from the pattern
4. Score based on pattern adherence

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-3 | No recognizable pattern, chaotic structure |
| 4-6 | Partially follows a pattern with significant deviations |
| 7-8 | Clear pattern with minor deviations |
| 9-10 | Masterful application of appropriate pattern |

#### Pattern Reference

| Pattern | ~Lines | Key Characteristics | When to Use |
|---------|--------|---------------------|-------------|
| Mindset | ~50 | Thinking > technique, strong NEVER list | Creative tasks |
| Navigation | ~30 | Minimal SKILL.md, routes to sub-files | Multiple scenarios |
| Philosophy | ~150 | Two-step: Philosophy → Express | Art/creation |
| Process | ~200 | Phased workflow, checkpoints | Complex projects |
| Tool | ~300 | Decision trees, code examples | Precise operations |

#### Scoring Examples

**Example 1: Score 3/10**

```markdown
[600 lines of mixed content]
- Some tutorials
- Some philosophy
- Some procedures
- Some anti-patterns
- No clear structure
```

**Analysis**:
- Pattern: None recognizable
- Structure: Chaotic
- **Score: 3/10**

---

**Example 2: Score 9/10**

```markdown
[50 lines total]

## Design Philosophy

Commit to a BOLD aesthetic direction. Pick an extreme...

## NEVER Do These

- NEVER use purple gradients on white backgrounds...
- NEVER use Inter, Roboto, or Arial...
```

**Analysis**:
- Pattern: Mindset (~50 lines)
- Task type: Creative/design
- Match: Perfect
- **Score: 9/10**

---

**Example 3: Score 9/10**

```markdown
[300 lines total]

## Decision Tree

| Scenario | Approach | Tool |
|----------|----------|------|
| Create document | Use docx-js | scripts/create.py |
| Edit document | Use OOXML | scripts/edit.py |

## Workflow

Step 1: Identify task type
Step 2: Load appropriate reference
Step 3: Execute script
```

**Analysis**:
- Pattern: Tool (~300 lines)
- Task type: Precise operations
- Match: Perfect
- **Score: 9/10**

---

### D8: Practical Usability (15 points)

#### How to Score

1. Check for decision trees
2. Check code examples work
3. Check error handling
4. Check edge cases
5. Score based on completeness

#### Score Ranges

| Score | Characteristics |
|-------|-----------------|
| 0-5 | Confusing, incomplete, contradictory |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive including edge cases |

#### Scoring Examples

**Example 1: Score 4/15**

```markdown
## PDF Processing

Use appropriate tools for PDF processing.
Handle errors properly.
Consider edge cases.

## Code Example

```python
# Process PDF
def process_pdf(file):
    # Add code here
    pass
```
```

**Analysis**:
- Decision trees: None
- Code examples: Pseudocode (won't work)
- Error handling: Generic
- Edge cases: None
- **Score: 4/15**

---

**Example 2: Score 14/15**

```markdown
## PDF Text Extraction

| Scenario | Primary Tool | Fallback | When to Use Fallback |
|----------|-------------|----------|----------------------|
| Standard PDF | pdftotext | PyMuPDF | Need layout info |
| Scanned PDF | OCR first | - | pdftotext returns blank |
| Encrypted PDF | PyMuPDF with password | - | pdftotext fails |

## Code Example

```python
import subprocess
from PyMuPDF import fitz

def extract_text(pdf_path, password=None):
    # Try pdftotext first (10x faster)
    try:
        result = subprocess.run(
            ['pdftotext', pdf_path, '-'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.stdout.strip():
            return result.stdout
    except Exception:
        pass

    # Fallback to PyMuPDF
    doc = fitz.open(pdf_path)
    if password:
        doc.authenticate(password)
    text = '\n'.join(page.get_text() for page in doc)
    doc.close()
    return text
```

## Common Issues

**Issue**: pdftotext returns empty text
**Cause**: PDF is scanned
**Solution**: Use OCR (tesseract) before extraction

**Issue**: Permission error
**Cause**: PDF is encrypted
**Solution**: Use PyMuPDF with password parameter
```

**Analysis**:
- Decision trees: Excellent (scenario table)
- Code examples: Working code with fallbacks
- Error handling: Comprehensive
- Edge cases: Covered (scanned, encrypted)
- **Score: 14/15**

---

## Common Scoring Pitfalls

### Pitfall 1: The "Professional Formatting" Trap

**Mistake**: Giving high scores because the skill looks professional.

**Reality**: Formatting ≠ value. A beautifully formatted skill that explains basics is still a waste of tokens.

**Correct approach**: Ignore formatting. Focus on content quality.

---

### Pitfall 2: The "Length Impresses" Trap

**Mistake**: Thinking longer skills are better.

**Reality**: A 43-line skill with pure expert knowledge > 500-line skill with 80% redundancy.

**Correct approach**: Score based on knowledge density, not word count.

---

### Pitfall 3: The "Helpful Context" Trap

**Mistake**: Forgiving redundant content because "it provides helpful context."

**Reality**: Context window is a shared resource. Every redundant paragraph wastes tokens.

**Correct approach**: Be ruthless. If Claude knows it, delete it.

---

### Pitfall 4: The "They Tried Hard" Trap

**Mistake**: Being generous because the author clearly put in effort.

**Reality**: Effort ≠ quality. Score objectively against criteria.

**Correct approach**: Score based on results, not effort.

---

### Pitfall 5: The "Missing Anti-Patterns" Trap

**Mistake**: Overlooking the absence of NEVER lists.

**Reality**: Half of expert knowledge is knowing what NOT to do. No NEVER list = significant gap.

**Correct approach**: Deduct points for missing anti-patterns.

---

### Pitfall 6: The "Description Doesn't Matter" Trap

**Mistake**: Undervaluing the description field.

**Reality**: Poor description = skill never gets used. It's the MOST IMPORTANT field.

**Correct approach**: Deduct heavily for poor descriptions.

---

## Final Score Calculation

### Grade Assignment

| Score Range | Grade | Interpretation |
|-------------|-------|----------------|
| 96-120 | A | Excellent - Production ready |
| 84-95 | B | Good - Minor improvements needed |
| 72-83 | C | Acceptable - Moderate improvements needed |
| 60-71 | D | Poor - Significant improvements needed |
| <60 | F | Fail - Major redesign required |

### Weighting Considerations

While all dimensions matter, some are more critical:

| Dimension | Weight | Why |
|-----------|--------|-----|
| D1: Knowledge Delta | HIGH | Core value - determines if skill is useful |
| D4: Description | HIGH | Determines if skill gets used at all |
| D3: Anti-Patterns | MEDIUM | Important but can be added later |
| D5: Progressive Disclosure | MEDIUM | Important for complex skills |
| D2, D6, D7, D8 | MEDIUM | Support dimensions |

### Borderline Cases

**Score 83/120 (C vs B)**:
- If D1 (Knowledge Delta) ≥ 16, bump to B
- If D4 (Description) ≥ 14, bump to B
- Otherwise, keep as C

**Score 71/120 (D vs C)**:
- If D1 (Knowledge Delta) ≥ 14, bump to C
- If skill has clear pattern (D7 ≥ 8), bump to C
- Otherwise, keep as D

**Score 59/120 (F vs D)**:
- If description is excellent (D4 = 15), bump to D
- Otherwise, keep as F

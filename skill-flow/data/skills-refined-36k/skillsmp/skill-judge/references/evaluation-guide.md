# Evaluation Guide

Detailed evaluation criteria for each of the 8 dimensions in the Skill Judge framework.

## D1: Knowledge Delta (20 points) - THE CORE DIMENSION

The most important dimension. Does the Skill add genuine expert knowledge?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-5 | Explains basics Claude knows (what is X, how to write code, standard library tutorials) |
| 6-10 | Mixed: some expert knowledge diluted by obvious content |
| 11-15 | Mostly expert knowledge with minimal redundancy |
| 16-20 | Pure knowledge delta — every paragraph earns its tokens |

### Red Flags (Instant Score ≤5)

- "What is [basic concept]" sections
- Step-by-step tutorials for standard operations
- Explaining how to use common libraries
- Generic best practices ("write clean code", "handle errors")
- Definitions of industry-standard terms
- Tutorials for things Claude can figure out from documentation

### Green Flags (Indicators of High Knowledge Delta)

- Decision trees for non-obvious choices ("when X fails, try Y because Z")
- Trade-offs only an expert would know ("A is faster but B handles edge case C")
- Edge cases from real-world experience
- "NEVER do X because [non-obvious reason]"
- Domain-specific thinking frameworks
- Non-obvious ordering or sequencing requirements
- Hidden constraints or gotchas

### Evaluation Questions

1. For each section, ask: "Does Claude already know this?"
2. If explaining something, ask: "Is this explaining TO Claude or FOR Claude?"
3. Count paragraphs that are Expert vs Activation vs Redundant
4. Would an expert read this and say "this is valuable" or "this is obvious"?

### Examples

**Poor Knowledge Delta (Score: 3/20)**
```markdown
## What is a PDF?

PDF (Portable Document Format) is a file format developed by Adobe...
It preserves document formatting across different platforms...
To create a PDF, you can use various tools...

## How to Read a PDF

Step 1: Open the file
Step 2: Read the content
Step 3: Extract text if needed
```

**Excellent Knowledge Delta (Score: 18/20)**
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
```

---

## D2: Mindset + Appropriate Procedures (15 points)

Does the Skill transfer expert **thinking patterns** along with **necessary domain-specific procedures**?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-3 | Only generic procedures Claude already knows |
| 4-7 | Has domain procedures but lacks thinking frameworks |
| 8-11 | Good balance: thinking patterns + domain-specific workflows |
| 12-15 | Expert-level: shapes thinking AND provides procedures Claude wouldn't know |

### Key Distinction

| Type | Example | Value |
|------|---------|-------|
| **Thinking patterns** | "Before designing, ask: What makes this memorable?" | High — shapes decision-making |
| **Domain-specific procedures** | "OOXML workflow: unpack → edit XML → validate → pack" | High — Claude may not know this |
| **Generic procedures** | "Step 1: Open file, Step 2: Edit, Step 3: Save" | Low — Claude already knows |

### Valuable Procedures

- Workflows Claude hasn't been trained on (new tools, proprietary systems)
- Correct ordering that's non-obvious (e.g., "validate BEFORE packing, not after")
- Critical steps that are easy to miss (e.g., "MUST recalculate formulas after editing")
- Domain-specific sequences (e.g., MCP server's 4-phase development process)
- Hidden dependencies or prerequisites

### Redundant Procedures

- Generic file operations (open, read, write, save)
- Standard programming patterns (loops, conditionals, error handling)
- Common library usage that's well-documented
- Obvious sequences that anyone would follow

### Expert Thinking Patterns

Good thinking patterns guide decision-making:

```markdown
Before [action], ask yourself:
- **Purpose**: What problem does this solve? Who uses it?
- **Constraints**: What are the hidden requirements?
- **Differentiation**: What makes this solution memorable?
- **Trade-offs**: What are we giving up?
```

### The Test

1. Does it tell Claude WHAT to think about? (thinking patterns)
2. Does it tell Claude HOW to do things it wouldn't know? (domain procedures)

A good Skill provides both when needed.

### Examples

**Poor (Score: 2/15)**
```markdown
## How to Create a Document

1. Create a new file
2. Add content to the file
3. Save the file
4. Test that it works
```

**Excellent (Score: 14/15)**
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
```

---

## D3: Anti-Pattern Quality (15 points)

Does the Skill have effective NEVER lists?

### Why This Matters

Half of expert knowledge is knowing what NOT to do. A senior designer sees purple gradient on white background and instinctively cringes — "too AI-generated." This intuition for "what absolutely not to do" comes from stepping on countless landmines.

Claude hasn't stepped on these landmines. It doesn't know Inter font is overused, doesn't know purple gradients are the signature of AI-generated content. Good Skills must explicitly state these "absolute don'ts."

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-3 | No anti-patterns mentioned |
| 4-7 | Generic warnings ("avoid errors", "be careful", "consider edge cases") |
| 8-11 | Specific NEVER list with some reasoning |
| 12-15 | Expert-grade anti-patterns with WHY — things only experience teaches |

### Expert Anti-Patterns (Specific + Reason)

```markdown
NEVER use generic AI-generated aesthetics like:
- Overused font families (Inter, Roboto, Arial)
- Cliched color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Default border-radius on everything

**WHY**: These are the hallmarks of AI-generated content. Using them
makes your work look generic and unoriginal.
```

### Weak Anti-Patterns (Vague, No Reasoning)

```markdown
Avoid making mistakes.
Be careful with edge cases.
Don't write bad code.
```

### The Test

Would an expert read the anti-pattern list and say "yes, I learned this the hard way"? Or would they say "this is obvious to everyone"?

### Examples

**Poor (Score: 2/15)**
```markdown
## Common Mistakes to Avoid

- Make sure to handle errors properly
- Don't forget to test your code
- Be careful with edge cases
```

**Excellent (Score: 14/15)**
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

---

## D4: Specification Compliance — Especially Description (15 points)

Does the Skill follow official format requirements? **Special focus on description quality.**

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-5 | Missing frontmatter or invalid format |
| 6-10 | Has frontmatter but description is vague or incomplete |
| 11-13 | Valid frontmatter, description has WHAT but weak on WHEN |
| 14-15 | Perfect: comprehensive description with WHAT, WHEN, and trigger keywords |

### Frontmatter Requirements

- `name`: lowercase, alphanumeric + hyphens only, ≤64 characters
- `description`: **THE MOST CRITICAL FIELD** — determines if skill gets used at all

### Why Description is THE MOST IMPORTANT Field

```
┌─────────────────────────────────────────────────────────────────────┐
│  SKILL ACTIVATION FLOW                                              │
│                                                                     │
│  User Request → Agent sees ALL skill descriptions → Decides which  │
│                 (only descriptions, not bodies!)     to activate    │
│                                                                     │
│  If description doesn't match → Skill NEVER gets loaded            │
│  If description is vague → Skill might not trigger when it should  │
│  If description lacks keywords → Skill is invisible to the Agent   │
└─────────────────────────────────────────────────────────────────────┘
```

**The brutal truth**: A Skill with perfect content but poor description is **useless** — it will never be activated. The description is the **only chance** to tell the Agent "use me in these situations."

### Description Must Answer THREE Questions

1. **WHAT**: What does this Skill do? (functionality)
2. **WHEN**: In what situations should it be used? (trigger scenarios)
3. **KEYWORDS**: What terms should trigger this Skill? (searchable terms)

### Excellent Description (All Three Elements)

```yaml
description: "Comprehensive document creation, editing, and analysis with support
for tracked changes, comments, formatting preservation, and text extraction.
When Claude needs to work with professional documents (.docx files) for:
(1) Creating new documents, (2) Modifying or editing content,
(3) Working with tracked changes, (4) Adding comments, or any other document tasks"
```

**Analysis**:
- WHAT: creation, editing, analysis, tracked changes, comments
- WHEN: "When Claude needs to work with... for: (1)... (2)... (3)..."
- KEYWORDS: .docx files, tracked changes, professional documents

### Poor Description (Missing Elements)

```yaml
description: "处理文档相关功能"
```

**Problems**:
- WHAT: vague ("文档相关功能" — what specifically?)
- WHEN: missing (when should Agent use this?)
- KEYWORDS: missing (no ".docx", no specific scenarios)

### Another Poor Example

```yaml
description: "A helpful skill for various tasks"
```

This is useless — Agent has no idea when to activate it.

### Description Quality Checklist

- [ ] Lists specific capabilities (not just "helps with X")
- [ ] Includes explicit trigger scenarios ("Use when...", "When user asks for...")
- [ ] Contains searchable keywords (file extensions, domain terms, action verbs)
- [ ] Specific enough that Agent knows EXACTLY when to use it
- [ ] Includes scenarios where this skill MUST be used (not just "can be used")

---

## D5: Progressive Disclosure (15 points)

Does the Skill implement proper content layering?

### Skill Loading Layers

```
Layer 1: Metadata (always in memory)
         Only name + description
         ~100 tokens per skill

Layer 2: SKILL.md Body (loaded after triggering)
         Detailed guidelines, code examples, decision trees
         Ideal: < 500 lines

Layer 3: Resources (loaded on demand)
         scripts/, references/, assets/
         No limit
```

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-5 | Everything dumped in SKILL.md (>500 lines, no structure) |
| 6-10 | Has references but unclear when to load them |
| 11-13 | Good layering with MANDATORY triggers present |
| 14-15 | Perfect: decision trees + explicit triggers + "Do NOT Load" guidance |

### Loading Trigger Quality (For Skills WITH references)

| Trigger Quality | Characteristics |
|-----------------|-----------------|
| Poor | References listed at end, no loading guidance |
| Mediocre | Some triggers but not embedded in workflow |
| Good | MANDATORY triggers in workflow steps |
| Excellent | Scenario detection + conditional triggers + "Do NOT Load" |

### The Loading Problem

```
Loading too little ◄─────────────────────────────────► Loading too much
- References sit unused                    - Wastes context space
- Agent doesn't know when to load          - Irrelevant info dilutes key content
- Knowledge is there but never accessed    - Unnecessary token overhead
```

### Good Loading Trigger (Embedded in Workflow)

```markdown
### Creating New Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`docx-js.md`](docx-js.md) (~500 lines) completely from start to finish.
**NEVER set any range limits when reading this file.**

**Do NOT load** `ooxml.md` or `redlining.md` for this task.
```

### Bad Loading Trigger (Just Listed)

```markdown
## References
- docx-js.md - for creating documents
- ooxml.md - for editing
- redlining.md - for tracking changes
```

### For Simple Skills (No References, <100 Lines)

Score based on conciseness and self-containment.

---

## D6: Freedom Calibration (15 points)

Is the level of specificity appropriate for the task's fragility?

Different tasks need different levels of constraint. This is about matching freedom to fragility.

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-5 | Severely mismatched (rigid scripts for creative tasks, vague for fragile ops) |
| 6-10 | Partially appropriate, some mismatches |
| 11-13 | Good calibration for most scenarios |
| 14-15 | Perfect freedom calibration throughout |

### The Freedom Spectrum

| Task Type | Should Have | Why | Example Skill |
|-----------|-------------|-----|---------------|
| Creative/Design | High freedom | Multiple valid approaches, differentiation is value | frontend-design |
| Code review | Medium freedom | Principles exist but judgment required | code-review |
| File format operations | Low freedom | One wrong byte corrupts file, consistency critical | docx, xlsx, pdf |

### High Freedom (Text-Based Instructions)

```markdown
Commit to a BOLD aesthetic direction. Pick an extreme: brutally minimal,
maximalist chaos, retro-futuristic, organic natural...
```

### Medium Freedom (Pseudocode or Parameterized)

```markdown
Review priority:
1. Security vulnerabilities (must fix)
2. Logic errors (must fix)
3. Performance issues (should fix)
4. Maintainability (optional)
```

### Low Freedom (Specific Scripts, Exact Steps)

```markdown
**MANDATORY**: Use exact script in `scripts/create-doc.py`
Parameters: --title "X" --author "Y"
Do NOT modify the script.
```

### The Test

Ask "if Agent makes a mistake, what's the consequence?"
- High consequence → Low freedom
- Low consequence → High freedom

---

## D7: Pattern Recognition (10 points)

Does the Skill follow an established official pattern?

### The 5 Main Design Patterns

| Pattern | ~Lines | Key Characteristics | Example | When to Use |
|---------|--------|---------------------|---------|-------------|
| **Mindset** | ~50 | Thinking > technique, strong NEVER list, high freedom | frontend-design | Creative tasks requiring taste |
| **Navigation** | ~30 | Minimal SKILL.md, routes to sub-files | internal-comms | Multiple distinct scenarios |
| **Philosophy** | ~150 | Two-step: Philosophy → Express, emphasizes craft | canvas-design | Art/creation requiring originality |
| **Process** | ~200 | Phased workflow, checkpoints, medium freedom | mcp-builder | Complex multi-step projects |
| **Tool** | ~300 | Decision trees, code examples, low freedom | docx, pdf, xlsx | Precise operations on specific formats |

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-3 | No recognizable pattern, chaotic structure |
| 4-6 | Partially follows a pattern with significant deviations |
| 7-8 | Clear pattern with minor deviations |
| 9-10 | Masterful application of appropriate pattern |

### Pattern Selection Guide

| Your Task Characteristics | Recommended Pattern |
|---------------------------|---------------------|
| Needs taste and creativity | Mindset (~50 lines) |
| Needs originality and craft quality | Philosophy (~150 lines) |
| Has multiple distinct sub-scenarios | Navigation (~30 lines) |
| Complex multi-step project | Process (~200 lines) |
| Precise operations on specific format | Tool (~300 lines) |

---

## D8: Practical Usability (15 points)

Can an Agent actually use this Skill effectively?

### Scoring Criteria

| Score | Criteria |
|-------|----------|
| 0-5 | Confusing, incomplete, contradictory, or untested guidance |
| 6-10 | Usable but with noticeable gaps |
| 11-13 | Clear guidance for common cases |
| 14-15 | Comprehensive coverage including edge cases and error handling |

### Check For

- **Decision trees**: For multi-path scenarios, is there clear guidance on which path to take?
- **Code examples**: Do they actually work? Or are they pseudocode that breaks?
- **Error handling**: What if the main approach fails? Are fallbacks provided?
- **Edge cases**: Are unusual but realistic scenarios covered?
- **Actionability**: Can Agent immediately act, or needs to figure things out?

### Good Usability (Decision Tree + Fallback)

```markdown
| Task | Primary Tool | Fallback | When to Use Fallback |
|------|-------------|----------|----------------------|
| Read text | pdftotext | PyMuPDF | Need layout info |
| Extract tables | camelot-py | tabula-py | camelot fails |

**Common issues**:
- Scanned PDF: pdftotext returns blank → Use OCR first
- Encrypted PDF: Permission error → Use PyMuPDF with password
```

### Poor Usability (Vague)

```markdown
Use appropriate tools for PDF processing.
Handle errors properly.
Consider edge cases.
```

### The Test

Can an Agent read this and immediately know exactly what to do, or does it need to figure things out? If it needs to figure things out, that's a usability gap.

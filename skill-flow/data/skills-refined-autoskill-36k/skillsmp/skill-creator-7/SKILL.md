---
name: skill-creator
description: Guide for creating production-ready Agent Skills. Use when creating new skills, improving existing skills, or diagnosing why a skill isn't working effectively. Covers skill quality standards, 5 skill type patterns, progressive disclosure design, loading triggers, and validation checklists.
---

# Skill Creator

## Core Philosophy

### What is a Skill?

**The Common Misconception:** Most people think skills are about **teaching AI how to do something**.

This is wrong.

Claude already knows how to write code, debug, design systems, and work with files. You don't need to teach it these things.

### Skills are Knowledge Externalization

Traditional AI knowledge is locked in model weights:

```
Traditional approach:
Collect data → GPU cluster → Parameter training → Deploy new version
Cost: $10,000 - $1,000,000+
Timeline: Weeks to months
```

Skills change this:

```
Skill approach:
Edit skills/SKILL.md → Save → Takes effect on next trigger
Cost: $0
Timeline: Instant
```

Think of it as a hot-swappable LoRA adapter that requires no training. You edit a Markdown file in natural language, and the model's behavior changes.

**This is a paradigm shift from "training AI" to "educating AI."**

### Tool vs Skill

| Concept | Essence | Function | Examples |
|---------|---------|----------|----------|
| **Tool** | What model **can do** | Execute actions | bash, read_file, write_file, WebSearch |
| **Skill** | What model **knows how to do** | Guide decisions | PDF processing, frontend design, code review |

Tools define capability boundaries. Skills inject knowledge.

**Core Formula:**

```
Good Skill = Expert-exclusive knowledge - Claude's existing knowledge
```

Or:

```
Agent Capability Ceiling = Model Capability + Skill Quality
```

The same Claude model, loading different skills, becomes different experts.

## Six Quality Standards

Every good Skill must meet these standards:

### 1. Token Efficiency

**Every paragraph must justify its token cost.**

Context window is a shared resource. Ask three questions for each paragraph:
- Does Claude really not know this?
- Will deleting it break functionality?
- What value do these 100 tokens provide?

**Bad**: Explaining what PDF is, how CSS flexbox works, Step 1-2-3 tutorials
**Good**: Decision trees, trap lists, edge cases, expert intuitions

### 2. Mental Models Over Mechanical Steps

**Transfer how experts think, not what they do.**

Expert vs novice difference isn't in "can they do it," but in "how they approach it."

**Bad Skill**:
```markdown
## Design Process
Step 1: Understand requirements
Step 2: Create wireframe
Step 3: Choose colors
Step 4: Write HTML
Step 5: Add CSS
```

**Good Skill** (frontend-design style):
```markdown
Before coding, answer these questions:

**Purpose**: What problem does this solve? Who uses it?
**Tone**: Pick an extreme—brutally minimal, maximalist chaos, retro-futuristic
**Differentiation**: What makes this UNFORGETTABLE?

Commit to a direction, then execute precisely.
```

### 3. Anti-Pattern Lists

**Explicitly state what NOT to do.**

Half of expert knowledge is knowing what absolutely fails.

```markdown
## NEVER do these things

- Overused fonts: Inter, Roboto, Arial
- Purple gradients on white backgrounds (AI-generated signature)
- All corners rounded to 8px
- Generic card layouts
- Cookie-cutter designs
```

### 4. Description Triggers

**Description is the primary activation mechanism.** Always in context (~100 tokens).

**Good description**:
```yaml
description: "Comprehensive document creation, editing, and analysis with
support for tracked changes, comments, formatting preservation, and text extraction.
Use when working with .docx files for: (1) Creating new documents,
(2) Modifying content, (3) Working with tracked changes, (4) Adding comments"
```

**Bad description**:
```yaml
description: "Document processing functionality"
```

### 5. Freedom Calibration

**Match specificity to task fragility:**

| Task Type | Freedom Level | Approach | Example Skills |
|-----------|--------------|----------|----------------|
| Creative design | HIGH | Principles over steps | frontend-design, canvas-design |
| Code review | MEDIUM | Guidelines with judgment | code-review |
| File format operations | LOW | Precise scripts, few parameters | docx, xlsx, pdf |

**Fragile operations** (Word OOXML, PDF parsing) → Low freedom, exact scripts
**Creative tasks** (UI design, art generation) → High freedom, aesthetic direction

### 6. Loading Trigger Design

**For Skills with references: explicitly design when to load what.**

Problem: Agents don't read references, or read too many.

**Solution - MANDATORY Syntax**:
```markdown
### Creating New Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`skills/references/docx-js.md`](skills/references/docx-js.md) (~500 lines) completely.
**NEVER set range limits when reading this file.**
```

**Solution - Conditional Routing**:
```markdown
| Task Type | Must Load | Do NOT Load |
|-----------|-----------|-------------|
| New document | `docx-js.md` | `ooxml.md`, `redlining.md` |
| Simple edits | `ooxml.md` | `docx-js.md` |
| Tracked changes | `redlining.md` | `docx-js.md` |
```

## Five Skill Type Patterns

### Type 1: Minimal Mindset (30-50 lines)

**Representative**: frontend-design (43 lines)

**Characteristics**:
- No technical details, transfers thinking patterns
- All content in skills/SKILL.md
- No references directory
- Emphasizes taste, differentiation, anti-patterns

**Empowerment**: Transforms generic agent (that writes cookie-cutter UI) into **designer agent with aesthetic taste**.

This agent asks key questions before writing code: What problem does this solve? Who uses it? What makes it unforgettable? It actively avoids "AI-generated" aesthetics.

**Best for**:
- Creative tasks requiring taste
- Differentiation comes from "how to think" not "what to know"
- No domain-specific knowledge needed

**No loading triggers needed** - load entire skills/SKILL.md at once.

---

### Type 2: Tool Operation (200-500 lines)

**Representative**: docx (197 lines), xlsx, pdf

**Characteristics**:
- Decision tree routes to correct workflow
- MANDATORY forced loading instructions
- Detailed code examples
- Large reference docs (300-600 lines each)
- Low freedom, precise steps

**Empowerment**: Transforms generic agent (that might corrupt documents) into **expert at precise file format operations**.

This agent knows: create new docs with docx-js, edit existing with OOXML direct manipulation, handle tracked changes with redlining workflow. It knows exact steps and won't break files.

**Best for**:
- File format operations
- Fragile operations requiring precision
- Heavy domain-specific knowledge

**Carefully designed loading triggers** - Decision tree by task type, forced loading before each workflow.

---

### Type 3: Process-Oriented (150-300 lines)

**Representative**: mcp-builder (237 lines)

**Characteristics**:
- Clear multi-stage workflow (e.g., four phases)
- Each stage has specific outputs and checkpoints
- References organized by stage/choice
- Medium freedom

**Empowerment**: Transforms generic agent (that might miss steps) into **systematic project builder**.

This agent knows building MCP servers requires: research → implementation → testing → evaluation. Each phase has clear deliverables and entry/exit criteria.

**Best for**:
- Complex multi-step tasks
- Requires stage checkpoints
- Multiple technical choices (TypeScript vs Python)

**Stage-by-stage loading triggers** - Load corresponding reference docs when entering each stage.

---

### Type 4: Philosophy + Execution (100-150 lines)

**Representative**: canvas-design (130 lines), algorithmic-art

**Characteristics**:
- Two-step flow: Philosophy (create concept) → Express (execute)
- Emphasizes craftsmanship and master-level execution
- Allows creative space
- References are inspirational examples, not required

**Empowerment**: Transforms generic agent (that outputs mediocre work) into **artist with creative philosophy**.

This agent doesn't start creating immediately. It first establishes a design philosophy—"Brutalist Joy" or "Chromatic Silence"—then uses that philosophy to guide visual expression. It pursues "looks like it took countless hours of careful crafting" quality.

**Best for**:
- Creative generation tasks
- Requires uniqueness and originality
- Quality over efficiency

**Optional loading triggers** - Core workflow self-contained, references are optional examples.

---

### Type 5: Navigation Router (20-50 lines)

**Representative**: internal-comms (33 lines)

**Characteristics**:
- skills/SKILL.md is minimalist, just a router
- Detailed content in skills/examples/ subdirectory
- Quick scenario identification, routes to corresponding file

**Structure**:
```markdown
## How to use this skill

1. **Identify the communication type** from the request
2. **Load the appropriate guideline file**:
   - `examples/3p-updates.md` - Progress/plan/problem updates
   - `examples/company-newsletter.md` - Company newsletters
   - `examples/faq-answers.md` - FAQ responses
3. **Follow the specific instructions** in that file
```

**Empowerment**: Transforms generic agent into **multi-scenario specialist**.

When user asks "help me write weekly report", agent identifies this as 3P update, loads corresponding guide, and follows company format/style.

**Best for**:
- Multiple distinct scenarios
- Each scenario has detailed independent guides
- Don't need to load all scenarios simultaneously

**Simple routing triggers** - Identify scenario type, load corresponding file.

---

### Type Selection Guide

| Your Task Characteristics | Recommended Type | Lines | Need Loading Triggers |
|---------------------------|------------------|-------|----------------------|
| Needs taste and creativity | Minimal Mindset | 30-50 | No |
| Needs uniqueness and craftsmanship | Philosophy + Execution | 100-150 | Optional |
| Multiple scenarios to distribute | Navigation Router | 20-50 | Yes (simple) |
| Complex multi-step project | Process-Oriented | 150-300 | Yes |
| Precise format operations | Tool Operation | 200-500 | Yes (carefully designed) |

## Bad vs Good Skill Comparison

### Bad Example: PDF Skill

```markdown
# PDF Processing Skill

## What is PDF

PDF (Portable Document Format) was developed by Adobe in 1993. It maintains
document formatting across platforms...

## PDF Features

1. Cross-platform compatibility
2. Consistent formatting
3. Encryption support
4. Small file size

## How to Read PDF

### Method 1: PyPDF2

Step 1: Install PyPDF2
`pip install PyPDF2`

Step 2: Import library
`from PyPDF2 import PdfReader`

Step 3: Open file
Step 4: Extract text
```

**Problems**:
- Explains basics (Claude already knows)
- Mechanical Step 1-2-3-4
- No decision guidance (when to use which method)
- No anti-patterns
- No edge cases (scanned PDFs, encrypted files)

---

### Good Example: PDF Skill

```markdown
# PDF Processing Decision Tree

Choose tool based on task:

| Task | First Choice | Backup | When to Use Backup |
|------|-------------|--------|-------------------|
| Text extraction | pdftotext | PyMuPDF | Need layout preservation |
| Table extraction | camelot-py | tabula-py | camelot fails |
| Form filling | PyMuPDF | pdftk | Unsupported form types |
| Merge/split | PyMuPDF | pdftk | Batch processing |
| Convert to images | pdf2image | PyMuPDF | Need resolution control |

## Common Traps

**Scanned PDFs**
- Symptom: pdftotext returns blank or garbled text
- Cause: PDF content is image, not text
- Solution: OCR (tesseract) first, then extract

**Encrypted PDFs**
- Symptom: Permission errors on read
- Solution: `PyMuPDF.open(path, password=xxx)` or decrypt with qpdf

**Complex Nested Tables**
- Symptom: camelot extraction is chaotic
- Solution: Consider LLM-assisted parsing, or convert to image + vision model

**Large File Performance**
- PDFs over 100 pages: avoid loading all pages at once
- Use paginated processing: `for page in reader.pages[start:end]`

## Quick Reference

```bash
# Command-line text extraction
pdftotext input.pdf -

# Convert to images (one per page)
pdftoppm -jpeg -r 150 input.pdf output_prefix
```
```

**Why it's good**:
- No basic explanations ("what is PDF")
- Decision-oriented (what tool for what situation)
- Common traps (scanned, encrypted, complex tables)
- Edge cases (large files)
- Actionable (direct commands, not tutorials)

---

### Another Comparison: Creative Skill

**Bad Creative Skill**:
```markdown
# Frontend Design Skill

## Design Principles

1. Maintain consistency
2. Focus on user experience
3. Use appropriate colors
4. Choose readable fonts
5. Implement responsive design

## Design Process

Step 1: Understand requirements
Step 2: Create wireframe
Step 3: Choose color scheme
Step 4: Write HTML structure
Step 5: Add CSS styles
Step 6: Implement responsive
Step 7: Test and optimize
```

**Problems**: All fluff. Claude already knows "consistency," "UX," "responsive."

---

**Good Creative Skill** (frontend-design style):
```markdown
# Design Thinking

Before writing code, answer these questions:

**Purpose**: What problem does this solve? Who uses it?
**Tone**: Pick an extreme—brutally minimal, maximalist chaos, retro-futuristic,
organic natural, luxurious, toy-like, magazine-style, brutalist, art deco...
**Differentiation**: What makes this UNFORGETTABLE?

**Key**: Choose a clear concept, then execute precisely. Bold maximalism
and refined minimalism both work—the key is intentional direction, not intensity.

## NEVER Do These

Typical "AI-generated" designs to avoid:

- Overused fonts: Inter, Roboto, Arial
- Purple gradients on white backgrounds (the AI signature)
- All corners rounded to 8px
- Cookie-cutter card layouts
- Generic, personality-free styles

## What to Pursue

- **Typography**: Choose distinctive fonts. Pair a unique display font with a refined body font
- **Color**: Commit to a coherent aesthetic. A dominant palette with sharp accents beats timid averaging
- **Animation**: Focus on high-impact moments—one精心 orchestrated page load beats scattered micro-interactions
- **Space**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Elements breaking the grid
- **Backgrounds**: Create atmosphere and depth, not default solid colors. Gradient meshes, noise textures, geometric patterns

## Execution Principles

**Match complexity to vision**:
- Maximalist design → complex code, lots of animation and effects
- Minimalist design → restraint, precision, meticulous spacing and typography

Elegance comes from executing the vision well, not from piling on effects.
```

## Skill Creation Process

Follow these steps to create a production-ready skill:

### Step 1: Understand with Concrete Examples

Skip ONLY when usage patterns are already crystal clear.

To create an effective skill, understand concrete examples of how it will be used:

**For image-editor skill**:
- "What functionality should it support? Editing, rotating?"
- "Can you give examples of how this skill would be used?"
- "What would a user say that should trigger this skill?"

Ask focused questions, don't overwhelm users.

### Step 2: Plan Reusable Contents

Analyze each example:
1. Consider how to execute from scratch
2. Identify scripts, references, assets that would help

**Analysis examples**:
- PDF rotation → same code rewritten repeatedly → Include `skills/scripts/rotate_pdf.py`
- Frontend projects → always need boilerplate → Include `skills/assets/hello-world/`
- BigQuery → constantly rediscovering schemas → Include `skills/references/schema.md`

### Step 3: Initialize Skill Structure

**MANDATORY**: Always run `init_skill.py` for new skills:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:
- Skill directory with `skills/` subdirectory
- Root-level `plugin.json` and `.claude-plugin/plugin.json`
- `skills/SKILL.md` template with proper frontmatter
- Example directories: `skills/scripts/`, `skills/references/`, `skills/assets/`

### Step 4: Implement Resources

**Start with reusable contents**:
- Write and test scripts (ensure deterministic output)
- Gather reference materials (API docs, schemas, policies)
- Prepare asset templates (boilerplate, samples)

**Delete unnecessary files**:
- Remove placeholder files created by init script
- Most skills don't need all three resource types

### Step 5: Write skills/SKILL.md

**Writing guidelines**:
- Use imperative/infinitive form ("Create" not "Creates")
- Be concise - code examples over verbose explanations
- Focus on what Claude doesn't know
- Include concrete examples for complex tasks
- **Target under 500 lines**

**Frontmatter**:
```yaml
---
name: your-skill-name
description: Clear description including WHAT it does and WHEN to use it.
Include specific triggers, file types, or contexts.
dependencies: python>=3.8  # Optional
allowed-tools: Bash, Read   # Optional
---
```

**Description best practices**:
- Max 1024 characters
- Include both functionality and trigger scenarios
- Example: "Process PDF forms including filling, validation, and extraction.
Use when working with PDF forms (.pdf) for: (1) Filling fillable fields,
(2) Extracting form data, (3) Validating form structure"

**Body structure**:
- Brief overview (1-2 sentences)
- Core principle or mental model
- Quick start or decision tree
- Links to references
- Anti-patterns (NEVER list)

### Step 6: Package and Validate

**Package the skill**:
```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:
```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The script will:
1. **Validate** automatically (YAML, naming, description, structure)
2. **Package** into .skill file (zip with .skill extension)

## Progressive Disclosure Patterns

### Three-Level Loading System

1. **Metadata** (~100 tokens) - Always loaded
   - `name` + `description` only
   - Primary triggering mechanism

2. **skills/SKILL.md body** (<5k tokens, target <500 lines) - On trigger
   - Core workflow and procedural instructions
   - Lean and focused

3. **Bundled resources** - As needed
   - Scripts: execute without loading
   - References: load only when linked
   - Assets: copy but never load

### Pattern 1: High-Level Guide with References

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [skills/references/FORMS.md](skills/references/FORMS.md) for complete guide
- **API reference**: See [skills/references/REFERENCE.md](skills/references/REFERENCE.md) for all methods
```

### Pattern 2: Domain-Specific Organization

```
bigquery-skill/
├── plugin.json
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── SKILL.md (overview and navigation)
    └── references/
        ├── finance.md (revenue, billing)
        ├── sales.md (opportunities, pipeline)
        ├── product.md (API usage, features)
        └── marketing.md (campaigns, attribution)
```

When user asks about sales → load only `skills/references/sales.md`

### Pattern 3: Conditional Details

```markdown
# DOCX Processing

## Creating documents
Use docx-js. See [skills/references/DOCX-JS.md](skills/references/DOCX-JS.md).

## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See [skills/references/REDLINING.md](skills/references/REDLINING.md)
**For OOXML details**: See [skills/references/OOXML.md](skills/references/OOXML.md)
```

## Skill Structure

```
skill-name/
├── plugin.json (required - root level)
├── .claude-plugin/
│   └── plugin.json (required - Claude plugin metadata)
└── skills/
    ├── SKILL.md (required)
    │   ├── YAML frontmatter (name, description)
    │   └── Markdown instructions
    └── Bundled Resources (optional)
        ├── scripts/      - Executable code
        ├── references/   - Documentation loaded as needed
        └── assets/       - Files used in output
```

### Scripts (`skills/scripts/`)

**When to include**: Same code rewritten repeatedly OR deterministic reliability needed
**Example**: `skills/scripts/rotate_pdf.py`
**Benefits**: Token efficient, deterministic, may execute without loading

### References (`skills/references/`)

**When to include**: Documentation Claude should reference while working
**Examples**: `skills/references/finance.md`, `skills/references/api_docs.md`
**Use cases**: Schemas, API docs, domain knowledge, policies
**Best practice**: If files >10k words, include grep patterns in skills/SKILL.md
**Avoid duplication**: Info lives in skills/SKILL.md OR references, not both

### Assets (`skills/assets/`)

**When to include**: Files used in final output, NOT in context
**Examples**: `skills/assets/logo.png`, `skills/assets/slides.pptx`, `skills/assets/font.ttf`
**Use cases**: Templates, images, icons, boilerplate, fonts

### What NOT to Include

- README.md (use skills/SKILL.md instead)
- INSTALLATION_GUIDE.md (installation info in skills/SKILL.md)
- QUICK_REFERENCE.md (quick reference in skills/SKILL.md)
- CHANGELOG.md (not needed for skills)
- LICENSE.md (unless required by dependencies)

**Note**: All skill-related content should be within the `skills/` subdirectory. Only `plugin.json` and `.claude-plugin/plugin.json` should be at the root level.
- Any user-facing documentation

**Skills are for AI agents, not humans.**

## Design Checklist

Use this checklist before deploying a skill:

```
Basic Compliance
[ ] Valid YAML frontmatter (name, description present)
[ ] Description includes both WHAT and WHEN to use
[ ] skills/SKILL.md < 500 lines

Content Quality
[ ] No explanation of concepts Claude already knows
[ ] No mechanical Step 1, 2, 3 tutorials
[ ] Has explicit anti-pattern list (NEVER list)
[ ] Has decision tree or selection guidance (if multiple paths)
[ ] Covers common traps and edge cases

Loading Mechanisms (for Skills with references)
[ ] Each reference has clear loading trigger conditions
[ ] Triggers embedded in workflow steps
[ ] Has mechanism to prevent over-loading

Freedom Calibration
[ ] Creative tasks → High freedom (principles not steps)
[ ] Fragile operations → Low freedom (precise scripts)

File Organization
[ ] No extraneous files (README, CHANGELOG, etc.)
[ ] All scripts tested and deterministic
[ ] References correctly linked from skills/SKILL.md
[ ] No duplication between skills/SKILL.md and references
[ ] All example files removed or customized
```

## Loading Trigger Techniques

### Technique 1: MANDATORY Syntax

Embed forced loading in workflow steps:

```markdown
### Creating New Document

**MANDATORY - READ ENTIRE FILE**: Before proceeding, you MUST read
[`skills/references/docx-js.md`](skills/references/docx-js.md) (~500 lines) completely.
**NEVER set any range limits when reading this file.**
```

Keywords: "MANDATORY", "MUST", "NEVER" - no ambiguity.

### Technique 2: Conditional Routing Table

```markdown
| Task Type | Must Load | Do NOT Load |
|-----------|-----------|-------------|
| New document | `skills/references/docx-js.md` | `skills/references/ooxml.md`, `skills/references/redlining.md` |
| Simple edits | `skills/references/ooxml.md` | `skills/references/docx-js.md` |
| Tracked changes | `skills/references/redlining.md` | `skills/references/docx-js.md` |
```

Tell Agent what to read AND what not to read.

### Technique 3: Scenario Detection

```markdown
**Scenario A: New Project**
- User says: "Build X from scratch", "Create a new..."
- **Must load**: `skills/references/greenfield.md`

**Scenario B: Fix Bug**
- User says: "X is broken", "Fix this bug"
- **Must load**: `skills/references/bugfix.md`
```

Route based on user input keywords.

## Reference Design Patterns

Consult these guides based on your skill's needs:

- **Multi-step processes**: See [skills/references/workflows.md](skills/references/workflows.md) for sequential workflows and conditional logic
- **Specific output formats**: See [skills/references/output-patterns.md](skills/references/output-patterns.md) for template and example patterns

## Security Considerations

- Audit third-party skills for unexpected behavior
- Never hardcode API keys; use environment variables
- Consider `allowed-tools` to restrict dangerous capabilities
- Test scripts in isolated environment when possible

## Evaluate Your Skill

After creating a skill, evaluate it using these dimensions:

| Dimension | Checks |
|-----------|--------|
| **Token Efficiency** | No explanations of concepts Claude already knows. Every paragraph justifies its token cost. |
| **Mental Models** | Transfers expert thinking patterns, not mechanical steps. Has clear decision framework. |
| **Anti-Patterns** | Explicit NEVER list. States what absolutely fails. |
| **Description Triggers** | Includes both WHAT it does and WHEN to use it. Clear activation scenarios. |
| **Freedom Calibration** | Creative tasks → high freedom (principles). Fragile operations → low freedom (scripts). |
| **Loading Design** | For skills with references: clear trigger conditions, MANDATORY syntax, conditional routing. |

**Self-evaluation questions:**
1. Would this skill make Claude perform like a domain expert?
2. Is every paragraph something Claude doesn't already know?
3. Are there explicit "what NOT to do" guidelines?
4. Can the agent decide when to activate this skill from the description?
5. Is the freedom level appropriate for the task fragility?
6. If there are references, does the agent know when to load each one?

**Scoring:**
- **Yes to all** → Excellent, production-ready
- **Mostly yes** → Good, minor improvements needed
- **Mixed** → Needs improvement
- **Mostly no** → Needs redesign

---

## Key Reminders

1. **Skills ≠ Tutorials** - They are compressed expert knowledge, not step-by-step guides
2. **Token efficiency is paramount** - Challenge every paragraph's value
3. **Mental models > Mechanical steps** - Teach how to think, not what to do
4. **Anti-patterns are critical** - Half of expert knowledge is what NOT to do
5. **Loading triggers matter** - For complex skills, explicitly design when to load what
6. **Match freedom to fragility** - Creative → high freedom, fragile → low freedom

**Before writing, ask yourself:**
- How do top experts in this domain think?
- What are their core decision principles?
- What pitfalls have they encountered?
- What do they absolutely never do?
- What knowledge does the model lack but need?

**Remember:**

```
Tools let models do things. Skills let models know how.
```

A good skill inherits expert thinking, not teaches basic operations.

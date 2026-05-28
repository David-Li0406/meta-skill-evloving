---
name: creating-skills
description: Creates Claude Code skills with proper structure, naming, and best practices. Use when the user asks to create a new skill, wants help writing a SKILL.md, or needs to structure skill content.
---

# Creating Skills

Skills extend Claude's capabilities with domain-specific knowledge and workflows.

## Structure

```
skill-name/
├── SKILL.md              # Required: metadata + instructions
├── reference.md          # Optional: detailed docs (loaded on demand)
└── scripts/              # Optional: utility scripts
```

## SKILL.md Template

````markdown
---
name: doing-the-thing
description: Does X and Y. Use when the user asks about Z or needs to accomplish W.
---

# Skill Title

One-line summary of what this skill does.

## Quick Start

```bash
# most common usage
```

## When to Use

- Trigger condition 1
- Trigger condition 2

## Workflow

1. First step
2. Second step
3. Verify result
````

## Frontmatter Rules

| Field | Constraints |
|-------|-------------|
| `name` | Max 64 chars, lowercase + hyphens only, no "anthropic" or "claude" |
| `description` | Max 1024 chars, third person, what it does + when to use it |

**Naming**: Use gerund form (`processing-pdfs`, `analyzing-data`) or action form (`process-pdfs`).

## Key Principles

**Be concise** - Claude already knows general concepts. Only add what's unique to this skill.

```markdown
# Bad: 150 tokens explaining PDFs
PDF (Portable Document Format) files are a common file format...

# Good: 50 tokens, actionable
Use pdfplumber for text extraction:
```

**Set freedom appropriately**:
- High freedom: "Analyze the code and suggest improvements"
- Low freedom: "Run exactly: `python scripts/migrate.py --verify`"

**Write in third person**:
- Good: "Extracts text from PDF files"
- Bad: "I can help you extract text" / "You can use this to extract"

## Workflow Pattern

For multi-step tasks, provide a checklist:

````markdown
## Processing Workflow

```
Progress:
- [ ] Step 1: Analyze input
- [ ] Step 2: Transform data
- [ ] Step 3: Validate output
```

**Step 1: Analyze input**
Run: `python scripts/analyze.py input.pdf`

**Step 2: Transform data**
...
````

## Progressive Disclosure

Keep SKILL.md under 500 lines. Split large content:

```markdown
## Advanced Features

**Form filling**: See [FORMS.md](FORMS.md)
**API reference**: See [REFERENCE.md](REFERENCE.md)
```

Keep references one level deep from SKILL.md.

## Anti-Patterns

- Vague names: `helper`, `utils`, `tools`
- Time-sensitive info: "If before August 2025..."
- Too many options: "You can use pypdf, or pdfplumber, or PyMuPDF..."
- Windows paths: `scripts\helper.py` → use `scripts/helper.py`
- Deep nesting: SKILL.md → advanced.md → details.md

## Checklist

Before finalizing:

- [ ] Description is specific with trigger conditions
- [ ] Under 500 lines
- [ ] No time-sensitive content
- [ ] Consistent terminology
- [ ] Clear workflows with steps
- [ ] One level deep references

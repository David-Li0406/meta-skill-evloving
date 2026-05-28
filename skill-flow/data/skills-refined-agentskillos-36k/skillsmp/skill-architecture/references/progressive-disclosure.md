**Skill**: [Skill Architecture](../SKILL.md)

# Progressive Disclosure

Context management pattern for efficient skill loading.

## Three-Level Loading System

### Level 1: Metadata (Always Loaded)

**What**: YAML frontmatter only
**Size**: ~100 words
**When**: Every Claude session
**Cost**: Negligible

```yaml
---
name: pdf-editor
description: Extract text, rotate, merge, split PDFs. Use when working with PDF files.
---
```

**Purpose**: Skill discovery - Claude knows the skill exists and when to use it.

### Level 2: SKILL.md Body (Loaded on Trigger)

**What**: Main skill instructions
**Size**: <5k words (aim for <2k)
**When**: Skill activates
**Cost**: Moderate (part of context window)

**Guidelines**:

- Essential procedures only
- Quick reference format
- Link to references/ for details
- Keep under 200 lines when possible

**Example**:

```markdown
## Quick Start

1. Rotate PDF: Run `scripts/rotate_pdf.py <file> <degrees>`
2. Merge PDFs: Run `scripts/merge_pdfs.py <file1> <file2>`

See [Advanced Operations](/skills/pdf-editor/references/advanced.md) for complex scenarios.
```

### Level 3: Bundled Resources (Loaded on Demand)

**What**: `references/`, `scripts/`, `assets/`
**Size**: Unlimited
**When**: Claude explicitly reads them
**Cost**: High (full file content) or Zero (scripts execute without loading)

**References** - Loaded when Claude needs deep context:

```markdown
See [Schema Documentation](/skills/api-client/references/schema.md)
```

**Scripts** - May execute without loading:

```bash
scripts/rotate_pdf.py input.pdf 90
# Claude runs without reading script content
```

**Assets** - Never loaded (copied/modified only):

```markdown
Copy template: `cp assets/template.html output.html`
```

## Designing for Progressive Disclosure

### Anti-Pattern: Monolithic SKILL.md

❌ **Bad**: 500-line SKILL.md with everything inline

```markdown
# PDF Editor

## Rotation

[50 lines of rotation details]

## Merging

[100 lines of merge details]

## Splitting

[80 lines of split details]

## Format Conversion

[150 lines of conversion details]

## Troubleshooting

[120 lines of error handling]
```

**Problem**: Every skill activation loads 500 lines, even for simple "rotate 90 degrees" task.

### Pattern: Lean Entry + Rich References

✅ **Good**: Lean SKILL.md + detailed references

```markdown
# PDF Editor

## Capabilities

- **Rotate**: `scripts/rotate_pdf.py <file> <degrees>`
- **Merge**: `scripts/merge_pdfs.py <files...> <output>`
- **Split**: `scripts/split_pdf.py <file> <page-ranges>`
- **Convert**: See [Conversion Guide](/skills/pdf-editor/references/conversion.md)

## Troubleshooting

Common issues: See [Troubleshooting](/skills/pdf-editor/references/troubleshooting.md)
```

**Benefit**: SKILL.md loads quickly, references loaded only when needed.

## When to Use Each Level

### Put in SKILL.md (Level 2):

- ✅ Common use cases (80% of tasks)
- ✅ Quick reference commands
- ✅ Navigation guide to references
- ✅ Security warnings
- ✅ Tool restrictions (`allowed-tools`)

### Put in references/ (Level 3):

- ✅ Detailed explanations (>100 words)
- ✅ Edge cases and advanced scenarios
- ✅ Comprehensive documentation
- ✅ Large schemas/API docs
- ✅ Troubleshooting guides

### Put in scripts/ (Level 3):

- ✅ Deterministic operations
- ✅ Repeatedly rewritten code
- ✅ External tool wrappers
- ✅ Complex algorithms

### Put in assets/ (Level 3):

- ✅ Templates (HTML, config files)
- ✅ Images, icons, fonts
- ✅ Boilerplate code
- ✅ Sample documents

## Real-World Example: BigQuery Skill

**Before Progressive Disclosure** (400 lines):

```markdown
# BigQuery

## Table Schemas

[200 lines of schema documentation]

## Query Patterns

[100 lines of query examples]

## Troubleshooting

[100 lines of error handling]
```

**After Progressive Disclosure** (80 lines + references):

````markdown
# BigQuery

## Quick Queries

Find today's user logins:

```sql
SELECT COUNT(*) FROM users WHERE login_date = CURRENT_DATE()
```
````

Complex queries: See Query Patterns (/skills/bigquery/references/query-patterns.md)

## Schema

Main tables: users, sessions, events
Full schema: See Schema Documentation (/skills/bigquery/references/schema.md)

Grep for tables: `grep -i "table_name" /skills/bigquery/references/schema.md`

## Troubleshooting

See Common Issues (/skills/bigquery/references/troubleshooting.md)

```

**Result**:
- Level 2: 80 lines (fast load, covers 80% of tasks)
- Level 3: 300+ lines in references (loaded only when needed)
- Token efficiency: 73% improvement for common tasks

## Measuring Effectiveness

**Good progressive disclosure**:
- SKILL.md handles 80% of tasks standalone
- References loaded <20% of the time
- No duplicate content between levels
- Clear navigation from SKILL.md to references

**Poor progressive disclosure**:
- SKILL.md too minimal (constant reference lookups)
- SKILL.md too detailed (loads unnecessary content)
- Duplicate content across SKILL.md and references
- Unclear when to consult references
```

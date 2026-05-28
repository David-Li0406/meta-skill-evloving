# Document Type Detection and Handling

Detect document type from path and filename, then apply type-specific transformations.

## Type Detection

| Type             | Detection Pattern                            | Priority |
| ---------------- | -------------------------------------------- | -------- |
| CLAUDE.md        | Filename is `CLAUDE.md` or `CLAUDE.local.md` | 1        |
| Skill file       | Path contains `.claude/skills/`              | 2        |
| Pattern file     | Path contains `claude-patterns/`             | 3        |
| General markdown | Extension is `.md`                           | 4        |

## Type-Specific Handling

### CLAUDE.md Files

**Target**: Under 300 lines (loaded into every conversation)

**Required sections**:

- Project Overview (1-2 sentences)
- Tech Stack (table format)
- Commands (table format)
- Critical rules (bulleted)

**Structure**:

```markdown
# Project Name

Brief description of what the project does.

## Tech Stack

| Technology | Purpose            |
| ---------- | ------------------ |
| React 18   | Frontend framework |

## Commands

| Command       | Purpose          |
| ------------- | ---------------- |
| `npm run dev` | Start dev server |

## Critical Rules

- Rule 1
- Rule 2

## Pattern References

For detailed patterns, see `claude-patterns/INDEX.md`
```

**Transformations**:

1. Move detailed explanations to pattern files
2. Convert prose to tables and bullets
3. Add pattern file references for depth
4. Remove redundant context

---

### Skill Files (SKILL.md)

**Target**: 200-300 lines

**Required frontmatter**:

```yaml
---
name: skill-name
description: Third-person description. Use when user says "trigger 1", "trigger 2". Brief purpose.
allowed-tools: Read, Edit, Bash, AskUserQuestion
version: 1.0.0
---
```

**Required sections**:

- `<when_to_use>` - Trigger phrases
- `<workflow>` - Phase table with actions
- `<approval_gates>` - User decision points
- `<references>` - Links to detailed docs

**Structure**:

```markdown
---
name: skill-name
description: ...
allowed-tools: ...
version: 1.0.0
---

# Skill Name

Brief description.

<when_to_use>

## When to Use

- "trigger phrase 1"
- "trigger phrase 2"
  </when_to_use>

<workflow>
## Workflow
| Phase | Action |
|-------|--------|
| 1 | First action |
</workflow>

<approval_gates>

## Approval Gates

| Gate    | Phase | Question   |
| ------- | ----- | ---------- |
| Confirm | 3     | "Proceed?" |

</approval_gates>

<references>
## References
- [references/details.md](references/details.md)
</references>

<version_history>

## Version History

- **v1.0.0** (YYYY-MM-DD): Initial release
  </version_history>
```

**Transformations**:

1. Add frontmatter if missing
2. Wrap sections in XML tags
3. Convert workflow to table format
4. Move detailed content to references/
5. Add version history

---

### Pattern Files

**Target**: 300-500 lines

**Required structure**:

- Title with "AI Instructions" note
- Numbered patterns with [OK]/[FAIL] examples
- Real consequences section
- Cross-references

**Structure**:

````markdown
# Pattern Name

_AI Instructions: Follow these patterns when [context]._

## Pattern 1: Name

**Rule**: Declarative statement.

[OK] CORRECT:

```code
example
```
````

[FAIL] WRONG:

```code
counter-example
```

**Why**: Explanation of consequences.

**Source**: [Link to authoritative source]

## Cross-References

- Related pattern 1
- Related pattern 2

```

**Transformations**:
1. Add AI instruction note at top
2. Number all patterns
3. Add [OK]/[FAIL] examples for each pattern
4. Include real-world consequences
5. Add source references

---

### General Markdown

**Target**: Varies by content

**Transformations applied**:
1. All structure rules (heading hierarchy, tables, bullets)
2. All content rules (terminology, references, imperative form)
3. All format rules (code blocks, length optimization)

**No type-specific requirements** - apply general best practices.

---

## Detection Implementation

```

function detectDocumentType(filePath):
filename = basename(filePath)

    if filename in ["CLAUDE.md", "CLAUDE.local.md"]:
        return "claude-md"

    if ".claude/skills/" in filePath:
        return "skill"

    if "claude-patterns/" in filePath:
        return "pattern"

    if filePath.endsWith(".md"):
        return "general"

    return "unknown"

```

## Transformation Priority

When transforming, apply rules in this order:

1. **Type-specific structure** (frontmatter, required sections)
2. **Structure rules** (headings, tables, bullets)
3. **Content rules** (terminology, references, imperative)
4. **Format rules** (code blocks, XML tags, length)
5. **Token optimization** (remove redundancy)
```

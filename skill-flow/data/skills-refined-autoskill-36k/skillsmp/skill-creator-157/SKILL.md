---
name: skill-creator
description: 'Meta-skill để tạo và validate Copilot skills. Bao gồm scripts, templates, và best practices cho skill development.'
---

# Skill Creator Skill

Meta-skill này provide guidelines và tools để tạo high-quality Copilot skills theo awesome-copilot format.

## Khi Nào Sử Dụng

- Tạo skill mới từ scratch
- Convert existing documentation thành skill format
- Validate skill structure
- Package skill for distribution
- Review và improve existing skills

---

## Skill Structure

```
skills/
└── my-skill/
    ├── SKILL.md           # Required: Main entry point
    └── references/         # Optional: Supporting documents
        ├── concept-a.md
        ├── concept-b.md
        └── examples.md
```

---

## SKILL.md Template

```markdown
---
name: skill-name-lowercase
description: 'Concise description (1-2 sentences). Explain WHAT and WHEN to use.'
---

# Skill Title

> Brief tagline hoặc summary

## Khi Nào Sử Dụng

- Use case 1
- Use case 2
- Use case 3

## Khi KHÔNG Sử Dụng

- Anti-pattern 1
- Anti-pattern 2

---

## Core Concepts

### Concept 1
[Explanation]

### Concept 2
[Explanation]

---

## Quick Reference

| Item | Description |
|------|-------------|
| A | Details |
| B | Details |

---

## Examples

### Example 1: [Name]
[Code or content]

### Example 2: [Name]
[Code or content]

---

## Checklist

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

---

## References

- [references/detailed-concept.md](references/detailed-concept.md)
- [External link](url)
```

---

## Frontmatter Guidelines

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Lowercase, hyphen-separated |
| `description` | string | 1-2 sentences, in quotes |

### Description Best Practices

✅ Good:
```yaml
description: 'Build MCP servers with TypeScript. Step-by-step guide from setup to deployment.'
```

❌ Bad:
```yaml
description: MCP  # Too short
description: 'This skill helps you...'  # Don't start with "This skill"
```

---

## Content Guidelines

### Principles

1. **Progressive Disclosure**
   - SKILL.md = Overview + Quick reference
   - references/ = Deep dives

2. **Scannable**
   - Use tables over paragraphs
   - Use bullet points
   - Use headers liberally

3. **Actionable**
   - Include code examples
   - Include checklists
   - Include templates

4. **Concise**
   - Cut unnecessary words
   - One concept per section
   - No fluff

### Writing Style

| Do | Don't |
|----|-------|
| Be direct | Use passive voice |
| Use tables | Write long paragraphs |
| Show examples | Only explain theory |
| Use code blocks | Describe code in words |

---

## Quality Checklist

### Structure
- [ ] Has SKILL.md with frontmatter
- [ ] Frontmatter has `name` and `description`
- [ ] Name is lowercase with hyphens
- [ ] Description is 1-2 sentences

### Content
- [ ] Has "Khi Nào Sử Dụng" section
- [ ] Has practical examples
- [ ] Has quick reference table
- [ ] Links to references (if any)

### Formatting
- [ ] Proper markdown syntax
- [ ] Consistent heading levels
- [ ] Code blocks with language tags
- [ ] Tables are well-formatted

### Completeness
- [ ] Covers main use cases
- [ ] Addresses common questions
- [ ] No placeholder content
- [ ] All links work

---

## Skill Categories

| Category | Examples |
|----------|----------|
| **Languages** | python, typescript, swift |
| **Frameworks** | react, ios-swiftui, flutter |
| **Tools** | git, docker, kubernetes |
| **Practices** | testing, documentation, security |
| **Design** | ui-design, accessibility |
| **Meta** | skill-creator, mcp-builder |

---

## Validation Script

```bash
#!/bin/bash
# validate-skill.sh

SKILL_DIR=$1

# Check SKILL.md exists
if [ ! -f "$SKILL_DIR/SKILL.md" ]; then
  echo "❌ Missing SKILL.md"
  exit 1
fi

# Check frontmatter
if ! head -1 "$SKILL_DIR/SKILL.md" | grep -q "^---$"; then
  echo "❌ Missing frontmatter"
  exit 1
fi

# Check name field
if ! grep -q "^name:" "$SKILL_DIR/SKILL.md"; then
  echo "❌ Missing name in frontmatter"
  exit 1
fi

# Check description field
if ! grep -q "^description:" "$SKILL_DIR/SKILL.md"; then
  echo "❌ Missing description in frontmatter"
  exit 1
fi

echo "✅ Skill valid: $SKILL_DIR"
```

---

## Reference File Template

```markdown
# [Concept Name]

> Part of [skill-name] skill

## Overview

Brief introduction to this concept.

## Details

### Section 1

Detailed content...

### Section 2

Detailed content...

## Examples

### Example 1

```code
example
```

## See Also

- [Other reference](other-reference.md)
- [Main skill](../SKILL.md)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too much content in SKILL.md | Move details to references/ |
| No examples | Add concrete code/content |
| Generic description | Be specific about use case |
| No quick reference | Add summary table |
| Broken links | Validate all paths |
| Inconsistent formatting | Use template |

---

## Skill Ideas

Questions to generate skills:

1. What do you explain repeatedly?
2. What patterns do you follow?
3. What mistakes do you see often?
4. What would help onboard new team members?
5. What best practices should be documented?

---

## Distribution

### Via Git Submodule
```bash
# Add to project
git submodule add https://github.com/user/skills.git .skills

# Reference in copilot-instructions.md
# See skills in .skills/
```

### Via Copy
Just copy the skill folder vào project's skills/ directory.

### Via npm (advanced)
Package as npm package với bin script để install skills.

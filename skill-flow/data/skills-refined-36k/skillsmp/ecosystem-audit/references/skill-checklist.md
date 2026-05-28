# Skill Validation Checklist

Structure and quality requirements for Claude Code skills.

## Required Structure

```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional (>= 50 lines each if present)
├── scripts/              # Optional (executable)
└── assets/               # Optional (templates, samples)
```

## SKILL.md Requirements

### Frontmatter (Required)

```yaml
---
name: skill-name
description: This skill should be used when... Triggers include...
---
```

| field | required | format |
|-------|----------|--------|
| name | yes | lowercase, hyphenated |
| description | yes | starts with "This skill should be used when..." |

### Sections (Recommended)

| section | required | purpose |
|---------|----------|---------|
| when to use | strongly | use/skip table |
| workflow | strongly | ordered steps |
| tool integration | strongly | CLI commands |
| anti-patterns | recommended | common mistakes |
| references | if has refs | link list |

## Quality Gates

### Size Guidelines

| complexity | lines | references | scripts |
|------------|-------|------------|---------|
| simple | 120-170 | 1-2 | 0-1 |
| medium | 170-240 | 2-4 | 1-2 |
| full-featured | 240-380 | 3-6 | 2-4 |

### Content Checks

| check | criteria |
|-------|----------|
| frontmatter | `---` on line 1 |
| description | third-person, trigger phrases |
| examples | 2+ tool command examples |
| tables | use tables over lists |
| voice | lowercase headers (except acronyms) |

## Validation Script

```bash
# Check skill structure
for skill_dir in ~/.agents/skills/*/; do
  skill_name=$(basename "$skill_dir")

  # SKILL.md exists
  [ -f "$skill_dir/SKILL.md" ] || echo "MISSING: $skill_name/SKILL.md"

  # Frontmatter present
  head -1 "$skill_dir/SKILL.md" | grep -q "^---" || echo "WARN: $skill_name missing frontmatter"

  # Description field
  grep -q "^description:" "$skill_dir/SKILL.md" || echo "WARN: $skill_name missing description"

  # Line count
  lines=$(wc -l < "$skill_dir/SKILL.md")
  [ "$lines" -lt 80 ] && echo "WARN: $skill_name too short ($lines lines)"
done
```

## Common Issues

| issue | symptom | fix |
|-------|---------|-----|
| missing frontmatter | skill not invoked | add `---` block |
| vague triggers | misfires | add explicit trigger phrases |
| no examples | users can't execute | add 2+ command examples |
| oversized SKILL.md | info buried | move to references/ |
| dead references | broken links | link in ## references |

## Best Practices

1. **triggers first** - make invocation criteria explicit
2. **tables over prose** - scannable information
3. **concrete thresholds** - numbers not vague guidance
4. **tool examples** - show exact commands
5. **anti-patterns** - document common mistakes

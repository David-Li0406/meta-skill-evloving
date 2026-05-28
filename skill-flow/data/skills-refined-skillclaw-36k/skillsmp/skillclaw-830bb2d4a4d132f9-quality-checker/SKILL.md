---
name: quality-checker
description: Use this skill to validate skill quality, completeness, and adherence to standards before packaging to ensure it meets quality requirements.
---

# Quality Checker Skill

## Purpose

Single responsibility: Validate Claude skill packages for quality, completeness, and standards compliance before upload.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Skill directory exists
- [ ] SKILL.md is present
- [ ] Quality criteria are defined
- [ ] Validation scope is clear (quick/full/custom)

**DO NOT validate without defining quality criteria.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Quality threshold unclear (strict vs lenient)
- Custom validation rules needed
- Failures found - block or warn?
- Edge cases in validation logic

**NEVER auto-pass quality checks without proper validation.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Skill directory, quality criteria | Other skills |
| PERIPHERAL | Quality examples for comparison | Source documentation |
| DISTRACTOR | Build process | Enhancement history |

## Quality Dimensions

| Dimension | Weight | Checks |
|-----------|--------|--------|
| Structure | 25% | Required files, directory layout |
| Content | 35% | SKILL.md completeness, references |
| Code Examples | 20% | Presence, syntax, relevance |
| Documentation | 20% | Clarity, navigation, completeness |

## Workflow Steps

### Step 1: Structure Validation

```bash
# Required files
SKILL_DIR="output/<skill-name>"

# Check SKILL.md
test -f "$SKILL_DIR/SKILL.md" && echo "✅ SKILL.md present" || echo "❌ SKILL.md missing"

# Check references directory
test -d "$SKILL_DIR/references" && echo "✅ references/ present" || echo "❌ references/ missing"

# Check at least one reference file
ls "$SKILL_DIR/references/"*.md >/dev/null 2>&1 && \
  echo "✅ Reference files present" || echo "❌ No reference files"

# Check for index
test -f "$SKILL_DIR/references/index.md" && \
  echo "✅ Index present" || echo "⚠️ No index.md (recommended)"
```

### Step 2: SKILL.md Content Validation

```bash
SKILL_MD="output/<skill-name>/SKILL.md"

# Required sections
echo "=== Section Check ==="
grep -q "^# " "$SKILL_MD" && echo "✅ Title present" || echo "❌ Missing title"
grep -q "^## Description\|^## Purpose" "$SKILL_MD" && echo "✅ Description present" || echo "❌ Missing description"
```
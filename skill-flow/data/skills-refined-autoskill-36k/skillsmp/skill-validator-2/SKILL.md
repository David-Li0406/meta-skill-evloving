---
name: skill-validator
description: "Skill validation process for Bosun plugin skills. Use when validating skills, checking skill quality, reviewing skill structure, or auditing skill references. Also use when creating a new Bosun skill, checking frontmatter format, validating referenced files exist, ensuring skills follow naming conventions, or auditing all skills before release. Essential for skill authors and plugin quality assurance."
---

# Skill Validator

## Overview

Skills are Bosun's knowledge packages. Invalid skills break the plugin. This skill guides systematic validation of Bosun skills before they ship.

**Core principle:** Validate early, validate often. A malformed skill wastes everyone's time.

## The Validation Process

### Phase 1: Frontmatter Validation

Check the YAML frontmatter at the top of SKILL.md:

1. **Required Fields**
   - `name` - Must be present, must be `{purpose}` format
   - `description` - Must be present, must include trigger phrases

2. **Forbidden Fields**
   - `tags` - Removed per skill-creator spec
   - Any field other than `name` and `description`

3. **Description Quality**
   - Includes "Use when..." trigger phrases
   - 50-100 words (comprehensive but concise)
   - No angle brackets (< or >)

### Phase 2: Structure Validation

Check the SKILL.md body structure:

1. **Required Sections**
   - Overview with core principle
   - "When to Use" or similar trigger section
   - Red Flags section
   - Checklist section
   - Quick Commands or Quick Patterns

2. **Length Check**
   - SKILL.md should be < 500 lines
   - If approaching limit, content should be in references/

3. **Code Examples**
   - Use ✅/❌ or checkmark/X pattern for good/bad
   - Examples should be practical and runnable

### Phase 3: Reference Validation

Check the references/ directory:

1. **Cited References Exist**
   - Every file mentioned in SKILL.md References section exists
   - Check: `references/{filename}.md`

2. **No Orphaned References**
   - Every file in references/ is cited in SKILL.md
   - Orphaned files waste space and cause confusion

3. **Naming Convention**
   - Files should be `{topic}.md` or `{topic}-patterns.md`
   - Avoid `{skill}-research.md` pattern

## Red Flags - STOP and Fix

### Frontmatter Red Flags
```yaml
# ❌ Has tags field (removed from spec)
tags: [security, owasp]

# ❌ Missing description
name: security

# ❌ Wrong naming pattern
name: security-skill  # Should be security

# ❌ No trigger phrases in description
description: "Security stuff"  # Should include "Use when..."
```

### Structure Red Flags
```
- SKILL.md over 500 lines (move content to references/)
- Missing Red Flags section (every skill needs warnings)
- Missing Checklist (users need actionable checks)
- No code examples (skills should show, not just tell)
- Deeply nested headers (keep it flat: h1 → h2 → h3 max)
```

### Reference Red Flags
```
- "See references/foo.md" but foo.md doesn't exist
- references/ has files never mentioned in SKILL.md
- Research files with no clear topic ({skill}-research.md)
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "Tags help discovery" | Description triggers skills. Tags are ignored. |
| "The skill is too long" | Move details to references/. Keep SKILL.md lean. |
| "References will be added later" | Don't cite what doesn't exist. |
| "The description is fine" | If it lacks "Use when...", Claude won't trigger it. |

## Validation Checklist

Before approving a skill:

**Frontmatter:**
- [ ] Only `name` and `description` fields
- [ ] Name follows `{purpose}` pattern
- [ ] Description includes trigger phrases ("Use when...")
- [ ] Description is 50-100 words

**Structure:**
- [ ] SKILL.md is < 500 lines
- [ ] Has Overview with core principle
- [ ] Has Red Flags section
- [ ] Has Checklist section
- [ ] Has Quick Commands/Patterns section
- [ ] Code examples use ✅/❌ pattern

**References:**
- [ ] All cited references exist in references/
- [ ] No orphaned files in references/
- [ ] Reference naming follows convention

## Quick Validation Commands

```bash
# Check frontmatter for forbidden fields
head -10 skills/*/SKILL.md | grep -E "^tags:"

# Count lines in each skill
wc -l skills/*/SKILL.md | sort -n

# Find skills over 400 lines (approaching limit)
wc -l skills/*/SKILL.md | awk '$1 > 400 {print}'

# List all reference files
ls skills/*/references/*.md

# Find cited references in a skill
grep -o 'references/[^`]*\.md' skills/security/SKILL.md
```

## Validation Output Format

When validating, report findings like this:

```
Validating security...
  ✓ Frontmatter valid
  ✓ Structure valid (178 lines)
  ✓ References valid (4 cited, 4 exist)

Validating architect...
  ✓ Frontmatter valid
  ✓ Structure valid (199 lines)
  ✗ Missing reference: api-design.md
  ✗ Missing reference: architecture-patterns.md

Summary: 18/20 skills valid, 2 with issues
```

## References

- Skill-creator specification for base validation rules
- CLAUDE.md for Bosun-specific conventions

---
name: skill-packager
description: Use this skill to package completed skill directories into uploadable ZIP files for Claude AI, ensuring all necessary validations are performed beforehand.
---

# Skill Packager Skill

## Purpose

Single responsibility: Package completed skill directories into ZIP files ready for upload to Claude AI.

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Skill directory exists with required structure
- [ ] SKILL.md is present and non-empty
- [ ] At least one reference file exists
- [ ] No sensitive data in skill directory
- [ ] Output path for ZIP is writable

**DO NOT package without validating skill structure.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Skill structure incomplete - proceed anyway?
- Large files detected - include or exclude?
- Sensitive patterns found (API keys, passwords)
- Multiple skill directories - which to package?

**NEVER package potentially sensitive content without review.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Skill directory contents, package config | Other skills |
| PERIPHERAL | Package size estimates | Source data |
| DISTRACTOR | Build process details | Scraping history |

## Workflow Steps

### Step 1: Validate Skill Structure (Grounding)

```bash
# Required structure check
test -f output/<skill-name>/SKILL.md || echo "ERROR: Missing SKILL.md"
test -d output/<skill-name>/references || echo "ERROR: Missing references/"

# Check SKILL.md is not empty
test -s output/<skill-name>/SKILL.md || echo "ERROR: SKILL.md is empty"

# Check for at least one reference
ls output/<skill-name>/references/*.md >/dev/null 2>&1 || echo "ERROR: No reference files"
```

### Step 2: Security Check

```bash
# Scan for potential sensitive data
grep -rE "(api[_-]?key|password|secret|token|credential)" output/<skill-name>/ && \
  echo "WARNING: Potential sensitive data found - review before packaging"

# Check for large files
find output/<skill-name>/ -size +10M -exec echo "WARNING: Large file: {}" \;

# Check for binary files
find output/<skill-name>/ -type f ! -name "*.md" ! -name "*.json" ! -name "*.txt" \
  -exec file {} \; | grep -v "text" && echo "WARNING: Non-text files found"
```

### Step 3: Calculate Package Size

```bash
# Estimate final size
du -sh output/<skill-name>/

# Count files
find output/<skill-name>/ -type f | wc -l
```
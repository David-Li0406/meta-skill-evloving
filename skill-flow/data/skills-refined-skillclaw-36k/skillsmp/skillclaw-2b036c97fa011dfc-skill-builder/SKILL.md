---
name: skill-builder
description: Use this skill to transform extracted documentation into properly structured Claude skill packages ready for upload after using a doc-scraper or pdf-extractor.
---

# Skill Builder Skill

## Purpose

Single responsibility: Transform extracted documentation into properly structured Claude skill packages ready for upload.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Input data directory exists and contains extracted content
- [ ] Content format is recognized (JSON pages, markdown, etc.)
- [ ] Output directory is writable
- [ ] Skill name follows Claude conventions (lowercase, alphanumeric, hyphens)

**DO NOT build without verifying input data quality.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Multiple input formats detected - which to prioritize?
- Category structure unclear from content
- Skill description ambiguous
- Target audience undefined

**NEVER generate placeholder content without user guidance.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Input data, skill config, output path | Other skills |
| PERIPHERAL | Similar skill examples | Unrelated documentation |
| DISTRACTOR | Previous build attempts | Source scraping details |

## Workflow Steps

### Step 1: Validate Input

```bash
# Check input data exists
ls -la output/<skill-name>_data/

# Verify page count
find output/<skill-name>_data/pages -name "*.json" | wc -l

# Check summary
cat output/<skill-name>_data/summary.json
```

### Step 2: Generate Skill Structure

Standard Claude skill structure:

```
output/<skill-name>/
├── SKILL.md              # Main skill file (required)
├── references/           # Reference documentation
│   ├── index.md          # Category index
│   ├── getting_started.md
│   ├── api_reference.md
│   └── guides.md
├── scripts/              # Optional automation scripts
└── assets/               # Optional images, diagrams
```

### Step 3: Create SKILL.md

Template for SKILL.md:

```markdown
# <Skill Name>

## Description
<When to use this skill - clear, specific>

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Quick Reference

### Common Patterns
<Most frequently used patterns with code examples>

### API Overview
<Key API methods/functions>

## Navigation

| Topic | File | Description |
|-------|------|-------------|
| Getting Started | <file> | <description> |
```
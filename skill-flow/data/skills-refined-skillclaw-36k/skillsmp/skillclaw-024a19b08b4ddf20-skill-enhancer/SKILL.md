---
name: skill-enhancer
description: Use this skill when you need to enhance basic SKILL.md files into comprehensive, high-quality documentation using AI.
---

# Skill Enhancer Skill

## Purpose

Single responsibility: Enhance basic SKILL.md files using AI to extract better examples, create comprehensive guides, and improve overall skill quality.

## Grounding Checkpoint

Before executing, VERIFY:

- [ ] Skill directory exists with SKILL.md and references/
- [ ] Reference files contain actual content (not empty)
- [ ] Enhancement mode selected (local or API)
- [ ] Backup of original SKILL.md created

**DO NOT enhance without backing up original content.**

## Uncertainty Escalation

ASK USER instead of guessing when:

- Content quality too low for meaningful enhancement
- Multiple valid enhancement directions possible
- Target audience unclear
- Enhancement scope undefined (full vs partial)

**NEVER hallucinate content not present in references.**

## Context Scope

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | SKILL.md, references/, skill purpose | Other skills |
| PERIPHERAL | Similar high-quality skills as examples | Unrelated documentation |
| DISTRACTOR | Source scraping details | Enhancement history |

## Enhancement Modes

| Mode | Method | Cost | Quality |
|------|--------|------|---------|
| Local | Claude Code Max plan | Free | 9/10 |
| API | Anthropic API | ~$0.05-0.20 | 9/10 |
| Manual | Guided template | Free | Variable |

## Workflow Steps

### Step 1: Backup Original

```bash
# Create backup
cp output/<skill-name>/SKILL.md output/<skill-name>/SKILL.md.backup

# Record backup timestamp
echo "Backup created: $(date)" > output/<skill-name>/.enhancement_backup
```

### Step 2: Analyze Current Content

```bash
# Check current SKILL.md quality
wc -l output/<skill-name>/SKILL.md
grep -c '```' output/<skill-name>/SKILL.md  # Code examples
grep -c '^## ' output/<skill-name>/SKILL.md  # Sections

# List reference files
ls -la output/<skill-name>/references/

# Sample reference content
head -50 output/<skill-name>/references/*.md
```

### Step 3: Execute Enhancement

**Option A: Local Enhancement (Recommended)**

Using Claude Code Max (no API costs):

```bash
# With skill-seekers
skill-seekers enhance output/<skill-name>/ --local

# This opens Claude Code in new terminal
```
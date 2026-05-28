# Agent Skills Portability Guide

This document covers how to write skills that work across both VS Code/GitHub Copilot and Claude Code.

## The Agent Skills Standard

Agent Skills is an open standard maintained at [agentskills.io](https://agentskills.io). Skills following this standard work across multiple agents.

## Supported Platforms

| Platform | Project Skills | Personal Skills |
|----------|---------------|-----------------|
| **Claude Code** | `.claude/skills/` | `~/.claude/skills/` |
| **VS Code/Copilot** | `.github/skills/` ✅ | `~/.copilot/skills/` ✅ |
| **VS Code/Copilot** | `.claude/skills/` (legacy) | `~/.claude/skills/` (legacy) |

**Key insights:**
- Both agents read from `.claude/skills/`, making it a compatible location
- VS Code prefers `.github/skills/` for repo-wide skills (works reliably)
- App-level skills (e.g., `apps/myapp/.copilot/skills/`) are **not currently discovered** in VS Code
- Users must enable `chat.useAgentSkills: true` in **both** User settings and Workspace settings

---

## Frontmatter Fields

### Standard Fields (Portable)

| Field | Required | Max Length | Description |
|-------|----------|------------|-------------|
| `name` | ✅ | 64 chars | Lowercase, numbers, hyphens only |
| `description` | ✅ | 1024 chars | What + when to use |
| `license` | ❌ | - | License name or file reference |
| `requirements` | ❌ | 500 chars | Environment requirements |
| `metadata` | ❌ | - | Arbitrary key-value pairs |

### Non-Standard Fields (Not Portable)

These fields are platform-specific and should NOT be used at the root level:

| Field | Platform | Alternative |
|-------|----------|-------------|
| `allowed-tools` | Claude Code | Use `metadata.claude-code.allowed-tools` |
| `model` | Claude Code | Use `metadata.claude-code.model` |
| `hooks` | Claude Code | No portable alternative |
| `context` | Claude Code | No portable alternative |
| `agent` | VS Code prompts | Not applicable to skills |
| `tools` | VS Code prompts | Not applicable to skills |

---

## Name Format

Valid names:
- `api-client` ✅
- `pdf-processing` ✅
- `a` ✅ (single character)
- `my-skill-123` ✅

Invalid names:
- `API-Client` ❌ (uppercase)
- `-my-skill` ❌ (starts with hyphen)
- `my-skill-` ❌ (ends with hyphen)
- `my skill` ❌ (spaces)
- `my_skill` ❌ (underscores)

---

## Description Best Practices

**The description is critical for skill discovery.** It's the primary "trigger surface" that determines whether Copilot loads your skill in response to a user query.

### Key principles (from Jan 2026 research)

Based on official GitHub/VS Code documentation and the Agent Skills specification:

- Descriptions are evaluated using **"match to description" logic**
- Matching algorithm is implementation-specific (keywords vs embeddings vs LLM reasoning)
- **You control reliability through description clarity**, not through the matching algorithm

### What to include in descriptions

1. **Explicit "Use when..."** phrasing (don't be subtle)
2. **What the skill does** (actions/capabilities)  
3. **When to use it** (trigger conditions - be specific)
4. **Key terms** (synonyms and keywords you expect in user prompts)
5. **Concrete examples** (2-4 specific use cases or trigger phrases)

### Good Example (skill loads reliably)

```yaml
description: >
  Extract text and tables from PDF files, fill PDF forms, merge multiple PDFs.
  Use when: working with PDF documents, extracting data, automating form filling,
  or manipulating document structures. Keywords: PDF, extract, form, merge, document.
  Examples: "Extract tables from PDF", "Fill PDF form", "Merge two PDFs".
```

### Poor Example (skill may not load)

```yaml
description: Helps with documents
```

### Why this matters

Better descriptions = higher probability skill loads across different LLM backends and matching strategies.  
Reference: `SKILL_LOADING_RESEARCH.md` in this directory for detailed research on how Copilot discovers and loads skills.

---

## Body Guidelines

### Length Limits

- Keep under **500 lines**
- Keep under **5000 tokens** (rough estimate: words ÷ 0.75)
- Move detailed content to `references/` directory

### Structure

```markdown
# Skill Name

## When to Use
[Trigger conditions]

## Process
[Step-by-step instructions]

## Examples
[Concrete examples with expected input/output]

## Guidelines
[Rules and best practices]
```

### File References

Use relative paths from the skill root:

```markdown
See [detailed guide](references/DETAILS.md) for more information.

Run the script:
```bash
python scripts/helper.py
```
```

---

## Progressive Disclosure

Skills use a three-level loading system:

1. **Discovery**: Only `name` and `description` are loaded initially
2. **Activation**: Full `SKILL.md` body loaded when skill matches
3. **Resources**: Files in `scripts/`, `references/`, etc. loaded on-demand

This means:
- Write a great description (it's the "hook")
- Keep `SKILL.md` focused (don't bloat with rarely-needed content)
- Put detailed docs in `references/` (loaded only when needed)

---

## Platform-Specific Features

### Using Claude-Only Features Safely

If you need `allowed-tools` or other Claude-specific features, use the `metadata` namespace:

```yaml
---
name: safe-reader
description: Read files without modifications
metadata:
  claude-code:
    allowed-tools: Read, Grep, Glob
---
```

This keeps the skill spec-compliant while providing hints for Claude Code.

### Overlay Approach (Advanced)

For more complex Claude-specific configurations:

```
.claude/skills/my-skill/
├── SKILL.md                    # Universal version
└── overlays/
    └── claude.yaml             # Claude-only additions
```

Build script to merge:

```bash
#!/bin/bash
# merge-overlay.sh
yq eval-all 'select(fileIndex == 0) * select(fileIndex == 1)' \
  SKILL.md overlays/claude.yaml > SKILL.claude.md
```

---

## Validation Checklist

Before deploying a skill, verify:

- [ ] `name` is lowercase, hyphens only, ≤64 chars
- [ ] `description` is ≤1024 chars and includes "when to use"
- [ ] No non-standard fields at root level
- [ ] SKILL.md body under 500 lines
- [ ] File references use relative paths
- [ ] Scripts have execute permissions
- [ ] Tested in both Claude Code and VS Code (if possible)

Run the validator:

```bash
python .claude/skills/skill-foundry/scripts/validate.py path/to/SKILL.md
```

---

## Common Pitfalls

### 1. Wrong Directory

| Symptom | Cause | Fix |
|---------|-------|-----|
| VS Code doesn't see skill | Skill not in `.github/skills/` or `.claude/skills/` | Check path |
| Claude Code doesn't see skill | Skill not in `.claude/skills/` | Move to correct location |

### 2. Invalid YAML

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill won't load | Tabs instead of spaces | Use spaces |
| Skill won't load | Missing `---` delimiters | Add `---` before and after frontmatter |
| Skill won't load | Special characters not quoted | Quote strings with `:`, `#`, etc. |

### 3. Discovery Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill not auto-activated | Description too vague | Add trigger words |
| Wrong skill activated | Overlapping descriptions | Make descriptions more specific |

---

## Resources

- [Agent Skills Standard](https://agentskills.io/specification)
- [VS Code Agent Skills Docs](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
- [Claude Code Skills Docs](https://code.claude.com/docs/en/skills)
- [Example Skills Repository](https://github.com/anthropics/skills)

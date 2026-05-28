---
name: plugin-validator
description: "Full plugin validation process for Bosun. Use when validating the entire plugin, checking plugin health, auditing agents and skills together, or preparing for release. Also use when checking cross-references between components, validating after major changes, onboarding to the Bosun codebase, or ensuring manifest, agents, skills, and commands work together. Essential before publishing or version bumps."
---

# Plugin Validator

## Overview

A valid plugin is a working plugin. This skill guides systematic validation of the entire Bosun plugin - manifest, agents, skills, and commands - and their cross-references.

**Core principle:** Validate the whole, not just the parts. Components must work together.

## The Validation Process

### Phase 1: Manifest Validation

Check `.claude-plugin/plugin.json`:

1. **Structure**
   - Valid JSON syntax
   - Required fields present (name, version, description)
   - Version follows semver (x.y.z)

2. **File References**
   - All referenced agent files exist
   - All referenced command files exist
   - All referenced skill directories exist

### Phase 2: Agent Validation

Check each file in `agents/*.md`:

1. **Frontmatter**
   - Required: `name`, `description`, `tools`, `model`
   - Optional: `skills`, `disallowedTools`

2. **Model Selection**
   - `opus` - For critical work (security, architecture)
   - `sonnet` - For standard work (quality, docs)
   - `haiku` - For quick tasks

3. **Skill References**
   - All skills in `skills: [...]` exist in `skills/` directory
   - Skills match agent's purpose

4. **Tool Selection**
   - Tools are valid Claude Code tools
   - Read-only agents use `disallowedTools: Edit, Write`

### Phase 3: Skill Validation

Delegate to `skill-validator` skill for each skill, plus:

1. **Agent Coverage**
   - Which agents reference each skill?
   - Are any skills orphaned (no agent uses them)?

2. **Category Balance**
   - Domain skills (security, architect, testing, etc.)
   - Language skills (golang, typescript, python, etc.)
   - Cloud skills (aws, gcp, azure)

### Phase 4: Command Validation

Check each file in `commands/*.md`:

1. **Frontmatter**
   - Required: `name`, `description`

2. **Content**
   - Clear usage instructions
   - Example output shown
   - Error handling documented

### Phase 5: Cross-Reference Validation

Check relationships between components:

1. **Skill-Agent Mapping**
   - All skills referenced by agents exist
   - Identify orphaned skills
   - Identify agents with no skills

2. **Consistency**
   - Naming conventions followed
   - No duplicate names across components

## Red Flags - STOP and Fix

### Manifest Red Flags
```json
// ❌ Invalid JSON
{ name: "bosun" }  // Missing quotes

// ❌ Missing version
{ "name": "bosun", "description": "..." }

// ❌ Invalid semver
{ "version": "1.0" }  // Should be "1.0.0"
```

### Agent Red Flags
```yaml
# ❌ Missing required field
name: security-agent
description: "..."
# Missing: tools, model

# ❌ Invalid model
model: gpt-4  # Should be opus, sonnet, or haiku

# ❌ Non-existent skill
skills: [nonexistent]

# ❌ Read-only agent with write tools
disallowedTools: Edit  # Missing Write
```

### Cross-Reference Red Flags
```
- Agent references skill that doesn't exist
- Skill exists but no agent uses it
- Command references non-existent agent
- Duplicate component names
```

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "The orphaned skill will be used later" | Remove it or assign it now. |
| "The agent doesn't need skills" | Every agent should leverage skills. |
| "The manifest is auto-generated" | Still validate it. Automation fails. |
| "Cross-references are obvious" | Make them explicit and verified. |

## Validation Checklist

Before approving the plugin:

**Manifest:**
- [ ] Valid JSON syntax
- [ ] Version follows semver
- [ ] All referenced files exist

**Agents:**
- [ ] All have required frontmatter fields
- [ ] Model is valid (opus/sonnet/haiku)
- [ ] Referenced skills exist
- [ ] Tools are valid

**Skills:**
- [ ] All pass skill-validator checks
- [ ] No orphaned skills (or documented why)
- [ ] Good category coverage

**Commands:**
- [ ] All have required frontmatter
- [ ] Usage documented
- [ ] Error handling covered

**Cross-References:**
- [ ] All skill references resolve
- [ ] No duplicate names
- [ ] Naming conventions followed

## Quick Validation Commands

```bash
# Validate manifest JSON
jq . .claude-plugin/plugin.json

# List all agents
ls agents/*.md

# List all skills
ls -d skills/*/

# List all commands
ls commands/*.md

# Find skills referenced by agents
grep -h "^skills:" agents/*.md

# Find orphaned skills (not in any agent)
comm -23 <(ls -d skills/*/ | xargs -n1 basename | sort) \
         <(grep -h "^skills:" agents/*.md | tr '[],' '\n' | grep bosun | sort -u)
```

## Validation Output Format

When validating, report findings like this:

```
Bosun Plugin Validation
=======================

Manifest (.claude-plugin/plugin.json)
  ✓ Valid JSON
  ✓ Version: 1.0.0
  ✓ All file references valid

Agents (9 files)
  ✓ security-agent (opus, 2 skills)
  ✓ quality-agent (sonnet, 4 skills)
  ✓ architecture-agent (opus, 2 skills)
  ... all valid

Skills (20 directories)
  ✓ 18/20 valid
  ✗ security: missing reference security-headers.md
  ✗ architect: missing references api-design.md, architecture-patterns.md

Commands (3 files)
  ✓ All valid

Cross-References
  ⚠ Orphaned skills: rust, java, csharp
    (exist but not assigned to any agent)

Overall: PASS with warnings
```

## References

- `skill-validator` for individual skill validation
- CLAUDE.md for Bosun conventions
- `.claude-plugin/plugin.json` for manifest schema

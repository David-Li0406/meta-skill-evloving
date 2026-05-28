---
name: skill-creator
description: Use when asked to create or update skills or extend agent capabilities in this configuration.
allowed-tools: ["write_file", "read_file"]
metadata:
  short-description: Create new Codex skills systematically
---

# Skill Creator

Guide for creating new Codex skills with the same rigor as existing ones.

## Context Efficiency (Anthropic Principle)

The context window is a public good. Only include what the model does **not** already know. Prefer concise guidance and move heavy references into separate files.

## Degree of Freedom Matching

Match instruction specificity to task fragility:
- **Low freedom** for fragile, error-prone workflows
- **High freedom** for exploratory work

## Progressive Disclosure

Use a three-layer structure:
1. **Frontmatter** for triggers only
2. **SKILL.md body** for workflow guidance
3. **References/scripts/assets** for heavy details

## TDD for Skills (Discipline)

Before creating or editing a skill:
- Define pressure scenarios that the skill must handle
- Validate behavior before/after changes
- Iterate to close loopholes

## Core Principle: Explicit References

**Never summarize guidance documents.** Always instruct to **read** the full documents, allowing all guidance to apply.

**Bad (summarizing):**
```markdown
Per quality.md:
- Correctness first
- Then safety
```

**Good (explicit read):**
```markdown
**Read these references:**
- `~/.config/agent/domain/coding/quality.md` - Complete quality priorities
```

## File Locations

All files in chezmoi source: `~/.local/share/chezmoi/home/`

**Skill Files (Parity Required):**
- Claude Code: `dot_claude/skills/<name>/SKILL.md`
- Codex: `dot_codex/skills/<name>/SKILL.md`
- Keep both in sync (strict parity)

**Apply with chezmoi:**
```bash
chezmoi apply ~/.codex
```

## Creating a Codex Skill

**Template:**
```markdown
---
name: skill-name
description: Use when <trigger conditions only; no workflow summary>
allowed-tools: ["shell", "apply_patch", "read_file", "write_file"]
metadata:
  short-description: Brief one-liner
---

# Skill Title

**Read these references:**
- `references/file1.md` - Purpose/summary
- `~/.config/agent/path/to/file2.md` - Purpose/summary

## Instructions

<Skill-specific guidance>

Apply all guidance from references listed above.

## Arguments

Target: ${ARGUMENTS}
```

**Key points:**
- `description` field triggers auto-activation - be specific about triggers
- `allowed-tools` is JSON array format: `["shell", "read_file"]`
- `metadata.short-description` for UI display
- Use `${ARGUMENTS}` for argument substitution (NOT `$ARGUMENTS`)
- No `@` includes - use explicit "Read these references" instead

**Reference Formats:**
- Local (via symlink): `references/file.md`
- Direct path: `~/.config/agent/path/to/file.md`
- AGENT.md is auto-loaded for all profiles

## Creating References Symlink

For skills needing domain-specific guidance:
```bash
# In deployed directory (NOT chezmoi source!)
cd ~/.codex/skills/skill-name
ln -s ~/.config/agent/domain/path references

# If also using Claude Code, mirror the same symlink:
cd ~/.claude/skills/skill-name
ln -s ~/.config/agent/domain/path references
```

Example: Go skills symlink to `~/.config/agent/domain/coding/go`

## Workflow for Creating New Skills

### 1. Identify Purpose
- What problem does this solve?
- When should it activate?
- What tools does it need?
- Is it command-style (explicit invocation) or auto-activation?

### 2. Identify Relevant Guidance
Which modules from `~/.config/agent/` apply?
- `core/` - Universal behaviors (methodology, task-management, etc.)
- `domain/` - Domain-specific (coding, testing, review, architecture)
- `workflows/` - Task workflows (feature implementation, etc.)

### 3. Design Skill Structure
- Frontmatter: name, description (with triggers), allowed-tools, metadata
- References section: List all guidance files to read
- Instructions: Skill-specific logic
- Arguments section: How to use ${ARGUMENTS}

### 4. Write SKILL.md File
In chezmoi source: `~/.local/share/chezmoi/home/dot_codex/skills/<name>/SKILL.md`
- Use explicit read instructions (not summaries)
- List ALL relevant guidance files
- Keep instructions focused and minimal
- Reference AGENT.md where applicable

### 5. Apply with Chezmoi
```bash
chezmoi apply ~/.codex
```

### 6. Create References Symlink (if needed)
In deployed directory: `~/.codex/skills/<name>/`
```bash
ln -s ~/.config/agent/domain/path references
```

### 7. Test
- Invoke skill: `$skill-name <arguments>`
- Verify skill activates correctly
- Confirm references are readable
- Validate guidance is being applied

## Existing Guidance Modules

All paths relative to `~/.config/agent/`:

**Core:**
- `core/behavior.md` - Critical thinking, evidence-based reasoning
- `core/communication.md` - Tone, style, conciseness
- `core/methodology.md` - 5-phase problem-solving
- `core/efficiency.md` - Parallelization, throughput
- `core/task-management.md` - TODO discipline
- `core/principles.md` - Engineering principles

**Architecture:**
- `domain/architecture/decomposition.md` - Problem breakdown
- `domain/architecture/parallelization.md` - Concurrent execution

**Coding (General):**
- `domain/coding/workflow.md` - Universal coding workflow
- `domain/coding/quality.md` - Quality priorities
- `domain/coding/safety.md` - Runtime + security safety

**Coding (Go):**
- `domain/coding/go/style.md` - Go code style
- `domain/coding/go/idioms.md` - Go conventions
- `domain/coding/go/concurrency.md` - Go thread safety
- `domain/coding/go/testing.md` - Go test practices
- `domain/coding/go/tooling.md` - Go commands
- `domain/coding/go/organization.md` - Go code structure
- `domain/coding/go/performance.md` - Go optimization

**Testing:**
- `domain/testing/unit.md` - Unit test strategies
- `domain/testing/coverage.md` - Coverage requirements

**Review:**
- `domain/review/process.md` - Review workflow
- `domain/review/priorities.md` - Review focus areas

**Workflows:**
- `workflows/feature.md` - Feature implementation

## Anti-Patterns to Avoid

❌ **Summarizing guidance:**
```markdown
From quality.md, the priorities are: correctness, safety...
```

❌ **Selective quoting:**
```markdown
Key rules: Rule A, Rule B
```

❌ **Using `@` includes (doesn't work in Codex):**
```markdown
Apply all guidance from:
- @~/.config/agent/file.md
```

✅ **Explicit read instructions:**
```markdown
**Read these references:**
- `references/file.md` - Complete guidance on topic
- `~/.config/agent/path/to/file.md` - Full details
```

## Examples

See existing Codex skills:
- `~/.codex/skills/go-development/SKILL.md` - With references symlink
- `~/.codex/skills/go-test/SKILL.md` - Command-style skill
- `~/.codex/skills/problem-solving/SKILL.md` - With multiple references
- `~/.codex/skills/feature/SKILL.md` - Workflow orchestration

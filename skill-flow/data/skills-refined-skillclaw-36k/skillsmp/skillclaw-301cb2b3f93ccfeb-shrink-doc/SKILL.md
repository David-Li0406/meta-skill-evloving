---
name: shrink-doc
description: Use this skill when you need to compress documentation files while ensuring execution equivalence through a validation-driven approach.
---

# Validation-Driven Document Compression

**Task**: Compress the documentation file: `{{arg}}`

**Goal**: Reduce document size while preserving execution equivalence using objective validation instead of prescriptive rules.

---

## Workflow

### Step 1: Validate Document Type

**BEFORE compression**, verify this is a Claude-facing document:

**ALLOWED** (Claude-facing):
- `.claude/` configuration files:
  - `.claude/agents/` - Agent definitions (prompts for sub-agents)
  - `.claude/commands/` - **Slash commands** (prompts that expand when invoked)
  - `.claude/hooks/` - Hook scripts (execute on events)
  - `.claude/settings.json` - Claude Code settings
- `CLAUDE.md` and project instructions
- `docs/project/` development protocol documentation
- `docs/code-style/*-claude.md` style detection patterns

**FORBIDDEN** (Human-facing):
- `README.md`, `changelog.md`, `CHANGELOG.md`
- `docs/studies/`, `docs/decisions/`, `docs/performance/`
- `docs/optional-modules/` (potentially user-facing)
- `todo.md`, `docs/code-style/*-human.md`

**⚠️ SPECIAL HANDLING: CLAUDE.md**

When compressing `CLAUDE.md`, use **content reorganization** instead of standard compression:

### Step 2: Analyze Content Location
Before compressing, categorize ALL content into:

| Category | Action |
|----------|--------|
| **Duplicates skills** | REMOVE - reference skill instead |
| **Main-agent-specific** | MOVE to main-agent-specific file |
| **Sub-agent-specific** | MOVE to sub-agent-specific file |
| **Universal (all agents)** | KEEP in CLAUDE.md |

### Step 3: Check for Duplication
```bash
# Check if content already exists in skills
ls .claude/skills/

# Check if procedural content duplicates a skill
grep -l "pattern" .claude/skills/*/SKILL.md
```

### Step 4: Content Categories

*Examples are illustrative; specific categories vary by project.*

**REMOVE (duplicates existing):**
- Procedural content that exists in skills
- Content already documented in agent-specific files

**MOVE (agent-specific):**
- Main-agent-only content (e.g., multi-agent coordination, repository structure)
- Sub-agent-specific content
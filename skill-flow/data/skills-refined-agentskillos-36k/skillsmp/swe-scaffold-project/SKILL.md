---
name: swe-scaffold-project
version: 1.0.0
description: Initialize workflow for new empty projects. Creates core memories and directory structure.
workflow:
  aware: true
  callable_from:
    - WF_START
    - WF_INITIAL_SETUP
  default_return: WF_START
  supports_standalone: true
  auto_transition: true
---

# Scaffold Project Skill

Initialize workflow system for new or empty projects.

## When to Use

- New projects without existing memories
- Projects missing INDEX_FEATURES
- Converting existing projects to workflow system

## Detection Triggers

Automatically suggested when:
- No `.serena/memories/` directory exists
- No `INDEX_FEATURES.md` file exists
- `INDEX_FEATURES.md` has zero features registered

## Process

### Stage 1: Project Detection

```bash
# Detect project root
git rev-parse --show-toplevel || pwd

# Detect package manager
[ -f "package.json" ] && echo "npm"
[ -f "composer.json" ] && echo "composer"
[ -f "Cargo.toml" ] && echo "cargo"
[ -f "requirements.txt" ] && echo "pip"
[ -f "go.mod" ] && echo "go"

# Detect primary language
find . -name "*.ts" -o -name "*.js" | head -1  # TypeScript/JavaScript
find . -name "*.py" | head -1                   # Python
find . -name "*.php" | head -1                  # PHP
find . -name "*.rs" | head -1                   # Rust
find . -name "*.go" | head -1                   # Go
```

### Stage 2: Directory Setup

```bash
mkdir -p .serena/memories
mkdir -p .claude/skills
mkdir -p .claude/hooks
```

### Stage 3: Core Memory Creation

Create from templates:

1. **_INDEX** - Navigation hub
```markdown
# _INDEX - Memory Navigation

## Quick Reference
- Features: INDEX_FEATURES
- Architecture: ARCH_INDEX
- Workflows: INDEX_WORKFLOWS_STATES

## Memory Types
| Prefix | Purpose |
|--------|---------|
| FEATURE_ | Feature configs |
| DOM_ | Domain behaviors |
| SYS_ | System references |
| REF_ | Reference docs |
| INDEX_ | Navigation |
| WF_ | Workflow states |
| WORKING_MEMORY_ | Session state |
```

2. **INDEX_FEATURES** - Empty feature registry
```markdown
# INDEX_FEATURES

## Registered Features
(none yet - run /swe-onboard-feature to add)

## Quick Start
1. `/swe-onboard-feature [KEY]` - Full wizard
2. `/swe-onboard-quick [KEY]` - Fast setup
```

3. **ARCH_INDEX** - Basic architecture placeholder
```markdown
# ARCH_INDEX - Architecture Overview

## Project Type
[Detected or unknown]

## Primary Language
[Detected]

## Framework
[Detected or none]

## Structure
(Run /swe-onboard-feature to populate)
```

### Stage 4: First Feature Prompt

**PROJECT SCAFFOLDED**

**Created:**
- .serena/memories/
- _INDEX
- INDEX_FEATURES
- ARCH_INDEX

Your project needs at least one feature to enable code changes.

**What is the main codebase?**
- Name: [e.g., "Backend API"]
- Key: [e.g., "BACKEND"]
- Path: [e.g., "src/"]

**Options:**
- **[A]** Set up now with /swe-onboard-feature (recommended)
- **[B]** Quick setup with /swe-onboard-quick
- **[C]** Skip - add features later (research-only mode)

### Stage 5: Optional Swarm Analysis

If swarm MCP available:
```
AI-powered codebase analysis available.

[A] Full DAA analysis (creates DOM_*, SYS_*, detailed INDEX_*)
[B] Quick scan (basic structure)
[C] Skip
```

## Minimal Workflow Mode

If user skips feature setup, enable minimal mode:

```json
{
  "mode": "minimal",
  "allowed_states": ["WF_START", "WF_RESEARCH", "WF_CLARIFY"],
  "blocked_states": ["WF_EXECUTE", "WF_CHECKPOINT"],
  "message": "Feature onboarding required for code changes"
}
```

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-scaffold-project
- **Status**: [success|needs_clarification]
- **Project Root**: [path]
- **Language**: [detected]
- **Framework**: [detected or none]
- **Memories Created**: _INDEX, INDEX_FEATURES, ARCH_INDEX
- **Next Step Hint**: WF_START or /swe-onboard-feature
```

## Exit

`> **Skill /swe-scaffold-project complete** - Project scaffolded, run /swe-onboard-feature to add first feature`

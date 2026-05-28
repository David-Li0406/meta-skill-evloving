---
name: agent-ops-install
description: Use this skill when you need to install the AgentOps framework into a new or existing project, handling both .agent/ setup and .github/ merging intelligently.
---

# AgentOps Installation

## Purpose
Install the AgentOps framework into any project—new or existing—with intelligent merging.

## Installation Modes

### Mode 1: Fresh Install (empty or new folder)
Creates full structure from scratch.

### Mode 2: Merge Install (existing .github/)
Preserves existing content, adds AgentOps alongside it.

### Mode 3: Update Install (existing AgentOps)
Updates skills/prompts to latest versions without touching state files.

---

## Pre-Installation Checklist

Before installing, gather:

1. **Project type** — What language/framework? (affects gitignore suggestions)
2. **Existing CI/CD** — Any workflows in .github/workflows/?
3. **Existing instructions** — Is there a copilot-instructions.md?
4. **Git status** — Is this a git repo? Any uncommitted changes?

---

## Installation Structure

### .agent/ (State - Created Fresh)

```
.agent/
├── constitution.md      # Project-specific rules (from template)
├── memory.md            # Empty, grows over time
├── focus.md             # Empty, session state
├── baseline.md          # Empty, captured on first baseline
├── docs/                # Agent-generated documentation
├── issues/
│   ├── critical.md      # P0 issues
│   ├── high.md          # P1 issues
│   ├── medium.md        # P2 issues
│   ├── low.md           # P3 issues
│   ├── history.md       # Archived issues
│   ├── references/      # Detailed specs for complex issues
│   │   └── README.md
│   └── .counter         # Issue ID counter (starts at 0)
└── specs/               # Requirement specifications
```

### .github/ (Framework - Merged)

```
.github/
├── copilot-instructions.md   # MERGE with existing or create
├── SKILL-TIERS.md            # Skill hierarchy reference
├── skills/                   # All AgentOps skills
│   ├── agent-ops-baseline/
│   ├── agent-ops-constitution/
│   ├── agent-ops-critical-review/
│   ├── agent-ops-dependencies/
│   ├── agent-ops-docs/
│   ├── agent-ops-focus-scan/
│   ├── agent-ops-git/
│   ├── agent-ops-guide/
│   ├── agent-ops-housekeeping/
│   ├── agent-ops-implementation/
│   ├── agent-ops-improvement-discovery/
│   ├── agent-ops-install/
│   ├── agent-ops-interview/
│   ├── agent-ops-planning/
│   ├── agent-ops-recovery/
│   └── ...
```
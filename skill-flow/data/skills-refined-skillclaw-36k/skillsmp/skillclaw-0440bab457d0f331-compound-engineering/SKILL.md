---
name: compound-engineering
description: Use this skill when you want to implement a development methodology that ensures each unit of work makes subsequent work easier through structured phases of research, planning, reviewing, and compounding learnings.
---

# Compound Engineering

Development methodology where each unit of work makes subsequent work easier. Knowledge flows into the codebase itself - CLAUDE.md, folder AGENTS.md, inline comments, tests.

## Core Philosophy

**Each unit of engineering work should make subsequent units easier--not harder.** Traditional development accumulates technical debt. Compound Engineering inverts this by creating a learning loop where every insight gets documented and reused.

**Time allocation:** 40% planning, 20% work, 20% review, 20% compound

## The Loop

```
Research -> Plan -> Work -> Review -> Compound
   ^                                  |
   +----------------------------------+
```

## Phase 1: Research

**Goal:** Understand before building. Research is ephemeral - capture what matters, discard the rest.

### Simple Tasks (< 1 hour)
Quick inline research:
- Search codebase for similar patterns
- Check CLAUDE.md for relevant guidance
- Look for folder AGENTS.md in target directories

### Complex Tasks (> 1 hour)
Spawn parallel Explore agents:

```
Agent 1: "Find patterns for [feature] in src/ - look at similar components, utilities, hooks"
Agent 2: "Check git history: git log --oneline --grep='[related term]' and git log -p [relevant files]"
Agent 3: "Review CLAUDE.md and any AGENTS.md files for guidance on [area]"
```

**Wait for all agents -> Synthesize into brief context**

### Research Output

**Do NOT create scout files.** Instead:
- If you learn something project-wide -> Add to CLAUDE.md
- If you learn something folder-specific -> Add to `src/[folder]/AGENTS.md`
- If it's only relevant for this task -> Keep in working memory, discard after

## Phase 2: Plan

**Goal:** Define what success looks like before writing code.

### Create Task List

Use TodoWrite with clear acceptance criteria:

```
TodoWrite([
  {
    content: "Add validatePhone to src/utils/validation.ts - follow email pattern, handle extensions, add JSDoc",
    status: "pending",
    activeForm: "Adding phone validation utility"
  },
  {
    content: "Add unit tests for validatePhone - valid formats, invalid formats, edge cases (extensions, international)"
  }
])
```
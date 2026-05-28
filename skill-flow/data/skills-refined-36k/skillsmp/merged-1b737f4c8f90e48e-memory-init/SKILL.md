---
name: memory-init
description: Use this skill to initialize the ConKeeper memory system for a project, creating the necessary directory structure and starter files for persistent AI context.
---

# Memory Initialization

Initialize ConKeeper's file-based memory system for this project.

## Pre-flight Checks

1. Confirm the working directory is a project root (has package.json, Cargo.toml, pyproject.toml, go.mod, or similar).
2. Check if `.claude/memory/` already exists:
   - If yes: Ask the user if they want to reset or review current memory.
   - If no: Proceed with initialization.

## Initialization Steps

### Step 1: Create Directory Structure

```bash
mkdir -p .claude/memory/decisions
mkdir -p .claude/memory/sessions
```

### Step 2: Gather Project Context

Ask the user (or infer from the codebase):
- What is this project? (1-2 sentences)
- What's the primary tech stack?
- Any key architectural decisions already made?
- What are you working on right now?

### Step 3: Create Initial Files

**product-context.md** - Populate with gathered info:
```markdown
# Product Context

## Project Overview
<!-- What is this project? What problem does it solve? -->

## Architecture
<!-- High-level architecture description -->

## Key Stakeholders
<!-- Who uses this? Who maintains it? -->

## Constraints
<!-- Technical, business, or regulatory constraints -->

## Non-Goals
<!-- What this project explicitly doesn't do -->

---
*Last updated: [date]*
```

**active-context.md** - Set current focus:
```markdown
# Active Context

## Current Focus
<!-- What are we working on right now? -->

## Recent Decisions
<!-- Decisions made in recent sessions -->

## Open Questions
<!-- Unresolved questions that need answers -->

## Blockers
<!-- What's preventing progress? -->

---
*Session: [date]*
```

**progress.md** - Initialize with known tasks:
```markdown
# Progress Tracker

## In Progress
- [ ] [Initial task if known]

## Completed (Recent)
<!-- Recently completed items -->

## Backlog
<!-- Future tasks -->

---
*Last updated: [date]*
```

**patterns.md** - Document code patterns:
```markdown
# Project Patterns

## Code Conventions
<!-- Coding standards and conventions -->

## Architecture Patterns
<!-- Recurring architectural patterns -->

## Testing Patterns
<!-- Testing conventions -->

---
*Last updated: [date]*
```

**glossary.md** - Project terminology:
```markdown
# Project Glossary

## Terms
| Term | Definition |
|------|------------|
<!-- Add project-specific terminology -->

## Abbreviations
| Abbrev | Expansion |
|--------|-----------|
<!-- Add common abbreviations -->

---
*Last updated: [date]*
```

### Step 4: Configure Token Budget

Ask the user:
> What token budget preset would you like?
> 1. **Economy** (~2000 tokens): Minimal context, fast loading
> 2. **Light** (~3000 tokens): Smaller projects, lighter footprint
> 3. **Standard** (~4000 tokens): Balanced for most projects (default)
> 4. **Detailed** (~6000 tokens): Comprehensive context, rich handoffs

Create `.claude/memory/.memory-config.md` with their choice:
```yaml
---
token_budget: standard
---
```

If the user accepts the default (Standard), this file can be omitted.

### Step 5: Git Handling

Ask the user:
> Should `.claude/memory/` be tracked in git?
> - Yes: Memory persists with repo (recommended for solo projects)
> - No: Add to .gitignore (recommended for shared repos)

If no:
```bash
grep -qxF '.claude/memory/' .gitignore 2>/dev/null || echo '.claude/memory/' >> .gitignore
```

### Step 6: Confirm

Output summary:
> Memory initialized for [project-name]
> - Product context: [summary]
> - Current focus: [focus]
> - Token budget: [economy/light/standard/detailed]
> - Git tracking: [yes/no]
>
> Use memory-sync to update memory as you work.
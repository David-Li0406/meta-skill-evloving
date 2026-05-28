---
name: docs-review
description: Review and improve repository documentation including both human-readable docs (`docs/`), `README.md`, and AI agent memory context files (`CLAUDE.md`, `CODEX.md`, `AGENTS.md`, `.cursorrules`, etc.) for clarity, minimal duplication, and modularity. Use when asked to review, audit, refactor, or improve documentation structure, consolidate rules, reduce redundancy, establish shared standards, or modularize monolithic instruction files.
---

# Documentation Review Skill

Review and improve repository documentation for both human-readable docs and AI agent context files to ensure clarity, minimal duplication, and modularity.

## Target Files

### Human Documentation
- `docs/README.md` — Docs overview + navigation (only file at docs root)
- `docs/onboarding/` — First-time setup guides (experience-agnostic)
- `docs/architecture/` — System design, diagrams, rationale, ADRs
- `docs/standards/` — Shared actionable patterns (humans + agents)
- `README.md` — Project introduction (repo root)

### Agent Context Files
- `CLAUDE.md` — Claude Code project context
- `.claude/rules/*.md` — Modular Claude rules
- `CODEX.md` — OpenAI Codex CLI project context
- `.codex/instructions.md` — Codex instructions file
- `AGENTS.md` — Multi-agent context (shared across tools)
- `.cursor/rules/*.mdc` or `.cursorrules` — Cursor-specific rules
- `.github/copilot-instructions.md` — GitHub Copilot context

**Note:** It's acceptable for `CLAUDE.md`, `CODEX.md`, and `AGENTS.md` to be symlinked to each other if the project uses identical context.

## When to Use This Skill

**Good fit:**
- Repos with scattered or duplicated documentation
- Monolithic CLAUDE.md files (>200 lines)
- Projects needing clear human vs. agent content separation

**May not apply:**
- Small projects with minimal docs (single README is fine)
- Monorepos with per-package documentation conventions
- Projects with intentionally different structures (adapt to their conventions first)

## Docs vs Rules Separation

Many repositories have both human-readable documentation (`docs/`) and agent context files (`.claude/rules/`). Avoid duplication by establishing clear boundaries.

**Important:** If the repo has existing documentation conventions, evaluate whether to adopt them or propose migration. Don't force the recommended structure if the existing approach is working well.

### Recommended Structure

```
repo/
├── docs/
│   ├── README.md                   # Only file at docs root (overview + navigation)
│   │
│   ├── standards/                  # Shared source of truth (humans + agents)
│   │   ├── code-style.md           # No numbered prefix in standards
│   │   ├── api.md
│   │   ├── database.md
│   │   ├── testing.md
│   │   └── git.md
│   │
│   ├── onboarding/                 # Human first-time setup (experience-agnostic)
│   │   ├── 01-getting-started.md   # Numbered files for reading order
│   │   ├── 02-local-development.md
│   │   └── 03-troubleshooting.md
│   │
│   └── architecture/               # System design + decisions
│       ├── 01-overview.md          # High-level diagrams + rationale
│       ├── 02-data-flow.md
│       └── decisions/              # Optional: Architecture Decision Records
│           ├── 001-use-postgresql.md
│           └── 002-event-driven-design.md
│
├── CLAUDE.md                      # Project context (root-level)
└── .claude/
    ├── rules/                      # Agent-only (behavioral)
    │   └── workflow/
    │       ├── testing.md
    │       └── pr-process.md
    └── settings.json
```

### Content Boundaries

| Location | Purpose | Audience | Content Type |
|----------|---------|----------|--------------|
| `docs/README.md` | Overview + navigation | Both | Project summary, links to subfolders |
| `docs/standards/` | Actionable patterns | Both | Do's/don'ts, code examples |
| `docs/onboarding/` | First-time setup | Humans | Step-by-step guides, experience-agnostic |
| `docs/architecture/` | System design | Humans | Diagrams, rationale, ADRs |
| `.claude/rules/` | Agent behavior | Agents | Workflow, constraints, pointers |

### Naming Conventions

**Docs root:** Only `README.md` at docs folder root
- `docs/README.md` — Project overview + navigation to subfolders

**Human doc folders:** No numbered prefix, lowercase names
- `docs/onboarding/`, `docs/architecture/`

**Human doc files:** Numbered prefix for reading order (except in `standards/`)
- `docs/onboarding/01-getting-started.md`, `docs/architecture/02-data-flow.md`

**Standards:** No numbered prefix, organized by domain
- `docs/standards/` — Shared patterns for humans + agents
- `docs/standards/[domain].md` (e.g., `api.md`, `testing.md`)

**Agent context:** Root-level CLAUDE.md for project overview
- `CLAUDE.md` at repository root provides project context

**General rules:**
- Folders: lowercase, single word when possible (`[domain]/`)
- Files: kebab-case, descriptive (`[domain]-patterns.md` not `[abbrev].md`)
- Avoid overly generic names: `[service]-authentication.md` not `auth.md`

### How Each Layer References Standards

**In `docs/architecture/01-overview.md` (human doc):**
```markdown
# Architecture Overview

[Diagrams, rationale, history]

For specific coding patterns, see `docs/standards/`.
For decision rationale, see `docs/architecture/decisions/`.
```

**In `CLAUDE.md` (project context at repo root):**
```markdown
# Project Context

Brief project summary.

## Before You Start

**CRITICAL**: Before making any changes or answering questions about this project, **ALWAYS consult the `docs/` folder first** as it is the source of truth for architectural decisions, conventions, patterns, standards, and project specific workflows

## Standards

Follow all patterns in `docs/standards/`:
- `docs/standards/frontend/` — [list relevant standards]
- `docs/standards/backend/` — [list relevant standards]
- `docs/standards/git.md` — Commit and branching

## Before Marking Complete

- Run linter and test commands and apply any necessary fixes to ensure they pass.
```

### Avoid Auto-Importing Docs

Do not use `@` imports to pull docs into rules:

```markdown
<!-- Avoid: Auto-imports entire doc, bloats context -->
See @docs/standards/api.md for details.

<!-- Prefer: Explicit reference, agent reads if needed -->
For API patterns, consult `docs/standards/api.md`.
```

**Why:**
- Hidden dependencies are hard to audit
- Full doc imported even when only a section is relevant
- Doc changes may unintentionally affect agent behavior

## Review Workflow

### 1. Discovery

Scan the repository for all documentation and agent context files:

```bash
# Find human docs (README + all markdown in docs/)
ls -la README.md 2>/dev/null
find docs/ -type f -name "*.md" 2>/dev/null

# Find agent context files
find . -type f \( \
  -name "CLAUDE.md" -o \
  -name "CODEX.md" -o \
  -name "AGENTS.md" -o \
  -name ".cursorrules" -o \
  -name "copilot-instructions.md" -o \
  -name "*.mdc" \
\) 2>/dev/null

# Check for rules directories
ls -la .claude/rules/ .codex/ .cursor/rules/ 2>/dev/null
```

### 2. Analysis

For each file, evaluate against these criteria:

| Criterion | Check |
|-----------|-------|
| **Clarity** | Instructions are unambiguous and actionable |
| **Scope** | Each file/section has a single, clear purpose |
| **Audience** | Content matches intended audience (human vs agent vs shared) |
| **Duplication** | No repeated content across files |
| **Three-layer separation** | Standards, human docs, and agent rules clearly separated |
| **Modularity** | Related content grouped; unrelated content separated |
| **Naming** | Doc files numbered (`01-overview.md`); standards unnumbered; only README.md at docs root |
| **Discoverability** | File/section names reflect content |
| **Maintainability** | Easy to update without side effects |
| **No auto-imports** | Rules reference docs explicitly, not via `@` |

### 3. Report Format

Generate findings using this structure:

```markdown
## Documentation Review Report

### Files Analyzed
- [list of files with line counts]

### Issues Found

#### Critical (Blocks Agent Effectiveness)
- Issue description → Recommended fix

#### Moderate (Reduces Clarity)
- Issue description → Recommended fix

#### Minor (Optimization Opportunity)
- Issue description → Recommended fix

### Recommendations
1. Prioritized action items
```

## Common Anti-Patterns

### Duplication

**Problem:** Same instruction appears in multiple files.
```
# In CLAUDE.md
Run tests before committing.

# In .claude/rules/testing.md
Always run the test suite before commits.
```

**Solution:** Single source of truth, reference from other locations if needed.

### Monolithic Files

**Problem:** Single file covers unrelated domains.
```
# CLAUDE.md (500+ lines)
## Code Style
## Database Conventions
## API Design
## Testing Strategy
## Git Workflow
## Deployment
```

**Solution:** Extract to `.claude/rules/`:
```
.claude/rules/
├── code-style.md
├── database.md
├── api.md
├── testing.md
└── git.md
```

### Vague Instructions

**Problem:** Non-actionable guidance.
```
Write good code.
Follow best practices.
Keep things clean.
```

**Solution:** Specific, verifiable instructions.
```
Limit functions to 50 lines. Extract helpers for complex logic.
Name boolean variables with is/has/should prefix.
```

### Contradictions

**Problem:** Conflicting rules across files.
```
# In code-style.md
Use 2-space indentation.

# In testing.md
Use 4-space indentation for test files.
```

**Solution:** Resolve conflicts, document exceptions with rationale.

### Stale Context

**Problem:** Outdated instructions that no longer apply.
```
Use [old-library] for [task].  # Project migrated to [new-library]
```

**Solution:** Regular audits, tie instructions to current dependencies.

## Modularization Strategy

### When to Modularize

Modularize when CLAUDE.md exceeds ~200 lines or covers 3+ unrelated domains. See "Recommended Structure" above for the target organization.

### Small Projects: Keep It Simple

For smaller projects, avoid over-engineering. A flat structure works well:

```
.claude/rules/
├── code-style.md
├── api.md
├── testing.md
└── git.md
```

**Signs you don't need the full three-layer structure:**
- Fewer than 10 rule files total
- Single developer or small team
- Limited documentation beyond README
- No existing `docs/` folder

### Cross-References

When rules in one file depend on another:
```markdown
<!-- In testing.md -->
Follow naming conventions from `code-style.md` for test files.
```

## Writing Effective Rules

### Rule Structure

```markdown
## [Category]: [Specific Topic]

[1-2 sentence context if needed]

**Do:**
- Specific actionable instruction
- Another instruction with example

**Don't:**
- Anti-pattern to avoid

**Example:**
[code block or concrete example]
```

### Characteristics of Good Rules

- **Atomic:** One concept per rule
- **Testable:** Can verify compliance
- **Contextual:** Explains "why" when non-obvious
- **Current:** Reflects actual project state

## Refactoring Checklist

When improving existing documentation:

### 1. Discovery
- [ ] Locate all docs (`docs/README.md`, `docs/onboarding/`, `docs/architecture/`, `docs/standards/`) and agent context files (`CLAUDE.md`, `.claude/rules/`, etc.)
- [ ] Identify actionable patterns that belong in `docs/standards/`

### 2. Audit
- [ ] Map content overlap and flag contradictions
- [ ] Flag stale instructions and `@` imports

### 3. Restructure
- [ ] Modularize monolithic files (>200 lines or 3+ domains)
- [ ] Apply naming conventions (numbered doc files, unnumbered folders, domain-organized standards, only README.md at docs root)
- [ ] Ensure three-layer separation (standards / human docs / agent rules)

### 4. Validate
- [ ] Check for orphaned references and broken links
- [ ] Verify CLAUDE.md includes pre-session requirements and post-session checks

### 5. Final Audit Pass
- [ ] Re-run analysis criteria (Review Workflow > Analysis) against all changed files
- [ ] Confirm no new duplication, contradictions, or anti-patterns introduced
- [ ] Verify changes maintain clarity, scope, and discoverability

## Output

After review, provide:

1. **Summary:** Current state assessment (1-2 paragraphs)
2. **Issues:** Categorized list with severity
3. **Proposed Structure:** Directory tree if reorganizing
4. **Migration Plan:** Steps to implement changes safely
5. **Updated Files:** Refactored content (if requested)

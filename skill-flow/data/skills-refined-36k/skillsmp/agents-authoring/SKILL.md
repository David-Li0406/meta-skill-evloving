---
name: agents-authoring
description: Best practices for writing AGENTS.md, agent configs, and skill files based on industry research
---

# AGENTS.md and Skill Authoring

Load this skill when creating or updating AGENTS.md files, OpenCode agents, or skills.

## Research Foundation

This guidance synthesizes:

- [agents.md](https://agents.md) - Open standard used by 60k+ projects, stewarded by Agentic AI
  Foundation under Linux Foundation
- GitHub's analysis of 2,500+ repositories with agents.md files
- Anthropic's context engineering documentation
- OpenAI Codex custom instructions guide
- Devin AI's good vs bad instructions documentation
- Builder.io's AGENTS.md best practices guide

## Core Concept

AGENTS.md is a "README for agents" - a dedicated, predictable place for AI coding agent context.
Supported by: OpenAI Codex, Google Jules, Cursor, VS Code, GitHub Copilot, Devin, Windsurf,
OpenCode, Aider, and many others.

## Essential Sections

Every AGENTS.md should cover:

### 1. Dos and Don'ts (Constraints)

Be nitpicky. Clear guidelines prevent repeated mistakes.

````markdown
### Do
- use TypeScript strict mode
- use functional components with hooks
- default to small, focused diffs

### Don't
- do not hard code colors - use design tokens
- do not add dependencies without approval
````

### 2. File-Scoped Commands

Prefer file-specific commands over project-wide. Faster feedback, fewer wasted cycles.

````markdown
### Commands
# Type check single file (seconds, not minutes)
npm run tsc --noEmit path/to/file.tsx

# Lint single file
npm run eslint --fix path/to/file.tsx

# Test single file
npm run vitest run path/to/file.test.tsx

# Full build only when explicitly requested
npm run build
````

### 3. Safety and Permissions

Explicit allow/ask lists prevent surprises.

````markdown
### Permissions
Allowed without asking:
- read files, list directories
- type check, lint, format single files
- run single unit tests

Ask first:
- package installs
- git push
- deleting files
- full build or E2E suites
````

### 4. Project Structure Hints

A tiny index saves exploration time every session.

````markdown
### Structure
- routes: `src/App.tsx`
- components: `src/components/`
- design tokens: `src/lib/theme/tokens.ts`
- API client: `src/api/client.ts`
````

### 5. Good/Bad Example Pointers

Point to real files. Examples beat abstractions.

````markdown
### Examples
Copy these patterns:
- forms: `src/components/UserForm.tsx`
- data fetching: `src/hooks/useProjects.ts`

Avoid these (legacy):
- class components like `src/legacy/Admin.tsx`
````

### 6. When Stuck Guidance

Escape hatch for uncertainty.

````markdown
### When stuck
- ask a clarifying question
- propose a short plan
- open a draft PR with notes
- do not push large speculative changes
````

### 7. PR/Commit Checklist

Define "ready" explicitly.

````markdown
### PR checklist
- lint, type check, tests: all green
- diff is small and focused
- brief summary of what changed and why
````

## Nested AGENTS.md for Monorepos

Place AGENTS.md in subdirectories for package-specific rules. Agent reads closest file to edited
code. Root file provides defaults; nested files override.

```txt
/root
  AGENTS.md           # Project-wide defaults
  /packages/legacy
    AGENTS.md         # React 17 rules for this package
  /packages/new-app
    AGENTS.md         # React 18 rules for this package
```

## Anthropic Context Engineering Principles

### Clarity at the Right Altitude

- Specific enough to guide behavior effectively
- Flexible enough to provide strong heuristics
- Not so detailed it becomes brittle

### Minimality

- Minimal set of information that fully outlines expected behavior
- Minimal does NOT mean short - it means only necessary information
- Remove redundancy ruthlessly

### Structure

- Organize into distinct sections
- Group related rules together
- Use consistent formatting

## Rule Writing Guidelines

### Format: Constraint + Consequence

Bad: "Don't commit directly to main"

Good: "NEVER commit directly to main - use feature branches and PRs"

### Prefer Positive Over Negative

Bad: "NEVER use var"

Good: "Use `const` by default, `let` when reassignment needed (NEVER `var`)"

### Be Specific, Not Vague

Bad: "Be careful with error handling"

Good: "All async functions MUST have try/catch - unhandled rejections crash the process"

### Use Examples Over Adjectives

Bad: "Write concise commit messages"

Good: "Format: `fix(auth): handle expired tokens`, `feat(api): add search endpoint`"

## Antipatterns

| Antipattern                       | Problem                   | Fix                           |
|-----------------------------------|---------------------------|-------------------------------|
| Verbose explanations              | Wastes tokens             | Terse rule + consequence      |
| Repeated rules                    | Inconsistency risk        | Single authoritative location |
| Vague adjectives                  | Subjective interpretation | Concrete criteria or examples |
| Embedded discoverable info        | Stale, bloated            | Point to source (--help)      |
| Prohibitions without alternatives | No guidance on what TO do | Include correct approach      |
| Project-wide commands only        | Slow feedback loops       | File-scoped commands          |

## OpenCode Agent Structure

OpenCode agents use markdown files with YAML frontmatter:

````markdown
---
description: Brief description of agent purpose
mode: subagent
permission:
  skill:
    "*": deny
    specific-skill: allow
---

# Agent Name

Brief intro. Pointer to load relevant skill.

## Workflow

Mandatory steps before starting work.

## Domain Ownership

Paths this agent is responsible for.

## Constraints

NEVER/MUST rules with consequences.

## Verification

Commands to validate work.

## When Stuck

Escape hatch for uncertainty.
````

### Agent vs Skill Separation

**Agent (always loaded):**

- Workflow/prerequisites (mandatory steps)
- Domain ownership (which paths)
- Hard constraints (NEVER rules)
- Verification commands
- Pointer to skill

**Skill (loaded on demand):**

- Code examples and patterns
- Step-by-step procedures
- File templates
- Debugging guides
- Comprehensive reference

### Decision Heuristic

Ask: "Is this needed in every conversation with this agent?"

- Yes -> Put in agent
- No, only for specific operations -> Put in skill

## OpenCode Skill Structure

### Location

- Project: `.opencode/skills/{name}/SKILL.md`
- Global: `~/.config/opencode/skills/{name}/SKILL.md`

### Frontmatter (Required)

```yaml
---
name: skill-name
description: 1-1024 chars describing when to use this skill
---
```

### Name Rules

- 1-64 characters
- Lowercase alphanumeric with single hyphen separators
- No leading/trailing hyphens, no consecutive hyphens
- Must match directory name

### Body Content

- Start with purpose statement
- Include copy-pasteable examples
- Show pattern variations
- Document common mistakes

## Good vs Bad Instructions (Devin Research)

### Good Instructions

- Name specific files/components
- Reference existing code as templates
- Include clear success criteria
- Define verification steps

Example: "Create endpoint `/users/stats` returning JSON. Reference `/orders/stats` in
`statsController.js` for structure. Add tests to `StatsController.test.js`."

### Bad Instructions

- Vague ("make it user-friendly")
- No specific components mentioned
- Unclear validation criteria
- Open-ended scope

Example: "Add a user stats endpoint." (No format, source, tests, or reference)

## Maintenance

### When to Update

- AGENTS.md: New constraints, infrastructure changes, command changes
- Skills: New patterns, better examples, common mistakes discovered

### Update Process

1. Identify what changed and why
2. Update the authoritative location (not duplicates)
3. Verify no contradictions introduced
4. Validate formatting (markdownlint)

## Validation Checklist

Before finalizing changes:

- [ ] No duplicate rules across agent and skill
- [ ] Each constraint has a consequence
- [ ] Commands are copy-pasteable and file-scoped where possible
- [ ] Examples reference real files (not invented)
- [ ] Skills referenced where detailed patterns live
- [ ] "When stuck" guidance included
- [ ] Line length <= 100 characters
- [ ] Code blocks have language specifiers

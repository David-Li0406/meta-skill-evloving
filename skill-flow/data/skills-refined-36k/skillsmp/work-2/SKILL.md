---
name: work
description: Implement pending tasks using Codex or Gemini, committing after each task. Use when ready to execute planned work. Triggers on "work on tasks", "implement tasks", "start working", "execute the plan", "do the work".
---

# Work Through Tasks

Implement pending tasks one-by-one, committing after each completion.

## Tool Selection

Choose the right tool based on task domain:

| Domain | Tool | Rationale |
|--------|------|-----------|
| Backend, APIs, business logic | Codex | Strong at algorithms, data flow, system design |
| Frontend, UI, visual design | Gemini | Better aesthetic judgment, visual coherence |
| Mixed (e.g., full-stack feature) | Split task or use both sequentially |  |

### Gemini-first tasks

Use `use-gemini` skill when the task involves:

- **Color palettes** - selection, theming, contrast
- **Layouts** - page structure, spacing, visual hierarchy
- **Components** - buttons, forms, cards, any UI elements
- **Typography** - font choices, sizing, readability
- **Animations/transitions** - motion design, timing
- **Responsive design** - breakpoints, mobile adaptation
- **Any user-facing surface** - web pages, GUI, dashboards

### Gemini as design authority

For visual tasks, Gemini can challenge existing specs:

1. Share the planned design/spec with Gemini
2. Ask for critical review before implementation
3. **Trust Gemini's feedback** on visual matters - it has better taste
4. Adjust the plan based on its recommendations
5. Then proceed with implementation

Example prompt addition for visual tasks:

```text
Before implementing, critically review this design spec.
Suggest improvements to colors, spacing, typography, or layout.
Challenge anything that feels generic or could be more distinctive.
```

### Codex-first tasks

Use `use-codex` skill when the task involves:

- Database schemas, migrations
- API endpoints, business logic
- Authentication, authorization
- Data processing, algorithms
- Testing, CI/CD configuration
- Backend infrastructure

## Workflow

### 1. Get pending tasks

Use `TaskList` tool to see all tasks. Filter for:

- Status: `pending`
- No blockers (empty `blockedBy`)
- No owner assigned

### 2. Claim and start task

For the first available task:

1. Use `TaskUpdate` to set `status: in_progress` and claim ownership
2. Use `TaskGet` to read full task description

### 3. Select and invoke tool

**Determine task domain** (see Tool Selection above), then:

**For Codex tasks:**

- Model: `gpt-5.2-codex` (default) or user preference
- Sandbox: `workspace-write` for code changes
- See `references/codex-integration.md`

**For Gemini tasks:**

- Permissions: `--allow-all-tools` for code changes
- Mode: `-p` for non-interactive
- See `references/gemini-integration.md`

### 4. Handle result

| Result | Action |
|--------|--------|
| Success | Continue to step 5 |
| Timeout | Split task (see below), mark original as blocked |
| Context exceeded | Split task, mark original as blocked |
| Error | Report to user, keep task in_progress |

### 5. Commit changes

```bash
git add -A && git commit -m "<type>(<scope>): <description>"
```

Commit message rules:

- Conventional commit format
- One line, no period
- Reference task ID if available

### 6. Mark complete and continue

1. Use `TaskUpdate` to set `status: completed`
2. Return to step 1 for next task
3. Stop when no pending tasks remain

## Task Splitting

When a tool can't complete a task (timeout/context), split it:

1. Analyze what was accomplished
2. Create 2-4 smaller tasks covering remaining work
3. Use `TaskCreate` for each subtask
4. Set dependencies with `TaskUpdate.addBlockedBy` if sequential
5. Mark original task as blocked or completed (if partially done)

### Split criteria

| Original scope | Split into |
|----------------|------------|
| Multiple files | One task per file |
| Multiple features | One task per feature |
| Large refactor | Extract → transform → cleanup |
| Full-stack feature | Backend task (Codex) → Frontend task (Gemini) |

## Reference Files

- `references/codex-integration.md` - Codex prompt templates and patterns
- `references/gemini-integration.md` - Gemini prompt templates and patterns

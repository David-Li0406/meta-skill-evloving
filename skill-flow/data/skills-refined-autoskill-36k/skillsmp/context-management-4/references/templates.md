# Templates

Use these templates to keep a stable prefix while pushing dynamic state to the end.

## Filesystem memory layout

Use a two-layer layout: global (stable) + local (project).

### Global (stable, cross-project)

- `~/.codex/`
  - `context_contract.md` (stable rules + constraints)
  - `prompt_template.md` (stable assembly template)
  - `context_checklist.md` (pre/post checks)

### Local (project-specific)

Create a small, predictable structure:

- `.cache/context/`
  - `todo.md` (goals + checklist; rewritten)
  - `state.md` (current state; rewritten)
  - `decisions.md` (append-only decisions + rationale)
  - `errors.md` (append-only failures + retry notes)
  - `log.md` (append-only: actions/observations pointers)
  - `.lock` (optional lock file for single-writer)
- `.cache/context/run/YYYYMMDD-HHMM/` (per-run artifacts, append-only)

## `.cache/context/todo.md`

```md
# Goal
<one sentence>

# Success criteria
- [ ] <criterion 1>
- [ ] <criterion 2>

# Plan (rewrite as needed)
- [ ] <step 1>
- [ ] <step 2>

# Next action
<exactly one concrete action>
```

## `.cache/context/errors.md`

```md
FAILED: <what failed>
WHY: <best guess>
NEXT: <next attempt>
```

## `.cache/context/state.md`

```md
# Current status
<2-5 bullets>

# Constraints
- <hard constraint>

# Known unknowns
- <question that blocks progress>

# Pointers
- <file path or URL>: <why it matters>
```

## Offload example (large output)

```text
Summary: tool output too large; wrote full log to .cache/context/run/20250123-1030/scan.log
Pointer: .cache/context/run/20250123-1030/scan.log
```

## Prompt assembly (decision step)

Keep everything above `=== DYNAMIC ===` as stable as possible across turns.

```text
<SYSTEM/DEVELOPER PREFIX: stable>
<TOOL DEFINITIONS: stable>

=== DYNAMIC ===
[Task]
<short restatement of current objective>

[Allowed actions]
- allow: <tool group or tool names>
- deny: <tool group or tool names>

[State]
<paste from .cache/context/state.md (short)>

[Todo]
<paste from .cache/context/todo.md (short)>

[Evidence pointers]
- .cache/context/run/<ts>/<file>: <1-line summary>

[Errors to remember]
- <pointer to error log>: <what failed and what changed>

[Next action]
<one concrete action>
```

---
name: planning-with-files
version: "4.0.0"
description: "Manus-style file-based planning for Codex CLI. Stores task_plan.md/findings.md/progress.md under docs/en/developer/plans/<session-hash>/ for durable planning + traceability."
---

# Planning with Files (Codex)

Work like Manus: Use persistent markdown files as your "working memory on disk."
{/* Refactor planning files to live under docs/en/developer/plans/<hash> for traceability. sddsa89612jk4hbwas678 */}

## What This Skill Does (Codex-Compatible)

Codex skills are instruction-only. There are **no automatic hooks** (e.g., "PreToolUse", "Stop").

To get the benefits, you must **manually**:
- Create a **session folder** under `docs/en/developer/plans/<session-hash>/`
- Re-read `task_plan.md` before major decisions
- Update `task_plan.md`, `findings.md`, and `progress.md` throughout the work
- Add the same `<session-hash>` into inline code comments for traceability

## Operational Checklist (Replace Claude Hooks)

When using this skill on a complex task:

1. Create a new session hash (example: `sddsa89612jk4hbwas678`).
2. If `docs/en/developer/plans/<session-hash>/` does not exist, initialize it (script or template copy).
3. Fill `task_plan.md` (goal, phases, key questions) **before** implementing anything.
4. Before major decisions or phase changes, re-read `task_plan.md` (refreshes goals into the attention window).
5. After every 2 information-gathering actions, append key discoveries into `findings.md` (2-Action Rule).
6. After completing a phase, return to the session folder and update:
   - phase status in `task_plan.md`
   - session log + tests in `progress.md`
7. When the task is done, update `docs/en/change-log/0.0.0.md` with the hash + one-line summary + relative link to the plan.

## Important: Where Files Go (Repo Layout)

When using this skill:

- **Skill assets** (templates/scripts/reference) live in: `.codex/skills/planning-with-files/`
  - Templates: `.codex/skills/planning-with-files/templates/`
  - Scripts: `.codex/skills/planning-with-files/scripts/`
- **Your planning files** live in a **hash folder** under: `docs/en/developer/plans/<session-hash>/`

| Location | What Goes There |
|----------|-----------------|
| Skill directory (`.codex/skills/planning-with-files/`) | Templates, scripts, reference docs |
| `docs/en/developer/plans/<session-hash>/` | `task_plan.md`, `findings.md`, `progress.md` |

This ensures your planning files are:
- durable (versionable docs)
- easy to link to (relative links)
- traceable from code via the session hash

## Quick Start

Before ANY complex task:

### Option A: Initialize via Script (Fastest)

Creates `docs/en/developer/plans/<session-hash>/` and copies templates there if missing.
{/* Document docs navigation sync behavior (Mintlify vs Docusaurus). docs/en/developer/plans/dsim8xybp9oa18nz1gfq/task_plan.md dsim8xybp9oa18nz1gfq */}
Also syncs `docs/docs.json` when present (Mintlify) so the new session files are discoverable; if `docs/docs.json` is absent (Docusaurus), the sync step is skipped.

```bash
bash .codex/skills/planning-with-files/scripts/init-session.sh "<session-hash>" "<session-title>"
```

If you need a one-off backfill or want to rebuild the navigation index deterministically:

```bash
bash .codex/skills/planning-with-files/scripts/sync-docs-json-plans.sh
```

### Option B: Copy Templates (Most Detailed)

```bash
mkdir -p docs/en/developer/plans/<session-hash>
cp .codex/skills/planning-with-files/templates/task_plan.md docs/en/developer/plans/<session-hash>/task_plan.md
cp .codex/skills/planning-with-files/templates/findings.md docs/en/developer/plans/<session-hash>/findings.md
cp .codex/skills/planning-with-files/templates/progress.md docs/en/developer/plans/<session-hash>/progress.md
```

Then:

1. **Fill `task_plan.md` first** — Goal, phases, key questions
2. **Re-read plan before decisions** — Refreshes goals in the attention window
3. **Update after each phase** — Mark status complete, log errors
4. **Log discoveries continuously** — `findings.md` for knowledge, `progress.md` for session/test logs

Optional completion check:

```bash
bash .codex/skills/planning-with-files/scripts/check-complete.sh <session-hash>
```

> **Note:** All three planning files should be created in `docs/en/developer/plans/<session-hash>/`, not in your project root and not in the skill folder.

## The Core Pattern

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

## File Purposes

| File | Purpose | When to Update |
|------|---------|----------------|
| `task_plan.md` | Phases, progress, decisions | After each phase |
| `findings.md` | Research, discoveries | After ANY discovery |
| `progress.md` | Session log, test results | Throughout session |

## Traceability: Hash in Inline Comments

To link code changes back to the plan folder, include the session hash in **every changed area** via an inline comment:

{/* Align traceability format with repo-root AGENTS.md (include plan path + hash). docs/en/developer/plans/docsworkflowapi20260121/task_plan.md docsworkflowapi20260121 */}
**Format:** `<one sentence in English> <relative-plan-path> <session-hash>`

**Plan path:** `docs/en/developer/plans/<session-hash>/task_plan.md`

Examples:

- JS/TS/Go: `// Add input validation for webhook payload. docs/en/developer/plans/sddsa89612jk4hbwas678/task_plan.md sddsa89612jk4hbwas678`
- Python/Shell/YAML: `# Document retry backoff behavior. docs/en/developer/plans/sddsa89612jk4hbwas678/task_plan.md sddsa89612jk4hbwas678`
- SQL: `-- Prevent duplicate inserts via unique key. docs/en/developer/plans/sddsa89612jk4hbwas678/task_plan.md sddsa89612jk4hbwas678`
- Markdown: `{/* Explain why this doc section changed. docs/en/developer/plans/sddsa89612jk4hbwas678/task_plan.md sddsa89612jk4hbwas678 */}`

This creates a stable backlink: comment → hash → `docs/en/developer/plans/<hash>/`.

## Release Note Update (Required)

When the task is completed, update `docs/en/change-log/0.0.0.md` with:
- the session hash
- a one-line summary
- a relative link to the plan (recommend linking `task_plan.md`)

Example entry:

```md
- sddsa89612jk4hbwas678: Refactor planning-with-files to store plans in hash folders. ([plan](../developer/plans/sddsa89612jk4hbwas678/task_plan.md))
```

{/* Keep changelog entries clean and single-line (no extra HTML comment lines). l290bb7v758opd6uxu6r */}
> **Note:** Do not add an extra `{/* ... */}` line above changelog bullets. The bullet itself (hash + plan link) is enough traceability.

{/* Prefer stdin to avoid shell expansion when summaries contain code-like characters. l290bb7v758opd6uxu6r */}
> **Tip:** If your summary contains backticks or other shell-sensitive characters, pipe it via stdin: `printf '%s' "<summary>" | bash .codex/skills/planning-with-files/scripts/append-changelog.sh "<hash>"`.

## Critical Rules

### 1. Create Plan First
Never start a complex task without a session folder containing `task_plan.md`. Non-negotiable.

### 2. The 2-Action Rule
> "After every 2 information-gathering actions, IMMEDIATELY save key findings to text files."

This prevents visual/multimodal information from being lost.

### 3. Read Before Decide
Before major decisions, read the plan file. This keeps goals in your attention window.

### 4. Update After Act
After completing any phase:
- Mark phase status: `in_progress` → `complete`
- Log any errors encountered
- Note files created/modified

### 5. Log ALL Errors
Every error goes in the plan file. This builds knowledge and prevents repetition.

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

### 6. Never Repeat Failures
```
if action_failed:
    next_action != same_action
```
Track what you tried. Mutate the approach.

## The 3-Strike Error Protocol

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully
  → Identify root cause
  → Apply targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different method
  → Different tool? Different library?
  → NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions
  → Search for solutions
  → Consider updating the plan

AFTER 3 FAILURES: Escalate to User
  → Explain what you tried
  → Share the specific error
  → Ask for guidance
```

## Read vs Write Decision Matrix

| Situation | Action | Reason |
|-----------|--------|--------|
| Just wrote a file | DON'T read | Content still in context |
| Viewed image/PDF | Write findings NOW | Multimodal → text before lost |
| Browser returned data | Write to file | Screenshots don't persist |
| Starting new phase | Read plan/findings | Re-orient if context stale |
| Error occurred | Read relevant file | Need current state to fix |
| Resuming after gap | Read all planning files | Recover state |

## The 5-Question Reboot Test

If you can answer these, your context management is solid:

| Question | Answer Source |
|----------|---------------|
| Where am I? | Current phase in task_plan.md |
| Where am I going? | Remaining phases |
| What's the goal? | Goal statement in plan |
| What have I learned? | findings.md |
| What have I done? | progress.md |

## When to Use This Pattern

**Use for:**
- Multi-step tasks (3+ steps)
- Research tasks
- Building/creating projects
- Tasks spanning many tool calls
- Anything requiring organization

**Skip for:**
- Simple questions
- Single-file edits
- Quick lookups

## Templates

Copy these templates to start:

- [templates/task_plan.md](templates/task_plan.md) — Phase tracking
- [templates/findings.md](templates/findings.md) — Research storage
- [templates/progress.md](templates/progress.md) — Session logging

## Scripts

Helper scripts for automation:

- `scripts/init-session.sh` — Initialize all planning files
- `scripts/check-complete.sh` — Verify all phases complete
- `scripts/append-changelog.sh` — Append changelog entry (hash + plan link)

## Advanced Topics

- **Manus Principles:** See [reference.md](reference.md)
- **Real Examples:** See [examples.md](examples.md)

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Keep todos only in chat memory | Persist the plan in task_plan.md |
| State goals once and forget | Re-read plan before decisions |
| Hide errors and retry silently | Log errors to plan file |
| Stuff everything in context | Store large content in files |
| Start executing immediately | Create plan file FIRST |
| Repeat failed actions | Track attempts, mutate approach |
| Create planning files in repo root | Create `docs/en/developer/plans/<hash>/` |

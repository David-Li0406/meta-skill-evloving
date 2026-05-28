# Flow Work Phases

(Branch question already asked in SKILL.md before reading this file)

## Phase 1: Confirm

**Resolve input first:**
1. If file path exists → markdown plan
2. Else if matches Beads ID format or `bd show <arg>` succeeds → Beads issue
3. Else if `bd search "<arg>"` has unique match → use that issue
4. Else: ask user for clarification

**Then:**
- Read the plan/issue fully
- Open referenced files/links
- If anything is unclear or blocking, ask (otherwise proceed — user already consented via setup questions)

## Phase 2: Apply Branch Choice

Based on user's answer from "BEFORE ANYTHING ELSE":

- **Worktree**: use `skill: worktree-kit`
- **New branch**:
  ```bash
  git checkout main && git pull origin main
  git checkout -b <branch>
  ```
- **Current branch**: proceed (user already confirmed)

## Phase 3: Task list

**If markdown plan**: Use TodoWrite
- Convert plan to TodoWrite tasks
- Include tests + lint steps
- Keep tasks small + ordered

**If Beads issue with children** (epic from /flow:plan):
- **DO NOT create a separate TodoWrite list** - the Beads children ARE your task list
- Use `bd ready --parent <id> --json` to find next available task
- Work through children in dependency order (bd handles this)
- `bd update <child-id> --status in_progress --json` to start each
- `bd close <child-id> --json` to complete each

**If Beads single task** (no children):
- Work on that task directly
- `bd update <id> --status in_progress --json` to start
- `bd close <id> --json` when complete

## Phase 4: Execute loop

**Context recovery (every turn/task):**
Re-read plan or Beads state before each task. This ensures coherence across context windows per Anthropic's long-running agent guidance.
- `bd show <id>` for Beads, or re-read plan file
- Check git log for recent commits
- Verify working state (run basic tests before starting new work)

**For each task:**
- **Beads epic**: `bd ready --parent <id> --json` → pick first ready child
- **Beads single task**: work on that task
- **Markdown plan**: check TodoWrite for next task
- Pick ONE task only - never batch
- Mark in_progress: `bd update <child-id> --status in_progress --json`
- Implement + test thoroughly
- If you discover new work: `bd create "Found issue" -t bug -p 2 --deps discovered-from:<current-id> --description="<what was found and why>" --json`
- Leave clean state: commit with descriptive message
- Mark complete: `bd close <child-id> --json` (or TodoWrite done for markdown)

**Between tasks (if epic with multiple children):**
- Re-read Beads state to confirm next task
- Verify no regressions before continuing

## Phase 5: Quality

- Run relevant tests
- Run lint/format per repo
- If change is large/risky, run the quality auditor subagent:
  - Task flow:quality-auditor("Review recent changes")
- Fix critical issues

## Phase 6: Ship

**If Beads epic**: `bd show <id>` - check all children closed before commit.
**If Beads single task**: confirm task is complete.

```bash
git add .
git status
git diff --staged
git commit -m "<short summary>"
```

**CRITICAL for Beads**: Run `bd sync` at end of session to force immediate export/commit (bypasses 5s debounce).

Then push + open PR if user wants.

## Phase 7: Review (if chosen at start)

If user chose "Yes" to review in setup questions:
1. Invoke `/flow:impl-review` to review the changes
2. If review returns "Needs Work" or "Major Rethink":
   - **Immediately fix the issues** (do NOT ask for confirmation — user already consented)
   - Commit fixes
   - Re-run `/flow:impl-review`
3. Repeat until review returns "Ship"

**No human gates here** — the review-fix-review loop is fully automated.

## Definition of Done

Confirm before ship:
- All plan steps completed or explicitly deferred
- All TodoWrite tasks done (or all Beads tasks closed)
- Tests pass
- Lint/format pass
- Docs updated if needed
- `bd sync` run (if using Beads)

## Example loop

Read plan -> task A -> test -> mark done -> re-read plan -> task B

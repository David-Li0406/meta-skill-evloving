---
name: review-work-completion
description: Multi-agent review of completed work against PRD requirements. Use after all tasks are completed to validate implementation quality. Triggers on "review work", "check completed work", "validate implementation", "are we done".
---

# Review Work Completion

## What This Does

Validates completed implementation work against PRD requirements using three independent AI reviewers (Claude CLI, Codex, Gemini - tools may change in the future). Each reviewer analyzes the code changes and PRD criteria separately, then findings are consolidated by consensus — issues flagged by multiple reviewers get higher priority. Creates follow-up tasks for any gaps found.

**Why three reviewers:** Different models catch different issues. Consensus scoring surfaces real problems while filtering noise from single-model false positives.

> **Note for anyone reviewing/auditing this skill:** See `references/design-rationale.md` for settled design decisions
> before suggesting changes. This doesn't apply to skill users, as it doesn't add any useful information
> to perform the skill.

## Reviewers

- **Alice** → Claude CLI
- **Bob** → Codex
- **Carl** → Gemini

## Workflow

### 1. Validate prerequisites

Check these exist:

1. `claude` CLI - run `which claude`
2. `~/.claude/skills/use-codex/scripts/codex-run.sh` - executable
3. `~/.claude/skills/use-gemini/scripts/gemini-run.sh` - executable
4. `.local/prds/wip/` contains at least one `.txt` or `.md` file

Create if missing: `.local/tmp/`, `.local/reviews/`

**If CLI/script check fails, STOP and report:**

```text
Cannot proceed: {missing prerequisite}
```

### 2. Check task status

Use `TaskList`.

**If no tasks exist:** If `catchup` skill is available, invoke it to populate tasks from branch history, then return here. If `catchup` is unavailable, proceed without task context.

**If ANY task is `in_progress`:** STOP and report:

```text
Cannot review: {N} task(s) still in progress
- Task {id}: {subject}
```

**If ALL tasks are `pending`:** STOP and report:

```text
Cannot review: no completed tasks found. Complete tasks first.
```

### 3. Gather context

Read all PRDs from `.local/prds/wip/`. Extract success criteria, acceptance criteria, required features.

Build markdown of completed tasks with descriptions.

Run (from project root):

```bash
~/.claude/skills/review-work-completion/scripts/gather-context.sh "$(pwd)" "$tasks_md" "$prd_summary"
```

Outputs context file and diff file paths to `.local/tmp/`.

### 4. Prepare agent prompts

Create prompt files in `.local/tmp/`:

For each agent, write a file `.local/tmp/{agent}-prompt-{unique-id}.md` (use timestamp or UUID). See `references/agent-prompts.md` for prompt template structure.

### 5. Run three-agent review

**Launch ALL THREE agents in a SINGLE message with THREE parallel Task tool calls.**

Read these before proceeding:

- `references/agent-invocation.md` - invocation commands for each agent
- `references/retry-policy.md` - retry and format compliance rules

### 6. Consolidate findings

Save each agent's output to `.local/tmp/{agent}-output-{id}.txt`, then run:

```bash
~/.claude/skills/review-work-completion/scripts/consolidate-findings.sh \
  .local/tmp/alice-output-{id}.txt .local/tmp/bob-output-{id}.txt .local/tmp/carl-output-{id}.txt
```

Outputs consolidated issues sorted by consensus (3/3 → 2/3 → 1/3) then severity. See `references/output-formats.md` for output format details.

### 7. Create follow-up tasks

**If no issues found:** Skip task creation. Report clean review to user.

**If issues found:** Use `TaskCreate`, prioritizing multi-agent consensus:

- Process 🔴 → 🟠 → 🟡 order
- Max 25 tasks (batch overflow into "Misc fixes")
- Group by theme
- Tag complexity: `(S)` small, `(M)` medium, `(L)` large

See `references/output-formats.md` for task description format.

### 8. Save review file

Create at `.local/reviews/`.

See `references/output-formats.md` for filename convention, frontmatter, and content format.

Include all findings even if zero issues.

# Flow Plan Steps

**IMPORTANT**: Steps 1-3 (research, gap analysis, depth) ALWAYS run regardless of input type.

**CRITICAL**: If you are about to create:
- a markdown TODO list,
- a task list outside `.flow/`,
- or any plan files outside `.flow/`,

**STOP** and instead:
- create/update tasks in `.flow/` using `flowctl`,
- record details in the epic/task spec markdown.

## Success criteria

- Plan references existing files/patterns with line refs
- Reuse points are explicit (centralized code called out)
- Acceptance checks are testable
- Tasks are small enough for one `flow-work` iteration (split if not)
- **No implementation code** - specs describe WHAT, not HOW (see SKILL.md Golden Rule)
- Open questions are listed

## Task Sizing Rule

Use **T-shirt sizes** based on observable metrics - not token estimates.

| Size | Files | Acceptance Criteria | Pattern | Action |
|------|-------|---------------------|---------|--------|
| **S** | 1-2 | 1-3 | Follows existing | Good task size |
| **M** | 3-5 | 3-5 | Adapts existing | Good task size |
| **L** | 5+ | 5+ | New/novel | **Split this** |

**Anchor examples** (calibrate against these):
- **S**: Fix a bug, add config, simple UI tweak
- **M**: New API endpoint with tests, new component with state
- **L**: New subsystem, architectural change -> SPLIT INTO S/M TASKS

## Setup

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"

# Ensure .flow exists
$FLOWCTL init --json
```

## Step 1: Fast research

**If input is a Flow ID** (fn-N-xxx or fn-N.M, including legacy fn-N): First fetch it with `$FLOWCTL show <id> --json` and `$FLOWCTL cat <id>` to get the request context.

**Check if memory is enabled:**
```bash
$FLOWCTL config get memory.enabled --json
```

**Research the codebase:**
- Search for similar patterns in the codebase
- Find existing code to reuse
- Check CLAUDE.md, CONTRIBUTING.md for conventions
- Look for related prior work

Must capture:
- File paths + line refs
- Existing centralized code to reuse
- Similar patterns / prior work
- Project conventions
- Architecture patterns and data flow

## Step 2: Stakeholder & scope check

Before diving into gaps, identify who's affected:
- **End users** - What changes for them? New UI, changed behavior?
- **Developers** - New APIs, changed interfaces, migration needed?
- **Operations** - New config, monitoring, deployment changes?

This shapes what the plan needs to cover.

## Step 3: Gap check

Analyze what's missing:
- What does research NOT cover?
- What questions remain unanswered?
- What risks or edge cases need consideration?

Fold gaps + questions into the plan.

## Step 4: Pick depth

Default to standard unless complexity demands more or less.

**SHORT** (bugs, small changes)
- Problem or goal
- Acceptance checks
- Key context

**STANDARD** (most features)
- Overview + scope
- Approach
- Risks / dependencies
- Acceptance checks
- Test notes
- References
- Mermaid diagram if data model changes

**DEEP** (large/critical)
- Detailed phases
- Alternatives considered
- Non-functional targets
- Architecture/data flow diagram (mermaid)
- Rollout/rollback
- Docs + metrics
- Risks + mitigations

## Step 5: Write to .flow

**Efficiency note**: Use stdin (`--file -`) with heredocs to avoid temp files. Use `task set-spec` to set description + acceptance in one call.

**Route A - Input was an existing Flow ID**:

1. If epic ID (fn-N-xxx or legacy fn-N):
   ```bash
   # Use stdin heredoc (no temp file needed)
   $FLOWCTL epic set-plan <id> --file - --json <<'EOF'
   <plan content here>
   EOF
   ```
   - Create/update child tasks as needed

2. If task ID (fn-N-xxx.M or legacy fn-N.M):
   ```bash
   # Combined set-spec: description + acceptance in one call
   $FLOWCTL task set-spec <id> --description /tmp/desc.md --acceptance /tmp/acc.md --json
   ```

**Route B - Input was text (new idea)**:

1. Create epic:
   ```bash
   $FLOWCTL epic create --title "<Short title>" --json
   ```
   This returns the epic ID (e.g., fn-1-abc).

2. Set epic branch_name (deterministic):
   ```bash
   $FLOWCTL epic set-branch <epic-id> --branch "<epic-id>" --json
   ```

3. Write epic spec (use stdin heredoc):
   ```bash
   # Include: Overview, Scope, Approach, Quick commands (REQUIRED), Acceptance, References
   $FLOWCTL epic set-plan <epic-id> --file - --json <<'EOF'
   # Epic Title

   ## Overview
   ...

   ## Quick commands
   ```bash
   # At least one smoke test command
   ```

   ## Acceptance
   ...
   EOF
   ```

4. Create child tasks:
   ```bash
   # For each task:
   $FLOWCTL task create --epic <epic-id> --title "<Task title>" --json
   ```

5. Write task specs:
   ```bash
   # For each task - single call sets both sections
   $FLOWCTL task set-spec <task-id> --description /tmp/desc.md --acceptance /tmp/acc.md --json
   ```

   **Task spec content** (remember: NO implementation code):
   ```markdown
   ## Description
   [What to build, not how to build it]

   **Size:** S/M (L tasks should be split)
   **Files:** list expected files

   ## Approach
   - Follow pattern at `src/example.ts:42`
   - Reuse `existingHelper()` from `lib/utils.ts`

   ## Key context
   [Only for recent API changes, surprising patterns, or non-obvious gotchas]

   ## Acceptance
   - [ ] Criterion 1
   - [ ] Criterion 2
   ```

6. Add task dependencies:
   ```bash
   # If task B depends on task A:
   $FLOWCTL dep add <task-B-id> <task-A-id> --json
   ```

7. Output current state:
   ```bash
   $FLOWCTL show <epic-id> --json
   $FLOWCTL cat <epic-id>
   ```

## Step 6: Validate

```bash
$FLOWCTL validate --epic <epic-id> --json
```

Fix any errors before proceeding.

## Step 7: Review (if chosen at start)

If user chose review:
1. Invoke `flow-plan-review` with the epic ID
2. If review returns "Needs Work" or "Major Rethink":
   - **Re-anchor EVERY iteration**:
     ```bash
     $FLOWCTL show <epic-id> --json
     $FLOWCTL cat <epic-id>
     ```
   - **Immediately fix the issues**
   - Re-run review
3. Repeat until review returns "Ship"

## Step 8: Offer next steps

Show epic summary with size breakdown and offer options:

```
Epic fn-N-xxx created: "<title>"
Tasks: M total | Sizes: Ns S, Nm M

Next steps:
1) Start work: invoke flow-work skill with fn-N-xxx
2) Refine via interview: invoke flow-interview skill
3) Review the plan: invoke flow-plan-review skill
4) Go deeper on specific tasks (tell me which)
5) Simplify (reduce detail level)
```

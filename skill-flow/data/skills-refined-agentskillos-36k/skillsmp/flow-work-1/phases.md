# Flow Work Phases

(Branch question already asked in SKILL.md before reading this file)

**CRITICAL**: If you are about to create:
- a markdown TODO list,
- a task list outside `.flow/`,
- or any plan files outside `.flow/`,

**STOP** and instead:
- create/update tasks in `.flow/` using `flowctl`,
- record details in the epic/task spec markdown.

## Setup

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"
```

## Phase 1: Resolve Input

Detect input type in this order (first match wins):

1. **Flow task ID** `fn-N-xxx.M` (e.g., fn-1-abc.3) or legacy `fn-N.M` -> **SINGLE_TASK_MODE**
2. **Flow epic ID** `fn-N-xxx` (e.g., fn-1-abc) or legacy `fn-N` -> **EPIC_MODE**
3. **Spec file** `.md` path that exists on disk -> **EPIC_MODE**
4. **Idea text** everything else -> **EPIC_MODE**

**Track the mode** - it controls looping in Phase 3.

---

**Flow task ID (fn-N-xxx.M or fn-N.M)** -> SINGLE_TASK_MODE:
- Read task: `$FLOWCTL show <id> --json`
- Read spec: `$FLOWCTL cat <id>`
- Get epic from task data for context: `$FLOWCTL show <epic-id> --json && $FLOWCTL cat <epic-id>`
- **This is the only task to execute** - no loop to next task

**Flow epic ID (fn-N-xxx or fn-N)** -> EPIC_MODE:
- Read epic: `$FLOWCTL show <id> --json`
- Read spec: `$FLOWCTL cat <id>`
- Get first ready task: `$FLOWCTL ready --epic <id> --json`

**Spec file start (.md path that exists)**:
1. Check file exists: `test -f "<path>"` - if not, treat as idea text
2. Initialize: `$FLOWCTL init --json`
3. Read file and extract title from first `# Heading` or use filename
4. Create epic: `$FLOWCTL epic create --title "<extracted-title>" --json`
5. Set spec from file: `$FLOWCTL epic set-plan <epic-id> --file <path> --json`
6. Create single task: `$FLOWCTL task create --epic <epic-id> --title "Implement <title>" --json`
7. Continue with epic-id

**Spec-less start (idea text)**:
1. Initialize: `$FLOWCTL init --json`
2. Create epic: `$FLOWCTL epic create --title "<idea>" --json`
3. Create single task: `$FLOWCTL task create --epic <epic-id> --title "Implement <idea>" --json`
4. Continue with epic-id

## Phase 2: Apply Branch Choice

Based on user's answer from setup questions:

- **New branch**:
  ```bash
  git checkout main && git pull origin main
  git checkout -b <branch>
  ```
- **Current branch**: proceed (user already confirmed)
- **Isolated worktree**: create worktree in separate directory

## Phase 3: Task Loop

**For each task**, implement with focused context.

### 3a. Find Next Task

```bash
$FLOWCTL ready --epic <epic-id> --json
```

If no ready tasks, go to Phase 4 (Quality).

### 3b. Start Task

```bash
$FLOWCTL start <task-id> --json
```

### 3c. Implement Task

For each task:

1. **Re-anchor**: Read the task spec and epic context
   ```bash
   $FLOWCTL show <task-id> --json
   $FLOWCTL cat <task-id>
   $FLOWCTL show <epic-id> --json
   $FLOWCTL cat <epic-id>
   ```

2. **Check git state**:
   ```bash
   git status
   git log -5 --oneline
   ```

3. **Capture base commit** (for scoped review):
   ```bash
   BASE_COMMIT=$(git rev-parse HEAD)
   ```

4. **Implement**: Read relevant code, implement the feature/fix. Follow existing patterns.

5. **Commit**:
   ```bash
   git add -A
   git commit -m "feat(<scope>): <description>

   - <detail 1>
   - <detail 2>

   Task: <task-id>"
   ```

6. **Review** (if enabled): Run implementation review, fix until SHIP verdict.

### 3d. Complete Task

Write evidence and complete:

```bash
COMMIT_HASH=$(git rev-parse HEAD)

cat > /tmp/evidence.json << EOF
{"commits": ["$COMMIT_HASH"], "tests": ["<test commands run>"], "prs": []}
EOF

cat > /tmp/summary.md << 'EOF'
<1-2 sentence summary>
EOF

$FLOWCTL done <task-id> --summary-file /tmp/summary.md --evidence-json /tmp/evidence.json
```

### 3e. Verify Completion

```bash
$FLOWCTL show <task-id> --json
```

If status is not `done`, investigate and retry.

### 3f. Loop or Finish

**SINGLE_TASK_MODE**: After 3e, go to Phase 4 (Quality). No loop.

**EPIC_MODE**: After 3e, return to 3a for next task.

## Phase 4: Quality

After all tasks complete (or periodically for large epics):

- Run relevant tests
- Run lint/format per repo
- Fix critical issues

## Phase 5: Ship

**Verify all tasks done**:
```bash
$FLOWCTL show <epic-id> --json
$FLOWCTL validate --epic <epic-id> --json
```

**Final commit** (if any uncommitted changes):
```bash
git add -A
git status
git diff --staged
git commit -m "<final summary>"
```

**Do NOT close the epic here** unless the user explicitly asked.

Then push + open PR if user wants.

## Definition of Done

Confirm before ship:
- All tasks have status "done"
- `$FLOWCTL validate --epic <id>` passes
- Tests pass
- Lint/format pass
- Docs updated if needed
- Working tree is clean

## Example flow

```
Phase 1 (resolve) -> Phase 2 (branch) -> Phase 3:
  |-- 3a-c: find task -> start -> implement
  |-- 3d: complete task
  |-- 3e: verify done
  |-- 3f: EPIC_MODE? -> loop to 3a | SINGLE_TASK_MODE? -> Phase 4
  |-- no more tasks -> Phase 4 (quality) -> Phase 5 (ship)
```

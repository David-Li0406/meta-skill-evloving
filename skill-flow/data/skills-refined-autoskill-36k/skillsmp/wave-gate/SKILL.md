---
name: wave-gate
version: "1.0.0"
description: "Run after wave implementation complete. Executes test + review gate sequence. Usage: /wave-gate"
tools: [Read, Bash, Task, Write]
---

# Wave Gate - Test & Review Sequence

Executes the gate sequence after all wave tasks reach "implemented". Handles tests, parallel code review, finding aggregation, GH comment, and wave advancement.

**Run this after SubagentStop hook outputs "Wave N implementation complete".**

---

## Sequence

### Step 1: Verify State

```bash
cat .claude/state/active_task_graph.json | jq '{wave: .current_wave, impl_complete: .wave_gates[.current_wave | tostring].impl_complete}'
```

Abort if `impl_complete != true`.

### Step 2: Run Integration Tests

**First check if already passed** (for re-runs after fixing issues):
```bash
jq -r '.wave_gates[(.current_wave | tostring)].tests_passed' .claude/state/active_task_graph.json
```
If `true`, skip to Step 3.

**Otherwise**, detect and run project test suite:
- `package.json` → `npm test`
- `build.gradle` / `build.gradle.kts` → `./gradlew test`
- `pom.xml` → `./mvnw test`
- `Cargo.toml` → `cargo test`
- `pyproject.toml` / `setup.py` → `pytest`

Run via Bash. Then:

```bash
# If tests pass
bash ~/.claude/hooks/helpers/mark-tests-passed.sh

# If tests fail
bash ~/.claude/hooks/helpers/mark-tests-passed.sh --failed
```

**If tests fail → STOP. Inform user. Do not proceed to review.**

### Step 3: Spawn Reviewers (Parallel)

Get wave tasks from state. **On re-run, only review tasks with `review_status == "blocked"`.**

```bash
# Get tasks needing review (all on first run, only blocked on re-run)
WAVE=$(jq -r '.current_wave' .claude/state/active_task_graph.json)
jq -r ".tasks[] | select(.wave == $WAVE) | select(.review_status == \"pending\" or .review_status == \"blocked\") | .id" .claude/state/active_task_graph.json
```

For EACH task needing review, spawn `task-reviewer` agent in **single message with multiple Task calls**:

```markdown
## Task: {task_id}
**Description:** {task description}

## Files to Review
{files changed by this task - identify from git diff/log}

## Context
- Wave: {N}
- Plan: {path to plan file from state}
```

The `task-reviewer` agent:
- Invokes `/review-pr` scoped to those files
- Outputs findings in standardized format with CRITICAL_COUNT/ADVISORY_COUNT

### Step 4: Parse & Store Findings

For each reviewer output, extract findings and pipe to store script (handles special chars safely):

```bash
bash ~/.claude/hooks/helpers/store-review-findings.sh --task T1 <<'EOF'
CRITICAL: SQL injection in query builder at UserRepo.java:45
CRITICAL: Missing authorization check on /api/admin endpoint
ADVISORY: Consider extracting validation logic to separate class
EOF
```

Format: Each line starts with `CRITICAL:` or `ADVISORY:` followed by the finding.

### Step 5: Post GH Comment

Get issue number from state. Post review summary:

```bash
gh issue comment {ISSUE} --body "$(cat <<'EOF'
## Wave {N} Review

### T1: {description}
**Status:** ✅ Passed | ❌ {N} critical findings
- {findings list}

### T2: {description}
...

---
**Wave Status:** ✅ Ready to advance | ❌ Blocked - fix critical issues
EOF
)"
```

### Step 6: Advance or Block

Check if any task has critical findings:

```bash
# Check state for critical findings (get wave first, then filter)
WAVE=$(jq -r '.current_wave' .claude/state/active_task_graph.json)
jq "[.tasks[] | select(.wave == $WAVE) | .critical_findings | length] | add // 0" .claude/state/active_task_graph.json
```

**If 0 critical findings:**
```bash
bash ~/.claude/hooks/helpers/complete-wave-gate.sh
```
Output: "Wave N complete. Ready for wave N+1."

**If critical findings exist:**
Output blocked status with list of what to fix. Do NOT advance.

---

## Re-review After Fixes

When user fixes critical issues, run `/wave-gate` again. It will:
- Skip tests if already passed (`tests_passed == true`)
- Re-review ONLY tasks with `review_status == "blocked"`
- Advance when all clear

---

## Constraints

- MUST spawn all reviewers in parallel (single message)
- MUST use helper scripts for state updates
- MUST post GH comment before advancing
- NEVER advance if critical findings exist
- NEVER skip tests (unless already passed this wave)

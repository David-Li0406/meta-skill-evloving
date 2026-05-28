---
model: sonnet
allowed-tools: Task, Glob, Grep, Read, Write, Edit, Bash, AskUserQuestion, TodoWrite
argument-hint: <spec file> [--incremental]
description: Execute spec with atlas pattern guidance (auto-creates implementation branch)
---

## Context

Arguments: `/navigator:build <SPEC_FILE>`
- **<spec_file>** - Path to spec file (e.g., `specs/add-user-profile.md`)

Current directory: !`pwd`
Current branch: !`git branch --show-current`

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**If atlas not found:**
```
❌ Atlas required for navigator commands.

Run `/cartographer:chart` to generate an atlas first.
```
**STOP** - Do not proceed without atlas.

**Verify spec file exists:**
```bash
test -f "{spec_file}" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found → Error: "Spec file not found: {spec_file}"

### 2. Load Context

**Read spec file:**
- Parse all sections
- Extract prerequisites, steps, validation commands
- Identify domains and patterns referenced
- Extract composition ID if present in spec

**Load atlas files:**
- `.claude/skills/atlas/SKILL.md`
- `.claude/skills/atlas/references/schema.yaml` - Unified codebase structure
- Relevant domain references (from spec "Atlas Context" section)
- Relevant pattern guides (from spec "Pattern Guides" section)

**Extract from schema.yaml patterns section for each pattern in spec:**
- File conventions (where to create files)
- Test conventions (where to create tests)
- Registration steps (where to wire up new code)
- Validation commands (how to verify each pattern)

### 3. Verify Prerequisites

**Phase 0: Run spec verification commands:**
If spec has a "Prerequisites > Verification" section with commands:
```bash
{verification_commands_from_spec}
```
- Parse output for ❌ MISSING indicators
- Collect all failures before reporting

**Check prerequisite files:**
```bash
test -f "{prerequisite_file}" && echo "✅ EXISTS" || echo "❌ MISSING"
```

**Check prerequisite patterns (from spec):**
For each required pattern, verify key files exist in expected locations.

**If ANY prerequisites missing:**
```
❌ Prerequisites not met

Missing Files:
- {file1} - {why_needed}
- {file2} - {why_needed}

Missing Patterns:
- {pattern} - {why_needed}

⛔ Cannot proceed until prerequisites are resolved.
```

**Use AskUserQuestion:**
```
How would you like to proceed?
1. Abort - I'll complete prerequisites first
2. Skip prerequisites (risky - may cause implementation failures)
3. Show me what's missing in detail
```

If user selects "Abort" → **EXIT** with clear message about what to complete first.
If user selects "Skip" → Continue with warning logged.

### 4. Setup Implementation Branch

**Extract branch info from spec:**
- `{target_branch}` - Implementation Branch from spec
- `{base_branch}` - Base Branch from spec

**Check current git state:**
```bash
git status --porcelain
git branch --show-current
```

**Handle dirty working directory:**

| Current Branch | Working Dir | Action |
|---------------|-------------|--------|
| target_branch | clean | Proceed |
| target_branch | dirty | Ask: "Uncommitted changes detected. Stash, commit, or continue?" |
| other branch | clean | Checkout/create target branch |
| other branch | dirty | Ask: "Uncommitted changes on {current}. Stash, commit, or abort?" |

**If dirty and user chooses stash:**
```bash
git stash push -m "navigator-build: auto-stash before switching to {target_branch}"
```

**Check if target branch exists:**
```bash
git rev-parse --verify {target_branch} 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

**If target branch does NOT exist:**
1. Verify base branch exists:
   ```bash
   git rev-parse --verify {base_branch} 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
   ```
   If base branch not found → Error: "Base branch '{base_branch}' does not exist"

2. Check if base branch is current (warn if stale):
   ```bash
   git log {base_branch}..origin/{base_branch} --oneline 2>/dev/null | head -5
   ```
   If commits exist → Warn: "⚠️ Base branch may be behind remote. Consider `git pull` first."

3. Create target branch from base branch:
   ```bash
   git checkout -b {target_branch} {base_branch}
   ```

**If target branch EXISTS:**
```bash
git checkout {target_branch}
```

**Verify on correct branch:**
```bash
git branch --show-current
```
Must match `{target_branch}` before proceeding.

**Report branch status:**
```
✅ On branch: {target_branch}
   Based on: {base_branch}
   Working directory: clean
```

### 5. Load Pattern Guidance (Atlas-First)

**Research Priority for Implementation Questions:**

| Priority | Source | Purpose |
|----------|--------|---------|
| 1. PRIMARY | schema.yaml patterns | File conventions, registration, validation |
| 2. SECONDARY | Pattern guides (references/patterns/*.md) | Templates, checklists, anti-patterns |
| 3. TERTIARY | example_files from schema.yaml | Reference implementations |
| 4. QUATERNARY | observations.md | Stack-specific notes and decisions |
| 5. EXTERNAL | Context7/web | Only if atlas doesn't cover it |

**Always cite atlas sources in implementation:**
```
// Following schema.yaml patterns.controllers.file_convention
// See references/patterns/controllers.md for template
```

**For each pattern in spec, load from schema.yaml patterns section:**
```yaml
{pattern_id}:
  file_convention: "{where to create file}"
  test_convention: "{where to create test}"
  registration:
    - file: "{registration file}"
      action: "{what to do}"
  validation_commands:
    - "{command 1}"
    - "{command 2}"
  example_files:
    - "{reference implementation to study}"
  anti_patterns_summary:
    - "{what to avoid}"
```

**For each pattern guide referenced in spec:**
- Read full pattern guide from `references/patterns/{pattern_id}.md`
- Extract codebase-specific template
- Extract implementation checklist
- Note anti-patterns to avoid

**Build guidance context:**
```
When implementing {pattern_name}:

File Conventions (from schema.yaml patterns):
- Create file at: {file_convention}
- Create test at: {test_convention}

Registration Steps:
- {action} in {file}

Reference Implementation (study before writing):
- {example_file}

Anti-Patterns to Avoid:
- {anti_pattern_1}
- {anti_pattern_2}

Checklist (from pattern guide):
- [ ] {checklist item 1}
- [ ] {checklist item 2}
```

### 6. Execute Steps (Incremental Mode)

**Execution Protocol with TodoWrite Tracking:**

```
1. Parse spec into discrete steps
2. Create TodoWrite with all steps
3. For each step:
   a. Mark step in_progress in TodoWrite
   b. Load relevant pattern guidance from schema.yaml
   c. Execute the step
   d. Run step-specific validation if defined
   e. If validation passes:
      - Commit with message: "[domain] step description"
      - Mark checkbox in spec file: `[x]`
      - Mark step completed in TodoWrite
   f. If validation fails:
      - Report failure, keep step in_progress
      - Allow retry (max 3 attempts)
4. Run full validation sequence at end
```

**For each step in spec:**

1. **Update TodoWrite:**
   ```
   Mark step {N} as in_progress
   ```

2. **Announce step:**
   ```
   ### Step {N}: {Step Title}
   ```

3. **Load relevant context (Atlas-First):**
   - Read files mentioned in step
   - Apply pattern guidance from schema.yaml patterns section
   - Study example_files if implementing new pattern
   - Review anti_patterns_summary to avoid common mistakes

4. **Implement changes:**
   - Follow spec instructions precisely
   - Use file_convention from schema.yaml patterns for new files
   - Use test_convention for test files
   - Adhere to pattern conventions from pattern guide
   - Write clean, documented code

5. **Complete registration steps:**
   - For each registration in schema.yaml patterns for this pattern
   - Perform {action} in {file}

6. **Verify step completion:**
   - Check expected outcome
   - Run pattern-specific validation_commands from schema.yaml patterns
   - Fix any issues before proceeding (max 3 attempts)

7. **Commit step (if validation passes):**
   ```bash
   git add {files_changed}
   git commit -m "[{domain}] {step_description}"
   ```

8. **Update spec file checkbox:**
   - Edit spec file to mark step complete: `- [x] Step {N}`

9. **Update TodoWrite:**
   ```
   Mark step {N} as completed
   ```

10. **Report progress:**
    ```
    ✅ Step {N} complete: {brief summary}
    - Files created: {list}
    - Registration: {completed steps}
    - Validation: {pass/fail}
    - Committed: {commit_hash}
    ```

**If step fails after 3 attempts:**
- Keep step as in_progress in TodoWrite
- Report specific error
- Ask user how to proceed
- Create blocking issue note in spec

**Spec File Step Format:**
```markdown
## Implementation Steps
- [ ] Step 1: Create user model
- [ ] Step 2: Add validation
- [x] Step 3: Write tests (completed)
```

### 7. Run Validation

**Validation protocol with retry limits:**

For each validation command, use this retry loop:

```
validation_results = []

for each command in [type_check, test, lint, build]:
    attempt = 1
    max_attempts = 3

    while attempt <= max_attempts:
        result = run(command)

        if result.success:
            log("✅ {command}: PASSED (attempt {attempt})")
            validation_results.append({command, "passed", attempt})
            break

        if attempt < max_attempts:
            log("⚠️ {command}: FAILED (attempt {attempt}/{max_attempts})")
            log("   Error: {result.error}")
            log("   Attempting fix...")
            attempt_fix(result.error)
            attempt += 1
        else:
            log("❌ {command}: FAILED after {max_attempts} attempts")
            validation_results.append({command, "failed", max_attempts, result.error})
```

**Execute validation commands from spec:**

```bash
# Type check
{type_check_command}
```
- If fails → Analyze type errors, attempt fixes, re-run (max 3)

```bash
# Tests
{test_command}
```
- If fails → Analyze failing tests, attempt fixes, re-run (max 3)

```bash
# Lint
{lint_command}
```
- If fails → Apply auto-fix if available, re-run (max 3)

```bash
# Build
{build_command}
```
- If fails → Analyze build errors, attempt fixes, re-run (max 3)

**After all validations complete:**
```
Validation Summary:
- Type check: ✅ Pass (1 attempt)
- Tests: ⚠️ Pass (2 attempts)
- Lint: ✅ Pass (1 attempt)
- Build: ❌ FAILED (3 attempts) - {error_summary}
```

**If any validation failed after max attempts:**
```
⚠️ Some validations failed after maximum retries.

Failed:
- {command}: {error_summary}

Options:
1. Continue anyway (not recommended)
2. Abort and fix manually
3. Show detailed error logs
```

### 8. Final Verification

**Check success criteria from spec:**
- [ ] Criterion 1 - verified how
- [ ] Criterion 2 - verified how
- [ ] Criterion 3 - verified how

**Review pattern adherence:**
- Did implementation follow documented patterns?
- Any deviations? (document if intentional)

### 9. Report Results

```markdown
## Build Complete

**Spec:** `{spec_file}`
**Branch:** `{current_branch}`

### Steps Completed
{list each step with status}

### Files Modified
{list files created/modified}

### Validation Results
| Command | Status | Attempts | Notes |
|---------|--------|----------|-------|
| Type check | ✅ Pass | 1 | |
| Tests | ✅ Pass | 2 | Fixed failing test in {file} |
| Lint | ✅ Pass | 1 | |
| Build | ✅ Pass | 1 | |

### Success Criteria
{list each criterion with ✅/❌}

### Pattern Adherence
{note any deviations from patterns}

### Next Steps
1. Run `/navigator:review {spec_file}` for quality review
2. Commit changes: `/git-actions:commit`
3. Create PR: `/git-actions:pr-write`
```

### 10. Post-Build Knowledge Capture

**Analyze the implementation for atlas improvements:**

After successful build completion, evaluate:

#### New Patterns Detected

**Question:** Did this implementation introduce reusable patterns?

If yes, identify:
- Pattern name and purpose
- File convention used
- Test convention used
- Example files created

```
📚 New pattern detected: {pattern_name}

Would you like to add this to schema.yaml patterns section?
- File convention: {convention}
- Example files: {files}
```

#### Anti-Patterns Avoided

**Question:** Did we catch any mistakes during implementation?

If yes, identify:
- What was the mistake
- Why it was wrong
- What we did instead

```
⚠️ Anti-pattern avoided: {description}

Would you like to add this to {pattern_id}.anti_patterns_summary?
- "Don't {anti_pattern}"
```

#### Task Mapping Discovery

**Question:** Is this a repeatable workflow?

If yes, identify:
- Task type
- Entry point
- Pattern sequence

```
🔄 Repeatable task detected: {task_name}

Would you like to add this to schema.yaml task_mappings or compositions?
- Description: {description}
- Entry point: {path}
- Patterns: {pattern_sequence}
```

#### Stack Observations

**Question:** Did we learn anything stack-specific?

If yes, identify:
- Technology/library insight
- Workaround discovered
- Configuration detail

```
💡 Stack observation: {description}

Would you like to add this to observations.md?
```

**Prompt user for approval before any atlas modifications:**

```
📝 Knowledge Capture Summary

Found {N} potential atlas improvements:
1. {improvement_1}
2. {improvement_2}

Would you like to:
1. Add all to atlas
2. Review individually
3. Skip (add later with /cartographer:capture)
```

**If user approves, update atlas files:**
- Add to schema.yaml patterns section
- Add to anti_patterns_summary
- Add to task_mappings or compositions
- Append to observations.md

---

## Step Execution Protocol

For each implementation step:

1. **Read before write** - Always read existing files first
2. **Follow patterns** - Check pattern guide before writing
3. **Small changes** - Make incremental changes, not massive edits
4. **Verify as you go** - Don't wait until end to find issues
5. **Document deviations** - If you must deviate from pattern, note why

---

## Handling Blockers

| Blocker | Action |
|---------|--------|
| File not found | Check path, ask user if truly missing |
| Pattern unclear | Read pattern guide, ask for clarification |
| Test failure | Analyze error, fix, re-run |
| Build failure | Check error, fix dependencies/types |
| Conflicting instructions | Ask user which to prioritize |

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas | Block with message | Run /cartographer:chart |
| No spec | Error with path | User provides correct path |
| Prerequisites missing | Block with list | User resolves or overrides |
| Step failure | Report, attempt fix | Ask user if stuck |
| Validation failure | Fix and retry | Ask user after 3 attempts |

---

## Error Recovery Protocol

### After 3 Failed Attempts

When a step or validation fails after 3 attempts:

**1. Preserve current state:**
```bash
git stash push -m "navigator-build: work-in-progress before failure at step {N}"
```

**2. Create recovery checkpoint:**
Write `.claude/build-recovery.json`:
```json
{
  "spec_file": "{spec_file}",
  "branch": "{current_branch}",
  "completed_steps": [1, 2, 3],
  "failed_step": 4,
  "failure_reason": "{error_summary}",
  "stash_ref": "{git stash ref}",
  "timestamp": "{ISO-8601}",
  "files_modified": ["{list of files changed}"],
  "commits_created": ["{list of commit hashes}"]
}
```

**3. Present recovery options:**
```
❌ Step {N} failed after 3 attempts

Error: {detailed_error}

Work preserved:
- Changes stashed: `git stash show -p`
- Recovery file: `.claude/build-recovery.json`
- Commits created: {count} (steps 1-{N-1})

Options:
1. Abort - Keep commits, discard uncommitted changes
2. Rollback - Revert all commits from this build session
3. Continue manually - I'll fix the issue myself
4. Show detailed logs - See all attempt errors
5. Resume later - Keep everything, I'll run /navigator:build --resume
```

### Partial Rollback Mechanism

**If user selects "Rollback":**

```bash
# Get commits created during this session
commits_to_revert=$(cat .claude/build-recovery.json | jq -r '.commits_created[]')

# Create rollback branch for safety
git branch build-rollback-{timestamp} HEAD

# Revert each commit in reverse order
for commit in $(echo $commits_to_revert | tac); do
  git revert --no-commit $commit
done

# Single rollback commit
git commit -m "Rollback: navigator:build failed at step {N}"
```

**Rollback report:**
```
🔄 Rollback complete

- Reverted {count} commits
- Rollback branch created: build-rollback-{timestamp}
- Working directory: clean

To restore work later:
  git cherry-pick {commit_hashes}

To delete rollback branch:
  git branch -D build-rollback-{timestamp}
```

### Resume Support

**If user runs `/navigator:build --resume` or `/navigator:build {spec} --resume`:**

1. Check for `.claude/build-recovery.json`
2. If found:
   ```
   🔄 Found recovery checkpoint

   Spec: {spec_file}
   Failed at: Step {N}
   Completed: Steps 1-{N-1}
   Stashed changes: {yes|no}

   Options:
   1. Resume from step {N} - Apply stash and continue
   2. Restart from step 1 - Keep existing commits, redo all steps
   3. Start fresh - Rollback and start over
   4. Cancel
   ```
3. If "Resume":
   ```bash
   git stash pop
   ```
   Continue from failed step with TodoWrite showing remaining steps

### State Preservation

**During build, maintain state file:** `.claude/build-state.json`

Updated after each step:
```json
{
  "spec_file": "{spec}",
  "start_time": "{timestamp}",
  "current_step": 3,
  "total_steps": 7,
  "status": "in_progress",
  "steps": [
    {"step": 1, "status": "completed", "commit": "abc123", "files": ["a.ts"]},
    {"step": 2, "status": "completed", "commit": "def456", "files": ["b.ts"]},
    {"step": 3, "status": "in_progress", "attempt": 2, "files": []}
  ],
  "validation_results": []
}
```

**On successful completion:** Delete state files
**On failure:** Preserve for recovery

### Cleanup Protocol

After successful build:
```bash
rm -f .claude/build-state.json
rm -f .claude/build-recovery.json
```

After rollback:
```bash
rm -f .claude/build-state.json
rm -f .claude/build-recovery.json
```

## Responsibilities

**YOU (handler):**
- Load all context (spec, atlas, patterns)
- Verify prerequisites
- Execute steps with pattern guidance
- Run validations and fix issues
- Report comprehensive results

**You are the implementer. Follow the spec precisely while adhering to atlas patterns.**

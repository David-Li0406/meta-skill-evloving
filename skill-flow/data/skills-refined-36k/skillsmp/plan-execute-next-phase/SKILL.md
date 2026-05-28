---
name: plan-execute-next-phase
description: |
  Execute the next phase from the project plan with full TDD workflow, 100% coverage, PR review, and quality gates.
  WHEN: Use to continue development on a project with phase-based plans. Invoke with "/plan:execute-next-phase".
  WHEN NOT: When debugging specific issues or exploring codebase.
---

# Execute Next Plan Phase

## Project Detection (RUN FIRST)

Before starting any gate, detect the project type and available commands.

### Step 0.1: Identify Project Root

```bash
# Find project root (look for common markers)
git rev-parse --show-toplevel
```

Use this as the project root for all commands.

### Step 0.2: Detect Project Type and Commands

Check for project markers and set commands accordingly:

| Marker File | Project Type | Test Command | Analyse Command | Format Command | Format Check Command |
|-------------|--------------|--------------|-----------------|----------------|----------------------|
| `composer.json` | PHP/Laravel | `php artisan test` or `./vendor/bin/phpunit` | `composer analyse` or `./vendor/bin/phpstan analyse` | `composer format` or `./vendor/bin/pint` | `composer format -- --test` or `./vendor/bin/pint --test` |
| `package.json` | Node.js | `npm test` or `yarn test` | `npm run lint` or `yarn lint` | `npm run format` or `yarn format` | `npm run format:check` or `yarn format:check` |
| `Cargo.toml` | Rust | `cargo test` | `cargo clippy` | `cargo fmt` | `cargo fmt -- --check` |
| `go.mod` | Go | `go test ./...` | `golangci-lint run` | `gofmt -w .` | `gofmt -l . \| grep .` (exits non-zero if files need formatting) |
| `pyproject.toml` / `setup.py` | Python | `pytest` or `python -m pytest` | `ruff check .` or `pylint` | `ruff format .` or `black .` | `ruff format --check .` or `black --check .` |
| `Gemfile` | Ruby | `bundle exec rspec` | `bundle exec rubocop` | `bundle exec rubocop -a` | `bundle exec rubocop --format simple` |
| `pom.xml` | Java (Maven) | `mvn test` or `./mvnw test` | `mvn checkstyle:check` or `mvn spotbugs:check` | `mvn spotless:apply` | `mvn spotless:check` |
| `build.gradle` / `build.gradle.kts` | Java/Kotlin (Gradle) | `./gradlew test` | `./gradlew check` or `./gradlew lint` | `./gradlew spotlessApply` | `./gradlew spotlessCheck` |
| `*.csproj` / `*.sln` | C#/.NET | `dotnet test` | `dotnet format --verify-no-changes` | `dotnet format` | `dotnet format --verify-no-changes` |
| `Package.swift` | Swift | `swift test` | `swiftlint lint` | `swiftlint lint --fix` | `swiftlint lint --strict` |

**Check `package.json` / `composer.json` / `pom.xml` / `build.gradle` scripts/plugins section for project-specific commands.**

#### Monorepo / Polyglot Projects

If multiple marker files exist at the project root:
1. Check for workspace configuration (`pnpm-workspace.yaml`, `lerna.json`, `nx.json`, `turbo.json`)
2. If workspace found, run commands at root level (e.g., `pnpm test`, `nx run-many --target=test`)
3. If no workspace config, identify the primary language from the main application code
4. Document all detected project types in the configuration output

#### Fallback Strategy (No Marker Files Found)

If no standard marker files are found:
1. Look for a `Makefile` with `test`, `lint`, `format` targets
2. Look for `scripts/` directory with test/lint scripts
3. Check for CI configuration files (`.github/workflows/*.yml`, `.gitlab-ci.yml`) to infer commands
4. Ask the user: "No standard project markers found. Please provide test, lint, and format commands."

### Step 0.3: Store Detected Commands

**Store the configuration in a code block that you will reference throughout this workflow.**

Announce the detected configuration:

```
PROJECT CONFIGURATION DETECTED:
- Project Root: <path>
- Project Type: <type> (or "monorepo: <types>" for polyglot)
- Test Command: <command>
- Analyse Command: <command or "not configured">
- Format Command: <command or "not configured">
- Format Check Command: <command or "not configured">
- Platform Notes: <any platform-specific notes>
```

**IMPORTANT:** Reference this configuration block whenever gates require running these commands.

#### Platform Considerations

- **Unix/macOS:** Commands shown above work as-is
- **Windows:** Use platform-appropriate alternatives:
  - Replace `./gradlew` with `gradlew.bat`
  - Replace `./mvnw` with `mvnw.cmd`
  - For `gofmt -l . | grep .`, use `gofmt -l . | findstr .`
  - PowerShell users: Commands with `||` require adjustment to `; if ($LASTEXITCODE -ne 0) { ... }`

**Use these detected commands throughout the workflow.**

---

## CRITICAL: MANDATORY ENFORCEMENT SYSTEM

**THIS IS NOT OPTIONAL. YOU MUST FOLLOW THIS EXACTLY.**

### STEP 0: Initialize Workflow Checklist (DO THIS FIRST!)

**IMMEDIATELY upon starting this skill, before ANY other action, you MUST:**

1. **Announce:** "I'm using the plan:execute-next-phase skill. Initializing mandatory workflow checklist."

2. **Create task tracking using Claude's TaskCreate/TaskUpdate tools:**

> **Note:** "TodoWrite" refers to Claude's built-in task tracking system. Use `TaskCreate` to create tasks and `TaskUpdate` to change their status.

Create tasks for each gate. Since the phase name is not known until GATE 1 completes, create initial tasks with generic names, then update GATE 1's task with the specific phase name once determined.

**Initial task creation (before GATE 1):**

```
TaskCreate: "GATE 1: Determine next phase" (activeForm: "Finding next phase")
TaskCreate: "GATE 2: Create feature branch from main" (activeForm: "Creating feature branch")
TaskCreate: "GATE 3: Execute phase tasks with TDD" (activeForm: "Implementing with TDD")
TaskCreate: "GATE 4: Run quality checks (tests, analyse, format)" (activeForm: "Running quality checks")
TaskCreate: "GATE 5: Brainstorm verify test coverage matches specs" (activeForm: "Verifying test coverage")
TaskCreate: "GATE 6: Run PR review toolkit" (activeForm: "Running PR review")
TaskCreate: "GATE 7: Apply ALL review fixes" (activeForm: "Applying review fixes")
TaskCreate: "GATE 8: Save review to docs/reviews/" (activeForm: "Saving review summary")
TaskCreate: "GATE 9: Run final quality gate check" (activeForm: "Final quality gate")
TaskCreate: "GATE 10: Create PR" (activeForm: "Creating PR")
TaskCreate: "GATE 11: Wait for user approval" (activeForm: "Waiting for approval")
```

**After GATE 1 completes:** Update subsequent task descriptions to include the phase name (e.g., "GATE 3: Execute Phase 2.1 tasks with TDD").

3. **RULE:** Before starting ANY gate, use `TaskUpdate` to mark it `in_progress`. After completing it, mark it `completed`.

4. **RULE:** You CANNOT start a gate until ALL previous gates are `completed`.

5. **RULE:** If you skip a gate, you have FAILED the workflow. Start over.

---

## GATE 1: Determine Next Phase

**Use `TaskUpdate` to mark GATE 1 as `in_progress` before starting.**

### 1.1 Validate Plan Structure

First, verify the project has the expected plan structure:

```bash
# Check if docs/plans/ exists
if [ -d "docs/plans" ]; then
  echo "Plan directory found"
  ls -la docs/plans/
else
  echo "ERROR: docs/plans/ directory not found"
fi
```

**If `docs/plans/` does not exist:**
1. Check for alternative plan locations: `plans/`, `PLAN.md`, `docs/PLAN.md`
2. If found elsewhere, note the location and adapt paths throughout this workflow
3. If no plan found, ask the user: "No project plan found. Please provide the plan location or create `docs/plans/` structure."

### 1.2 Check Current Progress

```bash
# Check current branch
git branch --show-current

# Check if on main and pull latest
git checkout main
git pull origin main

# Check merged PRs to see what's done
gh pr list --state merged --limit 5

# List available phases
ls docs/plans/phase-*/
```

### 1.3 Find Next Phase

Read the main plan file to understand phase order:
- Look for `docs/plans/` directory structure
- Check for phase files like `phase-0-*.md`, `phase-1-*.md`, etc.
- Identify sub-phases within each phase

**Output:** "Next phase to execute: X.Y - <name>"

**After determining the phase:** Update the task descriptions for GATE 2-11 to include the phase name for clarity.

**Use `TaskUpdate` to mark GATE 1 as `completed`.**

---

## GATE 2: Create Feature Branch

**Use `TaskUpdate` to mark GATE 2 as `in_progress` before starting.**

```bash
git checkout main
git pull origin main
git checkout -b feat/<sub-phase-name>
# Example: git checkout -b feat/0.3-ci-cd-pipeline
```

**Verify:** `git branch --show-current` shows the new branch.

**Use `TaskUpdate` to mark GATE 2 as `completed`.**

---

## GATE 3: Execute Phase with TDD

**Use `TaskUpdate` to mark GATE 3 as `in_progress` before starting.**

### MANDATORY SKILL INVOCATION

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "superpowers:executing-plans")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

### 3.1 Read Phase Plan

Read the sub-phase file: `docs/plans/phase-X/X.Y-<name>.md`

**If `docs/specifications/` exists:** Also read relevant specification files to understand acceptance criteria.

### 3.2 Execute Each Task Using the Executing-Plans Skill

The `/superpowers:executing-plans` skill guides you through:
- Breaking down tasks into actionable steps
- Following TDD workflow for code changes
- Running verification after each step
- Review checkpoints

**TDD PATTERN (MANDATORY for code changes):**
1. Write test FIRST
2. Run test -> MUST FAIL (red)
3. Write minimal code to pass
4. Run test -> MUST PASS (green)
5. Verify coverage

**After each task:**
```bash
cd <project-root>
<detected-test-command>
```

**If infrastructure/config only:** Verify by running the tool/config directly.

### 3.3 Handling Partial Task Failures

If a task cannot be completed:
1. **Document the blocker** in a code block with `BLOCKER:` prefix
2. **Create a follow-up task** using TaskCreate for the blocked work
3. **Continue with other tasks** if they are independent
4. **At gate end:** If any task is blocked, report to user before proceeding
5. **User decision required:** User must approve continuing with incomplete tasks or provide resolution

**GATE 3 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/superpowers:executing-plans`**

**Use `TaskUpdate` to mark GATE 3 as `completed` only after ALL tasks done (or user approves continuing with documented blockers).**

---

## GATE 4: Run Quality Checks

**Use `TaskUpdate` to mark GATE 4 as `in_progress` before starting.**

Run ALL available quality checks for the detected project type:

```bash
cd <project-root>

# 1. Tests (REQUIRED - GATE 4 FAILS if this fails)
<detected-test-command>

# 2. Coverage (if available)
<detected-test-command-with-coverage> || echo "Coverage not configured"

# 3. Static analysis (if configured)
<detected-analyse-command> || echo "Static analysis not configured"

# 4. Code style check (if configured)
<detected-format-check-command> || echo "Format check not configured"

# 5. Fix style if needed (if configured)
<detected-format-command>
```

### Handling "Not Configured" Commands

| Check Type | If Not Configured | Gate Status |
|------------|-------------------|-------------|
| **Tests** | GATE 4 FAILS - tests are mandatory | FAIL |
| **Coverage** | Log "Coverage reporting not configured" and continue | PASS |
| **Static Analysis** | Log "Static analysis not configured" and continue | PASS |
| **Format Check** | Log "Format check not configured" and continue | PASS |

**Important:** Only the test command is mandatory. If analyse/format commands are "not configured" (from Step 0.3), log that fact and continue. The gate passes as long as tests pass.

**LOOP until ALL configured checks pass.** Do NOT proceed with test failures.

**Use `TaskUpdate` to mark GATE 4 as `completed`.**

---

## GATE 5: Brainstorm Verify Test Coverage

**Use `TaskUpdate` to mark GATE 5 as `in_progress` before starting.**

### MANDATORY SKILL INVOCATION

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "superpowers:brainstorming")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

### Test Coverage Acceptance Criteria

| Criterion | Requirement |
|-----------|-------------|
| **Line Coverage** | Aim for 80%+ on new code (if coverage tooling available) |
| **Branch Coverage** | All conditional paths should have tests |
| **Specification Coverage** | Every requirement in the phase plan must have at least one test |
| **Edge Cases** | Error paths, boundary conditions, and null/empty inputs tested |

**After skill loads, use this prompt:**

```
Question: Do our tests fully cover the Phase X.Y specifications?

Context:
- Phase plan: docs/plans/phase-X/X.Y-<name>.md
- Current tests: <project-test-directory>
- Specifications: docs/specifications/ (if exists)

Deliverable:
- List specification requirements NOT covered by tests
- For each gap, specify what test should be added
- Note any untested edge cases or error paths
```

### If `docs/specifications/` Does Not Exist

If there is no specifications directory:
1. Use the phase plan file as the source of requirements
2. Check for inline acceptance criteria in the plan
3. Look for `requirements.md`, `REQUIREMENTS.md`, or similar files
4. If no formal specs exist, verify tests cover all tasks listed in the phase plan

**If gaps found:** Add the missing tests, then re-run GATE 4.

**GATE 5 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/superpowers:brainstorming`**

**Use `TaskUpdate` to mark GATE 5 as `completed`.**

---

## GATE 6: Run PR Review

**Use `TaskUpdate` to mark GATE 6 as `in_progress` before starting.**

### 6.1 Push Branch First

```bash
git add -A
git commit -m "feat(phase-X.Y): <phase description>"
git push -u origin feat/<sub-phase-name>
```

### 6.2 Invoke PR Review

### MANDATORY SKILL INVOCATION

**YOU MUST USE THE SKILL TOOL TO INVOKE:**
```
Skill(skill: "pr-review-toolkit:review-pr")
```

**THIS IS NOT OPTIONAL. DO NOT USE Task AGENT. DO NOT SKIP. INVOKE THE SKILL.**

Wait for ALL review agents to complete.

### 6.3 Review Completion Detection

The PR review skill spawns multiple review agents. Wait for completion by:

1. **Check agent status:** All dispatched agents should report back
2. **Timeout handling:** If no response after 5 minutes, check if agents are still running
3. **Partial completion:** If some agents fail:
   - Document which agents completed and which failed
   - Proceed with available review feedback
   - Note failed agents in the review summary (GATE 8)

**If review agents fail completely:**
1. Log the failure: "PR review agents failed to complete"
2. Perform a manual review using `git diff main...HEAD`
3. Document the manual review approach in GATE 8
4. Continue to GATE 7 with manual review findings

**GATE 6 IS NOT COMPLETE UNTIL YOU HAVE INVOKED `/pr-review-toolkit:review-pr`**

**Use `TaskUpdate` to mark GATE 6 as `completed`.**

---

## GATE 7: Apply ALL Review Fixes

**Use `TaskUpdate` to mark GATE 7 as `in_progress` before starting.**

### MANDATORY CORRECTION RULES

**YOU MUST FIX EVERY ISSUE. THIS IS NOT OPTIONAL.**

#### STEP 7.1: Create Issue Tracking List

**IMMEDIATELY create tasks using `TaskCreate` for ALL issues from the review:**

```
TaskCreate: "FIX CRITICAL: <issue description>" (activeForm: "Fixing critical issue")
TaskCreate: "FIX IMPORTANT: <issue description>" (activeForm: "Fixing important issue")
TaskCreate: "FIX OTHER: <issue description>" (activeForm: "Fixing issue")
TaskCreate: "EVALUATE SUGGESTION: <suggestion description>" (activeForm: "Evaluating suggestion")
```

#### STEP 7.2: Fix ALL Critical Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every Critical issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each Critical issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY Critical issue remains unfixed.**

#### STEP 7.3: Fix ALL Important Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every Important issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each Important issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY Important issue remains unfixed.**

#### STEP 7.4: Fix ALL Other Issues (MANDATORY - NO EXCEPTIONS)

| Rule | Enforcement |
|------|-------------|
| Every other issue | **MUST BE FIXED** |
| Skip allowed? | **NO - NEVER** |
| Partial fix allowed? | **NO - COMPLETE FIX ONLY** |

**For each other issue:**
1. Read the issue description and file location
2. Implement the complete fix
3. Verify the fix works
4. Mark todo as `completed`

**GATE 7 FAILS if ANY other issue remains unfixed.**

#### STEP 7.5: Evaluate ALL Suggestions (MANDATORY EVALUATION)

| Rule | Enforcement |
|------|-------------|
| Every suggestion | **MUST BE EVALUATED** |
| Skip evaluation? | **NO - MUST DECIDE** |
| Decision required | **APPLY or DOCUMENT WHY NOT** |

**For each suggestion:**
1. Read the suggestion carefully
2. **Evaluate pertinence:**
   - Does it improve code quality?
   - Does it align with project standards?
   - Is it worth the effort?
3. **Make a decision:**
   - **IF PERTINENT:** Apply the suggestion, mark todo `completed`
   - **IF NOT PERTINENT:** Document WHY in the review summary, mark todo `completed`

**Example of documenting rejected suggestion:**
```markdown
### Suggestion: Add baseline file for static analysis
**Decision:** NOT APPLIED
**Reason:** Project is new with zero existing errors. Baseline not needed until legacy code exists.
```

**GATE 7 FAILS if ANY suggestion was not evaluated.**

#### STEP 7.6: Verification Checklist

Before marking GATE 7 complete, verify using `TaskList`:

- [ ] ALL Critical issues have been fixed (tasks marked `completed`)
- [ ] ALL Important issues have been fixed (tasks marked `completed`)
- [ ] ALL other issues have been fixed (tasks marked `completed`)
- [ ] ALL suggestions have been evaluated (tasks marked `completed`)

#### STEP 7.7: Commit All Fixes

```bash
git add -A
git commit -m "fix(phase-X.Y): address all PR review feedback

- Fixed X critical issues
- Fixed X important issues
- Fixed X other issues
- Applied X suggestions
- Documented X suggestions as not applicable

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

**GATE 7 IS NOT COMPLETE UNTIL:**
1. Every Critical issue is fixed
2. Every Important issue is fixed
3. Every other issue is fixed
4. Every suggestion is evaluated (applied or rejected with reason)
5. All changes are committed and pushed

**Use `TaskUpdate` to mark GATE 7 as `completed`.**

---

## GATE 8: Save Review Summary

**Use `TaskUpdate` to mark GATE 8 as `in_progress` before starting.**

### 8.1 Create Reviews Directory

```bash
# Ensure the reviews directory exists
mkdir -p docs/reviews
```

### 8.2 Write Review Summary

**Write review summary to:** `docs/reviews/phase-X.Y-<name>.md`

Include:
- Date and PR number
- Review agents used (or "Manual review" if agents failed)
- Critical/Important/Suggestion issues (with status: FIXED or NOTED)
- Quality checklist results
- Any blockers or known issues carried forward

### 8.3 Commit Review Summary

```bash
git add docs/reviews/
git commit -m "docs(phase-X.Y): add review summary"
git push
```

**Use `TaskUpdate` to mark GATE 8 as `completed`.**

---

## GATE 9: Final Quality Gate

**Use `TaskUpdate` to mark GATE 9 as `in_progress` before starting.**

**Run FULL quality check again:**

```bash
cd <project-root>

# REQUIRED: Tests must pass
<detected-test-command>

# If configured: Static analysis
<detected-analyse-command>  # skip if "not configured"

# If configured: Format check
<detected-format-check-command>  # skip if "not configured"

# Verify clean working directory
git status
```

**If tests fail:** Fix and re-run. Do NOT proceed.
**If optional checks fail:** Fix and re-run (if they were passing in GATE 4).

**Use `TaskUpdate` to mark GATE 9 as `completed`.**

---

## GATE 10: Create PR

**Use `TaskUpdate` to mark GATE 10 as `in_progress` before starting.**

```bash
gh pr create \
  --title "feat(phase-X.Y): <name>" \
  --body "## Summary
<Brief description>

## Changes
- Change 1
- Change 2

## Quality Checks
- [x] All tests passing
- [x] Static analysis passing (or N/A if not configured)
- [x] Code style passing (or N/A if not configured)

## Review
See docs/reviews/phase-X.Y-<name>.md

## Phase Reference
docs/plans/phase-X/X.Y-<name>.md"
```

**Output:** PR URL

**Use `TaskUpdate` to mark GATE 10 as `completed`.**

---

## GATE 11: Wait for User Approval

**Use `TaskUpdate` to mark GATE 11 as `in_progress`.**

**STOP and announce this EXACT format:**

```
═══════════════════════════════════════════════════════════════
PHASE X.Y IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════════════════

PR: <URL>

WORKFLOW GATES COMPLETED:
[x] GATE 1: Determined next phase
[x] GATE 2: Created feature branch
[x] GATE 3: Executed phase tasks with TDD
[x] GATE 4: Quality checks passed
[x] GATE 5: Brainstorm verified test coverage
[x] GATE 6: PR review completed
[x] GATE 7: All review fixes applied
[x] GATE 8: Review saved to docs/reviews/
[x] GATE 9: Final quality gate passed
[x] GATE 10: PR created
[ ] GATE 11: Waiting for your approval

Review: docs/reviews/phase-X.Y-<name>.md

Waiting for your approval to merge and continue to Phase X.(Y+1).
═══════════════════════════════════════════════════════════════
```

**DO NOT proceed until user explicitly approves.**

**Use `TaskUpdate` to mark GATE 11 as `completed` only after user approves.**

---

## Error Recovery

### If Any Gate Fails
1. Fix the issue
2. Re-run that gate
3. Do NOT skip to the next gate

### If Blocked
1. Document what's blocking using a `BLOCKER:` code block
2. Ask user for guidance
3. Do NOT skip or workaround

### If You Forgot a Gate
1. STOP immediately
2. Go back and complete the missed gate
3. Re-run subsequent gates

### Partial Phase Failure Handling

If you cannot complete the phase due to blockers:

1. **Document all completed work:**
   - List tasks completed successfully
   - List tasks blocked with reasons
   - List any temporary workarounds applied

2. **Create follow-up tasks:**
   - Use `TaskCreate` for each blocked item
   - Include context and blocker description

3. **Inform the user:**
   ```
   PHASE X.Y PARTIALLY COMPLETE

   Completed: X of Y tasks
   Blocked: Z tasks (see details below)

   Blockers:
   - <blocker 1 description>
   - <blocker 2 description>

   Options:
   1. Resolve blockers and continue
   2. Create PR with partial implementation
   3. Abandon phase and revert
   ```

4. **Wait for user decision** before proceeding

---

## Self-Check Questions

Before marking a gate complete, ask yourself:

| Gate | Self-Check Question |
|------|---------------------|
| 1 | Did I identify the specific phase number and name? |
| 2 | Am I on a new feature branch from main? |
| 3 | **Did I call `Skill(skill: "superpowers:executing-plans")` and implement ALL tasks?** |
| 4 | Did all configured quality checks pass? |
| 5 | **Did I call `Skill(skill: "superpowers:brainstorming")`?** |
| 6 | **Did I call `Skill(skill: "pr-review-toolkit:review-pr")`?** |
| 7 | Did I fix ALL Critical, ALL Important, ALL other issues, and evaluate ALL suggestions? |
| 8 | Did I create docs/reviews/phase-X.Y-<name>.md? |
| 9 | Did ALL quality checks pass again after fixes? |
| 10 | Did I create the PR with gh pr create? |
| 11 | Did I show the final status and wait for approval? |

**If ANY answer is "no", you have not completed that gate.**

---

## Commit Message Format

Use consistent commit message format throughout the workflow:

| Gate | Commit Type | Format |
|------|-------------|--------|
| GATE 6 | Feature | `feat(phase-X.Y): <description>` |
| GATE 7 | Fixes | `fix(phase-X.Y): address all PR review feedback` |
| GATE 8 | Docs | `docs(phase-X.Y): add review summary` |

**Commit message rules:**
- Use conventional commits format: `type(scope): description`
- Scope should be the phase number (e.g., `phase-1.2`)
- Description should be lowercase, imperative mood
- Include `Co-Authored-By` footer when Claude contributes significantly

---

## CRITICAL SKILL INVOCATIONS

**These skills MUST be invoked using the Skill tool. NO EXCEPTIONS.**

| Gate | Required Skill Invocation |
|------|---------------------------|
| **GATE 3** | `Skill(skill: "superpowers:executing-plans")` |
| **GATE 5** | `Skill(skill: "superpowers:brainstorming")` |
| **GATE 6** | `Skill(skill: "pr-review-toolkit:review-pr")` |

**Using Task agent or any other method is NOT acceptable for these gates.**

---

## CRITICAL CORRECTION REQUIREMENTS (GATE 7)

**ALL issues from PR review MUST be addressed. NO EXCEPTIONS.**

| Issue Type | Action Required | Skip Allowed? |
|------------|-----------------|---------------|
| **Critical Issues** | FIX ALL | NEVER |
| **Important Issues** | FIX ALL | NEVER |
| **Other Issues** | FIX ALL | NEVER |
| **Suggestions** | EVALUATE ALL | NEVER (must apply OR document why not) |

**GATE 7 FAILS if:**
- Any Critical issue is not fixed
- Any Important issue is not fixed
- Any other issue is not fixed
- Any suggestion is not evaluated (applied or rejected with documented reason)

**You MUST create tasks using `TaskCreate` to track each issue individually.**

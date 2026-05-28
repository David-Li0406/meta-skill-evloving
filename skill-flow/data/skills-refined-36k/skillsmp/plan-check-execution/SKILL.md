---
name: plan-check-execution
description: |
  Verify that /plan:execute-next-phase workflow was followed correctly with all gates, skill invocations, and quality checks.
  WHEN: Use after completing a phase to audit workflow compliance. Invoke with "/plan:check-execution".
  WHEN NOT: During active development - use this for post-execution verification only.
---

# Check Plan Execution

## Purpose

This skill audits the `/plan:execute-next-phase` workflow to ensure:
1. ALL 11 GATES were completed
2. ALL mandatory skill invocations were made
3. Implementation matches the phase plan
4. Quality checks passed
5. PR review issues were all addressed

---

## Project Detection

**Before auditing, detect the project type using the same approach as `/plan:execute-next-phase`.**

Refer to the Project Detection section in `/plan:execute-next-phase` for:
- Step 0.1: Identify Project Root
- Step 0.2: Detect Project Type and Commands
- Step 0.3: Store Detected Commands

**Store the detected configuration:**

```
PROJECT CONFIGURATION DETECTED:
- Project Root: <path>
- Project Type: <type>
- Test Command: <command>
- Analyse Command: <command or "not configured">
- Format Command: <command or "not configured">
- Format Check Command: <command or "not configured">
```

**Use these detected commands for AUDIT 4 quality checks.**

---

## STEP 0: Initialize Audit Checklist

**IMMEDIATELY upon starting this skill, create tasks using TaskCreate:**

Create each audit task individually:

1. `TaskCreate` with:
   - subject: "AUDIT 1: Verify GATE compliance (all 11 gates)"
   - description: "Check all 11 gates were completed with proper evidence"
   - activeForm: "Auditing gate compliance"

2. `TaskCreate` with:
   - subject: "AUDIT 2: Verify mandatory skill invocations"
   - description: "Verify all 3 mandatory skills were invoked with proper artifacts"
   - activeForm: "Checking skill invocations"

3. `TaskCreate` with:
   - subject: "AUDIT 3: Verify implementation completeness"
   - description: "Check all tasks from phase plan were implemented"
   - activeForm: "Checking implementation"

4. `TaskCreate` with:
   - subject: "AUDIT 4: Verify quality checks passed"
   - description: "Run all quality commands and verify they pass"
   - activeForm: "Verifying quality checks"

5. `TaskCreate` with:
   - subject: "AUDIT 5: Verify PR review compliance"
   - description: "Check all review issues were properly addressed"
   - activeForm: "Checking PR review compliance"

6. `TaskCreate` with:
   - subject: "AUDIT 6: Generate audit report"
   - description: "Compile and present final audit report"
   - activeForm: "Generating audit report"

Use `TaskUpdate` with `status: "in_progress"` when starting each audit and `status: "completed"` when finishing.

---

## AUDIT 1: Verify GATE Compliance

**Use `TaskUpdate` to mark "AUDIT 1" as `in_progress`.**

### 1.1 Validate Project Root

**IMPORTANT:** Before proceeding, verify that the project root from the original execution matches the current working directory.

```bash
# Verify project root exists and is accessible
ls -la <detected-project-root>

# Verify .git directory exists at project root
ls -la <detected-project-root>/.git
```

**If project root has changed or is inaccessible:** STOP and report the discrepancy.

### 1.2 Validate Directory Structure

**Before auditing, verify required directories exist:**

```bash
# Check docs/plans/ directory exists
ls -la docs/plans/ 2>/dev/null || echo "ERROR: docs/plans/ directory not found"

# Check docs/reviews/ directory exists
ls -la docs/reviews/ 2>/dev/null || echo "ERROR: docs/reviews/ directory not found"
```

**If directories are missing:** The workflow was not followed correctly. Mark as FAILED.

### 1.3 Identify Current Phase

```bash
# Get current branch
git branch --show-current

# Get recent PRs
gh pr list --state all --limit 5

# Find phase from branch name or recent PR
```

### 1.4 Check Each GATE

**For each gate, verify evidence exists:**

| Gate | Verification Method | Evidence Required |
|------|---------------------|-------------------|
| GATE 1 | Branch name matches phase | `feat/X.Y-<name>` pattern |
| GATE 2 | Branch created from main | `git log --oneline main..HEAD` shows commits |
| GATE 3 | Tasks implemented | Code changes match phase plan |
| GATE 4 | Quality checks ran | Tests pass, analyse/format checks pass (if configured) |
| GATE 5 | Brainstorming done | Test coverage verified against specs |
| GATE 6 | PR review ran | Review summary exists |
| GATE 7 | Fixes applied | All issues in review marked FIXED |
| GATE 8 | Review saved | `docs/reviews/phase-X.Y-*.md` exists |
| GATE 9 | Final checks passed | All quality commands pass now |
| GATE 10 | PR created | `gh pr view` returns PR info **for the correct phase** |
| GATE 11 | Approval requested | PR is open or merged |

### 1.5 Gate Compliance Checklist

Run these verifications:

```bash
# Check branch pattern and extract phase number
CURRENT_BRANCH=$(git branch --show-current)
echo "Current branch: $CURRENT_BRANCH"
echo "$CURRENT_BRANCH" | grep -E "feat/[0-9]+\.[0-9]+-"

# Extract phase number from branch (e.g., "feat/1.2-name" -> "1.2")
PHASE_NUM=$(echo "$CURRENT_BRANCH" | grep -oE "[0-9]+\.[0-9]+")
echo "Phase number: $PHASE_NUM"

# Check commits exist
git log --oneline main..HEAD | head -5

# Check review doc exists for THIS phase
ls docs/reviews/phase-${PHASE_NUM}-*.md 2>/dev/null || echo "NO REVIEW DOC FOUND FOR PHASE $PHASE_NUM"

# Check PR exists AND is for the correct branch/phase
gh pr view 2>/dev/null || echo "NO PR FOUND"

# Verify PR is for the current branch (correct phase)
gh pr view --json headRefName --jq '.headRefName' 2>/dev/null | grep -q "$CURRENT_BRANCH" && echo "PR is for correct branch" || echo "WARNING: PR may be for different branch"
```

**Record findings:**
- [ ] GATE 1: Pass or Fail
- [ ] GATE 2: Pass or Fail
- [ ] GATE 3: Pass or Fail (verify in AUDIT 3)
- [ ] GATE 4: Pass or Fail (verify in AUDIT 4)
- [ ] GATE 5: Pass or Fail (verify in AUDIT 2)
- [ ] GATE 6: Pass or Fail (verify in AUDIT 2)
- [ ] GATE 7: Pass or Fail (verify in AUDIT 5)
- [ ] GATE 8: Pass or Fail
- [ ] GATE 9: Pass or Fail (verify in AUDIT 4)
- [ ] GATE 10: Pass or Fail (verify PR is for THIS phase branch)
- [ ] GATE 11: Pass or Fail

**Use `TaskUpdate` to mark "AUDIT 1" as `completed`.**

---

## AUDIT 2: Verify Mandatory Skill Invocations

**Use `TaskUpdate` to mark "AUDIT 2" as `in_progress`.**

### 2.1 Required Skill Invocations

The `/plan:execute-next-phase` workflow REQUIRES these skill invocations:

| Gate | Required Skill | How to Verify |
|------|----------------|---------------|
| **GATE 3** | `superpowers:executing-plans` | Implementation follows structured execution |
| **GATE 5** | `superpowers:brainstorming` | Test coverage analysis exists |
| **GATE 6** | `pr-review-toolkit:review-pr` | Multi-agent review completed |

### 2.2 Evidence Check

**For each skill, distinguish between:**
- **Not Invoked:** No artifacts or evidence exist
- **Started But Not Completed:** Partial artifacts exist but workflow incomplete
- **Fully Completed:** All required artifacts present

#### GATE 3 - Executing Plans (`superpowers:executing-plans`)

**Required Artifacts:**
- Commit messages showing incremental, task-by-task implementation
- Test files created BEFORE implementation files (TDD pattern)
- Structured progression visible in git history

**Verification Commands:**
```bash
# Check commit history for structured execution pattern
git log --oneline main..HEAD | head -20

# Check if test files were committed before implementation
# (Look for test commits preceding implementation commits)
git log --oneline --name-only main..HEAD | grep -E "(test|spec)\." | head -10
```

**Evidence Status:**
- [ ] **FULLY COMPLETED:** Multiple structured commits, TDD pattern visible
- [ ] **STARTED BUT NOT COMPLETED:** Some commits exist but no clear structure
- [ ] **NOT INVOKED:** No structured execution evidence, all changes in single commit

#### GATE 5 - Brainstorming (`superpowers:brainstorming`)

**Required Artifacts:**
- "Test Coverage Analysis" section in review document
- Gap analysis between specifications and tests
- Coverage assessment with specific findings

**Verification Commands:**
```bash
# Check review doc for brainstorming evidence
grep -l "Test Coverage" docs/reviews/phase-*.md 2>/dev/null
grep -l "Brainstorming" docs/reviews/phase-*.md 2>/dev/null
grep -l "Coverage Analysis" docs/reviews/phase-*.md 2>/dev/null
```

**Evidence Status:**
- [ ] **FULLY COMPLETED:** Coverage analysis section with specific findings
- [ ] **STARTED BUT NOT COMPLETED:** Section header exists but content incomplete
- [ ] **NOT INVOKED:** No coverage analysis section in review document

#### GATE 6 - PR Review (`pr-review-toolkit:review-pr`)

**Required Artifacts:**
- Multi-agent review sections in review document
- At minimum: code-reviewer, comment-analyzer, silent-failure-hunter results
- Categorized issues: Critical, Important, Suggestions

**Verification Commands:**
```bash
# Check review doc for multi-agent review evidence
grep -l "code-reviewer" docs/reviews/phase-*.md 2>/dev/null
grep -l "Critical Issues" docs/reviews/phase-*.md 2>/dev/null
grep -l "silent-failure" docs/reviews/phase-*.md 2>/dev/null
```

**Evidence Status:**
- [ ] **FULLY COMPLETED:** All agent sections present with categorized issues
- [ ] **STARTED BUT NOT COMPLETED:** Some agent sections but incomplete
- [ ] **NOT INVOKED:** No multi-agent review sections in document

### 2.3 Skill Invocation Checklist

| Skill | Status | Evidence Found |
|-------|--------|----------------|
| `superpowers:executing-plans` | Fully Completed / Started / Not Invoked | [describe evidence] |
| `superpowers:brainstorming` | Fully Completed / Started / Not Invoked | [describe evidence] |
| `pr-review-toolkit:review-pr` | Fully Completed / Started / Not Invoked | [describe evidence] |

**Failure Conditions:**
- If ANY skill is "Not Invoked": Mark as FAILED
- If ANY skill is "Started But Not Completed": Mark as FAILED with remediation note

**Use `TaskUpdate` to mark "AUDIT 2" as `completed`.**

---

## AUDIT 3: Verify Implementation Completeness

**Use `TaskUpdate` to mark "AUDIT 3" as `in_progress`.**

### 3.1 Read Phase Plan

```bash
# Find phase plan file (using phase number from AUDIT 1)
ls docs/plans/ | grep -i "phase"

# Read the specific phase plan
cat docs/plans/phase-X.Y-*.md
```

Read the relevant phase plan file.

### 3.2 Extract Required Tasks

**Task Extraction Patterns:**

Phase plans may use different formats. Extract tasks using these patterns:

1. **Checkbox format:** Lines starting with `- [ ]` or `- [x]`
   ```
   - [ ] Implement user authentication
   - [ ] Add input validation
   ```

2. **Numbered tasks:** Lines starting with numbers followed by `.` or `)`
   ```
   1. Implement user authentication
   2) Add input validation
   ```

3. **Task headers:** Sections with `## Task:` or `### Task` or `**Task:**`
   ```
   ## Task: Implement Authentication
   ### Task 1: Add Validation
   ```

4. **Deliverables section:** Items under "Deliverables", "Requirements", or "Implementation" headers
   ```
   ## Deliverables
   - User auth module
   - Validation helper
   ```

**Extraction Command:**
```bash
# Extract checkbox tasks
grep -E "^\s*-\s*\[.\]" docs/plans/phase-X.Y-*.md

# Extract numbered tasks
grep -E "^\s*[0-9]+[\.\)]" docs/plans/phase-X.Y-*.md

# Extract task headers
grep -E "^#+\s*(Task|Deliverable)" docs/plans/phase-X.Y-*.md
```

**Compile extracted tasks:**

```markdown
## Tasks from Phase X.Y Plan:

Source: docs/plans/phase-X.Y-name.md

| # | Task Description | Source Line |
|---|------------------|-------------|
| 1 | [task description] | Line XX |
| 2 | [task description] | Line XX |
| 3 | [task description] | Line XX |
```

### 3.3 Verify Each Task Implementation

**For EACH task in the plan:**

1. **Identify expected deliverable** (file, config, feature)
2. **Check if deliverable exists**
3. **Verify deliverable is correct/complete**

```bash
# Check files changed in this branch
git diff --name-only main..HEAD

# Check specific file exists
ls -la <expected-file-path>

# Read file to verify content
```

### 3.4 Implementation Completeness Checklist

For each task:

| Task | Status | Evidence |
|------|--------|----------|
| Task 1 | Implemented / Missing / Incomplete | [file path or commit] |
| Task 2 | Implemented / Missing / Incomplete | [file path or commit] |
| Task 3 | Implemented / Missing / Incomplete | [file path or commit] |

**Calculate completion percentage:** X/Y tasks = Z%

**If < 100%:** Mark as FAILED with list of missing/incomplete tasks.

**Use `TaskUpdate` to mark "AUDIT 3" as `completed`.**

---

## AUDIT 4: Verify Quality Checks Passed

**Use `TaskUpdate` to mark "AUDIT 4" as `in_progress`.**

### 4.1 Run All Quality Commands

Use the detected project configuration from the Project Detection section:

```bash
cd <project-root>

# 1. Run tests (REQUIRED)
<detected-test-command>

# 2. Run static analysis (if configured)
<detected-analyse-command>

# 3. Run code style check (if configured)
<detected-format-check-command>

# 4. Check git status is clean
git status
```

### 4.2 Quality Check Results

| Check | Command | Result |
|-------|---------|--------|
| Tests | `<detected-test-command>` | PASS / FAIL |
| Static Analysis | `<detected-analyse-command>` | PASS / FAIL / N/A |
| Code Style | `<detected-format-check-command>` | PASS / FAIL / N/A |
| Git Clean | `git status` | Clean / Dirty |

### 4.3 Coverage Check (Optional)

**Note:** Coverage is checked as part of the test command if the project supports it.

Coverage may be available via:
- Jest: `--coverage` flag (often included in test script)
- pytest: `--cov` flag (requires pytest-cov)
- Go: `-cover` flag
- Other: Check project's package.json, pytest.ini, or similar config

```bash
# Check if test command already includes coverage
# Look for coverage output in test results
# This is informational - not a failure condition if unavailable
```

**If the test command produces coverage output, note it in the report. Coverage availability is optional and depends on project configuration.**

**If tests fail:** Mark as FAILED.
**If configured checks (analyse/format) fail:** Mark as FAILED.

**Use `TaskUpdate` to mark "AUDIT 4" as `completed`.**

---

## AUDIT 5: Verify PR Review Compliance

**Use `TaskUpdate` to mark "AUDIT 5" as `in_progress`.**

### 5.1 Read Review Document

```bash
# Read the review document for this phase
cat docs/reviews/phase-X.Y-*.md
```

### 5.2 Expected Review Document Structure

The review document created by GATE 8 should follow this structure:

```markdown
# Phase X.Y Review: [Phase Name]

## Summary
- Date: YYYY-MM-DD
- Branch: feat/X.Y-name
- Reviewer: pr-review-toolkit

## Agent Results

### code-reviewer
[findings]

### comment-analyzer
[findings]

### silent-failure-hunter
[findings]

### type-design-analyzer (if applicable)
[findings]

### pr-test-analyzer (if applicable)
[findings]

## Issues

### Critical Issues
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 1 | [description] | [file:line] | FIXED / OPEN |

### Important Issues
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 1 | [description] | [file:line] | FIXED / OPEN |

### Other Issues
| # | Issue | Location | Status |
|---|-------|----------|--------|
| 1 | [description] | [file:line] | FIXED / OPEN |

## Suggestions
| # | Suggestion | Status | Notes |
|---|------------|--------|-------|
| 1 | [description] | APPLIED / DECLINED | [reason if declined] |

## Test Coverage Analysis
[From brainstorming skill]
```

**If review document does not follow this structure:** Note what sections are missing but continue audit with available information.

### 5.3 Extract All Issues

Parse the review document for:
- **Critical Issues** (must be 0 remaining OPEN)
- **Important Issues** (must all be FIXED)
- **Other Issues** (must all be FIXED)
- **Suggestions** (must all be EVALUATED - either APPLIED or DECLINED with reason)

**Extraction Commands:**
```bash
# Find Critical Issues section and count OPEN items
grep -A 20 "Critical Issues" docs/reviews/phase-*.md | grep -c "OPEN" || echo "0"

# Find Important Issues section and count OPEN items
grep -A 20 "Important Issues" docs/reviews/phase-*.md | grep -c "OPEN" || echo "0"

# Find Suggestions and check for unevaluated items
grep -A 30 "## Suggestions" docs/reviews/phase-*.md | grep -c "PENDING" || echo "0"
```

### 5.4 Verify Issue Resolution

**For Critical Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | Pass/Fail |
| Issue 2 | FIXED | Pass/Fail |

**For Important Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | Pass/Fail |
| Issue 2 | FIXED | Pass/Fail |

**For Other Issues:**
| Issue | Status Required | Actual Status |
|-------|-----------------|---------------|
| Issue 1 | FIXED | Pass/Fail |

**For Suggestions:**
| Suggestion | Required | Actual |
|------------|----------|--------|
| Suggestion 1 | APPLIED or DECLINED with reason | Pass/Fail |
| Suggestion 2 | APPLIED or DECLINED with reason | Pass/Fail |

### 5.5 PR Review Compliance Checklist

- [ ] All Critical issues: FIXED (0 remaining OPEN)
- [ ] All Important issues: FIXED
- [ ] All Other issues: FIXED
- [ ] All Suggestions: EVALUATED (APPLIED or DECLINED with documented reason)

**If ANY issue not properly addressed:** Mark as FAILED.

**Use `TaskUpdate` to mark "AUDIT 5" as `completed`.**

---

## AUDIT 6: Generate Audit Report

**Use `TaskUpdate` to mark "AUDIT 6" as `in_progress`.**

### 6.1 Compile Results

Create the final audit report:

```markdown
# Plan Execution Audit Report

**Phase:** X.Y - <name>
**Date:** YYYY-MM-DD
**Branch:** feat/X.Y-<name>
**PR:** #<number>

---

## GATE Compliance

| Gate | Description | Status |
|------|-------------|--------|
| 1 | Determine next phase | Pass/Fail |
| 2 | Create feature branch | Pass/Fail |
| 3 | Execute with TDD | Pass/Fail |
| 4 | Quality checks | Pass/Fail |
| 5 | Brainstorm coverage | Pass/Fail |
| 6 | PR review | Pass/Fail |
| 7 | Apply fixes | Pass/Fail |
| 8 | Save review | Pass/Fail |
| 9 | Final quality | Pass/Fail |
| 10 | Create PR | Pass/Fail |
| 11 | User approval | Pass/Fail |

**Gate Compliance:** X/11 (Y%)

---

## Mandatory Skill Invocations

| Gate | Skill | Invoked? |
|------|-------|----------|
| 3 | superpowers:executing-plans | Pass/Fail |
| 5 | superpowers:brainstorming | Pass/Fail |
| 6 | pr-review-toolkit:review-pr | Pass/Fail |

**Skill Compliance:** X/3 (Y%)

---

## Implementation Completeness

| Task | Status |
|------|--------|
| Task 1 | Pass/Fail/Incomplete |
| Task 2 | Pass/Fail/Incomplete |
| Task 3 | Pass/Fail/Incomplete |

**Implementation:** X/Y tasks (Z%)

---

## Quality Checks

| Check | Status |
|-------|--------|
| Tests | Pass/Fail |
| Static Analysis | Pass/Fail/N/A |
| Code Style | Pass/Fail/N/A |
| Git Clean | Pass/Fail |

**Quality:** X/Y passed

---

## PR Review Issues

| Category | Total | Fixed | Pending |
|----------|-------|-------|---------|
| Critical | X | X | 0 |
| Important | X | X | 0 |
| Other | X | X | 0 |
| Suggestions | X | X evaluated | 0 |

**Review Compliance:** 100% / X%

---

## OVERALL VERDICT

### PASSED - All checks passed

OR

### FAILED - Issues found:

1. [Issue 1]
2. [Issue 2]
3. [Issue 3]

### Required Actions:
1. [Action 1]
2. [Action 2]
```

### 6.2 Present Report to User

**Output the complete audit report.**

**If PASSED:**
```
===============================================================
AUDIT PASSED: Phase X.Y execution verified
===============================================================
All 11 gates completed.
All 3 mandatory skills invoked.
All tasks implemented.
All quality checks passed.
All PR review issues addressed.

The /plan:execute-next-phase workflow was followed correctly.
===============================================================
```

**If FAILED:**
```
===============================================================
AUDIT FAILED: Phase X.Y execution incomplete
===============================================================

FAILURES FOUND:
1. [Failure description]
2. [Failure description]

REQUIRED REMEDIATION:
1. [What needs to be done]
2. [What needs to be done]

Re-run /plan:execute-next-phase to complete missing steps.
===============================================================
```

**Use `TaskUpdate` to mark "AUDIT 6" as `completed`.**

---

## Quick Audit Commands

For fast verification, run these commands:

```bash
# 1. Check branch
git branch --show-current

# 2. Check review doc exists
ls docs/reviews/phase-*.md

# 3. Check PR exists
gh pr view

# 4. Run quality checks (use detected commands from Project Detection)
cd <project-root>
<detected-test-command>
<detected-analyse-command>  # if configured
<detected-format-check-command>  # if configured

# 5. Check git is clean
git status
```

---

## Remediation Guide

### If Gates Missing

| Missing Gate | Remediation |
|--------------|-------------|
| GATE 3 | Re-run `/superpowers:executing-plans` |
| GATE 5 | Run `/superpowers:brainstorming` for test coverage |
| GATE 6 | Run `/pr-review-toolkit:review-pr` |
| GATE 7 | Fix all issues from review |
| GATE 8 | Create `docs/reviews/phase-X.Y-*.md` (ensure `docs/reviews/` directory exists first) |

### If Quality Checks Fail

Use the detected format command to fix code style, then re-run quality checks:

```bash
cd <project-root>

# Fix code style (if format command configured)
<detected-format-command>

# Re-run checks
<detected-test-command>
<detected-analyse-command>  # if configured
<detected-format-check-command>  # if configured
```

### If Implementation Incomplete

1. Read the phase plan again
2. Identify missing tasks
3. Implement missing tasks with TDD
4. Re-run quality checks

---

## Self-Check Questions

Before marking audit complete:

| Question | Answer |
|----------|--------|
| Did I verify ALL 11 gates? | Yes/No |
| Did I check ALL 3 mandatory skill invocations? | Yes/No |
| Did I verify EVERY task from the phase plan? | Yes/No |
| Did I run ALL quality commands? | Yes/No |
| Did I check ALL PR review issues? | Yes/No |
| Did I generate the complete audit report? | Yes/No |

**If ANY answer is "No", the audit is incomplete.**

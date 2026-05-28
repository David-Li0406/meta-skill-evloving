<!--
Embedded Navigator Command: build
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Write, Edit, Bash, AskUserQuestion
argument-hint: <spec file>
description: Execute spec with atlas pattern guidance (auto-creates implementation branch)
---

## Context

Arguments: `/spec-build <SPEC_FILE>`
- **<spec_file>** - Path to spec file

Current directory: !`pwd`
Current branch: !`git branch --show-current`

## Workflow

### 1. Pre-flight

**Verify atlas:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**Verify spec:**
```bash
test -f "{spec_file}" && echo "EXISTS" || echo "NOT_FOUND"
```

### 2. Load Context

**Read spec:**
- Parse prerequisites, steps, validation
- Get domains and patterns referenced

**Load atlas:**
- SKILL.md and schema.yaml
- Relevant domain references
- Relevant pattern guides

### 3. Verify Prerequisites

Check all prerequisite files exist.

If missing → Block or ask to skip.

### 4. Setup Implementation Branch

**Extract from spec:**
- `{target_branch}` - from `**Implementation Branch**:` line
- `{base_branch}` - from `**Base Branch**:` line

**If NO branch specified in spec:**
- Use `AskUserQuestion`:
  ```
  ⚠️ No branch specified in spec. Which branch should be used?
  - Enter branch name, or
  - Type 'current' to use current branch
  ```
- If user provides branch name → use as `{target_branch}`
- If user types 'current' → set `{target_branch}` = result of `git branch --show-current`, skip to step 4.4

#### Step 4.1: Get Current Branch

```bash
git branch --show-current
```

Compare `{target_branch}` with current branch.

#### Step 4.2: Handle Branch Match/Mismatch

**✅ If branches MATCH:** Skip to Step 4.4

**❌ If branches DON'T MATCH:**

1. **Check if target branch exists:**
   ```bash
   # Check locally
   git branch --list {target_branch}

   # Check remotely
   git branch -r --list origin/{target_branch}
   ```

2. **Branch EXISTS (locally or remotely):**
   - Use `AskUserQuestion`:
     ```
     ⚠️ Branch mismatch:
       Current: {current_branch}
       Required: {target_branch}

     Switch to {target_branch}? (yes/no)
     ```
   - **If YES:**
     ```bash
     git checkout {target_branch}
     ```
     - If checkout fails → Go to Step 4.3
     - If successful → Go to Step 4.4
   - **If NO:** EXIT with message "Switch to `{target_branch}` manually, then re-run /spec-build"

3. **Branch DOESN'T EXIST:**
   - Use `AskUserQuestion`:
     ```
     Branch `{target_branch}` doesn't exist.
     Create it from `{base_branch}`? (yes/no/custom)

     - yes: Create from {base_branch}
     - no: Cancel implementation
     - custom: Specify different base branch
     ```
   - **If YES:**
     ```bash
     git checkout -b {target_branch} {base_branch}
     ```
     - If creation fails → Go to Step 4.3
     - If successful → Go to Step 4.4
   - **If CUSTOM:**
     - Ask: "Enter base branch name:"
     - Run: `git checkout -b {target_branch} {user_provided_base}`
     - Handle failure same as above
   - **If NO:** EXIT with message "Create branch manually, then re-run /spec-build"

#### Step 4.3: Handle Git Operation Failures

**Display the full error message and identify common issues:**

| Error Pattern | Suggested Fix |
|---------------|---------------|
| "uncommitted changes" | "Stash or commit your changes: `git stash` or `git commit -am 'msg'`" |
| "conflict" | "Resolve merge conflicts first, then retry" |
| "not found" / "unknown revision" | "Branch or remote not found. Check spelling or run `git fetch --all`" |
| "permission denied" | "Check file permissions or if files are locked by another process" |
| "CONFLICT" | "Merge conflict detected. Resolve conflicts, then `git add .` and retry" |

**Use `AskUserQuestion`:**
```
❌ Git operation failed:
{full_error_message}

Suggested fix: {suggestion from table above}

Resolve the issue and re-run /spec-build.
Press Enter to exit.
```
**EXIT**

#### Step 4.4: Verify Branch Setup Complete

**Confirm successful branch setup:**
```bash
git branch --show-current
```

**Report:**
```
✅ On branch: {target_branch}
   Based on: {base_branch}
```

Proceed to implementation.

### 5. Load Pattern Guidance

For each pattern guide:
- Read conventions
- Note anti-patterns

Build guidance context for implementation.

### 6. Execute Steps

For each step:

1. **Announce:** "### Step N: {Title}"
2. **Load context:** Read relevant files
3. **Implement:** Follow spec + patterns
4. **Verify:** Check outcome
5. **Report:** "✅ Step N complete"

If step fails: Report error, attempt recovery, ask if blocked.

### 7. Run Validation

Execute validation commands:
```bash
{type_check}
{tests}
{lint}
{build}
```

**Loop:** Max 3 attempts per validation. Fix and retry.

### 8. Final Verification

Check success criteria from spec.
Review pattern adherence.

### 9. Report

```markdown
## Build Complete

**Spec:** `{spec_file}`

### Steps Completed
{list}

### Files Modified
{list}

### Validation
- Type check: ✅
- Tests: ✅
- Lint: ✅
- Build: ✅

### Success Criteria
{list with status}

### Next Steps
1. `/spec-review {spec_file}`
2. Commit changes
3. Create PR
```

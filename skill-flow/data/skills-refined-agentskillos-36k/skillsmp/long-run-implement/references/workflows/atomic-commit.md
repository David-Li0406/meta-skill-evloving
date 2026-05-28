# Atomic Commit Protocol

## Purpose
Create per-task atomic commits with conventional commit format.

## Inputs
- `task`: Completed task object
- `plan_number`: Current plan number (e.g., "02")
- `task_number`: Current task number (e.g., 1)
- `files`: Array of file paths from <files> element

## Commit Type Inference

### Rules
| Condition | Type | Example |
|-----------|------|---------|
| New file created | `feat` | `feat(02): create API controller` |
| Existing file modified (new functionality) | `feat` | `feat(02): add auth middleware` |
| Bug fix (deviation Rule 1) | `fix` | `fix(02): correct validation logic` |
| Test file created/modified | `test` | `test(02): add API endpoint tests` |
| Refactor (no behavior change) | `refactor` | `refactor(02): extract helper function` |
| Config/dependency change | `chore` | `chore(02): add bcrypt dependency` |
| Documentation only | `docs` | `docs(02): add API comments` |

### Detection Logic
```
FOR each file in files:
  IF file is new (not in git):
    IF file matches *test* or *spec*:
      type_votes.push("test")
    ELSE:
      type_votes.push("feat")

  IF file is modified:
    diff = git diff file
    IF diff contains only comments/docs:
      type_votes.push("docs")
    ELSE IF diff is refactor (same behavior):
      type_votes.push("refactor")
    ELSE:
      type_votes.push("feat")

# Special overrides
IF task was deviation Rule 1 (bug fix):
  type = "fix"
ELSE IF all files are config (package.json, tsconfig, etc):
  type = "chore"
ELSE:
  type = most_common(type_votes) or "feat"
```

## Workflow

### Step 1: Pre-Commit Checks
```
1. Verify task completed successfully
2. Check verification command passed
3. Ensure files list is not empty
```

### Step 2: Stage Files
```
FOR each file in files:
  git add {file}

# Verify only expected files staged
staged = git diff --cached --name-only
unexpected = staged - files
IF unexpected.length > 0:
  FOR each file in unexpected:
    git reset HEAD {file}
  Log warning to SUMMARY.md
```

### Step 3: Create Commit
```
1. Infer commit type
2. Generate message:
   "{type}({plan_number}): {task.name}"

3. Execute commit:
   git commit -m "{message}"

4. Capture commit hash:
   hash = git rev-parse HEAD --short
```

### Step 4: Update Checkpoint
```
Read {plan}-CHECKPOINT.json
Update:
  - last_completed_task = task_number
  - task_commits[task_number] = hash
  - files_modified += files
  - updated_at = ISO timestamp
Write atomically
```

### Step 5: Output
```
Return {
  success: true,
  commit_hash: hash,
  commit_message: message,
  files_committed: files,
  type: inferred_type
}
```

## Error Handling

### Staging Fails
```
IF git add fails:
  Check if file exists
  Check file permissions
  Return error with details
```

### Commit Fails
```
IF git commit fails:
  Check for pre-commit hook failure
  IF hook modified files:
    Re-stage and retry (amend rules apply)
  ELSE:
    Return error with hook output
```

### Checkpoint Write Fails
```
IF checkpoint write fails:
  Commit already succeeded
  Log warning
  Checkpoint can be recovered from git log
```

## Examples

### New Feature File
```
Input:
  files: ["src/api/users/route.ts"]
  task.name: "Create users API endpoint"
  plan_number: "02"

Output:
  commit_hash: "abc1234"
  commit_message: "feat(02): Create users API endpoint"
```

### Test File
```
Input:
  files: ["src/api/__tests__/users.test.ts"]
  task.name: "Add users API tests"
  plan_number: "02"

Output:
  commit_hash: "def5678"
  commit_message: "test(02): Add users API tests"
```

### Bug Fix (Deviation)
```
Input:
  files: ["src/api/users/route.ts"]
  task.name: "Fix validation logic"
  plan_number: "02"
  deviation_rule: 1

Output:
  commit_hash: "ghi9012"
  commit_message: "fix(02): Fix validation logic"
```

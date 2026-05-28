

# Start-Phase Python Tools

Quality gate and validation tools for phase management.

## Tools (4 CRITICAL)

### 1. quality_gate.py - Quality Enforcement 🚦

**Purpose:** Run lint, build, and optional test checks

**Usage:**
```bash
# Run lint + build
python quality_gate.py /path/to/project

# Run lint + build + tests
python quality_gate.py /path/to/project --test
```

**Checks performed:**

**A. Lint Check** (required)
- Tries: `npm run lint`, `yarn lint`, `npx eslint .`
- Must pass: Zero lint errors
- Parses errors from output

**B. Build Check** (required)
- Tries: `npm run build`, `yarn build`, `npx tsc --noEmit`
- Must pass: Build completes without errors
- Detects TypeScript errors, module not found, etc.

**C. Test Check** (optional with --test)
- Tries: `npm test`, `yarn test`, `npx jest`
- Can pass even if tests fail (soft warning)
- Useful for CI/CD pipelines

**Output:**
```json
{
  "passed": true,
  "checks": {
    "lint": {
      "passed": true,
      "output": "...",
      "errors": []
    },
    "build": {
      "passed": true,
      "output": "...",
      "errors": []
    },
    "test": {
      "passed": null,
      "output": "...",
      "errors": []
    }
  },
  "summary": {
    "total_checks": 2,
    "passed_checks": 2,
    "failed_checks": 0
  }
}
```

**Exit codes:**
- 0: All checks passed
- 1: One or more checks failed

**Integration:**
- Used by quality-gate hook
- Runs after every task
- Blocks next task if fails

---

### 2. task_validator.py - Task Completion Validation ✅

**Purpose:** Validate task has all required artifacts

**Usage:**
```bash
python task_validator.py /path/to/project task-name
```

**Example:**
```bash
python task_validator.py ~/my-app setup-auth-api
```

**Validates:**

**A. Task Update File**
- Exists: `planning/task-updates/task-name.md`
- Not empty: >100 bytes
- Has sections: "What Changed", "Files Touched", "How to Verify"

**B. Code Review File**
- Exists: `planning/code-reviews/task-name.md`
- Not empty: >100 bytes
- Has sections: "Summary", "Issues", "Verdict"
- Has verdict: "Approved" or "Needs follow-up"

**C. Checklist Completion**
- Task update has checklist
- All items checked: `- [x]`
- Required items present:
  - Lint passed
  - Build passed
  - Review completed
  - Commit created

**D. Git Commit**
- Commit exists in git log
- Message contains task name
- Alternative formats checked

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Task update missing section: How to Verify"
  ],
  "checks_passed": 4,
  "total_checks": 4,
  "completion_percentage": 100.0
}
```

**Exit codes:**
- 0: Validation passed (may have warnings)
- 1: Validation failed (has errors)

**Integration:**
- Used by quality-gate hook
- Runs after quality checks pass
- Ensures documentation complete

---

### 3. validate_phase.py - Phase Structure Validation 📁

**Purpose:** Validate phase directory structure and planning files

**Usage:**
```bash
python validate_phase.py /path/to/project
```

**Validates:**

**A. Directory Structure**
- `planning/task-updates/` exists
- `planning/agent-delegation/` exists
- `planning/phase-structure/` exists
- `planning/code-reviews/` exists

**B. Planning Files**
- `planning/agent-delegation/task-delegation.md` exists
  - Contains Mermaid graph
  - Has agent assignments
  - Has priorities

- `planning/agent-delegation/sub-agent-plan.md` exists
  - Contains parallel execution strategy
  - Tasks organized into waves

- `planning/phase-structure/system-changes.md` exists
  - Contains Mermaid flowchart
  - Has SLOC tracking table

**C. Task Updates**
- Task update files exist
- Have required sections
- Have quality gate checklist

**D. Code Reviews**
- Code review files exist
- Have required sections
- Have clear verdict

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Planning file not found: planning/agent-delegation/task-delegation.md"
  ],
  "checks_passed": 8,
  "total_checks": 10,
  "structure_complete": false
}
```

**Exit codes:**
- 0: Structure valid (no errors, may have warnings)
- 1: Structure invalid (has errors)

**Integration:**
- Used by phase-start hook
- Validates setup before execution
- Can be run anytime to check status

---

### 4. sloc_tracker.py - SLOC Change Tracking 📊

**Purpose:** Track Source Lines of Code changes per file

**Usage:**

**Create baseline:**
```bash
python sloc_tracker.py /path/to/project --baseline src/api/auth.ts src/types/user.ts
```

**Update current SLOC:**
```bash
# Update specific files
python sloc_tracker.py /path/to/project --update src/api/auth.ts

# Update all tracked files
python sloc_tracker.py /path/to/project --update
```

**Generate final report:**
```bash
python sloc_tracker.py /path/to/project --final
```

**Workflow:**

1. **At phase start** (Part 2):
   ```bash
   # Create baseline for all files that will be changed
   python sloc_tracker.py . --baseline \
     src/api/auth.ts \
     src/types/user.ts \
     src/lib/db.ts
   ```

2. **During phase** (optional):
   ```bash
   # Update current SLOC after tasks
   python sloc_tracker.py . --update
   ```

3. **At phase end** (Part 5):
   ```bash
   # Generate final report
   python sloc_tracker.py . --final
   ```

**Output (--baseline):**
```json
{
  "action": "baseline_created",
  "files_tracked": 3,
  "total_baseline_sloc": 425,
  "baseline": {
    "src/api/auth.ts": {
      "baseline": 0,
      "current": 0,
      "delta": 0
    },
    "src/types/user.ts": {
      "baseline": 45,
      "current": 45,
      "delta": 0
    }
  }
}
```

**Output (--final):**
```json
{
  "action": "final_report",
  "summary": {
    "total_files": 3,
    "total_baseline_sloc": 45,
    "total_current_sloc": 892,
    "total_delta": 847,
    "files_created": 1,
    "files_modified": 2,
    "files_deleted": 0
  },
  "distribution": {
    "counts": {
      "source": 682,
      "tests": 210,
      "docs": 0,
      "other": 0
    },
    "percentages": {
      "source": 76.5,
      "tests": 23.5,
      "docs": 0.0,
      "other": 0.0
    },
    "total": 892
  },
  "markdown_table": "| File | Baseline SLOC | Current SLOC | Delta | Change % |\n..."
}
```

**SLOC Counting Rules:**
- Counts only non-blank, non-comment lines
- Skips: empty lines, `//` comments, `#` comments, `/* */` blocks
- Counts: actual code lines

**Stored baseline:**
- Location: `planning/phase-structure/.sloc-baseline.json`
- Format: JSON
- Tracks: baseline, current, delta per file

**Integration:**
- Used in Part 2 (create baseline)
- Used in Part 5 (final report)
- Updates `system-changes.md` with markdown table

---

## Dependencies

**None!** All tools use Python standard library only:
- `json` - JSON parsing
- `subprocess` - Running commands
- `pathlib` - File path handling
- `re` - Regular expressions
- `sys` - CLI arguments

No `pip install` required!

---

## Integration with Hooks

### phase-start Hook
- Runs: `validate_phase.py`
- When: Before Mode 2 starts
- Purpose: Ensure structure ready

### quality-gate Hook
- Runs: `quality_gate.py` → `task_validator.py`
- When: After each task
- Purpose: Enforce quality + validate completion

### phase-complete Hook
- Runs: `sloc_tracker.py --final`
- When: After all tasks
- Purpose: Generate SLOC report

---

## Performance

| Tool | Typical Time | When |
|------|--------------|------|
| **quality_gate.py** | 10-30s | Per task (lint + build) |
| **task_validator.py** | <2s | Per task |
| **validate_phase.py** | <3s | Phase start |
| **sloc_tracker.py** | <5s | Baseline, update, final |

**Total overhead per task:** ~15-35 seconds (quality gate + validation)

**Worth it:** Prevents hours of debugging broken code.

---

## Error Handling

All tools handle errors gracefully:

### Missing Commands
```json
{
  "passed": false,
  "checks": {
    "lint": {
      "passed": false,
      "output": "No lint command available (tried: npm run lint, yarn lint, npx eslint)",
      "errors": ["Lint command not found"]
    }
  }
}
```

### File Not Found
```json
{
  "valid": false,
  "errors": ["Task update file not found: planning/task-updates/task-name.md"],
  "warnings": []
}
```

### Timeout
```json
{
  "checks": {
    "build": {
      "passed": false,
      "output": "Command timed out after 300 seconds"
    }
  }
}
```

---

## Testing Tools

Test each tool independently:

### Test quality_gate.py
```bash
# Navigate to a project with lint/build
cd ~/my-app

# Run quality gate
python ~/.claude/skills/start-phase/scripts/quality_gate.py .

# Expected: JSON output with pass/fail
```

### Test task_validator.py
```bash
# Create test task files first
mkdir -p planning/task-updates planning/code-reviews

echo "# Task Update
## What Changed
Test change
## Files Touched
- test.ts
## How to Verify
Run test
## Checklist
- [x] Lint passed
- [x] Build passed
- [x] Review completed
- [x] Commit created
" > planning/task-updates/test-task.md

echo "# Code Review
## Summary
Good code
## Issues
None
## Verdict
Approved
" > planning/code-reviews/test-task.md

# Run validator
python ~/.claude/skills/start-phase/scripts/task_validator.py . test-task

# Expected: JSON with valid: true
```

### Test validate_phase.py
```bash
# Create test structure
mkdir -p planning/{task-updates,agent-delegation,phase-structure,code-reviews}

# Run validator
python ~/.claude/skills/start-phase/scripts/validate_phase.py .

# Expected: JSON with structure_complete: true or warnings
```

### Test sloc_tracker.py
```bash
# Create baseline
python ~/.claude/skills/start-phase/scripts/sloc_tracker.py . --baseline src/index.ts

# Update SLOC
python ~/.claude/skills/start-phase/scripts/sloc_tracker.py . --update

# Generate final report
python ~/.claude/skills/start-phase/scripts/sloc_tracker.py . --final

# Expected: JSON with SLOC data and markdown table
```

---

## Troubleshooting

### quality_gate.py not finding commands

**Problem:** "No lint command available"

**Solutions:**
1. Add lint script to package.json:
   ```json
   {
     "scripts": {
       "lint": "eslint ."
     }
   }
   ```

2. Install linter:
   ```bash
   npm install --save-dev eslint
   ```

3. Check if npm/yarn is in PATH:
   ```bash
   which npm
   ```

---

### task_validator.py reports missing files

**Problem:** "Task update file not found"

**Solution:**
Ensure task name matches exactly:
```bash
# If task is "setup-auth-api"
# File must be: planning/task-updates/setup-auth-api.md
# NOT: planning/task-updates/setup_auth_api.md
```

---

### sloc_tracker.py baseline not found

**Problem:** "No baseline found"

**Solution:**
Create baseline first:
```bash
python sloc_tracker.py . --baseline src/**/*.ts
```

Baseline saved to: `planning/phase-structure/.sloc-baseline.json`

---

### Tool returns non-zero exit code

**Expected behavior:**
- Tools return exit code 1 when checks fail
- This is intentional for CI/CD integration
- Check JSON output for details

---

## CI/CD Integration

Tools designed for CI/CD pipelines:

```yaml
# GitHub Actions example
- name: Quality Gate
  run: |
    python .claude/skills/start-phase/scripts/quality_gate.py . --test

- name: Validate Phase
  run: |
    python .claude/skills/start-phase/scripts/validate_phase.py .
```

Exit codes:
- 0 = Success
- 1 = Failure (fails CI build)

---

## Future Enhancements

Potential improvements (not implemented):

1. **quality_gate.py:**
   - Configurable timeout per command
   - Custom lint/build commands
   - Parallel check execution

2. **task_validator.py:**
   - Check code coverage threshold
   - Validate commit message format
   - Check for TODOs in code

3. **validate_phase.py:**
   - Validate Mermaid syntax
   - Check task dependencies
   - Verify no circular dependencies

4. **sloc_tracker.py:**
   - Support more languages (Java, Go, Rust)
   - Complexity metrics (cyclomatic complexity)
   - Churn analysis (files changing frequently)

---

## Summary

Four critical tools for quality enforcement:

1. **quality_gate.py** 🚦 - Enforce lint/build/test standards
2. **task_validator.py** ✅ - Validate task completion
3. **validate_phase.py** 📁 - Validate phase structure
4. **sloc_tracker.py** 📊 - Track code changes

**Zero dependencies** - Python stdlib only
**Fast execution** - Total overhead ~20-40s per task
**Comprehensive validation** - Catches issues early

**Result:** Quality-enforced phase management with automated checks.

---

See `hooks/start-phase/README.md` for hook integration details.
See `skills/start-phase/README.md` for complete start-phase documentation.

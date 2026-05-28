# Verifying On-Disk State

Cross-reference agent deliverables against actual filesystem state to verify what was successfully completed.

## Why Verification Matters

Agent logs show *intent* but not *outcome*:
- Write tool was called, but file may not exist (crash during write)
- Edit tool was called, but changes may be partial
- Tests were invoked, but results may be incomplete
- Files exist but may be empty or corrupted

**Always verify on-disk state before marking work as complete.**

## Verification Checklist

For each task/agent, verify:

- [ ] All expected files exist
- [ ] Files have content (not empty)
- [ ] Modification time aligns with session
- [ ] Code has no syntax errors (lint check)
- [ ] Tests pass (if test files created)
- [ ] Imports resolve (no missing dependencies)

## File Existence Verification

### Basic Existence Check

```bash
# For each file_path extracted from logs:
check_file() {
    local file_path="$1"
    if [ -f "$file_path" ]; then
        echo "VERIFIED: $file_path exists"
    else
        echo "MISSING: $file_path not found"
    fi
}

# Usage with extracted files
for file in $(cat extracted_files.txt); do
    check_file "$file"
done
```

### With Size Validation

```bash
# Verify file exists and has content
verify_file() {
    local file_path="$1"
    if [ ! -f "$file_path" ]; then
        echo "MISSING: $file_path"
        return 1
    fi

    local size=$(stat -f "%z" "$file_path")
    if [ "$size" -eq 0 ]; then
        echo "EMPTY: $file_path (0 bytes)"
        return 1
    fi

    echo "OK: $file_path ($size bytes)"
    return 0
}
```

### With Timestamp Validation

```bash
# Verify file was modified during session
verify_file_time() {
    local file_path="$1"
    local session_start="$2"  # Unix timestamp

    if [ ! -f "$file_path" ]; then
        echo "MISSING: $file_path"
        return 1
    fi

    local mtime=$(stat -f "%m" "$file_path")
    if [ "$mtime" -lt "$session_start" ]; then
        echo "STALE: $file_path (modified before session)"
        return 1
    fi

    echo "OK: $file_path (modified during session)"
    return 0
}
```

## Code Quality Verification

### Python Syntax Check

```bash
# Check Python file for syntax errors
check_python() {
    local file="$1"
    if python -m py_compile "$file" 2>/dev/null; then
        echo "VALID: $file"
    else
        echo "SYNTAX ERROR: $file"
    fi
}

# Check all Python files from agent
for file in $(grep -l '\.py$' extracted_files.txt); do
    check_python "$file"
done
```

### TypeScript/JavaScript Check

```bash
# Use tsc for TypeScript
check_typescript() {
    local file="$1"
    if npx tsc --noEmit "$file" 2>/dev/null; then
        echo "VALID: $file"
    else
        echo "TYPE ERROR: $file"
    fi
}

# Use eslint for JavaScript
check_javascript() {
    local file="$1"
    if npx eslint "$file" 2>/dev/null; then
        echo "VALID: $file"
    else
        echo "LINT ERROR: $file"
    fi
}
```

### Quick Lint Check

```bash
# Fast syntax validation for multiple languages
quick_lint() {
    local file="$1"
    local ext="${file##*.}"

    case "$ext" in
        py)
            python -m py_compile "$file" 2>/dev/null && echo "OK" || echo "FAIL"
            ;;
        ts|tsx)
            npx tsc --noEmit "$file" 2>/dev/null && echo "OK" || echo "FAIL"
            ;;
        js|jsx)
            node --check "$file" 2>/dev/null && echo "OK" || echo "FAIL"
            ;;
        json)
            jq . "$file" > /dev/null 2>&1 && echo "OK" || echo "FAIL"
            ;;
        *)
            echo "SKIP (unknown type)"
            ;;
    esac
}
```

## Test Verification

### Run Python Tests

```bash
# Run pytest for created test files
run_python_tests() {
    local test_file="$1"
    if pytest "$test_file" -v 2>&1 | tee /tmp/test_output.txt; then
        echo "TESTS PASS: $test_file"
        grep -E '[0-9]+ passed' /tmp/test_output.txt
    else
        echo "TESTS FAIL: $test_file"
        grep -E 'FAILED|ERROR' /tmp/test_output.txt
    fi
}
```

### Run JavaScript Tests

```bash
# Run jest for created test files
run_js_tests() {
    local test_file="$1"
    if npx jest "$test_file" --passWithNoTests 2>&1 | tee /tmp/test_output.txt; then
        echo "TESTS PASS: $test_file"
    else
        echo "TESTS FAIL: $test_file"
    fi
}
```

### Detect Test Files

```bash
# Identify test files from extracted files
find_test_files() {
    local files="$1"
    echo "$files" | grep -E 'test_.*\.py|.*\.test\.(ts|tsx|js|jsx)|.*\.spec\.(ts|tsx|js|jsx)'
}
```

## Git State Verification

### Compare with Git Status

```bash
# Check if files are tracked/modified
verify_git_state() {
    local file="$1"

    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
        # File is tracked
        if git diff --quiet "$file"; then
            echo "UNCHANGED: $file (tracked, no changes)"
        else
            echo "MODIFIED: $file (tracked, has changes)"
        fi
    else
        if [ -f "$file" ]; then
            echo "UNTRACKED: $file (new file)"
        else
            echo "MISSING: $file"
        fi
    fi
}
```

### Get Session Changes

```bash
# List all changes since session start
session_changes() {
    echo "=== Untracked Files ==="
    git ls-files --others --exclude-standard

    echo ""
    echo "=== Modified Files ==="
    git diff --name-only

    echo ""
    echo "=== Staged Files ==="
    git diff --cached --name-only
}
```

## Full Verification Script

```bash
#!/bin/bash
# Full verification workflow for recovered work

set -euo pipefail

EXTRACTED_FILES="$1"
SESSION_START="${2:-$(date -v-3H +%s)}"  # Default: 3 hours ago

echo "=== Verification Report ==="
echo "Session start: $(date -r $SESSION_START)"
echo ""

VERIFIED=0
MISSING=0
ISSUES=0

while IFS= read -r file; do
    [ -z "$file" ] && continue

    echo "Checking: $file"

    # 1. Existence check
    if [ ! -f "$file" ]; then
        echo "  MISSING"
        ((MISSING++))
        continue
    fi

    # 2. Size check
    size=$(stat -f "%z" "$file")
    if [ "$size" -eq 0 ]; then
        echo "  EMPTY (0 bytes)"
        ((ISSUES++))
        continue
    fi

    # 3. Timestamp check
    mtime=$(stat -f "%m" "$file")
    if [ "$mtime" -lt "$SESSION_START" ]; then
        echo "  WARNING: Modified before session"
    fi

    # 4. Syntax check (if applicable)
    ext="${file##*.}"
    case "$ext" in
        py)
            if ! python -m py_compile "$file" 2>/dev/null; then
                echo "  SYNTAX ERROR"
                ((ISSUES++))
                continue
            fi
            ;;
        ts|tsx)
            if ! npx tsc --noEmit "$file" 2>/dev/null; then
                echo "  TYPE ERROR"
                ((ISSUES++))
                continue
            fi
            ;;
    esac

    echo "  VERIFIED ($size bytes)"
    ((VERIFIED++))

done < "$EXTRACTED_FILES"

echo ""
echo "=== Summary ==="
echo "Verified: $VERIFIED"
echo "Missing: $MISSING"
echo "Issues: $ISSUES"

if [ "$MISSING" -gt 0 ] || [ "$ISSUES" -gt 0 ]; then
    exit 1
fi
```

## Node.js Verification

For programmatic verification, see `../scripts/`:

```javascript
import { access, stat, readFile } from 'fs/promises';
import { constants } from 'fs';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function verifyFile(filePath, sessionStart) {
  const result = {
    path: filePath,
    exists: false,
    size: 0,
    modifiedDuringSession: false,
    syntaxValid: null,
    issues: []
  };

  try {
    await access(filePath, constants.R_OK);
    result.exists = true;

    const stats = await stat(filePath);
    result.size = stats.size;
    result.modifiedDuringSession = stats.mtimeMs > sessionStart;

    if (result.size === 0) {
      result.issues.push('File is empty');
    }

    // Syntax check based on extension
    if (filePath.endsWith('.py')) {
      try {
        await execAsync(`python -m py_compile "${filePath}"`);
        result.syntaxValid = true;
      } catch (e) {
        result.syntaxValid = false;
        result.issues.push('Python syntax error');
      }
    }

  } catch (e) {
    result.issues.push(`Access error: ${e.message}`);
  }

  return result;
}
```

## Verification Patterns by Task Type

### UI Component Verification

```bash
# Component file exists
[ -f "src/components/MyComponent.tsx" ] || echo "MISSING: Component"

# Test file exists
[ -f "src/components/MyComponent.test.tsx" ] || echo "MISSING: Tests"

# Story file exists (optional)
[ -f "src/components/MyComponent.stories.tsx" ] || echo "MISSING: Story"

# Run component tests
npx jest MyComponent.test.tsx
```

### API Endpoint Verification

```bash
# Router file
[ -f "app/routers/my_router.py" ] || echo "MISSING: Router"

# Schema file
[ -f "app/schemas/my_schema.py" ] || echo "MISSING: Schema"

# Test file
[ -f "app/tests/test_my_router.py" ] || echo "MISSING: Tests"

# Run API tests
pytest app/tests/test_my_router.py -v
```

### Data Model Verification

```bash
# Model file
[ -f "app/models/my_model.py" ] || echo "MISSING: Model"

# Migration file (check for new migrations)
ls -t alembic/versions/*.py | head -1

# Run migration check
alembic check
```

## Troubleshooting

### File Exists but Empty

```bash
# Check if file was truncated
if [ -f "$file" ] && [ ! -s "$file" ]; then
    echo "File exists but is empty: $file"
    echo "This may indicate a crash during write"
fi
```

### Timestamp Mismatch

```bash
# File older than expected
if [ "$(stat -f "%m" "$file")" -lt "$session_start" ]; then
    echo "File was not modified during session"
    echo "May be pre-existing file that agent intended to modify"
fi
```

### Partial Writes

```bash
# Check for incomplete content
if grep -q 'TODO\|FIXME\|incomplete' "$file"; then
    echo "File may contain incomplete content"
fi
```

## Next Steps

After verification:
1. Mark verified files as COMPLETE
2. Mark missing/invalid files as FAILED or IN_PROGRESS
3. Generate recovery report with `./generating-resumption-plans.md`

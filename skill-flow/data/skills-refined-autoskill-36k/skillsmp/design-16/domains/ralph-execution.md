# Ralph Execution Domain Invariants

Extends: [[system-invariants]]
Domain: Ralph step generation and execution, bash script generation, cross-platform shell compatibility

---

## When to Use

Load this domain for:
- `/design implement` - generating Ralph steps from PRP
- `/design run` - executing Ralph steps
- Any shell script generation for build/test automation
- Cross-platform execution (macOS, Linux, devcontainers)

---

## Domain Invariants (70-76)

### 70. Unix Line Endings Required

**Principle**: All generated shell scripts MUST have Unix line endings (LF only)

**Violation**: CRLF line endings cause `bad interpreter` errors on Unix systems

**Examples**:
- ❌ Script with CRLF: `bad interpreter: /bin/bash^M: no such file or directory`
- ✅ Script with LF only: executes correctly

**Enforcement**:
- After generation: `file *.sh | grep -q CRLF && exit 1`
- Fix: `sed -i '' 's/\r$//' *.sh`

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 71. Directory Creation Before File Write

**Principle**: Every file write to a nested path MUST be preceded by directory creation

**Violation**: `cat > path/to/nested/file.py` fails if parent directories don't exist

**Examples**:
- ❌ `cat > tests/unit/generation/test_file.py << 'EOF'` (fails if dirs missing)
- ✅ `mkdir -p tests/unit/generation && cat > tests/unit/generation/test_file.py << 'EOF'`
- ✅ Use helper: `write_file() { mkdir -p "$(dirname "$1")" && cat > "$1"; }`

**Enforcement**:
- Grep for `cat >` without preceding `mkdir -p $(dirname ...)` → REJECT
- Or use `write_file` helper in all steps

**Pattern**:
```bash
write_file() {
  mkdir -p "$(dirname "$1")"
  cat > "$1"
}

write_file src/components/new/file.tsx << 'EOF'
// content
EOF
```

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 72. Bash 3.2 Compatibility Required

**Principle**: Ralph scripts MUST work with Bash 3.2 (macOS default) or explicitly fail with version check

**Violation**: Using Bash 4+ features (associative arrays, `${var,,}`, `|&`) breaks on stock macOS

**Examples**:
- ❌ `declare -A map` (associative arrays require Bash 4+)
- ❌ `${var,,}` (lowercase expansion requires Bash 4+)
- ❌ `cmd |& tee log` (pipe stderr requires Bash 4+)
- ✅ Use case statements instead of associative arrays
- ✅ Use `tr '[:upper:]' '[:lower:]'` for case conversion
- ✅ Use `cmd 2>&1 | tee log` for piping both streams

**Enforcement**:
- Run `shellcheck --shell=bash *.sh` with no Bash 4+ warnings
- Or add version check at script start:
```bash
if ((BASH_VERSINFO[0] < 4)); then
  echo "Error: Bash 4+ required. macOS users: brew install bash"
  exit 1
fi
```

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 73. Self-Contained Steps

**Principle**: Each step script MUST be executable independently without relying on previous steps

**Violation**: Step N assumes Step N-1 created directories or set variables

**Examples**:
- ❌ Step 5 writes to `src/routing/` assuming Step 1 created it
- ✅ Step 5 includes `mkdir -p src/routing` before writing
- ✅ Step 00 (setup) creates ALL directories upfront and is always run first

**Enforcement**:
- Each step either creates its own directories OR
- Generate step-00-setup.sh that creates all directories from PRP analysis
- Steps must pass when run in isolation: `./step-05.sh` works without running 01-04

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 74. Project Root Verification

**Principle**: Runner scripts MUST verify PROJECT_ROOT by checking for marker files

**Violation**: Incorrect relative path calculation leads to files created in wrong location

**Examples**:
- ❌ `PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"` (off-by-one error)
- ✅ Verify after calculation:
```bash
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]] && [[ ! -f "$PROJECT_ROOT/package.json" ]]; then
  echo "ERROR: PROJECT_ROOT ($PROJECT_ROOT) doesn't look like a project root"
  echo "Expected to find pyproject.toml or package.json"
  exit 1
fi
```

**Enforcement**: All runner scripts must verify project root before file operations

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 75. Separation of Step and Test Concerns

**Principle**: Step scripts create/modify files. Test scripts verify. Never mix.

**Violation**: Running pytest/build/validation inside step-NN.sh

**Examples**:
- ❌ Step script runs `python -m pytest` (fails if deps not installed)
- ❌ Step script runs `npm run build` as validation (belongs in test)
- ✅ Step script only uses: `cat >`, `mkdir -p`, `cp`, `mv`, `sed`
- ✅ Test script runs: `grep`, `test -f`, `npm run build`, `pytest`

**Enforcement**:
- Step scripts: file creation only (cat, mkdir, cp, mv, sed, echo)
- Test scripts: verification only (grep, test, npm, python, curl)
- Grep step scripts for `pytest`, `npm run`, `python -m` → REJECT

**Pattern**:
```bash
# step-NN.sh - ONLY creates files
cat > src/routing/intent.py << 'EOF'
# code
EOF

# test-NN.sh - verifies files exist and content
check_file "src/routing/intent.py"
check "grep -q 'class Intent' src/routing/intent.py" "Intent class exists"
```

**Source**: LEARNINGS-2026-01-23 (HLS Pathology project)

---

### 76. Python Interpreter Portability

**Principle**: Always use `python3` not `python` in shell scripts

**Violation**: `python` not in PATH on many systems (macOS, some Linux distros)

**Examples**:
- ❌ `python -c "import sys; print(sys.version)"` (fails on macOS)
- ❌ `python script.py` (fails if python not aliased)
- ✅ `python3 -c "import sys; print(sys.version)"`
- ✅ `python3 script.py`

**Enforcement**:
- Grep for `python -c` or `python ` without `3` → REJECT
- test-utils.sh must use `python3` in all check functions

**Source**: LEARNINGS-2026-01-23 (SA Assistant project)

---

## Validation Commands

Add to PRP validation section:
```bash
# INV-70: Unix line endings
file ralph-steps/*.sh | grep -v "ASCII text" && echo "FAIL: Non-Unix line endings" && exit 1

# INV-71: Directory creation before write
grep -n "cat >" ralph-steps/step-*.sh | grep -v "mkdir -p" && echo "WARN: cat without mkdir"

# INV-72: Bash compatibility
shellcheck --shell=bash ralph-steps/*.sh

# INV-73: Self-contained (each step creates dirs)
# Manual review required

# INV-74: Project root verification
grep -L "pyproject.toml\|package.json" ralph-steps/ralph.sh && echo "FAIL: No root verification"

# INV-75: Separation of concerns
grep -E "pytest|npm run|python -m" ralph-steps/step-*.sh && echo "FAIL: Step runs validation"

# INV-76: Python3 portability
grep "python -c\|python '" ralph-steps/*.sh && echo "FAIL: Use python3"
```

---

## Step Template with Invariants

```bash
#!/bin/bash
# INV-70: This file must have LF line endings
# INV-72: Bash 3.2 compatible (no associative arrays)
# INV-73: Self-contained (creates own directories)
# INV-74: Verifies project root
# INV-75: Only creates files (no validation)
# INV-76: Uses python3

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# INV-74: Verify project root
if [[ ! -f "$PROJECT_ROOT/pyproject.toml" ]] && [[ ! -f "$PROJECT_ROOT/package.json" ]]; then
  echo "ERROR: Not in project root"
  exit 1
fi

cd "$PROJECT_ROOT"

# INV-71: Helper function for safe file writes
write_file() {
  mkdir -p "$(dirname "$1")"
  cat > "$1"
}

# === IMPLEMENTATION ===
write_file src/example/file.py << 'EOF'
# content
EOF

echo "Step complete"
```

---

*Domain version: 1.0*
*Created: 2026-01-23*
*Source: Ralph execution failures across SA Assistant and HLS Pathology projects*

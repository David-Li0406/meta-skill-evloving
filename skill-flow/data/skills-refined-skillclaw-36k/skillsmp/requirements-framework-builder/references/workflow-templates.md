# Workflow Templates for Requirements Framework Builder

Detailed templates and scripts for the requirements framework implementation process.

## Status Display Template

Present status in this format:

```markdown
## Requirements Framework - Implementation Status

**Current Phase**: [phase number] ([phase name])
**Current Step**: [step number] ([step name])
**Overall Progress**: [percentage]% ([completed]/[total] steps)

### Progress Bar
[████████░░░░░░░░] 45%

### Completed Steps
✓ 1.1 - Directory structure
✓ 1.2 - Session management
✓ 1.3 - Git utilities

### In Progress
→ 1.4 - State storage

### Remaining in Phase
- 1.5 Config loader
- 1.6 Requirements manager
- 1.7 PreToolUse hook

**Estimated Time Remaining**: [X] hours
**On Track**: ✓ / ⚠️ / ❌
```

## Step Presentation Template

Full template for presenting implementation steps:

```markdown
## Phase [X], Step [Y.Z]: [Step Name]

**Goal**: [One-sentence description of what this step accomplishes]

**Time Estimate**: [X] minutes

**Prerequisites**:
- Step [Y.Z-1] completed
- [Any file/directory dependencies]
- [Any tool requirements]

---

### Implementation

[Detailed code blocks and commands]

```python
# Example code to write
def example_function():
    pass
```

```bash
# Commands to execute
mkdir -p ~/.claude/hooks/lib
```

---

### Verification

Run these checks to verify the step:

```bash
# Check 1: File exists
ls -la ~/.claude/hooks/lib/[filename]

# Check 2: Syntax valid
python3 -m py_compile ~/.claude/hooks/lib/[filename]

# Check 3: Basic functionality
python3 -c "from lib.[module] import [class]; print('✓ Import successful')"
```

**Expected Results**:
- [ ] File created at expected location
- [ ] No syntax errors
- [ ] Import works correctly

---

**Mark as Complete**: Reply "done" or "completed" when finished

**Having Issues?**: Reply "blocked" or describe the problem
```

## Verification Scripts

### Check All Files Exist

```bash
#!/bin/bash
# verify-files.sh - Check all framework files exist

FILES=(
    "$HOME/.claude/hooks/lib/__init__.py"
    "$HOME/.claude/hooks/lib/session.py"
    "$HOME/.claude/hooks/lib/git_utils.py"
    "$HOME/.claude/hooks/lib/state_storage.py"
    "$HOME/.claude/hooks/lib/config.py"
    "$HOME/.claude/hooks/lib/requirements.py"
    "$HOME/.claude/hooks/check-requirements.py"
    "$HOME/.claude/hooks/requirements-cli.py"
)

echo "Checking framework files..."
MISSING=0
for f in "${FILES[@]}"; do
    if [ -f "$f" ]; then
        echo "✓ $f"
    else
        echo "✗ $f (MISSING)"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo ""
    echo "All files present!"
else
    echo ""
    echo "$MISSING file(s) missing"
fi
```

### Validate Python Syntax

```bash
#!/bin/bash
# validate-syntax.sh - Check all Python files for syntax errors

echo "Validating Python syntax..."
ERRORS=0

for f in ~/.claude/hooks/lib/*.py ~/.claude/hooks/*.py; do
    if [ -f "$f" ]; then
        if python3 -m py_compile "$f" 2>/dev/null; then
            echo "✓ $f"
        else
            echo "✗ $f (SYNTAX ERROR)"
            python3 -m py_compile "$f"
            ERRORS=$((ERRORS + 1))
        fi
    fi
done

if [ $ERRORS -eq 0 ]; then
    echo ""
    echo "All files valid!"
else
    echo ""
    echo "$ERRORS file(s) with errors"
fi
```

### Test Imports

```bash
#!/bin/bash
# test-imports.sh - Test all module imports

echo "Testing module imports..."

cd ~/.claude/hooks

python3 << 'EOF'
import sys
sys.path.insert(0, '.')

modules = [
    ('lib.session', 'get_session_id'),
    ('lib.git_utils', 'get_current_branch'),
    ('lib.state_storage', 'load_state'),
    ('lib.config', 'load_config'),
    ('lib.requirements', 'BranchRequirements'),
]

for module, attr in modules:
    try:
        m = __import__(module, fromlist=[attr])
        getattr(m, attr)
        print(f"✓ {module}.{attr}")
    except Exception as e:
        print(f"✗ {module}.{attr}: {e}")
EOF
```

## Phase Completion Template

```markdown
## Phase [X] Complete! 🎉

**Summary**:
- Duration: [actual time vs estimate]
- Steps completed: [count]
- Steps skipped: [count] (if any)
- Tests passing: [status]
- Blockers encountered: [count]

### What's Working
- ✓ [Feature 1]
- ✓ [Feature 2]
- ✓ [Feature 3]

### Known Limitations
- [Limitation 1]
- [Limitation 2]

### Notes from Implementation
[List of notes from progress file]

---

**Next Steps**:
1. Use the framework for 1-2 weeks
2. Gather feedback on real-world usage
3. Decide if Phase [X+1] features are needed

**Would you like to**:
- Continue to Phase [X+1]
- Take a break and test Phase [X]
- Review what was built
```

## Error Recovery Templates

### Step Failure

```markdown
## Step [Y.Z] Failed ❌

**Error**:
```
[error message]
```

**Diagnosis**:
1. [Possible cause 1] - [likelihood]
2. [Possible cause 2] - [likelihood]
3. [Possible cause 3] - [likelihood]

**Suggested Fixes**:

**Option A (Quick Fix)**:
[Simple fix that addresses symptom]

**Option B (Thorough Fix)**:
[Complete fix that addresses root cause]

**Option C (Workaround)**:
[Alternative approach to achieve same goal]

---

**Which approach should we try?**
```

### Test Failure

```markdown
## Test Failure in [Component]

**Failed Test**: [test name or description]

**Expected**:
```
[expected output/behavior]
```

**Actual**:
```
[actual output/behavior]
```

**Root Cause Analysis**:
[Explanation of why this is happening]

**Fix Required**:
- **File**: [filename]
- **Line**: [line number if applicable]
- **Change**: [description of change]

**Proposed Fix**:
```python
# Before
[old code]

# After
[new code]
```

---

**Apply this fix?** Reply "yes" to proceed or describe an alternative approach.
```

## Blocker Recording Template

```markdown
## Blocker Recorded

**Step**: [Y.Z] - [Step Name]
**Type**: [technical/dependency/unclear/other]
**Description**: [User's description]

**Analysis**:
[Assessment of the blocker]

**Possible Solutions**:
1. [Solution 1]
2. [Solution 2]
3. [Ask user for more info about X]

**Blocker added to progress file**.

---

**How would you like to proceed?**
```

## Prerequisites Check Script

```bash
#!/bin/bash
# check-prerequisites.sh

echo "Checking prerequisites for Requirements Framework..."
echo ""

# Python version
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 9 ]; then
    echo "✓ Python $PYTHON_VERSION (3.9+ required)"
else
    echo "✗ Python $PYTHON_VERSION (3.9+ required)"
fi

# Git
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "✓ Git $GIT_VERSION"
else
    echo "✗ Git not found"
fi

# Write access to ~/.claude
if [ -w "$HOME/.claude" ]; then
    echo "✓ Write access to ~/.claude"
else
    echo "✗ No write access to ~/.claude"
fi

# Claude Code hooks directory
if [ -d "$HOME/.claude/hooks" ]; then
    echo "✓ ~/.claude/hooks directory exists"
else
    echo "⚠ ~/.claude/hooks directory does not exist (will be created)"
fi

# PyYAML (required)
if python3 -c "import yaml" 2>/dev/null; then
    echo "✓ PyYAML installed"
else
    echo "✗ PyYAML not installed (required for YAML config)"
fi

echo ""
echo "Prerequisites check complete."
```

## Progress File Operations

### Initialize Progress File

```python
import json
from datetime import datetime

def init_progress_file(path):
    """Create initial progress file for new implementation."""
    progress = {
        "version": "2.0",
        "current_phase": 1,
        "current_step": "1.1",
        "started_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "phases": {
            "1": {
                "name": "MVP",
                "status": "in_progress",
                "steps": {}
            }
        },
        "notes": [],
        "blockers": []
    }

    with open(path, 'w') as f:
        json.dump(progress, f, indent=2)

    return progress
```

### Update Step Status

```python
def update_step_status(progress_path, step_id, status, note=None):
    """Update status of a specific step."""
    with open(progress_path, 'r') as f:
        progress = json.load(f)

    phase_num = step_id.split('.')[0]

    if phase_num not in progress['phases']:
        progress['phases'][phase_num] = {'name': f'Phase {phase_num}', 'status': 'pending', 'steps': {}}

    step_data = progress['phases'][phase_num]['steps'].get(step_id, {})
    step_data['status'] = status

    if status == 'in_progress':
        step_data['started_at'] = datetime.utcnow().isoformat() + "Z"
    elif status == 'completed':
        step_data['completed_at'] = datetime.utcnow().isoformat() + "Z"

    if note:
        step_data['note'] = note

    progress['phases'][phase_num]['steps'][step_id] = step_data
    progress['current_step'] = step_id
    progress['updated_at'] = datetime.utcnow().isoformat() + "Z"

    with open(progress_path, 'w') as f:
        json.dump(progress, f, indent=2)
```

### Calculate Progress Percentage

```python
def calculate_progress(progress):
    """Calculate overall progress percentage."""
    total_steps = 0
    completed_steps = 0

    for phase in progress['phases'].values():
        for step in phase.get('steps', {}).values():
            total_steps += 1
            if step.get('status') == 'completed':
                completed_steps += 1

    # If no steps tracked yet, estimate based on phase
    if total_steps == 0:
        return 0

    return int((completed_steps / total_steps) * 100)
```

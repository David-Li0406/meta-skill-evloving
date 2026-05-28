# Example: Sequential Task (Skip Parallelization)

## User Request
"Fix the login form validation bug"

## Decomposition Output

### Task Analysis
- Single file change
- Linear dependency chain
- Below parallelization threshold

### Tasks

```
Task 1: Write Failing Test for Bug
- Depends on: none
- Files: components/LoginForm.test.tsx
- Done when: Test reproduces the validation bug
- Complexity: S

Task 2: Fix Validation Logic
- Depends on: [Task 1]
- Files: components/LoginForm.tsx
- Done when: Test passes, validation works correctly
- Complexity: S
```

### Execution Strategy

```
┌─────────────────────────────────────────────────────────────┐
│ ⏸️ Parallelization: DISABLED                                │
│    Reason: Only 2 tasks with linear dependency              │
│    Strategy: Sequential execution in main session           │
│    Order: Test → Fix                                        │
└─────────────────────────────────────────────────────────────┘
```

### Why Not Parallel

| Criterion | Value | Required |
|-----------|-------|----------|
| Independent tasks | 0 | >= 3 |
| Total tasks | 2 | >= 3 |
| Linear dependencies | Yes | No |

**Result:** Skip parallelization, execute sequentially.

### Feature List

```yaml
features:
  - id: task-001
    description: "Write failing test reproducing validation bug"
    status: failing
    verification_command: "npm test -- --testPathPattern='LoginForm'"
    expected_output: "1 failed"  # Test SHOULD fail initially
    evidence_required: true
    can_be_removed: false

  - id: task-002
    description: "Fix validation logic to pass test"
    status: failing
    verification_command: "npm test -- --testPathPattern='LoginForm'"
    expected_output: "Tests: X passed, 0 failed"
    evidence_required: true
    can_be_removed: false
```

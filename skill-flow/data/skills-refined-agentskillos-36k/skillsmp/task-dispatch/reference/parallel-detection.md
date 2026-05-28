# Parallel Task Detection

## Task Format

Tasks in tasks.md follow the pattern:

```
- [ ] TXXX [P?] [Story?] Description in path/to/file.ext
```

Components:
- **Checkbox:** `- [ ]` (markdown checkbox)
- **Task ID:** Sequential (T001, T002, T003...) in execution order
- **[P] marker:** Indicates parallelizable (different files, no dependencies)
- **[Story] label:** Maps to user story (format: [US1], [US2], etc.)
- **Description:** Clear action with exact file path

## Detection Algorithm

```python
def can_parallelize(task_a: str, task_b: str) -> bool:
    """Check if two tasks can run in parallel."""
    # Both must have [P] marker
    if not (has_p_marker(task_a) and has_p_marker(task_b)):
        return False

    # Must be in same phase (prerequisites complete)
    if get_phase(task_a) != get_phase(task_b):
        return False

    # Must modify different files
    files_a = extract_file_paths(task_a)
    files_b = extract_file_paths(task_b)
    if files_a & files_b:  # intersection not empty
        return False

    return True


def has_p_marker(task: str) -> bool:
    """Check if task has [P] parallelization marker."""
    return "[P]" in task


def get_phase(task: str) -> int:
    """Extract phase number from task context."""
    # Implementation depends on tasks.md structure
    # Typically parsed from "## Phase N" headers
    pass


def extract_file_paths(task: str) -> set[str]:
    """Extract file paths mentioned in task description."""
    # Match patterns like:
    # - src/module/file.py
    # - tests/test_file.py
    # - path/to/file.ext
    import re
    pattern = r'\b[\w./]+\.\w+\b'
    return set(re.findall(pattern, task))
```

## Batching Algorithm

Group consecutive parallelizable tasks into batches:

```python
def build_batches(tasks: list[str]) -> list[list[str]]:
    """Group tasks into execution batches."""
    batches = []
    current_batch = []

    for task in tasks:
        if not current_batch:
            current_batch.append(task)
            continue

        # Check if task can join current batch
        can_join = all(
            can_parallelize(task, existing)
            for existing in current_batch
        )

        if can_join:
            current_batch.append(task)
        else:
            # Finalize current batch, start new one
            batches.append(current_batch)
            current_batch = [task]

    if current_batch:
        batches.append(current_batch)

    return batches
```

## Example

Given tasks.md:

```markdown
## Phase 2: Implementation

- [ ] T005 [P] Implement auth middleware in src/middleware/auth.py
- [ ] T006 [P] Setup routing in src/routes/index.py
- [ ] T007 Create base models in src/models/base.py
- [ ] T008 [P] Add logging utility in src/utils/logger.py
- [ ] T009 [P] Create config loader in src/config/loader.py
```

Batching result:

| Batch | Tasks | Reason |
|-------|-------|--------|
| 1 | T005, T006 | Both [P], different files |
| 2 | T007 | No [P] marker |
| 3 | T008, T009 | Both [P], different files |

Execution:
1. Dispatch T005 + T006 simultaneously → wait → review
2. Dispatch T007 → wait → review
3. Dispatch T008 + T009 simultaneously → wait → review

## Edge Cases

**Same file in multiple tasks:**
```
- [ ] T010 [P] Add User model in src/models/user.py
- [ ] T011 [P] Add validation to User in src/models/user.py
```
→ Cannot parallelize (same file: `src/models/user.py`)

**Cross-phase tasks:**
```
## Phase 1
- [ ] T001 [P] Setup database connection

## Phase 2
- [ ] T002 [P] Create User table
```
→ Cannot parallelize (different phases, T002 depends on T001)

**No file path in description:**
```
- [ ] T015 [P] Refactor authentication logic
```
→ Default to sequential (cannot verify file independence)

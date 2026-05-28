---
name: review-criteria
description: Criteria for reviewing Codex worker outputs across 5 dimensions. Use when reviewing code submitted by workers before approval.
---

# Review Criteria Skill

This skill defines how the CEO (Claude) reviews outputs from Codex workers.

## Review Framework

Every Codex output must be reviewed across 5 dimensions:

### 1. Completeness (Required)

**Question**: Did the worker do what was asked?

**Checklist**:
- [ ] All files in task specification were created/modified
- [ ] The "Do" instruction was followed
- [ ] Output contains completion signal (TASK_COMPLETE)

**Fail Conditions**:
- Missing files that were specified
- Partial implementation with TODO comments
- No completion signal

### 2. Acceptance Criteria (Required)

**Question**: Does the output meet all acceptance criteria?

**Process**:
```markdown
For each acceptance criterion in the task:

- [ ] AC-1: {criterion} → PASS/FAIL: {reason}
- [ ] AC-2: {criterion} → PASS/FAIL: {reason}
- [ ] AC-3: {criterion} → PASS/FAIL: {reason}

Criteria Met: {passed}/{total}
```

**Fail Conditions**:
- Any P0/P1 criterion fails
- More than 50% of criteria fail

### 3. Code Quality (Required)

**Question**: Is the code well-written?

| Aspect | Weight | Check |
|--------|--------|-------|
| Patterns | High | Follows existing codebase patterns |
| Bugs | High | No obvious logical errors |
| Error Handling | Medium | Proper try/catch, null checks |
| Readability | Medium | Clear naming, reasonable complexity |
| Security | High | No obvious vulnerabilities |

**Fail Conditions**:
- Doesn't follow existing patterns
- Contains obvious bugs
- Missing critical error handling
- Security vulnerability present

### 4. Integration (Required)

**Question**: Will this work with existing code?

**Checklist**:
- [ ] Imports are correct and exist
- [ ] Exports match expected interface
- [ ] No circular dependencies
- [ ] Types are compatible (if TypeScript)

**Fail Conditions**:
- Broken imports
- Type mismatches
- Circular dependency introduced

### 5. Completeness of Output (Optional)

**Question**: Is the output complete and usable?

**Checklist**:
- [ ] No placeholder comments (`// TODO`, `// FIXME`)
- [ ] No incomplete implementations
- [ ] No `...` or ellipsis in code
- [ ] File contents are complete

**Fail Conditions**:
- Contains placeholder code
- Implementation is skeletal

## Review Decision Matrix

| Completeness | Criteria | Quality | Integration | Decision |
|--------------|----------|---------|-------------|----------|
| ✓ | ✓ | ✓ | ✓ | APPROVED |
| ✓ | ✓ | ✗ | ✓ | NEEDS_REVISION |
| ✓ | ✗ | ✓ | ✓ | NEEDS_REVISION |
| ✓ | ✓ | ✓ | ✗ | NEEDS_REVISION |
| ✗ | - | - | - | NEEDS_REVISION |
| - | ✗✗ | - | - | ESCALATE (if max retries) |

## Writing Review Feedback

### For APPROVED

```markdown
## Review: Task {id} - APPROVED ✓

All criteria met. Output is ready for verification.

**Summary**:
- Completeness: PASS
- Acceptance: {n}/{n} criteria met
- Quality: Good
- Integration: Compatible
```

### For NEEDS_REVISION

```markdown
## Review: Task {id} - NEEDS_REVISION ↻

Attempt {n} of {max}. Issues found:

**Issue 1**: {Specific issue}
- File: {path}
- Line: {number} (if applicable)
- Current: {what's wrong}
- Expected: {what's needed}
- Fix: {specific instruction}

**Issue 2**: {Specific issue}
- Fix: {specific instruction}

**Focus Areas for Retry**:
1. {Priority 1}
2. {Priority 2}
```

### For ESCALATE

```markdown
## Review: Task {id} - ESCALATE ⚠️

Max retries ({max}) reached or blocking issue found.

**Reason for Escalation**: {why}

**Attempts Summary**:
| Attempt | Issue | Feedback Given |
|---------|-------|----------------|
| 1 | {issue} | {feedback} |
| 2 | {issue} | {feedback} |
| 3 | {issue} | {feedback} |

**Options for User**:
1. Provide additional guidance and retry
2. Manually implement this task
3. Skip this task (if [OPTIONAL])
4. Modify requirements
```

## Quality Standards

### Code Pattern Matching

When reviewing, compare against:
1. Files in the same directory
2. Similar components/functions in codebase
3. Patterns specified in design.md
4. Project style guide (if exists)

### Common Issues to Watch For

**JavaScript/TypeScript**:
- Missing async/await
- Unhandled promise rejections
- Incorrect this binding
- Missing type annotations

**React**:
- Missing key props in lists
- Direct state mutation
- Missing dependency arrays in hooks
- Memory leaks (missing cleanup)

**API/Backend**:
- Missing input validation
- SQL injection risks
- Missing authentication checks
- Improper error responses

## Iteration Limits

| Task Type | Max Iterations | Escalate After |
|-----------|----------------|----------------|
| Standard | 3 | 3 failures |
| [CRITICAL] | 5 | 5 failures |
| [OPTIONAL] | 2 | Skip after 2 |

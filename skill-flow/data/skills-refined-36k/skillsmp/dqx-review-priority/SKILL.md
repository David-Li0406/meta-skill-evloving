---
name: dqx-review-priority
description: Categorize review feedback into P0/P1/P2 priorities
compatibility: opencode
metadata:
  workflow: code-review
  audience: dqx-feedback
---

## What I do

Help you categorize CodeRabbit review comments into priority levels so you can address the most critical issues first.

---

## Priority Levels

### P0 - Fix Immediately (Blockers)

**Must fix before merge** - These issues prevent the code from working correctly or passing CI.

**Categories**:
- ❌ **Type errors / mypy failures**
  - Missing type annotations
  - Incorrect type usage
  - Type inference failures

- ❌ **Test failures or missing tests**
  - Tests that don't pass
  - Critical scenarios without test coverage
  - Broken test fixtures

- ❌ **Security vulnerabilities**
  - SQL injection risks
  - Exposed credentials
  - Unsafe data handling

- ❌ **Breaking API changes (unintentional)**
  - Removed public methods
  - Changed method signatures
  - Incompatible return types

- ❌ **Incorrect logic/algorithm**
  - Logic errors that produce wrong results
  - Off-by-one errors
  - Race conditions

- ❌ **Code that won't pass CI**
  - Pre-commit hook failures
  - Linting errors that can't be auto-fixed
  - Import errors

**Processing**: Fix P0 issues FIRST, in order received

---

### P1 - Fix Before Merge (Important)

**Should fix before merge** - These issues affect code quality, maintainability, or completeness.

**Categories**:
- ⚠️ **Missing edge case tests**
  - Empty input handling
  - None/null cases
  - Boundary conditions

- ⚠️ **Unclear variable/function names**
  - Single-letter variables (except loop counters)
  - Abbreviations without context
  - Misleading names

- ⚠️ **Missing docstrings**
  - Public APIs without documentation
  - Complex functions without explanation
  - Incomplete docstring sections (missing Args, Returns, Raises)

- ⚠️ **Code style violations**
  - Inconsistent naming
  - Magic numbers without constants
  - Complex nested logic

- ⚠️ **Performance concerns**
  - N+1 query patterns
  - Unnecessary loops
  - Memory leaks

- ⚠️ **Missing error handling**
  - Unhandled exceptions
  - No validation of inputs
  - Silent failures

**Processing**: Fix P1 issues AFTER P0, in order received

---

### P2 - Consider for Future (Nice-to-have)

**Optional improvements** - These are suggestions that could improve the code but aren't required for merge.

**Categories**:
- 💡 **Refactoring suggestions**
  - Alternative implementations
  - Code organization improvements
  - Pattern suggestions (but current code works)

- 💡 **Performance micro-optimizations**
  - Minor performance improvements (< 5% gain)
  - Premature optimizations
  - Theoretical improvements without benchmarks

- 💡 **Documentation improvements (non-critical)**
  - Additional examples
  - More detailed explanations
  - Related documentation links

- 💡 **Alternative approaches (working code)**
  - Different design patterns
  - More idiomatic solutions
  - Stylistic preferences

**Processing**: Fix P2 issues if time permits, or defer to future work

---

## Decision Tree

Use this to quickly categorize comments:

```
Does it prevent code from working?
├─ YES → P0 (Blocker)
└─ NO
   └─ Does it affect code quality/completeness?
      ├─ YES → P1 (Important)
      └─ NO → P2 (Nice-to-have)
```

**Specific checks**:

**Type error?** → P0
**Test failure?** → P0
**Security issue?** → P0
**Logic error?** → P0

**Missing test for edge case?** → P1
**Unclear naming?** → P1
**Missing docstring?** → P1
**No error handling?** → P1

**Refactoring suggestion?** → P2
**Micro-optimization?** → P2
**Nice-to-have docs?** → P2
**Alternative approach?** → P2

---

## Examples

### Example 1: Type Error (P0)
**Comment**: "Function `process_data` is missing return type annotation"

**Category**: P0 - Blocker
**Reason**: MyPy will fail, preventing merge
**Action**: Add return type immediately

---

### Example 2: Missing Test (P1)
**Comment**: "Add test for empty string input to `validate_tag`"

**Category**: P1 - Important
**Reason**: Edge case not covered, affects completeness
**Action**: Add test before merge

---

### Example 3: Unclear Naming (P1)
**Comment**: "Variable `tmp` should have a more descriptive name"

**Category**: P1 - Important
**Reason**: Affects code readability and maintainability
**Action**: Rename to something meaningful

---

### Example 4: Refactoring (P2)
**Comment**: "Consider using list comprehension instead of for loop"

**Category**: P2 - Nice-to-have
**Reason**: Current code works, this is a stylistic preference
**Action**: Consider for future, not required now

---

### Example 5: Performance Suggestion (P1 or P2?)
**Comment**: "This query runs in O(n²), could be optimized"

**Decision process**:
- Is n typically large? → YES → P1 (performance concern)
- Is n typically small (< 100)? → NO impact → P2 (micro-optimization)

**Context matters!**

---

## Processing Order

**ALWAYS process in this order**: P0 → P1 → P2

**Workflow**:
1. Read all comments
2. Categorize each comment (P0/P1/P2)
3. Group by priority
4. Process P0 comments first
5. Then P1 comments
6. Finally P2 comments if time permits

---

## When to Ask for Clarification

If a comment is ambiguous:

**Example**: "Consider refactoring this"

**Your response**:
```text
"Could you clarify what specific refactoring you'd suggest?
The current approach follows the pattern from {existing_module}.py
(lines {X}-{Y}) for consistency."
```

**Always ask rather than guess!**

---

## When to use me

Use this skill when:
- **Received CodeRabbit feedback** and need to prioritize
- **Multiple review comments** to address
- **Unsure which issues to fix first**
- **Need to explain prioritization** to reviewer

---

## Integration with Workflow

**After categorizing**, address each comment:

For P0 issues:
```javascript
skill({ name: "dqx-code-standards" })  // Check standards
// Fix the issue
skill({ name: "dqx-quality-gate" })    // Verify fix
skill({ name: "dqx-conventional-commit" })  // Commit
```

Repeat for P1, then P2.

---

## Reference

Complete details: **dqx-feedback.md** (agent file)

This skill helps implement the prioritization logic from the dqx-feedback agent workflow.

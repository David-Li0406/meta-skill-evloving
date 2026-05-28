**Skill**: [Multi-Agent E2E Validation](../SKILL.md)

# E2E Validation Findings Report

**Validation ID**: ADR-XXXX
**Branch**: feat/your-feature-branch
**Date**: YYYY-MM-DD
**Target Release**: vX.Y.Z
**Status**: [⏳ IN_PROGRESS / ✅ RELEASE_READY / ❌ BLOCKED]

---

## Executive Summary

E2E validation of [feature/refactor name] discovered **N critical bugs** that would have caused [impact summary]:

| Finding        | Severity    | Status     | Impact                  | Agent   |
|----------------|-------------|------------|-------------------------|---------|
| **Bug 1 Name** | 🔴 Critical | ✅ Fixed    | 100% [specific failure] | Agent X |
| **Bug 2 Name** | 🔴 Critical | ✅ Fixed    | Data corruption         | Agent Y |
| **Bug 3 Name** | 🟡 Medium   | ⚠️ Partial | Below SLO performance   | Agent Z |

**Recommendation**: [RELEASE_READY / BLOCKED / DEFERRED]

**Rationale**: [Explain go/no-go decision based on bugs found and fixed]

---

## Agent 1: [Environment Setup] - [✅ PASS / ❌ FAIL]

**Validation**: [Brief description of what this agent validates]

### Results
- ✅ [Success criterion 1]
- ✅ [Success criterion 2]
- ❌ [Failure criterion] (if applicable)

### Artifacts
- `tmp/e2e-validation/agent-1-name/artifact1.log`
- `tmp/e2e-validation/agent-1-name/artifact2.txt`

**Verdict**: [Environment setup fully operational / Issues found]

---

## Agent 2: [Data Flow] - [✅ PASS / ❌ FAIL]

**Validation**: [Brief description of what this agent validates]

### Critical Bugs Found & Fixed

#### Bug 1: [Descriptive Name] (**CRITICAL** - [Status])

**Location**: `src/path/to/file.py:line_number`

**Issue**: [One-sentence description of the problem]

**Evidence**:
```
[Error message, stack trace, or query results demonstrating the bug]
```

**Impact**: [Quantified impact - e.g., "100% ingestion failure", "Data corruption affecting X% of records"]

**Root Cause**: [Technical explanation of why this happened]

**Fix Applied**:
```python
# BROKEN (before fix)
old_code_here()

# FIXED (after fix)
new_code_here()
```

**Verification**:
```
[Test results showing the fix works]
Test: [Test name]
Expected: [Expected outcome]
Actual: [Actual outcome] ✅
```

**Status**: [✅ FIXED / ⚠️ PARTIAL / ❌ OPEN]

---

#### Bug 2: [Descriptive Name] (**MEDIUM** - [Status])

[Same structure as Bug 1]

---

### Test Results Summary

| Test               | Result     | Details                                |
|--------------------|------------|----------------------------------------|
| **Test 1**: [Name] | ✅ PASS     | [Brief description of results]         |
| **Test 2**: [Name] | ❌ FAIL     | [Brief description of failure]         |
| **Test 3**: [Name] | ⚠️ PARTIAL | [Brief description of partial success] |

**Overall**: X/Y PASS, Z/Y FAIL (M blockers)

---

## Agent 3: [Query Interface] - [✅ PASS / ❌ FAIL]

**Validation**: [Brief description of what this agent validates]

### Test Results

| Test                      | Result     | Details                               |
|---------------------------|------------|---------------------------------------|
| **Test 1**: [Method name] | ✅ PASS     | [Brief results]                       |
| **Test 2**: [Method name] | ✅ PASS     | [Brief results]                       |
| **Test 3**: [Method name] | ⚠️ PARTIAL | [Brief results - explain why partial] |

**Critical Discovery**: [Any new bugs found, or confirmation that interfaces work]

**Verdict**: [Query interface functional / Issues found]

---

## Validation Logs

### Agent 1 Logs
See: `tmp/e2e-validation/agent-1-name/test_output.log`

### Agent 2 Logs
See: `tmp/e2e-validation/agent-2-name/test_output.log`

### Agent 3 Logs
See: `tmp/e2e-validation/agent-3-name/test_output.log`

---

## Release Decision Matrix

**Critical Bugs**: X found, Y fixed, Z open
**Medium Bugs**: A found, B fixed, C open
**Low Bugs**: D found, E fixed, F open

**Decision Criteria**:
```
BLOCKER = Any Critical bug unfixed
SHIP = All Critical bugs fixed + (Medium bugs acceptable OR fixed)
DEFER = >3 Medium bugs unfixed OR any High-severity bug
```

**Status**: [✅ RELEASE_READY / ❌ BLOCKED / ⏸️ DEFERRED]

**Next Steps**:
1. [Action item 1]
2. [Action item 2]
3. [Action item 3]

---

## Appendix: Full Test Outputs

[Optional: Include full test outputs if needed for detailed analysis]

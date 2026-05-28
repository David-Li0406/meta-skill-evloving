**Skill**: [Multi-Agent E2E Validation](../SKILL.md)

# Bug Severity Classification

## Severity Levels

### 🔴 Critical
**Definition**: Bugs that cause 100% system failure or complete data corruption

**Criteria**:
- System cannot start or deploy
- 100% of operations fail
- Complete data loss or corruption
- Security vulnerability allowing unauthorized access
- API incompatibility preventing all usage

**Examples**:
- Using non-existent API method (`Sender.from_uri()` doesn't exist)
- All timestamps defaulting to epoch 0 (100% data corruption)
- Type mismatch causing broken pipe (FLOAT→LONG cast failure)
- SQL syntax incompatibility (nested window functions crash)
- Schema application failure preventing database initialization

**Go/No-Go Impact**: **BLOCKER** - Cannot ship with any unfixed Critical bugs

**Time to Fix**: Immediate (must fix before release)

---

### 🟡 Medium
**Definition**: Bugs that cause degraded functionality or below-SLO performance

**Criteria**:
- System works but performs significantly below SLO (>30% deviation)
- Partial feature failure (some cases work, some don't)
- Non-critical data quality issues
- Degraded user experience but system usable
- Workarounds available but not ideal

**Examples**:
- Performance 55% below SLO target (47K vs 100K rows/sec)
- Query works but 30% slower than expected
- Gap detection works but misses edge cases
- Partial test failures due to data quality (not code bugs)
- Deduplication requires manual intervention

**Go/No-Go Impact**: **CONDITIONAL** - Can ship if ≤3 Medium bugs OR explicitly accepted

**Time to Fix**: Before next minor version (unless explicitly deferred)

---

### 🟢 Low
**Definition**: Minor issues, edge cases, or cosmetic problems

**Criteria**:
- Rare edge cases that don't affect normal operation
- Cosmetic issues (formatting, logging)
- Non-essential features with minor bugs
- Documentation gaps or typos
- Minor performance variations (<10% deviation)

**Examples**:
- Error message formatting inconsistent
- Debug logging too verbose
- Edge case timezone handling issue
- Non-critical validation missing
- Minor test flakiness

**Go/No-Go Impact**: **NON-BLOCKING** - Track for future release

**Time to Fix**: Next patch or minor version

---

## Classification Decision Tree

```
Does the bug prevent system startup or deployment?
├─ YES → 🔴 Critical
└─ NO → Continue

Does the bug cause 100% failure of a core feature?
├─ YES → 🔴 Critical
└─ NO → Continue

Does the bug cause complete data corruption?
├─ YES → 🔴 Critical
└─ NO → Continue

Does the bug cause >30% performance degradation below SLO?
├─ YES → 🟡 Medium
└─ NO → Continue

Does the bug affect normal user workflows?
├─ YES → 🟡 Medium
└─ NO → Continue

Does the bug only affect rare edge cases or cosmetics?
├─ YES → 🟢 Low
└─ NO → Re-evaluate (might be Medium)
```

---

## Real-World Examples from QuestDB Refactor

### 🔴 Critical Bug: Sender API Mismatch
**Impact**: 100% ingestion failure - system completely non-functional
**Evidence**: `AttributeError: type object 'Sender' has no attribute 'from_uri'`
**Why Critical**: Zero functionality - cannot ingest any data
**Fix Priority**: Immediate blocker

### 🔴 Critical Bug: Timestamp Parsing
**Impact**: 100% data corruption - all timestamps at epoch 0 (1970-01-01)
**Evidence**: Database query shows 70,784 rows in 1970-01 instead of 2024-01
**Why Critical**: Data completely unusable for time-series analysis
**Fix Priority**: Immediate blocker

### 🔴 Critical Bug: Deduplication Design Flaw
**Impact**: Zero-gap guarantee violated - duplicates created on re-ingestion
**Evidence**: 44,640 duplicate rows created (expected 0)
**Why Critical**: Core correctness SLO violated
**Fix Priority**: Immediate blocker

### 🟡 Medium Bug: Performance Below SLO
**Impact**: 47K rows/sec achieved vs 100K target (53% below SLO)
**Evidence**: Benchmark shows consistent 47K rows/sec across multiple runs
**Why Medium**: System works, but slower than designed
**Fix Priority**: Deferred (acceptable for v4.0.0, address in v4.1.0)

### 🟢 Low Bug: Test Timezone Comparison
**Impact**: Test fails with tz-naive vs tz-aware comparison
**Evidence**: TypeError in test code (not production code)
**Why Low**: Affects test only, not production functionality
**Fix Priority**: Fix during test development

---

## Severity Assessment Checklist

When triaging a new bug, ask:

- [ ] Can the system start/deploy? (No → Critical)
- [ ] Does any core feature work? (No → Critical)
- [ ] Is data integrity compromised? (Yes → Critical)
- [ ] Can users accomplish their goals? (No → Critical, Partially → Medium)
- [ ] Is performance >30% below SLO? (Yes → Medium)
- [ ] Is there a reasonable workaround? (No → increase severity)
- [ ] Does this affect production code? (No → Low)
- [ ] Is this an edge case? (Yes → Low)

---

## Dispute Resolution

If severity classification is unclear:

1. **Default to Higher Severity**: When in doubt, escalate (Low→Medium, Medium→Critical)
2. **Get Second Opinion**: Ask another engineer or team lead
3. **Run Go/No-Go Test**: If unsure whether to ship, assume Critical and investigate
4. **Document Rationale**: Explain why a bug was downgraded (e.g., "Downgraded to Medium because workaround exists")

Example dispute:
- **Initial Classification**: 🔴 Critical (performance 55% below SLO)
- **Disputed Classification**: 🟡 Medium (system works, just slower)
- **Resolution**: 🟡 Medium + explicit go/no-go decision documented
- **Rationale**: "System functional, deduplication fixed restores correctness SLO, performance can be addressed in v4.1.0"

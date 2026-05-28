---
name: validate-requirements
description: Validate requirements quality - unique keys, acceptance criteria, testability, clarity. Sensor detecting requirement quality issues. Use before moving to Design stage or as quality gate.
allowed-tools: [Read, Grep, Glob]
---

# validate-requirements

**Skill Type**: Sensor (Quality Gate)
**Purpose**: Validate requirement quality and completeness
**Prerequisites**: Requirements exist in documentation

---

## Agent Instructions

You are validating **requirement quality** as a quality gate.

**Validation checks**:
1. Unique REQ-* keys (no duplicates)
2. Valid key format (matches pattern)
3. Acceptance criteria present
4. Testable format (can write tests)
5. Traceability to intent
6. No ambiguous language

---

## Validation Checks

### Check 1: Unique Keys

**Rule**: All REQ-* keys must be unique

```bash
# Find duplicates
grep -rho "^## REQ-[A-Z-]*-[0-9]*" docs/requirements/ | sort | uniq -d
```

**Example**:
```
✅ Pass: All REQ-* keys unique
❌ Fail: <REQ-ID> appears in 2 files
```

---

### Check 2: Valid Key Format

**Rule**: All keys must match REQ-* pattern

```bash
# Check format
grep -rh "^## REQ-" docs/requirements/ | grep -vE "^## REQ-(F|NFR|DATA|BR)-[A-Z]{2,10}-[0-9]{3}"
```

---

### Check 3: Acceptance Criteria

**Rule**: All requirements must have acceptance criteria

```bash
# Find requirements without AC
grep -rn "^## REQ-" docs/requirements/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  # Check if AC section exists after requirement
  grep -A 20 "$line" "$file" | grep -q "Acceptance Criteria" || echo "Missing AC: $line"
done
```

---

### Check 4: Testability

**Rule**: Acceptance criteria must be testable

**❌ Not Testable**:
```
Acceptance Criteria:
- System should be user-friendly
- Performance should be good
```

**✅ Testable**:
```
Acceptance Criteria:
- Login response time < 500ms (p95)
- User sees "Welcome" message after successful login
```

---

### Check 5: Traceability

**Rule**: All REQ-* must link to INT-*

```bash
# Find requirements without intent link
grep -rn "^## REQ-" docs/requirements/ | while read line; do
  file=$(echo "$line" | cut -d: -f1)
  grep -A 10 "$line" "$file" | grep -q "Intent: INT-" || echo "Missing Intent: $line"
done
```

---

### Check 6: Ambiguous Language

**Detect vague terms**:
- "user-friendly", "fast", "good", "better", "nice"
- "should", "might", "possibly"
- "etc.", "and so on"

**Replace with**:
- Specific measurements ("response time < 500ms")
- Clear criteria ("user sees confirmation message")
- Complete lists (no "etc.")

---

## Output Format

```
[VALIDATE REQUIREMENTS]

Total Requirements Scanned: 42

✅ PASSED Checks (5/6):
  ✓ Unique keys: All REQ-* unique
  ✓ Valid format: All keys match pattern
  ✓ Acceptance criteria: All requirements have AC
  ✓ Traceability: All link to INT-*
  ✓ Testability: All AC measurable

❌ FAILED Checks (1/6):
  ✗ Ambiguous language: 3 requirements contain vague terms

Issues Found:

Ambiguous Language (3 requirements):
  1. REQ-F-PORTAL-001:
     - Line 45: "User interface should be user-friendly"
     - Fix: Replace with "User can complete task in ≤3 clicks"

  2. REQ-NFR-PERF-002:
     - Line 23: "Database performance should be good"
     - Fix: Replace with "Database queries complete in <100ms (p95)"

  3. REQ-F-NOTIF-001:
     - Line 67: "Notifications should be sent quickly"
     - Fix: Replace with "Notifications sent within 5 seconds"

Recommendations:
  1. Fix 3 requirements with ambiguous language
  2. Re-run validation after fixes
  3. Proceed to Design stage after all checks pass

Validation Status: ⚠️ FAILED (6 issues)
Quality Gate: ❌ BLOCKED (fix issues before proceeding)
```

---

## Quality Gate Behavior

**If validation passes**:
```
✅ All Requirements Valid

Quality gate: PASS
Ready for: Design stage
```

**If validation fails**:
```
❌ Validation Failed (6 issues)

Quality gate: BLOCKED
Action required: Fix issues before Design stage
Recommendation: Update requirements and re-validate
```

---

## Notes

**Why validate requirements?**
- **Quality gate**: Ensure requirements are implementation-ready
- **Prevent rework**: Catch issues before coding starts
- **Compliance**: Regulations require traceable, testable requirements
- **Clear specs**: Ambiguous requirements → ambiguous code

**Homeostasis Goal**:
```yaml
desired_state:
  all_requirements_valid: true
  quality_issues: 0
  ready_for_design_stage: true
```

**"Excellence or nothing"** 🔥

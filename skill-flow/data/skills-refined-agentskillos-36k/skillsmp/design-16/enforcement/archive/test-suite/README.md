# Validator Test Suite

This directory contains test specs to validate that `validator.sh` correctly enforces all 43 invariants.

## Quick Start

```bash
# Run all tests
./run-tests.sh

# Run validator on a single spec
../validator.sh bad-spec-universal.md

# Run with domain-specific invariants
../validator.sh bad-spec-construction.md --domain ../../domains/physical-construction.md
```

## Test Files

### bad-spec-universal.md
**Purpose**: Violates ALL 10 universal invariants (1-10)
**Expected Result**: Exit code 1, ≥10 violations (spec triggers additional due to realistic content)

Contains deliberate violations of:
| # | Invariant | Violation |
|---|-----------|-----------|
| 1 | Ambiguity is Invalid | "properly", "efficiently", "intuitive" |
| 2 | State Must Be Explicit | "update preferences" without → |
| 3 | Emotional Intent Must Compile | "feel confident" without := |
| 4 | No Irreversible Without Recovery | "delete", "purge" without recovery |
| 5 | Execution Must Fail Loudly | "gracefully", "silently" |
| 6 | Scope Must Be Bounded | "all", "everything", "entire" |
| 7 | Validation Must Be Executable | "ensure quality", "verify looks right" |
| 8 | Cost Boundaries Must Be Explicit | API calls without limits |
| 9 | Blast Radius Must Be Declared | Database changes without scope |
| 10 | Degradation Path Must Exist | External APIs without fallbacks |

---

### good-spec-universal.md
**Purpose**: Passes ALL universal invariants correctly
**Expected Result**: Exit code 0, 0 violations, 0 warnings

Shows correct patterns for each invariant:
- Ambiguity → Operational definitions with metrics
- State → before → action → after transitions
- Emotion → := concrete mechanisms
- Destructive → recovery + time windows
- Errors → detection + alerting + blocking
- Scope → max/limit/pagination
- Validation → metric + threshold + method
- Cost → limits + budgets + circuit breakers
- Blast radius → affects + dependencies
- Degradation → primary → fallback1 → fallback2

---

### bad-spec-capability.md
**Purpose**: Violates skill gap transcendence invariants (37-43) plus universal invariants
**Expected Result**: Exit code 1, ≥5 violations (triggers both universal and domain invariants)
**Domain**: `--domain ../../domains/skill-gap-transcendence.md`

This realistic spec triggers:
- Universal invariants (3: "should" without :=, 6: "all" without bounds)
- Domain-specific skill gap checks (37, 39, 41)

---

### bad-spec-consumer.md
**Purpose**: Violates consumer product invariants (11-15) plus universal invariants
**Expected Result**: Exit code 1, ≥5 violations, ≥3 warnings
**Domain**: `--domain ../../domains/consumer-product.md`

This realistic spec triggers:
- Universal violations (3: "should" without :=)
- Consumer domain warnings (11-15: emotion, friction, accessibility, offline, loading)

---

### bad-spec-construction.md
**Purpose**: Violates physical construction invariants (16-21) plus universal invariants
**Expected Result**: Exit code 1, ≥5 violations, ≥1 warning
**Domain**: `--domain ../../domains/physical-construction.md`

This realistic spec triggers:
- Universal violations (1: "good quality", 3: "should be solid", 6: "all aspects")
- Construction domain warnings (16-21: materials, vendors, climate, inspections)

---

## How run-tests.sh Works

1. Runs `validator.sh` on each test spec
2. Captures exit code, violation count, and warning count
3. Compares against expected values
4. Reports PASS/FAIL for each test
5. Exits with 0 if all pass, 1 if any fail

### Test Function Signature
```bash
run_test \
    "Test name" \
    "path/to/spec.md" \
    "--domain path/to/domain.md"  # optional, empty string if none
    expected_exit_code \
    expected_violations \
    expected_warnings
```

---

## Adding New Tests

### 1. Create the test spec
```bash
# Create a new test spec
touch test-suite/bad-spec-newdomain.md
```

### 2. Add violations/correct patterns
```markdown
<!-- VIOLATES INVARIANT X: Name -->
Text that violates the invariant...

<!-- PASSES INVARIANT X: Name -->
Text that passes the invariant with proper format...
```

### 3. Add test to run-tests.sh
```bash
run_test \
    "bad-spec-newdomain.md (description)" \
    "$SCRIPT_DIR/bad-spec-newdomain.md" \
    "--domain $DOMAINS_DIR/newdomain.md" \
    1 \    # expected exit code (1 for violations, 0 for warnings only)
    5 \    # expected number of violations
    3      # expected number of warnings
```

### 4. Run and verify
```bash
./run-tests.sh
```

---

## Debugging Failed Tests

If a test fails:

1. **Check the output**: The test runner shows truncated validator output
2. **Run manually**: `../validator.sh bad-spec-xxx.md --domain ...`
3. **Review patterns**: Some words trigger multiple invariants
4. **Check detection logic**: Review `validator.sh` grep patterns

### Common Issues

**Too many/few violations?**
- Check if your text accidentally triggers other invariants
- Some words like "update" or "all" are checked by multiple rules

**Domain not loading?**
- Verify domain file path is correct
- Check domain file name matches pattern in validator.sh

**False positives?**
- The validator uses simple grep patterns
- Comments and code blocks are not fully excluded
- May need to adjust patterns in validator.sh

---

## Coverage Matrix

| Invariant | Test File | Type | Status |
|-----------|-----------|------|--------|
| 1-10 | bad-spec-universal.md | Violation | ✅ Tested |
| 1-10 | good-spec-universal.md | Pass | ✅ Tested |
| 11-15 | bad-spec-consumer.md | Warning + Universal Violations | ✅ Tested |
| 16-21 | bad-spec-construction.md | Warning + Universal Violations | ✅ Tested |
| 22-26 | (not yet created) | Data Architecture | TODO |
| 27-30 | (not yet created) | Integration | TODO |
| 31-36 | (not yet created) | Remote Management | TODO |
| 37-43 | bad-spec-capability.md | Violation + Universal | ✅ Tested |

### Key Insight: Universal Invariants Always Apply
Realistic specs will trigger both domain-specific AND universal invariants. This is correct behavior - a good spec must pass ALL applicable invariants.

### Future Test Files
- `bad-spec-data.md` - Data architecture domain (22-26)
- `bad-spec-integration.md` - Integration domain (27-30)
- `bad-spec-remote.md` - Remote management domain (31-36)
- `good-spec-*.md` - Passing specs for each domain

---

## CI Integration

Add to your CI pipeline:

```yaml
# .github/workflows/validate.yml
- name: Run validator tests
  run: |
    cd DesignOps/enforcement/test-suite  # Adjust path based on your repo structure
    chmod +x run-tests.sh
    ./run-tests.sh
```

---

*Last updated: 2026-01-20*

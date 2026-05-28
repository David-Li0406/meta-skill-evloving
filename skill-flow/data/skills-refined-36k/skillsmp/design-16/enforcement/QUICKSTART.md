# Invariant Validator Quickstart

Get productive in 5 minutes. Catches spec problems before they become execution disasters.

## 1. Installation

```bash
cd /path/to/DesignOps/enforcement
chmod +x validator.sh
```

## 2. Basic Usage

```bash
./validator.sh my-spec.md                                      # Core invariants only
./validator.sh spec.md --domain ../domains/physical-construction.md  # With domain rules
```

**Example output (violation):**
```
❌ VIOLATION: Invariant #1 (Ambiguity is Invalid)
   Line 23: "The system should process data properly"
   → Fix: Replace 'properly' with objective criteria: metric + threshold + measurement
```

**Example output (success):**
```
✅ All invariants validated
✅ Spec ready for PRP compilation
```

## 3. Try It Now

```bash
# Create a bad spec
echo "Process data properly and ensure quality is good" > test.md
./validator.sh test.md
# Output: ❌ VIOLATION: Invariant #1 (Ambiguity is Invalid)

# Fix it
echo "Data processing := validate_schema + reject_invalid + log_errors" > test.md
./validator.sh test.md
# Output: ✅ All invariants validated

rm test.md
```

## 4. Common Violations and Fixes

### #1: Ambiguity (Words Without Metrics)

| Bad | Good |
|-----|------|
| `Process data properly` | `Data processing := validate_schema + reject_invalid + log_errors` |
| `User-friendly interface` | `User-friendly := max_3_clicks + response_time < 200ms` |

### #2: State Changes Without Before/After

| Bad | Good |
|-----|------|
| `Update preferences in database` | `preferences = {light} → set_theme(dark) → preferences = {dark}` |

### #3: Emotions Without Mechanisms

| Bad | Good |
|-----|------|
| `Users should feel confident` | `confident := show_success_rate(≥95%) + undo_option(5min)` |

### #4: Destructive Actions Without Recovery

| Bad | Good |
|-----|------|
| `Delete all user data` | `soft_delete(30d_retention) → backup → hard_delete_after_30d` |

### #5: Silent Failures

| Bad | Good |
|-----|------|
| `Handle error gracefully` | `error → block_execution + alert_slack + require_human_decision` |

## 5. How to Add Domain Files

Create `domains/payments.md`:

```markdown
# Payments Domain Invariants

## Domain Invariants

### P1. Transactions Must Be Idempotent
Every charge needs unique idempotency key. Retries must not duplicate charges.

### P2. Amounts Must Have Currency
No raw numbers for money. Bad: 100. Good: 100 USD.
```

Use it:
```bash
./validator.sh checkout.md --domain domains/payments.md
```

## 6. Integration with Workflow

```
Research ──► Journeys ──► Specs ──► [VALIDATOR] ──► PRP ──► Execution
                                        │
                                   ┌────┴────┐
                                   │         │
                                ❌ FAIL   ✅ PASS
                                   │         │
                               Fix spec   Continue
```

**The rule:** No spec becomes a PRP until it passes validation.

## 7. Troubleshooting

**Q: Permission denied**
```bash
chmod +x validator.sh
```

**Q: Spec file not found**
```bash
./validator.sh /full/path/to/spec.md  # Use absolute paths
```

**Q: False positive on "properly configured"**
```markdown
# Add explicit definition to avoid trigger:
Properly configured := port_443_open + SSL_cert_valid + healthcheck_passing
```

**Q: Skip validation for a section?**
```markdown
<!-- Comments are ignored by the validator -->
```

**Q: Validator passes but spec seems vague?**

The validator catches common patterns, not everything. If it feels vague, make it concrete. The invariants are a floor, not a ceiling.

## Quick Reference

| Flag | Purpose |
|------|---------|
| `--domain <file>` | Add domain-specific rules |
| `--help` | Show usage |
| `--version` | Show version |

| Exit Code | Meaning |
|-----------|---------|
| 0 | Pass (or warnings only) |
| 1 | Violations found - rejected |

```bash
./validator.sh spec.md || echo "Validation failed"  # CI/CD usage
```

---

*Time to first validation: ~2 minutes*

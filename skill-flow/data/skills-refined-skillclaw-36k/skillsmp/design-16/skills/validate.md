---
name: design-validate
description: Validate specs against system invariants. USE WHEN validate spec, check invariants, spec validation.
context: fork
---

# Design Validate

Validates a specification against system invariants before PRP compilation. Runs in isolated context to avoid polluting the main conversation with invariant checking details.

## Why Forked Context

- Invariant validation is self-contained — doesn't need conversation history
- Validation output can be verbose (10+ invariant checks with details)
- Keeps main context clean for follow-up discussion

## Usage

```
/design-validate docs/design/specs/feature-spec.md
/design-validate specs/mobile-app.md --domain consumer-product
/design-validate specs/house-foundation.md --domain physical-construction --domain remote-management
```

## Execution

1. **Load invariants:**
   - Read `system-invariants.md` for universal rules (1-10)
   - Load domain-specific invariants if `--domain` specified

2. **Run validator:**
   ```bash
   ./enforcement/validator.sh "{spec-file}" [--domain "{domain-file}"]
   ```

3. **Parse and report:**
   - PASS: Spec ready for PRP compilation
   - FAIL: List violations with line numbers and fix suggestions

## Output Format

**On PASS:**
```
Validating: specs/my-feature.md

Checking Universal Invariants...
  [1] Ambiguity is Invalid........... PASS
  [2] State Must Be Explicit......... PASS
  ...
  [10] Degradation Path Exists....... PASS

Violations: 0
Warnings: 0

PASS - Spec ready for PRP compilation
Run: /design prp specs/my-feature.md
```

**On FAIL:**
```
VIOLATION: Invariant #1 (Ambiguity is Invalid)
  Line 23: "Process data properly"
  Fix: Replace 'properly' with objective criteria: metric + threshold + measurement

REJECTED - Fix violations before proceeding
```

## Related Commands

- `/design prp` — Generate PRP after validation passes
- `/design orchestrate` — Full pipeline including validation

---

*Forked skill — returns summary to main context*

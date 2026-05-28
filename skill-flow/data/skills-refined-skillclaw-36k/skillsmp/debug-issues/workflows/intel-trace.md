# Phase 3: Intel Trace

**Purpose**: Systematic 4-query workflow to trace from error to root cause using project-intel.mjs.

---

## Query 1: Locate Function

Find the file containing the function mentioned in the error:

```bash
project-intel.mjs --search "calculateTotal" --type ts --json > /tmp/debug_search.json
```

**Result:**
```json
{
  "files": [
    "src/pricing/calculator.ts",
    "src/pricing/calculator.test.ts"
  ]
}
```

**Purpose**: Identify which file(s) contain the relevant code.

---

## Query 2: Analyze Symbols

Get symbols from the identified file to find exact line numbers:

```bash
project-intel.mjs --symbols src/pricing/calculator.ts --json > /tmp/debug_symbols.json
```

**Result:**
```json
{
  "symbols": [
    {"name": "calculateTotal", "line": 62, "type": "function"},
    {"name": "applyDiscount", "line": 89, "type": "function"},
    {"name": "getDiscount", "line": 105, "type": "function"}
  ]
}
```

**Key Finding:** calculateTotal is at line 62, error at line 67 (5 lines into function)

**Purpose**: Pinpoint exact function location and understand what line the error is on.

---

## Query 3: Trace Dependencies

Check what the error-causing function imports:

```bash
# What does calculateTotal import?
project-intel.mjs --dependencies src/pricing/calculator.ts --direction upstream --json
```

**Result:**
```json
{
  "imports": [
    {"module": "./discountService", "symbols": ["getDiscount"]},
    {"module": "../models/Cart", "symbols": ["Cart"]},
    {"module": "../utils/currency", "symbols": ["formatPrice"]}
  ]
}
```

**Key Finding:** Imports getDiscount from discountService - likely source of undefined

**Purpose**: Identify external dependencies that may be causing the issue.

---

## Query 4: Check Dependency Function

Analyze the suspicious dependency to understand its behavior:

```bash
project-intel.mjs --symbols src/pricing/discountService.ts --json
```

**Result:**
```json
{
  "symbols": [
    {"name": "getDiscount", "line": 12, "type": "function", "returns": "Discount | undefined"}
  ]
}
```

**CRITICAL FINDING:** getDiscount returns `Discount | undefined` - can be undefined!

**Purpose**: Confirm the dependency can return values that cause the error.

---

## Enforcement Checklist

Before proceeding to Phase 4, verify:

- [ ] All relevant files identified via Query 1
- [ ] Symbol locations found via Query 2
- [ ] Dependencies traced via Query 3
- [ ] Return types checked via Query 4
- [ ] Critical findings documented with evidence

**Next Step**: Proceed to Phase 4 (Root Cause Analysis) with targeted file reads.

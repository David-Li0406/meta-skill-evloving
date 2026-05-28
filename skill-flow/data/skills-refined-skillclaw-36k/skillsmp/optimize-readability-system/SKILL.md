---
name: optimize-readability-system
description: "Interactive guide for tuning the unmangleJS Readability Scoring System(readability.ts) and Semantic Scoring System (semantic.ts). Use when Golden Set validation fails, when scoring heuristics need adjustment, or when improving obfuscation detection accuracy. Emphasizes experiment-driven development: run tests, analyze data, draw conclusions - never guess blindly."
---

# Optimize Readability/Semantic Scoring System

Interactive guide for tuning the unmangleJS scoring systems.

## Core Philosophy

> **"Do experiments, get data, draw conclusions. Don't guess blindly."**

This is the golden rule for all optimization work.

---

## System Overview

### 1. Semantic Scoring (`src/utils/semantic.ts`)

Analyzes names and structures for semantic meaning.

**Key Functions:**
- `scoreKeySemantic(key)` - Score a single identifier (0-2.5 average)
- `getSemanticThreshold(keyLength)` - Get length-based threshold (1.0-1.5)
- `isObjectSemantic()` / `isSubjectSemantic()` - Judge semantic content

### 2. Readability Scoring (`src/utils/readability.ts`)

Decides whether to simplify AST subtrees.

**7 Signals:**
- `semantic-*` (5 signals, veto: true) - Protect semantic content
- `cognitive-density` - Cognitive load (0-1)
- `linearity-violation` - Linearity (0-1)

**Decision Rules:**
1. Semantic Veto - One-vote veto power
2. Dual Confirmation - cognitive < 0.4 AND linearity < 0.4
3. Average Fallback - threshold: 0.5

### 3. Golden Set (`tests/readability/golden/`)

Constitutional test suite defining system values.

- `should-simplify.json` - Obfuscated samples (must simplify)
- `should-not-simplify.json` - Semantic samples (must preserve)
- Success metric: 100% pass rate (excluding `undecided`)

---

## When to Use This Skill

**Scenario A: Golden Set Already Failing**
```
Current state: Golden Set validation fails
Action: Use this skill directly to diagnose and fix
```

**Scenario B: Adding New Samples**
```
Current state: Golden Set passes, but found edge case
Action: Follow "Adding New Samples" flow below
```

**Scenario C: New Sample Causes Failure**
```
Current state: Golden Set passes → Add sample → Fails
Action: Use this skill starting from Step 2 (Analyze Failures)
```

---

## Optimization Workflow

### Step 1: Run Golden Set

```bash
npm test -- tests/readability/golden.test.ts
```

**Expected:** 50/50 passed (100%)

**If failing → Continue to Step 2**

### Step 2: Analyze Failures

Use professional analysis tools (DO NOT write temporary scripts):

#### Tool 1: readability-analyzer.js

**Purpose:** Analyze code and output detailed readability scoring reports

**Usage:**
```bash
# Build first
npm run build

# Analyze a file
node tools/readability-analyzer.js <file>

# From stdin
echo 'const x = { a: 1 };' | node tools/readability-analyzer.js

# NEW: Filter by node type
node tools/readability-analyzer.js <file> --types SequenceExpression
node tools/readability-analyzer.js <file> -t seq,obj,cond  # Multiple types
node tools/readability-analyzer.js --list-types  # Show available types
```

**Output:**
- Part 1: Decision Summary (should simplify? yes/no, threshold check)
- Part 2: All Signals (cognitive-density, linearity-violation, semantic-*)
- Part 3: Veto Check (which signal triggered veto)
- Part 4: Decision Logic (which rules passed/failed)

**When to use:**
- Any Golden Set test failure
- Debugging `shouldSimplify()` behavior
- Understanding why veto was triggered

#### Tool 2: semantic-analyzer.js

**Purpose:** Analyze semantic structures (Object, Array, Function, Variable)

**Usage:**
```bash
npm run build
node tools/semantic-analyzer.js <file>
echo 'const obj = { a: 1 };' | node tools/semantic-analyzer.js

# NEW: Filter by node type
node tools/semantic-analyzer.js <file> --types ObjectExpression
node tools/semantic-analyzer.js <file> -t obj,arr,var  # Multiple types
node tools/semantic-analyzer.js --list-types  # Show available types
```

**Supported Node Types:**
- ObjectExpression - 4-part analysis
- ArrayExpression - 2-part analysis
- Function (Declaration/Expression/Arrow) - 2-part analysis
- VariableDeclarator - 2-part analysis (simple + destructuring)

**When to use:**
- Object/array/function/variable semantic analysis
- Debugging `isSubjectSemantic()` behavior
- Checking individual scores with dynamic thresholds

### Step 3: Answer Key Questions

For each failing sample:

1. Which signals are causing the wrong decision?
2. Are semantic signals vetoing correctly?
3. Is cognitive/linearity score appropriate?
4. For semantic nodes: Are individual name scores correct?

### Step 4: Form Hypothesis

Based on data, form a specific hypothesis.

**Examples:**
- "Short obfuscated names score too high because entropy threshold is too lenient"
- "Object linearity scores (0.9) prevent deletion, should be 0.3"

### Step 5: Test with CLI

**CRITICAL:** Always test with real CLI behavior.

```bash
# Test obfuscated pattern
cat > tmp/test.js << 'EOF'
const _0x1 = { UoAwJ: "x", YXLlx: "y" };
EOF
./bin/unmanglejs.js tmp/test.js -p
# Expected: Object should be inlined

# Test semantic pattern
cat > tmp/test2.js << 'EOF'
const config = { UNKNOWN: 0, OK: 1 };
EOF
./bin/unmanglejs.js tmp/test2.js -p
# Expected: Object should be preserved
```

**Interpret Results:**
- Obfuscated code NOT transformed → False negative (too conservative)
- Semantic code IS transformed → False positive (too aggressive)

### Step 6: Apply Minimal Fix

Change one thing at a time. Validate after each change.

**Example fixes:**

```typescript
// Fix 1: Adjust entropy threshold
let threshold: number;
if (key.length <= 4) threshold = 2.5;  // Very strict
else if (key.length <= 6) threshold = 3.0;  // Strict
else threshold = 3.5;  // Normal

// Fix 2: Add semantic shield check
if (t.isCallExpression(expr) && t.isIdentifier(expr.callee)) {
  const score = scoreKeySemantic(expr.callee.name);
  if (score.average >= 1.5) semanticCount++;
}

// Fix 3: Add obfuscation penalty
if (metrics.semanticRatio < 0.3 && metrics.distinctIdentifiers >= 2) {
  score -= 0.3;
}
```

### Step 7: Validate Full Suite

```bash
npm test
# Expected: All tests passing
```

---

## Common Issues

### Issue: Golden Set < 100% Pass Rate

**Diagnosis:**
1. Run tools on failing samples
2. Categorize: too conservative OR too aggressive
3. Identify root cause

**Common Fixes:**
- Too conservative → Raise threshold, add penalties
- Too aggressive → Lower threshold, strengthen veto

### Issue: Semantic Names Not Protected

**Symptom:** `if(initialize(), validate())` gets flattened

**Root Cause:** Semantic shield missing pattern OR names score below threshold

**Fix:** Add missing pattern check (see Step 6 examples)

### Issue: Short Obfuscated Names Score High

**Symptom:** `{ UoAwJ: "x" }` scores 1.25 (semantic!)

**Root Cause:** Short names have naturally low entropy

**Fix:** Use stricter thresholds for short keys (see Step 6 examples)

### Issue: Object Linearity Too High

**Symptom:** Objects score 0.9 linearity, preventing deletion

**Fix:** Object linearity shouldn't affect deletion
```typescript
if (path.isObjectExpression()) {
  return 0.3;  // Low score = "linearity doesn't apply"
}
```

### Issue: Pass Behavior Differs by Context

**Symptom:** `for(a=1, b=2)` behaves differently than `if(a(), b())`

**Explanation:** Some passes don't extract from certain parent contexts by design

**Fix:** Understand pass behavior first, don't assume uniform behavior

---

## Golden Set Management

### Adding New Samples

When you encounter a new edge case:

**Step 1:** Validate current state (100% pass)

**Step 2:** Test new sample with tools
```bash
npm run build
node tools/readability-analyzer.js tmp/new-sample.js
```

**Step 3:** Categorize
- Clearly obfuscated → `should-simplify.json`
- Clearly semantic → `should-not-simplify.json`
- Ambiguous → Mark as `"expected": "undecided"`

**Step 4:** Add to appropriate file
```bash
cat >> tests/readability/golden/should-simplify.json << 'EOF'
{
  "id": "descriptive-id",
  "code": "const x = <obfuscated code>;",
  "expected": true,
  "invariant": false,
  "reason": "obfuscated pattern description"
}
EOF
```

**Step 5:** Validate
```bash
npm test -- tests/readability/golden.test.ts
```

**If tests pass:** Done ✅

**If tests fail:** New sample revealed system defect → Use optimization workflow to fix

### Invariant Levels

- `invariant: true` - System-defining values, should never change
- `invariant: false` - Heuristic cases, can evolve
- `expected: "undecided"` - Ambiguous boundary cases

---

## Best Practices

### 1. Experiment-Driven Development

**ALWAYS:**
1. Run tests first
2. Use professional tools for analysis
3. Identify specific failures
4. Form hypothesis
5. Test with CLI
6. Apply minimal fix
7. Validate all tests

**NEVER:**
- ❌ Guess what the issue might be
- ❌ Tune thresholds without data
- ❌ Write temporary scripts when tools are available
- ❌ Make broad changes for specific failures

### 2. Keep Tools in Sync

When modifying `semantic.ts` or `readability.ts`, update analysis tools:

1. Adding new signals → Update `readability-analyzer.js`
2. Adding new semantic functions → Update `semantic-analyzer.js`
3. Changing thresholds → Update tool output and docs

**Test tools after changes:**
```bash
npm run build
echo 'const x = { a: 1 };' | node tools/semantic-analyzer.js
```

### 3. Minimal Diff Principle

- Change one thing at a time
- Validate after each change
- Keep changelog of what worked

---

## Quick Reference

### Key Files

**Source:**
- `src/utils/semantic.ts` - Semantic scoring
- `src/utils/readability.ts` - Readability decision

**Tests:**
- `tests/readability/golden/*.json` - Golden Set samples
- `tests/readability/golden.test.ts` - Validator

**Tools:**
- `tools/readability-analyzer.js` - Readability analysis
- `tools/semantic-analyzer.js` - Semantic analysis

### Key Constants

```typescript
// readability.ts
const DEFAULT_THRESHOLD = 0.5;
const COGNITIVE_CONFIRM = 0.4;
const LINEARITY_CONFIRM = 0.4;

// semantic.ts - Dynamic thresholds
function getSemanticThreshold(keyLength: number): number {
  if (keyLength <= 3) return 1.0;   // Very short
  if (keyLength <= 5) return 1.25;  // Short
  if (keyLength <= 7) return 1.4;   // Medium
  return 1.5;                       // Standard
}

// semantic.ts - Fixed thresholds
const OBJECT_SEMANTIC_THRESHOLD = 1.4;
```

### Common Commands

```bash
# Build (required before using tools)
npm run build

# Run Golden Set
npm test -- tests/readability/golden.test.ts

# Run all tests
npm test

# Analysis tools
node tools/readability-analyzer.js <file>
node tools/semantic-analyzer.js <file>

# With type filtering
node tools/readability-analyzer.js <file> -t seq,obj
node tools/semantic-analyzer.js <file> -t obj,arr,var

# List available types
node tools/readability-analyzer.js --list-types
node tools/semantic-analyzer.js --list-types
```

### Tool Type Filters

**readability-analyzer:**
- `SequenceExpression` (seq, sequence)
- `ObjectExpression` (obj, object)
- `ConditionalExpression` (cond, conditional)
- `Identifier` (id, identifier)

**semantic-analyzer:**
- `ObjectExpression` (obj, object)
- `ArrayExpression` (arr, array)
- `FunctionDeclaration` (func-decl)
- `FunctionExpression` (func-expr)
- `ArrowFunctionExpression` (arrow)
- `VariableDeclarator` (var, variable)

### Success Metrics

- Golden Set: 50/50 passed (100%)
- All tests: 976/976 passing
- Zero false positives (semantic protected)
- Minimal false negatives (obfuscated caught)

---

## Summary

**Golden Rule:** Do experiments, get data, draw conclusions.

**Key Principles:**
1. Always start with Golden Set validation
2. Use professional tools for analysis
3. Apply minimal, targeted fixes
4. Validate with full test suite
5. Keep tools in sync with implementation

**Remember:**
- The system is heuristic, not a correctness engine
- Golden Set is the constitution
- Veto provides precision, scoring provides recall
- Context matters - test in real scenarios

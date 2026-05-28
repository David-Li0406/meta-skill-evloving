---
name: scicode-fix
description: Analyze and fix "ineffective" subproblems in SciCode benchmark. Classify issues as MAJOR or MINOR, apply minimal fixes to MAJOR issues. Use when "analyze subproblem", "classify issue", "fix benchmark problem", "MAJOR or MINOR", "ineffective problem".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(python:*)
---

# SciCode Subproblem Analysis & Fixing

Analyze "ineffective" subproblems in the SciCode benchmark and classify issues as MAJOR or MINOR.

## The Key Question

> **"Can an LLM with domain expertise still produce correct code despite the issue?"**

| Classification | Answer | Action |
|---------------|--------|--------|
| **MINOR** | Yes, LLM can still solve it | Classify only, no fix needed |
| **MAJOR** | No, impossible to solve correctly | Classify AND apply minimal fix |

## Quick Decision Tree

```
Issue found in subproblem
        │
        ▼
Can code execute at all?
        │
        ├─ NO (TypeError, missing params) ──→ MAJOR
        │
       YES
        ↓
Is the algorithm/method unambiguous?
        │
        ├─ NO (multiple valid methods) ──→ MAJOR
        │
       YES
        ↓
Would different interpretations produce same output?
        │
        ├─ NO (different matrices/values) ──→ MAJOR
        │
       YES
        ↓
Is missing info well-known in the domain?
        │
        ├─ YES (physics constants, standard algorithms) ──→ MINOR
        │
       NO
        ↓
      MAJOR (when in doubt)
```

## Analysis Workflow

### Phase 1: Read All Components

For each subproblem, read:
1. **Subquestion text** - what's being asked
2. **Function header** - parameters and return types
3. **Test cases** - expected behavior
4. **Step background** - scientific context
5. **Expert opinions** - identified issues
6. **Reviewer assessment** - authoritative classification

### Phase 2: Classify

Apply the decision tree to determine MAJOR or MINOR.

### Phase 3: Fix (MAJOR only)

Apply the **Minimal Fix Principle**:

| Bad Approach | Good Approach |
|--------------|---------------|
| Rewrite entire docstring | Just add missing parameter |
| Add detailed explanations | Add one sentence with method name |
| Repeat formulas from background | Reference "as defined in background" |

### Phase 4: Document

Use template from [TEMPLATES.md](TEMPLATES.md).

### Phase 5: Validate Empirically

Write Python code to test your classification:
- MAJOR: Should crash or produce different outputs
- MINOR: Should work with domain knowledge

## Components That Can Be Fixed

| Component | When to Fix | Example |
|-----------|-------------|---------|
| **Subquestion Text** | Add method specification | "Use explicit finite difference method" |
| **Function Header** | Fix signature mismatch | Add missing parameter |
| **Step Background** | Fix formula typos | Correct index in recurrence |
| **Test Cases** | Rarely needed | Usually tests are correct |

## Red Flags for MAJOR

- Function has N parameters but tests call with M arguments (N ≠ M)
- Multiple valid methods exist but none specified
- Background shows Formula A but tests expect Formula B
- Terms used in equations are never defined
- Dependencies reference undefined functions

## Yellow Flags for MINOR

- Typo in physical constant (but value is well-known)
- Variable naming inconsistency (but meaning is clear)
- Missing edge case handling (but core algorithm works)
- Docstring type doesn't match (but either works)

## Analogies for Non-Expert Readers

Use analogies to explain issues to reviewers from other fields:

| Issue Type | Analogy |
|------------|---------|
| Method ambiguity | "Calculate area of shape" without knowing if circle/square/triangle |
| Signature mismatch | Recipe says "add flour" but instructions say "add flour and sugar" |
| Formula typo | GPS coordinates with wrong sign - you end up in wrong hemisphere |

## Reference Files

- [CLASSIFICATION.md](CLASSIFICATION.md) - Detailed examples of MAJOR vs MINOR
- [TEMPLATES.md](TEMPLATES.md) - Analysis document templates

## Project Structure

```
scicode-benchmark/
├── analysis/                    # Your analysis work
│   ├── analysis-XX-X-*.md      # One per subproblem
│   ├── validation_test.py       # Empirical tests
│   └── LESSONS-LEARNED.md       # Learnings document
├── docs/                        # Reference materials
│   ├── SCICODE-PILOT-INSTRUCTIONS.md
│   └── subproblem-XX-X.md       # Original problem specs
└── problems/                    # Raw problem files
```

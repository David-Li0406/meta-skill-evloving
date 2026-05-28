---
name: mutation-test
description: Use this skill when you need to validate test quality beyond code coverage by assessing the effectiveness of your test suite through mutation testing.
---

# Skill body

## Purpose

Run mutation testing to measure test suite effectiveness. Mutation testing introduces small changes (mutants) to code and checks if tests catch them. High coverage with low mutation score indicates weak tests.

## Research Foundation

| Concept | Source | Reference |
|---------|--------|-----------|
| Mutation Testing Theory | IEEE TSE (2019) | Papadakis et al. "Mutation Testing Advances" |
| ICST Mutation Workshop | IEEE Annual | [Mutation 2024](https://conf.researchr.org/home/icst-2024/mutation-2024) |
| Stryker Mutator | Industry Tool | [stryker-mutator.io](https://stryker-mutator.io/) |
| PITest | Java Tool | [pitest.org](https://pitest.org/) |
| mutmut | Python Tool | [github.com/boxed/mutmut](https://github.com/boxed/mutmut) |

## When This Skill Applies

- User asks to "validate test quality" or "check test effectiveness"
- User mentions "mutation testing" or "mutation score"
- User wants to know if tests are "actually testing anything"
- High coverage but bugs still escaping
- Assessing test suite health
- Pre-release quality validation

## Trigger Phrases

| Natural Language | Action |
|------------------|--------|
| "Run mutation testing" | Execute mutation analysis |
| "Check if my tests are effective" | Run mutation + analyze |
| "Validate test quality" | Mutation score report |
| "Are my tests catching real bugs?" | Mutation analysis |
| "Find weak tests" | Identify low-score tests |
| "Why did this bug escape tests?" | Mutation analysis on module |

## Mutation Testing Concepts

### What is a Mutant?

A mutant is a small code change that should cause tests to fail:

```javascript
// Original
if (age >= 18) { return "adult"; }

// Mutant 1: Changed >= to >
if (age > 18) { return "adult"; }

// Mutant 2: Changed >= to ==
if (age == 18) { return "adult"; }

// Mutant 3: Changed "adult" to ""
if (age >= 18) { return ""; }
```

### Mutation Operators

| Operator | Example | Tests |
|----------|---------|-------|
| Arithmetic | `+` → `-` | Math operations |
| Relational | `>=` → `>` | Boundary conditions |
| Logical | `&&` → `\|\|` | Boolean logic |
| Literal | `true` → `false` | Constant handling |
| Return | `return x` → `return null` | Return value handling |

### Mutation Score

```
Mutation Score = (Killed Mutants / Total Mutants) * 100
```
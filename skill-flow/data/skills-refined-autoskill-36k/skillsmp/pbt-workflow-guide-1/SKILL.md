---
name: pbt-workflow-guide
description: Root workflow for introducing, updating, maintaining, and improving Property-Based Testing (PBT) in MoonBit repositories using moonbitlang/quickcheck.
---

# PBT Workflow Guide

## Overview

This skill provides a workflow for introducing, updating, and improving Property-Based Testing (PBT) in MoonBit repositories using `moonbitlang/quickcheck`. Use this guide to:

- Select appropriate PBT patterns based on function characteristics
- Design effective generators with proper distribution control
- Implement custom `Shrink` for complex types
- Write meaningful property-based tests

## Installation

```bash
moon add moonbitlang/quickcheck
moon install
```

Add to your `moon.pkg.json`:

```json
{
  "import": [{ "path": "moonbitlang/quickcheck", "alias": "qc" }]
}
```

## Quick Start

### Writing Your First Property

A property is a function that should hold for all inputs. Use `quick_check_fn` to test it:

```mbt
test "reverse is involutive" {
  @qc.quick_check_fn!(fn(arr : Array[Int]) {
    arr.copy().reverse().reverse() == arr
  })
}
```

Output on success:
```
+++ [100/0/100] Ok, passed!
```

### When Properties Fail

QuickCheck finds counterexamples and **shrinks** them to minimal failing cases:

```
*** [8/0/100] Failed! Falsified.
(0, [0, 0])
```

## Core Traits

### Testable

Types that can be tested. `Bool` implements `Testable`, so most properties return `Bool`.

### Arbitrary

Types that can generate random values. Derive automatically or implement manually:

```mbt
enum Nat {
  Zero
  Succ(Nat)
} derive(Arbitrary, Show)
```

### Shrink

Types that can be simplified to find minimal counterexamples:

```mbt
pub impl Shrink for MyType with shrink(self) -> Iter[MyType] {
  let mut shrunk : Array[MyType] = []
  shrunk.push(MyType::default())  // Try simplest first
  for field_shrunk in self.field.shrink() {
    shrunk.push(MyType::new(field_shrunk, self.other_field))
  }
  shrunk.iter()
}
```

## Pattern Decision Tree

Use this flow to select the appropriate pattern:

```
Q1: What type of function?
│
├─ Transformation (A -> B)
│   └─ Q2: Inverse exists?
│       ├─ YES → Round-Trip
│       └─ NO → Q3: Measurable output properties?
│           ├─ YES → Invariant
│           └─ NO → Q4: Reference implementation exists?
│               ├─ YES → Oracle
│               └─ NO → Producer-Consumer or unit tests
│
├─ Normalization (A -> A)
│   └─ Idempotent
│
└─ Stateful system
    └─ State Machine
```

### Pattern Summary

| Pattern | Use Case | Example |
|---------|----------|---------|
| Round-Trip | Encode/decode pairs | `parse(to_string(x)) == x` |
| Idempotent | Normalization functions | `sort(sort(x)) == sort(x)` |
| Invariant | Collection operations | `map(f, xs).length() == xs.length()` |
| Oracle | Algorithm verification | `my_sort(x) == stdlib_sort(x)` |

## Generator Design

### Distribution Strategy

| Category | Percentage | Purpose |
|----------|------------|---------|
| Normal values | 70% | Typical usage patterns |
| Edge cases | 15% | Empty, zero, single element |
| Boundary values | 15% | Limits, extremes |

### Generator Combinators

| Expression | Purpose |
|------------|---------|
| `@qc.pure(x)` | Always generate x |
| `@qc.one_of([g1, g2])` | Equal probability choice |
| `@qc.frequency([(w1, g1), (w2, g2)])` | Weighted choice |
| `@qc.sized(fn(n) { ... })` | Size-dependent generation |
| `@qc.resize(n, gen)` | Override size parameter |
| `gen.fmap(f)` | Transform generated values |
| `gen.bind(f)` | Chain generators |
| `gen.filter(pred)` | Filter values |

### Example: Custom Distribution

```mbt
fn gen_my_int() -> @qc.Gen[Int] {
  @qc.frequency([
    (70, @qc.Gen::spawn()),  // Normal values
    (15, @qc.one_of([@qc.pure(0), @qc.pure(1), @qc.pure(-1)])),  // Edge cases
    (15, @qc.one_of([@qc.pure(@int.max_value), @qc.pure(@int.min_value)])),  // Boundaries
  ])
}
```

### Recursive Types with `sized`

```mbt
fn gen_tree[T](gen_value : @qc.Gen[T]) -> @qc.Gen[Tree[T]] {
  @qc.sized(fn(size) {
    if size <= 0 {
      gen_value.fmap(Leaf)
    } else {
      @qc.frequency([
        (1, gen_value.fmap(Leaf)),
        (3, @qc.resize(size / 2, gen_tree(gen_value)).bind(fn(left) {
          @qc.resize(size / 2, gen_tree(gen_value)).fmap(fn(right) {
            Node(left, right)
          })
        })),
      ])
    }
  })
}
```

## Using `forall` for Custom Generators

Use `forall` for explicit quantification with custom generators:

```mbt
test "custom generator" {
  @qc.quick_check!(
    @qc.forall(@qc.Gen::spawn(), fn(x : List[Int]) {
      x.rev().rev() == x
    })
  )
}
```

Nested `forall` with dependent generators:

```mbt
test "element from array" {
  @qc.quick_check!(
    @qc.forall(@qc.Gen::spawn(), fn(arr : Array[Int]) {
      @qc.forall(@qc.one_of_array(arr), fn(elem : Int) {
        arr.contains(elem)
      }) |> @qc.filter(arr.length() != 0)
    })
  )
}
```

## Classifying Test Data

### classify

```mbt
test "with classification" {
  @qc.quick_check_fn!(fn(xs : List[Int]) {
    @qc.Arrow(fn(_x) { true })
    |> @qc.classify(xs.length() > 5, "long list")
    |> @qc.classify(xs.length() <= 5, "short list")
  })
}
```

Output:
```
+++ [100/0/100] Ok, passed!
22% : short list
78% : long list
```

### label and collect

```mbt
// Label with string
|> @qc.label(if x.is_empty() { "trivial" } else { "non-trivial" })

// Collect for value distribution
|> @qc.collect(value, "category")
```

## Workflow Steps

### Step 1: Identify Target Functions

Categorize functions in your module:
- Transformation functions (input -> different output)
- Normalization functions (input -> same type, simplified)
- Stateful operations (side effects, state changes)

### Step 2: Apply Pattern Decision Tree

For each function, walk through the decision tree to select a pattern.

### Step 3: Design Generators

1. Identify edge cases specific to your domain
2. Choose distribution percentages
3. Implement using `frequency`, `one_of`, `sized`

### Step 4: Write Properties

Implement the property tests using selected patterns.

### Step 5: Add Statistics

Add `classify` calls to verify coverage, adjust generators if needed.

### Step 6: Run and Fix

```bash
moon info && moon fmt
moon test
```

## Migration from Aletheia

For repositories currently using `f4ah6o/aletheia`:

### Step 1: Update Dependencies

```bash
moon remove f4ah6o/aletheia
moon add moonbitlang/quickcheck
moon install
```

### Step 2: Update Imports

```diff
{
  "import": [
-   { "path": "f4ah6o/aletheia/quickcheck", "alias": "qc" }
+   { "path": "moonbitlang/quickcheck", "alias": "qc" }
  ]
}
```

### Step 3: API Compatibility

| Aletheia API | quickcheck API | Notes |
|--------------|----------------|-------|
| `@aletheia.quick_check_fn` | `@qc.quick_check_fn` | Compatible |
| `@aletheia.forall` | `@qc.forall` | Compatible |
| `@aletheia.frequency` | `@qc.frequency` | Compatible |
| `@aletheia.one_of` | `@qc.one_of` | Compatible |
| `@aletheia.classify` | `@qc.classify` | Compatible |

### Step 4: Clean Up

Delete `.pbt.md` files (Aletheia templates are no longer used).

### Step 5: Verify

```bash
moon info && moon fmt
moon test
```

## CI Workflow (Branch + Worktree + PR)

1. Create branch: `git checkout -b pbt/<short-topic>`
2. Create worktree: `git worktree add ../<repo>-pbt pbt/<short-topic>`
3. Run PBT workflow in worktree
4. Commit, push, and create PR
5. After merge: `git worktree remove ../<repo>-pbt`

## Type-Specific Edge Cases

| Type | Edge Cases |
|------|------------|
| Int | 0, 1, -1, MAX_INT, MIN_INT |
| String | "", single char, unicode, multiline (`\n`) |
| Array | [], single element, all same, sorted, reversed |
| Option | None, Some(edge_value) |
| Map | empty, single entry, duplicate values |

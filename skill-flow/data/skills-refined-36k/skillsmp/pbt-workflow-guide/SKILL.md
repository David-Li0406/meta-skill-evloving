---
name: pbt-workflow-guide
description: Root workflow for introducing, updating, migrating, and improving PBT in MoonBit repos. Delegates to aletheia-pbt or aletheia-self-pbt and includes CI/worktree flow.
---

# PBT Workflow Guide

## Overview

This skill provides a root workflow for introducing, updating, migrating, and improving Property-Based Testing (PBT) in MoonBit repositories. It delegates Aletheia template generation/sync to sub skills, and provides design guidance for patterns, generators, shrinking, and state machines. Use this guide to orchestrate the workflow end-to-end, including CI practices (branch + git worktree + PR).

- Select appropriate PBT patterns based on function characteristics
- Design effective generators with proper distribution control
- Implement custom `Shrink` for complex types
- Design state machine tests with shim abstractions

## Root vs Sub Skills (Selection Rules)

This skill is the root workflow. It chooses a sub skill based on the repository:

- If the target repo is `f4ah6o/aletheia.mbt` (this repo), use `aletheia-self-pbt`.
- Otherwise, use `aletheia-pbt`.

Use this guide for PBT design choices (pattern selection, generator distribution, custom shrink, and state machine modeling) regardless of repository.

## Workflow Modes

Use the matching mode for your task:

1. New adoption (no existing `.pbt.md` or PBT tests)
2. Update (sync/regenerate after code changes)
3. Migration/Improvement (existing Aletheia usage, but templates/tests need refactor, expansion, or modernization)
4. Expansion (add new coverage areas, patterns, or state-machine tests)

## Default Behavior (No Extra User Instructions)

If the user does not specify targets or depth, do the following instead of stopping after Aletheia CLI runs:

1. Run Aletheia analyze/generate/sync for the module or the most central package.
2. Pick 2-3 representative public, pure-ish functions (prefer stable behavior, small input domains).
3. Convert at least 1-3 properties from `mbt nocheck` to `mbt check` with real generators.
4. Ensure `sync` emits `pbt_generated_test.mbt` (or equivalent) in at least one package.
5. Run `moon info && moon fmt`, then `moon test` (use `--update` if snapshots change).
6. If tests fail, fix the properties/generators/shrinkers and re-run until tests pass.

If Aletheia detects zero patterns for a package, either remove the empty template or add a small manual property, and note the reason.

## Definition of Done (Minimum)

- At least one non-trivial property is implemented in `mbt check` (not just template output).
- Aletheia sync produces generated tests (e.g. `pbt_generated_test.mbt`).
- Tests pass (`moon test` or `moon test --update`), with failures fixed and re-run.

## When to Ask Questions

Ask for clarification if any of the following blocks progress:

- Expected behavior is unclear (no docs or tests; ambiguous semantics).
- All candidate functions are highly stateful or require external resources.
- The repo lacks a runnable MoonBit toolchain or tests cannot be executed.
- A test failure indicates ambiguous expected behavior that cannot be inferred from code or docs.

## If User Instructions Are Ambiguous (Offer Options)

When the user says "do PBT" without scope/stop conditions, propose 3 concrete options and ask them to pick one:

1. **Outcome-driven**: "Cover core public APIs and ensure each applicable pattern type has at least one property; minimum 3; stop when further properties are redundant or time budget is reached."
2. **Scope-driven**: "Target top 2-3 most-used modules; add the most meaningful property per module (more if cheap); minimum 3 total; stop when high-impact functions are covered."
3. **Budget-driven**: "Aim for 3-6 properties; continue past 3 if low-effort wins exist; stop at 6 or when test runtime exceeds 2 minutes."

## Aletheia-Assisted Setup (Delegated to Sub Skill)

Use the appropriate sub skill to detect patterns, generate `.pbt.md` templates, and sync them into package tests:

```bash
# In a project that depends on Aletheia (mooncakes.io) -> aletheia-pbt
moon run f4ah6o/aletheia/aletheia -- analyze <target> --explain
moon run f4ah6o/aletheia/aletheia -- generate <target>
moon run f4ah6o/aletheia/aletheia -- sync <target>

# In the aletheia.mbt repo itself -> aletheia-self-pbt
moon run src/aletheia -- analyze <target> --explain
moon run src/aletheia -- generate <target>
moon run src/aletheia -- sync <target>
```

Then refine the generated properties using the rest of this guide:
- Keep manual edits outside `<!-- aletheia:begin -->` / `<!-- aletheia:end -->`.
- Start code blocks as `mbt nocheck`, switch to `mbt check` after validating logic.
- Prefer public APIs in generated blackbox tests.

### MoonBit Markdown-Oriented Programming (MOP) Integration

- Prefer `.pbt.md` for Aletheia templates to avoid MoonBit treating them as source.
- If you find `.pbt.mbt.md`, rename it to `.pbt.md`.
- When using MoonBit-native `.mbt.md`, place tests in ` ```mbt test` / ` ```mbt check` blocks and sync with Aletheia.

**Migration snippet:**
```bash
find . -name "*.pbt.mbt.md" -exec sh -c 'mv "$1" "${1%.pbt.mbt.md}.pbt.md"' _ {} \;
```

## Pattern Decision Tree

Use this flow to select the appropriate pattern for a given function:

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
    └─ State Machine + Shim
```

### Pattern Summary

| Pattern | Use Case | Example |
|---------|----------|---------|
| Round-Trip | Encode/decode pairs | `parse(to_string(x)) == x` |
| Idempotent | Normalization functions | `sort(sort(x)) == sort(x)` |
| Invariant | Collection operations | `map(f, xs).length() == xs.length()` |
| Oracle | Algorithm verification | `my_sort(x) == stdlib_sort(x)` |
| Producer-Consumer | Chained operations | `consume(produce(x))` succeeds |
| State Machine | Stateful systems | Commands executed against model |

## Generator Design Guide

### Distribution Strategy

Effective PBT requires intentional control over input distribution:

| Category | Percentage | Purpose |
|----------|------------|---------|
| Normal values | 70% | Typical usage patterns |
| Edge cases | 15% | Empty, zero, single element |
| Boundary values | 15% | Limits, extremes |

### Using `frequency` for Distribution Control

```mbt
fn gen_my_int() -> @qc.Gen[Int] {
  @qc.frequency([
    (70, @qc.int()),                    // Normal values
    (15, @qc.one_of([@qc.pure(0), @qc.pure(1), @qc.pure(-1)])),  // Edge cases
    (15, @qc.one_of([@qc.pure(@int.max_value), @qc.pure(@int.min_value)])),  // Boundaries
  ])
}
```

### Type-Specific Edge Cases

| Type | Edge Cases |
|------|------------|
| Int | 0, 1, -1, MAX_INT, MIN_INT |
| String | "", single char, unicode, multiline (`\n`) |
| Array | [], single element, all same, sorted, reversed |
| Option | None, Some(edge_value) |
| Map | empty, single entry, duplicate values |

### Using `sized` for Recursive Types

For recursive types (trees, nested structures), use `sized` to prevent infinite recursion:

```mbt
fn gen_tree[T](gen_value : @qc.Gen[T]) -> @qc.Gen[Tree[T]] {
  @qc.sized(fn(size) {
    if size <= 0 {
      gen_value.map(Leaf)
    } else {
      @qc.frequency([
        (1, gen_value.map(Leaf)),
        (3, @qc.resize(size / 2, gen_tree(gen_value)).bind(fn(left) {
          @qc.resize(size / 2, gen_tree(gen_value)).map(fn(right) {
            Node(left, right)
          })
        })),
      ])
    }
  })
}
```

## Statistics & Classification Guide

### Using `classify` for Test Insight

Add classification to understand what your tests actually cover:

```mbt
test "my_property" {
  @qc.quick_check_fn(fn(xs : Array[Int]) {
    @qc.classify(xs.is_empty(), "empty")
    @qc.classify(xs.length() == 1, "single")
    @qc.classify(xs.length() > 10, "large")
    // ... property assertion
  })
}
```

### Using `collect` for Value Distribution

```mbt
test "check_distribution" {
  @qc.quick_check_fn(fn(n : Int) {
    @qc.collect(n % 10, "last digit")
    // ... property assertion
  })
}
```

### Interpreting Statistics

- If edge cases appear < 1% of the time, increase their frequency in the generator
- If certain categories never appear, your generator may have blind spots
- Use statistics to validate your distribution assumptions

## Shrink Implementation Guide

### Why Custom Shrink Matters

When a property fails, QuickCheck shrinks the counterexample to find the minimal failing case. Custom `Shrink` implementations help:

- Find smaller, more readable counterexamples
- Debug faster by isolating the essential failure

### Shrink Implementation Template

```mbt
pub impl Shrink for MyType with shrink(self) -> Iter[MyType] {
  let mut shrunk : Array[MyType] = []

  // Phase 1: Try simplest values first
  shrunk.push(MyType::default())

  // Phase 2: Simplify individual fields
  for field_shrunk in self.field.shrink() {
    shrunk.push(MyType::new(field_shrunk, self.other_field))
  }
  for other_shrunk in self.other_field.shrink() {
    shrunk.push(MyType::new(self.field, other_shrunk))
  }

  // Phase 3: Try boundary values
  shrunk.push(MyType::with_boundary_values())

  shrunk.iter()
}
```

### Shrinking Order Principles

1. **Try empty/zero first** - Simplest possible values
2. **Shrink one field at a time** - Isolate the problematic component
3. **Preserve structure when possible** - Keep overall shape while simplifying contents
4. **Respect invariants** - Don't generate invalid shrunk values

## State Machine Testing Guide

State machine testing verifies stateful systems by:
1. Generating sequences of commands
2. Executing them against both a model (pure) and the real system
3. Verifying postconditions after each command

### Shim Abstraction Pattern

Wrap non-deterministic or side-effecting operations in a shim:

```mbt
// Shim interface - isolates side effects
trait Shim {
  fn create_user(self, name : String) -> Result[UserId, Error]
  fn get_user(self, id : UserId) -> Result[User, Error]
  fn delete_user(self, id : UserId) -> Result[Unit, Error]
}

// Real implementation
struct RealShim { ... }

// Test implementation with controlled behavior
struct TestShim {
  users : Map[UserId, User]
  next_id : Int
}
```

### StateM Model Design

```mbt
// Model state - pure, no side effects
struct ModelState {
  users : Map[UserId, User]
  deleted : Set[UserId]
}

// Commands
enum UserCmd {
  Create(String)
  Get(UserId)
  Delete(UserId)
}

// State machine definition
let sm = StateM::new(
  "UserSystem",
  ModelState::default(),  // initial state
  fn(state, cmd) {        // next_state - must be PURE!
    match cmd {
      Create(name) => { ... }
      Get(id) => state  // queries don't change state
      Delete(id) => { ... }
    }
  },
)
.with_precondition(fn(state, cmd) {
  // Only allow valid commands
  match cmd {
    Get(id) | Delete(id) => state.users.contains(id)
    _ => true
  }
})
.with_postcondition(fn(state, cmd, result) {
  // Verify model matches reality
  match cmd {
    Get(id) => result == state.users.get(id)
    _ => true
  }
})
```

### Deterministic Model Principles

1. **Model state must be pure** - No side effects in `next_state`
2. **Model should be simple** - Easier than the real implementation
3. **Capture essential behavior** - Abstract away implementation details
4. **Use shims for non-determinism** - Wrap timestamps, random values, I/O

## Workflow Steps

### Step 0: Bootstrap with Aletheia (optional but recommended)

Let Aletheia generate the initial test templates, then use this guide to refine the properties, generators, and shrinkers.

### Step 1: Identify Target Functions

List functions in your module and categorize them:
- Transformation functions (input -> different output)
- Normalization functions (input -> same type, simplified)
- Stateful operations (side effects, state changes)

### Step 2: Apply Pattern Decision Tree

For each function, walk through the decision tree to select a pattern.

### Step 3: Design Generators

For each input type:
1. Identify edge cases specific to your domain
2. Choose distribution percentages
3. Implement using `frequency`, `one_of`, `sized` as needed

### Step 4: Add Statistics

Add `classify` and `collect` calls to verify coverage:
- Run tests with verbose output
- Verify edge cases appear at expected frequencies
- Adjust generators if distribution is skewed

### Step 5: Implement Custom Shrink (if needed)

For custom types with complex structure:
1. Implement `Shrink` trait
2. Follow shrinking order principles
3. Test that shrunk values maintain type invariants

### Step 6: Write Properties

Implement the actual property tests using the selected patterns.

### Step 7: Iterate

- Run tests and analyze failures
- Use statistics to improve coverage
- Refine generators based on discovered edge cases

## Migration/Improvement Guide (Existing Aletheia Users)

Use this when the repo already has `.pbt.md` or PBT tests but needs modernization or expansion.

1. Inventory existing templates/tests and identify gaps:
   - Missing patterns for key functions
   - Weak generators (no edge/boundary distribution)
   - Missing shrinks for complex types
   - No state-machine coverage for stateful APIs
2. Regenerate or resync templates with the correct sub skill.
3. Merge Aletheia-generated sections and keep manual edits outside markers.
4. Refine properties using the Pattern Decision Tree and Generator Design Guide.
5. Add statistics (`classify`, `collect`) to validate distribution.
6. Convert stable `mbt nocheck` blocks to `mbt check`.
7. Update snapshots if behavior changes are intentional.

## CI Workflow (Branch + Worktree + PR)

When applying this workflow in CI-oriented repos, follow a worktree-based flow:

1. Create a branch:
   - `git checkout -b pbt/<short-topic>`
2. Create a worktree for isolated edits:
   - `git worktree add ../<repo>-pbt pbt/<short-topic>`
3. Run the sub skill workflow in the worktree:
   - Analyze/generate/sync
   - Update properties/generators/shrinks
   - Run `moon info && moon fmt`
   - Run `moon test` (or `moon test --update` if snapshots change)
4. Commit changes and push the branch.
5. Create a PR from the branch.
6. Remove the worktree after merge:
   - `git worktree remove ../<repo>-pbt`

## End-to-End Scenarios

### Scenario A: New Adoption in a Non-Aletheia Repo

1. Create a branch and worktree.
2. Use `aletheia-pbt` to analyze/generate/sync templates for the target module.
3. Refine properties and generators per this guide.
4. Run `moon info && moon fmt`, then `moon test` (or `moon test --update` if snapshots change).
5. Commit, push, and open a PR.

### Scenario B: Migration/Improvement in an Existing Aletheia Repo

1. Create a branch and worktree.
2. Inventory existing `.pbt.md` and `_test.mbt` coverage; list gaps.
3. Regenerate or resync with the correct sub skill (`aletheia-pbt` for most repos, `aletheia-self-pbt` for this repo).
4. Merge generated sections and keep manual edits outside markers.
5. Upgrade generators and add missing shrinks/statistics.
6. Run `moon info && moon fmt`, then `moon test --update` if snapshots change.
7. Commit, push, and open a PR.

## Quick Reference

### Generator Expressions

| Expression | Purpose |
|------------|---------|
| `@qc.pure(x)` | Always generate x |
| `@qc.one_of([g1, g2])` | Equal probability choice |
| `@qc.frequency([(w1, g1), (w2, g2)])` | Weighted choice |
| `@qc.sized(fn(n) { ... })` | Size-dependent generation |
| `@qc.resize(n, gen)` | Override size parameter |
| `gen.filter(pred)` | Only values satisfying pred |
| `gen.map(f)` | Transform generated values |
| `gen.bind(f)` | Chain generators |

### Property Patterns

```mbt
// Round-Trip
decode(encode(x)) == x

// Idempotent
f(f(x)) == f(x)

// Invariant
output.property() satisfies constraint

// Oracle
my_impl(x) == reference_impl(x)
```

### Statistics Patterns

```mbt
// Binary classification
@qc.classify(condition, "label")

// Value collection
@qc.collect(value, "category")

// Multiple labels
@qc.classify(c1, "l1")
@qc.classify(c2, "l2")
```

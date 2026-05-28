---
name: refactor
description: This skill should be used when the user asks to "refactor", "extract function", "rename", "improve code quality", "reduce duplication", or "remove code smell". Supports Lean 4 and general refactoring patterns.
---

# Code Refactoring Guidelines

Guidance for restructuring existing code to improve readability, maintainability, and design without changing external behavior.

## Refactoring Workflow

1. Read and understand the target code thoroughly
2. Identify the specific refactoring opportunity (duplication, long function, etc.)
3. Ensure tests exist or behavior is well-understood before changes
4. Apply the refactoring in small, incremental steps
5. Verify behavior is preserved after each change
6. Run existing tests if available

## Code Restructuring Operations

### Extract Function/Method

When to use: Long functions, duplicated code blocks, or code with a clear single purpose.

```
Before:
  - Function does multiple things
  - Code block is repeated
  - Complex logic that deserves a name

After:
  - Extracted function with descriptive name
  - Single responsibility
  - Improved readability
```

Steps:
1. Identify the code block to extract
2. Determine required parameters and return values
3. Create new function with descriptive name
4. Replace original code with function call
5. Verify behavior is unchanged

### Rename

When to use: Names that don't clearly express intent or are misleading.

Guidelines:
- Use descriptive names that reveal intent
- Follow language conventions (camelCase, snake_case, etc.)
- Make names pronounceable
- Avoid abbreviations unless universally understood

### Move Code

When to use: Code that belongs in a different module/file based on cohesion.

Consider moving when:
- Code uses more from another module than its own
- A group of functions always change together
- Code doesn't fit the current module's responsibility

### Inline

When to use: A function/variable that adds no clarity.

Inline when:
- The body is as clear as the name
- Indirection obscures rather than clarifies
- Over-delegation makes code hard to follow

## Pattern-Based Refactoring

### Remove Duplication

1. Identify duplicated code blocks
2. Extract common logic into shared function
3. Parameterize differences
4. Replace duplicates with calls to shared function

### Simplify Conditionals

| Smell | Refactoring |
|-------|-------------|
| Nested conditionals | Use guard clauses (early return) |
| Complex boolean logic | Extract to well-named predicate function |
| Switch on type | Consider polymorphism or pattern matching |
| Repeated condition checks | Consolidate into single check |

### Reduce Function Parameters

- Group related parameters into a struct/record
- Use builder pattern for many optional parameters
- Consider whether function is doing too much

### Decompose Large Functions

Signs a function is too large:
- More than ~20-30 lines
- Multiple levels of abstraction
- Comments explaining sections
- Difficulty naming what it does

Approach:
1. Identify logical sections (often marked by comments or blank lines)
2. Extract each section into well-named function
3. Keep the original function as orchestration

## Code Smells to Address

| Smell | Description | Solution |
|-------|-------------|----------|
| Long Method | Function does too much | Extract smaller functions |
| Large Class | Class has too many responsibilities | Split into focused classes |
| Feature Envy | Method uses another class more than its own | Move method to that class |
| Data Clumps | Same group of data appears together | Create a struct/class |
| Primitive Obsession | Using primitives instead of small objects | Create domain types |
| Divergent Change | One class changed for multiple reasons | Split by responsibility |
| Shotgun Surgery | One change requires many small edits | Consolidate into one place |
| Dead Code | Unreachable or unused code | Delete it |

## Safety Guidelines

### Before Refactoring

- Ensure you understand the current behavior
- Check for existing tests
- Identify all callers/usages of code being changed
- Consider impact on public API

### During Refactoring

- Make one change at a time
- Keep changes small and reviewable
- Preserve external behavior exactly
- Maintain backward compatibility for public APIs

### After Refactoring

- Run all existing tests
- Verify functionality manually if no tests exist
- Review diff to confirm no unintended changes
- Consider if new tests are needed for clarity

## Language-Specific Patterns

Refactoring patterns vary by programming language. Identify the target language and consult the appropriate reference file.

### Selecting the Right Pattern File

1. Identify the language of the code being refactored
2. Load the corresponding pattern file from `references/`
3. Apply language-specific idioms and conventions

### Available Pattern Files

| Language | Reference File | Focus Areas |
|----------|----------------|-------------|
| Lean 4 | `references/patterns-lean.md` | Tactics, type classes, do-notation, structures |
| General | `references/patterns-general.md` | Language-agnostic OOP/FP patterns |

### Lean 4 Specific Considerations

For Lean 4 projects (like this ziku compiler):
- Prefer `where` clauses for local helpers
- Use tactic mode for complex proofs, term mode for simple ones
- Leverage type classes for extensibility
- Organize code with namespaces and sections
- Mark frequently used lemmas with `@[simp]`

## Additional Resources

### Reference Files

- **`references/patterns-lean.md`** - Lean 4 specific: tactics, structures, monads, type classes
- **`references/patterns-general.md`** - Language-agnostic OOP/FP refactoring patterns

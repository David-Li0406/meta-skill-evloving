---
name: jscodeshift-codemods
description: Use this skill when writing and debugging AST-based codemods with jscodeshift for automated code transformations, such as migrations, API upgrades, and large-scale refactoring.
---

# jscodeshift Codemods

**Core Philosophy:** Transform AST nodes, not text. Let recast handle printing to preserve formatting and structure.

<IMPORTANT>
1. Always use TDD - write failing tests before implementing transforms.
2. Transform the minimal AST necessary - surgical changes preserve formatting.
3. Handle edge cases explicitly - codemods run on thousands of files.
</IMPORTANT>

## When to Use

Use codemods for:

- **API migrations** - Library upgrades (e.g., React Router v5→v6).
- **Pattern standardization** - Enforce coding conventions across the codebase.
- **Deprecation removal** - Remove deprecated APIs systematically.
- **Large-scale refactoring** - Rename functions, restructure imports, update patterns.

**Don't use codemods for:**

- One-off changes (faster to do manually).
- Changes requiring semantic understanding (business logic).
- Non-deterministic transformations.

## Codemod Workflow

Copy this checklist and track your progress:

```
Codemod Progress:
- [ ] Phase 1: Identify Patterns
  - [ ] Collect before/after examples from real code.
  - [ ] Document transformation rules.
  - [ ] Identify edge cases.
- [ ] Phase 2: Create Test Fixtures
  - [ ] Create input fixture with pattern to transform.
  - [ ] Create expected output fixture.
  - [ ] Verify test fails (TDD).
- [ ] Phase 3: Implement Transform
  - [ ] Find target nodes.
  - [ ] Apply transformation.
  - [ ] Return modified source.
- [ ] Phase 4: Handle Edge Cases
  - [ ] Add fixtures for edge cases.
  - [ ] Handle already-transformed code (idempotency).
  - [ ] Handle missing dependencies.
- [ ] Phase 5: Validate at Scale
  - [ ] Dry run on target codebase.
  - [ ] Review sample of changes.
  - [ ] Run with --fail-on-error.
```

## Project Structure

Standard codemod project layout:

```
codemods/
├── my-transform.ts                    # Transform implementation
├── __tests__/
│   └── my-transform-test.ts           # Test file
└── __testfixtures__/
    ├── my-transform.input.ts          # Input fixture
    ├── my-transform.output.ts         # Expected output
    ├── edge-case.input.ts             # Additional fixtures
    └── edge-case.output.ts
```

## Transform Module Anatomy

Every transform exports a function with this signature:

```typescript
import type { API, FileInfo, Options } from "jscodeshift";

export default function transform(
  fileInfo: FileInfo,
  api: API,
  options: Options
): string | null | undefined {
  const j = api.jscodeshift;
  const root = j(fileInfo.source);

  // Find and transform nodes
  root
    .find(j.Identifier, { name: "oldName" })
    .forEach((path) => {
      path.node.name = "newName";
    });

  // Return transformed source, null to skip, or undefined for no change
  return root.toSource();
}
```

**Return values:**

| Return | Meaning |
|--------|---------|
| `string` | Transformed source code |
| `null` | Skip this file (no output) |
| `undefined` | No changes made |

## Testing with defineTest

jscodeshift provides fixture-based testing utilities:

```typescript
// __tests__/my-transform-test.ts
jest.autoMockOff();
const defineTest = require("jscodeshift/dist/testUtils").defineTest;

// Basic test - uses my-transform.input.ts → my-transform.output.ts
defineTest(__dirname, "my-transform");

// Named fixtures for edge cases
defineTest(__dirname, "my-transform", null, "already-transformed");
defineTest(__dirname, "my-transform", null, "missing-import");
defineTest(__dirname, "my-transform", null, "multiple-occurrences");
```

## Common Node Types

| Node Type | Represents | Example Code |
|-----------|------------|--------------|
| `Identifier` | Variable/function names | `foo`, `myVar` |
| `CallExpression` | Function calls | `foo()`, `obj.method()` |
| `MemberExpression` | Property access | `obj.prop`, `arr[0]` |
| `ImportDeclaration` | Import statements | `import { x } from 'y'` |
| `VariableDeclaration` | Variable declarations | `const x = 1` |
| `FunctionDeclaration` | Named functions | `function foo() {}` |

## Common Transformation Patterns

### Rename Import Source

```typescript
root
  .find(j.ImportDeclaration, { source: { value: "old-package" } })
  .forEach((path) => {
    path.node.source.value = "new-package";
  });
```

### Rename Function Calls

```typescript
root
  .find(j.CallExpression, { callee: { name: "oldFunction" } })
  .forEach((path) => {
    path.node.callee.name = "newFunction";
  });
```

## Debugging Transforms

### Dry Run with Print

```bash
npx jscodeshift -t my-transform.ts target/ --dry --print
```

### Verbose Mode

```bash
npx jscodeshift -t my-transform.ts target/ --verbose=2
```

## CLI Quick Reference

```bash
# Basic usage
npx jscodeshift -t transform.ts src/
```

## Integration

**Complementary skills:**

- **writing-tests** - For test-first codemod development.
- **systematic-debugging** - When transforms produce unexpected results.
- **verification-before-completion** - Verify codemod works before claiming done.
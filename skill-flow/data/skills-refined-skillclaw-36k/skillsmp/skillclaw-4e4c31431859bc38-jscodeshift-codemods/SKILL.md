---
name: jscodeshift-codemods
description: Use this skill when you need to write and debug AST-based codemods using jscodeshift for automated code transformations, such as migrations, API upgrades, or large-scale refactoring.
---

# Skill body

**Core Philosophy:** Transform AST nodes, not text. Let recast handle printing to preserve formatting and structure.

<IMPORTANT>
1. Always use TDD - write failing tests before implementing transforms.
2. Transform the minimal AST necessary - surgical changes preserve formatting.
3. Handle edge cases explicitly - codemods run on thousands of files.
</IMPORTANT>

## When to Use

Use codemods for:

- **API migrations** - Library upgrades (e.g., React Router v5→v6, enzyme→RTL).
- **Pattern standardization** - Enforce coding conventions across the codebase.
- **Deprecation removal** - Systematically remove deprecated APIs.
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
├── my-transform.ts                    # Transform implementation.
├── __tests__/
│   └── my-transform-test.ts           # Test file.
└── __testfixtures__/
    ├── my-transform.input.ts          # Input fixture.
    ├── my-transform.output.ts         # Expected output.
    ├── edge-case.input.ts             # Additional fixtures.
    └── edge-case.output.ts
```

## Transform Module Anatomy

Every transform exports a function with this signature:

```typescript
import type { API, FileInfo, Options } from 'jscodeshift';
```
---
name: typescript-optimization
description: Use this skill when you need to optimize TypeScript performance, configure tsconfig.json, fix type errors, or improve async patterns in your TypeScript projects.
---

# TypeScript Best Practices

This guide provides comprehensive performance optimization strategies for TypeScript applications, containing rules across various categories prioritized by their impact to assist in automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Configuring `tsconfig.json` for a new or existing project
- Writing complex type definitions or generics
- Optimizing async/await patterns and data fetching
- Organizing modules and managing imports
- Reviewing code for compilation or runtime performance

## Rule Categories by Priority

| Priority | Category                     | Impact        | Prefix   |
|----------|------------------------------|---------------|----------|
| 1        | Type System Performance       | CRITICAL      | `type-`  |
| 2        | Compiler Configuration        | CRITICAL      | `tscfg-` |
| 3        | Async Patterns                | HIGH          | `async-` |
| 4        | Module Organization           | HIGH          | `module-` |
| 5        | Type Safety Patterns          | MEDIUM-HIGH   | `safety-` |
| 6        | Memory Management             | MEDIUM        | `mem-`   |
| 7        | Runtime Optimization          | LOW-MEDIUM    | `runtime-` |
| 8        | Advanced Patterns             | LOW           | `advanced-` |

## Quick Reference

### 1. Type System Performance (CRITICAL)

- `type-interfaces-over-intersections`: Prefer interfaces over type intersections for faster resolution.
- `type-avoid-large-unions`: Avoid unions with 12+ members to prevent O(n²) checking.
- `type-extract-conditional-types`: Extract conditional types to enable caching.
- `type-limit-recursion-depth`: Add depth limits to recursive types.
- `type-explicit-return-types`: Add explicit return types to exported functions.
- `type-avoid-deep-generics`: Flatten deeply nested generic hierarchies.
- `type-simplify-mapped-types`: Break complex mapped types into smaller utilities.

### 2. Compiler Configuration (CRITICAL)

- `tscfg-enable-incremental`: Enable incremental compilation for 50-90% faster rebuilds.
- `tscfg-skip-lib-check`: Skip declaration file checking for 20-40% faster builds.
- `tscfg-isolate-modules`: Enable single-file transpilation for bundler integration.
- `tscfg-project-references`: Split large codebases into smaller projects for better management.

### 3. Async Patterns (HIGH)

- `async-use-promises`: Prefer promises over callbacks for better readability and error handling.
- `async-avoid-nested-promises`: Avoid nesting promises to prevent callback hell.

### 4. Module Organization (HIGH)

- `module-keep-imports-clean`: Organize imports to avoid circular dependencies.
- `module-use-absolute-paths`: Use absolute paths for easier navigation and refactoring.

### 5. Type Safety Patterns (MEDIUM-HIGH)

- `safety-use-strict-types`: Enforce strict types to catch errors early.
- `safety-avoid-any`: Avoid using `any` to maintain type safety.

### 6. Memory Management (MEDIUM)

- `mem-avoid-global-variables`: Limit the use of global variables to reduce memory leaks.
- `mem-use-weak-references`: Use weak references for large objects to allow garbage collection.

### 7. Runtime Optimization (LOW-MEDIUM)

- `runtime-avoid-unnecessary-computations`: Cache results of expensive computations.
- `runtime-use-lazy-loading`: Implement lazy loading for large modules.

### 8. Advanced Patterns (LOW)

- `advanced-use-decorators`: Leverage decorators for cleaner code and separation of concerns.
- `advanced-implement-middleware`: Use middleware patterns for better request handling.

This skill provides a structured approach to enhancing TypeScript applications, ensuring optimal performance and maintainability.
---
name: javascript-best-practices
description: JavaScript coding standards and best practices. This skill should be used when writing, reviewing, or refactoring JavaScript code. Triggers on tasks involving vanilla JavaScript, DOM manipulation, async operations, or performance optimization.
trigger_patterns:
  - javascript
  - vanilla js
  - dom manipulation
  - event listener
  - promise
  - async/await
auto_load_with:
  - react-best-practices
  - nextjs-best-practices
---

# JavaScript Best Practices

Comprehensive coding standards for JavaScript development, optimized for AI agents and LLMs. Contains 24 rules across 8 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Writing vanilla JavaScript code
- Implementing async operations and promises
- Handling DOM manipulation
- Optimizing JavaScript performance
- Reviewing code for security issues
- Working with ES modules and modern features

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Performance | CRITICAL | `perf-` |
| 2 | Async Patterns | CRITICAL | `async-` |
| 3 | Security | HIGH | `security-` |
| 4 | Error Handling | HIGH | `error-` |
| 5 | ES Modules | MEDIUM-HIGH | `module-` |
| 6 | Data Structures | MEDIUM | `data-` |
| 7 | DOM Manipulation | MEDIUM | `dom-` |
| 8 | Modern Features | LOW-MEDIUM | `modern-` |

## Quick Reference

### 1. Performance (CRITICAL)
- `perf-avoid-memory-leaks` - Clean up event listeners and intervals
- `perf-dom-batch-updates` - Batch DOM updates with DocumentFragment
- `perf-debounce-throttle` - Debounce scroll/resize handlers
- `perf-avoid-layout-thrashing` - Separate reads and writes to DOM
- `perf-web-workers` - Use Web Workers for heavy computation

### 2. Async Patterns (CRITICAL)
- `async-promise-all` - Use Promise.all() for parallel operations
- `async-promise-allsettled` - Use allSettled() when some can fail
- `async-error-boundaries` - Handle promise rejections properly
- `async-avoid-nested-promises` - Flatten with async/await
- `async-cancellation` - Use AbortController for cancellable requests

### 3. Security (HIGH)
- `security-no-innerhtml` - Use textContent instead of innerHTML
- `security-no-eval` - Never use eval() or new Function()
- `security-sanitize-user-input` - Sanitize before DOM insertion
- `security-csp-compliance` - Write CSP-compliant code

### 4. Error Handling (HIGH)
- `error-custom-errors` - Create custom Error classes
- `error-async-try-catch` - Wrap async operations in try-catch
- `error-global-handler` - Implement window.onerror handler

### 5. ES Modules (MEDIUM-HIGH)
- `module-named-exports` - Prefer named exports for tree-shaking
- `module-barrel-files` - Avoid barrel files in performance-critical code
- `module-dynamic-imports` - Use dynamic imports for code splitting

### 6. Data Structures (MEDIUM)
- `data-map-over-object` - Use Map for dynamic key collections
- `data-set-for-uniqueness` - Use Set for unique value collections
- `data-immutable-updates` - Use spread operator for immutability

### 7. Modern Features (LOW-MEDIUM)
- `modern-optional-chaining` - Use ?. for safe property access

## How to Use

Read individual rule files for detailed explanations and code examples.

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

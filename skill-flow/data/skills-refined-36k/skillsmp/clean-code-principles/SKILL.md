---
name: clean-code-principles
description: Language-agnostic coding principles for high-quality, maintainable code. Apply when generating new code, reviewing existing code, or refactoring. Covers DRY, KISS, YAGNI, Fail Fast, avoiding over-validation, and generalized SOLID principles (SRP, DIP). Automatically detect violations and provide corrected code.
---

# Clean Code Principles

Apply these principles to all code generation, review, and refactoring tasks.

## Core Principles

### DRY (Don't Repeat Yourself)
Extract duplicated logic into reusable functions/modules. Violation signs: copy-pasted code, similar patterns in multiple places.

### KISS (Keep It Simple, Stupid)
Prefer straightforward solutions. Avoid: clever one-liners that sacrifice readability, unnecessary abstractions, premature optimization.

### YAGNI (You Aren't Gonna Need It)
Implement only what's currently needed. Avoid: speculative features, unused parameters "for future use", over-engineered extensibility.

## Practical Principles

### Fail Fast
Detect and report errors at the earliest possible point. Validate at system boundaries (public APIs, user input), not deep in internal logic.

### Avoid Over-Validation
Validate once at the entry point. Internal functions can trust their callers. Signs of over-validation:
- Same null/type checks repeated across call chain
- Defensive checks in private/internal methods
- Redundant validation after already-validated data

## Design Principles (Generalized)

### Single Responsibility (SRP)
Each function/module should have one reason to change. Split when a function does multiple unrelated tasks.

### Dependency Inversion (DIP)
Depend on abstractions, not concrete implementations. Pass dependencies as parameters (functions, interfaces) rather than hardcoding them.

### Open-Closed & Interface Segregation (Light)
- OCP: Extend behavior without modifying existing code (via composition, callbacks, plugins)
- ISP: Keep interfaces/APIs minimal—expose only what clients need

## Workflow

**When generating code**: Apply principles from the start. Prefer simple, focused implementations.

**When reviewing code**: Identify violations → explain briefly → provide corrected version.

**When refactoring**: Prioritize by impact. Fix critical issues (DRY, over-validation) before stylistic ones.

## Violation Response Format

When violations are found, respond with:
1. Brief identification of the issue and which principle it violates
2. Corrected code

Keep explanations concise. For detailed examples of each principle, see [references/examples.md](references/examples.md).

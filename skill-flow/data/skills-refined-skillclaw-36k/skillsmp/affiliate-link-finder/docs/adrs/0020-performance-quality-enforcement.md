# ADR 0020: Performance & Quality Enforcement

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

As the codebase grew, a large number of lint warnings (84+) and minor performance inefficiencies (non-const widgets) began to accumulate. We needed a policy to ensure the project remains maintainable and high-performing as it moves toward production.

## Decision

Adopt a **"Zero-Warning" policy** enforced by `flutter analyze` and a mandatory **`const` optimization** strategy for the UI layer.

Key points:
1. **Analyis**: All builds/commits must pass `flutter analyze` with 0 issues.
2. **Const Correctness**: Every widget declaration and instantiation must use `const` where possible to minimize build context overhead.
3. **Type Safety**: Explicit typing for generic classes (e.g., `MaterialPageRoute<void>`) is required to avoid inference ambiguity.
4. **Redundancy**: No dead code or placeholder `TODO`s allowed in production paths.

## Rationale
- **Performance**: `const` constructors allow Flutter to skip entire subtrees during rebuilds, which is critical for smooth scrolling on complex dashboards with charts.
- **Maintainability**: A clean analysis makes it easy to spot *new* issues immediately instead of them being buried in existing noise.
- **Predictability**: Explicit generic types prevent runtime errors related to navigation and dialog returns.

## Consequences

**Positive:**
- Noticeable improvement in UI responsiveness and battery efficiency.
- Faster developer onboarding due to clean, self-documenting code style.
- Drastic reduction in "low hanging fruit" bugs (null safety, type mismatches).

**Negative:**
- Initial high effort to refactor existing screens (completed).
- Slightly more verbose code (adding `const` keywords).

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Allow Warnings | Leads to "broken window" syndrome where critical errors are ignored because the warning list is too long. |
| Selective Const | Hard to enforce consistently; easier to make it a universal rule. |
| Auto-fixers only | `dart fix` handles many cases but often misses context-specific optimizations or type inference issues. |

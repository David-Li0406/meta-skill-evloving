---
name: quality-assurance-standards
description: Use this skill to maintain code hygiene, implement automated checks, and ensure testing integrity.
---

# Quality Assurance - High-Density Standards

Standards for maintaining code hygiene, automated checks, and testing integrity.

## **Priority: P1 (MAINTENANCE)**

Standards for maintaining code quality, automated checks, and testing integrity.

## 🔍 Code Quality & Linting

- **Zero Tolerance**: Treat all linter warnings/infos as fatal errors in CI.
- **Automated Formatting**: Enforce strict formatting on every commit using hooks.
- **Type Safety**: Never use `any` or `dynamic` unless absolutely necessary. Use specific interfaces/types for all data boundaries.
- **Dead Code**: Proactively remove unused imports, variables, and deprecated methods.

## 🧪 Testing & TDD

- **F-I-R-S-T**: Tests must be Fast, Independent, Repeatable, Self-Validating, and Timely.
- **TDD (Red-Green-Refactor)**: Follow strict cycle enforcement for Test-Driven Development.
- **Edge Cases**: Always test null/empty states, boundary limits, and error conditions.
- **Mock Dependencies**: Isolate code by mocking external systems (APIs, DBs) to ensure deterministic results.

## 🔺 The Test Pyramid

- **Unit Tests (70%)**: Fast, isolated tests for individual functions/classes (TDD focus).
- **Integration Tests (20%)**: Tests for interactions between modules (e.g., Service + DB).
- **E2E Tests (10%)**: Slow, realistic tests for user flows from UI to Backend.

## 🎯 Risk-Based Testing

- **Prioritize Critical Paths**: Ensure high coverage for Login, Payments, and Data Integrity.
- **Impact Analysis**: Assess the consequences of failures, especially for critical data.

## 🛠 Refactoring & Code Reviews

- **Code Smells**: Proactively refactor duplicated code, long methods (>20 lines), and "god classes".
- **Incremental Changes**: Perform small, behavior-preserving transformations (Extract Method, Rename Variable).
- **Quality Gate**: Use peer reviews to share knowledge and catch logic errors before merging.
- **Constructive Feedback**: Critique the code, not the author. Explain the "why" behind suggestions.

## 🛠 Automation & Hooks

- **Pre-commit Hooks**: Validate linting, formatting, and unit tests before every push.
- **Documentation**: Keep public APIs documented. Use triple-slash/JSDoc.
- **Strict Dependencies**: Lock versions in `pubspec.lock` / `package-lock.json` / `pnpm-lock.yaml`.

## 🚫 Anti-Patterns

- **Broken Window**: No ignoring warnings; leaving "small" lint errors leads to codebase rot.
- **Testing Implementation**: No testing internals; changes to private methods shouldn't break tests.
- **Manual QA Dependency**: No "Test-Last"; verification must be automated and continuous.
- **Magic Strings**: No hardcoded IDs; use constants or generated keys for accessibility/test IDs.

## 📚 References

- [TDD Cycle & Feedback Examples](references/TDD_FEEDBACK.md)
---
name: quality-assurance-standards
description: Use this skill when you need to establish and maintain high standards for code hygiene, automated checks, and testing integrity in your development process.
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

- **Unit Tests (70%)**: Fast, isolated tests for individual functions/classes.
- **Integration Tests (20%)**: Tests for interactions between modules (e.g., Service + DB).
- **E2E Tests (10%)**: Slow, realistic tests for user flows from UI to Backend.

## 🎯 Risk-Based Testing

- **Prioritize Critical Paths**: Ensure high coverage for critical paths like Login, Payments, and Data Integrity.
- **Impact Analysis**: Assess the consequences of failures and test thoroughly if the impact is significant (e.g., Data Loss).

## 🛠 Refactoring & Code Reviews

- **Code Smells**: Proactively refactor duplicated code, long methods (>20 lines), and "god classes".
- **Incremental Changes**: Perform small, behavior-preserving transformations (e.g., Extract Method, Rename Variable).
- **Quality Gate**: Use peer reviews to share knowledge and catch logic errors before merging.
- **Constructive Feedback**: Critique the code, not the author. Explain the "why" behind suggestions.

## 🛠 Automation & Hooks

- **Pre-commit Hooks**: Validate linting, formatting, and unit tests before every push.
- **Documentation**: Keep public APIs documented. Use triple-slash/JSDoc.
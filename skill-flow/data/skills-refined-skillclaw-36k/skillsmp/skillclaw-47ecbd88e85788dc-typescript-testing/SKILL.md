---
name: typescript-testing
description: Use this skill when writing frontend tests or reviewing test quality, particularly with Vitest, React Testing Library, and MSW.
---

# TypeScript Testing Rules (Frontend)

## Test Framework
- **Vitest**: This project uses Vitest.
- **React Testing Library**: For component testing.
- **MSW (Mock Service Worker)**: For API mocking.
- Test imports: `import { describe, it, expect, beforeEach, vi } from 'vitest'`
- Component test imports: `import { render, screen, fireEvent } from '@testing-library/react'`
- Mock creation: Use `vi.mock()`.

## Basic Testing Policy

### Quality Requirements
- **Coverage**: Unit test coverage must be 60% or higher (Frontend standard 2025).
- **Independence**: Each test can run independently without depending on other tests.
- **Reproducibility**: Tests are environment-independent and always return the same results.
- **Readability**: Test code maintains the same quality as production code.

### Coverage Requirements (ADR-0002 Compliant)
**Mandatory**: Unit test coverage must be 60% or higher.
**Component-specific targets**:
- Atoms (Button, Text, etc.): 70% or higher.
- Molecules (FormField, etc.): 65% or higher.
- Organisms (Header, Footer, etc.): 60% or higher.
- Custom Hooks: 65% or higher.
- Utils: 70% or higher.

**Metrics**: Statements, Branches, Functions, Lines.

### Test Types and Scope
1. **Unit Tests (React Testing Library)**
   - Verify behavior of individual components or functions.
   - Mock all external dependencies.
   - Most numerous, implemented with fine granularity.
   - Focus on user-observable behavior.

2. **Integration Tests (React Testing Library + MSW)**
   - Verify coordination between multiple components.
   - Mock APIs with MSW (Mock Service Worker).
   - No actual DB connections (backend manages DB).
   - Verify major functional flows.

3. **Cross-functional Verification in E2E Tests**
   - Mandatory verification of impact on existing features when adding new features.
   - Cover integration points with "High" and "Medium" impact levels from Design Doc's "Integration Point Map".
   - Verification pattern: Existing feature operation → Enable new feature → Verify continuity of existing features.
   - Success criteria: No change in displayed content, rendering time within 5 seconds.
   - Designed for automatic execution in CI/CD pipelines.

## Red-Green-Refactor Process (Test-First Development)
- Recommended practice for developing tests before implementing features.
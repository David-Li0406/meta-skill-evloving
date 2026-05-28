---
name: software-architecture
description: Use this skill when you want to write code, design architecture, or analyze code in any software development context.
---

# Software Architecture Development Skill

This skill provides guidance for quality-focused software development and architecture, based on Clean Architecture and Domain Driven Design principles.

## Code Style Rules

### General Principles

- **Early return pattern**: Always use early returns when possible, over nested conditions for better readability.
- Avoid code duplication through the creation of reusable functions and modules.
- Decompose long components and functions (more than 80 lines of code) into smaller ones. If they cannot be reused, keep them in the same file; however, if a file exceeds 200 lines, it should be split into multiple files.
- Use arrow functions instead of function declarations when possible.

### Best Practices

#### Library-First Approach

- **ALWAYS search for existing solutions before writing custom code**:
  - Check npm for existing libraries that solve the problem.
  - Evaluate existing services/SaaS solutions.
  - Consider third-party APIs for common functionality.
- Use libraries instead of writing your own utilities or helpers. For example, use `cockatiel` for retry logic.
- **When custom code IS justified**:
  - Specific business logic unique to the domain.
  - Performance-critical paths with special requirements.
  - When external dependencies would be overkill.
  - Security-sensitive code requiring full control.
  - When existing solutions don't meet requirements after thorough evaluation.

#### Architecture and Design

- **Clean Architecture & DDD Principles**:
  - Follow domain-driven design and ubiquitous language.
  - Separate domain entities from infrastructure concerns.
  - Keep business logic independent of frameworks.
  - Define use cases clearly and keep them isolated.
- **Naming Conventions**:
  - **AVOID** generic names: `utils`, `helpers`, `common`, `shared`.
  - **USE** domain-specific names: `OrderCalculator`, `UserAuthenticator`, `InvoiceGenerator`.
  - Follow bounded context naming patterns.
  - Each module should have a single, clear purpose.
- **Separation of Concerns**:
  - Do NOT mix business logic with UI components.
  - Keep database queries out of controllers.
  - Maintain clear boundaries between contexts.
  - Ensure proper separation of responsibilities.

#### Anti-Patterns to Avoid

- **NIH (Not Invented Here) Syndrome**:
  - Don't build custom auth when existing solutions like Auth0/Supabase are available.
  - Don't write custom state management instead of using established libraries like Redux/Zustand.
  - Don't create custom form validation instead of using established libraries.
- **Poor Architectural Choices**:
  - Mixing business logic with UI components.
  - Database queries directly in controllers.
  - Lack of clear separation of concerns.
- **Generic Naming Anti-Patterns**:
  - `utils.js` or `utils.cs` with unrelated functions.
  - `helpers/misc.js` or `helpers/misc.cs` as a dumping ground.
  - `common/shared.js` or `common/shared.cs` with unclear purpose.
- Remember: Every line of custom code is a liability that needs maintenance, testing, and documentation.

#### Code Quality

- Proper error handling with typed catch blocks.
- Break down complex logic into smaller, reusable functions.
- Avoid deep nesting (max 3 levels).
- Keep functions focused and under 50 lines when possible.
- Keep files focused and under 200 lines of code when possible.
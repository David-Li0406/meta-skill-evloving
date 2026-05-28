---
name: software-architecture
description: Use this skill when you want to design quality-focused software architecture, write code, or analyze existing code in any software development context.
---

# Software Architecture Development Skill

This skill provides guidance for quality-focused software development and architecture, based on Clean Architecture and Domain Driven Design principles.

## Code Style Rules

### General Principles

- **Early return pattern**: Always use early returns when possible, over nested conditions for better readability.
- Avoid code duplication by creating reusable functions and modules.
- Decompose long components and functions (more than 80 lines of code) into smaller ones. If they cannot be reused, keep them in the same file. If a file exceeds 200 lines, split it into multiple files.
- Use arrow functions instead of function declarations when possible.

### Best Practices

#### Library-First Approach

- **ALWAYS search for existing solutions before writing custom code**:
  - Check npm for existing libraries that solve the problem.
  - Evaluate existing services/SaaS solutions.
  - Consider third-party APIs for common functionality.
- Use libraries instead of writing your own utilities or helpers. For example, use `cockatiel` instead of writing your own retry logic.
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
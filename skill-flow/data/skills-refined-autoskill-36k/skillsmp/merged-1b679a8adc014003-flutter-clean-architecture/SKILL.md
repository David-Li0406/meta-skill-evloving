---
name: flutter-clean-architecture
description: Use this skill when implementing Clean Architecture patterns in Flutter applications, focusing on separation of concerns, dependency rules, and testability.
---

# Flutter Clean Architecture

## Core Principles

Clean Architecture enforces separation of concerns through distinct layers with dependencies pointing inward:

1. **Domain Layer** (innermost) - Business logic and entities
2. **Application Layer** - Use cases and application-specific logic
3. **Infrastructure Layer** - External concerns (databases, APIs, frameworks)
4. **Presentation Layer** (outermost) - UI and user interaction

The fundamental rule: inner layers must never depend on outer layers.

## Structure

```text
lib/
├── domain/ # Pure Dart: entities (@freezed), failures, repository interfaces
├── infrastructure/ # Implementation: DTOs, data sources, mappers, repo impls
├── application/ # Orchestration: BLoCs / Cubits
└── presentation/ # UI: Screens, reusable components
```

## Implementation Guidelines

- **Dependency Flow**: `Presentation -> Application -> Domain <- Infrastructure`. Dependencies point inward.
- **Pure Domain**: No Flutter (Material/Store) or Infrastructure (Dio/Hive) dependencies in `Domain`.
- **Functional Error Handling**: Repositories must return `Either<Failure, Success>`.
- **Always Map**: Infrastructure must map DTOs to Domain Entities; do not leak DTOs to UI.
- **Immutability**: Use `@freezed` for all entities and failures.
- **Logic Placement**: No business logic in UI; widgets only display state and emit events.
- **Inversion of Control**: Use `get_it` to inject repository implementations into BLoCs.

## Anti-Patterns

- **No DTOs in UI**: Never import a `.g.dart` or Data class directly in a Widget.
- **No Material in Domain**: Do not import `package:flutter/material.dart` in the `domain` layer.
- **No Shared Prefs in Repo**: Do not use `shared_preferences` directly in a Repository; use a Data Source.

## Related Topics

- feature-based-clean-architecture
- bloc-state-management
- dependency-injection
- error-handling

## Key Libraries

- `flutter_bloc` - State management
- `freezed` - Immutable classes and unions
- `get_it` - Service locator for DI
- `dartz` - Functional programming utilities

## Testing Strategy

- Write table-driven unit tests with mocks.
- Separate fast unit tests from integration tests.
- Use interfaces to inject test doubles.
- Achieve high coverage of business logic.
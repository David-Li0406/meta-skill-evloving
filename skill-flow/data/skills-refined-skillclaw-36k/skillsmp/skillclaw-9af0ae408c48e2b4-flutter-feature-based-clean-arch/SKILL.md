---
name: flutter-feature-based-clean-architecture
description: Use this skill when you want to organize your Flutter code by feature to enhance scalability and maintainability.
---

# Feature-Based Clean Architecture

## **Priority: P0 (CRITICAL)**

Standard for modular Clean Architecture organized by business features in `lib/features/`.

## Structure

```text
lib/
├── features/ <feature_name>/
│   ├── domain/ # Business Logic (Pure Dart): entities, interfaces, use_cases
│   ├── data/ # Implementation: data_sources, dtos, repositories
│   └── presentation/ # UI & State: blocs, pages, widgets
├── core/ # Shared infrastructure & utilities
└── shared/ # Common UI components & shared entities
```

## Implementation Guidelines

- **Feature Encapsulation**: Keep logic, models, and UI internal to the feature directory.
- **Strict Layering**: Maintain 3-layer separation (Domain/Data/Presentation) within each feature.
- **Dependency Rule**: `Presentation -> Domain <- Data`. Domain must have zero external dependencies.
- **Cross-Feature Communication**: Features only depend on the **Domain** layer of other features.
- **Flat features**: Keep `lib/features/` flat; avoid nested features.
- **No DTO Leakage**: Never expose DTOs or Data Sources to UI or other features; return Domain Entities.
- **Shared logic**: Move cross-cutting concerns to `lib/shared/` or `lib/core/`.

## Reference & Examples

For feature folder blueprints and cross-layer dependency templates, see [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

layer-based-clean-architecture | retrofit-networking | go-router-navigation | bloc-state-management | dependency-injection
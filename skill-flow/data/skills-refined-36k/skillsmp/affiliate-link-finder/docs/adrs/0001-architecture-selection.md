# 1. Architecture Selection

Date: 2026-01-18

## Status

Accepted

## Context

The ADHD Supplement App requires a robust, scalable, and testable architecture. We need to support cross-platform development (Flutter), handle complex business logic (medication interactions), and allow for future backend flexibility (currently Firebase). The code needs to be maintainable by ensuring a clear separation of concerns.

## Decision

We have decided to adopt a hybrid **Hexagonal Architecture (Ports and Adapters)** combined with the **MVVM (Model-View-ViewModel)** pattern.

### Structure
- **Domain Layer (`lib/domain`)**: Contains pure business logic, entities (Supplement, Medication), and repository interfaces. No Flutter dependencies.
- **Application Layer (`lib/application`)**: Contains ViewModels that manage state and act as a bridge between the Domain and Presentation layers.
- **Infrastructure Layer (`lib/infrastructure`)**: Implements repository interfaces (Mock/Firebase) and external services (Url, Notifications).
- **Presentation Layer (`lib/presentation`)**: Contains Flutter Widgets and Views that observe ViewModels.

## Consequences

### Positive
- **Testability**: Domain logic can be tested in isolation without UI or Flutter framework dependencies.
- **Flexibility**: Infrastructure implementations (e.g., swapping Mock data for Firebase) can be changed without affecting the core logic.
- **Separation**: UI code is focused solely on rendering, while logic resides in ViewModels and Domain services.

### Negative
- **Boilerplate**: Requires creating interfaces and implementations for repositories, which adds initial setup time.
- **Complexity**: Slightly steeper learning curve for developers unfamiliar with clean architecture compared to a simple MVC pattern.

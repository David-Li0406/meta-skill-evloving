---
name: flutter-architecture
description: Master Flutter app architecture patterns including MVVM, Clean Architecture, dependency injection, and design patterns for building scalable and maintainable applications. Use when designing app structure, implementing architecture patterns, or organizing code for large-scale projects.
version: 1.0.0
---

# Flutter Architecture

Master Flutter app architecture patterns including MVVM, Clean Architecture, and design patterns for building scalable, maintainable applications.

## When to Use This Skill

Use this skill when:

- Architecting a new Flutter application from scratch
- Refactoring an existing Flutter app to improve maintainability and scalability
- Implementing MVVM pattern with ViewModels and state management
- Applying Clean Architecture principles with proper layer separation
- Setting up dependency injection with get_it and injectable
- Organizing project structure (feature-based vs layer-based)
- Implementing repository and service patterns
- Building applications that require high testability
- Working on team projects with multiple developers
- Scaling a Flutter codebase for long-term maintenance

## Why Architecture Matters in Flutter

Architecture is the foundation of any successful Flutter application. While Flutter makes it easy to build beautiful UIs quickly, without proper architecture, applications become difficult to maintain, test, and scale as they grow.

### The Cost of Poor Architecture

Many Flutter developers start building apps without considering architecture, leading to:

- **Massive widget files** containing business logic, UI code, and data fetching all mixed together
- **Tight coupling** between components making changes risky and time-consuming
- **Difficult testing** because logic is embedded in widgets that require full widget testing
- **Merge conflicts** when multiple developers work on the same features
- **Slow onboarding** as new developers struggle to understand the codebase structure
- **Technical debt** that compounds over time, eventually requiring expensive rewrites

### The Benefits of Intentional Architecture

Investing in proper architecture from the start provides significant long-term benefits:

**Maintainability**: Well-architected code is easier to modify, update, and fix. When business requirements change (and they always do), you can make updates confidently without breaking unrelated features.

**Scalability**: Multiple developers can work on different features simultaneously without stepping on each other's toes. The clear separation of concerns means team members can focus on specific layers or features.

**Testability**: Separation of concerns makes it possible to write unit tests for business logic without dealing with widget trees or UI rendering. Simpler classes with well-defined inputs and outputs are easier to mock and test in isolation.

**Lower Cognitive Load**: New developers become productive faster when they can follow established patterns. Code reviews become easier when everyone follows the same architectural principles.

**Better User Experience**: Features ship faster with fewer bugs when the codebase is well-organized and testable. Developers can focus on delivering value rather than fighting with technical debt.

## MVVM Pattern in Flutter

Model-View-ViewModel (MVVM) is the recommended architectural pattern for Flutter applications. It separates a feature into three distinct parts that work together while maintaining clear boundaries.

### The Three Components

**Model**: Represents the data layer of your application. In Flutter MVVM, this includes repositories and services that fetch, cache, and manage data from various sources (APIs, databases, local storage). The Model layer is responsible for business rules related to data access and transformation.

**View**: Describes how to present application data to the user. Views are compositions of widgets that make up a feature or screen. In Flutter, a view is often a StatelessWidget or StatefulWidget that builds the UI based on state provided by the ViewModel.

**ViewModel**: Contains the logic that converts app data into UI state. The ViewModel sits between the Model and View, fetching data from repositories/services, processing it, and exposing it in a format that's ready for display. ViewModels also handle user interactions and trigger appropriate business logic.

### Key Principles of Flutter MVVM

**One-to-One Relationship**: Views and ViewModels should have a one-to-one relationship. Each screen or major feature should have its own ViewModel that manages state specifically for that view.

**Unidirectional Knowledge**: The View knows about the ViewModel, and the ViewModel knows about the Model, but the Model is unaware of the ViewModel, and the ViewModel is unaware of the View. This unidirectional dependency prevents circular dependencies and keeps concerns separated.

**State Management Integration**: ViewModels work with state management solutions like Provider, Riverpod, or BLoC to expose state to the View and notify it of changes. The choice of state management solution doesn't change the fundamental MVVM pattern.

### Why MVVM for Flutter

MVVM aligns naturally with Flutter's reactive programming model. The pattern works seamlessly with Flutter's state management ecosystem and provides clear guidelines for where different types of code should live. The official Flutter documentation, updated in 2026, recommends MVVM as the standard pattern for building scalable Flutter applications.

## Clean Architecture in Flutter

Clean Architecture takes the separation of concerns further by defining explicit layers with clear responsibilities and dependencies. While MVVM focuses on the UI layer, Clean Architecture provides a complete system architecture.

### The Three Layers

**Presentation Layer**: The outermost layer containing all UI components, widgets, screens, and presentation logic holders (ViewModels, Controllers, BLoCs). This layer depends on the Domain layer but is independent of data sources.

**Domain Layer**: The heart of the application containing core business logic, entities, and use cases. This layer is completely independent of frameworks, UI, and data sources. It's written in pure Dart without any Flutter dependencies.

**Data Layer**: Responsible for retrieving data from various sources (REST APIs, GraphQL, local databases, platform plugins). This layer implements the repository interfaces defined in the Domain layer.

### The Dependency Rule

The fundamental rule of Clean Architecture is the dependency rule: source code dependencies must point inward toward higher-level policies. The Domain layer doesn't depend on anything. The Data and Presentation layers both depend on the Domain layer but not on each other.

This is achieved through dependency inversion - the Domain layer defines abstract repository interfaces, and the Data layer provides concrete implementations. The Presentation layer depends on the Domain layer's use cases and entities, never directly on data sources.

### Communication Flow

State flows from the Data layer through the Domain layer and eventually to the Presentation layer. User events flow in the opposite direction: from the Presentation layer through use cases in the Domain layer and to repositories in the Data layer.

This unidirectional flow makes the system predictable and easy to reason about. Each layer has a clear responsibility and doesn't need to know about implementation details in other layers.

## SOLID Principles in Flutter

SOLID principles provide specific guidelines for writing clean, maintainable object-oriented code. Applying these principles in Flutter creates well-structured applications that are easier to understand, modify, and extend.

### Single Responsibility Principle (SRP)

A class should have only one reason to change. This prevents "god classes" that try to do everything. In Flutter, this means:

- Widgets focus only on UI layout and composition
- ViewModels handle only presentation logic for specific views
- Repositories focus only on data access for specific entities
- Services handle only specific business operations

### Open/Closed Principle (OCP)

Classes should be open for extension but closed for modification. Use inheritance, composition, and interfaces to allow future extensions without modifying existing code. In Flutter, this often means:

- Defining abstract base classes for common behaviors
- Using composition to add functionality
- Leveraging Dart's mixin system for reusable behaviors

### Liskov Substitution Principle (LSP)

Subtypes should be substitutable for their base types without altering correctness. If you have a base class and derived classes, using a derived class should work seamlessly without unexpected behavior. This is crucial for repository interfaces and their implementations.

### Interface Segregation Principle (ISP)

Clients shouldn't depend on interfaces they don't use. Create small, focused interfaces rather than large, monolithic ones. In Flutter, prefer multiple specific repository interfaces over one giant data access interface.

### Dependency Inversion Principle (DIP)

High-level modules should depend on abstractions, not concrete implementations. This is the foundation of Clean Architecture's dependency rule. Use abstract classes and dependency injection to ensure flexibility and testability.

## Dependency Injection in Flutter

Dependency Injection (DI) is essential for implementing Clean Architecture and maintaining testability. DI makes dependencies explicit, controls object lifetimes, and enables easy testing through mock substitution.

### Why Dependency Injection

Without DI, classes create their own dependencies, leading to tight coupling and difficult testing. With DI, dependencies are provided from outside, making it easy to substitute implementations for testing or to support different configurations.

### get_it: Flutter's Service Locator

get_it is the most popular dependency injection solution for Flutter. It provides a simple service locator pattern that works well with Flutter's architecture. Combined with the injectable package for code generation, it provides a complete DI solution with minimal boilerplate.

### Best Practices for DI in Flutter

**Centralize Registration**: Register all dependencies at app start in a single composition root. This makes it easy to see all dependencies and their lifecycles.

**Use Constructor Injection**: Make dependencies explicit through constructor parameters. If you can't tell what a class depends on by reading its constructor, your DI has failed.

**Manage Lifecycles**: Use singleton registration for app-wide services and factory registration for short-lived objects. Most memory leaks in Flutter are DI lifetime bugs.

**Environment-Specific Injection**: Use injectable's environment support to provide different implementations for development, testing, and production.

## Project Structure

How you organize your Flutter project has a significant impact on maintainability and scalability. The two main approaches are feature-based and layer-based organization.

### Feature-Based Structure

Feature-based structure creates a folder for each feature, with layers as subfolders within each feature. This approach keeps all code related to a specific feature in one place, making it easier to develop, test, and maintain features independently.

Feature-based organization is recommended for medium to large projects because it scales well and minimizes merge conflicts when multiple developers work on different features.

### Layer-Based Structure

Layer-based structure organizes by layers first (presentation, domain, data), with features nested inside each layer. While this provides a clear view of architectural layers, it can be cumbersome for large projects as files belonging to different layers of the same feature are far apart.

Layer-based structure works well for smaller projects or when you want to emphasize architectural layers over features.

### File Naming Conventions

Regardless of structure choice, consistent file naming is essential:

- Use snake_case for all file names
- Suffix files by type: `user_repository.dart`, `login_view_model.dart`, `home_view.dart`
- Group related files in appropriately named subdirectories
- Keep test files parallel to source files with `_test.dart` suffix

## Design Patterns

Several design patterns are fundamental to Flutter architecture and appear repeatedly in well-structured applications.

### Repository Pattern

Repositories abstract data access, providing a clean API for the domain layer to access data without knowing about implementation details. Repositories handle concerns like caching, data source selection, and error handling.

### Service Pattern

Services combine multiple repositories to provide more complex domain operations. While repositories focus on single entities, services orchestrate multiple data sources to fulfill business requirements.

### Factory Pattern

Factories encapsulate object creation logic, useful for creating complex objects or selecting implementations based on configuration. In Flutter, factories are often used for creating platform-specific implementations.

### Singleton Pattern

Singletons ensure only one instance of a class exists. In Flutter, use get_it's singleton registration rather than implementing singletons manually. This provides better testability and lifecycle management.

## Integration with State Management

Architecture patterns work with, not against, state management solutions. MVVM and Clean Architecture are compatible with all major Flutter state management approaches.

### Riverpod (Recommended for 2026)

Riverpod is the modern standard for new Flutter projects. It provides compile-time safety, built-in dependency injection, and excellent testability. Riverpod providers can serve as ViewModels in MVVM architecture.

### BLoC

BLoC (Business Logic Component) enforces a strict separation between UI and business logic through streams and events. BLoC works naturally with Clean Architecture, with BLoCs serving as ViewModels in the Presentation layer.

### Provider

Provider was Flutter's official recommendation for years and remains stable and widely used. While Riverpod is recommended for new projects, Provider works well with MVVM and Clean Architecture patterns.

## Testing Strategy

Proper architecture makes testing straightforward and effective. Each layer can be tested independently with appropriate testing strategies.

### Unit Testing

Test business logic in isolation:
- Use cases in the Domain layer
- ViewModels in the Presentation layer
- Repository implementations in the Data layer

Mock dependencies using packages like mockito or mocktail to isolate the code under test.

### Widget Testing

Test Views in isolation by providing mock ViewModels. Widget tests verify that the UI correctly displays state and triggers appropriate ViewModel methods in response to user interaction.

### Integration Testing

Test complete features end-to-end, verifying that layers work together correctly. Integration tests validate the system as a whole while still using test doubles for external dependencies like APIs.

## Getting Started

To implement proper architecture in your Flutter project:

1. **Choose your structure**: Decide between feature-based and layer-based organization based on project size and team preferences
2. **Set up dependency injection**: Configure get_it and injectable for dependency management
3. **Define your layers**: Establish clear boundaries between Presentation, Domain, and Data
4. **Implement MVVM**: Create Views, ViewModels, and Models following the pattern's principles
5. **Apply SOLID principles**: Review each class for single responsibility and proper abstraction
6. **Write tests**: Build testability in from the start with comprehensive unit and widget tests

## Related Skills

- **flutter-state-management**: Deep dive into state management solutions
- **flutter-testing**: Comprehensive testing strategies for Flutter apps
- **flutter-performance**: Optimizing Flutter app performance

## Additional Resources

For detailed implementation guidance, code examples, and best practices, see the reference documents in this skill:

- `references/mvvm-pattern.md` - Complete MVVM implementation guide
- `references/clean-architecture.md` - Clean Architecture layer details
- `references/dependency-injection.md` - DI setup and configuration
- `references/project-structure.md` - Organizing your codebase
- `references/design-patterns.md` - Common patterns in Flutter
- `examples/feature-structure.md` - Complete feature module example
- `examples/layered-app.md` - Full Clean Architecture example

# ADR 0035: Modular Dependency Injection (Locator Refactor)

## Status
Accepted

## Context
As the application grew, the `locator.dart` file (using the `GetIt` package) became a monolithic registration block. Service dependencies were scattered, making it difficult to find specific registrations and increasing the risk of coupling errors. To maintain clean hexagonal architecture and support future scaling, a more organized approach to dependency management was required.

## Decision
We refactored the central `setupLocator()` function into domain-specific registration modules:
1.  **Logical Grouping**: Introduced private helper methods within `locator.dart` (e.g., `_setupCoreServices`, `_setupInfrastructure`, `_setupViewModels`) to encapsulate related registrations.
2.  **Explicit Initialization Phase**: Standardized the startup sequence to ensure hardware/storage abstractions (SharedPrefs) are initialized before higher-level application services.
3.  **Encapsulation**: Reduced visibility of implementation-specific details by grouping them within these modular blocks.

## Consequences
- **Maintainability**: New features can now be added by creating/modifying specific registration blocks rather than appending to a 500-line function.
- **Traceability**: Dependencies are now grouped by their role in the hexagonal architecture (Infrastructure vs. Presentation).
- **Initialization Clarity**: The boot sequence is now explicitly ordered, preventing "race conditions" where services were requested before their underlying drivers were ready.

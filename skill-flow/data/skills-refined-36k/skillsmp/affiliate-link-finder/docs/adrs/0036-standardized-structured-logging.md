# ADR 0036: Standardized Structured Logging

## Status
Accepted

## Context
Initial development relied on scattered `print`, `debugPrint`, and `log` statements. This made it impossible to filter logs by severity or domain, and critical errors were not consistently captured by production monitoring tools like Firebase Crashlytics. To ensure high-quality diagnostics in production and a clean console during development, a unified logging framework was necessary.

## Decision
We implemented a centralized diagnostic system using the `AppLogger` utility:
1.  **Severity Levels**: Introduced explicit categories for logic tracing:
    -   `d` (Debug): Fine-grained information for development.
    -   `i` (Info): High-level operational events.
    -   `w` (Warning): Potentially harmful situations or fallbacks.
    -   `e` (Error): Critical failures requiring immediate attention + Stack Traces.
2.  **Production Integration**: Configured `AppLogger.e` to automatically forward error messages and exception metadata to **Firebase Crashlytics** when `kReleaseMode` is true.
3.  **Visual Clarity**: Added console emojis (🐛, ℹ️, ⚠️, ❌) to improve dev-time scannability.
4.  **No-Mock Policy**: Enforced that logs must represent real system state, never fallback mock data hidden from the user.

## Consequences
- **Observability**: Production crashes now include the precise "breadcrumb" of Info/Warning logs leading up to the error.
- **Maintainability**: Future developers have a single interface for all diagnostic needs.
- **System Hygiene**: Local console output is no longer cluttered with noise, allowing developers to focus on the active task.

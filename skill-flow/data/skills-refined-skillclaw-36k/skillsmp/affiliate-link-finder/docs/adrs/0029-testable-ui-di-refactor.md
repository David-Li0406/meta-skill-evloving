# ADR 0029: Testable UI & Dependency Injection Refactor

## Status
Accepted

## Context
Widget tests for `InsightsScreen` were flaky and skipped because the screen relied solely on global state (locator) for its ViewModel. This created race conditions during tests where the mock registered in `GetIt` might not be ready or could be disposed of by asynchronous processes within the screen. Additionally, continuous background animations prevented `pumpAndSettle` from completing.

## Decision
We refactored the UI architecture to prioritize testability via explicit dependency injection (DI):

1.  **Optional ViewModel Injection**: Updated `InsightsScreen` to accept an optional `InsightsViewModel` in its constructor.
2.  **Fallback to Locator**: maintained the production convenience of `locator` by having the screen fall back to the locator ONLY if no ViewModel is provided.
3.  **Animation Isolation**: Wrapped loading skeletons and animated components in containers that allow for stable snapshots during tests.
4.  **Mock Standardization**: Standardized the use of `MultiProvider` in tests to ensure that the environment precisely matches production without hitting real network/database layers.

## Consequences
- **Positive**: Bulletproof, non-flaky widget tests; clearly defined dependency boundaries; faster test execution (no reliance on global service locator setup/teardown in every test).
- **Maintenance**: Minor update to screen constructors across the app as this pattern is rolled out.

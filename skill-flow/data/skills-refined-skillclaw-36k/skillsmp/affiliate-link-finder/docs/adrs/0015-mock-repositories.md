# ADR 0015: Mock Repository Pattern for Development

## Status
Accepted

## Context
The app uses Firebase (Auth, Firestore) as the backend, but:
- Firebase requires active internet connection
- Firebase configuration needs real credentials
- Local development benefits from fast, offline data
- Testing shouldn't depend on external services

We needed a way to develop and test without Firebase dependencies.

## Decision
We implemented mock repositories that mirror Firebase repositories' interfaces:

**Mock Repositories Created:**
- `MockSupplementRepository`: Provides hardcoded supplement data
- `MockSymptomRepository`: Returns predefined symptom tracking data
- `MockBillingService`: Simulates subscription states

**Implementation:**
- All repositories implement the same interface (`SupplementRepository`, etc.)
- Dependency injection (`GetIt`) allows switching between mock and real implementations
- Mock data is realistic and comprehensive
- No network calls, instant responses

**Usage:**
```dart
// Development (in locator.dart)
locator.registerLazySingleton<SupplementRepository>(
  () => MockSupplementRepository()
);

// Production (future)
locator.registerLazySingleton<SupplementRepository>(
  () => FirebaseSupplementRepository()
);
```

## Consequences

### Positive
- Fast iteration without Firebase setup
- Offline development fully functional
- Predictable, consistent test data
- Easy to test edge cases with mock data
- No Firebase costs during development

### Negative
- Mock data can diverge from real Firebase data structures
- Need to maintain both mock and real implementations
- Risk of implementing features that don't work with real backend

### Neutral
- Clear migration path to Firebase (same interfaces)
- Mock repositories useful for automated testing
- Dependency injection makes switching trivial

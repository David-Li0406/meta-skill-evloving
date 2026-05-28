# ADR 0009: Repository Pattern for Data Layer

**Date:** 2026-01-19  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The app needs to persist user data (stacks, logs, supplements, user profile) to Firebase Firestore. We needed:
- Abstraction from Firebase implementation details
- Testability via mock repositories
- Consistent async patterns
- Real-time stream support

## Decision

Implement the **Repository Pattern** with interface abstraction.

### Domain Layer (Interfaces)

```dart
// lib/domain/repositories/log_repository.dart
abstract class LogRepository {
  Future<DailyLog?> getLogForDate(String userId, DateTime date);
  Future<void> saveLog(DailyLog log);
  Future<int> getStreakCount(String userId);
  Stream<DailyLog?> watchTodayLog(String userId);
}
```

### Infrastructure Layer (Firebase Implementation)

```dart
// lib/infrastructure/repositories/firebase_log_repository.dart
class FirebaseLogRepository implements LogRepository {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  
  @override
  Future<DailyLog?> getLogForDate(String userId, DateTime date) async {
    final doc = await _firestore
        .collection('users')
        .doc(userId)
        .collection('logs')
        .doc(_dateKey(date))
        .get();
    // ...
  }
}
```

### Repositories Implemented

| Repository | Interface | Implementation |
|------------|-----------|----------------|
| Auth | `AuthRepository` | `FirebaseAuthRepository` |
| Supplements | `SupplementRepository` | `FirebaseSupplementRepository` |
| Stacks | `StackRepository` | `FirebaseStackRepository` |
| Logs | `LogRepository` | `FirebaseLogRepository` |

### DI Registration

```dart
locator.registerLazySingleton<StackRepository>(() => FirebaseStackRepository());
locator.registerLazySingleton<LogRepository>(() => FirebaseLogRepository());
```

## Entity Models

```dart
class DailyLog {
  final String id;
  final String userId;
  final DateTime date;
  final List<LogEntry> entries;
  final Map<String, int>? symptomRatings;
  
  Map<String, dynamic> toJson() => { /* ... */ };
  factory DailyLog.fromJson(Map<String, dynamic> json) => /* ... */;
}
```

## Consequences

**Positive:**
- Swappable implementations (mock for tests)
- Clear async/stream contracts
- Decoupled domain from infrastructure
- Consistent Firestore patterns

**Negative:**
- More files to maintain
- Requires discipline to keep interfaces updated

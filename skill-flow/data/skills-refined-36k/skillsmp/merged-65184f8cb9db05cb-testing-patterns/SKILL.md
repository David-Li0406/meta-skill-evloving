---
name: testing-patterns
description: Use this skill when you need to implement and understand various testing patterns, including unit, integration, and widget tests, along with mocking strategies.
---

# Testing Patterns

## Overview

This document outlines principles and patterns for creating reliable test suites, including unit tests, integration tests, widget tests, and mocking strategies.

## 1. Testing Pyramid

```
        /\          E2E (Few)
       /  \         Critical flows
      /----\
     /      \       Integration (Some)
    /--------\      API, DB queries
   /          \
  /------------\    Unit (Many)
                    Functions, classes
```

## 2. AAA Pattern

| Step        | Purpose                 |
| ----------- | ----------------------- |
| **Arrange** | Set up test data        |
| **Act**     | Execute code under test |
| **Assert**  | Verify outcome          |

## 3. Test Type Selection

### When to Use Each

| Type            | Best For              | Speed        |
| --------------- | --------------------- | ------------ |
| **Unit**        | Pure functions, logic | Fast (<50ms) |
| **Integration** | API, DB, services     | Medium       |
| **E2E**         | Critical user flows   | Slow         |

## 4. Unit Test Principles

### Good Unit Tests

| Principle     | Meaning                |
| ------------- | ---------------------- |
| Fast          | < 100ms each           |
| Isolated      | No external deps       |
| Repeatable    | Same result always     |
| Self-checking | No manual verification |
| Timely        | Written with code      |

### What to Unit Test

| Test           | Don't Test       |
| -------------- | ---------------- |
| Business logic | Framework code   |
| Edge cases     | Third-party libs |
| Error handling | Simple getters   |

## 5. Integration Test Principles

### What to Test

| Area              | Focus                 |
| ----------------- | --------------------- |
| API endpoints     | Request/response      |
| Database          | Queries, transactions |
| External services | Contracts             |

### Setup/Teardown

| Phase       | Action            |
| ----------- | ----------------- |
| Before All  | Connect resources |
| Before Each | Reset state       |
| After Each  | Clean up          |
| After All   | Disconnect        |

## 6. Mocking Principles

### When to Mock

| Mock            | Don't Mock          |
| --------------- | ------------------- |
| External APIs   | The code under test |
| Database (unit) | Simple dependencies |
| Time/random     | Pure functions      |
| Network         | In-memory stores    |

### Mock Types

| Type | Use                       |
| ---- | ------------------------- |
| Stub | Return fixed values       |
| Spy  | Track calls               |
| Mock | Set expectations          |
| Fake | Simplified implementation |

## 7. Test Organization

### Naming

| Pattern         | Example                       |
| --------------- | ----------------------------- |
| Should behavior | "should return error when..." |
| When condition  | "when user not found..."      |
| Given-when-then | "given X, when Y, then Z"     |

### Grouping

| Level      | Use                 |
| ---------- | ------------------- |
| describe   | Group related tests |
| it/test    | Individual case     |
| beforeEach | Common setup        |

## 8. Test Data

### Strategies

| Approach  | Use                    |
| --------- | ---------------------- |
| Factories | Generate test data     |
| Fixtures  | Predefined datasets    |
| Builders  | Fluent object creation |

### Principles

- Use realistic data
- Randomize non-essential values (faker)
- Share common fixtures
- Keep data minimal

## 9. Best Practices

| Practice            | Why                  |
| ------------------- | -------------------- |
| One assert per test | Clear failure reason |
| Independent tests   | No order dependency  |
| Fast tests          | Run frequently       |
| Descriptive names   | Self-documenting     |
| Clean up            | Avoid side effects   |

## 10. Anti-Patterns

| ❌ Don't            | ✅ Do             |
| ------------------- | ----------------- |
| Test implementation | Test behavior     |
| Duplicate test code | Use factories     |
| Complex test setup  | Simplify or split |
| Ignore flaky tests  | Fix root cause    |
| Skip cleanup        | Reset state       |

## 11. Example Implementations

### Unit Tests (Domain & Data Layers)

#### Use Case Testing

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dartz/dartz.dart';

class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUser useCase;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    useCase = GetUser(mockRepository);
  });

  group('GetUser', () {
    final tUser = User(
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      createdAt: DateTime(2024),
    );

    test('should return user when repository call is successful', () async {
      // Arrange
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) async => Right(tUser));

      // Act
      final result = await useCase('1');

      // Assert
      expect(result, Right(tUser));
      verify(() => mockRepository.getUser('1')).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return ServerFailure when repository fails', () async {
      // Arrange
      when(() => mockRepository.getUser('1'))
          .thenAnswer((_) async => Left(ServerFailure('Error')));

      // Act
      final result = await useCase('1');

      // Assert
      expect(result, isA<Left>());
      verify(() => mockRepository.getUser('1')).called(1);
    });
  });
}
```

### Widget Tests

```dart
void main() {
  testWidgets('UserPage displays loading indicator', (tester) async {
    // Arrange
    final mockController = MockUserController();
    when(() => mockController.isLoading).thenReturn(true);
    when(() => mockController.user).thenReturn(null);
    when(() => mockController.error).thenReturn(null);
    
    Get.put<UserController>(mockController);

    // Act
    await tester.pumpWidget(
      GetMaterialApp(home: UserPage()),
    );

    // Assert
    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    
    // Cleanup
    Get.delete<UserController>();
  });
}
```

### Integration Tests

```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('User Flow Integration Tests', () {
    testWidgets('complete user login flow', (tester) async {
      // Start app
      await tester.pumpWidget(MyApp());
      await tester.pumpAndSettle();

      // Navigate to login
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle();

      // Enter credentials
      await tester.enterText(find.byType(TextField).at(0), 'test@example.com');
      await tester.enterText(find.byType(TextField).at(1), 'password');
      await tester.pumpAndSettle();

      // Submit
      await tester.tap(find.text('Submit'));
      await tester.pumpAndSettle();

      // Verify navigation to home
      expect(find.text('Home'), findsOneWidget);
    });
  });
}
```

### Golden Tests

```dart
void main() {
  testWidgets('UserCard golden test', (tester) async {
    final tUser = User(
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: DateTime(2024),
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: UserCard(user: tUser),
        ),
      ),
    );

    await expectLater(
      find.byType(UserCard),
      matchesGoldenFile('goldens/user_card.png'),
    );
  });
}
```

> **Remember:** Tests are documentation. If someone can't understand what the code does from the tests, rewrite them.
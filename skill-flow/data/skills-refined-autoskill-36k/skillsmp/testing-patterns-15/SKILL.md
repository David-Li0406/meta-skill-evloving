---
name: "Testing Patterns"
description: "Unit, widget, integration, and golden test patterns with mocking strategies"
version: "1.0.0"
---

# Testing Patterns

## Unit Tests (Domain & Data Layers)

### Use Case Testing

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

### Repository Testing

```dart
class MockUserProvider extends Mock implements UserProvider {}
class MockUserLocalSource extends Mock implements UserLocalSource {}
class MockNetworkInfo extends Mock implements NetworkInfo {}

void main() {
  late UserRepositoryImpl repository;
  late MockUserProvider mockProvider;
  late MockUserLocalSource mockLocalSource;
  late MockNetworkInfo mockNetworkInfo;

  setUp(() {
    mockProvider = MockUserProvider();
    mockLocalSource = MockUserLocalSource();
    mockNetworkInfo = MockNetworkInfo();
    repository = UserRepositoryImpl(
      mockProvider,
      mockLocalSource,
      mockNetworkInfo,
    );
  });

  group('getUser', () {
    final tUserModel = UserModel(
      id: '1',
      name: 'Test',
      email: 'test@example.com',
      createdAt: DateTime(2024),
    );

    test('should return remote data when online', () async {
      // Arrange
      when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => true);
      when(() => mockProvider.fetchUser('1'))
          .thenAnswer((_) async => tUserModel);
      when(() => mockLocalSource.cacheUser(tUserModel))
          .thenAnswer((_) async => {});

      // Act
      final result = await repository.getUser('1');

      // Assert
      verify(() => mockProvider.fetchUser('1'));
      verify(() => mockLocalSource.cacheUser(tUserModel));
      expect(result, Right(tUserModel.toEntity()));
    });

    test('should return cached data when offline', () async {
      // Arrange
      when(() => mockNetworkInfo.isConnected).thenAnswer((_) async => false);
      when(() => mockLocalSource.getCachedUser('1'))
          .thenAnswer((_) async => tUserModel);

      // Act
      final result = await repository.getUser('1');

      // Assert
      verify(() => mockLocalSource.getCachedUser('1'));
      verifyNever(() => mockProvider.fetchUser('1'));
      expect(result, Right(tUserModel.toEntity()));
    });
  });
}
```

### Controller Testing

```dart
class MockGetUser extends Mock implements GetUser {}

void main() {
  late UserController controller;
  late MockGetUser mockGetUser;

  setUp(() {
    mockGetUser = MockGetUser();
    controller = UserController(getUserUseCase: mockGetUser);
  });

  tearDown(() {
    controller.dispose();
  });

  group('UserController', () {
    final tUser = User(
      id: '1',
      name: 'Test',
      email: 'test@example.com',
      createdAt: DateTime(2024),
    );

    test('initial state should be empty', () {
      expect(controller.user, null);
      expect(controller.isLoading, false);
      expect(controller.error, null);
    });

    test('should load user successfully', () async {
      // Arrange
      when(() => mockGetUser('1')).thenAnswer((_) async => Right(tUser));

      // Act
      await controller.loadUser('1');

      // Assert
      expect(controller.user, tUser);
      expect(controller.isLoading, false);
      expect(controller.error, null);
    });

    test('should handle error', () async {
      // Arrange
      when(() => mockGetUser('1'))
          .thenAnswer((_) async => Left(ServerFailure('Error')));

      // Act
      await controller.loadUser('1');

      // Assert
      expect(controller.user, null);
      expect(controller.isLoading, false);
      expect(controller.error, isNotNull);
    });
  });
}
```

## Widget Tests

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

  testWidgets('UserPage displays user data', (tester) async {
    // Arrange
    final tUser = User(
      id: '1',
      name: 'John Doe',
      email: 'john@example.com',
      createdAt: DateTime(2024),
    );
    
    final mockController = MockUserController();
    when(() => mockController.isLoading).thenReturn(false);
    when(() => mockController.user).thenReturn(tUser);
    when(() => mockController.error).thenReturn(null);
    
    Get.put<UserController>(mockController);

    // Act
    await tester.pumpWidget(
      GetMaterialApp(home: UserPage()),
    );

    // Assert
    expect(find.text('John Doe'), findsOneWidget);
    expect(find.text('john@example.com'), findsOneWidget);
    
    // Cleanup
    Get.delete<UserController>();
  });

  testWidgets('UserPage displays error', (tester) async {
    // Arrange
    final mockController = MockUserController();
    when(() => mockController.isLoading).thenReturn(false);
    when(() => mockController.user).thenReturn(null);
    when(() => mockController.error).thenReturn('Server error');
    
    Get.put<UserController>(mockController);

    // Act
    await tester.pumpWidget(
      GetMaterialApp(home: UserPage()),
    );

    // Assert
    expect(find.text('Server error'), findsOneWidget);
    expect(find.byIcon(Icons.error_outline), findsOneWidget);
    
    // Cleanup
    Get.delete<UserController>();
  });
}
```

## Integration Tests

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

## Golden Tests

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

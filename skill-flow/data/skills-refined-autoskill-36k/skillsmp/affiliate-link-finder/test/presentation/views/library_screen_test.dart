import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/views/library_screen.dart';
import 'package:provider/provider.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/domain/repositories/auth_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/mock_supplement_repository.dart';
import 'package:adhd_supplement_app/infrastructure/repositories/mock_stack_repository.dart';
import 'package:adhd_supplement_app/config/locator.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Simple mock AuthRepository that doesn't use plugins
class MockAuthRepository implements AuthRepository {
  @override
  Stream<User?> authStateChanges() {
    final testUser = User(
      id: 'test-user',
      email: 'test@example.com',
      createdAt: DateTime.now(),
    );
    return Stream.value(testUser);
  }

  @override
  Future<User> signInWithEmail(String email, String password) async {
    throw UnimplementedError();
  }

  @override
  Future<User> signUpWithEmail(
      String email, String password, String displayName) async {
    throw UnimplementedError();
  }

  @override
  Future<User> signInAnonymously() async {
    throw UnimplementedError();
  }

  @override
  Future<void> signOut() async {
    throw UnimplementedError();
  }

  @override
  Future<User?> getCurrentUser() async {
    throw UnimplementedError();
  }

  @override
  Future<void> updateUserProfile(User user) async {
    throw UnimplementedError();
  }

  @override
  Future<void> deleteUser() async {
    throw UnimplementedError();
  }
}

void main() {
  setUpAll(() {
    // Mock SharedPreferences
    SharedPreferences.setMockInitialValues({});
  });

  setUp(() async {
    // Initialize the locator with test dependencies
    await setupLocator();
    // Replace Firebase supplement repository with mock
    locator.unregister<SupplementRepository>();
    locator.registerLazySingleton<SupplementRepository>(
        () => const MockSupplementRepository());
    // Replace Firebase stack repository with mock
    locator.unregister<StackRepository>();
    locator.registerLazySingleton<StackRepository>(() => MockStackRepository());
  });

  Widget createScreen() {
    // Create a simple mock AuthRepository without platform dependencies
    final mockAuthRepo = MockAuthRepository();

    // Create AuthProvider with mock repository
    final authProvider = AuthProvider(mockAuthRepo);

    return MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: authProvider),
      ],
      child: const MaterialApp(
        home: LibraryScreen(),
      ),
    );
  }

  testWidgets('LibraryScreen renders correctly', (WidgetTester tester) async {
    await tester.pumpWidget(createScreen());

    // Wait for view model to initialize and load data
    await tester.pumpAndSettle(const Duration(milliseconds: 600));

    // Verify header elements
    expect(find.text('LIBRARY'), findsOneWidget);
    expect(find.byIcon(Icons.arrow_back), findsOneWidget);
    expect(find.byIcon(Icons.bookmark_outline), findsOneWidget);

    // Verify status toggle
    expect(find.text('Recommended'), findsOneWidget);
    expect(find.text('Avoid List'), findsOneWidget);

    // Verify search bar
    expect(find.byIcon(Icons.search), findsOneWidget);
    expect(find.byIcon(Icons.tune), findsOneWidget);
  });
}

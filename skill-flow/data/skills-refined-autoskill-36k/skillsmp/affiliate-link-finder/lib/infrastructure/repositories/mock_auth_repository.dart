import 'dart:async';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';

class MockAuthRepository implements AuthRepository {
  final _authStateController = StreamController<User?>.broadcast();
  User? _currentUser;

  MockAuthRepository() {
    // Initial state: unauthenticated
    _authStateController.add(null);
  }

  @override
  Future<User?> getCurrentUser() async {
    return _currentUser;
  }

  @override
  Future<User> signInWithEmail(String email, String password) async {
    await Future<void>.delayed(const Duration(milliseconds: 500));
    _currentUser = User(
      id: 'mock-user-123',
      email: email,
      displayName: 'Mock User',
      createdAt: DateTime.now(),
      hasCompletedOnboarding: true,
    );
    _authStateController.add(_currentUser);
    return _currentUser!;
  }

  @override
  Future<User> signUpWithEmail(
      String email, String password, String displayName) async {
    await Future<void>.delayed(const Duration(milliseconds: 500));
    _currentUser = User(
      id: 'mock-user-123',
      email: email,
      displayName: displayName,
      createdAt: DateTime.now(),
      hasCompletedOnboarding: false,
    );
    _authStateController.add(_currentUser);
    return _currentUser!;
  }

  @override
  Future<void> signOut() async {
    _currentUser = null;
    _authStateController.add(null);
  }

  @override
  Stream<User?> authStateChanges() async* {
    yield _currentUser;
    yield* _authStateController.stream;
  }

  @override
  Future<void> updateUserProfile(User user) async {
    _currentUser = user;
    _authStateController.add(_currentUser);
  }

  @override
  Future<void> deleteUser() async {
    _currentUser = null;
    _authStateController.add(null);
  }

  @override
  Future<User> signInAnonymously() async {
    await Future<void>.delayed(const Duration(milliseconds: 200));
    _currentUser = User(
      id: 'mock-anonymous-user',
      email: 'anonymous@dev.mode',
      displayName: 'Guest Hero',
      createdAt: DateTime.now(),
      hasCompletedOnboarding: true,
    );
    _authStateController.add(_currentUser);
    return _currentUser!;
  }

  void dispose() {
    _authStateController.close();
  }
}

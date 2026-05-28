import '../entities/user.dart';

abstract class AuthRepository {
  /// Get the current authenticated user
  Future<User?> getCurrentUser();

  /// Sign in with email and password
  Future<User> signInWithEmail(String email, String password);

  /// Sign up with email and password
  Future<User> signUpWithEmail(
      String email, String password, String displayName);

  /// Sign out
  Future<void> signOut();

  /// Stream of auth state changes
  Stream<User?> authStateChanges();

  /// Update user profile
  Future<void> updateUserProfile(User user);

  /// Sign in anonymously (Dev Mode bypass)
  Future<User> signInAnonymously();

  /// Delete user account
  Future<void> deleteUser();
}

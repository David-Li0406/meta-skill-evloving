import 'package:firebase_auth/firebase_auth.dart' as firebase_auth;
import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../utils/logger.dart';

class FirebaseAuthRepository implements AuthRepository {
  final firebase_auth.FirebaseAuth _firebaseAuth;
  final FirebaseFirestore _firestore;

  FirebaseAuthRepository({
    firebase_auth.FirebaseAuth? firebaseAuth,
    FirebaseFirestore? firestore,
  })  : _firebaseAuth = firebaseAuth ?? firebase_auth.FirebaseAuth.instance,
        _firestore = firestore ?? FirebaseFirestore.instance;

  @override
  Future<User?> getCurrentUser() async {
    final firebaseUser = _firebaseAuth.currentUser;
    if (firebaseUser == null) return null;

    // Try to get user data from Firestore
    try {
      final doc =
          await _firestore.collection('users').doc(firebaseUser.uid).get();
      if (doc.exists) {
        return User.fromJson(doc.data()!);
      }
    } catch (e) {
      // Fall back to Firebase Auth data
    }

    return _mapFirebaseUser(firebaseUser);
  }

  @override
  Future<User> signInWithEmail(String email, String password) async {
    try {
      final credential = await _firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Sign in failed');
      }

      // Get user data from Firestore
      final doc =
          await _firestore.collection('users').doc(credential.user!.uid).get();
      if (doc.exists) {
        return User.fromJson(doc.data()!);
      }

      return _mapFirebaseUser(credential.user!);
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _mapAuthException(e);
    }
  }

  @override
  Future<User> signUpWithEmail(
      String email, String password, String displayName) async {
    try {
      final credential = await _firebaseAuth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );

      if (credential.user == null) {
        throw Exception('Sign up failed');
      }

      // Update display name
      await credential.user!.updateDisplayName(displayName);

      final user = User(
        id: credential.user!.uid,
        email: email,
        displayName: displayName,
        createdAt: DateTime.now(),
        hasCompletedOnboarding: false,
      );

      // Save to Firestore
      await _firestore.collection('users').doc(user.id).set(user.toJson());

      return user;
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _mapAuthException(e);
    }
  }

  @override
  Future<void> signOut() async {
    await _firebaseAuth.signOut();
  }

  @override
  Stream<User?> authStateChanges() {
    return _firebaseAuth.authStateChanges().asyncMap((firebaseUser) async {
      if (firebaseUser == null) return null;

      try {
        final doc = await _firestore
            .collection('users')
            .doc(firebaseUser.uid)
            .get(const GetOptions(source: Source.serverAndCache))
            .timeout(const Duration(seconds: 3));
        if (doc.exists) {
          return User.fromJson(doc.data()!);
        }
      } catch (e) {
        // Fall back to local cache if server is slow
        AppLogger.w('Firestore server fetch timed out, trying cache', e);
        try {
          final doc = await _firestore
              .collection('users')
              .doc(firebaseUser.uid)
              .get(const GetOptions(source: Source.cache));
          if (doc.exists) {
            return User.fromJson(doc.data()!);
          }
        } catch (cacheErr) {
          AppLogger.e('Firestore cache fetch failed', cacheErr);
        }
      }

      return _mapFirebaseUser(firebaseUser);
    });
  }

  @override
  Future<void> updateUserProfile(User user) async {
    await _firestore
        .collection('users')
        .doc(user.id)
        .set(user.toJson(), SetOptions(merge: true));
  }

  @override
  Future<void> deleteUser() async {
    final user = _firebaseAuth.currentUser;
    if (user == null) {
      throw Exception('No user signed in');
    }

    // Delete from Firestore
    await _firestore.collection('users').doc(user.uid).delete();

    // Delete from Firebase Auth
    // Note: This requires recent login. If it fails with 'requires-recent-login',
    // the UI should prompt to re-authenticate.
    await user.delete();
  }

  @override
  Future<User> signInAnonymously() async {
    try {
      final credential = await _firebaseAuth.signInAnonymously();

      if (credential.user == null) {
        throw Exception('Anonymous sign in failed');
      }

      // Check if user already exists in Firestore
      final doc =
          await _firestore.collection('users').doc(credential.user!.uid).get();
      if (doc.exists) {
        return User.fromJson(doc.data()!);
      }

      // Create a temporary user profile
      final user = User(
        id: credential.user!.uid,
        email: 'anonymous@dev.mode',
        displayName: 'Guest Hero',
        createdAt: DateTime.now(),
        hasCompletedOnboarding: true,
      );

      // Save to Firestore so other repositories can find it
      await _firestore.collection('users').doc(user.id).set(user.toJson());

      return user;
    } on firebase_auth.FirebaseAuthException catch (e) {
      throw _mapAuthException(e);
    }
  }

  User _mapFirebaseUser(firebase_auth.User firebaseUser) {
    return User(
      id: firebaseUser.uid,
      email: firebaseUser.email!,
      displayName: firebaseUser.displayName,
      photoUrl: firebaseUser.photoURL,
      createdAt: firebaseUser.metadata.creationTime ?? DateTime.now(),
    );
  }

  String _mapAuthException(firebase_auth.FirebaseAuthException e) {
    switch (e.code) {
      case 'user-not-found':
        return 'No user found with this email.';
      case 'wrong-password':
        return 'Wrong password.';
      case 'email-already-in-use':
        return 'An account already exists with this email.';
      case 'weak-password':
        return 'Password is too weak.';
      case 'invalid-email':
        return 'Invalid email address.';
      case 'admin-restricted-operation':
      case 'operation-not-allowed':
        return 'Anonymous login is disabled. Please enable it in Firebase Console -> Authentication -> Sign-in method.';
      default:
        return e.message ?? 'Authentication failed.';
    }
  }
}

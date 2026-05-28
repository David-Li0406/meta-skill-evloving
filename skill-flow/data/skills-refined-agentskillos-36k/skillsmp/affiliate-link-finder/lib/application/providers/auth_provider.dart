import 'package:flutter/foundation.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/services/billing_service.dart';
import '../../utils/logger.dart';

enum AuthStatus { initial, authenticated, unauthenticated }

class AuthProvider extends ChangeNotifier {
  final AuthRepository _authRepository;
  final BillingService _billingService;

  User? _user;
  AuthStatus _status = AuthStatus.initial;
  String? _errorMessage;

  AuthProvider(this._authRepository, this._billingService) {
    _initialize();
  }

  User? get user => _user;
  AuthStatus get status => _status;
  String? get errorMessage => _errorMessage;
  bool get isAuthenticated => _status == AuthStatus.authenticated;

  void _initialize() {
    _authRepository.authStateChanges().listen((user) async {
      _user = user;
      _status =
          user != null ? AuthStatus.authenticated : AuthStatus.unauthenticated;

      if (_user != null) {
        await refreshEntitlements();
      }

      notifyListeners();
    });
  }

  Future<void> refreshEntitlements() async {
    if (_user == null) return;
    try {
      final entitlements = await _billingService.getEntitlements();
      _user = _user!.copyWith(activeEntitlements: entitlements);
      notifyListeners();
    } catch (e) {
      AppLogger.e('Failed to refresh entitlements', e);
    }
  }

  bool canAccess(String entitlementId) {
    return _user?.activeEntitlements.contains(entitlementId) ?? false;
  }

  bool get isPremium => canAccess('pro');

  Future<void> signIn(String email, String password) async {
    try {
      _errorMessage = null;
      notifyListeners();

      _user = await _authRepository.signInWithEmail(email, password);
      _status = AuthStatus.authenticated;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _status = AuthStatus.unauthenticated;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> signUp(String email, String password, String displayName) async {
    try {
      _errorMessage = null;
      notifyListeners();

      _user =
          await _authRepository.signUpWithEmail(email, password, displayName);
      _status = AuthStatus.authenticated;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _status = AuthStatus.unauthenticated;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> signInAnonymously() async {
    try {
      _errorMessage = null;
      notifyListeners();

      _user = await _authRepository.signInAnonymously();
      _status = AuthStatus.authenticated;
      notifyListeners();
    } catch (e) {
      _errorMessage = e.toString();
      _status = AuthStatus.unauthenticated;
      notifyListeners();
      rethrow;
    }
  }

  Future<void> signOut() async {
    await _authRepository.signOut();
    _user = null;
    _status = AuthStatus.unauthenticated;
    _errorMessage = null;
    notifyListeners();
  }

  Future<void> updateProfile(User user) async {
    await _authRepository.updateUserProfile(user);
    _user = user;
    notifyListeners();
  }
}

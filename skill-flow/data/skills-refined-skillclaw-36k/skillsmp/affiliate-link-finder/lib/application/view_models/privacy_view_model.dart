import 'package:flutter/foundation.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/repositories/log_repository.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../config/locator.dart';

class PrivacyViewModel extends ChangeNotifier {
  final AuthRepository _authRepository = locator<AuthRepository>();
  final SettingsRepository _settingsRepository = locator<SettingsRepository>();
  // ignore: unused_field
  final LogRepository _logRepository = locator<LogRepository>();

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  bool _biometricLockEnabled = false;
  bool get biometricLockEnabled => _biometricLockEnabled;

  bool _localStorageOnly = true;
  bool get localStorageOnly => _localStorageOnly;

  bool _analyticsEnabled = false;
  bool get analyticsEnabled => _analyticsEnabled;

  bool _crashReportingEnabled = false;
  bool get crashReportingEnabled => _crashReportingEnabled;

  String? _error;
  String? get error => _error;

  PrivacyViewModel() {
    _loadSettings();
  }

  void _loadSettings() {
    _biometricLockEnabled = _settingsRepository.getBiometricLockEnabled();
    _localStorageOnly = _settingsRepository.getLocalStorageOnly();
    _analyticsEnabled = _settingsRepository.getAnalyticsEnabled();
    _crashReportingEnabled = _settingsRepository.getCrashReportingEnabled();
    notifyListeners();
  }

  Future<void> setBiometricLockEnabled(bool value) async {
    _biometricLockEnabled = value;
    await _settingsRepository.setBiometricLockEnabled(value);
    notifyListeners();
  }

  Future<void> setLocalStorageOnly(bool value) async {
    _localStorageOnly = value;
    await _settingsRepository.setLocalStorageOnly(value);
    notifyListeners();
  }

  Future<void> setAnalyticsEnabled(bool value) async {
    _analyticsEnabled = value;
    await _settingsRepository.setAnalyticsEnabled(value);
    notifyListeners();
  }

  Future<void> setCrashReportingEnabled(bool value) async {
    _crashReportingEnabled = value;
    await _settingsRepository.setCrashReportingEnabled(value);
    notifyListeners();
  }

  Future<void> downloadData() async {
    _setLoading(true);
    _error = null;
    try {
      // Simulate data generation time
      await Future<void>.delayed(const Duration(seconds: 2));
      // In a real app, this would generate a CSV/PDF and share it
    } catch (e) {
      _error = 'Failed to generate data export.';
    } finally {
      _setLoading(false);
    }
  }

  Future<void> deleteAccount() async {
    _setLoading(true);
    _error = null;
    try {
      final user = await _authRepository.getCurrentUser();
      if (user != null) {
        await _logRepository.clearAllLogs(user.id);
      }
      await _authRepository.deleteUser();
      // App should navigate to login/onboarding after this
    } catch (e) {
      _error = 'Failed to delete account. Please try again.';
    } finally {
      _setLoading(false);
    }
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
}

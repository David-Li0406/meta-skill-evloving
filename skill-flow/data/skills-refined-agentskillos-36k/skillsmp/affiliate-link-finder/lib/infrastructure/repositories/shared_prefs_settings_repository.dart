import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../domain/repositories/settings_repository.dart';

class SharedPrefsSettingsRepository implements SettingsRepository {
  final SharedPreferences _prefs;

  SharedPrefsSettingsRepository(this._prefs);

  // Keys
  static const String _keyNudgeEnabled = 'nudge_enabled';
  static const String _keyNudgeHour = 'nudge_hour';
  static const String _keyNudgeMinute = 'nudge_minute';
  static const String _keyWarningOption = 'warning_option';
  static const String _keyExtendedEnabled = 'extended_enabled';
  static const String _keyThemeMode = 'theme_mode';
  static const String _keyReducedMotion = 'reduced_motion_enabled';
  static const String _keyHapticFeedback = 'haptic_feedback_enabled';
  static const String _keyFontSizeScale = 'font_size_scale';
  static const String _keyAcceptedDisclaimer = 'accepted_medical_disclaimer';

  @override
  Future<void> init() async {
    // Already initialized via constructor in this implementation
  }

  @override
  bool getNudgeModeEnabled() {
    return _prefs.getBool(_keyNudgeEnabled) ?? true; // Default true
  }

  @override
  Future<void> setNudgeModeEnabled(bool enabled) async {
    await _prefs.setBool(_keyNudgeEnabled, enabled);
  }

  @override
  TimeOfDay getNudgeTime() {
    final hour = _prefs.getInt(_keyNudgeHour) ?? 8; // Default 8:00 AM
    final minute = _prefs.getInt(_keyNudgeMinute) ?? 0;
    return TimeOfDay(hour: hour, minute: minute);
  }

  @override
  Future<void> setNudgeTime(TimeOfDay time) async {
    await _prefs.setInt(_keyNudgeHour, time.hour);
    await _prefs.setInt(_keyNudgeMinute, time.minute);
  }

  @override
  TimeOfDay getSlotTime(String slot) {
    final hour = _prefs.getInt('slot_${slot}_hour');
    final minute = _prefs.getInt('slot_${slot}_minute');

    if (hour != null && minute != null) {
      return TimeOfDay(hour: hour, minute: minute);
    }

    // Default times
    switch (slot.toLowerCase()) {
      case 'morning':
        return const TimeOfDay(hour: 8, minute: 0);
      case 'afternoon':
        return const TimeOfDay(hour: 13, minute: 0);
      case 'evening':
        return const TimeOfDay(hour: 18, minute: 0);
      case 'night':
        return const TimeOfDay(hour: 21, minute: 0);
      default:
        return const TimeOfDay(hour: 8, minute: 0);
    }
  }

  @override
  Future<void> setSlotTime(String slot, TimeOfDay time) async {
    await _prefs.setInt('slot_${slot}_hour', time.hour);
    await _prefs.setInt('slot_${slot}_minute', time.minute);
  }

  @override
  String getWarningNudgeOption() {
    return _prefs.getString(_keyWarningOption) ?? '15m';
  }

  @override
  Future<void> setWarningNudgeOption(String option) async {
    await _prefs.setString(_keyWarningOption, option);
  }

  @override
  bool getExtendedRemindersEnabled() {
    return _prefs.getBool(_keyExtendedEnabled) ?? true;
  }

  @override
  Future<void> setExtendedRemindersEnabled(bool enabled) async {
    await _prefs.setBool(_keyExtendedEnabled, enabled);
  }

  // Privacy Settings
  static const String _keyBiometricEnabled = 'biometric_enabled';
  static const String _keyLocalStorageOnly = 'local_storage_only';
  static const String _keyAnalyticsEnabled = 'analytics_enabled';
  static const String _keyCrashReportingEnabled = 'crash_reporting_enabled';

  @override
  bool getBiometricLockEnabled() {
    return _prefs.getBool(_keyBiometricEnabled) ?? false;
  }

  @override
  Future<void> setBiometricLockEnabled(bool enabled) async {
    await _prefs.setBool(_keyBiometricEnabled, enabled);
  }

  @override
  bool getLocalStorageOnly() {
    return _prefs.getBool(_keyLocalStorageOnly) ?? true;
  }

  @override
  Future<void> setLocalStorageOnly(bool enabled) async {
    await _prefs.setBool(_keyLocalStorageOnly, enabled);
  }

  @override
  bool getAnalyticsEnabled() {
    return _prefs.getBool(_keyAnalyticsEnabled) ?? false;
  }

  @override
  Future<void> setAnalyticsEnabled(bool enabled) async {
    await _prefs.setBool(_keyAnalyticsEnabled, enabled);
  }

  @override
  bool getCrashReportingEnabled() {
    return _prefs.getBool(_keyCrashReportingEnabled) ?? false;
  }

  @override
  Future<void> setCrashReportingEnabled(bool enabled) async {
    await _prefs.setBool(_keyCrashReportingEnabled, enabled);
  }

  @override
  ThemeMode getThemeMode() {
    final index = _prefs.getInt(_keyThemeMode) ?? ThemeMode.system.index;
    return ThemeMode.values[index];
  }

  @override
  Future<void> setThemeMode(ThemeMode mode) async {
    await _prefs.setInt(_keyThemeMode, mode.index);
  }

  @override
  bool getReducedMotionEnabled() {
    return _prefs.getBool(_keyReducedMotion) ?? false;
  }

  @override
  Future<void> setReducedMotionEnabled(bool enabled) async {
    await _prefs.setBool(_keyReducedMotion, enabled);
  }

  @override
  bool getHapticFeedbackEnabled() {
    return _prefs.getBool(_keyHapticFeedback) ?? true;
  }

  @override
  Future<void> setHapticFeedbackEnabled(bool enabled) async {
    await _prefs.setBool(_keyHapticFeedback, enabled);
  }

  @override
  double getFontSizeScale() {
    return _prefs.getDouble(_keyFontSizeScale) ?? 1.0;
  }

  @override
  Future<void> setFontSizeScale(double scale) async {
    await _prefs.setDouble(_keyFontSizeScale, scale);
  }

  @override
  bool hasAcceptedDisclaimer() {
    return _prefs.getBool(_keyAcceptedDisclaimer) ?? false;
  }

  @override
  Future<void> setAcceptedDisclaimer(bool accepted) async {
    await _prefs.setBool(_keyAcceptedDisclaimer, accepted);
  }
}

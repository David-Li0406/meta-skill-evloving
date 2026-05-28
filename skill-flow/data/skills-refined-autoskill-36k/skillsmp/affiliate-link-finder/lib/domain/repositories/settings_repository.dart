import 'package:flutter/material.dart';

abstract class SettingsRepository {
  Future<void> init();

  // Notification Settings
  bool getNudgeModeEnabled();
  Future<void> setNudgeModeEnabled(bool enabled);

  TimeOfDay getNudgeTime();
  Future<void> setNudgeTime(TimeOfDay time);

  TimeOfDay getSlotTime(String slot);
  Future<void> setSlotTime(String slot, TimeOfDay time);

  String getWarningNudgeOption();
  Future<void> setWarningNudgeOption(String option);

  bool getExtendedRemindersEnabled();
  Future<void> setExtendedRemindersEnabled(bool enabled);

  // Privacy Settings
  bool getBiometricLockEnabled();
  Future<void> setBiometricLockEnabled(bool enabled);

  bool getLocalStorageOnly();
  Future<void> setLocalStorageOnly(bool enabled);

  bool getAnalyticsEnabled();
  Future<void> setAnalyticsEnabled(bool enabled);

  bool getCrashReportingEnabled();
  Future<void> setCrashReportingEnabled(bool enabled);

  // App Settings
  ThemeMode getThemeMode();
  Future<void> setThemeMode(ThemeMode mode);

  // Accessibility Settings
  bool getReducedMotionEnabled();
  Future<void> setReducedMotionEnabled(bool enabled);

  bool getHapticFeedbackEnabled();
  Future<void> setHapticFeedbackEnabled(bool enabled);

  double getFontSizeScale();
  Future<void> setFontSizeScale(double scale);

  // Compliance
  bool hasAcceptedDisclaimer();
  Future<void> setAcceptedDisclaimer(bool accepted);
}

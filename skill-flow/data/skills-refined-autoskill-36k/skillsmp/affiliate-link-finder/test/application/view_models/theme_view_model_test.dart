import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/application/view_models/theme_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';

class MockSettingsRepository implements SettingsRepository {
  ThemeMode themeMode = ThemeMode.system;

  @override
  Future<void> init() async {}

  @override
  ThemeMode getThemeMode() => themeMode;

  @override
  Future<void> setThemeMode(ThemeMode mode) async {
    themeMode = mode;
  }

  // Other methods not needed for this test

  @override
  bool getNudgeModeEnabled() => false;
  @override
  Future<void> setNudgeModeEnabled(bool enabled) async {}

  @override
  TimeOfDay getNudgeTime() => const TimeOfDay(hour: 8, minute: 0);
  @override
  Future<void> setNudgeTime(TimeOfDay time) async {}

  @override
  String getWarningNudgeOption() => '15m';
  @override
  Future<void> setWarningNudgeOption(String option) async {}

  @override
  TimeOfDay getSlotTime(String slot) => const TimeOfDay(hour: 8, minute: 0);
  @override
  Future<void> setSlotTime(String slot, TimeOfDay time) async {}

  @override
  bool getExtendedRemindersEnabled() => false;
  @override
  Future<void> setExtendedRemindersEnabled(bool enabled) async {}

  @override
  bool getBiometricLockEnabled() => false;
  @override
  Future<void> setBiometricLockEnabled(bool enabled) async {}

  @override
  bool getLocalStorageOnly() => false;
  @override
  Future<void> setLocalStorageOnly(bool enabled) async {}

  @override
  bool getAnalyticsEnabled() => true;
  @override
  Future<void> setAnalyticsEnabled(bool enabled) async {}

  @override
  bool getCrashReportingEnabled() => true;
  @override
  Future<void> setCrashReportingEnabled(bool enabled) async {}

  @override
  bool getReducedMotionEnabled() => false;
  @override
  Future<void> setReducedMotionEnabled(bool enabled) async {}

  @override
  bool getHapticFeedbackEnabled() => true;
  @override
  Future<void> setHapticFeedbackEnabled(bool enabled) async {}

  @override
  double getFontSizeScale() => 1.0;
  @override
  Future<void> setFontSizeScale(double scale) async {}

  @override
  bool hasAcceptedDisclaimer() => true;

  @override
  Future<void> setAcceptedDisclaimer(bool accepted) async {}
}

void main() {
  group('ThemeViewModel', () {
    late MockSettingsRepository settingsRepository;
    late ThemeViewModel viewModel;

    setUp(() {
      settingsRepository = MockSettingsRepository();
      viewModel = ThemeViewModel(settingsRepository);
    });

    test('initial theme mode is system', () {
      expect(viewModel.themeMode, ThemeMode.system);
      expect(viewModel.isDarkMode, false);
    });

    test('toggleTheme switches between light and dark', () async {
      // Start as system (counts as not dark for toggle logic)
      await viewModel.toggleTheme();
      expect(viewModel.themeMode, ThemeMode.dark);
      expect(viewModel.isDarkMode, true);

      await viewModel.toggleTheme();
      expect(viewModel.themeMode, ThemeMode.light);
      expect(viewModel.isDarkMode, false);

      await viewModel.toggleTheme();
      expect(viewModel.themeMode, ThemeMode.dark);
    });

    test('setThemeMode updates mode and notifies listeners', () async {
      bool notified = false;
      viewModel.addListener(() => notified = true);

      await viewModel.setThemeMode(ThemeMode.light);
      expect(viewModel.themeMode, ThemeMode.light);
      expect(notified, true);
    });
  });
}

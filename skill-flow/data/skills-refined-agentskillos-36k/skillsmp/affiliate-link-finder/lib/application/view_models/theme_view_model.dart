import 'package:flutter/material.dart';
import '../../domain/repositories/settings_repository.dart';

class ThemeViewModel extends ChangeNotifier {
  final SettingsRepository _settingsRepository;

  ThemeViewModel(this._settingsRepository);

  ThemeMode get themeMode => _settingsRepository.getThemeMode();

  bool get isDarkMode => themeMode == ThemeMode.dark;

  Future<void> toggleTheme() async {
    final nextMode = isDarkMode ? ThemeMode.light : ThemeMode.dark;
    await _settingsRepository.setThemeMode(nextMode);
    notifyListeners();
  }

  Future<void> setThemeMode(ThemeMode mode) async {
    await _settingsRepository.setThemeMode(mode);
    notifyListeners();
  }

  double get fontScale => _settingsRepository.getFontSizeScale();
  bool get reducedMotion => _settingsRepository.getReducedMotionEnabled();
  bool get hapticEnabled => _settingsRepository.getHapticFeedbackEnabled();

  Future<void> updateFontScale(double scale) async {
    await _settingsRepository.setFontSizeScale(scale);
    notifyListeners();
  }

  Future<void> updateReducedMotion(bool enabled) async {
    await _settingsRepository.setReducedMotionEnabled(enabled);
    notifyListeners();
  }

  Future<void> updateHapticEnabled(bool enabled) async {
    await _settingsRepository.setHapticFeedbackEnabled(enabled);
    notifyListeners();
  }
}

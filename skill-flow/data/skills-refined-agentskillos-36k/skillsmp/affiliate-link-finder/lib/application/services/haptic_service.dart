import 'package:flutter/services.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../config/locator.dart';

class HapticService {
  final SettingsRepository _settings;

  HapticService({SettingsRepository? settings})
      : _settings = settings ?? locator<SettingsRepository>();

  bool get _isEnabled => _settings.getHapticFeedbackEnabled();

  Future<void> lightImpact() async {
    if (_isEnabled) {
      await HapticFeedback.lightImpact();
    }
  }

  Future<void> mediumImpact() async {
    if (_isEnabled) {
      await HapticFeedback.mediumImpact();
    }
  }

  Future<void> heavyImpact() async {
    if (_isEnabled) {
      await HapticFeedback.heavyImpact();
    }
  }

  Future<void> selectionClick() async {
    if (_isEnabled) {
      await HapticFeedback.selectionClick();
    }
  }

  Future<void> vibrate() async {
    if (_isEnabled) {
      await HapticFeedback.vibrate();
    }
  }
}

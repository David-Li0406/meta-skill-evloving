import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/theme_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';

@GenerateMocks([SettingsRepository])
import 'theme_view_model_test.mocks.dart';

void main() {
  late ThemeViewModel viewModel;
  late MockSettingsRepository mockSettingsRepository;

  setUp(() {
    mockSettingsRepository = MockSettingsRepository();

    // Default mock behavior for initialization
    when(mockSettingsRepository.getThemeMode()).thenReturn(ThemeMode.light);
    when(mockSettingsRepository.getFontSizeScale()).thenReturn(1.0);
    when(mockSettingsRepository.getReducedMotionEnabled()).thenReturn(false);
    when(mockSettingsRepository.getHapticFeedbackEnabled()).thenReturn(true);

    viewModel = ThemeViewModel(mockSettingsRepository);
  });

  group('ThemeViewModel', () {
    test('initial values are loaded from repository', () {
      expect(viewModel.themeMode, ThemeMode.light);
      expect(viewModel.isDarkMode, isFalse);
      expect(viewModel.fontScale, 1.0);
      expect(viewModel.reducedMotion, isFalse);
      expect(viewModel.hapticEnabled, isTrue);
    });

    test('toggleTheme switches between light and dark', () async {
      when(mockSettingsRepository.setThemeMode(any))
          .thenAnswer((_) async => true);

      // Light to Dark
      await viewModel.toggleTheme();
      verify(mockSettingsRepository.setThemeMode(ThemeMode.dark)).called(1);

      // Mock repository update for next call
      when(mockSettingsRepository.getThemeMode()).thenReturn(ThemeMode.dark);

      // Dark to Light
      await viewModel.toggleTheme();
      verify(mockSettingsRepository.setThemeMode(ThemeMode.light)).called(1);
    });

    test('setThemeMode persists change', () async {
      when(mockSettingsRepository.setThemeMode(any))
          .thenAnswer((_) async => true);

      await viewModel.setThemeMode(ThemeMode.system);

      verify(mockSettingsRepository.setThemeMode(ThemeMode.system)).called(1);
    });

    test('updateFontScale persists change', () async {
      when(mockSettingsRepository.setFontSizeScale(any))
          .thenAnswer((_) async => true);

      await viewModel.updateFontScale(1.2);

      verify(mockSettingsRepository.setFontSizeScale(1.2)).called(1);
    });

    test('updateReducedMotion persists change', () async {
      when(mockSettingsRepository.setReducedMotionEnabled(any))
          .thenAnswer((_) async => true);

      await viewModel.updateReducedMotion(true);

      verify(mockSettingsRepository.setReducedMotionEnabled(true)).called(1);
    });

    test('updateHapticEnabled persists change', () async {
      when(mockSettingsRepository.setHapticFeedbackEnabled(any))
          .thenAnswer((_) async => true);

      await viewModel.updateHapticEnabled(false);

      verify(mockSettingsRepository.setHapticFeedbackEnabled(false)).called(1);
    });
  });
}

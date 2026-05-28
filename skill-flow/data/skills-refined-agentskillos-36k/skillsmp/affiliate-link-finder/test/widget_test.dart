// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:adhd_supplement_app/main.dart';
import 'package:adhd_supplement_app/config/locator.dart';
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/application/view_models/safety_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/supplement_view_model.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:adhd_supplement_app/domain/repositories/auth_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/safety_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_interaction.dart';
import 'package:adhd_supplement_app/domain/entities/safety_override.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';
import 'package:adhd_supplement_app/application/view_models/persistent_reminders_view_model.dart';
import 'package:adhd_supplement_app/application/view_models/theme_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:adhd_supplement_app/infrastructure/services/seeding_service.dart';
import 'package:adhd_supplement_app/domain/services/analytics_service.dart';

void main() {
  setUp(() {
    // Ensure GetIt has the minimal registrations needed for AdhdSupplementApp.build.
    locator.reset();

    locator.registerFactory<SupplementViewModel>(
      () => SupplementViewModel(
        _FakeSupplementRepository(),
        UrlService(),
        _FakeAnalyticsService(),
      ),
    );

    locator.registerLazySingleton<AuthRepository>(() => _FakeAuthRepository());
    locator.registerFactory<AuthProvider>(
      () => AuthProvider(locator<AuthRepository>()),
    );

    locator
        .registerLazySingleton<SafetyRepository>(() => _FakeSafetyRepository());
    locator.registerFactoryParam<SafetyViewModel, String, void>(
      (userId, _) => SafetyViewModel(
        repository: locator<SafetyRepository>(),
        userId: userId,
      ),
    );

    locator.registerLazySingleton<SettingsRepository>(
        () => _FakeSettingsRepository());
    locator.registerFactory<ThemeViewModel>(
      () => ThemeViewModel(locator<SettingsRepository>()),
    );
    locator.registerLazySingleton<NotificationService>(
        () => _FakeNotificationService());
    locator
        .registerLazySingleton<AnalyticsService>(() => _FakeAnalyticsService());
    locator.registerLazySingleton<SeedingService>(() => _FakeSeedingService());
    locator.registerLazySingleton<SupplementRepository>(
        () => _FakeSupplementRepository());
    locator.registerFactory<PersistentRemindersViewModel>(
      () => PersistentRemindersViewModel(
        locator<SettingsRepository>(),
        locator<NotificationService>(),
      ),
    );
  });

  testWidgets('App builds (smoke test)', (WidgetTester tester) async {
    await tester.pumpWidget(const AdhdSupplementApp(isFirebaseReady: true));
    await tester.pumpAndSettle(const Duration(milliseconds: 2000));

    expect(find.byType(MaterialApp), findsOneWidget);
  });
}

class _FakeAuthRepository implements AuthRepository {
  @override
  Future<void> deleteUser() async {}

  @override
  Stream<User?> authStateChanges() => Stream<User?>.value(null);

  @override
  Future<User?> getCurrentUser() async => null;

  @override
  Future<User> signInAnonymously() async {
    return User(
      id: 'u1',
      email: 'test@example.com',
      createdAt: DateTime.now(),
      unlockedAchievements: const [],
    );
  }

  @override
  Future<User> signInWithEmail(String email, String password) async {
    return User(
      id: 'u1',
      email: email,
      createdAt: DateTime.now(),
      unlockedAchievements: const [],
    );
  }

  @override
  Future<User> signUpWithEmail(
      String email, String password, String displayName) async {
    return User(
      id: 'u1',
      email: email,
      displayName: displayName,
      createdAt: DateTime.now(),
      unlockedAchievements: const [],
    );
  }

  @override
  Future<void> signOut() async {}

  @override
  Future<void> updateUserProfile(User user) async {}
}

class _FakeSupplementRepository implements SupplementRepository {
  @override
  Future<List<Supplement>> getAllSupplements({String? userId}) async => [];

  @override
  Future<Supplement?> getSupplement(String id, {String? userId}) async => null;

  @override
  Future<List<Supplement>> getSupplementsByCategory(String category,
          {String? userId}) async =>
      [];

  @override
  Future<List<Supplement>> searchSupplements(String query,
          {String? userId}) async =>
      [];

  @override
  Future<void> saveCustomSupplement(Supplement supplement) async {}

  @override
  Future<void> deleteCustomSupplement(String id, String userId) async {}

  @override
  Future<void> trackReferralClick(String supplementId) async {}

  @override
  Stream<List<Supplement>> watchSupplements({String? userId}) =>
      const Stream.empty();
}

class _FakeSafetyRepository implements SafetyRepository {
  @override
  Future<List<SupplementInteraction>> getInteractionsForSupplements(
    List<String> supplementIds,
  ) async =>
      [];

  @override
  Future<void> logSafetyOverride(SafetyOverride override) async {}

  @override
  Future<List<SafetyOverride>> getSafetyOverrides(String userId) async => [];

  @override
  Future<SupplementInteraction?> getInteractionById(String id) async => null;
}

class _FakeSettingsRepository implements SettingsRepository {
  @override
  Future<void> init() async {}

  @override
  bool getNudgeModeEnabled() => true;
  @override
  Future<void> setNudgeModeEnabled(bool enabled) async {}

  @override
  TimeOfDay getNudgeTime() => const TimeOfDay(hour: 8, minute: 0);
  @override
  Future<void> setNudgeTime(TimeOfDay time) async {}

  @override
  TimeOfDay getSlotTime(String slot) {
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
  Future<void> setSlotTime(String slot, TimeOfDay time) async {}

  @override
  String getWarningNudgeOption() => '15m';
  @override
  Future<void> setWarningNudgeOption(String option) async {}

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
  bool getExtendedRemindersEnabled() => true;
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
  ThemeMode getThemeMode() => ThemeMode.system;
  @override
  Future<void> setThemeMode(ThemeMode mode) async {}

  @override
  bool hasAcceptedDisclaimer() => true;

  @override
  Future<void> setAcceptedDisclaimer(bool accepted) async {}
}

class _FakeNotificationService implements NotificationService {
  @override
  Future<void> init() async {}
  @override
  Future<void> showNotification({
    required int id,
    required String title,
    required String body,
  }) async {}
  @override
  Future<void> scheduleNotification({
    required int id,
    required String title,
    required String body,
    required DateTime scheduledDate,
  }) async {}
  @override
  Future<void> scheduleRecurringNotification({
    required int id,
    required String title,
    required String body,
    required int hour,
    required int minute,
    int second = 0,
    bool startFromTomorrow = false,
  }) async {}
  @override
  Future<void> cancelNotification(int id) async {}
  @override
  Future<void> cancelAllNotifications() async {}
  @override
  Future<void> cancelAllSupplementNudges(String supplementId,
      [int maxNudges = 12]) async {}
  @override
  Future<List<PendingNotificationRequest>> getPendingNotifications() async =>
      [];
  @override
  Future<void> schedulePersistentNudge({
    required String supplementId,
    required String title,
    required String body,
    required DateTime initialTime,
    int maxNudges = 12,
  }) async {}
  @override
  Future<void> snoozePersistentNudge({
    required String supplementId,
    required String title,
    required String body,
    int maxNudges = 12,
  }) async {}
}

class _FakeSeedingService implements SeedingService {
  @override
  Future<void> seedSupplements() async {}

  @override
  Future<void> createTestUser(String email, String password) async {}
}

class _FakeAnalyticsService implements AnalyticsService {
  @override
  Future<void> logEvent(String name,
      {Map<String, dynamic>? parameters}) async {}
  @override
  Future<void> logScreenView(String screenName) async {}
  @override
  Future<void> setUserId(String userId) async {}
  @override
  Future<void> setUserProperty(String name, String value) async {}
}

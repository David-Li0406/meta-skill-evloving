import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:get_it/get_it.dart';
import 'package:adhd_supplement_app/presentation/views/splash_screen.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/seeding_service.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/presentation/navigation/app_router.dart';

// Mocks
class MockSettingsRepository extends Mock implements SettingsRepository {
  @override
  Future<void> init() async => Future.value();

  @override
  bool getNudgeModeEnabled() => true;
  @override
  Future<void> setNudgeModeEnabled(bool? enabled) async {}
  @override
  TimeOfDay getNudgeTime() => const TimeOfDay(hour: 8, minute: 0);
  @override
  Future<void> setNudgeTime(TimeOfDay? time) async {}
  @override
  TimeOfDay getSlotTime(String? slot) => const TimeOfDay(hour: 8, minute: 0);
  @override
  Future<void> setSlotTime(String? slot, TimeOfDay? time) async {}
  @override
  String getWarningNudgeOption() => '15m';
  @override
  Future<void> setWarningNudgeOption(String? option) async {}
  @override
  bool getExtendedRemindersEnabled() => true;
  @override
  Future<void> setExtendedRemindersEnabled(bool? enabled) async {}
  @override
  bool getBiometricLockEnabled() => false;
  @override
  Future<void> setBiometricLockEnabled(bool? enabled) async {}
  @override
  bool getLocalStorageOnly() => false;
  @override
  Future<void> setLocalStorageOnly(bool? enabled) async {}
  @override
  bool getAnalyticsEnabled() => true;
  @override
  Future<void> setAnalyticsEnabled(bool? enabled) async {}
  @override
  bool getCrashReportingEnabled() => true;
  @override
  Future<void> setCrashReportingEnabled(bool? enabled) async {}
  @override
  ThemeMode getThemeMode() => ThemeMode.system;
  @override
  Future<void> setThemeMode(ThemeMode? mode) async {}
  @override
  bool getReducedMotionEnabled() => false;
  @override
  Future<void> setReducedMotionEnabled(bool? enabled) async {}
  @override
  bool getHapticFeedbackEnabled() => true;
  @override
  Future<void> setHapticFeedbackEnabled(bool? enabled) async {}
  @override
  double getFontSizeScale() => 1.0;
  @override
  Future<void> setFontSizeScale(double? scale) async {}
}

class MockNotificationService extends Mock implements NotificationService {
  @override
  Future<void> init() async => Future.value();
}

class MockSeedingService extends Mock implements SeedingService {
  @override
  Future<void> seedSupplements() async => Future.value();
  @override
  Future<void> createTestUser(String email, String password) async =>
      Future.value();
}

class MockSupplementRepository extends Mock implements SupplementRepository {
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
  Stream<List<Supplement>> watchSupplements({String? userId}) =>
      const Stream.empty();

  @override
  Future<void> saveCustomSupplement(Supplement supplement) async {}

  @override
  Future<void> deleteCustomSupplement(String id, String userId) async {}

  @override
  Future<void> trackReferralClick(String supplementId) async {}
}

void main() {
  final locator = GetIt.instance;

  setUp(() {
    locator.reset();
    locator.registerSingleton<SettingsRepository>(MockSettingsRepository());
    locator.registerSingleton<NotificationService>(MockNotificationService());
    locator.registerSingleton<SeedingService>(MockSeedingService());
    locator.registerSingleton<SupplementRepository>(MockSupplementRepository());
  });

  tearDown(() {
    locator.reset();
  });

  testWidgets('SplashScreen initializes services and navigates',
      (WidgetTester tester) async {
    // Build SplashScreen wrapped in MaterialApp to handle navigation
    await tester.pumpWidget(
      MaterialApp(
        initialRoute: AppRouter.splash,
        onGenerateRoute: (settings) {
          debugPrint('DEBUG: Generated route for ${settings.name}');
          if (settings.name == AppRouter.home) {
            return MaterialPageRoute(
                builder: (_) => const Scaffold(body: Text('Home Screen')));
          }
          if (settings.name == AppRouter.splash) {
            return MaterialPageRoute(
                builder: (_) => const SplashScreen(isFirebaseReady: true));
          }
          return null;
        },
      ),
    );

    // Verify initial state
    expect(
        find.byType(CircularProgressIndicator), findsNothing); // We used Linear
    expect(find.byType(LinearProgressIndicator), findsOneWidget);
    expect(find.text('Loading preferences...'), findsOneWidget);

    // Pump to flush microtasks (init calls)
    await tester.pump(const Duration(milliseconds: 100)); // Short pump

    // Should be at specific step now (Settings done, Notifications done, Seeding started)
    // "Checking supplements..."
    // Note: depending on microtask scheduling, it might be fast.

    await tester.pump(const Duration(milliseconds: 100));
    expect(find.text('Setting up reminders...'), findsOneWidget);

    // Wait for the specific delay in SplashScreen (1500ms)
    // We already pumped 200ms. Pump remaining + buffer.
    await tester.pump(const Duration(milliseconds: 3000));

    // Allow navigation to start
    await tester.pump();
    // Allow navigation transition to complete
    await tester.pump(const Duration(milliseconds: 800));

    expect(find.text('Home Screen'), findsOneWidget);
  });
}

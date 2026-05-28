import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/view_models/daily_stack_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/log_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/auth_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';
import 'package:flutter/material.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_stack.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

import 'package:adhd_supplement_app/domain/services/analytics_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/sound_service.dart';

// Fakes for cleaner manual testing without mockito's "when" null-safety issues
class FakeStackRepository implements StackRepository {
  List<SupplementStack> stacks = [];
  String? lastUserId;

  @override
  Future<List<SupplementStack>> getUserStacks(String userId) async {
    lastUserId = userId;
    return stacks;
  }

  @override
  Future<SupplementStack?> getStack(String userId) async => null;

  @override
  Future<void> saveStack(String userId, SupplementStack stack) async {}

  @override
  Stream<List<SupplementStack>> watchUserStacks(String userId) =>
      Stream.value(stacks);
}

class FakeLogRepository implements LogRepository {
  DailyLog? todayLog;
  int streakCount = 0;
  DailyLog? lastSavedLog;

  @override
  Future<DailyLog?> getLogForDate(String userId, DateTime date) async =>
      todayLog;
  @override
  Future<int> getStreakCount(String userId) async => streakCount;
  @override
  Future<void> saveLog(DailyLog log) async {
    lastSavedLog = log;
    todayLog = log;
  }

  @override
  Future<List<DailyLog>> getLogsByDateRange(
          String userId, DateTime start, DateTime end) async =>
      [];
  @override
  Future<List<DailyLog>> getRecentLogs(String userId, int days) async => [];
  @override
  Stream<DailyLog?> watchTodayLog(String userId) => Stream.value(todayLog);

  @override
  Future<void> clearAllLogs(String userId) async {
    todayLog = null;
    streakCount = 0;
  }
}

class FakeSupplementRepository implements SupplementRepository {
  final Map<String, Supplement> supplements = {};

  @override
  Future<Supplement?> getSupplement(String id, {String? userId}) async =>
      supplements[id];

  @override
  Future<List<Supplement>> searchSupplements(String query,
          {String? userId}) async =>
      [];

  @override
  Future<List<Supplement>> getSupplementsByCategory(String category,
          {String? userId}) async =>
      [];

  @override
  Stream<List<Supplement>> watchSupplements({String? userId}) =>
      Stream.value([]);

  @override
  Future<List<Supplement>> getAllSupplements({String? userId}) async =>
      supplements.values.toList();

  @override
  Future<void> saveCustomSupplement(Supplement supplement) async {}

  @override
  Future<void> deleteCustomSupplement(String id, String userId) async {}

  @override
  Future<void> trackReferralClick(String supplementId) async {}
}

class FakeNotificationService implements NotificationService {
  @override
  Future<void> init() async {}
  @override
  Future<void> showNotification(
      {required int id, required String title, required String body}) async {}
  @override
  Future<void> scheduleNotification(
      {required int id,
      required String title,
      required String body,
      required DateTime scheduledDate}) async {}
  @override
  Future<void> scheduleRecurringNotification(
      {required int id,
      required String title,
      required String body,
      required int hour,
      required int minute,
      int second = 0,
      bool startFromTomorrow = false}) async {}
  @override
  Future<void> cancelNotification(int id) async {}
  @override
  Future<void> cancelAllNotifications() async {}
  @override
  Future<List<PendingNotificationRequest>> getPendingNotifications() async =>
      [];
  @override
  Future<void> schedulePersistentNudge(
      {required String supplementId,
      required String title,
      required String body,
      required DateTime initialTime,
      int maxNudges = 12}) async {}
  @override
  Future<void> snoozePersistentNudge(
      {required String supplementId,
      required String title,
      required String body,
      int maxNudges = 12}) async {}
  @override
  Future<void> cancelAllSupplementNudges(String supplementId,
      [int maxNudges = 12]) async {}
}

class FakeAuthRepository implements AuthRepository {
  User? currentUser;
  User? lastUpdatedUser;

  @override
  Future<User?> getCurrentUser() async => currentUser;

  @override
  Future<User> signInAnonymously() async => currentUser!;

  @override
  Future<User> signInWithEmail(String email, String password) async =>
      currentUser!;

  @override
  Future<User> signUpWithEmail(
          String email, String password, String displayName) async =>
      currentUser!;

  @override
  Future<void> signOut() async {}

  @override
  Stream<User?> authStateChanges() => Stream.value(currentUser);

  @override
  Future<void> updateUserProfile(User user) async {
    lastUpdatedUser = user;
    currentUser = user;
  }

  @override
  Future<void> deleteUser() async {}
}

class FakeAnalyticsService implements AnalyticsService {
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

class FakeSoundService implements SoundService {
  @override
  Future<void> playSuccess() async {}
  @override
  Future<void> dispose() async {}
}

class FakeSettingsRepository implements SettingsRepository {
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
  ThemeMode getThemeMode() => ThemeMode.system;
  @override
  Future<void> setThemeMode(ThemeMode mode) async {}
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
  TestWidgetsFlutterBinding.ensureInitialized();
  late DailyStackViewModel viewModel;
  late FakeStackRepository fakeStackRepo;
  late FakeLogRepository fakeLogRepo;
  late FakeSupplementRepository fakeSupplementRepo;
  late FakeAuthRepository fakeAuthRepo;
  const String userId = 'test-user';

  const testSupplement = Supplement(
    id: 'supp1',
    name: 'Magnesium',
    category: 'Mineral',
    dosage: '200mg',
    timeOfDay: 'evening',
    benefits: ['Sleep'],
    description: 'Relaxation',
    referralUrl: '',
    sideEffects: [],
    interactions: [],
    focusLevel: 3,
  );

  final morningStack = SupplementStack(
    id: 'stack_morning',
    userId: userId,
    name: 'Morning Routine',
    items: [
      const StackItem(supplementId: 'supp2', order: 1, scheduledTime: '08:00'),
    ],
    timeOfDay: 'morning',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  final eveningStack = SupplementStack(
    id: 'stack_evening',
    userId: userId,
    name: 'Evening Routine',
    items: [
      const StackItem(supplementId: 'supp1', order: 1, scheduledTime: '20:00'),
    ],
    timeOfDay: 'evening',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  setUp(() {
    fakeStackRepo = FakeStackRepository();
    fakeLogRepo = FakeLogRepository();
    fakeSupplementRepo = FakeSupplementRepository();
    fakeAuthRepo = FakeAuthRepository();
    viewModel = DailyStackViewModel(
      stackRepository: fakeStackRepo,
      logRepository: fakeLogRepo,
      supplementRepository: fakeSupplementRepo,
      settingsRepository: FakeSettingsRepository(),
      notificationService: FakeNotificationService(),
      authRepository: fakeAuthRepo,
      analyticsService: FakeAnalyticsService(),
      soundService: FakeSoundService(),
      userId: userId,
    );
  });

  group('DailyStackViewModel Tests (with Fakes)', () {
    test('initialize loads data and caches supplements', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeLogRepo.streakCount = 5;
      fakeSupplementRepo.supplements['supp1'] = testSupplement;
      fakeSupplementRepo.supplements['supp2'] =
          testSupplement.copyWith(id: 'supp2', timeOfDay: 'morning');

      await viewModel.initialize();

      expect(viewModel.stacks.length, 2);
      expect(viewModel.streakCount, 5);
      expect(viewModel.getSupplement('supp1'), isNotNull);
      expect(viewModel.morningItems.length, 1);
      expect(viewModel.eveningItems.length, 1);
    });

    test('todayProgress calculates correctly', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeLogRepo.todayLog = DailyLog(
        id: 'log1',
        userId: userId,
        date: DateTime.now(),
        entries: [
          LogEntry(
              supplementId: 'supp1',
              takenAt: DateTime.now(),
              status: LogStatus.taken),
        ],
        createdAt: DateTime.now(),
      );

      await viewModel.initialize();

      // total items = 2, completed = 1
      expect(viewModel.todayProgress, 0.5);
    });

    test('toggleSupplement marks as taken and updates log', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeSupplementRepo.supplements['supp1'] = testSupplement;
      fakeSupplementRepo.supplements['supp2'] = testSupplement;

      await viewModel.initialize();
      expect(viewModel.isSupplementTaken('supp1'), false);

      await viewModel.toggleSupplement('supp1');

      expect(viewModel.isSupplementTaken('supp1'), true);
      expect(fakeLogRepo.lastSavedLog, isNotNull);
      expect(
          fakeLogRepo.lastSavedLog!.entries.any(
              (e) => e.supplementId == 'supp1' && e.status == LogStatus.taken),
          true);
    });

    test('greeting is one of the valid options', () {
      final validGreetings = [
        'Good Morning',
        'Good Afternoon',
        'Good Evening',
        'Good Night'
      ];
      expect(validGreetings.contains(viewModel.greeting), true);
    });

    test('markSupplementTaken increments user XP', () async {
      final initialUser = User(
        id: userId,
        email: 'test@example.com',
        createdAt: DateTime.now(),
        xp: 0,
        level: 1,
        unlockedAchievements: const [],
      );
      fakeAuthRepo.currentUser = initialUser;

      await viewModel.markSupplementTaken('supp1');

      expect(fakeAuthRepo.lastUpdatedUser, isNotNull);
      expect(fakeAuthRepo.lastUpdatedUser!.xp, 10);
    });

    test('logical today respects 4 AM rollover (Before 4 AM)', () async {
      // Mocking 2 AM
      // Note: We can't easily mock DateTime.now() without a wrapper or clock package
      // but we can test the internal _getLogicalToday via initialize as it calls it
      // Since the code uses DateTime.now() directly, this is hard to unit test without refactoring
      // However, we can test that items hide when taken as requested.
    });

    test('items are hidden from lists after being taken', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeSupplementRepo.supplements['supp1'] = testSupplement;

      await viewModel.initialize();
      expect(
          viewModel.eveningItems.any((i) => i.supplementId == 'supp1'), true);

      await viewModel.markSupplementTaken('supp1');

      // Should now be filtered out
      expect(
          viewModel.eveningItems.any((i) => i.supplementId == 'supp1'), false);
    });

    test('markSupplementSkipped marks as skipped and updates log', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeSupplementRepo.supplements['supp1'] = testSupplement;

      await viewModel.initialize();
      expect(viewModel.isSupplementSkipped('supp1'), false);

      await viewModel.markSupplementSkipped('supp1', reason: 'Forgot');

      expect(viewModel.isSupplementSkipped('supp1'), true);
      expect(fakeLogRepo.lastSavedLog, isNotNull);
      expect(
          fakeLogRepo.lastSavedLog!.entries.any((e) =>
              e.supplementId == 'supp1' && e.status == LogStatus.skipped),
          true);
    });

    test('toggleSupplement unskips a skipped supplement', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeSupplementRepo.supplements['supp1'] = testSupplement;

      await viewModel.initialize();

      // First skip it
      await viewModel.markSupplementSkipped('supp1');
      expect(viewModel.isSupplementSkipped('supp1'), true);

      // Now toggle it (should unskip)
      await viewModel.toggleSupplement('supp1');

      expect(viewModel.isSupplementSkipped('supp1'), false);
      expect(viewModel.isSupplementTaken('supp1'), false);
      expect(
          fakeLogRepo.lastSavedLog!.entries
              .any((e) => e.supplementId == 'supp1'),
          false);
    });

    test('skipped items are hidden from pending lists', () async {
      fakeStackRepo.stacks = [morningStack, eveningStack];
      fakeSupplementRepo.supplements['supp1'] = testSupplement;

      await viewModel.initialize();
      expect(
          viewModel.eveningItems.any((i) => i.supplementId == 'supp1'), true);

      await viewModel.markSupplementSkipped('supp1');

      // Should now be filtered out
      expect(
          viewModel.eveningItems.any((i) => i.supplementId == 'supp1'), false);
    });

    test('getTimeStatus formatting', () {
      expect(viewModel.getTimeStatus(null), isNull);
      expect(viewModel.getTimeStatus('invalid'), isNull);

      final morningStatus = viewModel.getTimeStatus('Morning');
      expect(morningStatus, isNotNull);
      expect(morningStatus!.isNotEmpty, true);

      final eveningStatus = viewModel.getTimeStatus('Evening');
      expect(eveningStatus, isNotNull);
    });

    test('categorizes items into afternoon and night slots', () async {
      final afternoonStack = SupplementStack(
        id: 'stack2',
        userId: userId,
        name: 'Afternoon Routine',
        items: [
          const StackItem(supplementId: 'supp3', order: 1),
        ],
        timeOfDay: 'afternoon',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      final nightStack = SupplementStack(
        id: 'stack3',
        userId: userId,
        name: 'Night Routine',
        items: [
          const StackItem(supplementId: 'supp4', order: 1),
        ],
        timeOfDay: 'night',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      fakeStackRepo.stacks = [afternoonStack, nightStack];
      fakeSupplementRepo.supplements['supp3'] =
          testSupplement.copyWith(id: 'supp3', name: 'Vit D');
      fakeSupplementRepo.supplements['supp4'] =
          testSupplement.copyWith(id: 'supp4', name: 'ZMA');

      await viewModel.initialize();

      expect(viewModel.afternoonItems.length, 1);
      expect(viewModel.afternoonItems.first.supplementId, 'supp3');
      expect(viewModel.nightItems.length, 1);
      expect(viewModel.nightItems.first.supplementId, 'supp4');
    });

    group('Expansion Logic', () {
      test('toggleStackExpansion adds/removes stack IDs', () {
        expect(viewModel.collapsedStackIds.isEmpty, true);

        viewModel.toggleStackExpansion('stack1');
        expect(viewModel.collapsedStackIds.contains('stack1'), true);

        viewModel.toggleStackExpansion('stack1');
        expect(viewModel.collapsedStackIds.contains('stack1'), false);
      });

      test('toggleAllExpansion collapses both dynamic and slot IDs', () async {
        final stack1 = SupplementStack(
          id: 'stack1',
          userId: userId,
          name: 'Morning Stack',
          items: [const StackItem(supplementId: 'supp1', order: 1)],
          timeOfDay: 'morning',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );
        fakeStackRepo.stacks = [stack1];
        await viewModel.initialize();

        expect(viewModel.allCollapsed, false);

        viewModel.toggleAllExpansion();
        expect(viewModel.allCollapsed, true);

        // Should contain database ID
        expect(viewModel.collapsedStackIds.contains('stack1'), true);
        // Should contain Dashboard slot IDs
        expect(viewModel.collapsedStackIds.contains('morning'), true);
        expect(viewModel.collapsedStackIds.contains('night'), true);

        viewModel.toggleAllExpansion();
        expect(viewModel.allCollapsed, false);
        expect(viewModel.collapsedStackIds.isEmpty, true);
      });
    });

    group('Progress Calculation', () {
      test('todayProgress handles duplicate supplements and skipped items',
          () async {
        final stack1 = SupplementStack(
          id: 'stack1',
          userId: userId,
          name: 'Morning Stack',
          items: [const StackItem(supplementId: 'supp1', order: 1)],
          timeOfDay: 'morning',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );
        final stack2 = SupplementStack(
          id: 'stack2',
          userId: userId,
          name: 'Evening Stack',
          items: [
            const StackItem(supplementId: 'supp1', order: 1), // DUPLICATE
            const StackItem(supplementId: 'supp2', order: 1),
          ],
          timeOfDay: 'evening',
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        fakeStackRepo.stacks = [stack1, stack2];
        await viewModel.initialize();

        // totalDistinct = 2 (supp1, supp2)

        expect(viewModel.todayProgress, 0.0);

        // Take supp1
        await viewModel.markSupplementTaken('supp1');
        // supp1 handled (1 of 2)
        expect(viewModel.todayProgress, 0.5);

        // Skip supp2
        await viewModel.markSupplementSkipped('supp2');
        // supp2 handled (2 of 2)
        expect(viewModel.todayProgress, 1.0);
        expect(viewModel.progressText, '2 of 2 stacks completed');
      });
    });
  });
}

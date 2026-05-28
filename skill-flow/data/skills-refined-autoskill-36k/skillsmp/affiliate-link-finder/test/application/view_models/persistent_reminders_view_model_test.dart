import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:adhd_supplement_app/application/view_models/persistent_reminders_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/settings_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';

class _FakeSettingsRepository implements SettingsRepository {
  bool nudgeModeEnabled;
  TimeOfDay nudgeTime;
  String warningNudgeOption;
  bool extendedRemindersEnabled;

  _FakeSettingsRepository({
    this.nudgeModeEnabled = true,
    TimeOfDay? nudgeTime,
    this.warningNudgeOption = '15m',
    this.extendedRemindersEnabled = true,
    Map<String, TimeOfDay>? slotTimes,
  })  : nudgeTime = nudgeTime ?? const TimeOfDay(hour: 8, minute: 0),
        slotTimes = slotTimes ??
            {
              'morning': const TimeOfDay(hour: 8, minute: 0),
              'afternoon': const TimeOfDay(hour: 13, minute: 0),
              'evening': const TimeOfDay(hour: 18, minute: 0),
              'night': const TimeOfDay(hour: 21, minute: 0),
            };

  Map<String, TimeOfDay> slotTimes;

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
  Future<void> init() async {}

  @override
  bool getNudgeModeEnabled() => nudgeModeEnabled;

  @override
  Future<void> setNudgeModeEnabled(bool enabled) async {
    nudgeModeEnabled = enabled;
  }

  @override
  TimeOfDay getNudgeTime() => nudgeTime;

  @override
  Future<void> setNudgeTime(TimeOfDay time) async {
    nudgeTime = time;
  }

  @override
  String getWarningNudgeOption() => warningNudgeOption;

  @override
  TimeOfDay getSlotTime(String slot) =>
      slotTimes[slot.toLowerCase()] ?? const TimeOfDay(hour: 8, minute: 0);

  @override
  Future<void> setSlotTime(String slot, TimeOfDay time) async {
    slotTimes[slot.toLowerCase()] = time;
  }

  @override
  Future<void> setWarningNudgeOption(String option) async {
    warningNudgeOption = option;
  }

  @override
  bool getExtendedRemindersEnabled() => extendedRemindersEnabled;

  @override
  Future<void> setExtendedRemindersEnabled(bool enabled) async {
    extendedRemindersEnabled = enabled;
  }

  @override
  bool getBiometricLockEnabled() {
    return false;
  }

  @override
  Future<void> setBiometricLockEnabled(bool enabled) async {}

  @override
  bool getLocalStorageOnly() => false;

  @override
  Future<void> setLocalStorageOnly(bool enabled) async {}

  @override
  bool getAnalyticsEnabled() => false;

  @override
  Future<void> setAnalyticsEnabled(bool enabled) async {}

  @override
  bool getCrashReportingEnabled() => false;

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

class _FakeNotificationService extends NotificationService {
  final List<int> scheduledIds = [];
  final Map<int, (int, int)> scheduledTimes = {};
  int scheduleCallCount = 0;

  final List<int> cancelledIds = [];
  int cancelCallCount = 0;

  int? lastShownId;
  String? lastShownTitle;
  String? lastShownBody;

  @override
  Future<void> scheduleRecurringNotification({
    required int id,
    required String title,
    required String body,
    required int hour,
    required int minute,
    int second = 0,
    bool startFromTomorrow = false,
  }) async {
    scheduledIds.add(id);
    scheduledTimes[id] = (hour, minute);
    scheduleCallCount++;
  }

  @override
  Future<void> cancelNotification(int id) async {
    cancelledIds.add(id);
    cancelCallCount++;
  }

  @override
  Future<void> showNotification({
    required int id,
    required String title,
    required String body,
  }) async {
    lastShownId = id;
    lastShownTitle = title;
    lastShownBody = body;
  }

  void clear() {
    scheduledIds.clear();
    scheduledTimes.clear();
    scheduleCallCount = 0;
    cancelledIds.clear();
    cancelCallCount = 0;
  }
}

void main() {
  group('PersistentRemindersViewModel', () {
    late _FakeSettingsRepository settingsRepository;
    late _FakeNotificationService notificationService;
    late PersistentRemindersViewModel viewModel;

    setUp(() {
      settingsRepository = _FakeSettingsRepository(
        nudgeModeEnabled: true,
        nudgeTime: const TimeOfDay(hour: 9, minute: 30),
        warningNudgeOption: 'followup',
        extendedRemindersEnabled: false,
      );
      notificationService = _FakeNotificationService();
      viewModel =
          PersistentRemindersViewModel(settingsRepository, notificationService);
    });

    test('loads initial settings from repository', () {
      expect(viewModel.nudgeModeEnabled, isTrue);
      expect(viewModel.nudgeTime.hour, 9);
      expect(viewModel.nudgeTime.minute, 30);
      expect(viewModel.warningNudgeOption, 'followup');
      expect(viewModel.extendedRemindersEnabled, isFalse);
    });

    test('setNudgeModeEnabled true schedules multiple notifications', () async {
      notificationService.clear();
      await viewModel.setNudgeModeEnabled(true);

      expect(settingsRepository.nudgeModeEnabled, isTrue);
      // Expected IDs: 1000 (main), 1001 (warning), 1002 (followup if enabled), 2000 (evening)
      // In setUp, warningNudgeOption is 'followup', so all 4 should be scheduled
      expect(notificationService.scheduleCallCount, 4);
      expect(notificationService.scheduledIds,
          containsAll([1000, 1001, 1002, 2000]));

      // Verify evening summary time (8 PM)
      expect(notificationService.scheduledTimes[2000], (20, 0));
    });

    test('setNudgeModeEnabled false cancels all notifications', () async {
      notificationService.clear();
      await viewModel.setNudgeModeEnabled(false);

      expect(settingsRepository.nudgeModeEnabled, isFalse);
      expect(notificationService.cancelCallCount, 4);
      expect(notificationService.cancelledIds,
          containsAll([1000, 1001, 1002, 2000]));
    });

    test('setNudgeTime updates time and reschedules notifications', () async {
      const newTime = TimeOfDay(hour: 7, minute: 15);
      notificationService.clear();

      await viewModel.setNudgeTime(newTime);

      expect(viewModel.nudgeTime, newTime);
      expect(settingsRepository.nudgeTime, newTime);
      // Verify main nudge is at newTime + 5m (Soft Nudge logic)
      expect(notificationService.scheduledTimes[1000], (7, 20));
    });

    test('setWarningNudgeOption updates setting only', () async {
      await viewModel.setWarningNudgeOption('15m');

      expect(viewModel.warningNudgeOption, '15m');
      expect(settingsRepository.warningNudgeOption, '15m');
      // Should not touch notifications
      expect(notificationService.scheduleCallCount, 0);
      expect(notificationService.cancelCallCount, 0);
    });

    test('setExtendedRemindersEnabled updates setting only', () async {
      await viewModel.setExtendedRemindersEnabled(true);

      expect(viewModel.extendedRemindersEnabled, isTrue);
      expect(settingsRepository.extendedRemindersEnabled, isTrue);
      // Should not touch notifications
      expect(notificationService.scheduleCallCount, 0);
      expect(notificationService.cancelCallCount, 0);
    });

    test('testNotification triggers a one-time notification', () async {
      await viewModel.testNotification();

      expect(notificationService.lastShownId, 999);
      expect(notificationService.lastShownTitle, isNotEmpty);
      expect(notificationService.lastShownBody, isNotEmpty);
    });

    test('loads slot times from repository', () {
      expect(viewModel.morningTime, const TimeOfDay(hour: 8, minute: 0));
      expect(viewModel.afternoonTime, const TimeOfDay(hour: 13, minute: 0));
      expect(viewModel.eveningTime, const TimeOfDay(hour: 18, minute: 0));
      expect(viewModel.nightTime, const TimeOfDay(hour: 21, minute: 0));
    });

    test('setSlotTime updates state and repository', () async {
      const newMorningTime = TimeOfDay(hour: 7, minute: 30);
      const newNightTime = TimeOfDay(hour: 22, minute: 0);

      await viewModel.setSlotTime('morning', newMorningTime);
      await viewModel.setSlotTime('night', newNightTime);

      expect(viewModel.morningTime, newMorningTime);
      expect(settingsRepository.getSlotTime('morning'), newMorningTime);
      expect(viewModel.nightTime, newNightTime);
      expect(settingsRepository.getSlotTime('night'), newNightTime);
    });
  });
}

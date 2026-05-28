import 'package:flutter/material.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../infrastructure/services/notification_service.dart';

class PersistentRemindersViewModel extends ChangeNotifier {
  final SettingsRepository _settingsRepository;
  final NotificationService _notificationService;

  PersistentRemindersViewModel(
    this._settingsRepository,
    this._notificationService,
  ) {
    _loadSettings();
  }

  bool _nudgeModeEnabled = true;
  TimeOfDay _nudgeTime = const TimeOfDay(hour: 8, minute: 0);
  String _warningNudgeOption = '15m'; // '15m' or 'followup'
  bool _extendedRemindersEnabled = true;

  TimeOfDay _morningTime = const TimeOfDay(hour: 8, minute: 0);
  TimeOfDay _afternoonTime = const TimeOfDay(hour: 13, minute: 0);
  TimeOfDay _eveningTime = const TimeOfDay(hour: 18, minute: 0);
  TimeOfDay _nightTime = const TimeOfDay(hour: 21, minute: 0);

  bool get nudgeModeEnabled => _nudgeModeEnabled;
  TimeOfDay get nudgeTime => _nudgeTime;
  String get warningNudgeOption => _warningNudgeOption;
  bool get extendedRemindersEnabled => _extendedRemindersEnabled;

  TimeOfDay get morningTime => _morningTime;
  TimeOfDay get afternoonTime => _afternoonTime;
  TimeOfDay get eveningTime => _eveningTime;
  TimeOfDay get nightTime => _nightTime;

  void _loadSettings() {
    _nudgeModeEnabled = _settingsRepository.getNudgeModeEnabled();
    _nudgeTime = _settingsRepository.getNudgeTime();
    _warningNudgeOption = _settingsRepository.getWarningNudgeOption();
    _extendedRemindersEnabled =
        _settingsRepository.getExtendedRemindersEnabled();

    _morningTime = _settingsRepository.getSlotTime('morning');
    _afternoonTime = _settingsRepository.getSlotTime('afternoon');
    _eveningTime = _settingsRepository.getSlotTime('evening');
    _nightTime = _settingsRepository.getSlotTime('night');

    notifyListeners();
  }

  Future<void> setNudgeModeEnabled(bool value) async {
    _nudgeModeEnabled = value;
    await _settingsRepository.setNudgeModeEnabled(value);
    await _scheduleOrCancelNotifications();
    notifyListeners();
  }

  Future<void> setNudgeTime(TimeOfDay time) async {
    _nudgeTime = time;
    await _settingsRepository.setNudgeTime(time);
    await _scheduleOrCancelNotifications();
    notifyListeners();
  }

  Future<void> setWarningNudgeOption(String option) async {
    _warningNudgeOption = option;
    await _settingsRepository.setWarningNudgeOption(option);
    notifyListeners();
  }

  Future<void> setExtendedRemindersEnabled(bool value) async {
    _extendedRemindersEnabled = value;
    await _settingsRepository.setExtendedRemindersEnabled(value);
    notifyListeners();
  }

  Future<void> setSlotTime(String slot, TimeOfDay time) async {
    switch (slot.toLowerCase()) {
      case 'morning':
        _morningTime = time;
        break;
      case 'afternoon':
        _afternoonTime = time;
        break;
      case 'evening':
        _eveningTime = time;
        break;
      case 'night':
        _nightTime = time;
        break;
    }
    await _settingsRepository.setSlotTime(slot, time);
    notifyListeners();
  }

  Future<void> _scheduleOrCancelNotifications() async {
    // 1000 is the ID for the daily reminder
    // 1001 is the ID for the warning/follow-up nudge
    if (_nudgeModeEnabled) {
      // Soft Nudge (+5m)
      int softHour = _nudgeTime.hour;
      int softMinute = _nudgeTime.minute + 5;
      if (softMinute >= 60) {
        softHour = (softHour + 1) % 24;
        softMinute = softMinute - 60;
      }
      await _notificationService.scheduleRecurringNotification(
        id: 1000,
        title: 'Time for your daily stack! (Soft Nudge)',
        body: 'Keep your streak alive. Take your supplements now.',
        hour: softHour,
        minute: softMinute,
      );

      // Medium Nudge (+15m)
      int mediumHour = _nudgeTime.hour;
      int mediumMinute = _nudgeTime.minute + 15;
      if (mediumMinute >= 60) {
        mediumHour = (mediumHour + 1) % 24;
        mediumMinute = mediumMinute - 60;
      }
      await _notificationService.scheduleRecurringNotification(
        id: 1001,
        title: 'Missed your stack? (Medium Nudge)',
        body: 'Just a friendly nudge to log your supplements!',
        hour: mediumHour,
        minute: mediumMinute,
      );

      // CRITICAL Alert (+30m)
      int criticalHour = _nudgeTime.hour;
      int criticalMinute = _nudgeTime.minute + 30;
      if (criticalMinute >= 60) {
        criticalHour = (criticalHour + 1) % 24;
        criticalMinute = criticalMinute - 60;
      }
      await _notificationService.scheduleRecurringNotification(
        id: 1002,
        title: 'STILL HAVEN\'T LOGGED? (CRITICAL)',
        body: 'Consistency is key! Tracking helps your doctor help you.',
        hour: criticalHour,
        minute: criticalMinute,
      );

      // Evening Summary (20:00) - Always on if Nudge Mode is active
      await _notificationService.scheduleRecurringNotification(
        id: 2000,
        title: 'Daily Summary 🌙',
        body: 'Tap to see your progress for today!',
        hour: 20,
        minute: 0,
      );
    } else {
      await _notificationService.cancelNotification(1000);
      await _notificationService.cancelNotification(1001);
      await _notificationService.cancelNotification(1002);
      await _notificationService.cancelNotification(2000);
    }
  }

  Future<void> testNotification() async {
    await _notificationService.showNotification(
      id: 999, // Test ID
      title: 'Test Reminder',
      body: 'This is how your daily nudge will look and sound.',
    );
  }

  Future<void> clearAllNotifications() async {
    await _notificationService.cancelAllNotifications();
    // Reschedule recurring ones if nudge mode is on
    if (_nudgeModeEnabled) {
      await _scheduleOrCancelNotifications();
    }
  }
}

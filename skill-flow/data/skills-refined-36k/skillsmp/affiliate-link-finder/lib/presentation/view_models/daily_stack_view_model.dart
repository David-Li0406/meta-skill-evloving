import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../utils/logger.dart';
import '../../domain/entities/supplement_stack.dart';
import '../../domain/entities/daily_log.dart';
import '../../domain/entities/supplement.dart';
import '../../domain/repositories/stack_repository.dart';
import '../../domain/repositories/log_repository.dart';
import '../../domain/repositories/supplement_repository.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../infrastructure/services/notification_service.dart';
import '../../infrastructure/services/sound_service.dart';
import '../../domain/services/analytics_service.dart';
import 'dart:async';

/// View model for the Daily Stack screen
/// Manages today's stacks, intake status, and progress tracking
class DailyStackViewModel extends ChangeNotifier {
  final StackRepository _stackRepository;
  final LogRepository _logRepository;
  final SupplementRepository _supplementRepository;
  final SettingsRepository _settingsRepository;
  final NotificationService _notificationService;
  final AuthRepository _authRepository;
  final AnalyticsService _analyticsService;
  final SoundService _soundService;
  final String _userId;

  // State
  List<SupplementStack> _stacks = [];
  DailyLog? _todayLog;
  final Map<String, Supplement> _supplementCache = {};
  int _streakCount = 0;
  bool _isLoading = false;
  String? _error;
  bool _isDisposed = false;
  final Set<String> _snoozedSupplements = {};
  final Set<String> _collapsedStackIds = {};
  bool _allCollapsed = false;
  StreamSubscription<List<SupplementStack>>? _stackSubscription;

  // Time-based slots
  List<StackItem> get morningItems => _getItemsForSlot('morning');
  List<StackItem> get afternoonItems => _getItemsForSlot('afternoon');
  List<StackItem> get eveningItems => _getItemsForSlot('evening');
  List<StackItem> get nightItems => _getItemsForSlot('night');

  /// Get the data for the "Up Next" routine card
  Map<String, dynamic>? get upcomingStack {
    if (morningItems.isNotEmpty) {
      return {
        'slot': 'morning',
        'title': 'Morning Focus',
        'subtitle': 'Daily Startup',
        'time': _settingsRepository.getSlotTime('morning'),
        'items': morningItems,
      };
    }
    if (afternoonItems.isNotEmpty) {
      return {
        'slot': 'afternoon',
        'title': 'Afternoon Focus',
        'subtitle': 'Mid-day Boost',
        'time': _settingsRepository.getSlotTime('afternoon'),
        'items': afternoonItems,
      };
    }
    if (eveningItems.isNotEmpty) {
      return {
        'slot': 'evening',
        'title': 'Evening Stack',
        'subtitle': 'Sundown Support',
        'time': _settingsRepository.getSlotTime('evening'),
        'items': eveningItems,
      };
    }
    if (nightItems.isNotEmpty) {
      return {
        'slot': 'night',
        'title': 'Night Stack',
        'subtitle': 'Rest & Recovery',
        'time': _settingsRepository.getSlotTime('night'),
        'items': nightItems,
      };
    }
    return null;
  }

  /// Get all items that were skipped today
  List<StackItem> get skippedItems {
    return _stacks
        .expand((stack) => stack.items)
        .where((item) => isSupplementSkipped(item.supplementId))
        .toList();
  }

  // Getters
  List<SupplementStack> get stacks => _stacks;
  DailyLog? get todayLog => _todayLog;
  int get streakCount => _streakCount;
  bool get isLoading => _isLoading;
  String? get error => _error;
  Set<String> get snoozedSupplements => _snoozedSupplements;
  Set<String> get collapsedStackIds => _collapsedStackIds;
  bool get allCollapsed => _allCollapsed;

  /// Get all items that are pending (neither taken nor skipped)
  List<StackItem> get pendingItems {
    return _stacks
        .expand((stack) => stack.items)
        .where((item) =>
            !isSupplementTaken(item.supplementId) &&
            !isSupplementSkipped(item.supplementId))
        .toList();
  }

  /// Whether there are any skipped items today
  bool get hasSkippedItems {
    return _stacks
        .any((s) => s.items.any((i) => isSupplementSkipped(i.supplementId)));
  }

  /// Get dynamic greeting based on time of day
  String get greeting {
    final hour = DateTime.now().hour;
    if (hour >= 5 && hour < 12) {
      return 'Good Morning';
    }
    if (hour >= 12 && hour < 17) {
      return 'Good Afternoon';
    }
    if (hour >= 17 && hour < 21) {
      return 'Good Evening';
    }
    return 'Good Night';
  }

  /// Calculate today's progress as a percentage (0.0 - 1.0)
  double get todayProgress {
    if (_stacks.isEmpty) return 0.0;

    // Get unique supplement IDs across all stacks
    final scheduledSupps =
        _stacks.expand((s) => s.items.map((i) => i.supplementId)).toSet();
    final totalDistinct = scheduledSupps.length;

    if (totalDistinct == 0) return 0.0;

    int completedItems = 0;
    if (_todayLog != null) {
      for (final entry in _todayLog!.entries) {
        // Only count if it's one of the supplements we actually have scheduled today
        if (scheduledSupps.contains(entry.supplementId)) {
          if (entry.status == LogStatus.taken ||
              entry.status == LogStatus.skipped) {
            completedItems++;
          }
        }
      }
    }

    return completedItems / totalDistinct;
  }

  /// Get count of completed stacks vs total
  String get progressText {
    if (_stacks.isEmpty) return 'No stacks configured';

    int completedStacks = 0;
    for (final stack in _stacks) {
      if (stack.items.isEmpty) continue;

      final allHandled = stack.items.every((item) {
        if (_todayLog == null) return false;
        return _todayLog!.entries.any(
          (e) =>
              e.supplementId == item.supplementId &&
              (e.status == LogStatus.taken || e.status == LogStatus.skipped),
        );
      });

      if (allHandled) {
        completedStacks++;
      }
    }

    return '$completedStacks of ${_stacks.length} stacks completed';
  }

  /// Get the target time for a specific slot
  TimeOfDay getSlotTime(String slot) {
    return _settingsRepository.getSlotTime(slot);
  }

  DailyStackViewModel({
    required StackRepository stackRepository,
    required LogRepository logRepository,
    required SupplementRepository supplementRepository,
    required SettingsRepository settingsRepository,
    required NotificationService notificationService,
    required AuthRepository authRepository,
    required AnalyticsService analyticsService,
    required SoundService soundService,
    required String userId,
  })  : _stackRepository = stackRepository,
        _logRepository = logRepository,
        _supplementRepository = supplementRepository,
        _settingsRepository = settingsRepository,
        _notificationService = notificationService,
        _authRepository = authRepository,
        _analyticsService = analyticsService,
        _soundService = soundService,
        _userId = userId;

  /// Initialize the view model - load stacks, today's log, and streak
  Future<void> initialize() async {
    _setLoading(true);
    _error = null;

    if (_userId.isEmpty) {
      _error = 'User not authenticated';
      _setLoading(false);
      return;
    }

    try {
      AppLogger.i('Initializing DailyStackViewModel for user: $_userId');
      final logicalToday = _getLogicalToday();
      AppLogger.d('Logical today determined as: $logicalToday');

      // Load in parallel with timeouts
      AppLogger.d('Starting parallel data load (Stacks, Log, Streak)...');
      final results = await Future.wait([
        _stackRepository.getUserStacks(_userId),
        _logRepository.getLogForDate(_userId, logicalToday),
        _logRepository.getStreakCount(_userId),
      ]);
      AppLogger.d('Parallel data load complete.');

      _stacks = results[0] as List<SupplementStack>;
      _todayLog = results[1] as DailyLog?;
      _streakCount = results[2] as int;

      // Notify immediately so UI shows structure (with "Loading..." for missing supplements)
      notifyListeners();

      // Cache supplements for display
      await _cacheSupplements();
      notifyListeners();

      // Listen for future updates
      _stackSubscription?.cancel();
      _stackSubscription =
          _stackRepository.watchUserStacks(_userId).listen((updatedStacks) {
        AppLogger.i('Reactive Update: Stacks refreshed from repository.');
        _stacks = List.from(updatedStacks);
        notifyListeners(); // Immediate feedback
        _cacheSupplements().then((_) => notifyListeners()); // Refined feedback
      });

      _snoozedSupplements.clear();

      // Check for achievements on load
      final currentUser = await _authRepository.getCurrentUser();
      if (_streakCount >= 7) {
        await unlockAchievement('7_day_warrior');
      }
      if ((currentUser?.level ?? 1) >= 5) {
        await unlockAchievement('focus_master');
      }
    } catch (e) {
      _error = 'Failed to load daily stack: $e';
      AppLogger.e(_error!);
    } finally {
      _setLoading(false);
    }
  }

  /// Mark a supplement as taken
  Future<void> markSupplementTaken(String supplementId) async {
    _snoozedSupplements.remove(supplementId);
    AppLogger.d('Marking supplement as taken: $supplementId');
    HapticFeedback.mediumImpact();
    _soundService.playSuccess();
    final now = DateTime.now();
    final entry = LogEntry(
      supplementId: supplementId,
      takenAt: now,
      status: LogStatus.taken,
      confidenceScore: 5, // Default to high certainty for manual logs
    );

    await _updateTodayLog(entry);

    await _analyticsService.logEvent('dose_logged', parameters: {
      'supplement_id': supplementId,
      'status': 'taken',
    });

    AppLogger.d('Today log updated for $supplementId');

    // Give 10 XP per supplement taken
    await _incrementUserXP(10);

    // Cancel any active nudges for this supplement
    try {
      await _notificationService.cancelAllSupplementNudges(supplementId);
      await _checkAndCancelGlobalNudges();
    } catch (e) {
      AppLogger.e('Failed to cancel nudges', e);
    }
  }

  Future<void> _incrementUserXP(int amount) async {
    try {
      final user = await _authRepository.getCurrentUser();
      if (user != null) {
        final updatedUser = user.copyWith(xp: user.xp + amount);
        await _authRepository.updateUserProfile(updatedUser);
        AppLogger.d('XP Added: $amount. Total: ${updatedUser.xp}');
      }
    } catch (e) {
      AppLogger.e('Failed to update user XP', e);
    }
  }

  /// Unlock an achievement for the user
  Future<void> unlockAchievement(String achievementId) async {
    try {
      final user = await _authRepository.getCurrentUser();
      if (user != null) {
        if (!user.unlockedAchievements.contains(achievementId)) {
          final updatedAchievements =
              List<String>.from(user.unlockedAchievements)..add(achievementId);
          final updatedUser =
              user.copyWith(unlockedAchievements: updatedAchievements);
          await _authRepository.updateUserProfile(updatedUser);

          await _analyticsService.logEvent('achievement_unlocked', parameters: {
            'achievement_id': achievementId,
          });

          AppLogger.d('Achievement Unlocked: $achievementId');
        }
      }
    } catch (e) {
      AppLogger.e('Failed to unlock achievement', e);
    }
  }

  /// Mark a supplement as skipped
  Future<void> markSupplementSkipped(String supplementId,
      {String? reason}) async {
    _snoozedSupplements.remove(supplementId);
    HapticFeedback.lightImpact();
    final now = DateTime.now();
    final entry = LogEntry(
      supplementId: supplementId,
      takenAt: now,
      status: LogStatus.skipped,
      skippedReason: reason,
    );

    await _updateTodayLog(entry);

    // Cancel any active nudges for this supplement
    try {
      await _notificationService.cancelAllSupplementNudges(supplementId);
      await _checkAndCancelGlobalNudges();
    } catch (e) {
      AppLogger.e('Failed to cancel nudges', e);
    }
  }

  /// Toggle a supplement's taken/skipped status (removes from log if already handled)
  Future<void> toggleSupplement(String supplementId) async {
    final isTaken = isSupplementTaken(supplementId);
    final isSkipped = isSupplementSkipped(supplementId);

    if (isTaken || isSkipped) {
      // Remove the entry (undo / unskip)
      await _deleteFromTodayLog(supplementId);
    } else {
      await markSupplementTaken(supplementId);
    }
  }

  /// Toggle expansion state of a stack
  void toggleStackExpansion(String stackId) {
    if (_collapsedStackIds.contains(stackId)) {
      _collapsedStackIds.remove(stackId);
    } else {
      _collapsedStackIds.add(stackId);
    }

    // Update allCollapsed state
    if (_collapsedStackIds.length == _stacks.length) {
      _allCollapsed = true;
    } else if (_collapsedStackIds.isEmpty) {
      _allCollapsed = false;
    }

    notifyListeners();
  }

  /// Toggle expansion for ALL stacks
  void toggleAllExpansion() {
    if (_allCollapsed) {
      _collapsedStackIds.clear();
      _allCollapsed = false;
    } else {
      // Add all dynamic stack IDs
      for (final stack in _stacks) {
        _collapsedStackIds.add(stack.id);
      }
      // Also add standard dashboard slot IDs to ensure Dashboard collapses too
      _collapsedStackIds.addAll(['morning', 'afternoon', 'evening', 'night']);
      _allCollapsed = true;
    }
    notifyListeners();
  }

  /// Snooze a persistent nudge for a supplement
  Future<void> snoozeSupplement(String supplementId) async {
    final supplement = _supplementCache[supplementId];
    if (supplement == null) return;

    await _notificationService.snoozePersistentNudge(
      supplementId: supplementId,
      title: 'Time for ${supplement.name}',
      body: 'Snoozed for 5 minutes. Don\'t forget your focus stack!',
    );
    _snoozedSupplements.add(supplementId);
    notifyListeners();
  }

  bool isSupplementSnoozed(String supplementId) {
    return _snoozedSupplements.contains(supplementId);
  }

  /// Check if a supplement has been taken today
  bool isSupplementTaken(String supplementId) {
    if (_todayLog == null) return false;
    return _todayLog!.entries.any(
      (e) => e.supplementId == supplementId && e.status == LogStatus.taken,
    );
  }

  /// Check if a supplement has been skipped today
  bool isSupplementSkipped(String supplementId) {
    if (_todayLog == null) return false;
    return _todayLog!.entries.any(
      (e) => e.supplementId == supplementId && e.status == LogStatus.skipped,
    );
  }

  /// Get supplement details from cache
  Supplement? getSupplement(String supplementId) {
    return _supplementCache[supplementId];
  }

  /// Save symptom ratings for today
  Future<void> saveSymptomRatings(Map<String, int> ratings) async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);

    final log = _todayLog ??
        DailyLog(
          id: '${_userId}_${today.toIso8601String()}',
          userId: _userId,
          date: today,
          entries: [],
          createdAt: now,
        );

    final updatedLog = log.copyWith(symptomRatings: ratings);
    await _logRepository.saveLog(updatedLog);
    _todayLog = updatedLog;
    notifyListeners();
  }

  /// Save mood and focus scores for today
  Future<void> saveScores({int? mood, int? focus}) async {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);

    final log = _todayLog ??
        DailyLog(
          id: '${_userId}_${today.toIso8601String()}',
          userId: _userId,
          date: today,
          entries: [],
          createdAt: now,
        );

    final updatedLog = log.copyWith(
      moodScore: mood ?? log.moodScore,
      focusScore: focus ?? log.focusScore,
    );
    await _logRepository.saveLog(updatedLog);
    _todayLog = updatedLog;
    notifyListeners();
  }

  /// Get formatted time status string for a given item
  String? getItemTimeStatus(StackItem item) {
    final supplement = _supplementCache[item.supplementId];
    String? timeStr = item.scheduledTime;

    // If no specific scheduled time, use the slot default
    if (timeStr == null && supplement?.timeOfDay != null) {
      final slot = supplement!.timeOfDay!.toLowerCase();
      if (slot.contains('morning')) {
        timeStr = "08:00";
      } else if (slot.contains('afternoon')) {
        timeStr = "13:00";
      } else if (slot.contains('evening')) {
        timeStr = "18:00";
      } else if (slot.contains('night')) {
        timeStr = "21:00";
      }
    }

    if (timeStr == null) return null;

    try {
      final now = DateTime.now();
      final parts = timeStr.split(':');
      final target = DateTime(now.year, now.month, now.day, int.parse(parts[0]),
          int.parse(parts[1]));
      final diff = target.difference(now);

      if (diff.isNegative) {
        if (diff.abs().inHours > 4) {
          return 'Overdue';
        }
        return 'Overdue by ${diff.abs().inMinutes}m';
      } else {
        if (diff.inHours > 0) {
          return 'in ${diff.inHours}h ${diff.inMinutes % 60}m';
        }
        return 'in ${diff.inMinutes}m';
      }
    } catch (_) {
      return null;
    }
  }

  /// Get formatted time status string for a given time slots
  String? getTimeStatus(String? timeOfDay) {
    if (timeOfDay == null) return null;
    int targetHour;

    // Normalize string
    final slot = timeOfDay.toLowerCase();
    if (!['morning', 'afternoon', 'evening', 'night'].contains(slot)) {
      return null;
    }
    final targetTime = _settingsRepository.getSlotTime(slot);
    targetHour = targetTime.hour;

    final now = DateTime.now();
    final target = DateTime(now.year, now.month, now.day, targetHour);
    final diff = target.difference(now);

    if (diff.isNegative) {
      // If overdue by more than 4 hours, just say "Today" or simplified status
      // But user requested "Time Urgency", so "Overdue" is good.
      if (diff.abs().inHours > 4) {
        return 'Overdue';
      }
      return 'Overdue by ${diff.abs().inMinutes}m';
    } else {
      if (diff.inHours > 0) {
        return 'in ${diff.inHours}h ${diff.inMinutes % 60}m';
      }
      return 'in ${diff.inMinutes}m';
    }
  }

  // Private helpers

  List<StackItem> _getItemsForSlot(String slot) {
    final List<StackItem> items = [];

    for (final stack in _stacks) {
      // Check if stack matches requested slot
      if (stack.timeOfDay?.toLowerCase() == slot.toLowerCase()) {
        for (final item in stack.items) {
          // Check if already in list (for multi-stack duplicates, though rare)
          final exists = items.any((i) => i.supplementId == item.supplementId);
          if (!exists) {
            items.add(item);
          }
        }
      }
    }

    return items;
  }

  Future<void> _updateTodayLog(LogEntry entry) async {
    final now = DateTime.now();
    final logicalToday = _getLogicalToday();

    List<LogEntry> entries;
    if (_todayLog != null) {
      // Replace existing entry for same supplement, or add new
      entries = _todayLog!.entries
          .where((e) => e.supplementId != entry.supplementId)
          .toList();
      entries.add(entry);
    } else {
      entries = [entry];
    }

    final log = _todayLog?.copyWith(entries: entries) ??
        DailyLog(
          id: '${_userId}_${logicalToday.toIso8601String().split('T').first}',
          userId: _userId,
          date: logicalToday,
          entries: entries,
          createdAt: now,
        );

    try {
      // Update local state and notify immediately for responsiveness
      _todayLog = log;
      notifyListeners();

      // Persist in background
      await _logRepository.saveLog(log);
    } catch (e) {
      _error = 'Failed to save log: $e';
      notifyListeners();
    }
  }

  /// Remove an entry from today's log for a specific supplement
  Future<void> _deleteFromTodayLog(String supplementId) async {
    if (_todayLog == null) return;

    final updatedEntries = _todayLog!.entries
        .where((e) => e.supplementId != supplementId)
        .toList();

    final updatedLog = _todayLog!.copyWith(entries: updatedEntries);

    try {
      _todayLog = updatedLog;
      notifyListeners();
      await _logRepository.saveLog(updatedLog);
    } catch (e) {
      _error = 'Failed to update log: $e';
      notifyListeners();
    }
  }

  /// Automatically cancel global reminders if everything is done for the day
  Future<void> _checkAndCancelGlobalNudges() async {
    if (_stacks.isEmpty) return;

    // Check if ALL items in ALL stacks are handled (taken or skipped)
    final allHandled = _stacks.expand((s) => s.items).every((item) {
      if (_todayLog == null) return false;
      return _todayLog!.entries.any(
        (e) =>
            e.supplementId == item.supplementId &&
            (e.status == LogStatus.taken || e.status == LogStatus.skipped),
      );
    });

    if (allHandled) {
      AppLogger.d(
          'Smart Nudge: All items handled. Canceling all remaining nudges for today.');

      // Cancel all global nudge notifications for today
      await _notificationService.cancelNotification(1000);
      await _notificationService.cancelNotification(1001);
      await _notificationService.cancelNotification(1002);
    }
  }

  DateTime _getLogicalToday() {
    // Centralized 4 AM rollover logic from date_utils.dart
    final now = DateTime.now();
    if (now.hour < 4) {
      return DateTime(now.year, now.month, now.day)
          .subtract(const Duration(days: 1));
    }
    return DateTime(now.year, now.month, now.day);
  }

  Future<void> _cacheSupplements() async {
    AppLogger.d('Caching supplements...');
    final supplementIds = <String>{};
    for (final stack in _stacks) {
      for (final item in stack.items) {
        if (!_supplementCache.containsKey(item.supplementId) &&
            item.supplementId.isNotEmpty) {
          supplementIds.add(item.supplementId);
        }
      }
    }

    if (supplementIds.isEmpty) return;

    AppLogger.d('Parallel fetching ${supplementIds.length} supplements...');

    await Future.wait(supplementIds.map((id) async {
      try {
        final supplement =
            await _supplementRepository.getSupplement(id, userId: _userId);
        if (supplement != null) {
          _supplementCache[id] = supplement;
        }
      } catch (e) {
        AppLogger.e('Failed to load supplement $id', e);
      }
    }));
  }

  @override
  void dispose() {
    _isDisposed = true;
    _stackSubscription?.cancel();
    super.dispose();
  }

  @override
  void notifyListeners() {
    if (!_isDisposed) {
      super.notifyListeners();
    }
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}

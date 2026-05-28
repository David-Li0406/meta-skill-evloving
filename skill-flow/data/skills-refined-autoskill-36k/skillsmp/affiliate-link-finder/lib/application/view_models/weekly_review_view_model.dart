import 'package:flutter/foundation.dart';
import '../../domain/repositories/log_repository.dart';
import '../../utils/logger.dart';
import '../../domain/entities/daily_log.dart';
import '../../config/locator.dart';

class WeeklyReviewViewModel extends ChangeNotifier {
  final LogRepository _logRepository;
  final String _userId;

  bool _isLoading = false;
  // ignore: unused_field
  List<DailyLog> _weeklyLogs = [];
  Map<String, int> _consistencyMap =
      {}; // "Mon" -> 1 (Complete), 0 (Missed), 2 (Grace)
  int _streakDays = 0;
  double _focusImprovement = 0.0;

  bool get isLoading => _isLoading;
  int get streakDays => _streakDays;
  double get focusImprovement => _focusImprovement;
  Map<String, int> get consistencyMap => _consistencyMap;

  WeeklyReviewViewModel({
    required LogRepository logRepository,
    required String userId,
  })  : _logRepository = logRepository,
        _userId = userId;

  factory WeeklyReviewViewModel.withParams(String userId) {
    return WeeklyReviewViewModel(
      logRepository: locator<LogRepository>(),
      userId: userId,
    );
  }

  Future<void> fetchWeeklyStats() async {
    _isLoading = true;
    notifyListeners();

    try {
      // final now = DateTime.now(); // Unused
      // Get last 14 days to compare weeks
      _weeklyLogs = await _logRepository.getRecentLogs(_userId, 14);

      _calculateConsistency();
      _calculateStreak();
      _calculateFocusImprovement();
    } catch (e) {
      AppLogger.e('Error fetching weekly stats', e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _calculateConsistency() {
    // 0 = Missed, 1 = Complete, 2 = Grace
    final now = DateTime.now();
    final Map<String, int> consistency = {};
    final weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

    // We want the last 7 days ending today or yesterday? Usually a generic week view.
    // Let's assume we show the last 7 days relative to today.
    for (int i = 6; i >= 0; i--) {
      final dateToCheck = now.subtract(Duration(days: i));
      final dayName = weekDays[dateToCheck.weekday - 1]; // weekday is 1-7

      // Find log for this date
      final log = _weeklyLogs.firstWhere(
        (l) =>
            l.date.year == dateToCheck.year &&
            l.date.month == dateToCheck.month &&
            l.date.day == dateToCheck.day,
        orElse: () => DailyLog(
            id: '',
            userId: '',
            date: dateToCheck,
            entries: [],
            createdAt: DateTime.now()),
      );

      if (log.entries.isNotEmpty &&
          log.entries.any((e) => e.status == LogStatus.taken)) {
        consistency[dayName] = 1;
      } else if (log.entries.isNotEmpty &&
          log.entries.any((e) => e.status == LogStatus.skipped)) {
        consistency[dayName] = 2; // Grace/Skipped
      } else {
        consistency[dayName] = 0; // Missed
      }
    }
    _consistencyMap = consistency;
  }

  void _calculateStreak() {
    // Calculate streak from the logs we have (up to 14 days)
    int streak = 0;
    final now = DateTime.now();
    // Sort logs by date desc just in case
    final sortedLogs = List<DailyLog>.from(_weeklyLogs)
      ..sort((a, b) => b.date.compareTo(a.date));

    // Simple check: for each day back from today, is there a complete log?
    for (int i = 0; i < 14; i++) {
      final dateToCheck = now.subtract(Duration(days: i));
      final hasLog = sortedLogs.any((l) =>
          l.date.year == dateToCheck.year &&
          l.date.month == dateToCheck.month &&
          l.date.day == dateToCheck.day &&
          l.entries.any((e) => e.status == LogStatus.taken));

      if (hasLog) {
        streak++;
      } else {
        // If it's today and we haven't logged yet, don't break streak immediately if we are just checking history?
        // But for "current streak", if today is missing, it might still be valid if yesterday was done.
        // Let's keep it simple: strict consecutive days.
        if (i == 0) continue; // Allow today to be incomplete
        break;
      }
    }
    _streakDays = streak;
  }

  void _calculateFocusImprovement() {
    if (_weeklyLogs.isEmpty) {
      _focusImprovement = 0.0;
      return;
    }

    final now = DateTime.now();
    final lastWeekStart = now.subtract(const Duration(days: 7));

    final thisWeekLogs =
        _weeklyLogs.where((l) => l.date.isAfter(lastWeekStart)).toList();
    final prevWeekLogs =
        _weeklyLogs.where((l) => l.date.isBefore(lastWeekStart)).toList();

    double getAvg(List<DailyLog> logs) {
      if (logs.isEmpty) return 0.0;
      final scores = logs
          .where((l) => l.focusScore != null)
          .map((l) => l.focusScore!)
          .toList();
      if (scores.isEmpty) return 0.0;
      return scores.reduce((a, b) => a + b) / scores.length;
    }

    final thisWeekAvg = getAvg(thisWeekLogs);
    final prevWeekAvg = getAvg(prevWeekLogs);

    if (prevWeekAvg == 0) {
      _focusImprovement = thisWeekAvg > 0 ? 100.0 : 0.0;
    } else {
      _focusImprovement = ((thisWeekAvg - prevWeekAvg) / prevWeekAvg) * 100;
    }
  }
}

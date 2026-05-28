import '../../domain/entities/daily_log.dart';
import '../../domain/entities/streak.dart';

class StreakService {
  /// Calculate current streak from daily logs
  /// Returns updated Streak object
  Streak calculateStreak({
    required Streak currentStreak,
    required List<DailyLog> recentLogs,
  }) {
    // Sort logs by date descending
    final sortedLogs = List<DailyLog>.from(recentLogs)
      ..sort((a, b) => b.date.compareTo(a.date));

    final today = DateTime.now();
    final yesterday = today.subtract(const Duration(days: 1));

    // Check if user completed today
    final todayLog = sortedLogs.firstWhere(
      (log) => _isSameDay(log.date, today),
      orElse: () => DailyLog(
        id: '',
        userId: currentStreak.userId,
        date: today,
        entries: [],
        createdAt: today,
      ),
    );

    final completedToday = _isLogComplete(todayLog);

    // final completedYesterday = _isLogComplete(yesterdayLog);

    // Calculate new streak
    int newStreak = currentStreak.currentStreak;
    DateTime? newLastCompleted = currentStreak.lastCompletedDate;
    int newGraceDaysRemaining = currentStreak.graceDaysRemaining;
    int newGraceDaysUsed = currentStreak.graceDaysUsed;

    if (completedToday) {
      // User completed today
      if (currentStreak.lastCompletedDate == null ||
          _isSameDay(currentStreak.lastCompletedDate!, yesterday)) {
        // Continue streak
        newStreak = currentStreak.currentStreak + 1;
      } else if (!_isSameDay(currentStreak.lastCompletedDate!, today)) {
        // New streak started
        newStreak = 1;
      }
      newLastCompleted = today;
    } else if (!completedToday &&
        currentStreak.lastCompletedDate != null &&
        _isSameDay(currentStreak.lastCompletedDate!, yesterday)) {
      // User missed today but completed yesterday
      // Check if grace day should be applied
      if (newGraceDaysRemaining > 0) {
        // Apply grace day - streak continues
        newGraceDaysRemaining--;
        newGraceDaysUsed++;
      } else {
        // No grace days left - reset streak
        newStreak = 0;
        newLastCompleted = null;
      }
    }

    final newLongestStreak = newStreak > currentStreak.longestStreak
        ? newStreak
        : currentStreak.longestStreak;

    return currentStreak.copyWith(
      currentStreak: newStreak,
      longestStreak: newLongestStreak,
      lastCompletedDate: newLastCompleted,
      graceDaysRemaining: newGraceDaysRemaining,
      graceDaysUsed: newGraceDaysUsed,
      updatedAt: DateTime.now(),
    );
  }

  /// Check if grace day should be applied
  bool shouldApplyGraceDay({
    required Streak streak,
    required DateTime missedDate,
  }) {
    if (streak.graceDaysRemaining <= 0) {
      return false;
    }

    if (streak.lastCompletedDate == null) {
      return false;
    }

    final daysSinceLastCompleted =
        missedDate.difference(streak.lastCompletedDate!).inDays;

    // Grace day only applies if user missed exactly 1 day
    return daysSinceLastCompleted == 1;
  }

  /// Reset grace days (typically at start of month)
  Streak resetGraceDays(Streak streak, {int graceDaysPerMonth = 2}) {
    return streak.copyWith(
      graceDaysRemaining: graceDaysPerMonth,
      graceDaysUsed: 0,
      updatedAt: DateTime.now(),
    );
  }

  /// Check if a daily log is considered "complete"
  /// A log is complete if user has taken at least one supplement
  bool _isLogComplete(DailyLog log) {
    if (log.entries.isEmpty) {
      return false;
    }

    return log.entries.any((entry) => entry.status == LogStatus.taken);
  }

  /// Check if two dates are the same day
  bool _isSameDay(DateTime a, DateTime b) {
    return a.year == b.year && a.month == b.month && a.day == b.day;
  }
}

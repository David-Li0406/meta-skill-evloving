import '../entities/daily_log.dart';

abstract class LogRepository {
  /// Get logs for a specific date range
  Future<List<DailyLog>> getLogsByDateRange(
      String userId, DateTime start, DateTime end);

  /// Get log for a specific date
  Future<DailyLog?> getLogForDate(String userId, DateTime date);

  /// Create or update a daily log
  Future<void> saveLog(DailyLog log);

  /// Get the current streak count
  Future<int> getStreakCount(String userId);

  /// Get logs for the last N days
  Future<List<DailyLog>> getRecentLogs(String userId, int days);

  /// Stream of today's log (real-time updates)
  Stream<DailyLog?> watchTodayLog(String userId);

  /// Delete all logs for a user (Privacy/Data Reset)
  Future<void> clearAllLogs(String userId);
}

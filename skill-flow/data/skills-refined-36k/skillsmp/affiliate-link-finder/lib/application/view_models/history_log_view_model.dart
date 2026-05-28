import 'package:flutter/foundation.dart';
import '../../domain/entities/daily_log.dart';
import '../../domain/repositories/log_repository.dart';
import '../../utils/logger.dart';
import '../../domain/repositories/stack_repository.dart';
import '../../config/locator.dart';

/// View model for the History Log screen
/// Manages historical logs and filtering by date/status
class HistoryLogViewModel extends ChangeNotifier {
  final LogRepository _logRepository;
  final StackRepository? _stackRepository;
  final String _userId;

  // State
  List<DailyLog> _recentLogs = [];
  String _selectedFilter = 'All'; // All, Missed, Taken, Dismissed
  bool _isLoading = false;
  String? _error;
  bool _isDisposed = false;

  // Getters
  List<DailyLog> get recentLogs => _recentLogs;
  List<DailyLog> get logs => _recentLogs; // Compatibility getter
  String get selectedFilter => _selectedFilter;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Group logs by date sections (Today, Yesterday, This Week, etc.)
  Map<String, List<DailyLog>> get groupedLogs {
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);
    final yesterday = today.subtract(const Duration(days: 1));

    final groups = <String, List<DailyLog>>{};

    for (final log in _recentLogs) {
      final logDate = DateTime(log.date.year, log.date.month, log.date.day);

      String groupKey;
      if (logDate == today) {
        groupKey = 'Earlier Today';
      } else if (logDate == yesterday) {
        groupKey = 'Yesterday';
      } else if (logDate.isAfter(today.subtract(const Duration(days: 7)))) {
        groupKey = 'This Week';
      } else {
        groupKey = 'Earlier';
      }

      groups.putIfAbsent(groupKey, () => []);
      groups[groupKey]!.add(log);
    }

    return groups;
  }

  /// Calculate completion stats
  Map<String, dynamic> get stats {
    int totalEntries = 0;
    int takenCount = 0;
    int missedCount = 0;

    for (final log in _recentLogs) {
      for (final entry in log.entries) {
        totalEntries++;
        if (entry.status == LogStatus.taken) {
          takenCount++;
        } else {
          missedCount++;
        }
      }
    }

    final completionRate =
        totalEntries > 0 ? (takenCount / totalEntries * 100).round() : 0;

    return {
      'total': totalEntries,
      'taken': takenCount,
      'missed': missedCount,
      'completionRate': completionRate,
    };
  }

  HistoryLogViewModel({
    required LogRepository logRepository,
    StackRepository? stackRepository,
    required String userId,
  })  : _logRepository = logRepository,
        _stackRepository = stackRepository,
        _userId = userId;

  factory HistoryLogViewModel.withParams(String userId) {
    return HistoryLogViewModel(
      logRepository: locator<LogRepository>(),
      stackRepository: locator<StackRepository>(),
      userId: userId,
    );
  }

  /// Initialize - load recent logs
  Future<void> initialize({int days = 30}) async {
    await fetchHistory(days: days);
  }

  /// Core fetch history method
  Future<void> fetchHistory({int days = 30}) async {
    _setLoading(true);
    _error = null;

    try {
      final fetchedLogs = await _logRepository.getRecentLogs(_userId, days);
      _recentLogs = List<DailyLog>.from(fetchedLogs);
      _recentLogs.sort((a, b) => b.date.compareTo(a.date)); // Most recent first
    } catch (e) {
      _error = 'Failed to load history: $e';
      AppLogger.e(_error ?? 'Failed to load history');
    } finally {
      _setLoading(false);
    }
  }

  /// Load logs for a specific date range
  Future<void> loadDateRange(DateTime start, DateTime end) async {
    _setLoading(true);
    _error = null;

    try {
      final fetchedLogs =
          await _logRepository.getLogsByDateRange(_userId, start, end);
      _recentLogs = List<DailyLog>.from(fetchedLogs);
      _recentLogs.sort((a, b) => b.date.compareTo(a.date));
    } catch (e) {
      _error = 'Failed to load history: $e';
    } finally {
      _setLoading(false);
    }
  }

  /// Resolve all missed items for today
  Future<void> resolveAllMissed() async {
    if (_stackRepository == null) return;

    _setLoading(true);
    try {
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);

      // 1. Get today's log or create a new one
      var log = await _logRepository.getLogForDate(_userId, today) ??
          DailyLog(
            id: '${_userId}_${today.toIso8601String()}',
            userId: _userId,
            date: today,
            entries: [],
            createdAt: now,
          );

      // 2. Get user stacks to find what SHOULD have been taken
      final stacks = await _stackRepository!.getUserStacks(_userId);
      final allScheduledItems = stacks.expand((s) => s.items).toList();

      // 3. Identify missed items (scheduled but no entry)
      bool changed = false;
      final existingIds = log.entries.map((e) => e.supplementId).toSet();

      final newEntries = List<LogEntry>.from(log.entries);

      for (final item in allScheduledItems) {
        if (!existingIds.contains(item.supplementId)) {
          // Check if scheduled time has passed
          if (_isTimePassed(item.scheduledTime)) {
            newEntries.add(LogEntry(
              supplementId: item.supplementId,
              takenAt: now,
              status: LogStatus.late,
              skippedReason: 'Acknowledged missed reminder',
            ));
            changed = true;
          }
        }
      }

      if (changed) {
        await _logRepository.saveLog(log.copyWith(entries: newEntries));
        await fetchHistory();
      }
    } catch (e) {
      _error = 'Failed to resolve items: $e';
    } finally {
      _setLoading(false);
    }
  }

  bool _isTimePassed(String? scheduledTime) {
    if (scheduledTime == null) return false;
    try {
      final parts = scheduledTime.split(':');
      final hour = int.parse(parts[0]);
      final minute = int.parse(parts[1]);
      final now = DateTime.now();

      if (now.hour > hour) return true;
      if (now.hour == hour && now.minute >= minute) return true;
    } catch (_) {}
    return false;
  }

  /// Filter by status (All, Missed, Taken, Dismissed)
  void setFilter(String filter) {
    _selectedFilter = filter;
    notifyListeners();
  }

  /// Get filtered entries based on selected filter
  List<LogEntry> getFilteredEntries(DailyLog log) {
    if (_selectedFilter == 'All') {
      return log.entries;
    }

    return log.entries.where((entry) {
      switch (_selectedFilter) {
        case 'Taken':
          return entry.status == LogStatus.taken;
        case 'Missed':
          return entry.status == LogStatus.skipped &&
              entry.skippedReason == null;
        case 'Dismissed':
          return entry.status == LogStatus.skipped &&
              entry.skippedReason != null;
        default:
          return true;
      }
    }).toList();
  }

  // Private helpers

  @override
  void dispose() {
    _isDisposed = true;
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

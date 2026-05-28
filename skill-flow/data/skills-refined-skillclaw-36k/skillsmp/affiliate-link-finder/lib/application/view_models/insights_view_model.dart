import 'package:flutter/foundation.dart';
import '../../utils/logger.dart';
import '../../domain/repositories/log_repository.dart';

/// ViewModel for the Insights Screen.
///
/// Responsible for calculating user consistency, tracking streaks,
/// and providing encouragement based on user progress.
///
/// Principles:
/// - **Dopamine**: Provide immediate positive feedback (streaks, encouragement).
/// - **Simplicity**: Abstract complex data into simple percentages.
class InsightsViewModel extends ChangeNotifier {
  final LogRepository _logRepository;
  final String _userId;

  bool _isLoading = true;
  bool get isLoading => _isLoading;

  int _streakCount = 0;
  int get streakCount => _streakCount;

  double _consistencyScore = 0.0;
  double get consistencyScore => _consistencyScore;

  String _encouragementText = "Start your journey!";
  String get encouragementText => _encouragementText;

  // For the chart - focused on simplified monthly view for now
  // We could expand this to be a list of daily focus scores if needed
  // but for V1 we keep it simple as per "Rule of One" / Low Cognitive Load
  final List<double> _weeklyFocusScores = [];
  List<double> get weeklyFocusScores => _weeklyFocusScores;

  InsightsViewModel({
    required LogRepository logRepository,
    required String userId,
  })  : _logRepository = logRepository,
        _userId = userId {
    loadData();
  }

  Future<void> loadData() async {
    _isLoading = true;
    notifyListeners();

    try {
      // 1. Get current streak
      _streakCount = await _logRepository.getStreakCount(_userId);

      // 2. Calculate Consistency (Last 30 days)
      final now = DateTime.now();
      final thirtyDaysAgo = now.subtract(const Duration(days: 30));
      final logs = await _logRepository.getLogsByDateRange(
        _userId,
        thirtyDaysAgo,
        now,
      );

      // Simple consistency: Days logged / 30
      final daysLogged = logs.length;
      _consistencyScore = (daysLogged / 30) * 100;
      if (_consistencyScore > 100) _consistencyScore = 100;

      // 3. Calculate Weekly Focus Trends (Last 7 days)
      _weeklyFocusScores.clear();
      for (int i = 6; i >= 0; i--) {
        final date =
            DateTime(now.year, now.month, now.day).subtract(Duration(days: i));

        // Find log for this specific date
        // Use where to ensure we get the right type
        final logsForDate = logs.where((l) =>
            l.date.year == date.year &&
            l.date.month == date.month &&
            l.date.day == date.day);

        final logForDate = logsForDate.isNotEmpty ? logsForDate.first : null;

        // If no log or no focus score, default to 0
        _weeklyFocusScores.add((logForDate?.focusScore ?? 0).toDouble());
      }

      // 4. Set Encouragement Text
      _updateEncouragement();
    } catch (e) {
      AppLogger.e('Error loading insights', e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void _updateEncouragement() {
    if (_streakCount == 0) {
      _encouragementText = "Start your journey today!";
    } else if (_streakCount < 3) {
      _encouragementText = "You're off to a great start!";
    } else if (_streakCount < 7) {
      _encouragementText = "Keep up the momentum! 🔥";
    } else if (_streakCount < 14) {
      _encouragementText = "You're on fire! One week down! 🚀";
    } else if (_streakCount < 30) {
      _encouragementText = "Consistency is key. You're analyzing it! 🧠";
    } else {
      _encouragementText = "Unstoppable! You've built a solid habit. 🏆";
    }
  }
}

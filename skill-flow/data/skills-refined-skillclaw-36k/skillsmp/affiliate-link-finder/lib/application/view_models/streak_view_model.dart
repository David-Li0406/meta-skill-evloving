import 'package:flutter/foundation.dart';
import '../../utils/logger.dart';
import '../../domain/entities/daily_log.dart';
import '../../domain/entities/streak.dart';
import '../../domain/repositories/streak_repository.dart';
import '../../infrastructure/services/streak_service.dart';

class StreakViewModel extends ChangeNotifier {
  final StreakService _streakService;
  final StreakRepository _streakRepository;

  Streak? _currentStreak;
  bool _isLoading = false;
  String? _error;

  StreakViewModel(this._streakService, this._streakRepository);

  Streak? get currentStreak => _currentStreak;
  bool get isLoading => _isLoading;
  String? get error => _error;

  /// Initialize streak for a user
  void initializeStreak(String userId) {
    _currentStreak = Streak.initial(userId);
    notifyListeners();
  }

  /// Update streak based on daily logs
  Future<void> updateStreak({
    required List<DailyLog> recentLogs,
  }) async {
    if (_currentStreak == null) {
      _error = 'Streak not initialized';
      notifyListeners();
      return;
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _currentStreak = _streakService.calculateStreak(
        currentStreak: _currentStreak!,
        recentLogs: recentLogs,
      );

      await saveStreak();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Apply grace day manually (if user wants to use it)
  void applyGraceDay() {
    if (_currentStreak == null) {
      _error = 'Streak not initialized';
      notifyListeners();
      return;
    }

    if (_currentStreak!.graceDaysRemaining <= 0) {
      _error = 'No grace days remaining';
      notifyListeners();
      return;
    }

    _currentStreak = _currentStreak!.copyWith(
      graceDaysRemaining: _currentStreak!.graceDaysRemaining - 1,
      graceDaysUsed: _currentStreak!.graceDaysUsed + 1,
      updatedAt: DateTime.now(),
    );

    notifyListeners();
  }

  /// Reset grace days (typically at start of month)
  void resetGraceDays({int graceDaysPerMonth = 2}) {
    if (_currentStreak == null) {
      _error = 'Streak not initialized';
      notifyListeners();
      return;
    }

    _currentStreak = _streakService.resetGraceDays(
      _currentStreak!,
      graceDaysPerMonth: graceDaysPerMonth,
    );

    notifyListeners();
  }

  /// Load streak from storage
  Future<void> loadStreak(String userId) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _currentStreak = await _streakRepository.getStreak(userId);

      // If no streak exists yet, initialize it
      if (_currentStreak == null) {
        _currentStreak = Streak.initial(userId);
        await saveStreak();
      }

      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Save streak to storage
  Future<void> saveStreak() async {
    if (_currentStreak == null) {
      return;
    }

    try {
      await _streakRepository.saveStreak(_currentStreak!);
      AppLogger.d(
          'Streak saved successfully for user: ${_currentStreak!.userId}');
    } catch (e) {
      _error = e.toString();
      notifyListeners();
    }
  }
}

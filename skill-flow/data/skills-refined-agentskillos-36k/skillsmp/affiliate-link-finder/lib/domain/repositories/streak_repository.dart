import '../entities/streak.dart';

abstract class StreakRepository {
  /// Get user's current streak info
  Future<Streak?> getStreak(String userId);

  /// Save/Update user's streak info
  Future<void> saveStreak(Streak streak);

  /// Stream of streak changes
  Stream<Streak?> watchStreak(String userId);
}

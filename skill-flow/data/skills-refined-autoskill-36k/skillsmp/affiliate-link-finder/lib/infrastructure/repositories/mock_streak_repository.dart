import '../../domain/entities/streak.dart';
import '../../domain/repositories/streak_repository.dart';

class MockStreakRepository implements StreakRepository {
  final Map<String, Streak> _streaks = {};

  @override
  Future<Streak?> getStreak(String userId) async {
    await Future<void>.delayed(const Duration(milliseconds: 200));
    return _streaks[userId];
  }

  @override
  Future<void> saveStreak(Streak streak) async {
    await Future<void>.delayed(const Duration(milliseconds: 100));
    _streaks[streak.userId] = streak;
  }

  @override
  Stream<Streak?> watchStreak(String userId) async* {
    yield _streaks[userId];
    // In a real mock, we might want a StreamController here
  }
}

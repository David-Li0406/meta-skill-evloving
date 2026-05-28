import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'package:adhd_supplement_app/domain/entities/streak.dart';
import 'package:adhd_supplement_app/infrastructure/services/streak_service.dart';

void main() {
  late StreakService streakService;

  setUp(() {
    streakService = StreakService();
  });

  group('StreakService', () {
    group('calculateStreak', () {
      test('should increment streak when user completes today', () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: yesterday,
        );

        final todayLog = DailyLog(
          id: 'log1',
          userId: 'user1',
          date: today,
          entries: [
            LogEntry(
              supplementId: 'sup1',
              takenAt: today,
              status: LogStatus.taken,
            ),
          ],
          createdAt: today,
        );

        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [todayLog],
        );

        expect(result.currentStreak, 6);
        expect(result.lastCompletedDate?.day, today.day);
      });

      test('should start new streak when user completes after a gap', () {
        final today = DateTime.now();
        final threeDaysAgo = today.subtract(const Duration(days: 3));

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: threeDaysAgo,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: threeDaysAgo,
        );

        final todayLog = DailyLog(
          id: 'log1',
          userId: 'user1',
          date: today,
          entries: [
            LogEntry(
              supplementId: 'sup1',
              takenAt: today,
              status: LogStatus.taken,
            ),
          ],
          createdAt: today,
        );

        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [todayLog],
        );

        expect(result.currentStreak, 1);
        expect(result.lastCompletedDate?.day, today.day);
      });

      test(
          'should apply grace day when user misses today but completed yesterday',
          () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: yesterday,
        );

        // No log for today (user missed it)
        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [],
        );

        expect(result.graceDaysRemaining, 1);
        expect(result.graceDaysUsed, 1);
        expect(result.currentStreak, 5); // Streak preserved
      });

      test('should reset streak when grace days exhausted', () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 0, // No grace days left
          graceDaysUsed: 2,
          updatedAt: yesterday,
        );

        // No log for today (user missed it)
        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [],
        );

        expect(result.currentStreak, 0);
        expect(result.lastCompletedDate, null);
      });

      test('should update longest streak when current exceeds it', () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 10,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: yesterday,
        );

        final todayLog = DailyLog(
          id: 'log1',
          userId: 'user1',
          date: today,
          entries: [
            LogEntry(
              supplementId: 'sup1',
              takenAt: today,
              status: LogStatus.taken,
            ),
          ],
          createdAt: today,
        );

        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [todayLog],
        );

        expect(result.currentStreak, 11);
        expect(result.longestStreak, 11);
      });

      test('should not increment if user already completed today', () {
        final today = DateTime.now();

        final currentStreak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: today,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: today,
        );

        final todayLog = DailyLog(
          id: 'log1',
          userId: 'user1',
          date: today,
          entries: [
            LogEntry(
              supplementId: 'sup1',
              takenAt: today,
              status: LogStatus.taken,
            ),
          ],
          createdAt: today,
        );

        final result = streakService.calculateStreak(
          currentStreak: currentStreak,
          recentLogs: [todayLog],
        );

        expect(result.currentStreak, 5); // No change
        expect(result.lastCompletedDate?.day, today.day);
      });
    });

    group('shouldApplyGraceDay', () {
      test(
          'should return true when user has grace days and missed exactly 1 day',
          () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final streak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: yesterday,
        );

        final result = streakService.shouldApplyGraceDay(
          streak: streak,
          missedDate: today,
        );

        expect(result, true);
      });

      test('should return false when user has no grace days remaining', () {
        final today = DateTime.now();
        final yesterday = today.subtract(const Duration(days: 1));

        final streak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: yesterday,
          graceDaysRemaining: 0,
          graceDaysUsed: 2,
          updatedAt: yesterday,
        );

        final result = streakService.shouldApplyGraceDay(
          streak: streak,
          missedDate: today,
        );

        expect(result, false);
      });

      test('should return false when user never completed before', () {
        final today = DateTime.now();

        final streak = Streak(
          userId: 'user1',
          currentStreak: 0,
          longestStreak: 0,
          lastCompletedDate: null,
          graceDaysRemaining: 2,
          graceDaysUsed: 0,
          updatedAt: today,
        );

        final result = streakService.shouldApplyGraceDay(
          streak: streak,
          missedDate: today,
        );

        expect(result, false);
      });
    });

    group('resetGraceDays', () {
      test('should reset grace days to default value', () {
        final streak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: DateTime.now(),
          graceDaysRemaining: 0,
          graceDaysUsed: 2,
          updatedAt: DateTime.now(),
        );

        final result = streakService.resetGraceDays(streak);

        expect(result.graceDaysRemaining, 2);
        expect(result.graceDaysUsed, 0);
      });

      test('should allow custom grace days per month', () {
        final streak = Streak(
          userId: 'user1',
          currentStreak: 5,
          longestStreak: 10,
          lastCompletedDate: DateTime.now(),
          graceDaysRemaining: 0,
          graceDaysUsed: 3,
          updatedAt: DateTime.now(),
        );

        final result =
            streakService.resetGraceDays(streak, graceDaysPerMonth: 3);

        expect(result.graceDaysRemaining, 3);
        expect(result.graceDaysUsed, 0);
      });
    });
  });
}

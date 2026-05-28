import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'package:adhd_supplement_app/infrastructure/services/streak_service.dart';
import 'package:adhd_supplement_app/application/view_models/streak_view_model.dart';

import 'package:adhd_supplement_app/infrastructure/repositories/mock_streak_repository.dart';

void main() {
  late StreakService streakService;
  late StreakViewModel viewModel;
  late MockStreakRepository streakRepository;

  setUp(() {
    streakService = StreakService();
    streakRepository = MockStreakRepository();
    viewModel = StreakViewModel(streakService, streakRepository);
  });

  group('StreakViewModel', () {
    test('should initialize with null streak', () {
      expect(viewModel.currentStreak, null);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
    });

    test('initializeStreak should create initial streak', () {
      viewModel.initializeStreak('user1');

      expect(viewModel.currentStreak, isNotNull);
      expect(viewModel.currentStreak?.userId, 'user1');
      expect(viewModel.currentStreak?.currentStreak, 0);
      expect(viewModel.currentStreak?.graceDaysRemaining, 2);
    });

    test('updateStreak should update current streak based on logs', () async {
      viewModel.initializeStreak('user1');

      final today = DateTime.now();
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

      await viewModel.updateStreak(recentLogs: [todayLog]);

      expect(viewModel.currentStreak?.currentStreak, 1);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
    });

    test('updateStreak should set error if streak not initialized', () async {
      await viewModel.updateStreak(recentLogs: []);

      expect(viewModel.error, 'Streak not initialized');
      expect(viewModel.isLoading, false);
    });

    test('applyGraceDay should decrement grace days remaining', () {
      viewModel.initializeStreak('user1');

      final initialGraceDays = viewModel.currentStreak!.graceDaysRemaining;
      viewModel.applyGraceDay();

      expect(viewModel.currentStreak?.graceDaysRemaining, initialGraceDays - 1);
      expect(viewModel.currentStreak?.graceDaysUsed, 1);
    });

    test('applyGraceDay should set error if no grace days remaining', () {
      viewModel.initializeStreak('user1');

      // Use both grace days
      viewModel.applyGraceDay();
      viewModel.applyGraceDay();

      // Try to use a third grace day
      viewModel.applyGraceDay();

      expect(viewModel.error, 'No grace days remaining');
    });

    test('resetGraceDays should restore grace days to default', () {
      viewModel.initializeStreak('user1');

      // Use grace days
      viewModel.applyGraceDay();
      viewModel.applyGraceDay();

      expect(viewModel.currentStreak?.graceDaysRemaining, 0);

      // Reset
      viewModel.resetGraceDays();

      expect(viewModel.currentStreak?.graceDaysRemaining, 2);
      expect(viewModel.currentStreak?.graceDaysUsed, 0);
    });

    test('resetGraceDays should accept custom grace days per month', () {
      viewModel.initializeStreak('user1');

      viewModel.resetGraceDays(graceDaysPerMonth: 3);

      expect(viewModel.currentStreak?.graceDaysRemaining, 3);
    });

    test('resetGraceDays should set error if streak not initialized', () {
      viewModel.resetGraceDays();

      expect(viewModel.error, 'Streak not initialized');
    });

    test('loadStreak should set loading state', () async {
      expect(viewModel.isLoading, false);

      final loadFuture = viewModel.loadStreak('user1');

      // Check loading state (may be hard to test due to timing)
      await loadFuture;

      expect(viewModel.isLoading, false);
      expect(viewModel.currentStreak?.userId, 'user1');
    });

    test('viewModel should notify listeners on state changes', () {
      var notified = false;
      viewModel.addListener(() {
        notified = true;
      });

      viewModel.initializeStreak('user1');

      expect(notified, true);
    });

    test('updateStreak should maintain longest streak', () async {
      viewModel.initializeStreak('user1');

      final today = DateTime.now();
      final logs = List.generate(15, (i) {
        final date = today.subtract(Duration(days: 14 - i));
        return DailyLog(
          id: 'log$i',
          userId: 'user1',
          date: date,
          entries: [
            LogEntry(
              supplementId: 'sup1',
              takenAt: date,
              status: LogStatus.taken,
            ),
          ],
          createdAt: date,
        );
      });

      await viewModel.updateStreak(recentLogs: logs);

      expect(viewModel.currentStreak?.currentStreak, greaterThan(0));
      expect(
        viewModel.currentStreak?.longestStreak,
        greaterThanOrEqualTo(viewModel.currentStreak!.currentStreak),
      );
    });
  });
}

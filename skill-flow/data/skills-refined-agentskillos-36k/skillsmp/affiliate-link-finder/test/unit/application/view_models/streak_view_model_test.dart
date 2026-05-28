import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/streak_view_model.dart';
import 'package:adhd_supplement_app/infrastructure/services/streak_service.dart';
import 'package:adhd_supplement_app/domain/repositories/streak_repository.dart';
import 'package:adhd_supplement_app/domain/entities/streak.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';

@GenerateMocks([StreakService, StreakRepository])
import 'streak_view_model_test.mocks.dart';

void main() {
  late StreakViewModel viewModel;
  late MockStreakService mockService;
  late MockStreakRepository mockRepository;
  const testUserId = 'user_99';

  setUp(() {
    mockService = MockStreakService();
    mockRepository = MockStreakRepository();
    viewModel = StreakViewModel(mockService, mockRepository);
  });

  group('StreakViewModel', () {
    test('initializeStreak creates a new initial streak', () {
      viewModel.initializeStreak(testUserId);

      expect(viewModel.currentStreak, isNotNull);
      expect(viewModel.currentStreak!.userId, testUserId);
      expect(viewModel.currentStreak!.currentStreak, 0);
    });

    test('updateStreak calls service and saves result', () async {
      viewModel.initializeStreak(testUserId);
      final logs = <DailyLog>[];
      final updatedStreak = viewModel.currentStreak!.copyWith(currentStreak: 5);

      when(mockService.calculateStreak(
        currentStreak: anyNamed('currentStreak'),
        recentLogs: anyNamed('recentLogs'),
      )).thenReturn(updatedStreak);

      when(mockRepository.saveStreak(any)).thenAnswer((_) async => true);

      await viewModel.updateStreak(recentLogs: logs);

      expect(viewModel.currentStreak!.currentStreak, 5);
      expect(viewModel.isLoading, isFalse);
      verify(mockRepository.saveStreak(updatedStreak)).called(1);
    });

    test('applyGraceDay fails if no streak initialized', () {
      viewModel.applyGraceDay();
      expect(viewModel.error, contains('not initialized'));
    });

    test('applyGraceDay decrements grace days correctly', () async {
      final initialStreak = Streak(
        userId: testUserId,
        currentStreak: 10,
        longestStreak: 10,
        graceDaysRemaining: 2,
        graceDaysUsed: 0,
        updatedAt: DateTime.now(),
      );

      when(mockRepository.getStreak(testUserId))
          .thenAnswer((_) async => initialStreak);
      await viewModel.loadStreak(testUserId);

      viewModel.applyGraceDay();

      expect(viewModel.currentStreak!.graceDaysRemaining, 1);
      expect(viewModel.currentStreak!.graceDaysUsed, 1);
    });

    test('applyGraceDay sets error if none left', () async {
      final noGraceStreak = Streak(
        userId: testUserId,
        currentStreak: 10,
        longestStreak: 10,
        graceDaysRemaining: 0,
        graceDaysUsed: 2,
        updatedAt: DateTime.now(),
      );

      when(mockRepository.getStreak(testUserId))
          .thenAnswer((_) async => noGraceStreak);
      await viewModel.loadStreak(testUserId);

      viewModel.applyGraceDay();

      expect(viewModel.error, contains('No grace days remaining'));
    });

    test('resetGraceDays calls service', () async {
      final initialStreak = Streak.initial(testUserId);
      when(mockRepository.getStreak(testUserId))
          .thenAnswer((_) async => initialStreak);
      await viewModel.loadStreak(testUserId);

      final resetStreak = initialStreak.copyWith(graceDaysRemaining: 3);
      when(mockService.resetGraceDays(any, graceDaysPerMonth: 3))
          .thenReturn(resetStreak);

      viewModel.resetGraceDays(graceDaysPerMonth: 3);

      expect(viewModel.currentStreak!.graceDaysRemaining, 3);
    });

    test('loadStreak handles null (initializes and saves)', () async {
      when(mockRepository.getStreak(testUserId)).thenAnswer((_) async => null);
      when(mockRepository.saveStreak(any)).thenAnswer((_) async => true);

      await viewModel.loadStreak(testUserId);

      expect(viewModel.currentStreak, isNotNull);
      expect(viewModel.currentStreak!.userId, testUserId);
      verify(mockRepository.saveStreak(any)).called(1);
    });

    test('saveStreak handles repository error', () async {
      viewModel.initializeStreak(testUserId);
      when(mockRepository.saveStreak(any)).thenThrow(Exception('Save Fail'));

      await viewModel.saveStreak();

      expect(viewModel.error, contains('Save Fail'));
    });
  });
}

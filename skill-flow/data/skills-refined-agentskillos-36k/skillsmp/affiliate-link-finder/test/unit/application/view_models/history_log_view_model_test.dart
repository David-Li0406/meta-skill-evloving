import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/history_log_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/log_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/stack_repository.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_stack.dart';

@GenerateMocks([LogRepository, StackRepository])
import 'history_log_view_model_test.mocks.dart';

void main() {
  late HistoryLogViewModel viewModel;
  late MockLogRepository mockLogRepository;
  late MockStackRepository mockStackRepository;
  const testUserId = 'user_history';

  final today = DateTime.now();
  final yesterday = today.subtract(const Duration(days: 1));

  final testLogs = [
    DailyLog(
      id: 'log1',
      userId: testUserId,
      date: today,
      entries: [
        LogEntry(supplementId: 's1', takenAt: today, status: LogStatus.taken),
      ],
      createdAt: today,
    ),
    DailyLog(
      id: 'log2',
      userId: testUserId,
      date: yesterday,
      entries: [
        LogEntry(
            supplementId: 's1', takenAt: yesterday, status: LogStatus.skipped),
      ],
      createdAt: yesterday,
    ),
  ];

  setUp(() {
    mockLogRepository = MockLogRepository();
    mockStackRepository = MockStackRepository();
    viewModel = HistoryLogViewModel(
      logRepository: mockLogRepository,
      stackRepository: mockStackRepository,
      userId: testUserId,
    );
  });

  group('HistoryLogViewModel', () {
    test('fetchHistory loads recent logs and sorts them', () async {
      when(mockLogRepository.getRecentLogs(testUserId, 30))
          .thenAnswer((_) async => testLogs);

      await viewModel.fetchHistory();

      expect(viewModel.recentLogs.length, 2);
      expect(viewModel.recentLogs.first.id, 'log1'); // Sort descending
      expect(viewModel.isLoading, isFalse);
    });

    test('groupedLogs categorizes logs correctly', () async {
      when(mockLogRepository.getRecentLogs(testUserId, 30))
          .thenAnswer((_) async => testLogs);

      await viewModel.fetchHistory();
      final groups = viewModel.groupedLogs;

      expect(groups.containsKey('Earlier Today'), isTrue);
      expect(groups.containsKey('Yesterday'), isTrue);
    });

    test('stats calculates correct values', () async {
      when(mockLogRepository.getRecentLogs(testUserId, 30))
          .thenAnswer((_) async => testLogs);

      await viewModel.fetchHistory();
      final stats = viewModel.stats;

      expect(stats['total'], 2);
      expect(stats['taken'], 1);
      expect(stats['missed'], 1);
      expect(stats['completionRate'], 50);
    });

    test('setFilter and getFilteredEntries work together', () async {
      when(mockLogRepository.getRecentLogs(testUserId, 30))
          .thenAnswer((_) async => testLogs);
      await viewModel.fetchHistory();

      viewModel.setFilter('Taken');
      final log = viewModel.recentLogs.first; // Today's log with 1 taken entry
      final filtered = viewModel.getFilteredEntries(log);

      expect(filtered.length, 1);
      expect(filtered.first.status, LogStatus.taken);
    });

    test('resolveAllMissed identifies and saves missing items', () async {
      final now = DateTime.now();

      when(mockLogRepository.getLogForDate(testUserId, any))
          .thenAnswer((_) async => null);
      when(mockStackRepository.getUserStacks(testUserId))
          .thenAnswer((_) async => [
                SupplementStack(
                  id: 'stack1',
                  userId: testUserId,
                  name: 'Morning Stack',
                  items: [
                    const StackItem(
                        supplementId: 's2', scheduledTime: '06:00', order: 0),
                  ],
                  createdAt: now,
                  updatedAt: now,
                ),
              ]);
      when(mockLogRepository.saveLog(any)).thenAnswer((_) async => true);
      when(mockLogRepository.getRecentLogs(testUserId, any))
          .thenAnswer((_) async => []);

      await viewModel.resolveAllMissed();

      // If it's currently past 06:00, it should have added an entry
      if (now.hour > 6) {
        verify(mockLogRepository.saveLog(any)).called(1);
      }
    });

    test('fetchHistory error sets error message', () async {
      when(mockLogRepository.getRecentLogs(testUserId, 30))
          .thenThrow(Exception('Log error'));

      await viewModel.fetchHistory();

      expect(viewModel.error, contains('Failed to load history'));
    });
  });
}

import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/nightly_reflection_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/log_repository.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';

@GenerateMocks([LogRepository])
import 'nightly_reflection_view_model_test.mocks.dart';

void main() {
  late NightlyReflectionViewModel viewModel;
  late MockLogRepository mockRepository;
  const testUserId = 'user_abc';

  setUp(() {
    mockRepository = MockLogRepository();
    viewModel = NightlyReflectionViewModel(
      logRepository: mockRepository,
      userId: testUserId,
    );
  });

  group('NightlyReflectionViewModel', () {
    test('initial state is correct', () {
      expect(viewModel.focusValue, 0.5);
      expect(viewModel.isSleepReady, isTrue);
      expect(viewModel.journalController.text, isEmpty);
      expect(viewModel.isLoading, isFalse);
    });

    test('updateFocusValue updates state', () {
      viewModel.updateFocusValue(0.8);
      expect(viewModel.focusValue, 0.8);
    });

    test('toggleSleepReady updates state', () {
      viewModel.toggleSleepReady(false);
      expect(viewModel.isSleepReady, isFalse);
    });

    test('loadTodayReflection maps focusScore correctly', () async {
      final today = DateTime.now();
      final existingLog = DailyLog(
        id: 'log1',
        userId: testUserId,
        date: today,
        entries: [],
        focusScore: 7,
        notes: 'Great day',
        createdAt: today,
      );

      when(mockRepository.getLogForDate(testUserId, any))
          .thenAnswer((_) async => existingLog);

      await viewModel.loadTodayReflection();

      expect(viewModel.focusValue, 0.7);
      expect(viewModel.journalController.text, 'Great day');
      expect(viewModel.isLoading, isFalse);
    });

    test('saveReflection updates existing log', () async {
      final now = DateTime.now();
      final today = DateTime(now.year, now.month, now.day);
      final existingLog = DailyLog(
        id: 'log1',
        userId: testUserId,
        date: today,
        entries: [],
        createdAt: now,
      );

      when(mockRepository.getLogForDate(testUserId, any))
          .thenAnswer((_) async => existingLog);
      when(mockRepository.saveLog(any)).thenAnswer((_) async => true);

      viewModel.updateFocusValue(0.9);
      viewModel.journalController.text = 'Updated note';

      final result = await viewModel.saveReflection();

      expect(result, isTrue);
      expect(viewModel.isSaving, isFalse);

      final captured = verify(mockRepository.saveLog(captureAny))
          .captured
          .single as DailyLog;
      expect(captured.focusScore, 9);
      expect(captured.notes, 'Updated note');
    });

    test('saveReflection handles auto-save flag', () async {
      when(mockRepository.getLogForDate(testUserId, any))
          .thenAnswer((_) async => null);
      when(mockRepository.saveLog(any)).thenAnswer((_) async => true);

      final future = viewModel.saveReflection(isAutoSave: true);
      expect(viewModel.isAutoSaving, isTrue);
      expect(viewModel.isSaving, isFalse);

      await future;
      expect(viewModel.isAutoSaving, isFalse);
    });

    test('saveReflection failure returns false', () async {
      when(mockRepository.getLogForDate(testUserId, any))
          .thenThrow(Exception('Save error'));

      final result = await viewModel.saveReflection();

      expect(result, isFalse);
      expect(viewModel.isSaving, isFalse);
    });
  });
}

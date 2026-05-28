import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/symptom_checkin_viewmodel.dart';
import 'package:adhd_supplement_app/domain/repositories/symptom_repository.dart';

@GenerateMocks([SymptomRepository])
import 'symptom_checkin_viewmodel_test.mocks.dart';

void main() {
  late SymptomCheckInViewModel viewModel;
  late MockSymptomRepository mockRepository;
  const testUserId = 'user_123';

  setUp(() {
    mockRepository = MockSymptomRepository();
    viewModel = SymptomCheckInViewModel(
      repository: mockRepository,
      userId: testUserId,
    );
  });

  group('SymptomCheckInViewModel', () {
    test('initial state has default values', () {
      expect(viewModel.focusLevel, 50.0);
      expect(viewModel.energyLevel, 50.0);
      expect(viewModel.moodLevel, 50.0);
      expect(viewModel.notes, isNull);
      expect(viewModel.isLoading, isFalse);
    });

    test('setting values updates state', () {
      viewModel.setFocusLevel(75.0);
      viewModel.setEnergyLevel(60.0);
      viewModel.setMoodLevel(80.0);
      viewModel.setNotes('Feeling good');

      expect(viewModel.focusLevel, 75.0);
      expect(viewModel.energyLevel, 60.0);
      expect(viewModel.moodLevel, 80.0);
      expect(viewModel.notes, 'Feeling good');
    });

    test('checkTodayStatus updates hasCheckedInToday', () async {
      when(mockRepository.hasCheckedInToday(testUserId))
          .thenAnswer((_) async => true);

      await viewModel.checkTodayStatus();

      expect(viewModel.hasCheckedInToday, isTrue);
      expect(viewModel.isLoading, isFalse);
      verify(mockRepository.hasCheckedInToday(testUserId)).called(1);
    });

    test('submitCheckIn success resets form and sets hasCheckedInToday',
        () async {
      viewModel.setFocusLevel(80.0);
      viewModel.setNotes('Test note');

      when(mockRepository.logCheckIn(any)).thenAnswer((_) async => true);

      final result = await viewModel.submitCheckIn();

      expect(result, isTrue);
      expect(viewModel.hasCheckedInToday, isTrue);
      expect(viewModel.focusLevel, 50.0); // Reset
      expect(viewModel.notes, isNull); // Reset
      verify(mockRepository.logCheckIn(any)).called(1);
    });

    test('submitCheckIn with isAutoSave does not reset form', () async {
      viewModel.setFocusLevel(80.0);

      when(mockRepository.logCheckIn(any)).thenAnswer((_) async => true);

      final result = await viewModel.submitCheckIn(isAutoSave: true);

      expect(result, isTrue);
      expect(viewModel.focusLevel, 80.0); // Not reset
      verify(mockRepository.logCheckIn(any)).called(1);
    });

    test('submitCheckIn failure sets error', () async {
      when(mockRepository.logCheckIn(any)).thenThrow(Exception('DB Error'));

      final result = await viewModel.submitCheckIn();

      expect(result, isFalse);
      expect(viewModel.error, contains('Failed to submit'));
      expect(viewModel.isLoading, isFalse);
    });

    test('reset clears form and error', () async {
      viewModel.setFocusLevel(90.0);
      viewModel.setNotes('Error here');

      when(mockRepository.logCheckIn(any)).thenThrow(Exception('Fail'));
      await viewModel.submitCheckIn();

      expect(viewModel.error, isNotNull);

      viewModel.reset();

      expect(viewModel.focusLevel, 50.0);
      expect(viewModel.notes, isNull);
      expect(viewModel.error, isNull);
    });
  });
}

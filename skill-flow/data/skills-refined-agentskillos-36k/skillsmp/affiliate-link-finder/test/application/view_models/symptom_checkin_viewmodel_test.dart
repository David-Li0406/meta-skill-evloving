import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/application/view_models/symptom_checkin_viewmodel.dart';
import 'package:adhd_supplement_app/domain/entities/symptom_checkin.dart';
import 'package:adhd_supplement_app/domain/repositories/symptom_repository.dart';

class MockSymptomRepository implements SymptomRepository {
  final List<SymptomCheckIn> _checkIns = [];
  bool _hasCheckedInToday = false;
  bool _shouldThrow = false;

  void setHasCheckedInToday(bool value) => _hasCheckedInToday = value;
  void setShouldThrow(bool value) => _shouldThrow = value;
  void setCheckIns(List<SymptomCheckIn> checkIns) => _checkIns.addAll(checkIns);

  @override
  Future<void> logCheckIn(SymptomCheckIn checkIn) async {
    if (_shouldThrow) {
      throw Exception('Repository error');
    }
    await Future<void>.delayed(const Duration(milliseconds: 100));
    _checkIns.add(checkIn);
    _hasCheckedInToday = true;
  }

  @override
  Future<List<SymptomCheckIn>> getCheckIns(String userId) async {
    return _checkIns.where((c) => c.userId == userId).toList();
  }

  @override
  Future<List<SymptomCheckIn>> getCheckInsByDateRange(
    String userId,
    DateTime startDate,
    DateTime endDate,
  ) async {
    if (_shouldThrow) {
      throw Exception('Repository error');
    }
    return _checkIns
        .where((c) =>
            c.userId == userId &&
            c.timestamp.isAfter(startDate.subtract(const Duration(days: 1))) &&
            c.timestamp.isBefore(endDate.add(const Duration(days: 1))))
        .toList();
  }

  @override
  Future<SymptomCheckIn?> getLatestCheckIn(String userId) async {
    try {
      return _checkIns.where((c) => c.userId == userId).last;
    } catch (e) {
      return null;
    }
  }

  @override
  Future<bool> hasCheckedInToday(String userId) async {
    if (_shouldThrow) {
      throw Exception('Repository error');
    }
    await Future<void>.delayed(const Duration(milliseconds: 50));
    return _hasCheckedInToday;
  }

  @override
  Future<void> deleteCheckIn(String id) async {
    _checkIns.removeWhere((c) => c.id == id);
  }
}

void main() {
  late MockSymptomRepository mockRepository;
  late SymptomCheckInViewModel viewModel;
  const userId = 'user1';

  setUp(() {
    mockRepository = MockSymptomRepository();
    viewModel = SymptomCheckInViewModel(
      repository: mockRepository,
      userId: userId,
    );
  });

  group('SymptomCheckInViewModel', () {
    test('should initialize with correct default values', () {
      expect(viewModel.focusLevel, 50.0);
      expect(viewModel.energyLevel, 50.0);
      expect(viewModel.moodLevel, 50.0);
      expect(viewModel.notes, null);
      expect(viewModel.isLoading, false);
      expect(viewModel.hasCheckedInToday, false);
      expect(viewModel.error, null);
    });

    test('setFocusLevel should update focus level', () {
      viewModel.setFocusLevel(75.0);

      expect(viewModel.focusLevel, 75.0);
    });

    test('setEnergyLevel should update energy level', () {
      viewModel.setEnergyLevel(80.0);

      expect(viewModel.energyLevel, 80.0);
    });

    test('setMoodLevel should update mood level', () {
      viewModel.setMoodLevel(65.0);

      expect(viewModel.moodLevel, 65.0);
    });

    test('setNotes should update notes', () {
      viewModel.setNotes('Feeling great today');

      expect(viewModel.notes, 'Feeling great today');
    });

    test('setNotes should handle null', () {
      viewModel.setNotes('Some notes');
      viewModel.setNotes(null);

      expect(viewModel.notes, null);
    });

    test('checkTodayStatus should set loading state', () async {
      final statusFuture = viewModel.checkTodayStatus();

      expect(viewModel.isLoading, true);

      await statusFuture;

      expect(viewModel.isLoading, false);
    });

    test('checkTodayStatus should update hasCheckedInToday', () async {
      mockRepository.setHasCheckedInToday(true);

      await viewModel.checkTodayStatus();

      expect(viewModel.hasCheckedInToday, true);
      expect(viewModel.error, null);
    });

    test('checkTodayStatus should handle errors', () async {
      mockRepository.setShouldThrow(true);

      await viewModel.checkTodayStatus();

      expect(viewModel.error, contains('Failed to check status'));
      expect(viewModel.isLoading, false);
    });

    test('submitCheckIn should set loading state', () async {
      final submitFuture = viewModel.submitCheckIn();

      expect(viewModel.isLoading, true);

      await submitFuture;

      expect(viewModel.isLoading, false);
    });

    test('submitCheckIn should create check-in and reset form', () async {
      viewModel.setFocusLevel(80.0);
      viewModel.setEnergyLevel(70.0);
      viewModel.setMoodLevel(75.0);
      viewModel.setNotes('Great day');

      final success = await viewModel.submitCheckIn();

      expect(success, true);
      expect(viewModel.hasCheckedInToday, true);
      expect(viewModel.focusLevel, 50.0);
      expect(viewModel.energyLevel, 50.0);
      expect(viewModel.moodLevel, 50.0);
      expect(viewModel.notes, null);
      expect(viewModel.error, null);
    });

    test('submitCheckIn should round values', () async {
      viewModel.setFocusLevel(75.7);
      viewModel.setEnergyLevel(82.3);
      viewModel.setMoodLevel(68.9);

      await viewModel.submitCheckIn();

      // Values should be rounded in the check-in
      expect(viewModel.hasCheckedInToday, true);
    });

    test('submitCheckIn should handle errors', () async {
      mockRepository.setShouldThrow(true);
      viewModel.setFocusLevel(80.0);

      final success = await viewModel.submitCheckIn();

      expect(success, false);
      expect(viewModel.error, contains('Failed to submit check-in'));
      expect(viewModel.isLoading, false);
      // Form should not be reset on error
      expect(viewModel.focusLevel, 80.0);
    });

    test('getRecentCheckIns should return check-ins', () async {
      final now = DateTime.now();
      final checkIns = [
        SymptomCheckIn(
          id: '1',
          userId: userId,
          timestamp: now.subtract(const Duration(days: 1)),
          focusLevel: 70,
          energyLevel: 60,
          moodLevel: 50,
        ),
        SymptomCheckIn(
          id: '2',
          userId: userId,
          timestamp: now.subtract(const Duration(days: 3)),
          focusLevel: 80,
          energyLevel: 70,
          moodLevel: 60,
        ),
      ];
      mockRepository.setCheckIns(checkIns);

      final recent = await viewModel.getRecentCheckIns(days: 7);

      expect(recent.length, 2);
      expect(viewModel.error, null);
    });

    test('getRecentCheckIns should handle errors', () async {
      mockRepository.setShouldThrow(true);

      final recent = await viewModel.getRecentCheckIns();

      expect(recent, isEmpty);
      expect(viewModel.error, contains('Failed to load check-ins'));
    });

    test('reset should reset form to defaults', () {
      viewModel.setFocusLevel(80.0);
      viewModel.setEnergyLevel(70.0);
      viewModel.setMoodLevel(75.0);
      viewModel.setNotes('Some notes');

      viewModel.reset();

      expect(viewModel.focusLevel, 50.0);
      expect(viewModel.energyLevel, 50.0);
      expect(viewModel.moodLevel, 50.0);
      expect(viewModel.notes, null);
      expect(viewModel.error, null);
    });

    test('should notify listeners on state changes', () {
      var notified = false;
      viewModel.addListener(() {
        notified = true;
      });

      viewModel.setFocusLevel(75.0);

      expect(notified, true);
    });
  });
}

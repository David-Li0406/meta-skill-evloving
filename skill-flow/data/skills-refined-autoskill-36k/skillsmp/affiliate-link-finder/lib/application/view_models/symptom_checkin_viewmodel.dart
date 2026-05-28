import 'package:flutter/foundation.dart';
import '../../domain/entities/symptom_checkin.dart';
import '../../domain/repositories/symptom_repository.dart';
import 'package:uuid/uuid.dart';

class SymptomCheckInViewModel extends ChangeNotifier {
  final SymptomRepository _repository;
  final String _userId;

  SymptomCheckInViewModel({
    required SymptomRepository repository,
    required String userId,
  })  : _repository = repository,
        _userId = userId;

  // Current check-in state
  double _focusLevel = 50.0;
  double _energyLevel = 50.0;
  double _moodLevel = 50.0;
  String? _notes;
  bool _isLoading = false;
  bool _hasCheckedInToday = false;
  String? _error;
  String? _currentSessionId;
  bool _isDisposed = false;

  // Getters
  double get focusLevel => _focusLevel;
  double get energyLevel => _energyLevel;
  double get moodLevel => _moodLevel;
  String? get notes => _notes;
  bool get isLoading => _isLoading;
  bool get hasCheckedInToday => _hasCheckedInToday;
  String? get error => _error;

  // Setters
  void setFocusLevel(double value) {
    _focusLevel = value;
    notifyListeners();
  }

  void setEnergyLevel(double value) {
    _energyLevel = value;
    notifyListeners();
  }

  void setMoodLevel(double value) {
    _moodLevel = value;
    notifyListeners();
  }

  void setNotes(String? value) {
    _notes = value;
    notifyListeners();
  }

  /// Check if user has already checked in today
  Future<void> checkTodayStatus() async {
    try {
      _isLoading = true;
      notifyListeners();

      _hasCheckedInToday = await _repository.hasCheckedInToday(_userId);
      _error = null;
    } catch (e) {
      _error = 'Failed to check status: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  /// Submit the check-in
  Future<bool> submitCheckIn({bool isAutoSave = false}) async {
    try {
      if (!isAutoSave) _isLoading = true;
      _error = null;
      notifyListeners();

      // Use existing session ID or create new
      _currentSessionId ??= const Uuid().v4();

      final checkIn = SymptomCheckIn(
        id: _currentSessionId!,
        userId: _userId,
        timestamp: DateTime.now(),
        focusLevel: _focusLevel.round(),
        energyLevel: _energyLevel.round(),
        moodLevel: _moodLevel.round(),
        notes: _notes,
      );

      await _repository.logCheckIn(checkIn);
      _hasCheckedInToday = true;

      if (!isAutoSave) {
        // Reset form only on final submit
        _focusLevel = 50.0;
        _energyLevel = 50.0;
        _moodLevel = 50.0;
        _notes = null;
        _currentSessionId = null;
      }

      return true;
    } catch (e) {
      _error = 'Failed to submit check-in: $e';
      return false;
    } finally {
      if (!isAutoSave) _isLoading = false;
      notifyListeners();
    }
  }

  /// Get recent check-ins for insights
  Future<List<SymptomCheckIn>> getRecentCheckIns({int days = 7}) async {
    try {
      final endDate = DateTime.now();
      final startDate = endDate.subtract(Duration(days: days));
      return await _repository.getCheckInsByDateRange(
          _userId, startDate, endDate);
    } catch (e) {
      _error = 'Failed to load check-ins: $e';
      return [];
    }
  }

  /// Reset the form
  void reset() {
    _focusLevel = 50.0;
    _energyLevel = 50.0;
    _moodLevel = 50.0;
    _notes = null;
    _currentSessionId = null;
    _error = null;
    notifyListeners();
  }

  @override
  void dispose() {
    _isDisposed = true;
    super.dispose();
  }

  @override
  void notifyListeners() {
    if (!_isDisposed) {
      super.notifyListeners();
    }
  }
}

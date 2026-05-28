import 'package:flutter/material.dart';
import '../../domain/entities/daily_log.dart';
import '../../domain/repositories/log_repository.dart';
import '../../utils/logger.dart';
// import 'package:uuid/uuid.dart';

class NightlyReflectionViewModel extends ChangeNotifier {
  final LogRepository _logRepository;
  final String _userId;

  bool _isLoading = false;
  bool _isSaving = false;
  bool _isAutoSaving = false;
  double _focusValue = 0.5;
  bool _isSleepReady = true;
  final TextEditingController _journalController = TextEditingController();

  NightlyReflectionViewModel({
    required LogRepository logRepository,
    required String userId,
  })  : _logRepository = logRepository,
        _userId = userId;

  bool get isLoading => _isLoading;
  bool get isSaving => _isSaving;
  bool get isAutoSaving => _isAutoSaving;
  double get focusValue => _focusValue;
  bool get isSleepReady => _isSleepReady;
  TextEditingController get journalController => _journalController;

  @override
  void dispose() {
    _journalController.dispose();
    super.dispose();
  }

  void updateFocusValue(double value) {
    _focusValue = value;
    notifyListeners();
  }

  void toggleSleepReady(bool value) {
    _isSleepReady = value;
    notifyListeners();
  }

  Future<void> loadTodayReflection() async {
    _isLoading = true;
    notifyListeners();

    try {
      final now = DateTime.now();
      final log = await _logRepository.getLogForDate(_userId, now);

      if (log != null) {
        // Map focusScore (1-10) to focusValue (0.0-1.0)
        if (log.focusScore != null) {
          _focusValue = (log.focusScore! / 10).clamp(0.0, 1.0);
        }
        _journalController.text = log.notes ?? '';
        // Note: isSleepReady is not persisted in generic Log currently,
        // could map to custom logic or ignore for MVP reload
      }
    } catch (e) {
      AppLogger.e('Error loading reflection', e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<bool> saveReflection({bool isAutoSave = false}) async {
    if (isAutoSave) {
      _isAutoSaving = true;
    } else {
      _isSaving = true;
    }
    notifyListeners();

    try {
      // Scale focus value (0.0 - 1.0) to score (1 - 10)
      final focusScore = (_focusValue * 10).round().clamp(1, 10);
      final notes = _journalController.text;

      // We need to fetch/create today's log first to preserve other fields
      final now = DateTime.now();
      DailyLog? log = await _logRepository.getLogForDate(_userId, now);

      final today = DateTime(now.year, now.month, now.day);

      log ??= DailyLog(
        id: '${_userId}_${today.toIso8601String()}',
        userId: _userId,
        date: today,
        entries: [],
        createdAt: now,
      );

      final updatedLog = log.copyWith(
        focusScore: focusScore,
        notes: notes.isEmpty ? null : notes,
      );

      await _logRepository.saveLog(updatedLog);
      return true;
    } catch (e) {
      AppLogger.e('Error saving reflection', e);
      return false;
    } finally {
      if (isAutoSave) {
        _isAutoSaving = false;
      } else {
        _isSaving = false;
      }
      notifyListeners();
    }
  }
}

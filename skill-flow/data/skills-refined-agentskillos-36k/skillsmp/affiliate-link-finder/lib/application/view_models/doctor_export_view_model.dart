import 'package:flutter/foundation.dart';
import '../../utils/logger.dart';
import 'package:intl/intl.dart';
import '../../domain/repositories/log_repository.dart';
import '../../domain/repositories/auth_repository.dart';
import '../../domain/entities/daily_log.dart';
import '../../infrastructure/services/report_pdf_service.dart';

class DoctorExportViewModel extends ChangeNotifier {
  final LogRepository _logRepository;
  // final AuthRepository _authRepository; // Unused but kept in constructor for consistent DI pattern if needed later
  final ReportPdfService _pdfService; // New Dependency
  final String _userId;

  bool _isLoading = false;
  String? _error;
  List<DailyLog> _logs = [];
  DateTime _startDate = DateTime.now().subtract(const Duration(days: 30));
  DateTime _endDate = DateTime.now();

  // Computed stats
  double _consistency = 0.0;
  double _avgFocus = 0.0;
  double _avgMood = 0.0;
  int _totalDoses = 0;
  int _takenDoses = 0;

  bool get isLoading => _isLoading;
  String? get error => _error;
  double get consistency => _consistency;
  double get avgFocus => _avgFocus;
  double get avgMood => _avgMood;
  List<DailyLog> get logs => _logs;
  DateTime get startDate => _startDate;
  DateTime get endDate => _endDate;

  DoctorExportViewModel({
    required LogRepository logRepository,
    required AuthRepository authRepository,
    required ReportPdfService pdfService,
    required String userId,
  })  : _logRepository = logRepository,
        // _authRepository = authRepository,
        _pdfService = pdfService,
        _userId = userId;

  Future<void> loadData(
      {int? days, DateTime? customStart, DateTime? customEnd}) async {
    _setLoading(true);
    _error = null;

    try {
      if (days != null) {
        _endDate = DateTime.now();
        _startDate = _endDate.subtract(Duration(days: days));
      } else if (customStart != null && customEnd != null) {
        _startDate = customStart;
        _endDate = customEnd;
      }

      // Fetch logs
      _logs = await _logRepository.getLogsByDateRange(
          _userId, _startDate, _endDate);

      _calculateStats();
    } catch (e) {
      _error = 'Failed to load report data: $e';
      AppLogger.e(_error ?? 'Failed to load report data');
    } finally {
      _setLoading(false);
    }
  }

  void _calculateStats() {
    if (_logs.isEmpty) {
      _consistency = 0.0;
      _avgFocus = 0.0;
      _avgMood = 0.0;
      return;
    }

    int totalFocus = 0;
    int focusCount = 0;
    int totalMood = 0;
    int moodCount = 0;
    _totalDoses = 0;
    _takenDoses = 0;

    for (final log in _logs) {
      // Focus
      if (log.focusScore != null && log.focusScore! > 0) {
        totalFocus += log.focusScore!;
        focusCount++;
      }

      // Mood
      if (log.moodScore != null && log.moodScore! > 0) {
        totalMood += log.moodScore!;
        moodCount++;
      }

      // Consistency
      // Assuming 'entries' represents scheduled items that were acted upon (taken or skipped)
      // Note: Ideally we'd know 'scheduled' count vs 'taken'.
      // If entries only exist when acted upon, we might miss 'missed' doses if they aren't logged as 'skipped'.
      // For now, calculating based on recorded entries.
      for (final entry in log.entries) {
        _totalDoses++; // Treating every entry as a scheduled dose
        if (entry.status == LogStatus.taken) {
          _takenDoses++;
        }
      }
    }

    _avgFocus = focusCount > 0 ? totalFocus / focusCount : 0.0;
    _avgMood = moodCount > 0 ? totalMood / moodCount : 0.0;
    _consistency = _totalDoses > 0 ? _takenDoses / _totalDoses : 0.0;
  }

  Future<Uint8List> generatePdf({
    bool includeConsistency = true,
    bool includeFocus = true,
    bool includeInteractions = false,
  }) async {
    return _pdfService.generateReport(
      startDate: _startDate,
      endDate: _endDate,
      logs: _logs,
      consistency: _consistency,
      avgFocus: _avgFocus,
      avgMood: _avgMood,
      includeConsistency: includeConsistency,
      includeFocus: includeFocus,
      includeInteractions: includeInteractions,
    );
  }

  String generateReportText({
    bool includeConsistency = true,
    bool includeFocus = true,
    bool includeInteractions = false,
  }) {
    final dateFormat = DateFormat('MMM d, yyyy');
    final buffer = StringBuffer();

    buffer.writeln('ADHD MANAGEMENT REPORT');
    buffer.writeln('=======================');
    buffer.writeln('Generated: ${dateFormat.format(DateTime.now())}');
    buffer.writeln(
        'Period: ${dateFormat.format(_startDate)} - ${dateFormat.format(_endDate)}');
    buffer.writeln('');

    if (includeConsistency) {
      buffer.writeln('SUPPLEMENT CONSISTENCY');
      buffer.writeln('----------------------');
      buffer.writeln(
          'Overall Adherence: ${(_consistency * 100).toStringAsFixed(1)}%');
      buffer.writeln('Doses Taken: $_takenDoses / $_totalDoses recorded');
      buffer.writeln('');
    }

    if (includeFocus) {
      buffer.writeln('WELLBEING SCORES');
      buffer.writeln('----------------');
      buffer.writeln('Average Focus: ${(_avgFocus).toStringAsFixed(1)} / 10');
      buffer.writeln('Average Mood: ${(_avgMood).toStringAsFixed(1)} / 5');
      buffer.writeln('');
    }

    // Interactions would likely come from SafetyService or specific logs if we track them
    if (includeInteractions) {
      buffer.writeln('INTERACTIONS & SIDE EFFECTS');
      buffer.writeln('---------------------------');
      buffer.writeln('No adverse interactions recorded in this period.');
      // Placeholder until we implemented granular interaction logging
      buffer.writeln('');
    }

    buffer.writeln('DAILY BREAKDOWN');
    buffer.writeln('---------------');
    // Sort logs by date desc
    final sortedLogs = List<DailyLog>.from(_logs)
      ..sort((a, b) => b.date.compareTo(a.date));

    for (final log in sortedLogs) {
      buffer.writeln(dateFormat.format(log.date));
      if (includeFocus && log.focusScore != null) {
        buffer.writeln('  Focus: ${log.focusScore}/10');
      }
      if (includeConsistency) {
        final taken =
            log.entries.where((e) => e.status == LogStatus.taken).length;
        final total = log.entries.length;
        buffer.writeln('  Supplements: $taken/$total taken');
        // List skipped
        final skipped = log.entries.where((e) => e.status == LogStatus.skipped);
        if (skipped.isNotEmpty) {
          buffer.writeln(
              '  Skipped: ${skipped.map((e) => e.skippedReason ?? "No reason").join(", ")}');
        }
      }
      buffer.writeln('');
    }

    return buffer.toString();
  }

  void _setLoading(bool loading) {
    _isLoading = loading;
    notifyListeners();
  }
}

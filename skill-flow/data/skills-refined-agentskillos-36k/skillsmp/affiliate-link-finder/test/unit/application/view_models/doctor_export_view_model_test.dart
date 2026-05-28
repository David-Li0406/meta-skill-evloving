import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/doctor_export_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/log_repository.dart';
import 'package:adhd_supplement_app/domain/repositories/auth_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/report_pdf_service.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'dart:typed_data';

// Generate Mocks
@GenerateMocks([LogRepository, AuthRepository, ReportPdfService])
import 'doctor_export_view_model_test.mocks.dart';

void main() {
  late MockLogRepository mockLogRepository;
  late MockAuthRepository mockAuthRepository;
  late MockReportPdfService mockPdfService;
  late DoctorExportViewModel viewModel;
  const String userId = 'test_user';

  setUp(() {
    mockLogRepository = MockLogRepository();
    mockAuthRepository = MockAuthRepository();
    mockPdfService = MockReportPdfService();

    viewModel = DoctorExportViewModel(
      logRepository: mockLogRepository,
      authRepository: mockAuthRepository,
      pdfService: mockPdfService,
      userId: userId,
    );
  });

  group('DoctorExportViewModel Tests', () {
    test('Initial state is correct', () {
      expect(viewModel.isLoading, false);
      expect(viewModel.logs, isEmpty);
      expect(viewModel.consistency, 0.0);
    });

    test('loadData fetches logs and calculates stats correctly', () async {
      // Arrange
      final now = DateTime.now();
      final logs = [
        DailyLog(
          id: '1',
          userId: userId,
          date: now,
          entries: [
            LogEntry(supplementId: 's1', takenAt: now, status: LogStatus.taken),
            LogEntry(
                supplementId: 's2', takenAt: now, status: LogStatus.skipped),
          ],
          focusScore: 8,
          moodScore: 4,
          createdAt: now,
        ),
        DailyLog(
          id: '2',
          userId: userId,
          date: now.subtract(const Duration(days: 1)),
          entries: [
            LogEntry(supplementId: 's1', takenAt: now, status: LogStatus.taken),
          ],
          focusScore: 6,
          moodScore: 3,
          createdAt: now,
        ),
      ];

      when(mockLogRepository.getLogsByDateRange(userId, any, any))
          .thenAnswer((_) async => logs);

      // Act
      await viewModel.loadData();

      // Assert
      expect(viewModel.logs.length, 2);
      expect(viewModel.avgFocus, 7.0); // (8+6)/2
      expect(viewModel.avgMood, 3.5); // (4+3)/2

      // Consistency:
      // Log 1: 1 taken / 2 total
      // Log 2: 1 taken / 1 total
      // Total: 2 taken / 3 total = 0.666...
      expect(viewModel.consistency, closeTo(0.66, 0.01));
    });

    test('generatePdf calls service with correct data', () async {
      // Arrange
      final now = DateTime.now();
      final logs = [
        DailyLog(
            id: '1', userId: userId, date: now, entries: [], createdAt: now)
      ];
      when(mockLogRepository.getLogsByDateRange(userId, any, any))
          .thenAnswer((_) async => logs);
      when(mockPdfService.generateReport(
        startDate: anyNamed('startDate'),
        endDate: anyNamed('endDate'),
        logs: anyNamed('logs'),
        consistency: anyNamed('consistency'),
        avgFocus: anyNamed('avgFocus'),
        avgMood: anyNamed('avgMood'),
        includeConsistency: anyNamed('includeConsistency'),
        includeFocus: anyNamed('includeFocus'),
        includeInteractions: anyNamed('includeInteractions'),
      )).thenAnswer((_) async => Uint8List(0));

      await viewModel.loadData();

      // Act
      await viewModel.generatePdf();

      // Assert
      verify(mockPdfService.generateReport(
        startDate: anyNamed('startDate'),
        endDate: anyNamed('endDate'),
        logs: logs,
        consistency: anyNamed('consistency'),
        avgFocus: anyNamed('avgFocus'),
        avgMood: anyNamed('avgMood'),
        includeConsistency: true,
        includeFocus: true,
        includeInteractions: false,
      )).called(1);
    });
  });
}

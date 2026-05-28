import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/infrastructure/services/report_pdf_service.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';
import 'dart:typed_data';

void main() {
  late ReportPdfService pdfService;

  setUp(() {
    pdfService = ReportPdfService();
  });

  group('ReportPdfService Tests', () {
    test('generateReport returns non-empty byte list', () async {
      // Arrange
      final now = DateTime.now();
      final logs = [
        DailyLog(
          id: '1',
          userId: 'test_user',
          date: now,
          entries: [],
          createdAt: now,
        )
      ];

      // Act
      final Uint8List result = await pdfService.generateReport(
        startDate: now.subtract(const Duration(days: 7)),
        endDate: now,
        logs: logs,
        consistency: 0.8,
        avgFocus: 7.5,
        avgMood: 4.0,
      );

      // Assert
      expect(result.isNotEmpty, true);
      // Basic check: file signature for PDF is %PDF (Hex: 25 50 44 46)
      // Dart Uint8List: [37, 80, 68, 70]
      expect(result.length, greaterThan(4));
      expect(result[0], 0x25); // %
      expect(result[1], 0x50); // P
      expect(result[2], 0x44); // D
      expect(result[3], 0x46); // F
    });
  });
}

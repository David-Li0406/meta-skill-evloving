import 'dart:typed_data';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:intl/intl.dart';
// import 'package:printing/printing.dart';
import '../../domain/entities/daily_log.dart';

class ReportPdfService {
  Future<Uint8List> generateReport({
    required DateTime startDate,
    required DateTime endDate,
    required List<DailyLog> logs,
    required double consistency,
    required double avgFocus,
    required double avgMood,
    bool includeConsistency = true,
    bool includeFocus = true,
    bool includeInteractions = false,
  }) async {
    final pdf = pw.Document();
    final dateFormat = DateFormat('MMM d, yyyy');

    pdf.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        build: (pw.Context context) {
          return [
            _buildHeader(startDate, endDate, dateFormat),
            pw.SizedBox(height: 20),
            _buildSummary(
              consistency,
              avgFocus,
              avgMood,
              includeConsistency,
              includeFocus,
              includeInteractions,
            ),
            pw.SizedBox(height: 20),
            pw.Text(
              'Daily Logs',
              style: pw.TextStyle(
                fontSize: 18,
                fontWeight: pw.FontWeight.bold,
              ),
            ),
            pw.SizedBox(height: 10),
            _buildLogTable(logs, dateFormat, includeConsistency, includeFocus),
            pw.SizedBox(height: 20),
            _buildFooter(),
          ];
        },
      ),
    );

    return await pdf.save();
  }

  pw.Widget _buildHeader(DateTime start, DateTime end, DateFormat dateFormat) {
    return pw.Column(
      crossAxisAlignment: pw.CrossAxisAlignment.start,
      children: [
        pw.Text(
          'ADHD Management Report',
          style: pw.TextStyle(
            fontSize: 24,
            fontWeight: pw.FontWeight.bold,
          ),
        ),
        pw.SizedBox(height: 8),
        pw.Text(
          'Period: ${dateFormat.format(start)} - ${dateFormat.format(end)}',
          style: const pw.TextStyle(
            fontSize: 14,
            color: PdfColors.grey700,
          ),
        ),
        pw.SizedBox(height: 8),
        pw.Text(
          'Generated from FocusStack App',
          style: const pw.TextStyle(
            fontSize: 12,
            color: PdfColors.grey500,
          ),
        ),
        pw.Divider(),
      ],
    );
  }

  pw.Widget _buildSummary(
    double consistency,
    double avgFocus,
    double avgMood,
    bool includeConsistency,
    bool includeFocus,
    bool includeInteractions,
  ) {
    return pw.Container(
      padding: const pw.EdgeInsets.all(10),
      decoration: pw.BoxDecoration(
        border: pw.Border.all(color: PdfColors.grey300),
        borderRadius: pw.BorderRadius.circular(8),
        color: PdfColors.grey100,
      ),
      child: pw.Column(
        crossAxisAlignment: pw.CrossAxisAlignment.start,
        children: [
          pw.Text(
            'Summary Statistics',
            style: pw.TextStyle(fontSize: 16, fontWeight: pw.FontWeight.bold),
          ),
          pw.SizedBox(height: 10),
          pw.Row(
            mainAxisAlignment: pw.MainAxisAlignment.spaceAround,
            children: [
              if (includeConsistency)
                _buildStatItem('Consistency',
                    '${(consistency * 100).toStringAsFixed(0)}%'),
              if (includeFocus)
                _buildStatItem(
                    'Avg Focus', '${avgFocus.toStringAsFixed(1)}/10'),
              if (includeFocus)
                _buildStatItem('Avg Mood', '${avgMood.toStringAsFixed(1)}/5'),
            ],
          ),
          if (includeInteractions) ...[
            pw.SizedBox(height: 10),
            pw.Divider(),
            pw.SizedBox(height: 5),
            pw.Text(
              'Interaction Warnings: None Recorded', // Placeholder for now
              style: const pw.TextStyle(fontSize: 12, color: PdfColors.red900),
            ),
          ]
        ],
      ),
    );
  }

  pw.Widget _buildStatItem(String label, String value) {
    return pw.Column(
      children: [
        pw.Text(value,
            style: pw.TextStyle(
                fontSize: 20,
                fontWeight: pw.FontWeight.bold,
                color: PdfColors.blue800)),
        pw.Text(label,
            style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700)),
      ],
    );
  }

  pw.Widget _buildLogTable(List<DailyLog> logs, DateFormat dateFormat,
      bool includeConsistency, bool includeFocus) {
    if (logs.isEmpty) {
      return pw.Text('No data recorded for this period.');
    }

    final headers = ['Date'];
    if (includeConsistency) headers.add('Adherence');
    if (includeFocus) headers.addAll(['Focus', 'Mood']);

    final data = logs.map((log) {
      final row = [dateFormat.format(log.date)];

      if (includeConsistency) {
        final taken =
            log.entries.where((e) => e.status == LogStatus.taken).length;
        final total = log.entries.length;
        row.add(total > 0 ? '$taken/$total' : '-');
      }

      if (includeFocus) {
        row.add(log.focusScore?.toString() ?? '-');
        row.add(log.moodScore?.toString() ?? '-');
      }

      return row;
    }).toList();

    return pw.TableHelper.fromTextArray(
      headers: headers,
      data: data,
      headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold),
      headerDecoration: const pw.BoxDecoration(color: PdfColors.grey200),
      cellHeight: 30,
      cellAlignments: {
        0: pw.Alignment.centerLeft,
        1: pw.Alignment.center,
        2: pw.Alignment.center,
        3: pw.Alignment.center,
      },
    );
  }

  pw.Widget _buildFooter() {
    return pw.Column(
      children: [
        pw.Divider(),
        pw.SizedBox(height: 10),
        pw.Text(
          'Disclaimer: This report is generated by an app and is not a substitute for professional medical advice. Please discuss these results with your healthcare provider.',
          style: const pw.TextStyle(fontSize: 8, color: PdfColors.grey600),
          textAlign: pw.TextAlign.center,
        ),
      ],
    );
  }
}

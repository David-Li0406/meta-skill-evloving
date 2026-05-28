import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/utils/date_utils.dart';

void main() {
  group('getLogicalDate', () {
    test('returns same day when hour is 4 AM or later', () {
      // 5 AM on Jan 15th
      final fiveAM = DateTime(2026, 1, 15, 5, 0, 0);
      final result = getLogicalDate(fiveAM);
      expect(result.day, 15);
      expect(result.month, 1);
      expect(result.year, 2026);
    });

    test('returns same day when hour is exactly 4 AM', () {
      // Exactly 4 AM on Jan 15th
      final fourAM = DateTime(2026, 1, 15, 4, 0, 0);
      final result = getLogicalDate(fourAM);
      expect(result.day, 15);
    });

    test('returns previous day when hour is before 4 AM', () {
      // 2:30 AM on Jan 15th -> should return Jan 14th
      final twoAM = DateTime(2026, 1, 15, 2, 30, 0);
      final result = getLogicalDate(twoAM);
      expect(result.day, 14);
      expect(result.month, 1);
    });

    test('handles midnight correctly (returns previous day)', () {
      // Midnight on Jan 15th -> should return Jan 14th
      final midnight = DateTime(2026, 1, 15, 0, 0, 0);
      final result = getLogicalDate(midnight);
      expect(result.day, 14);
    });

    test('handles month boundary correctly', () {
      // 1 AM on Feb 1st -> should return Jan 31st
      final earlyFeb = DateTime(2026, 2, 1, 1, 0, 0);
      final result = getLogicalDate(earlyFeb);
      expect(result.day, 31);
      expect(result.month, 1);
    });

    test('handles year boundary correctly', () {
      // 3 AM on Jan 1st, 2026 -> should return Dec 31st, 2025
      final earlyNewYear = DateTime(2026, 1, 1, 3, 0, 0);
      final result = getLogicalDate(earlyNewYear);
      expect(result.day, 31);
      expect(result.month, 12);
      expect(result.year, 2025);
    });
  });

  group('getLogicalDateString', () {
    test('returns ISO8601 date string for same day', () {
      final afternoon = DateTime(2026, 1, 15, 14, 30, 0);
      final result = getLogicalDateString(afternoon);
      expect(result, '2026-01-15');
    });

    test('returns previous day ISO8601 string when before 4 AM', () {
      final lateNight = DateTime(2026, 1, 15, 1, 0, 0);
      final result = getLogicalDateString(lateNight);
      expect(result, '2026-01-14');
    });
  });
}

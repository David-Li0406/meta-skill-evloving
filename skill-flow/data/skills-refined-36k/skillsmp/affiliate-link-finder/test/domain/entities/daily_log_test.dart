import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/daily_log.dart';

void main() {
  group('DailyLog', () {
    test('should create DailyLog with all required fields', () {
      final now = DateTime.now();
      final log = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [],
        createdAt: now,
      );

      expect(log.id, 'log1');
      expect(log.userId, 'user1');
      expect(log.date, now);
      expect(log.entries, isEmpty);
      expect(log.createdAt, now);
    });

    test('should create DailyLog with optional fields', () {
      final now = DateTime.now();
      final log = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [],
        symptomRatings: {'focus': 4, 'energy': 3},
        notes: 'Feeling good today',
        createdAt: now,
      );

      expect(log.symptomRatings, {'focus': 4, 'energy': 3});
      expect(log.notes, 'Feeling good today');
    });

    test('copyWith should update specified fields', () {
      final now = DateTime.now();
      final original = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [],
        symptomRatings: {'focus': 3},
        notes: 'Original notes',
        createdAt: now,
      );

      final updated = original.copyWith(
        notes: 'Updated notes',
        symptomRatings: {'focus': 5},
      );

      expect(updated.id, original.id);
      expect(updated.userId, original.userId);
      expect(updated.date, original.date);
      expect(updated.entries, original.entries);
      expect(updated.notes, 'Updated notes');
      expect(updated.symptomRatings, {'focus': 5});
      expect(updated.createdAt, original.createdAt);
    });

    test('copyWith should preserve original values when null', () {
      final now = DateTime.now();
      final original = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [
          LogEntry(
            supplementId: 'sup1',
            takenAt: now,
            status: LogStatus.taken,
          )
        ],
        symptomRatings: {'focus': 3},
        notes: 'Original notes',
        createdAt: now,
      );

      final updated = original.copyWith();

      expect(updated.id, original.id);
      expect(updated.userId, original.userId);
      expect(updated.date, original.date);
      expect(updated.entries, original.entries);
      expect(updated.notes, original.notes);
      expect(updated.symptomRatings, original.symptomRatings);
      expect(updated.createdAt, original.createdAt);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final log = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [
          LogEntry(
            supplementId: 'sup1',
            takenAt: now,
            status: LogStatus.taken,
            skippedReason: null,
          ),
        ],
        symptomRatings: {'focus': 4},
        notes: 'Test notes',
        createdAt: now,
      );

      final json = log.toJson();

      expect(json['id'], 'log1');
      expect(json['userId'], 'user1');
      expect(json['date'], now.toIso8601String());
      expect(json['entries'], isA<List<dynamic>>());
      expect(json['entries'].length, 1);
      expect(json['symptomRatings'], {'focus': 4});
      expect(json['notes'], 'Test notes');
      expect(json['createdAt'], now.toIso8601String());
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'id': 'log1',
        'userId': 'user1',
        'date': now.toIso8601String(),
        'entries': [
          {
            'supplementId': 'sup1',
            'takenAt': now.toIso8601String(),
            'status': 'taken',
            'skippedReason': null,
          }
        ],
        'symptomRatings': {'focus': 4, 'energy': 3},
        'notes': 'Test notes',
        'createdAt': now.toIso8601String(),
      };

      final log = DailyLog.fromJson(json);

      expect(log.id, 'log1');
      expect(log.userId, 'user1');
      expect(log.date.year, now.year);
      expect(log.date.month, now.month);
      expect(log.date.day, now.day);
      expect(log.entries.length, 1);
      expect(log.entries.first.supplementId, 'sup1');
      expect(log.symptomRatings, {'focus': 4, 'energy': 3});
      expect(log.notes, 'Test notes');
    });

    test('fromJson should handle null optional fields', () {
      final now = DateTime.now();
      final json = {
        'id': 'log1',
        'userId': 'user1',
        'date': now.toIso8601String(),
        'entries': <Map<String, dynamic>>[],
        'createdAt': now.toIso8601String(),
      };

      final log = DailyLog.fromJson(json);

      expect(log.symptomRatings, null);
      expect(log.notes, null);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = DailyLog(
        id: 'log1',
        userId: 'user1',
        date: now,
        entries: [
          LogEntry(
            supplementId: 'sup1',
            takenAt: now,
            status: LogStatus.taken,
            skippedReason: 'Forgot',
          ),
        ],
        symptomRatings: {'focus': 4},
        notes: 'Test notes',
        createdAt: now,
      );

      final json = original.toJson();
      final restored = DailyLog.fromJson(json);

      expect(restored.id, original.id);
      expect(restored.userId, original.userId);
      expect(restored.entries.length, original.entries.length);
      expect(restored.entries.first.supplementId,
          original.entries.first.supplementId);
      expect(restored.entries.first.taken, original.entries.first.taken);
      expect(restored.entries.first.skippedReason,
          original.entries.first.skippedReason);
      expect(restored.symptomRatings, original.symptomRatings);
      expect(restored.notes, original.notes);
    });
  });

  group('LogEntry', () {
    test('should create LogEntry with all fields', () {
      final now = DateTime.now();
      final entry = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.taken,
        skippedReason: null,
      );

      expect(entry.supplementId, 'sup1');
      expect(entry.takenAt, now);
      expect(entry.taken, true);
      expect(entry.skippedReason, null);
    });

    test('should create LogEntry with skippedReason', () {
      final now = DateTime.now();
      final entry = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.skipped,
        skippedReason: 'Forgot to take',
      );

      expect(entry.taken, false);
      expect(entry.skippedReason, 'Forgot to take');
    });

    test('copyWith should update specified fields', () {
      final now = DateTime.now();
      final original = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.skipped,
        skippedReason: 'Forgot',
      );

      final updated = original.copyWith(
        status: LogStatus.taken,
        skippedReason: null,
      );

      expect(updated.supplementId, original.supplementId);
      expect(updated.takenAt, original.takenAt);
      expect(updated.taken, true);
      expect(updated.skippedReason, null);
    });

    test('copyWith should preserve original values when null', () {
      final now = DateTime.now();
      final original = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.taken,
        skippedReason: 'Original reason',
      );

      final updated = original.copyWith();

      expect(updated.supplementId, original.supplementId);
      expect(updated.takenAt, original.takenAt);
      expect(updated.taken, original.taken);
      expect(updated.skippedReason, original.skippedReason);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final entry = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.taken,
        skippedReason: 'Forgot',
      );

      final json = entry.toJson();

      expect(json['supplementId'], 'sup1');
      expect(json['takenAt'], now.toIso8601String());
      expect(json['status'], 'taken');
      expect(json['skippedReason'], 'Forgot');
    });

    test('toJson should handle null skippedReason', () {
      final now = DateTime.now();
      final entry = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.taken,
        skippedReason: null,
      );

      final json = entry.toJson();

      expect(json['skippedReason'], null);
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'supplementId': 'sup1',
        'takenAt': now.toIso8601String(),
        'taken': true,
        'skippedReason': 'Forgot',
      };

      final entry = LogEntry.fromJson(json);

      expect(entry.supplementId, 'sup1');
      expect(entry.takenAt.year, now.year);
      expect(entry.takenAt.month, now.month);
      expect(entry.takenAt.day, now.day);
      expect(entry.taken, true);
      expect(entry.skippedReason, 'Forgot');
    });

    test('fromJson should handle null skippedReason', () {
      final now = DateTime.now();
      final json = {
        'supplementId': 'sup1',
        'takenAt': now.toIso8601String(),
        'taken': true,
        'skippedReason': null,
      };

      final entry = LogEntry.fromJson(json);

      expect(entry.skippedReason, null);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = LogEntry(
        supplementId: 'sup1',
        takenAt: now,
        status: LogStatus.skipped,
        skippedReason: 'Forgot to take',
      );

      final json = original.toJson();
      final restored = LogEntry.fromJson(json);

      expect(restored.supplementId, original.supplementId);
      expect(restored.takenAt.year, original.takenAt.year);
      expect(restored.takenAt.month, original.takenAt.month);
      expect(restored.takenAt.day, original.takenAt.day);
      expect(restored.taken, original.taken);
      expect(restored.skippedReason, original.skippedReason);
    });
  });
}

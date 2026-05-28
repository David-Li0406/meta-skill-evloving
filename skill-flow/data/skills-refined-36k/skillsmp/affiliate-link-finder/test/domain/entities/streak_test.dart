import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/streak.dart';

void main() {
  group('Streak', () {
    test('should create Streak with all required fields', () {
      final now = DateTime.now();
      final streak = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      expect(streak.userId, 'user1');
      expect(streak.currentStreak, 5);
      expect(streak.longestStreak, 10);
      expect(streak.lastCompletedDate, now);
      expect(streak.graceDaysRemaining, 2);
      expect(streak.graceDaysUsed, 1);
      expect(streak.updatedAt, now);
    });

    test('should create Streak with null lastCompletedDate', () {
      final now = DateTime.now();
      final streak = Streak(
        userId: 'user1',
        currentStreak: 0,
        longestStreak: 0,
        lastCompletedDate: null,
        graceDaysRemaining: 2,
        graceDaysUsed: 0,
        updatedAt: now,
      );

      expect(streak.lastCompletedDate, null);
    });

    test('Streak.initial should create initial streak', () {
      final streak = Streak.initial('user1');

      expect(streak.userId, 'user1');
      expect(streak.currentStreak, 0);
      expect(streak.longestStreak, 0);
      expect(streak.lastCompletedDate, null);
      expect(streak.graceDaysRemaining, 2);
      expect(streak.graceDaysUsed, 0);
      expect(streak.updatedAt, isA<DateTime>());
    });

    test('copyWith should update specified fields', () {
      final now = DateTime.now();
      final original = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      final updated = original.copyWith(
        currentStreak: 6,
        graceDaysRemaining: 1,
      );

      expect(updated.userId, original.userId);
      expect(updated.currentStreak, 6);
      expect(updated.longestStreak, original.longestStreak);
      expect(updated.lastCompletedDate, original.lastCompletedDate);
      expect(updated.graceDaysRemaining, 1);
      expect(updated.graceDaysUsed, original.graceDaysUsed);
      expect(updated.updatedAt, original.updatedAt);
    });

    test('copyWith should preserve original values when null', () {
      final now = DateTime.now();
      final original = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      final updated = original.copyWith();

      expect(updated.userId, original.userId);
      expect(updated.currentStreak, original.currentStreak);
      expect(updated.longestStreak, original.longestStreak);
      expect(updated.lastCompletedDate, original.lastCompletedDate);
      expect(updated.graceDaysRemaining, original.graceDaysRemaining);
      expect(updated.graceDaysUsed, original.graceDaysUsed);
      expect(updated.updatedAt, original.updatedAt);
    });

    test('copyWith should handle null lastCompletedDate', () {
      final now = DateTime.now();
      final original = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      final updated = original.copyWith(lastCompletedDate: null);

      expect(updated.lastCompletedDate, null);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final streak = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      final json = streak.toJson();

      expect(json['userId'], 'user1');
      expect(json['currentStreak'], 5);
      expect(json['longestStreak'], 10);
      expect(json['lastCompletedDate'], now.toIso8601String());
      expect(json['graceDaysRemaining'], 2);
      expect(json['graceDaysUsed'], 1);
      expect(json['updatedAt'], now.toIso8601String());
    });

    test('toJson should handle null lastCompletedDate', () {
      final now = DateTime.now();
      final streak = Streak(
        userId: 'user1',
        currentStreak: 0,
        longestStreak: 0,
        lastCompletedDate: null,
        graceDaysRemaining: 2,
        graceDaysUsed: 0,
        updatedAt: now,
      );

      final json = streak.toJson();

      expect(json['lastCompletedDate'], null);
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'userId': 'user1',
        'currentStreak': 5,
        'longestStreak': 10,
        'lastCompletedDate': now.toIso8601String(),
        'graceDaysRemaining': 2,
        'graceDaysUsed': 1,
        'updatedAt': now.toIso8601String(),
      };

      final streak = Streak.fromJson(json);

      expect(streak.userId, 'user1');
      expect(streak.currentStreak, 5);
      expect(streak.longestStreak, 10);
      expect(streak.lastCompletedDate, isNotNull);
      expect(streak.lastCompletedDate!.year, now.year);
      expect(streak.lastCompletedDate!.month, now.month);
      expect(streak.lastCompletedDate!.day, now.day);
      expect(streak.graceDaysRemaining, 2);
      expect(streak.graceDaysUsed, 1);
      expect(streak.updatedAt.year, now.year);
    });

    test('fromJson should handle null lastCompletedDate', () {
      final now = DateTime.now();
      final json = {
        'userId': 'user1',
        'currentStreak': 0,
        'longestStreak': 0,
        'lastCompletedDate': null,
        'graceDaysRemaining': 2,
        'graceDaysUsed': 0,
        'updatedAt': now.toIso8601String(),
      };

      final streak = Streak.fromJson(json);

      expect(streak.lastCompletedDate, null);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = Streak(
        userId: 'user1',
        currentStreak: 5,
        longestStreak: 10,
        lastCompletedDate: now,
        graceDaysRemaining: 2,
        graceDaysUsed: 1,
        updatedAt: now,
      );

      final json = original.toJson();
      final restored = Streak.fromJson(json);

      expect(restored.userId, original.userId);
      expect(restored.currentStreak, original.currentStreak);
      expect(restored.longestStreak, original.longestStreak);
      expect(restored.lastCompletedDate, isNotNull);
      expect(restored.lastCompletedDate!.year, original.lastCompletedDate!.year);
      expect(restored.lastCompletedDate!.month, original.lastCompletedDate!.month);
      expect(restored.lastCompletedDate!.day, original.lastCompletedDate!.day);
      expect(restored.graceDaysRemaining, original.graceDaysRemaining);
      expect(restored.graceDaysUsed, original.graceDaysUsed);
    });

    test('toJson and fromJson should be reversible with null lastCompletedDate', () {
      final now = DateTime.now();
      final original = Streak(
        userId: 'user1',
        currentStreak: 0,
        longestStreak: 0,
        lastCompletedDate: null,
        graceDaysRemaining: 2,
        graceDaysUsed: 0,
        updatedAt: now,
      );

      final json = original.toJson();
      final restored = Streak.fromJson(json);

      expect(restored.lastCompletedDate, null);
    });
  });
}

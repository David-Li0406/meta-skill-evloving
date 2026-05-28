import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:adhd_supplement_app/domain/entities/medication.dart';

void main() {
  group('User Entity', () {
    final baseUser = User(
      id: '123',
      email: 'test@example.com',
      createdAt: DateTime(2023, 1, 1),
    );

    test('should copyWith level and xp correctly', () {
      final updatedUser = baseUser.copyWith(
        level: 10,
        xp: 2500,
      );

      expect(updatedUser.level, 10);
      expect(updatedUser.xp, 2500);
      expect(updatedUser.email, baseUser.email);
    });

    test('should copyWith unlockedAchievements correctly', () {
      final updatedUser = baseUser.copyWith(
        unlockedAchievements: ['badge_1', 'badge_2'],
      );

      expect(updatedUser.unlockedAchievements.length, 2);
      expect(updatedUser.unlockedAchievements, contains('badge_1'));
      expect(updatedUser.unlockedAchievements, contains('badge_2'));
    });

    test('should copyWith currentMedication correctly', () {
      final med = Medication.fromName('Adderall XR', dosage: 20);
      final updatedUser = baseUser.copyWith(currentMedication: med);

      expect(updatedUser.currentMedication, isNotNull);
      expect(updatedUser.currentMedication?.name, 'Adderall XR');
      expect(updatedUser.currentMedication?.dosageMg, 20);
    });

    test('should serialize unlockedAchievements and medication to JSON', () {
      final med = Medication.fromName('Vyvanse', dosage: 30);
      final user = baseUser.copyWith(
        unlockedAchievements: ['badge_1'],
        level: 5,
        xp: 500,
        currentMedication: med,
      );

      final json = user.toJson();

      expect(json['unlockedAchievements'], isA<List<String>>());
      expect(json['unlockedAchievements'], contains('badge_1'));
      expect(json['level'], 5);
      expect(json['xp'], 500);
      expect(json['currentMedication'], isNotNull);
      expect(json['currentMedication']['name'], 'Vyvanse');
    });

    test('should deserialize unlockedAchievements and medication from JSON',
        () {
      final json = {
        'id': '123',
        'email': 'test@example.com',
        'createdAt': '2023-01-01T00:00:00.000',
        'level': 2,
        'xp': 100,
        'unlockedAchievements': ['badge_3', 'badge_4'],
        'currentMedication': {
          'id': 'm1',
          'name': 'Concerta',
          'type': 'stimulant',
          'dosageMg': 18.0,
        },
      };

      final user = User.fromJson(json);

      expect(user.level, 2);
      expect(user.unlockedAchievements.length, 2);
      expect(user.unlockedAchievements, contains('badge_3'));
      expect(user.currentMedication, isNotNull);
      expect(user.currentMedication?.name, 'Concerta');
      expect(user.currentMedication?.type, MedicationType.stimulant);
    });

    test('should handle missing unlockedAchievements in JSON gracefully', () {
      final json = {
        'id': '123',
        'email': 'test@example.com',
        'createdAt': '2023-01-01T00:00:00.000',
        // unlockedAchievements missing
      };

      final user = User.fromJson(json);

      expect(user.unlockedAchievements, isEmpty);
    });
  });
}

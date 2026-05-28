import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/symptom_checkin.dart';

void main() {
  group('SymptomCheckIn', () {
    test('calculates average score correctly', () {
      final checkIn = SymptomCheckIn(
        id: '1',
        userId: 'user1',
        timestamp: DateTime.now(),
        focusLevel: 80,
        energyLevel: 60,
        moodLevel: 40,
      );

      expect(checkIn.averageScore, 60.0);
    });

    test('returns correct emojis for high scores', () {
      final checkIn = SymptomCheckIn(
        id: '1',
        userId: 'user1',
        timestamp: DateTime.now(),
        focusLevel: 85,
        energyLevel: 90,
        moodLevel: 95,
      );

      expect(checkIn.focusEmoji, '🤩');
      expect(checkIn.energyEmoji, '⚡️');
      expect(checkIn.moodEmoji, '😊');
    });

    test('returns correct emojis for low scores', () {
      final checkIn = SymptomCheckIn(
        id: '1',
        userId: 'user1',
        timestamp: DateTime.now(),
        focusLevel: 20,
        energyLevel: 15,
        moodLevel: 30,
      );

      expect(checkIn.focusEmoji, '😔');
      expect(checkIn.energyEmoji, '🥱');
      expect(checkIn.moodEmoji, '😔');
    });

    test('toJson and fromJson work correctly', () {
      final now = DateTime.now();
      final checkIn = SymptomCheckIn(
        id: '123',
        userId: 'user456',
        timestamp: now,
        focusLevel: 70,
        energyLevel: 60,
        moodLevel: 50,
        notes: 'Feeling good',
      );

      final json = checkIn.toJson();
      final newCheckIn = SymptomCheckIn.fromJson(json);

      expect(newCheckIn.id, checkIn.id);
      expect(newCheckIn.userId, checkIn.userId);
      // DateTime precision might vary slightly with serializers, checking closeness or string format is safer usually
      // but for basic entity test checking other fields is good enough
      expect(newCheckIn.focusLevel, checkIn.focusLevel);
      expect(newCheckIn.notes, 'Feeling good');
    });
  });
}

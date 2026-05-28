import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/safety_override.dart';

void main() {
  group('SafetyOverride', () {
    test('should create SafetyOverride with all required fields', () {
      final now = DateTime.now();
      final override = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
      );

      expect(override.id, 'override1');
      expect(override.userId, 'user1');
      expect(override.interactionId, 'interaction1');
      expect(override.timestamp, now);
      expect(override.userReason, null);
      expect(override.isAcknowledged, false);
    });

    test('should create SafetyOverride with optional fields', () {
      final now = DateTime.now();
      final override = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
        userReason: 'Doctor approved',
        isAcknowledged: true,
      );

      expect(override.userReason, 'Doctor approved');
      expect(override.isAcknowledged, true);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final override = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
        userReason: 'Doctor approved',
        isAcknowledged: true,
      );

      final json = override.toJson();

      expect(json['id'], 'override1');
      expect(json['userId'], 'user1');
      expect(json['interactionId'], 'interaction1');
      expect(json['timestamp'], now.toIso8601String());
      expect(json['userReason'], 'Doctor approved');
      expect(json['isAcknowledged'], true);
    });

    test('toJson should handle null userReason', () {
      final now = DateTime.now();
      final override = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
        userReason: null,
        isAcknowledged: false,
      );

      final json = override.toJson();

      expect(json['userReason'], null);
      expect(json['isAcknowledged'], false);
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'id': 'override1',
        'userId': 'user1',
        'interactionId': 'interaction1',
        'timestamp': now.toIso8601String(),
        'userReason': 'Doctor approved',
        'isAcknowledged': true,
      };

      final override = SafetyOverride.fromJson(json);

      expect(override.id, 'override1');
      expect(override.userId, 'user1');
      expect(override.interactionId, 'interaction1');
      expect(override.timestamp.year, now.year);
      expect(override.timestamp.month, now.month);
      expect(override.timestamp.day, now.day);
      expect(override.userReason, 'Doctor approved');
      expect(override.isAcknowledged, true);
    });

    test('fromJson should handle null userReason', () {
      final now = DateTime.now();
      final json = {
        'id': 'override1',
        'userId': 'user1',
        'interactionId': 'interaction1',
        'timestamp': now.toIso8601String(),
        'userReason': null,
        'isAcknowledged': false,
      };

      final override = SafetyOverride.fromJson(json);

      expect(override.userReason, null);
      expect(override.isAcknowledged, false);
    });

    test('fromJson should default isAcknowledged to false when missing', () {
      final now = DateTime.now();
      final json = {
        'id': 'override1',
        'userId': 'user1',
        'interactionId': 'interaction1',
        'timestamp': now.toIso8601String(),
        'userReason': null,
      };

      final override = SafetyOverride.fromJson(json);

      expect(override.isAcknowledged, false);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
        userReason: 'Doctor approved',
        isAcknowledged: true,
      );

      final json = original.toJson();
      final restored = SafetyOverride.fromJson(json);

      expect(restored.id, original.id);
      expect(restored.userId, original.userId);
      expect(restored.interactionId, original.interactionId);
      expect(restored.timestamp.year, original.timestamp.year);
      expect(restored.timestamp.month, original.timestamp.month);
      expect(restored.timestamp.day, original.timestamp.day);
      expect(restored.userReason, original.userReason);
      expect(restored.isAcknowledged, original.isAcknowledged);
    });

    test('toJson and fromJson should be reversible with null userReason', () {
      final now = DateTime.now();
      final original = SafetyOverride(
        id: 'override1',
        userId: 'user1',
        interactionId: 'interaction1',
        timestamp: now,
        userReason: null,
        isAcknowledged: false,
      );

      final json = original.toJson();
      final restored = SafetyOverride.fromJson(json);

      expect(restored.userReason, null);
      expect(restored.isAcknowledged, false);
    });
  });
}

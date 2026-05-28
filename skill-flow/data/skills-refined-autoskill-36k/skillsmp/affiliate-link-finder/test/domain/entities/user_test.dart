import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';

void main() {
  group('User', () {
    test('should create User with all required fields', () {
      final now = DateTime.now();
      final user = User(
        id: 'user1',
        email: 'test@example.com',
        createdAt: now,
      );

      expect(user.id, 'user1');
      expect(user.email, 'test@example.com');
      expect(user.createdAt, now);
      expect(user.displayName, null);
      expect(user.photoUrl, null);
      expect(user.hasCompletedOnboarding, false);
    });

    test('should create User with optional fields', () {
      final now = DateTime.now();
      final user = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Test User',
        photoUrl: 'https://example.com/photo.jpg',
        createdAt: now,
        hasCompletedOnboarding: true,
      );

      expect(user.displayName, 'Test User');
      expect(user.photoUrl, 'https://example.com/photo.jpg');
      expect(user.hasCompletedOnboarding, true);
    });

    test('copyWith should update specified fields', () {
      final now = DateTime.now();
      final original = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Original Name',
        createdAt: now,
        hasCompletedOnboarding: false,
      );

      final updated = original.copyWith(
        displayName: 'Updated Name',
        hasCompletedOnboarding: true,
      );

      expect(updated.id, original.id);
      expect(updated.email, original.email);
      expect(updated.displayName, 'Updated Name');
      expect(updated.photoUrl, original.photoUrl);
      expect(updated.createdAt, original.createdAt);
      expect(updated.hasCompletedOnboarding, true);
    });

    test('copyWith should preserve original values when null', () {
      final now = DateTime.now();
      final original = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Test User',
        photoUrl: 'https://example.com/photo.jpg',
        createdAt: now,
        hasCompletedOnboarding: true,
      );

      final updated = original.copyWith();

      expect(updated.id, original.id);
      expect(updated.email, original.email);
      expect(updated.displayName, original.displayName);
      expect(updated.photoUrl, original.photoUrl);
      expect(updated.createdAt, original.createdAt);
      expect(updated.hasCompletedOnboarding, original.hasCompletedOnboarding);
    });

    test('copyWith should handle null optional fields', () {
      final now = DateTime.now();
      final original = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Test User',
        photoUrl: 'https://example.com/photo.jpg',
        createdAt: now,
      );

      final updated = original.copyWith(
        displayName: null,
        photoUrl: null,
      );

      expect(updated.displayName, null);
      expect(updated.photoUrl, null);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final user = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Test User',
        photoUrl: 'https://example.com/photo.jpg',
        createdAt: now,
        hasCompletedOnboarding: true,
      );

      final json = user.toJson();

      expect(json['id'], 'user1');
      expect(json['email'], 'test@example.com');
      expect(json['displayName'], 'Test User');
      expect(json['photoUrl'], 'https://example.com/photo.jpg');
      expect(json['createdAt'], now.toIso8601String());
      expect(json['hasCompletedOnboarding'], true);
    });

    test('toJson should handle null optional fields', () {
      final now = DateTime.now();
      final user = User(
        id: 'user1',
        email: 'test@example.com',
        createdAt: now,
      );

      final json = user.toJson();

      expect(json['displayName'], null);
      expect(json['photoUrl'], null);
      expect(json['hasCompletedOnboarding'], false);
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'id': 'user1',
        'email': 'test@example.com',
        'displayName': 'Test User',
        'photoUrl': 'https://example.com/photo.jpg',
        'createdAt': now.toIso8601String(),
        'hasCompletedOnboarding': true,
      };

      final user = User.fromJson(json);

      expect(user.id, 'user1');
      expect(user.email, 'test@example.com');
      expect(user.displayName, 'Test User');
      expect(user.photoUrl, 'https://example.com/photo.jpg');
      expect(user.createdAt.year, now.year);
      expect(user.createdAt.month, now.month);
      expect(user.createdAt.day, now.day);
      expect(user.hasCompletedOnboarding, true);
    });

    test('fromJson should handle null optional fields', () {
      final now = DateTime.now();
      final json = {
        'id': 'user1',
        'email': 'test@example.com',
        'displayName': null,
        'photoUrl': null,
        'createdAt': now.toIso8601String(),
        'hasCompletedOnboarding': false,
      };

      final user = User.fromJson(json);

      expect(user.displayName, null);
      expect(user.photoUrl, null);
      expect(user.hasCompletedOnboarding, false);
    });

    test('fromJson should default hasCompletedOnboarding to false when missing', () {
      final now = DateTime.now();
      final json = {
        'id': 'user1',
        'email': 'test@example.com',
        'createdAt': now.toIso8601String(),
      };

      final user = User.fromJson(json);

      expect(user.hasCompletedOnboarding, false);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = User(
        id: 'user1',
        email: 'test@example.com',
        displayName: 'Test User',
        photoUrl: 'https://example.com/photo.jpg',
        createdAt: now,
        hasCompletedOnboarding: true,
      );

      final json = original.toJson();
      final restored = User.fromJson(json);

      expect(restored.id, original.id);
      expect(restored.email, original.email);
      expect(restored.displayName, original.displayName);
      expect(restored.photoUrl, original.photoUrl);
      expect(restored.createdAt.year, original.createdAt.year);
      expect(restored.createdAt.month, original.createdAt.month);
      expect(restored.createdAt.day, original.createdAt.day);
      expect(restored.hasCompletedOnboarding, original.hasCompletedOnboarding);
    });

    test('toJson and fromJson should be reversible with null optional fields', () {
      final now = DateTime.now();
      final original = User(
        id: 'user1',
        email: 'test@example.com',
        createdAt: now,
      );

      final json = original.toJson();
      final restored = User.fromJson(json);

      expect(restored.displayName, null);
      expect(restored.photoUrl, null);
      expect(restored.hasCompletedOnboarding, false);
    });
  });
}

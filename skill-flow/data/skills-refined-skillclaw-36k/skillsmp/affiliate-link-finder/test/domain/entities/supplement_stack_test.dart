import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_stack.dart';

void main() {
  group('StackItem', () {
    test('should create StackItem with required and optional fields', () {
      const item = StackItem(
        supplementId: 'sup1',
        customDosage: '100mg',
        customNotes: 'Take with food',
        order: 1,
      );

      expect(item.supplementId, 'sup1');
      expect(item.customDosage, '100mg');
      expect(item.customNotes, 'Take with food');
      expect(item.order, 1);
    });

    test('copyWith should update specified fields and preserve others', () {
      const original = StackItem(
        supplementId: 'sup1',
        customDosage: '100mg',
        customNotes: 'Original notes',
        order: 1,
      );

      final updated = original.copyWith(
        customDosage: '200mg',
        customNotes: 'Updated notes',
        order: 2,
      );

      expect(updated.supplementId, original.supplementId);
      expect(updated.customDosage, '200mg');
      expect(updated.customNotes, 'Updated notes');
      expect(updated.order, 2);
    });

    test('copyWith with no arguments should preserve all values', () {
      const original = StackItem(
        supplementId: 'sup1',
        customDosage: '100mg',
        customNotes: 'Notes',
        order: 1,
      );

      final updated = original.copyWith();

      expect(updated.supplementId, original.supplementId);
      expect(updated.customDosage, original.customDosage);
      expect(updated.customNotes, original.customNotes);
      expect(updated.order, original.order);
    });

    test('toJson should serialize correctly', () {
      const item = StackItem(
        supplementId: 'sup1',
        customDosage: '100mg',
        customNotes: 'Notes',
        order: 1,
      );

      final json = item.toJson();

      expect(json['supplementId'], 'sup1');
      expect(json['customDosage'], '100mg');
      expect(json['customNotes'], 'Notes');
      expect(json['order'], 1);
    });

    test('fromJson should deserialize correctly', () {
      final json = {
        'supplementId': 'sup1',
        'customDosage': '100mg',
        'customNotes': 'Notes',
        'order': 1,
      };

      final item = StackItem.fromJson(json);

      expect(item.supplementId, 'sup1');
      expect(item.customDosage, '100mg');
      expect(item.customNotes, 'Notes');
      expect(item.order, 1);
    });

    test('fromJson should handle null optional fields', () {
      final json = {
        'supplementId': 'sup1',
        'customDosage': null,
        'customNotes': null,
        'order': 1,
      };

      final item = StackItem.fromJson(json);

      expect(item.customDosage, null);
      expect(item.customNotes, null);
    });
  });

  group('SupplementStack', () {
    test('should create SupplementStack with required fields', () {
      final now = DateTime.now();
      final stack = SupplementStack(
        id: 'stack1',
        userId: 'user1',
        name: 'Morning Stack',
        items: const [
          StackItem(
            supplementId: 'sup1',
            customDosage: '100mg',
            customNotes: 'Notes',
            order: 1,
          ),
        ],
        timeOfDay: 'morning',
        createdAt: now,
        updatedAt: now,
      );

      expect(stack.id, 'stack1');
      expect(stack.userId, 'user1');
      expect(stack.name, 'Morning Stack');
      expect(stack.items.length, 1);
      expect(stack.timeOfDay, 'morning');
      expect(stack.createdAt, now);
      expect(stack.updatedAt, now);
    });

    test('copyWith should update specified fields and preserve others', () {
      final now = DateTime.now();
      final original = SupplementStack(
        id: 'stack1',
        userId: 'user1',
        name: 'Morning Stack',
        items: const [
          StackItem(
            supplementId: 'sup1',
            customDosage: '100mg',
            customNotes: 'Notes',
            order: 1,
          ),
        ],
        timeOfDay: 'morning',
        createdAt: now,
        updatedAt: now,
      );

      final later = now.add(const Duration(days: 1));
      final updated = original.copyWith(
        name: 'Updated Stack',
        timeOfDay: 'evening',
        updatedAt: later,
      );

      expect(updated.id, original.id);
      expect(updated.userId, original.userId);
      expect(updated.name, 'Updated Stack');
      expect(updated.items, original.items);
      expect(updated.timeOfDay, 'evening');
      expect(updated.createdAt, original.createdAt);
      expect(updated.updatedAt, later);
    });

    test('copyWith with no arguments should preserve all values', () {
      final now = DateTime.now();
      final original = SupplementStack(
        id: 'stack1',
        userId: 'user1',
        name: 'Morning Stack',
        items: const [
          StackItem(
            supplementId: 'sup1',
            customDosage: '100mg',
            customNotes: 'Notes',
            order: 1,
          ),
        ],
        timeOfDay: 'morning',
        createdAt: now,
        updatedAt: now,
      );

      final updated = original.copyWith();

      expect(updated.id, original.id);
      expect(updated.userId, original.userId);
      expect(updated.name, original.name);
      expect(updated.items, original.items);
      expect(updated.timeOfDay, original.timeOfDay);
      expect(updated.createdAt, original.createdAt);
      expect(updated.updatedAt, original.updatedAt);
    });

    test('toJson should serialize correctly', () {
      final now = DateTime.now();
      final stack = SupplementStack(
        id: 'stack1',
        userId: 'user1',
        name: 'Morning Stack',
        items: const [
          StackItem(
            supplementId: 'sup1',
            customDosage: '100mg',
            customNotes: 'Notes',
            order: 1,
          ),
        ],
        timeOfDay: 'morning',
        createdAt: now,
        updatedAt: now,
      );

      final json = stack.toJson();

      expect(json['id'], 'stack1');
      expect(json['userId'], 'user1');
      expect(json['name'], 'Morning Stack');
      expect(json['items'], isA<List<dynamic>>());
      expect((json['items'] as List).length, 1);
      expect(json['timeOfDay'], 'morning');
      expect(json['createdAt'], now.toIso8601String());
      expect(json['updatedAt'], now.toIso8601String());
    });

    test('fromJson should deserialize correctly', () {
      final now = DateTime.now();
      final json = {
        'id': 'stack1',
        'userId': 'user1',
        'name': 'Morning Stack',
        'items': [
          {
            'supplementId': 'sup1',
            'customDosage': '100mg',
            'customNotes': 'Notes',
            'order': 1,
          }
        ],
        'timeOfDay': 'morning',
        'createdAt': now.toIso8601String(),
        'updatedAt': now.toIso8601String(),
      };

      final stack = SupplementStack.fromJson(json);

      expect(stack.id, 'stack1');
      expect(stack.userId, 'user1');
      expect(stack.name, 'Morning Stack');
      expect(stack.items.length, 1);
      expect(stack.items.first.supplementId, 'sup1');
      expect(stack.timeOfDay, 'morning');
      expect(stack.createdAt.year, now.year);
      expect(stack.updatedAt.year, now.year);
    });

    test('toJson and fromJson should be reversible', () {
      final now = DateTime.now();
      final original = SupplementStack(
        id: 'stack1',
        userId: 'user1',
        name: 'Morning Stack',
        items: const [
          StackItem(
            supplementId: 'sup1',
            customDosage: '100mg',
            customNotes: 'Notes',
            order: 1,
          ),
        ],
        timeOfDay: 'morning',
        createdAt: now,
        updatedAt: now,
      );

      final json = original.toJson();
      final restored = SupplementStack.fromJson(json);

      expect(restored.id, original.id);
      expect(restored.userId, original.userId);
      expect(restored.name, original.name);
      expect(restored.items.length, original.items.length);
      expect(
          restored.items.first.supplementId, original.items.first.supplementId);
      expect(restored.timeOfDay, original.timeOfDay);
      expect(restored.createdAt.year, original.createdAt.year);
      expect(restored.updatedAt.year, original.updatedAt.year);
    });
  });
}

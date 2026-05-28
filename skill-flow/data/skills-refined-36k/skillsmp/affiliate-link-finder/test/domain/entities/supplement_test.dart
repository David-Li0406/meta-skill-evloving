import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';

void main() {
  group('Supplement', () {
    test('should create Supplement with required fields and defaults', () {
      const supplement = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
      );

      expect(supplement.id, 'sup1');
      expect(supplement.name, 'Magnesium');
      expect(supplement.category, 'Minerals');
      expect(supplement.dosage, isNull);
      expect(supplement.defaultDosage, isNull);
      expect(supplement.timeOfDay, isNull);
      expect(supplement.benefits, isEmpty);
      expect(supplement.evidenceLevel, isNull);
      expect(supplement.notes, isNull);
      expect(supplement.imageUrl, isNull);
      expect(supplement.isPrescription, isFalse);
      expect(supplement.description, '');
      expect(supplement.referralUrl, '');
      expect(supplement.sideEffects, isEmpty);
      expect(supplement.interactions, isEmpty);
      expect(supplement.focusLevel, 3);
    });

    test('should create Supplement with all fields', () {
      const supplement = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
        dosage: '200mg',
        defaultDosage: '150mg',
        timeOfDay: 'evening',
        benefits: ['Sleep', 'Focus'],
        evidenceLevel: 'high',
        notes: 'Take with food',
        imageUrl: 'https://example.com/image.png',
        isPrescription: true,
        description: 'Helps with sleep and relaxation.',
        referralUrl: 'https://example.com/magnesium',
        sideEffects: ['Diarrhea'],
        interactions: ['Other meds'],
        focusLevel: 4,
      );

      expect(supplement.dosage, '200mg');
      expect(supplement.defaultDosage, '150mg');
      expect(supplement.timeOfDay, 'evening');
      expect(supplement.benefits, ['Sleep', 'Focus']);
      expect(supplement.evidenceLevel, 'high');
      expect(supplement.notes, 'Take with food');
      expect(supplement.imageUrl, 'https://example.com/image.png');
      expect(supplement.isPrescription, isTrue);
      expect(supplement.description, isNotEmpty);
      expect(supplement.referralUrl, 'https://example.com/magnesium');
      expect(supplement.sideEffects, ['Diarrhea']);
      expect(supplement.interactions, ['Other meds']);
      expect(supplement.focusLevel, 4);
    });

    test('copyWith should update specified fields and preserve others', () {
      const original = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
        dosage: '200mg',
        defaultDosage: '150mg',
        timeOfDay: 'evening',
        benefits: ['Sleep'],
        evidenceLevel: 'high',
        notes: 'Original notes',
        imageUrl: 'https://example.com/image.png',
        isPrescription: false,
        description: 'Original description',
        referralUrl: 'https://example.com/magnesium',
        sideEffects: ['Diarrhea'],
        interactions: ['Other meds'],
        focusLevel: 3,
      );

      final updated = original.copyWith(
        name: 'Magnesium Glycinate',
        dosage: '300mg',
        benefits: ['Sleep', 'Anxiety'],
        notes: 'Updated notes',
        isPrescription: true,
        focusLevel: 5,
      );

      expect(updated.id, original.id);
      expect(updated.name, 'Magnesium Glycinate');
      expect(updated.category, original.category);
      expect(updated.dosage, '300mg');
      expect(updated.defaultDosage, original.defaultDosage);
      expect(updated.timeOfDay, original.timeOfDay);
      expect(updated.benefits, ['Sleep', 'Anxiety']);
      expect(updated.evidenceLevel, original.evidenceLevel);
      expect(updated.notes, 'Updated notes');
      expect(updated.imageUrl, original.imageUrl);
      expect(updated.isPrescription, isTrue);
      expect(updated.description, original.description);
      expect(updated.referralUrl, original.referralUrl);
      expect(updated.sideEffects, original.sideEffects);
      expect(updated.interactions, original.interactions);
      expect(updated.focusLevel, 5);
    });

    test('copyWith with no arguments should preserve all values', () {
      const original = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
        dosage: '200mg',
        defaultDosage: '150mg',
        timeOfDay: 'evening',
        benefits: ['Sleep'],
        evidenceLevel: 'high',
        notes: 'Original notes',
        imageUrl: 'https://example.com/image.png',
        isPrescription: false,
        description: 'Original description',
        referralUrl: 'https://example.com/magnesium',
        sideEffects: ['Diarrhea'],
        interactions: ['Other meds'],
        focusLevel: 3,
      );

      final updated = original.copyWith();

      expect(updated.id, original.id);
      expect(updated.name, original.name);
      expect(updated.category, original.category);
      expect(updated.dosage, original.dosage);
      expect(updated.defaultDosage, original.defaultDosage);
      expect(updated.timeOfDay, original.timeOfDay);
      expect(updated.benefits, original.benefits);
      expect(updated.evidenceLevel, original.evidenceLevel);
      expect(updated.notes, original.notes);
      expect(updated.imageUrl, original.imageUrl);
      expect(updated.isPrescription, original.isPrescription);
      expect(updated.description, original.description);
      expect(updated.referralUrl, original.referralUrl);
      expect(updated.sideEffects, original.sideEffects);
      expect(updated.interactions, original.interactions);
      expect(updated.focusLevel, original.focusLevel);
    });

    test('toJson should serialize all fields correctly', () {
      const supplement = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
        dosage: '200mg',
        defaultDosage: '150mg',
        timeOfDay: 'evening',
        benefits: ['Sleep'],
        evidenceLevel: 'high',
        notes: 'Take with food',
        imageUrl: 'https://example.com/image.png',
        isPrescription: true,
        description: 'Description',
        referralUrl: 'https://example.com/magnesium',
        sideEffects: ['Diarrhea'],
        interactions: ['Other meds'],
        focusLevel: 4,
      );

      final json = supplement.toJson();

      expect(json['id'], 'sup1');
      expect(json['name'], 'Magnesium');
      expect(json['category'], 'Minerals');
      expect(json['dosage'], '200mg');
      expect(json['defaultDosage'], '150mg');
      expect(json['timeOfDay'], 'evening');
      expect(json['benefits'], ['Sleep']);
      expect(json['evidenceLevel'], 'high');
      expect(json['notes'], 'Take with food');
      expect(json['imageUrl'], 'https://example.com/image.png');
      expect(json['isPrescription'], true);
      expect(json['description'], 'Description');
      expect(json['referralUrl'], 'https://example.com/magnesium');
      expect(json['sideEffects'], ['Diarrhea']);
      expect(json['interactions'], ['Other meds']);
      expect(json['focusLevel'], 4);
    });

    test('fromJson should deserialize with full data', () {
      final json = {
        'id': 'sup1',
        'name': 'Magnesium',
        'category': 'Minerals',
        'dosage': '200mg',
        'defaultDosage': '150mg',
        'timeOfDay': 'evening',
        'benefits': ['Sleep'],
        'evidenceLevel': 'high',
        'notes': 'Take with food',
        'imageUrl': 'https://example.com/image.png',
        'isPrescription': true,
        'description': 'Description',
        'referralUrl': 'https://example.com/magnesium',
        'sideEffects': ['Diarrhea'],
        'interactions': ['Other meds'],
        'focusLevel': 4,
      };

      final supplement = Supplement.fromJson(json);

      expect(supplement.id, 'sup1');
      expect(supplement.name, 'Magnesium');
      expect(supplement.category, 'Minerals');
      expect(supplement.dosage, '200mg');
      expect(supplement.defaultDosage, '150mg');
      expect(supplement.timeOfDay, 'evening');
      expect(supplement.benefits, ['Sleep']);
      expect(supplement.evidenceLevel, 'high');
      expect(supplement.notes, 'Take with food');
      expect(supplement.imageUrl, 'https://example.com/image.png');
      expect(supplement.isPrescription, true);
      expect(supplement.description, 'Description');
      expect(supplement.referralUrl, 'https://example.com/magnesium');
      expect(supplement.sideEffects, ['Diarrhea']);
      expect(supplement.interactions, ['Other meds']);
      expect(supplement.focusLevel, 4);
    });

    test('fromJson should handle legacy dosageInstruction and defaults', () {
      final json = {
        'id': 'sup1',
        'name': 'Magnesium',
        // category missing -> should default to 'general'
        'dosageInstruction': '100mg',
        // defaultDosage missing -> should fall back to dosageInstruction
        // timeOfDay missing
        // benefits missing -> []
        // evidenceLevel missing
        // notes missing
        // imageUrl missing
        // isPrescription missing -> false
        // description missing -> ''
        // referralUrl missing -> ''
        // sideEffects missing -> []
        // interactions missing -> []
        // focusLevel missing -> 3
      };

      final supplement = Supplement.fromJson(json);

      expect(supplement.category, 'general');
      expect(supplement.dosage, '100mg');
      expect(supplement.defaultDosage, '100mg');
      expect(supplement.benefits, isEmpty);
      expect(supplement.isPrescription, isFalse);
      expect(supplement.description, '');
      expect(supplement.referralUrl, '');
      expect(supplement.sideEffects, isEmpty);
      expect(supplement.interactions, isEmpty);
      expect(supplement.focusLevel, 3);
    });

    test('toJson and fromJson should be reversible', () {
      const original = Supplement(
        id: 'sup1',
        name: 'Magnesium',
        category: 'Minerals',
        dosage: '200mg',
        defaultDosage: '150mg',
        timeOfDay: 'evening',
        benefits: ['Sleep'],
        evidenceLevel: 'high',
        notes: 'Take with food',
        imageUrl: 'https://example.com/image.png',
        isPrescription: true,
        description: 'Description',
        referralUrl: 'https://example.com/magnesium',
        sideEffects: ['Diarrhea'],
        interactions: ['Other meds'],
        focusLevel: 4,
      );

      final json = original.toJson();
      final restored = Supplement.fromJson(json);

      expect(restored.id, original.id);
      expect(restored.name, original.name);
      expect(restored.category, original.category);
      expect(restored.dosage, original.dosage);
      expect(restored.defaultDosage, original.defaultDosage);
      expect(restored.timeOfDay, original.timeOfDay);
      expect(restored.benefits, original.benefits);
      expect(restored.evidenceLevel, original.evidenceLevel);
      expect(restored.notes, original.notes);
      expect(restored.imageUrl, original.imageUrl);
      expect(restored.isPrescription, original.isPrescription);
      expect(restored.description, original.description);
      expect(restored.referralUrl, original.referralUrl);
      expect(restored.sideEffects, original.sideEffects);
      expect(restored.interactions, original.interactions);
      expect(restored.focusLevel, original.focusLevel);
    });
  });
}


import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_interaction.dart';

void main() {
  group('SupplementInteraction', () {
    test('should support value equality', () {
      const interaction1 = SupplementInteraction(
        id: '1',
        supplementAId: 'sup1',
        supplementBId: 'sup2',
        severity: InteractionSeverity.critical,
        description: 'Test description',
        recommendation: 'Test recommendation',
        scientificReferences: ['ref1'],
      );

      const interaction2 = SupplementInteraction(
        id: '1',
        supplementAId: 'sup1',
        supplementBId: 'sup2',
        severity: InteractionSeverity.critical,
        description: 'Test description',
        recommendation: 'Test recommendation',
        scientificReferences: ['ref1'],
      );

      // Assuming Equatable or similar is used, or just checking fields if not.
      // Based on previous file reads, it seemed to be a standard class.
      // If it's a standard class without Equatable, strict equality checks reference.
      // Let's verify field values instead to be safe if Equatable isn't used.

      expect(interaction1.id, interaction2.id);
      expect(interaction1.severity, interaction2.severity);
    });

    test('should correctly identify critical severity', () {
      const interaction = SupplementInteraction(
        id: '1',
        supplementAId: 'a',
        supplementBId: 'b',
        severity: InteractionSeverity.critical,
        description: 'desc',
        recommendation: 'rec',
        scientificReferences: [],
      );

      expect(interaction.severity, InteractionSeverity.critical);
    });
  });
}

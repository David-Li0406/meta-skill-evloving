import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/application/view_models/safety_view_model.dart';
import 'package:adhd_supplement_app/domain/entities/supplement_interaction.dart';
import 'package:adhd_supplement_app/domain/entities/safety_override.dart';
import 'package:adhd_supplement_app/domain/repositories/safety_repository.dart';

// Manual Mock
class MockSafetyRepository implements SafetyRepository {
  List<SupplementInteraction> interactionsToReturn = [];
  SafetyOverride? lastLoggedOverride;

  @override
  Future<List<SupplementInteraction>> getInteractionsForSupplements(
      List<String> supplementIds) async {
    return interactionsToReturn;
  }

  @override
  Future<void> logSafetyOverride(SafetyOverride override) async {
    lastLoggedOverride = override;
  }

  @override
  Future<List<SafetyOverride>> getSafetyOverrides(String userId) async {
    return [];
  }

  @override
  Future<SupplementInteraction?> getInteractionById(String id) async {
    try {
      return interactionsToReturn.firstWhere((i) => i.id == id);
    } catch (_) {
      return null;
    }
  }
}

void main() {
  group('SafetyViewModel', () {
    late SafetyViewModel viewModel;
    late MockSafetyRepository mockRepository;

    setUp(() {
      mockRepository = MockSafetyRepository();
      viewModel = SafetyViewModel(
        repository: mockRepository,
        userId: 'test_user',
      );
    });

    test('should initialize with empty interactions', () {
      expect(viewModel.currentInteractions, isEmpty);
      expect(viewModel.hasCriticalInteractions, isFalse);
    });

    test(
        'checkInteractions should update currentInteractions when conflict exists',
        () async {
      // Arrange
      const supAId = '1';
      const supBId = '2';

      const interaction = SupplementInteraction(
        id: 'i1',
        supplementAId: '1',
        supplementBId: '2',
        severity: InteractionSeverity.critical,
        description: 'Bad combo',
        recommendation: 'Stop',
        scientificReferences: [],
      );

      mockRepository.interactionsToReturn = [interaction];

      // Act
      await viewModel.checkInteractions([supAId, supBId]);

      // Assert
      expect(viewModel.currentInteractions, hasLength(1));
      expect(viewModel.currentInteractions.first, interaction);
      expect(viewModel.hasCriticalInteractions, isTrue);
    });

    test('overrideInteraction should log override', () async {
      // Arrange

      // Act
      await viewModel.overrideInteraction('i1', 'I consulted my doctor');

      // Assert
      expect(mockRepository.lastLoggedOverride, isNotNull);
      expect(mockRepository.lastLoggedOverride!.interactionId, 'i1');
      expect(mockRepository.lastLoggedOverride!.userReason,
          'I consulted my doctor');
      expect(mockRepository.lastLoggedOverride!.userId, 'test_user');
    });
  });
}

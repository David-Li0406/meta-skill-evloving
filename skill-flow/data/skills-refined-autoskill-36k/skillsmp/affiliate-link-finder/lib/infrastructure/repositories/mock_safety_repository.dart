import '../../domain/repositories/safety_repository.dart';
import '../../domain/entities/supplement_interaction.dart';
import '../../domain/entities/safety_override.dart';

class MockSafetyRepository implements SafetyRepository {
  @override
  Future<List<SupplementInteraction>> getInteractionsForSupplements(
      List<String> supplementIds) async {
    // Return a dummy interaction if caffeine and melatonin are present together for testing
    // Or just empty list by default
    if (supplementIds.length > 1) {
      // Mock logic: randomly return an interaction or return empty
      return [];
    }
    return [];
  }

  @override
  Future<void> logSafetyOverride(SafetyOverride override) async {
    await Future<void>.delayed(const Duration(milliseconds: 500));
  }

  @override
  Future<List<SafetyOverride>> getSafetyOverrides(String userId) async {
    return [];
  }

  @override
  Future<SupplementInteraction?> getInteractionById(String id) async {
    return null;
  }
}

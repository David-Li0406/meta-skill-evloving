import '../entities/supplement_interaction.dart';
import '../entities/safety_override.dart';

abstract class SafetyRepository {
  /// Get all known interactions between a list of supplements
  Future<List<SupplementInteraction>> getInteractionsForSupplements(
      List<String> supplementIds);

  /// Log a user's decision to override a safety warning
  Future<void> logSafetyOverride(SafetyOverride override);

  /// Get all safety overrides for a specific user
  Future<List<SafetyOverride>> getSafetyOverrides(String userId);

  /// Get a specific interaction by ID
  Future<SupplementInteraction?> getInteractionById(String id);
}

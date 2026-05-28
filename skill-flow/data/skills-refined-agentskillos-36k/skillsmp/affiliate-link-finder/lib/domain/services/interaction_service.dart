import '../entities/supplement.dart';
import '../entities/medication.dart';

abstract class InteractionService {
  /// Check if a supplement interacts with any of the user's medications.
  /// Returns a list of [InteractionWarning]s.
  Future<List<InteractionWarning>> checkInteractions({
    required Supplement supplement,
    required List<Medication> userMedications,
  });

  /// Check if a set of supplements (a Stack) has internal interactions.
  Future<List<InteractionWarning>> checkStackInteractions({
    required List<Supplement> supplements,
    required List<Medication> userMedications,
  });
}

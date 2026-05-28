import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/entities/medication.dart';
import 'package:adhd_supplement_app/domain/services/interaction_service.dart';
import 'package:adhd_supplement_app/domain/services/safety_guard.dart';
import 'package:adhd_supplement_app/domain/services/adhd_interaction_guard.dart';

class FDAInteractionService implements InteractionService {
  @override
  Future<List<InteractionWarning>> checkInteractions({
    required Supplement supplement,
    required List<Medication> userMedications,
  }) async {
    // Initial implementation uses the local SafetyGuard logic
    final guard = SafetyGuard(userMedications);
    final warnings = guard.checkSupplement(supplement);

    // Additionally check against ADHDInteractionGuard rules
    for (final med in userMedications) {
      final interaction =
          ADHDInteractionGuard.checkInteraction(med.name, supplement.name);
      if (interaction['risk'] != 'Low') {
        // Map simplified check to InteractionWarning
        final exists = warnings.any((w) =>
            w.medicationName == med.name &&
            w.supplementName == supplement.name);
        if (!exists) {
          warnings.add(InteractionWarning(
            supplementName: supplement.name,
            medicationName: med.name,
            severity: _mapRiskToSeverity(interaction['risk'] as String),
            title:
                (interaction['warning'] as String?) ?? 'Interaction Detected',
            description: interaction['message'] as String,
            recommendation: interaction['recommendation'] as String,
          ));
        }
      }
    }

    // TODO: Implement actual FDA API call for real-time cross-reference in future update
    return warnings;
  }

  @override
  Future<List<InteractionWarning>> checkStackInteractions({
    required List<Supplement> supplements,
    required List<Medication> userMedications,
  }) async {
    final allWarnings = <InteractionWarning>[];
    for (final supplement in supplements) {
      final warnings = await checkInteractions(
        supplement: supplement,
        userMedications: userMedications,
      );
      allWarnings.addAll(warnings);
    }
    return allWarnings;
  }

  WarningSeverity _mapRiskToSeverity(String risk) {
    switch (risk.toLowerCase()) {
      case 'high':
      case 'danger':
        return WarningSeverity.danger;
      case 'moderate':
      case 'warning':
        return WarningSeverity.warning;
      case 'caution':
        return WarningSeverity.caution;
      default:
        return WarningSeverity.info;
    }
  }
}

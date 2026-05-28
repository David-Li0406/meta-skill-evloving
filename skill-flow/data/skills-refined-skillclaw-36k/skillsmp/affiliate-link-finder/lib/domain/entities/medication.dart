/// Medication Entity
///
/// Represents an ADHD or related medication taken by the user.
/// Includes logic for categorizing medications for interaction checks.
library;

class Medication {
  final String id;
  final String name;
  final MedicationType type;
  final double dosageMg;

  const Medication({
    required this.id,
    required this.name,
    required this.type,
    required this.dosageMg,
  });

  /// Helper to create from string name (useful for onboarding/profile data)
  factory Medication.fromName(String name, {double dosage = 0.0}) {
    final lower = name.toLowerCase();
    MedicationType type = MedicationType.other;

    if (lower.contains('adderall') ||
        lower.contains('vyvanse') ||
        lower.contains('ritalin') ||
        lower.contains('concerta') ||
        lower.contains('dexedrine') ||
        lower.contains('stimulant')) {
      type = MedicationType.stimulant;
    } else if (lower.contains('strattera') ||
        lower.contains('qelbree') ||
        lower.contains('intuniv')) {
      type = MedicationType.nonStimulant;
    } else if (lower.contains('prozac') ||
        lower.contains('zoloft') ||
        lower.contains('lexapro') ||
        lower.contains('antidepressant')) {
      type = MedicationType.antidepressant;
    }

    return Medication(
      id: name.replaceAll(' ', '_').toLowerCase(),
      name: name,
      type: type,
      dosageMg: dosage,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'type': type.name,
      'dosageMg': dosageMg,
    };
  }

  factory Medication.fromJson(Map<String, dynamic> json) {
    return Medication(
      id: json['id'] as String,
      name: json['name'] as String,
      type: MedicationType.values.byName(json['type'] as String),
      dosageMg: (json['dosageMg'] as num).toDouble(),
    );
  }
}

enum MedicationType {
  stimulant, // Adderall, Ritalin, Vyvanse, etc.
  nonStimulant, // Strattera, Wellbutrin, etc.
  antidepressant, // SSRIs, SNRIs
  other,
}

/// Severity level for interaction warnings
enum WarningSeverity {
  info, // Educational, no action needed
  caution, // Consider timing separation
  warning, // Consult doctor recommended
  danger, // Do not combine without medical supervision
}

/// Represents an interaction warning
class InteractionWarning {
  final String supplementName;
  final String medicationName;
  final WarningSeverity severity;
  final String title;
  final String description;
  final String recommendation;

  const InteractionWarning({
    required this.supplementName,
    required this.medicationName,
    required this.severity,
    required this.title,
    required this.description,
    required this.recommendation,
  });
}

/// Safety Guard - Medication Interaction Checker
///
/// Cross-references user's ADHD medications with supplements to detect
/// potentially harmful interactions and display appropriate warnings.
library;

import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/entities/medication.dart';

/// Safety Guard class for checking supplement-medication interactions
class SafetyGuard {
  final List<Medication> _userMedications;

  SafetyGuard(this._userMedications);

  /// Known interaction rules database
  /// In production, this should be fetched from a medical API or database
  static final List<_InteractionRule> _interactionRules = [
    // CRITICAL: VITAMIN C + AMPHETAMINE-BASED STIMULANTS
    // This is the most important interaction for ADHD users
    const _InteractionRule(
      supplementPattern: 'vitamin c',
      medicationType: MedicationType.stimulant,
      checkHighDose: true,
      highDoseThresholdMg: 500.0,
      severity: WarningSeverity.warning,
      title: 'Interaction Detected',
      description: 'Vitamin C can reduce the effectiveness of your stimulant '
          'medication by increasing acidity in the GI tract and urine. This causes '
          'amphetamines (Adderall, Vyvanse, Dexedrine, etc.) to be flushed out of '
          'your system faster, significantly lowering blood levels.',
      recommendation: 'Wait at least 1-2 hours before or after taking your '
          'medication to take this supplement. Avoid taking Vitamin C within your '
          'medication\'s peak effectiveness window.',
    ),

    // ASCORBIC ACID (pure form)
    const _InteractionRule(
      supplementPattern: 'ascorbic acid',
      medicationType: MedicationType.stimulant,
      severity: WarningSeverity.warning,
      title: 'Interaction Detected',
      description:
          'Ascorbic Acid (Vitamin C) increases GI and urinary acidity, '
          'which accelerates the excretion of amphetamine-based stimulants.',
      recommendation: 'Wait at least 1-2 hours before or after taking your '
          'medication to take this supplement.',
    ),

    // CITRUS-BASED SUPPLEMENTS
    const _InteractionRule(
      supplementPattern: 'citrus',
      medicationType: MedicationType.stimulant,
      severity: WarningSeverity.caution,
      title: 'Timing Consideration',
      description: 'Citrus supplements often contain high amounts of Vitamin C '
          'and citric acid, which can affect stimulant medication absorption.',
      recommendation: 'Take at least 1 hour apart from stimulant medications.',
    ),

    // L-TYROSINE + STIMULANTS
    const _InteractionRule(
      supplementPattern: 'tyrosine',
      medicationType: MedicationType.stimulant,
      severity: WarningSeverity.caution,
      title: 'Timing Consideration',
      description: 'L-Tyrosine is a dopamine precursor. Taking it with '
          'stimulants may cause overstimulation in some individuals.',
      recommendation: 'Start with low doses and monitor for increased '
          'anxiety or jitteriness. Consider taking on medication holidays.',
    ),

    // 5-HTP + ANTIDEPRESSANTS
    const _InteractionRule(
      supplementPattern: '5-htp',
      medicationType: MedicationType.antidepressant,
      severity: WarningSeverity.danger,
      title: 'Dangerous Interaction',
      description: '5-HTP combined with SSRIs or SNRIs can cause '
          'serotonin syndrome, a potentially life-threatening condition.',
      recommendation: 'Do NOT take 5-HTP with antidepressants without '
          'explicit doctor approval and monitoring.',
    ),

    // ST. JOHN'S WORT + MULTIPLE
    const _InteractionRule(
      supplementPattern: "john's wort",
      medicationType: MedicationType.stimulant,
      severity: WarningSeverity.warning,
      title: 'Warning: Consult Doctor',
      description: "St. John's Wort can affect the metabolism of many "
          'medications, potentially making them less effective.',
      recommendation: 'Consult your doctor before combining with any '
          'prescription ADHD medication.',
    ),

    // GINKGO + STIMULANTS
    const _InteractionRule(
      supplementPattern: 'ginkgo',
      medicationType: MedicationType.stimulant,
      severity: WarningSeverity.caution,
      title: 'Blood Pressure Consideration',
      description: 'Ginkgo may affect blood pressure and circulation, '
          'which could interact with stimulant effects.',
      recommendation: 'Monitor blood pressure if combining. Consult doctor '
          'if you have cardiovascular concerns.',
    ),
  ];

  /// Check a supplement against user's medications for interactions
  ///
  /// Returns a list of warnings (empty if no interactions found)
  List<InteractionWarning> checkSupplement(Supplement supplement) {
    final warnings = <InteractionWarning>[];
    final supplementName = supplement.name.toLowerCase();

    // 1. Check dynamic rules from _interactionRules
    for (final medication in _userMedications) {
      for (final rule in _interactionRules) {
        if (_matchesRule(supplementName, medication, rule)) {
          warnings.add(InteractionWarning(
            supplementName: supplement.name,
            medicationName: medication.name,
            severity: rule.severity,
            title: rule.title,
            description: rule.description,
            recommendation: rule.recommendation,
          ));
        }
      }
    }

    // 2. Check supplement's structured data (adhdMedInteractions)
    if (supplement.adhdMedInteractions != null) {
      for (final medication in _userMedications) {
        final medNameLower = medication.name.toLowerCase();
        for (final entry in supplement.adhdMedInteractions!.entries) {
          if (medNameLower.contains(entry.key.toLowerCase())) {
            // Check if already exist to avoid duplicate
            final exists = warnings.any((w) =>
                w.medicationName.toLowerCase() == medNameLower &&
                w.description == entry.value);

            if (!exists) {
              warnings.add(InteractionWarning(
                supplementName: supplement.name,
                medicationName: medication.name,
                severity: WarningSeverity.warning,
                title: 'Clinical Interaction Alert',
                description: entry.value,
                recommendation: 'Consult your doctor before combining.',
              ));
            }
          }
        }
      }
    }

    return warnings;
  }

  /// Check if supplement name and medication match an interaction rule
  bool _matchesRule(
    String supplementName,
    Medication medication,
    _InteractionRule rule,
  ) {
    // Check if supplement name matches the pattern
    if (!supplementName.contains(rule.supplementPattern)) {
      return false;
    }

    // Check if medication type matches
    if (medication.type != rule.medicationType) {
      return false;
    }

    // If high dose check is required, we'd need supplement dosage info
    // For now, we flag it regardless (conservative approach)

    return true;
  }

  /// Check if user is on any stimulant medications
  bool get isOnStimulants =>
      _userMedications.any((m) => m.type == MedicationType.stimulant);

  /// Check if user is on any antidepressants
  bool get isOnAntidepressants =>
      _userMedications.any((m) => m.type == MedicationType.antidepressant);

  /// Get the highest severity warning from a list
  static WarningSeverity? getHighestSeverity(
      List<InteractionWarning> warnings) {
    if (warnings.isEmpty) return null;

    const severityOrder = [
      WarningSeverity.info,
      WarningSeverity.caution,
      WarningSeverity.warning,
      WarningSeverity.danger,
    ];

    return warnings.map((w) => w.severity).reduce(
        (a, b) => severityOrder.indexOf(a) > severityOrder.indexOf(b) ? a : b);
  }
}

/// Internal rule definition
class _InteractionRule {
  final String supplementPattern;
  final MedicationType medicationType;
  final bool checkHighDose;
  final double? highDoseThresholdMg;
  final WarningSeverity severity;
  final String title;
  final String description;
  final String recommendation;

  const _InteractionRule({
    required this.supplementPattern,
    required this.medicationType,
    this.checkHighDose = false,
    this.highDoseThresholdMg,
    required this.severity,
    required this.title,
    required this.description,
    required this.recommendation,
  });
}

/// ADHD Interaction Guard - Simplified Quick-Check System
/// 
/// This is a supplementary class that provides quick validation
/// using the lists defined in the user's specification.
/// Works alongside the main SafetyGuard for comprehensive checking.
library;

class ADHDInteractionGuard {
  // List of amphetamine-based stimulant medications affected by GI/Urinary acidity
  static const List<String> stimulantMeds = [
    'Adderall',
    'Vyvanse', 
    'Mydayis',
    'Dexedrine',
    'Evekeo',
    'Adzenys',
    'Dyanavel',
    // Generic names
    'Amphetamine',
    'Dextroamphetamine',
    'Lisdexamfetamine',
    'Mixed Amphetamine Salts',
  ];

  // List of supplements that are highly acidic/contain high Vitamin C
  // These can lower blood levels of amphetamines by increasing excretion
  static const List<String> acidicSupplements = [
    'Vitamin C',
    'Ascorbic Acid',
    'Multivitamin (with Vit C)',
    'Multivitamin',  // Most contain Vitamin C
    'Orange Extract',
    'Citrus Bioflavonoids',
    'Lemon Extract',
    'Acerola Cherry',
    'Rose Hips',
    'Camu Camu',
  ];

  /// Quick check for stimulant-acidic supplement interaction
  /// Returns a detailed status map
  static Map<String, dynamic> checkInteraction(String med, String supplement) {
    final medLower = med.toLowerCase();
    final suppLower = supplement.toLowerCase();
    
    bool isStimulant = stimulantMeds.any(
      (stimMed) => medLower.contains(stimMed.toLowerCase())
    );
    
    bool isAcidic = acidicSupplements.any(
      (acidSup) => suppLower.contains(acidSup.toLowerCase())
    );

    if (isStimulant && isAcidic) {
      return {
        'risk': 'Moderate',
        'warning': 'Interaction Detected',
        'message': 'Vitamin C can reduce the effectiveness of your stimulant '
            'medication by flushing it out of your system faster. This happens '
            'because acidic substances increase the acidity of your GI tract and '
            'urine, causing amphetamines to be excreted more rapidly.',
        'recommendation': 'Wait at least 1-2 hours before or after taking your '
            'medication to take this supplement. Best practice: take Vitamin C '
            'in the evening if your stimulant is taken in the morning.',
        'mechanism': 'Increased GI/urinary acidity → Faster amphetamine excretion',
      };
    }

    return {
      'risk': 'Low',
      'warning': null,
      'message': 'No known timing interaction found.',
      'recommendation': 'Take as directed.',
      'mechanism': null,
    };
  }

  /// Check if a medication is an amphetamine-based stimulant
  static bool isAmphetamineStimulant(String medication) {
    final medLower = medication.toLowerCase();
    return stimulantMeds.any(
      (stimMed) => medLower.contains(stimMed.toLowerCase())
    );
  }

  /// Check if a supplement contains acidic compounds
  static bool isAcidicSupplement(String supplement) {
    final suppLower = supplement.toLowerCase();
    return acidicSupplements.any(
      (acidSup) => suppLower.contains(acidSup.toLowerCase())
    );
  }

  /// Get all possible interactions for a given supplement
  /// Returns a list of medication names that may interact
  static List<String> getPotentialInteractionsFor(String supplement) {
    if (isAcidicSupplement(supplement)) {
      return List.from(stimulantMeds);
    }
    return [];
  }
}

enum InteractionSeverity {
  critical, // Major risk, should not be combined
  caution, // Moderate risk, monitor closely or consult doctor
  stable // Known interaction but usually safe with monitoring
}

class SupplementInteraction {
  final String id;
  final String supplementAId;
  final String supplementBId;
  final InteractionSeverity severity;
  final String description;
  final String recommendation;
  final List<String> scientificReferences;

  const SupplementInteraction({
    required this.id,
    required this.supplementAId,
    required this.supplementBId,
    required this.severity,
    required this.description,
    required this.recommendation,
    this.scientificReferences = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'supplementAId': supplementAId,
      'supplementBId': supplementBId,
      'severity': severity.name,
      'description': description,
      'recommendation': recommendation,
      'scientificReferences': scientificReferences,
    };
  }

  factory SupplementInteraction.fromJson(Map<String, dynamic> json) {
    return SupplementInteraction(
      id: json['id'] as String,
      supplementAId: json['supplementAId'] as String,
      supplementBId: json['supplementBId'] as String,
      severity: InteractionSeverity.values.byName(json['severity'] as String),
      description: json['description'] as String,
      recommendation: json['recommendation'] as String,
      scientificReferences: (json['scientificReferences'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
    );
  }
}

class SafetyOverride {
  final String id;
  final String userId;
  final String interactionId;
  final DateTime timestamp;
  final String? userReason;
  final bool
      isAcknowledged; // Whether user explicitly checked "I understand the risks"

  const SafetyOverride({
    required this.id,
    required this.userId,
    required this.interactionId,
    required this.timestamp,
    this.userReason,
    this.isAcknowledged = false,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'interactionId': interactionId,
      'timestamp': timestamp.toIso8601String(),
      'userReason': userReason,
      'isAcknowledged': isAcknowledged,
    };
  }

  factory SafetyOverride.fromJson(Map<String, dynamic> json) {
    return SafetyOverride(
      id: json['id'] as String,
      userId: json['userId'] as String,
      interactionId: json['interactionId'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      userReason: json['userReason'] as String?,
      isAcknowledged: json['isAcknowledged'] as bool? ?? false,
    );
  }
}

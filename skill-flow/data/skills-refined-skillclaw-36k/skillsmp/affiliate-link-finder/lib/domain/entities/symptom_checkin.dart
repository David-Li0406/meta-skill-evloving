class SymptomCheckIn {
  final String id;
  final String userId;
  final DateTime timestamp;
  final int focusLevel; // 0-100
  final int energyLevel; // 0-100
  final int moodLevel; // 0-100
  final String? notes;

  const SymptomCheckIn({
    required this.id,
    required this.userId,
    required this.timestamp,
    required this.focusLevel,
    required this.energyLevel,
    required this.moodLevel,
    this.notes,
  });

  SymptomCheckIn copyWith({
    String? id,
    String? userId,
    DateTime? timestamp,
    int? focusLevel,
    int? energyLevel,
    int? moodLevel,
    String? notes,
  }) {
    return SymptomCheckIn(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      timestamp: timestamp ?? this.timestamp,
      focusLevel: focusLevel ?? this.focusLevel,
      energyLevel: energyLevel ?? this.energyLevel,
      moodLevel: moodLevel ?? this.moodLevel,
      notes: notes ?? this.notes,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'timestamp': timestamp.toIso8601String(),
      'focusLevel': focusLevel,
      'energyLevel': energyLevel,
      'moodLevel': moodLevel,
      'notes': notes,
    };
  }

  factory SymptomCheckIn.fromJson(Map<String, dynamic> json) {
    return SymptomCheckIn(
      id: json['id'] as String,
      userId: json['userId'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
      focusLevel: json['focusLevel'] as int,
      energyLevel: json['energyLevel'] as int,
      moodLevel: json['moodLevel'] as int,
      notes: json['notes'] as String?,
    );
  }

  // Helper methods for UI display
  String get focusEmoji {
    if (focusLevel >= 80) return '🤩';
    if (focusLevel >= 60) return '😊';
    if (focusLevel >= 40) return '😐';
    if (focusLevel >= 20) return '😔';
    return '😫';
  }

  String get energyEmoji {
    if (energyLevel >= 80) return '⚡️';
    if (energyLevel >= 60) return '😊';
    if (energyLevel >= 40) return '😐';
    if (energyLevel >= 20) return '😔';
    return '🥱';
  }

  String get moodEmoji {
    if (moodLevel >= 80) return '😊';
    if (moodLevel >= 60) return '🙂';
    if (moodLevel >= 40) return '😐';
    if (moodLevel >= 20) return '😔';
    return '😔';
  }

  // Calculate average wellness score
  double get averageScore => (focusLevel + energyLevel + moodLevel) / 3;
}

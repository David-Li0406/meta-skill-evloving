enum LogStatus { taken, skipped, late }

class DailyLog {
  final String id;
  final String userId;
  final DateTime date;
  final List<LogEntry> entries;
  final Map<String, int>? symptomRatings; // symptom name -> rating (1-5)
  final int? moodScore; // From Backend Spec v1.0
  final int? focusScore; // From Backend Spec v1.0
  final String? notes;
  final DateTime createdAt;

  const DailyLog({
    required this.id,
    required this.userId,
    required this.date,
    required this.entries,
    this.symptomRatings,
    this.moodScore,
    this.focusScore,
    this.notes,
    required this.createdAt,
  });

  DailyLog copyWith({
    String? id,
    String? userId,
    DateTime? date,
    List<LogEntry>? entries,
    Map<String, int>? symptomRatings,
    int? moodScore,
    int? focusScore,
    String? notes,
    DateTime? createdAt,
  }) {
    return DailyLog(
      id: id ?? this.id,
      userId: userId ?? this.userId,
      date: date ?? this.date,
      entries: entries ?? this.entries,
      symptomRatings: symptomRatings ?? this.symptomRatings,
      moodScore: moodScore ?? this.moodScore,
      focusScore: focusScore ?? this.focusScore,
      notes: notes ?? this.notes,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'userId': userId,
      'date': date.toIso8601String(),
      'entries': entries.map((e) => e.toJson()).toList(),
      'symptomRatings': symptomRatings,
      'moodScore': moodScore,
      'focusScore': focusScore,
      'notes': notes,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  factory DailyLog.fromJson(Map<String, dynamic> json) {
    return DailyLog(
      id: json['id'] as String,
      userId: json['userId'] as String,
      date: DateTime.parse(json['date'] as String),
      entries: (json['entries'] as List<dynamic>)
          .map((e) => LogEntry.fromJson(e as Map<String, dynamic>))
          .toList(),
      symptomRatings: (json['symptomRatings'] as Map<String, dynamic>?)?.map(
        (key, value) => MapEntry(key, value as int),
      ),
      moodScore: json['moodScore'] as int? ?? json['mood_score'] as int?,
      focusScore: json['focusScore'] as int? ?? json['focus_score'] as int?,
      notes: json['notes'] as String?,
      createdAt: DateTime.parse(json['createdAt'] as String),
    );
  }
}

class LogEntry {
  final String supplementId;
  final DateTime takenAt;
  final LogStatus status;
  final String? skippedReason;
  final int? confidenceScore; // 1-5: 1=think, 5=certain

  // Backward compatibility
  bool get taken => status == LogStatus.taken;

  const LogEntry({
    required this.supplementId,
    required this.takenAt,
    required this.status,
    this.skippedReason,
    this.confidenceScore,
  });

  static const Object _unset = Object();

  LogEntry copyWith({
    String? supplementId,
    DateTime? takenAt,
    LogStatus? status,
    Object? skippedReason = _unset,
    int? confidenceScore,
  }) {
    return LogEntry(
      supplementId: supplementId ?? this.supplementId,
      takenAt: takenAt ?? this.takenAt,
      status: status ?? this.status,
      skippedReason: identical(skippedReason, _unset)
          ? this.skippedReason
          : skippedReason as String?,
      confidenceScore: confidenceScore ?? this.confidenceScore,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'supplementId': supplementId,
      'takenAt': takenAt.toIso8601String(),
      'status': status.name,
      'skippedReason': skippedReason,
      'confidenceScore': confidenceScore,
    };
  }

  factory LogEntry.fromJson(Map<String, dynamic> json) {
    final statusStr = json['status'] as String?;
    final takenBool = json['taken'] as bool?;

    return LogEntry(
      supplementId: json['supplementId'] as String,
      takenAt: DateTime.parse(json['takenAt'] as String),
      status: LogStatus.values.firstWhere(
        (e) =>
            e.name == (statusStr ?? (takenBool == true ? 'taken' : 'skipped')),
        orElse: () => LogStatus.skipped,
      ),
      skippedReason: json['skippedReason'] as String?,
      confidenceScore: json['confidenceScore'] as int?,
    );
  }
}

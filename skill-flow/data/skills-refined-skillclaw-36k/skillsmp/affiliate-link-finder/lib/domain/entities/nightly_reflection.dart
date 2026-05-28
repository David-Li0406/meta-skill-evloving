class NightlyReflection {
  final String id;
  final DateTime date;
  final double focusRating;
  final String journalEntry;
  final bool isSleepReady;

  NightlyReflection({
    required this.id,
    required this.date,
    required this.focusRating,
    required this.journalEntry,
    required this.isSleepReady,
  });

  NightlyReflection copyWith({
    String? id,
    DateTime? date,
    double? focusRating,
    String? journalEntry,
    bool? isSleepReady,
  }) {
    return NightlyReflection(
      id: id ?? this.id,
      date: date ?? this.date,
      focusRating: focusRating ?? this.focusRating,
      journalEntry: journalEntry ?? this.journalEntry,
      isSleepReady: isSleepReady ?? this.isSleepReady,
    );
  }
}

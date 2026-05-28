class Streak {
  final String userId;
  final int currentStreak;
  final int longestStreak;
  final DateTime? lastCompletedDate;
  final int graceDaysRemaining;
  final int graceDaysUsed;
  final DateTime updatedAt;

  const Streak({
    required this.userId,
    required this.currentStreak,
    required this.longestStreak,
    this.lastCompletedDate,
    required this.graceDaysRemaining,
    required this.graceDaysUsed,
    required this.updatedAt,
  });

  static const Object _unset = Object();

  /// Note: [lastCompletedDate] supports explicitly setting null by passing
  /// `lastCompletedDate: null`.
  Streak copyWith({
    String? userId,
    int? currentStreak,
    int? longestStreak,
    Object? lastCompletedDate = _unset,
    int? graceDaysRemaining,
    int? graceDaysUsed,
    DateTime? updatedAt,
  }) {
    return Streak(
      userId: userId ?? this.userId,
      currentStreak: currentStreak ?? this.currentStreak,
      longestStreak: longestStreak ?? this.longestStreak,
      lastCompletedDate: identical(lastCompletedDate, _unset)
          ? this.lastCompletedDate
          : lastCompletedDate as DateTime?,
      graceDaysRemaining: graceDaysRemaining ?? this.graceDaysRemaining,
      graceDaysUsed: graceDaysUsed ?? this.graceDaysUsed,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'userId': userId,
      'currentStreak': currentStreak,
      'longestStreak': longestStreak,
      'lastCompletedDate': lastCompletedDate?.toIso8601String(),
      'graceDaysRemaining': graceDaysRemaining,
      'graceDaysUsed': graceDaysUsed,
      'updatedAt': updatedAt.toIso8601String(),
    };
  }

  factory Streak.fromJson(Map<String, dynamic> json) {
    return Streak(
      userId: json['userId'] as String,
      currentStreak: json['currentStreak'] as int,
      longestStreak: json['longestStreak'] as int,
      lastCompletedDate: json['lastCompletedDate'] != null
          ? DateTime.parse(json['lastCompletedDate'] as String)
          : null,
      graceDaysRemaining: json['graceDaysRemaining'] as int,
      graceDaysUsed: json['graceDaysUsed'] as int,
      updatedAt: DateTime.parse(json['updatedAt'] as String),
    );
  }

  /// Creates a new streak for a user
  factory Streak.initial(String userId) {
    return Streak(
      userId: userId,
      currentStreak: 0,
      longestStreak: 0,
      lastCompletedDate: null,
      graceDaysRemaining: 2, // Default 2 grace days per month
      graceDaysUsed: 0,
      updatedAt: DateTime.now(),
    );
  }
}

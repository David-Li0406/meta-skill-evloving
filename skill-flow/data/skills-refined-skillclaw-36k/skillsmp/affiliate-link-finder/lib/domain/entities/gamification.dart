import 'package:flutter/material.dart';

enum BadgeTier { bronze, silver, gold }

class GamificationBadge {
  final String id;
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final bool isEarned;
  final DateTime? earnedDate;
  final bool isLocked;
  final BadgeTier tier;
  final double progress; // 0.0 to 1.0
  final int targetValue; // Actual count needed to unlock
  final int currentValue; // User's current count
  final int xpReward;

  const GamificationBadge({
    required this.id,
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    this.isEarned = false,
    this.earnedDate,
    this.isLocked = true,
    this.tier = BadgeTier.bronze,
    this.progress = 0.0,
    this.targetValue = 1,
    this.currentValue = 0,
    this.xpReward = 100,
  });

  GamificationBadge copyWith({
    String? id,
    String? title,
    String? subtitle,
    IconData? icon,
    Color? color,
    bool? isEarned,
    DateTime? earnedDate,
    bool? isLocked,
    BadgeTier? tier,
    double? progress,
    int? targetValue,
    int? currentValue,
    int? xpReward,
  }) {
    return GamificationBadge(
      id: id ?? this.id,
      title: title ?? this.title,
      subtitle: subtitle ?? this.subtitle,
      icon: icon ?? this.icon,
      color: color ?? this.color,
      isEarned: isEarned ?? this.isEarned,
      earnedDate: earnedDate ?? this.earnedDate,
      isLocked: isLocked ?? this.isLocked,
      tier: tier ?? this.tier,
      progress: progress ?? this.progress,
      targetValue: targetValue ?? this.targetValue,
      currentValue: currentValue ?? this.currentValue,
      xpReward: xpReward ?? this.xpReward,
    );
  }
}

class GamificationProfile {
  final String userId;
  final int level;
  final String levelTitle; // e.g. "Supplement Master"
  final int currentXp;
  final int xpToNextLevel;
  final List<GamificationBadge> badges;

  const GamificationProfile({
    required this.userId,
    required this.level,
    required this.levelTitle,
    required this.currentXp,
    required this.xpToNextLevel,
    required this.badges,
  });

  // Helpers for progress
  double get progress => currentXp / xpToNextLevel;
  int get earnedBadgesCount => badges.where((b) => b.isEarned).length;
  int get totalBadgesCount => badges.length;
}

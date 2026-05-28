import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import '../../domain/entities/gamification.dart';
import '../../domain/entities/user.dart';
import '../../domain/repositories/gamification_repository.dart';
import '../../utils/logger.dart';

class FirebaseGamificationRepository implements GamificationRepository {
  final FirebaseFirestore _firestore;

  FirebaseGamificationRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  // Master list of all available badges
  static const List<GamificationBadge> _badgeDefinitions = [
    GamificationBadge(
      id: 'early_bird',
      title: 'Early Bird',
      subtitle: 'Log morning stack before 9 AM',
      icon: Icons.wb_sunny,
      color: Colors.amber,
      xpReward: 150,
    ),
    GamificationBadge(
      id: '7_day_warrior',
      title: '7-Day Warrior',
      subtitle: 'Maintain a 7-day streak',
      icon: Icons.local_fire_department,
      color: Color(0xFFEC1380),
      tier: BadgeTier.bronze,
      targetValue: 7,
      xpReward: 500,
    ),
    GamificationBadge(
      id: '30_day_legend',
      title: '30-Day Legend',
      subtitle: 'Maintain a 30-day streak',
      icon: Icons.workspace_premium,
      color: Color(0xFFFFD700),
      tier: BadgeTier.silver,
      targetValue: 30,
      xpReward: 2000,
    ),
    GamificationBadge(
      id: 'safety_first',
      title: 'Safety First',
      subtitle: 'Check 1 interaction',
      icon: Icons.verified_user,
      color: Colors.blue,
      xpReward: 100,
    ),
    GamificationBadge(
      id: 'focus_adept',
      title: 'Focus Adept',
      subtitle: 'Reach Level 10',
      icon: Icons.psychology,
      color: Colors.purple,
      tier: BadgeTier.silver,
      targetValue: 10,
      xpReward: 1000,
    ),
    GamificationBadge(
      id: 'alpha_hero',
      title: 'Alpha Hero',
      subtitle: 'Early app supporter',
      icon: Icons.auto_awesome,
      color: Color(0xFFFFD700),
      tier: BadgeTier.gold,
      xpReward: 5000,
    ),
  ];

  @override
  Future<GamificationProfile> getProfile(String userId) async {
    try {
      final userDoc = await _firestore.collection('users').doc(userId).get();
      if (!userDoc.exists) {
        throw Exception('User not found');
      }

      final user = User.fromJson(userDoc.data()!);
      final badges = await getBadges(userId, user: user);

      return GamificationProfile(
        userId: userId,
        level: user.level,
        levelTitle: _getLevelTitle(user.level),
        currentXp: user.xp,
        xpToNextLevel: _getXpToNextLevel(user.level),
        badges: badges,
      );
    } catch (e) {
      AppLogger.e('Error fetching gamification profile', e);
      rethrow;
    }
  }

  @override
  Future<List<GamificationBadge>> getBadges(String userId, {User? user}) async {
    // If user object not provided, fetch it
    if (user == null) {
      final doc = await _firestore.collection('users').doc(userId).get();
      if (!doc.exists) return [];
      user = User.fromJson(doc.data()!);
    }

    final unlockedIds = user.unlockedAchievements;

    // Fetch streak for progress calculation
    final streakDoc = await _firestore.collection('streaks').doc(userId).get();
    final currentStreak = streakDoc.exists
        ? (streakDoc.data()?['currentStreak'] as int? ?? 0)
        : 0;

    return _badgeDefinitions.map((def) {
      final isEarned = unlockedIds.contains(def.id);

      // Calculate progress
      int currentValue = 0;
      if (isEarned) {
        currentValue = def.targetValue;
      } else {
        if (def.id.contains('streak') || def.id.contains('_day_')) {
          currentValue = currentStreak;
        } else if (def.id == 'focus_adept') {
          currentValue = user!.level;
        }
      }

      double progress = def.targetValue > 0
          ? (currentValue / def.targetValue).clamp(0.0, 1.0)
          : 0.0;

      return def.copyWith(
        isEarned: isEarned,
        isLocked: !isEarned,
        currentValue: currentValue,
        progress: progress,
      );
    }).toList();
  }

  int _getXpToNextLevel(int level) {
    // ADHD-friendly: Fast progression at first
    if (level < 5) return 500;
    if (level < 10) return 1000;
    return level * 200; // Scales up linearly later
  }

  String _getLevelTitle(int level) {
    if (level < 5) return 'Novice';
    if (level < 10) return 'Apprentice';
    if (level < 20) return 'Focus Adept';
    if (level < 50) return 'Mental Warrior';
    return 'Zen Master';
  }
}

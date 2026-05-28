import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/gamification.dart';

void main() {
  group('GamificationBadge Entity', () {
    const baseBadge = GamificationBadge(
      id: 'test_badge',
      title: 'Test Badge',
      subtitle: 'Testing subtitle',
      icon: Icons.star,
      color: Colors.blue,
    );

    test('should have default values set correctly', () {
      expect(baseBadge.isEarned, isFalse);
      expect(baseBadge.isLocked, isTrue);
      expect(baseBadge.tier, BadgeTier.bronze);
      expect(baseBadge.progress, 0.0);
      expect(baseBadge.currentValue, 0);
      expect(baseBadge.targetValue, 1);
      expect(baseBadge.xpReward, 100);
    });

    test('should copyWith all fields correctly', () {
      final earnedDate = DateTime.now();
      final updatedBadge = baseBadge.copyWith(
        isEarned: true,
        isLocked: false,
        tier: BadgeTier.gold,
        progress: 1.0,
        currentValue: 10,
        targetValue: 10,
        xpReward: 500,
        earnedDate: earnedDate,
      );

      expect(updatedBadge.isEarned, isTrue);
      expect(updatedBadge.isLocked, isFalse);
      expect(updatedBadge.tier, BadgeTier.gold);
      expect(updatedBadge.progress, 1.0);
      expect(updatedBadge.currentValue, 10);
      expect(updatedBadge.targetValue, 10);
      expect(updatedBadge.xpReward, 500);
      expect(updatedBadge.earnedDate, earnedDate);
    });
  });

  group('GamificationProfile', () {
    test('should calculate progress and counts correctly', () {
      final badges = [
        const GamificationBadge(
          id: 'b1',
          title: 'B1',
          subtitle: '',
          icon: Icons.abc,
          color: Colors.red,
          isEarned: true,
        ),
        const GamificationBadge(
          id: 'b2',
          title: 'B2',
          subtitle: '',
          icon: Icons.abc,
          color: Colors.red,
          isEarned: false,
        ),
      ];

      final profile = GamificationProfile(
        userId: 'u1',
        level: 5,
        levelTitle: 'Master',
        currentXp: 500,
        xpToNextLevel: 1000,
        badges: badges,
      );

      expect(profile.progress, 0.5);
      expect(profile.earnedBadgesCount, 1);
      expect(profile.totalBadgesCount, 2);
    });
  });
}

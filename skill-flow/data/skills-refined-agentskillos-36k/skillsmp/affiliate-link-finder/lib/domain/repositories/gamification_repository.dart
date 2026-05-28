import '../entities/gamification.dart';

abstract class GamificationRepository {
  /// Get full gamification profile for a user
  Future<GamificationProfile> getProfile(String userId);

  /// Get just the list of badges (optional convenience)
  Future<List<GamificationBadge>> getBadges(String userId);
}

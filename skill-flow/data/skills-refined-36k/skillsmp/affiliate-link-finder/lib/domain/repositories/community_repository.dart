import '../entities/community_post.dart';

abstract class CommunityRepository {
  /// Get posts, optionally filtered by category/tag
  Future<List<CommunityPost>> getPosts({String? category});

  /// Toggle helpful/insightful status
  Future<void> toggleHelpful(String postId);
}

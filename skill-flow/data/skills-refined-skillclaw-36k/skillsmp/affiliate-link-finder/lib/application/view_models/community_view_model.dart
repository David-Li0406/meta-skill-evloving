import 'package:flutter/foundation.dart';
import '../../utils/logger.dart';
import '../../domain/entities/community_post.dart';
import '../../domain/repositories/community_repository.dart';

class CommunityViewModel extends ChangeNotifier {
  final CommunityRepository _repository;

  List<CommunityPost> _posts = [];
  List<CommunityPost> get posts => _posts;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String _selectedFilter = '#All';
  String get selectedFilter => _selectedFilter;

  final List<String> filters = [
    '#All',
    '#MorningRoutine',
    '#FocusTips',
    '#SleepHacks',
  ];

  CommunityViewModel(this._repository) {
    loadPosts();
  }

  Future<void> loadPosts() async {
    _isLoading = true;
    notifyListeners();

    try {
      _posts = await _repository.getPosts(category: _selectedFilter);
    } catch (e) {
      if (kDebugMode) {
        AppLogger.e('Error loading posts', e);
      }
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void setFilter(String filter) {
    if (_selectedFilter != filter) {
      _selectedFilter = filter;
      loadPosts();
    }
  }

  Future<void> toggleHelpful(String postId) async {
    // Optimistic update
    final index = _posts.indexWhere((p) => p.id == postId);
    if (index != -1) {
      final post = _posts[index];
      final updatedPost = post.copyWith(
        isInsightful: !post.isInsightful,
        helpfulCount:
            post.isInsightful ? post.helpfulCount - 1 : post.helpfulCount + 1,
      );
      _posts[index] = updatedPost;
      notifyListeners();

      try {
        await _repository.toggleHelpful(postId);
      } catch (e) {
        // Revert on error
        _posts[index] = post;
        notifyListeners();
      }
    }
  }
}

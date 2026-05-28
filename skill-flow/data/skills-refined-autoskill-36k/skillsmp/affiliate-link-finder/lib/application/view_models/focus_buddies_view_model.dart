import 'package:flutter/foundation.dart';

import '../../domain/repositories/auth_repository.dart';
import '../../domain/repositories/log_repository.dart';

class FocusBuddiesViewModel extends ChangeNotifier {
  // Ignored for now as they are placeholders for future implementation
  // ignore: unused_field
  final AuthRepository _authRepository;
  // ignore: unused_field
  final LogRepository _logRepository;

  FocusBuddiesViewModel(this._authRepository, this._logRepository);

  // Mock data for now, would come from SocialRepository
  final double _teamGoalProgress = 0.75;
  final int _sharedGoalDays = 6;
  final int _totalDaysGoal = 8;

  final String _opponentName = "Alex";
  final int _opponentStreak = 10;
  final String _opponentImage =
      'https://lh3.googleusercontent.com/aida-public/AB6AXuC2ESo4fGI8ZC0JqCjTqfeMrymcGC86qXyaKokGASl6caxhGNVViQQz5zf1HtFYlDwm7KsGm7sDC5E_J-d6g7nIaf3DkondKQ7hD7dZsrArtf1ddF9qqbkvG1pSnhh690nlE8n25x4dqFy3OlGr46QPR7vmKlVvdxlb4i8elu3rmA-NjZMo6xxF2zLZ15lyepeWzklRLOT9PxUelGa-UjLj4JpS3B7NuNNttb4TmXmSz7DCcvsK3DvbEXU4v0VjDecArCGEtiqdyiM';

  final int _userStreak = 12;
  final String _userImage =
      'https://lh3.googleusercontent.com/aida-public/AB6AXuCW4otpvyD5on_5_YykKsYQDwXOKJ03f_jAdGJZmcqhS5WzZbNDZSvwtkfTzmEZz2LigExl9e5SkShfbDq-5RZHiXQe8puS2SFpKn1YdTQT4YI3bQuKhRg6yd6vHyloHlQWxEV7rj4yYC_nFRh16-9-YSc9xji_OrmO-y5bhTT-EhkNYCgRXC5kzsUKzqukF_ui02Awx2B-k6etsC2bAv0IOvojziEOo95cqEAeAVAf1pgq4vQI7kKcVWe9ZSX7ubYEODJ2IBUiWwA';

  final String _teamXP = '4,550';
  final String _teamGrowth = '+15%';
  final String _daysActive = '22';
  final String _activeGrowth = '+2';

  final List<BuddyFeedItem> _feedItems = [
    BuddyFeedItem(
      iconType: FeedIconType.check,
      text: "You logged Morning Stack! +50 XP",
      timestamp: DateTime.now().subtract(const Duration(hours: 2)),
    ),
    BuddyFeedItem(
      iconType: FeedIconType.notification,
      text: "Alex needs a nudge for Afternoon Stack.",
      timestamp: DateTime.now().subtract(const Duration(hours: 4)),
      isActionable: true,
    ),
  ];

  bool _isLoading = false;

  // Getters
  double get teamGoalProgress => _teamGoalProgress;
  int get sharedGoalDays => _sharedGoalDays;
  int get totalDaysGoal => _totalDaysGoal;
  String get opponentName => _opponentName;
  int get opponentStreak => _opponentStreak;
  String get opponentImage => _opponentImage;
  int get userStreak => _userStreak;
  String get userImage => _userImage;
  String get teamXP => _teamXP;
  String get teamGrowth => _teamGrowth;
  String get daysActive => _daysActive;
  String get activeGrowth => _activeGrowth;
  List<BuddyFeedItem> get feedItems => _feedItems;
  bool get isLoading => _isLoading;

  Future<void> loadData() async {
    _isLoading = true;
    notifyListeners();
    // Simulate network delay
    await Future<void>.delayed(const Duration(milliseconds: 500));
    _isLoading = false;
    notifyListeners();
  }

  Future<void> sendNudge() async {
    // Logic to send nudge
    // In real app, call repository
    await Future<void>.delayed(const Duration(seconds: 1));
    // Could add a feed item saying "You nudged Alex"
    _feedItems.insert(
        0,
        BuddyFeedItem(
          iconType: FeedIconType.bolt,
          text: "You nudged $_opponentName!",
          timestamp: DateTime.now(),
        ));
    notifyListeners();
  }

  Future<void> addBuddy(String email) async {
    // Simulate API call
    _isLoading = true;
    notifyListeners();
    await Future<void>.delayed(const Duration(seconds: 1));
    _isLoading = false;

    // In a real app, this would update the list of buddies.
    // For now, we just add a feed item.
    _feedItems.insert(
        0,
        BuddyFeedItem(
          iconType: FeedIconType.check,
          text: "Invite sent to $email",
          timestamp: DateTime.now(),
        ));

    notifyListeners();
  }
}

enum FeedIconType { check, notification, bolt }

class BuddyFeedItem {
  final FeedIconType iconType;
  final String text;
  final DateTime timestamp;
  final bool isActionable;

  BuddyFeedItem({
    required this.iconType,
    required this.text,
    required this.timestamp,
    this.isActionable = false,
  });
}

import 'package:flutter/foundation.dart';
import '../../domain/entities/gamification.dart';
import '../../domain/repositories/gamification_repository.dart';

class TrophyRoomViewModel extends ChangeNotifier {
  final GamificationRepository _repository;
  final String _userId;

  GamificationProfile? _profile;
  GamificationProfile? get profile => _profile;

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  String? _error;
  String? get error => _error;

  TrophyRoomViewModel(this._repository, this._userId) {
    _loadData();
  }

  Future<void> _loadData() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _profile = await _repository.getProfile(_userId);
    } catch (e) {
      _error = 'Failed to load trophy room: $e';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  // Derived getters for UI
  List<GamificationBadge> get recentWins {
    // Return earned badges, maybe sorted by date if dates were real
    // For now just take the first 4 earned ones
    return _profile?.badges.where((b) => b.isEarned).take(4).toList() ?? [];
  }

  List<GamificationBadge> get allGridBadges {
    // Return all badges for the grid
    return _profile?.badges ?? [];
  }
}

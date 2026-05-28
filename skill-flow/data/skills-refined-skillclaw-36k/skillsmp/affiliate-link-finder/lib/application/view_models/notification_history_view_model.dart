import 'package:flutter/foundation.dart';
import '../../domain/entities/notification_log_item.dart';

class NotificationHistoryViewModel extends ChangeNotifier {
  List<NotificationLogItem> _notifications = [];
  bool _isLoading = false;

  List<NotificationLogItem> get notifications => _notifications;
  bool get isLoading => _isLoading;

  NotificationHistoryViewModel() {
    loadHistory();
  }

  Future<void> loadHistory() async {
    _isLoading = true;
    notifyListeners();

    // Simulate network delay
    await Future<void>.delayed(const Duration(milliseconds: 800));

    // Mock Data
    _notifications = [
      NotificationLogItem(
        id: '1',
        title: 'Morning Stack Reminder',
        body: 'Time to take your morning stack! 💊',
        timestamp: DateTime.now().subtract(const Duration(minutes: 30)),
        type: NotificationType.medication,
      ),
      NotificationLogItem(
        id: '2',
        title: 'Hydration Check',
        body: 'Have you had water in the last hour? 💧',
        timestamp: DateTime.now().subtract(const Duration(hours: 2)),
        type: NotificationType.nudge,
      ),
      NotificationLogItem(
        id: '3',
        title: 'Evening Reflection',
        body: 'How did your day go? Log your symptoms.',
        timestamp: DateTime.now().subtract(const Duration(days: 1, hours: 4)),
        type: NotificationType.system,
      ),
      NotificationLogItem(
        id: '4',
        title: 'Milestone Unlocked!',
        body: 'You hit a 7-day streak! Keep it up! 🏆',
        timestamp: DateTime.now().subtract(const Duration(days: 2)),
        type: NotificationType.achievement,
        isRead: true,
      ),
    ];

    _isLoading = false;
    notifyListeners();
  }

  void markAsRead(String id) {
    final index = _notifications.indexWhere((n) => n.id == id);
    if (index != -1) {
      _notifications[index].isRead = true;
      notifyListeners();
    }
  }

  void deleteNotification(String id) {
    _notifications.removeWhere((n) => n.id == id);
    notifyListeners();
  }

  void clearAll() {
    _notifications.clear();
    notifyListeners();
  }
}

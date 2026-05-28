enum NotificationType {
  medication,
  nudge,
  system,
  achievement,
}

class NotificationLogItem {
  final String id;
  final String title;
  final String body;
  final DateTime timestamp;
  final NotificationType type;
  bool isRead;

  NotificationLogItem({
    required this.id,
    required this.title,
    required this.body,
    required this.timestamp,
    required this.type,
    this.isRead = false,
  });
}

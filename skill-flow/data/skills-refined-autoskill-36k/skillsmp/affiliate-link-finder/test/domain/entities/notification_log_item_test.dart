import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/notification_log_item.dart';

void main() {
  group('NotificationLogItem', () {
    test('should create NotificationLogItem with default isRead false', () {
      final now = DateTime.now();
      final item = NotificationLogItem(
        id: 'notif1',
        title: 'Reminder',
        body: 'Time to take your supplements',
        timestamp: now,
        type: NotificationType.medication,
      );

      expect(item.id, 'notif1');
      expect(item.title, 'Reminder');
      expect(item.body, 'Time to take your supplements');
      expect(item.timestamp, now);
      expect(item.type, NotificationType.medication);
      expect(item.isRead, isFalse);
    });

    test('should create NotificationLogItem with isRead true', () {
      final now = DateTime.now();
      final item = NotificationLogItem(
        id: 'notif1',
        title: 'Reminder',
        body: 'Time to take your supplements',
        timestamp: now,
        type: NotificationType.nudge,
        isRead: true,
      );

      expect(item.isRead, isTrue);
    });

    test('should allow updating isRead flag', () {
      final now = DateTime.now();
      final item = NotificationLogItem(
        id: 'notif1',
        title: 'Reminder',
        body: 'Time to take your supplements',
        timestamp: now,
        type: NotificationType.system,
      );

      expect(item.isRead, isFalse);

      item.isRead = true;

      expect(item.isRead, isTrue);
    });
  });
}


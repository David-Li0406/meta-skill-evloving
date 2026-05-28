import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/infrastructure/services/notification_service.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

void main() {
  late NotificationService notificationService;

  setUp(() {
    notificationService = NotificationService();
  });

  group('NotificationService', () {
    test('should create instance successfully', () {
      expect(notificationService, isNotNull);
      final service = NotificationService();
      expect(service, isA<NotificationService>());
    });

    test('exposes expected method signatures (unit-test friendly)', () {
      // We intentionally do NOT call these methods here because they use platform
      // channels (flutter_local_notifications + timezone) which require integration
      // testing or explicit platform mocking.

      expect(
        notificationService.scheduleNotification,
        isA<
            Future<void> Function({
              required int id,
              required String title,
              required String body,
              required DateTime scheduledDate,
            })>(),
      );

      expect(
        notificationService.scheduleRecurringNotification,
        isA<
            Future<void> Function({
              required int id,
              required String title,
              required String body,
              required int hour,
              required int minute,
              int second,
            })>(),
      );

      expect(
        notificationService.cancelNotification,
        isA<Future<void> Function(int)>(),
      );

      expect(
        notificationService.cancelAllNotifications,
        isA<Future<void> Function()>(),
      );

      expect(
        notificationService.getPendingNotifications,
        isA<Future<List<PendingNotificationRequest>> Function()>(),
      );
    });
  });
}

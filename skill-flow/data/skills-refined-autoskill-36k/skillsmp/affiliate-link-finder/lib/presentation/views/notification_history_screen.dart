import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../../application/view_models/notification_history_view_model.dart';
import '../../domain/entities/notification_log_item.dart';
import '../theme/app_theme.dart';

class NotificationHistoryScreen extends StatelessWidget {
  const NotificationHistoryScreen({super.key});

  static Widget withProvider() {
    return ChangeNotifierProvider(
      create: (_) => NotificationHistoryViewModel(),
      child: const NotificationHistoryScreen(),
    );
  }

  @override
  Widget build(BuildContext context) {
    final viewModel = context.watch<NotificationHistoryViewModel>();
    final isDark = Theme.of(context).brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Notification History'),
        actions: [
          if (viewModel.notifications.isNotEmpty)
            IconButton(
              icon: const Icon(Icons.delete_sweep),
              tooltip: 'Clear All',
              onPressed: () {
                showDialog<void>(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Clear All History?'),
                    content: const Text(
                        'This will permanently delete all notification logs.'),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.pop(ctx),
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () {
                          viewModel.clearAll();
                          Navigator.pop(ctx);
                        },
                        child: const Text(
                          'Clear',
                          style: TextStyle(color: Colors.red),
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
        ],
      ),
      body: viewModel.isLoading
          ? const Center(child: CircularProgressIndicator())
          : viewModel.notifications.isEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(
                        Icons.notifications_off_outlined,
                        size: 64,
                        color: isDark ? Colors.grey[700] : Colors.grey[300],
                      ),
                      const SizedBox(height: 16),
                      Text(
                        'No notifications yet',
                        style: TextStyle(
                          fontSize: 18,
                          color: isDark ? Colors.grey[600] : Colors.grey[400],
                        ),
                      ),
                    ],
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(16),
                  itemCount: viewModel.notifications.length,
                  itemBuilder: (context, index) {
                    final notification = viewModel.notifications[index];
                    return Dismissible(
                      key: Key(notification.id),
                      direction: DismissDirection.endToStart,
                      background: Container(
                        alignment: Alignment.centerRight,
                        padding: const EdgeInsets.only(right: 20),
                        color: Colors.red,
                        child: const Icon(Icons.delete, color: Colors.white),
                      ),
                      onDismissed: (_) {
                        viewModel.deleteNotification(notification.id);
                      },
                      child: _NotificationTile(notification: notification),
                    );
                  },
                ),
    );
  }
}

class _NotificationTile extends StatelessWidget {
  final NotificationLogItem notification;

  const _NotificationTile({required this.notification});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;

    IconData getIcon() {
      switch (notification.type) {
        case NotificationType.medication:
          return Icons.medication;
        case NotificationType.nudge:
          return Icons
              .touch_app; // Use touch_app instead of circle_notifications
        case NotificationType.achievement:
          return Icons.emoji_events;
        case NotificationType.system:
          return Icons.info_outline;
      }
    }

    Color getColor() {
      switch (notification.type) {
        case NotificationType.medication:
          return AppColors.secondary;
        case NotificationType.nudge:
          return AppColors.primary;
        case NotificationType.achievement:
          return Colors.amber;
        case NotificationType.system:
          return Colors.grey;
      }
    }

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 0,
      color: isDark ? AppColors.cardDark.withValues(alpha: 0.5) : Colors.white,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: isDark ? Colors.white10 : Colors.grey[200]!,
        ),
      ),
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: getColor().withValues(alpha: 0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(
            getIcon(),
            color: getColor(),
            size: 20,
          ),
        ),
        title: Text(
          notification.title,
          style: TextStyle(
            fontWeight:
                notification.isRead ? FontWeight.normal : FontWeight.bold,
            color: isDark ? Colors.white : Colors.black87,
          ),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text(
              notification.body,
              style: TextStyle(
                color: isDark ? Colors.grey[400] : Colors.grey[600],
              ),
            ),
            const SizedBox(height: 4),
            Text(
              DateFormat.jm().add_yMMMd().format(notification.timestamp),
              style: TextStyle(
                fontSize: 12,
                color: isDark ? Colors.grey[600] : Colors.grey[500],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

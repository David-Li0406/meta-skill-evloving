import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/application/view_models/notification_history_view_model.dart';

void main() {
  late NotificationHistoryViewModel viewModel;

  setUp(() {
    viewModel = NotificationHistoryViewModel();
  });

  test('Initial state is correct', () {
    expect(viewModel.notifications, isEmpty);
    // isLoading might be true briefly due to constructor call, but we can't easily wait for constructor async.
    // In a real app we'd inject a service and mock it to control timing.
    // For this MVP ViewModel, loadHistory is called in constructor.
  });

  test('loadHistory populates notifications', () async {
    // Wait for the async constructor simulation
    await Future<void>.delayed(const Duration(milliseconds: 1000));

    expect(viewModel.notifications, isNotEmpty);
    expect(viewModel.notifications.length, 4); // Based on mock data
  });

  test('markAsRead updates item status', () async {
    await Future<void>.delayed(const Duration(milliseconds: 1000));

    final id = viewModel.notifications.first.id;
    viewModel.markAsRead(id);

    expect(viewModel.notifications.first.isRead, true);
  });

  test('deleteNotification removes item', () async {
    await Future<void>.delayed(const Duration(milliseconds: 1000));
    final initialLength = viewModel.notifications.length;
    final id = viewModel.notifications.first.id;

    viewModel.deleteNotification(id);

    expect(viewModel.notifications.length, initialLength - 1);
    expect(viewModel.notifications.where((n) => n.id == id), isEmpty);
  });

  test('clearAll removes all items', () async {
    await Future<void>.delayed(const Duration(milliseconds: 1000));
    expect(viewModel.notifications, isNotEmpty);

    viewModel.clearAll();

    expect(viewModel.notifications, isEmpty);
  });
}

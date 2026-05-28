import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';

void main() {
  test('User.fromJson should correctly parse ISO8601 createdAt string', () {
    final jsonData = {
      'id': 'test-uid',
      'email': 'test@daily-stack.com',
      'displayName': 'Test User',
      'createdAt': DateTime.now().toIso8601String(),
      'hasCompletedOnboarding': true,
      'unlockedAchievements': <String>[],
    };

    final user = User.fromJson(jsonData);

    expect(user.id, 'test-uid');
    expect(user.email, 'test@daily-stack.com');
    expect(user.createdAt, isA<DateTime>());
  });
}

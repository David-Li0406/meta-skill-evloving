import 'package:uuid/uuid.dart';
import '../../domain/entities/symptom_checkin.dart';
import '../../domain/repositories/symptom_repository.dart';

class MockSymptomRepository implements SymptomRepository {
  final List<SymptomCheckIn> _checkIns = [];

  MockSymptomRepository() {
    // Seed with some dummy data for demo
    final now = DateTime.now();
    _checkIns.addAll([
      SymptomCheckIn(
        id: const Uuid().v4(),
        userId: 'demo_user',
        timestamp: now.subtract(const Duration(days: 1)),
        focusLevel: 65,
        energyLevel: 70,
        moodLevel: 75,
        notes: 'Felt pretty good yesterday.',
      ),
      SymptomCheckIn(
        id: const Uuid().v4(),
        userId: 'demo_user',
        timestamp: now.subtract(const Duration(days: 2)),
        focusLevel: 50,
        energyLevel: 60,
        moodLevel: 55,
      ),
    ]);
  }

  @override
  Future<void> logCheckIn(SymptomCheckIn checkIn) async {
    // Simulate network delay
    await Future<void>.delayed(const Duration(milliseconds: 500));
    _checkIns.add(checkIn);
  }

  @override
  Future<List<SymptomCheckIn>> getCheckIns(String userId) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    return _checkIns.where((c) => c.userId == userId).toList()
      ..sort((a, b) => b.timestamp.compareTo(a.timestamp));
  }

  @override
  Future<List<SymptomCheckIn>> getCheckInsByDateRange(
    String userId,
    DateTime startDate,
    DateTime endDate,
  ) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    return _checkIns.where((c) {
      return c.userId == userId &&
          c.timestamp.isAfter(startDate) &&
          c.timestamp.isBefore(endDate);
    }).toList()
      ..sort((a, b) => b.timestamp.compareTo(a.timestamp));
  }

  @override
  Future<SymptomCheckIn?> getLatestCheckIn(String userId) async {
    await Future<void>.delayed(const Duration(milliseconds: 200));
    final userCheckIns = _checkIns.where((c) => c.userId == userId).toList()
      ..sort((a, b) => b.timestamp.compareTo(a.timestamp));

    if (userCheckIns.isEmpty) return null;
    return userCheckIns.first;
  }

  @override
  Future<bool> hasCheckedInToday(String userId) async {
    final now = DateTime.now();
    final startOfDay = DateTime(now.year, now.month, now.day);
    final endOfDay = startOfDay.add(const Duration(days: 1));

    final latest = await getLatestCheckIn(userId);
    if (latest == null) return false;

    return latest.timestamp.isAfter(startOfDay) &&
        latest.timestamp.isBefore(endOfDay);
  }

  @override
  Future<void> deleteCheckIn(String id) async {
    await Future<void>.delayed(const Duration(milliseconds: 300));
    _checkIns.removeWhere((c) => c.id == id);
  }
}

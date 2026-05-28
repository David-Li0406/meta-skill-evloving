import '../entities/symptom_checkin.dart';

abstract class SymptomRepository {
  /// Log a new symptom check-in
  Future<void> logCheckIn(SymptomCheckIn checkIn);

  /// Get all check-ins for a user
  Future<List<SymptomCheckIn>> getCheckIns(String userId);

  /// Get check-ins within a date range
  Future<List<SymptomCheckIn>> getCheckInsByDateRange(
    String userId,
    DateTime startDate,
    DateTime endDate,
  );

  /// Get the most recent check-in
  Future<SymptomCheckIn?> getLatestCheckIn(String userId);

  /// Check if user has checked in today
  Future<bool> hasCheckedInToday(String userId);

  /// Delete a check-in
  Future<void> deleteCheckIn(String id);
}

// ADHD-friendly date utilities.
//
// Provides functions that handle the "4 AM Rollover" logic,
// where the "logical day" resets at 4:00 AM instead of midnight.
// This accommodates users with erratic sleep schedules.

/// Rollover hour constant. The logical day starts at this hour.
const int kRolloverHour = 4;

/// Returns the "logical date" for ADHD-friendly day boundaries.
///
/// If the current time is before [kRolloverHour] (4 AM), we consider it
/// still "yesterday" from a tracking perspective.
///
/// Example:
/// - At 2:30 AM on Jan 15th, `getLogicalDate()` returns Jan 14th.
/// - At 5:00 AM on Jan 15th, `getLogicalDate()` returns Jan 15th.
DateTime getLogicalDate([DateTime? now]) {
  final current = now ?? DateTime.now();
  if (current.hour < kRolloverHour) {
    // Subtract one day; DateTime handles month/year boundaries.
    return DateTime(current.year, current.month, current.day - 1);
  }
  return DateTime(current.year, current.month, current.day);
}

/// Returns the "logical date" as an ISO8601 string (date part only).
///
/// Useful for Firestore queries where dates are stored as strings.
String getLogicalDateString([DateTime? now]) {
  final date = getLogicalDate(now);
  return date.toIso8601String().split('T').first;
}

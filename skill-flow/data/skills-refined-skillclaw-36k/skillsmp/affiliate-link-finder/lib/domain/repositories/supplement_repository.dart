import '../entities/supplement.dart';

abstract class SupplementRepository {
  /// Get all available supplements (Global + User-specific if userId provided)
  Future<List<Supplement>> getAllSupplements({String? userId});

  /// Get supplements by category
  Future<List<Supplement>> getSupplementsByCategory(String category,
      {String? userId});

  /// Search supplements by name or benefits
  Future<List<Supplement>> searchSupplements(String query, {String? userId});

  /// Get a specific supplement by ID
  Future<Supplement?> getSupplement(String id, {String? userId});

  /// Stream of all supplements (real-time updates)
  Stream<List<Supplement>> watchSupplements({String? userId});

  /// Save a user-created custom supplement
  Future<void> saveCustomSupplement(Supplement supplement);

  /// Delete a user-created custom supplement
  Future<void> deleteCustomSupplement(String id, String userId);

  /// Track a referral click
  Future<void> trackReferralClick(String supplementId);
}

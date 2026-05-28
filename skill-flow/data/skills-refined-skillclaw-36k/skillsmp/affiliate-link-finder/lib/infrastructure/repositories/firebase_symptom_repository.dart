import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/symptom_checkin.dart';
import '../../domain/repositories/symptom_repository.dart';
import '../../utils/logger.dart';

class FirebaseSymptomRepository implements SymptomRepository {
  final FirebaseFirestore _firestore;
  static const String _collection = 'symptom_checkins';

  FirebaseSymptomRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  @override
  Future<void> logCheckIn(SymptomCheckIn checkIn) async {
    try {
      await _firestore
          .collection(_collection)
          .doc(checkIn.id)
          .set(checkIn.toJson());
    } catch (e) {
      AppLogger.e('Error logging check-in', e);
      throw Exception('Failed to log check-in: $e');
    }
  }

  @override
  Future<List<SymptomCheckIn>> getCheckIns(String userId) async {
    try {
      final snapshot = await _firestore
          .collection(_collection)
          .where('userId', isEqualTo: userId)
          .orderBy('timestamp', descending: true)
          .get(const GetOptions(source: Source.serverAndCache))
          .timeout(const Duration(seconds: 3));

      return snapshot.docs
          .map((doc) => SymptomCheckIn.fromJson(doc.data()))
          .toList();
    } catch (e) {
      AppLogger.w('Fetching check-ins from cache (offline)', e);
      try {
        final snapshot = await _firestore
            .collection(_collection)
            .where('userId', isEqualTo: userId)
            .get(const GetOptions(source: Source.cache));
        return snapshot.docs
            .map((doc) => SymptomCheckIn.fromJson(doc.data()))
            .toList();
      } catch (cacheErr) {
        AppLogger.e('Symptom cache failure', cacheErr);
        return [];
      }
    }
  }

  @override
  Future<List<SymptomCheckIn>> getCheckInsByDateRange(
    String userId,
    DateTime startDate,
    DateTime endDate,
  ) async {
    final snapshot = await _firestore
        .collection(_collection)
        .where('userId', isEqualTo: userId)
        .where('timestamp', isGreaterThanOrEqualTo: startDate.toIso8601String())
        .where('timestamp', isLessThanOrEqualTo: endDate.toIso8601String())
        .orderBy('timestamp', descending: true)
        .get();

    return snapshot.docs
        .map((doc) => SymptomCheckIn.fromJson(doc.data()))
        .toList();
  }

  @override
  Future<SymptomCheckIn?> getLatestCheckIn(String userId) async {
    try {
      final snapshot = await _firestore
          .collection(_collection)
          .where('userId', isEqualTo: userId)
          .orderBy('timestamp', descending: true)
          .limit(1)
          .get(const GetOptions(source: Source.serverAndCache))
          .timeout(const Duration(seconds: 3));

      if (snapshot.docs.isEmpty) return null;
      return SymptomCheckIn.fromJson(snapshot.docs.first.data());
    } catch (e) {
      AppLogger.w('Fetching latest check-in from cache', e);
      try {
        final snapshot = await _firestore
            .collection(_collection)
            .where('userId', isEqualTo: userId)
            .orderBy('timestamp', descending: true)
            .limit(1)
            .get(const GetOptions(source: Source.cache));
        if (snapshot.docs.isEmpty) return null;
        return SymptomCheckIn.fromJson(snapshot.docs.first.data());
      } catch (cacheErr) {
        AppLogger.e('Latest check-in cache failure', cacheErr);
        return null;
      }
    }
  }

  @override
  Future<bool> hasCheckedInToday(String userId) async {
    final now = DateTime.now();
    final startOfDay = DateTime(now.year, now.month, now.day);
    final endOfDay = startOfDay.add(const Duration(days: 1));

    final snapshot = await _firestore
        .collection(_collection)
        .where('userId', isEqualTo: userId)
        .where('timestamp',
            isGreaterThanOrEqualTo: startOfDay.toIso8601String())
        .where('timestamp', isLessThan: endOfDay.toIso8601String())
        .limit(1)
        .get();

    return snapshot.docs.isNotEmpty;
  }

  @override
  Future<void> deleteCheckIn(String id) async {
    await _firestore.collection(_collection).doc(id).delete();
  }
}

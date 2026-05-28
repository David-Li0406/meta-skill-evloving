import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/supplement_interaction.dart';
import '../../domain/entities/safety_override.dart';
import '../../domain/repositories/safety_repository.dart';

class FirebaseSafetyRepository implements SafetyRepository {
  final FirebaseFirestore _firestore;

  FirebaseSafetyRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  @override
  Future<List<SupplementInteraction>> getInteractionsForSupplements(
      List<String> supplementIds) async {
    if (supplementIds.length < 2) return [];

    try {
      // For simplicity, we fetch all interactions and filter locally
      // In a large database, we would use a more optimized query
      final snapshot = await _firestore.collection('interactions').get();

      final allInteractions = snapshot.docs
          .map((doc) =>
              SupplementInteraction.fromJson({...doc.data(), 'id': doc.id}))
          .toList();

      return allInteractions.where((interaction) {
        return supplementIds.contains(interaction.supplementAId) &&
            supplementIds.contains(interaction.supplementBId);
      }).toList();
    } catch (e) {
      throw Exception('Failed to fetch interactions: $e');
    }
  }

  @override
  Future<void> logSafetyOverride(SafetyOverride override) async {
    try {
      await _firestore
          .collection('safety_overrides')
          .doc(override.id)
          .set(override.toJson());
    } catch (e) {
      throw Exception('Failed to log safety override: $e');
    }
  }

  @override
  Future<List<SafetyOverride>> getSafetyOverrides(String userId) async {
    try {
      final snapshot = await _firestore
          .collection('safety_overrides')
          .where('userId', isEqualTo: userId)
          .get();

      return snapshot.docs
          .map((doc) => SafetyOverride.fromJson({...doc.data(), 'id': doc.id}))
          .toList();
    } catch (e) {
      throw Exception('Failed to fetch safety overrides: $e');
    }
  }

  @override
  Future<SupplementInteraction?> getInteractionById(String id) async {
    try {
      final doc = await _firestore.collection('interactions').doc(id).get();
      if (!doc.exists) return null;
      return SupplementInteraction.fromJson({...doc.data()!, 'id': doc.id});
    } catch (e) {
      throw Exception('Failed to fetch interaction: $e');
    }
  }
}

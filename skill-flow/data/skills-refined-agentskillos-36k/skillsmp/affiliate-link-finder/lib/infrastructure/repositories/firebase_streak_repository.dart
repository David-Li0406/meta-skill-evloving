import 'package:cloud_firestore/cloud_firestore.dart';
import '../../domain/entities/streak.dart';
import '../../domain/repositories/streak_repository.dart';

class FirebaseStreakRepository implements StreakRepository {
  final FirebaseFirestore _firestore;

  FirebaseStreakRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  @override
  Future<Streak?> getStreak(String userId) async {
    final doc = await _firestore.collection('streaks').doc(userId).get();
    if (doc.exists) {
      return Streak.fromJson(doc.data()!);
    }
    return null;
  }

  @override
  Future<void> saveStreak(Streak streak) async {
    await _firestore
        .collection('streaks')
        .doc(streak.userId)
        .set(streak.toJson());
  }

  @override
  Stream<Streak?> watchStreak(String userId) {
    return _firestore.collection('streaks').doc(userId).snapshots().map((doc) {
      if (doc.exists && doc.data() != null) {
        return Streak.fromJson(doc.data()!);
      }
      return null;
    });
  }
}

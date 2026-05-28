import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../../domain/entities/referral.dart';
import '../../domain/repositories/referral_repository.dart';

class FirebaseReferralRepository implements ReferralRepository {
  final FirebaseFirestore _firestore;
  final FirebaseAuth _auth;

  FirebaseReferralRepository({
    FirebaseFirestore? firestore,
    FirebaseAuth? auth,
  })  : _firestore = firestore ?? FirebaseFirestore.instance,
        _auth = auth ?? FirebaseAuth.instance;

  @override
  Future<ReferralData> getReferralData() async {
    final user = _auth.currentUser;
    if (user == null) {
      throw Exception('User not authenticated');
    }

    final referralCode = 'REF-${user.uid.substring(0, 5).toUpperCase()}';
    final shareLink = 'https://adhd-stack.app/r/$referralCode';

    // Fetch users who used this code (assuming schema has 'referredBy')
    // This part assumes we track referrals. Since we likely don't yet,
    // it will return empty, which is correct "Real Data".
    final snap = await _firestore
        .collection('users')
        .where('referredBy', isEqualTo: referralCode)
        .get();

    final referrals = snap.docs.map((doc) {
      final data = doc.data();
      final name = data['displayName'] as String? ?? 'Unknown User';
      final joinedAt =
          (data['createdAt'] as Timestamp?)?.toDate() ?? DateTime.now();

      return Referral(
        id: doc.id,
        initials: name.isNotEmpty ? name.substring(0, 2).toUpperCase() : '??',
        name: name,
        date: 'Joined ${_formatDate(joinedAt)}',
        status: 'Successful', // Simplification
        reward: '+1 Grace Day', // Simplification
        isActive: true,
      );
    }).toList();

    return ReferralData(
      referralCode: referralCode,
      shareLink: shareLink,
      referrals: referrals,
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year}';
  }
}

import '../entities/referral.dart';

abstract class ReferralRepository {
  Future<ReferralData> getReferralData();
}

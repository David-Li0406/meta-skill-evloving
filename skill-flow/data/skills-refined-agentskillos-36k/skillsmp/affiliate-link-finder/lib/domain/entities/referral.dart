class Referral {
  final String id;
  final String initials;
  final String name;
  final String date;
  final String status; // 'Successful', 'Pending'
  final String? reward;
  final bool isActive;

  Referral({
    required this.id,
    required this.initials,
    required this.name,
    required this.date,
    required this.status,
    this.reward,
    required this.isActive,
  });
}

class ReferralData {
  final String referralCode;
  final String shareLink;
  final List<Referral> referrals;

  ReferralData({
    required this.referralCode,
    required this.shareLink,
    required this.referrals,
  });
}

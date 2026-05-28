import 'package:flutter/material.dart';
import '../../utils/logger.dart';
import 'package:share_plus/share_plus.dart';
import '../../domain/entities/referral.dart';
import '../../domain/repositories/referral_repository.dart';

class ReferFriendViewModel extends ChangeNotifier {
  final ReferralRepository _referralRepository;

  ReferralData? _referralData;
  bool _isLoading = false;

  ReferFriendViewModel(this._referralRepository);

  ReferralData? get referralData => _referralData;
  bool get isLoading => _isLoading;

  Future<void> loadData() async {
    _isLoading = true;
    notifyListeners();

    try {
      _referralData = await _referralRepository.getReferralData();
    } catch (e) {
      AppLogger.e('Error loading referral data', e);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> shareReferral() async {
    if (_referralData == null) return;

    await Share.share(
      'Join me on ADHD Stack! Use my code ${_referralData!.referralCode} to get 1 month of Pro for free: ${_referralData!.shareLink}',
      subject: 'Gift from a friend: 1 Month of ADHD Stack Pro',
    );
  }
}

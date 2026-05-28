import 'package:flutter/material.dart';

import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/domain/services/analytics_service.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';

class SupplementViewModel extends ChangeNotifier {
  final SupplementRepository _repository;
  final UrlService _urlService;
  final AnalyticsService _analyticsService;

  SupplementViewModel(
      this._repository, this._urlService, this._analyticsService) {
    _fetchSupplements();
  }

  bool _isLoading = false;
  List<Supplement> _supplements = [];
  String? _error;

  bool get isLoading => _isLoading;
  List<Supplement> get supplements => _supplements;
  String? get error => _error;

  Future<void> _fetchSupplements() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _supplements = await _repository.getAllSupplements();
    } catch (e) {
      _error = 'Failed to load supplements';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> onReferralClicked(Supplement supplement) async {
    await _repository.trackReferralClick(supplement.id);
    await _analyticsService.logEvent('referral_clicked', parameters: {
      'supplement_id': supplement.id,
      'supplement_name': supplement.name,
      'category': supplement.category,
    });
    await _urlService.launchReferral(supplement.referralUrl);
  }
}

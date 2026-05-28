import 'package:flutter/material.dart';
import '../../domain/services/billing_service.dart';
import '../../domain/services/analytics_service.dart';
import '../../config/locator.dart';

class SubscriptionViewModel extends ChangeNotifier {
  final BillingService _billingService = locator<BillingService>();
  final AnalyticsService _analyticsService = locator<AnalyticsService>();

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  bool _isSubscribed = false;
  bool get isSubscribed => _isSubscribed;

  String? _error;
  String? get error => _error;

  SubscriptionViewModel() {
    _checkSubscriptionStatus();
  }

  Future<void> _checkSubscriptionStatus() async {
    _isSubscribed = await _billingService.isSubscribed;
    notifyListeners();
  }

  Future<void> purchaseSubscription(String planId) async {
    _setLoading(true);
    _error = null;
    try {
      final success =
          await _billingService.purchaseSubscription(planId: planId);
      if (success) {
        _isSubscribed = true;
        await _analyticsService.logEvent('subscription_purchased', parameters: {
          'plan_id': planId,
        });
      } else {
        _error = 'Purchase failed. Please try again.';
      }
    } catch (e) {
      _error = 'An error occurred during purchase.';
    } finally {
      _setLoading(false);
    }
  }

  Future<void> restorePurchases() async {
    _setLoading(true);
    _error = null;
    try {
      final success = await _billingService.restorePurchases();
      if (success) {
        _isSubscribed = true;
      } else {
        _error = 'No purchases found to restore.';
      }
    } catch (e) {
      _error = 'An error occurred during restore.';
    } finally {
      _setLoading(false);
    }
  }

  void _setLoading(bool value) {
    _isLoading = value;
    notifyListeners();
  }
}

import '../../domain/services/billing_service.dart';
import '../../application/view_models/subscription_view_model.dart';
import '../../application/providers/auth_provider.dart';
import 'package:provider/provider.dart';

class MockBillingService implements BillingService {
  bool _isSubscribed = false;

  @override
  Future<bool> initialize() async {
    await Future<void>.delayed(const Duration(seconds: 1));
    return true;
  }

  @override
  Future<bool> get isSubscribed async {
    return _isSubscribed;
  }

  @override
  Future<bool> purchaseSubscription({required String planId}) async {
    await Future<void>.delayed(const Duration(seconds: 2));
    _isSubscribed = true;
    return true;
  }

  @override
  Future<bool> restorePurchases() async {
    await Future<void>.delayed(const Duration(seconds: 2));
    _isSubscribed = true;
    return true;
  }

  @override
  Future<bool> hasEntitlement(String entitlementId) async {
    return _isSubscribed;
  }

  @override
  Future<List<String>> getEntitlements() async {
    return _isSubscribed ? ['pro'] : [];
  }
}

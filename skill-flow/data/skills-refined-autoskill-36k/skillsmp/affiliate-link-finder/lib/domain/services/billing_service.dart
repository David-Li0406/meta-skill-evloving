abstract class BillingService {
  Future<bool> initialize();
  Future<bool> purchaseSubscription({required String planId});
  Future<bool> restorePurchases();
  Future<bool> get isSubscribed;
  Future<bool> hasEntitlement(String entitlementId);
  Future<List<String>> getEntitlements();
}

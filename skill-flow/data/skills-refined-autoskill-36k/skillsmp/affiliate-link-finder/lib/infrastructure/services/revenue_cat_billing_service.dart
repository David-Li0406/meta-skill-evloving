import 'package:purchases_flutter/purchases_flutter.dart';
import 'dart:io' show Platform;
import '../../domain/services/billing_service.dart';
import '../../utils/logger.dart';

class RevenueCatBillingService implements BillingService {
  // Keys should ideally be loaded from environment variables or a secure config
  // Use 'flutter build --dart-define=RC_ANDROID_KEY=your_key'
  static const _androidApiKey = String.fromEnvironment('RC_ANDROID_KEY',
      defaultValue: 'goog_placeholder_api_key');
  static const _iosApiKey = String.fromEnvironment('RC_IOS_KEY',
      defaultValue: 'appl_placeholder_api_key');

  bool _isInitialized = false;

  @override
  Future<bool> initialize() async {
    if (_isInitialized) return true;

    try {
      if (Platform.isAndroid) {
        await Purchases.configure(PurchasesConfiguration(_androidApiKey));
      } else if (Platform.isIOS) {
        await Purchases.configure(PurchasesConfiguration(_iosApiKey));
      }

      _isInitialized = true;
      AppLogger.i('RevenueCat initialized successfully');
      return true;
    } catch (e) {
      AppLogger.e('Failed to initialize RevenueCat', e);
      return false;
    }
  }

  @override
  Future<bool> get isSubscribed async {
    return hasEntitlement('pro');
  }

  @override
  Future<bool> hasEntitlement(String entitlementId) async {
    if (!_isInitialized) await initialize();
    try {
      CustomerInfo customerInfo = await Purchases.getCustomerInfo();
      return customerInfo.entitlements.all[entitlementId]?.isActive ?? false;
    } catch (e) {
      AppLogger.e('Error checking entitlement: $entitlementId', e);
      return false;
    }
  }

  @override
  Future<List<String>> getEntitlements() async {
    if (!_isInitialized) await initialize();
    try {
      CustomerInfo customerInfo = await Purchases.getCustomerInfo();
      return customerInfo.entitlements.all.values
          .where((e) => e.isActive)
          .map((e) => e.identifier)
          .toList();
    } catch (e) {
      AppLogger.e('Error fetching all entitlements', e);
      return [];
    }
  }

  @override
  Future<bool> restorePurchases() async {
    try {
      await Purchases.restorePurchases();
      return true;
    } catch (e) {
      AppLogger.e('Error restoring purchases', e);
      return false;
    }
  }

  @override
  Future<bool> purchaseSubscription({required String planId}) async {
    try {
      Offerings offerings = await Purchases.getOfferings();

      Package? packageToPurchase;
      if (offerings.current != null) {
        // Try to find package by ID if provided, otherwise fallback to first available
        try {
          packageToPurchase = offerings.current!.availablePackages.firstWhere(
            (p) =>
                p.identifier == planId || p.storeProduct.identifier == planId,
          );
        } catch (_) {
          // If explicitly looking for a plan and not found, we could fail or use first
          // For now, let's use the first available as a fallback if planId is "default" or similar
          if (offerings.current!.availablePackages.isNotEmpty) {
            packageToPurchase = offerings.current!.availablePackages.first;
          }
        }
      }

      if (packageToPurchase != null) {
        await Purchases.purchasePackage(packageToPurchase);
        return true;
      } else {
        throw Exception('No offerings available for plan: $planId');
      }
    } catch (e) {
      AppLogger.e('Purchase failed', e);
      return false;
    }
  }
}

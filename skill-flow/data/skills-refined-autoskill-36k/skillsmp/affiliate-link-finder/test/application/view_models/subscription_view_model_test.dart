import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/application/view_models/subscription_view_model.dart';
import 'package:adhd_supplement_app/domain/services/billing_service.dart';
import 'package:adhd_supplement_app/domain/services/analytics_service.dart';
import 'package:adhd_supplement_app/config/locator.dart';

class MockBillingServiceForTest implements BillingService {
  bool _isSubscribed = false;
  bool _shouldFailPurchase = false;
  bool _shouldFailRestore = false;
  bool _shouldThrowOnPurchase = false;
  bool _shouldThrowOnRestore = false;

  void setSubscribed(bool value) => _isSubscribed = value;
  void setShouldFailPurchase(bool value) => _shouldFailPurchase = value;
  void setShouldFailRestore(bool value) => _shouldFailRestore = value;
  void setShouldThrowOnPurchase(bool value) => _shouldThrowOnPurchase = value;
  void setShouldThrowOnRestore(bool value) => _shouldThrowOnRestore = value;

  @override
  Future<bool> initialize() async => true;

  @override
  Future<bool> get isSubscribed async => _isSubscribed;

  @override
  Future<bool> purchaseSubscription({required String planId}) async {
    if (_shouldThrowOnPurchase) {
      throw Exception('Purchase error');
    }
    if (_shouldFailPurchase) {
      return false;
    }
    _isSubscribed = true;
    return true;
  }

  @override
  Future<bool> restorePurchases() async {
    if (_shouldThrowOnRestore) {
      throw Exception('Restore error');
    }
    if (_shouldFailRestore) {
      return false;
    }
    _isSubscribed = true;
    return true;
  }
}

class MockAnalyticsService implements AnalyticsService {
  @override
  Future<void> logEvent(String name,
      {Map<String, dynamic>? parameters}) async {}
  @override
  Future<void> logScreenView(String screenName) async {}
  @override
  Future<void> setUserId(String userId) async {}
  @override
  Future<void> setUserProperty(String name, String value) async {}
}

void main() {
  late MockBillingServiceForTest mockBillingService;
  late MockAnalyticsService mockAnalyticsService;

  setUp(() {
    // Clear any existing registrations
    if (locator.isRegistered<BillingService>()) {
      locator.unregister<BillingService>();
    }
    if (locator.isRegistered<AnalyticsService>()) {
      locator.unregister<AnalyticsService>();
    }

    // Register mocks
    mockBillingService = MockBillingServiceForTest();
    mockAnalyticsService = MockAnalyticsService();
    locator.registerLazySingleton<BillingService>(() => mockBillingService);
    locator.registerLazySingleton<AnalyticsService>(() => mockAnalyticsService);
  });

  tearDown(() {
    // Clean up GetIt
    if (locator.isRegistered<BillingService>()) {
      locator.unregister<BillingService>();
    }
    if (locator.isRegistered<AnalyticsService>()) {
      locator.unregister<AnalyticsService>();
    }
  });

  group('SubscriptionViewModel', () {
    test('should initialize with correct initial state', () async {
      mockBillingService.setSubscribed(false);
      final viewModel = SubscriptionViewModel();

      // Wait for async initialization
      await Future<void>.delayed(const Duration(milliseconds: 100));

      expect(viewModel.isSubscribed, false);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
    });

    test('should initialize with subscribed state when user is subscribed',
        () async {
      mockBillingService.setSubscribed(true);
      final viewModel = SubscriptionViewModel();

      // Wait for async initialization
      await Future<void>.delayed(const Duration(milliseconds: 100));

      expect(viewModel.isSubscribed, true);
      expect(viewModel.isLoading, false);
      expect(viewModel.error, null);
    });

    test('purchaseSubscription should set loading state', () async {
      mockBillingService.setSubscribed(false);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      final purchaseFuture = viewModel.purchaseSubscription('plan1');

      // Check loading state immediately
      expect(viewModel.isLoading, true);

      await purchaseFuture;

      expect(viewModel.isLoading, false);
    });

    test('purchaseSubscription should update isSubscribed on success',
        () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldFailPurchase(false);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.purchaseSubscription('plan1');

      expect(viewModel.isSubscribed, true);
      expect(viewModel.error, null);
      expect(viewModel.isLoading, false);
    });

    test('purchaseSubscription should set error on failure', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldFailPurchase(true);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.purchaseSubscription('plan1');

      expect(viewModel.isSubscribed, false);
      expect(viewModel.error, 'Purchase failed. Please try again.');
      expect(viewModel.isLoading, false);
    });

    test('purchaseSubscription should handle exceptions', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldThrowOnPurchase(true);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.purchaseSubscription('plan1');

      expect(viewModel.isSubscribed, false);
      expect(viewModel.error, 'An error occurred during purchase.');
      expect(viewModel.isLoading, false);
    });

    test('restorePurchases should set loading state', () async {
      mockBillingService.setSubscribed(false);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      final restoreFuture = viewModel.restorePurchases();

      // Check loading state immediately
      expect(viewModel.isLoading, true);

      await restoreFuture;

      expect(viewModel.isLoading, false);
    });

    test('restorePurchases should update isSubscribed on success', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldFailRestore(false);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.restorePurchases();

      expect(viewModel.isSubscribed, true);
      expect(viewModel.error, null);
      expect(viewModel.isLoading, false);
    });

    test('restorePurchases should set error on failure', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldFailRestore(true);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.restorePurchases();

      expect(viewModel.isSubscribed, false);
      expect(viewModel.error, 'No purchases found to restore.');
      expect(viewModel.isLoading, false);
    });

    test('restorePurchases should handle exceptions', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldThrowOnRestore(true);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      await viewModel.restorePurchases();

      expect(viewModel.isSubscribed, false);
      expect(viewModel.error, 'An error occurred during restore.');
      expect(viewModel.isLoading, false);
    });

    test('should clear error on new purchase attempt', () async {
      mockBillingService.setSubscribed(false);
      mockBillingService.setShouldFailPurchase(true);
      final viewModel = SubscriptionViewModel();
      await Future<void>.delayed(const Duration(milliseconds: 100));

      // First purchase fails
      await viewModel.purchaseSubscription('plan1');
      expect(viewModel.error, isNotNull);

      // Second purchase clears error
      mockBillingService.setShouldFailPurchase(false);
      await viewModel.purchaseSubscription('plan2');
      expect(viewModel.error, null);
    });
  });
}

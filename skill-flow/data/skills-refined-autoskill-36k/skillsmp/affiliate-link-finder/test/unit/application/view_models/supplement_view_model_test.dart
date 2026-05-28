import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/application/view_models/supplement_view_model.dart';
import 'package:adhd_supplement_app/domain/repositories/supplement_repository.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/domain/services/analytics_service.dart';

@GenerateMocks([SupplementRepository, UrlService])
import 'supplement_view_model_test.mocks.dart';

class FakeAnalyticsService implements AnalyticsService {
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
  late SupplementViewModel viewModel;
  late MockSupplementRepository mockRepository;
  late MockUrlService mockUrlService;
  late FakeAnalyticsService mockAnalyticsService;

  final testSupplements = [
    const Supplement(
      id: '1',
      name: 'Omega-3',
      category: 'Vitamins',
      description: 'Test description',
      referralUrl: 'https://example.com/omega3',
    ),
  ];

  setUp(() {
    mockRepository = MockSupplementRepository();
    mockUrlService = MockUrlService();
    mockAnalyticsService = FakeAnalyticsService();

    // Default mock behavior for initial fetch
    when(mockRepository.getAllSupplements())
        .thenAnswer((_) async => testSupplements);
  });

  group('SupplementViewModel', () {
    test('initialization triggers supplement fetch', () async {
      viewModel = SupplementViewModel(
          mockRepository, mockUrlService, mockAnalyticsService);

      // Need to wait for the microtask/async fetch in constructor
      await Future<void>.delayed(Duration.zero);

      expect(viewModel.isLoading, isFalse);
      expect(viewModel.supplements, testSupplements);
      verify(mockRepository.getAllSupplements()).called(1);
    });

    test('fetch error sets error message', () async {
      when(mockRepository.getAllSupplements())
          .thenThrow(Exception('Network error'));

      viewModel = SupplementViewModel(
          mockRepository, mockUrlService, mockAnalyticsService);
      await Future<void>.delayed(Duration.zero);

      expect(viewModel.isLoading, isFalse);
      expect(viewModel.error, contains('Failed to load supplements'));
    });

    test('onReferralClicked tracks click and launches URL', () async {
      viewModel = SupplementViewModel(
          mockRepository, mockUrlService, mockAnalyticsService);
      await Future<void>.delayed(Duration.zero);

      final supplement = testSupplements.first;
      when(mockRepository.trackReferralClick(supplement.id))
          .thenAnswer((_) async => true);
      when(mockUrlService.launchReferral(supplement.referralUrl))
          .thenAnswer((_) async => true);

      await viewModel.onReferralClicked(supplement);

      verify(mockRepository.trackReferralClick(supplement.id)).called(1);
      verify(mockUrlService.launchReferral(supplement.referralUrl)).called(1);
    });
  });
}

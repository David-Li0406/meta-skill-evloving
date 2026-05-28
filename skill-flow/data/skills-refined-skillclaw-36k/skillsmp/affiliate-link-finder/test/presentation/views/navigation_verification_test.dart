import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:adhd_supplement_app/config/locator.dart';
import 'package:adhd_supplement_app/presentation/views/insights_screen.dart';
import 'package:adhd_supplement_app/presentation/views/science_hub_screen.dart';
import 'package:adhd_supplement_app/application/view_models/science_hub_view_model.dart';
import 'package:adhd_supplement_app/presentation/widgets/unified_bottom_nav.dart';
import 'package:adhd_supplement_app/domain/entities/article.dart';
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:adhd_supplement_app/application/view_models/insights_view_model.dart';

import 'package:adhd_supplement_app/domain/entities/faq_item.dart';
import 'package:adhd_supplement_app/domain/entities/study.dart';
import 'package:adhd_supplement_app/domain/entities/educational_article.dart';
import 'package:adhd_supplement_app/infrastructure/services/url_service.dart';

class MockAuthProvider extends ChangeNotifier implements AuthProvider {
  bool get isLoading => false;
  @override
  String? get errorMessage => null;
  @override
  bool get isAuthenticated => true;
  @override
  AuthStatus get status => AuthStatus.authenticated;
  @override
  User? get user => User(
        id: 'test-user',
        email: 'test@example.com',
        displayName: 'Test User',
        createdAt: DateTime.parse('2023-01-01'),
      );
  @override
  Future<void> signIn(String email, String password) async {}
  @override
  Future<void> signUp(
      String email, String password, String displayName) async {}
  @override
  Future<void> signOut() async {}
  @override
  Future<void> signInAnonymously() async {}
  @override
  Future<void> updateProfile(User user) async {}
}

class MockScienceHubViewModel extends ChangeNotifier
    implements ScienceHubViewModel {
  @override
  bool get isLoading => false;
  String? get error => null;
  @override
  Article? get articleOfTheDay => null;
  @override
  List<Article> get articles => [];

  @override
  String get searchQuery => '';
  @override
  bool get isSearching => false;
  @override
  void setSearchQuery(String query) {}

  @override
  List<FaqItem> get faqs => [];
  @override
  String get selectedFaqCategory => 'All';
  @override
  List<FaqItem> get filteredFaqs => [];
  @override
  void setFaqCategory(String category) {}

  @override
  List<Study> get studies => [];
  @override
  String get selectedResearchCategory => 'All';
  @override
  List<Study> get filteredStudies => [];
  @override
  void setResearchCategory(String category) {}

  @override
  List<EducationalArticle> get educationalArticles => [];
  @override
  String get selectedEduCategory => 'All';
  @override
  List<EducationalArticle> get filteredEduArticles => [];
  @override
  void setEduCategory(String category) {}

  @override
  Future<void> loadData() async {}
}

class MockInsightsViewModel extends ChangeNotifier
    implements InsightsViewModel {
  @override
  bool get isLoading => false;

  @override
  int get streakCount => 7;

  @override
  double get consistencyScore => 0.85;

  @override
  List<double> get weeklyFocusScores => [4.0, 5.0, 3.0, 4.0, 5.0, 4.0, 5.0];

  @override
  String get encouragementText => "You're doing great!";

  @override
  Future<void> loadData() async {}
}

class MockUrlService implements UrlService {
  @override
  Future<void> launchReferral(String url) async {}
  @override
  Future<void> launchUri(String url) async {}
  @override
  Future<void> launchInAppBrowser(String url) async {}
}

void main() {
  setUp(() {
    locator.reset();
    locator
        .registerFactory<ScienceHubViewModel>(() => MockScienceHubViewModel());
    locator.registerFactory<InsightsViewModel>(() => MockInsightsViewModel());
    locator.registerLazySingleton<UrlService>(() => MockUrlService());
  });

  testWidgets('InsightsScreen renders and has correct bottom nav index',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider<AuthProvider>(
            create: (_) => MockAuthProvider(),
          ),
        ],
        child: const MaterialApp(
          home: InsightsScreen(),
        ),
      ),
    );
    await tester.pump();

    final navFinder = find.byType(UnifiedBottomNav);
    expect(navFinder, findsOneWidget);

    final nav = tester.widget<UnifiedBottomNav>(navFinder);
    expect(nav.currentIndex, 4); // Insights is now index 4 (Profile)
  });

  testWidgets('ScienceHubScreen renders without crashing',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider<AuthProvider>(
            create: (_) => MockAuthProvider(),
          ),
        ],
        child: const MaterialApp(
          home: ScienceHubScreen(),
        ),
      ),
    );
    await tester.pump();
    expect(find.byType(Scaffold), findsOneWidget);
  });
}

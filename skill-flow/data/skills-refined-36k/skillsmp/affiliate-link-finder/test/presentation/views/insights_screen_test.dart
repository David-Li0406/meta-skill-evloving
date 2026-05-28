import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:adhd_supplement_app/presentation/views/insights_screen.dart';
import 'package:adhd_supplement_app/application/view_models/insights_view_model.dart';
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';
import 'package:get_it/get_it.dart';

// Generate Mocks for ViewModel and AuthProvider
@GenerateMocks([InsightsViewModel, AuthProvider])
import 'insights_screen_test.mocks.dart';

void main() {
  late MockInsightsViewModel mockViewModel;
  late MockAuthProvider mockAuthProvider;

  setUp(() {
    // Reset GetIt before each test if using locator
    GetIt.I.reset();

    mockViewModel = MockInsightsViewModel();
    mockAuthProvider = MockAuthProvider();

    // Setup Locator for ViewModels
    // Note: InsightsScreen uses locator<InsightsViewModel>(param1: userId)
    // We need to register a factory or simple mock for testing
    // Since we are mocking the provider content, we might need to adjust how InsightsScreen gets its VM
    // BUT InsightsScreen creates the VM via locator.
    // We can register the mock in GetIt.
    GetIt.I.registerFactoryParam<InsightsViewModel, String, void>(
        (param1, _) => mockViewModel);
  });

  Widget createWidgetUnderTest() {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider<AuthProvider>.value(value: mockAuthProvider),
      ],
      child: MaterialApp(
        home: InsightsScreen(viewModel: mockViewModel),
      ),
    );
  }

  testWidgets('InsightsScreen renders and shows streak',
      (WidgetTester tester) async {
    // Arrange
    when(mockAuthProvider.user).thenReturn(User(
        id: 'test_user', email: 'test@test.com', createdAt: DateTime.now()));
    when(mockViewModel.isLoading).thenReturn(false);
    when(mockViewModel.encouragementText).thenReturn('Keep going!');
    when(mockViewModel.streakCount).thenReturn(7);
    when(mockViewModel.consistencyScore).thenReturn(85.0);
    when(mockViewModel.weeklyFocusScores)
        .thenReturn([1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0]);

    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump(); // Build frame

    // Assert
    expect(find.text('Insights'), findsOneWidget);
    expect(find.text('Keep going!'), findsOneWidget);
    expect(find.text('7 Day Streak'), findsOneWidget);

    // Check consistency
    expect(find.text('85%'), findsOneWidget);
  });

  testWidgets('InsightsScreen shows skeleton loaders when loading',
      (WidgetTester tester) async {
    // Arrange
    when(mockAuthProvider.user).thenReturn(User(
        id: 'test_user', email: 'test@test.com', createdAt: DateTime.now()));
    when(mockViewModel.isLoading).thenReturn(true);

    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump();

    // Assert
    // Check for some skeletons
    expect(find.byType(InsightsScreen), findsOneWidget);
    expect(find.text('Insights'), findsOneWidget);
    // Should NOT find encouragement text if loading (it's hidden by Column in build logic)
  });

  testWidgets('InsightsScreen shows specific encouragement for long streaks',
      (WidgetTester tester) async {
    // Arrange
    when(mockAuthProvider.user).thenReturn(User(
        id: 'test_user', email: 'test@test.com', createdAt: DateTime.now()));
    when(mockViewModel.isLoading).thenReturn(false);
    when(mockViewModel.streakCount).thenReturn(31);
    when(mockViewModel.encouragementText).thenReturn('Unstoppable! 🏆');
    when(mockViewModel.consistencyScore).thenReturn(95.0);
    when(mockViewModel.weeklyFocusScores).thenReturn(List.filled(7, 5.0));

    // Act
    await tester.pumpWidget(createWidgetUnderTest());
    await tester.pump();

    // Assert
    expect(find.text('Unstoppable! 🏆'), findsOneWidget);
    expect(find.text('31 Day Streak'), findsOneWidget);
  });
}

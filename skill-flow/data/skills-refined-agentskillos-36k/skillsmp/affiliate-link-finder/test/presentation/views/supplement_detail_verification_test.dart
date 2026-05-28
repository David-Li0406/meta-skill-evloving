import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:adhd_supplement_app/presentation/views/supplement_detail.dart';
import 'package:adhd_supplement_app/domain/entities/supplement.dart';
import 'package:adhd_supplement_app/presentation/view_models/library_view_model.dart';
import 'package:adhd_supplement_app/application/providers/auth_provider.dart';
import 'package:adhd_supplement_app/config/locator.dart';
import 'package:mockito/mockito.dart';
import 'package:adhd_supplement_app/domain/entities/user.dart';

class MockLibraryViewModel extends Mock implements LibraryViewModel {}

class MockAuthProvider extends Mock implements AuthProvider {
  @override
  User? get user => User(
      id: 'test_user',
      email: 'test@example.com',
      displayName: 'Test',
      createdAt: DateTime.parse('2023-01-01'));
}

void main() {
  setUpAll(() {
    locator.registerFactoryParam<LibraryViewModel, String, void>(
      (userId, _) => MockLibraryViewModel(),
    );
  });

  tearDownAll(() {
    locator.reset();
  });

  testWidgets('SupplementDetailScreen displays rich intelligence data',
      (WidgetTester tester) async {
    const supplement = Supplement(
      id: 'test-id',
      name: 'Test Supplement',
      category: 'Test Category',
      description: 'Test Description',
      mechanismOfAction: 'This is how it works.',
      timingRationale: 'Take it in the morning.',
      detailedBenefits: ['Benefit A', 'Benefit B'],
      studyLinks: {'Study 1': 'http://example.com'},
      scientificEvidenceRank: 90,
    );

    await tester.pumpWidget(
      MultiProvider(
        providers: [
          ChangeNotifierProvider<AuthProvider>(
            create: (_) => MockAuthProvider(),
          ),
        ],
        child: const MaterialApp(
          home: SupplementDetail(supplement: supplement),
        ),
      ),
    );

    // Verify Mechanism of Action
    expect(find.text('Mechanism of Action'), findsOneWidget);
    expect(find.text('This is how it works.'), findsOneWidget);

    // Verify Timing Strategy
    expect(find.text('Timing Strategy'), findsOneWidget);
    expect(find.text('Take it in the morning.'), findsOneWidget);

    // Verify Detailed Benefits
    expect(find.text('ADHD Specific Benefits'), findsOneWidget);
    expect(find.text('Benefit A'), findsOneWidget);
    expect(find.text('Benefit B'), findsOneWidget);

    // Verify Scientific Evidence
    expect(find.text('Scientific Evidence'), findsOneWidget);
    expect(find.text('Study 1'), findsOneWidget);
  });
}

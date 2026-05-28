import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/views/quick_setup_wizard_screen.dart';

void main() {
  testWidgets('QuickSetupWizardScreen renders initial step',
      (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(
      home: QuickSetupWizardScreen(),
    ));

    // Verify Step 1 content
    expect(find.text('Quick Setup'), findsOneWidget);
    expect(find.text('What\'s your main goal?'), findsOneWidget);

    // Verify Goal options
    expect(find.text('Mental Clarity'), findsOneWidget);
    expect(find.text('Better Sleep'), findsOneWidget);
    expect(find.text('Energy Boost'), findsOneWidget);

    // Verify Next button initially exists
    expect(find.text('Next'), findsOneWidget);
  });

  testWidgets('Navigation through steps works', (WidgetTester tester) async {
    await tester.pumpWidget(const MaterialApp(
      home: QuickSetupWizardScreen(),
    ));

    // Select a goal
    await tester.tap(find.text('Mental Clarity'));
    await tester.pump();

    // Tap Next
    await tester.tap(find.text('Next'));
    await tester.pump();

    // Verify Step 2 (Stack Selection)
    expect(find.text('Choose a starter stack'), findsOneWidget);
    expect(find.text('Focus Stack'), findsOneWidget);
  });
}

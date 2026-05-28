import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/widgets/skeleton_loader.dart';

void main() {
  testWidgets('SkeletonLoader renders correctly', (WidgetTester tester) async {
    // Build the widget
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SkeletonLoader(
            width: 100,
            height: 20,
            borderRadius: 8,
          ),
        ),
      ),
    );

    // Verify it exists in the tree
    expect(find.byType(SkeletonLoader), findsOneWidget);
    expect(find.byType(Container), findsOneWidget);

    // Verify dimensions (indirectly via layout if needed, but existence is good for now)
  });

  testWidgets('SkeletonLoader animates', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SkeletonLoader(width: 100, height: 20),
        ),
      ),
    );

    // Advance time to verify ticker doesn't crash
    await tester.pump(const Duration(milliseconds: 500));
    await tester.pump(const Duration(milliseconds: 500));
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/widgets/skeleton_loader.dart';

void main() {
  group('SkeletonLoader', () {
    testWidgets('renders with correct dimensions', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: SkeletonLoader(width: 200, height: 50),
          ),
        ),
      );

      final containerFinder = find.byType(Container);
      expect(containerFinder, findsOneWidget);

      final container = tester.widget<Container>(containerFinder);
      expect(container.constraints?.maxWidth, 200);
      expect(container.constraints?.maxHeight, 50);
    });

    testWidgets('renders with correct border radius',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: SkeletonLoader(height: 50, borderRadius: 12),
          ),
        ),
      );

      final container = tester.widget<Container>(find.byType(Container));
      final decoration = container.decoration as BoxDecoration;
      expect(decoration.borderRadius, BorderRadius.circular(12));
    });

    testWidgets('animates gradient stops', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: SkeletonLoader(height: 50),
          ),
        ),
      );

      // Get initial stops
      final container1 = tester.widget<Container>(find.byType(Container));
      final gradient1 = container1.decoration as BoxDecoration;
      final stops1 = (gradient1.gradient as LinearGradient).stops!;

      // Advance time
      await tester.pump(const Duration(milliseconds: 500));

      // Get new stops
      final container2 = tester.widget<Container>(find.byType(Container));
      final gradient2 = container2.decoration as BoxDecoration;
      final stops2 = (gradient2.gradient as LinearGradient).stops!;

      // Compare stops - they should have changed due to animation
      expect(stops1, isNot(equals(stops2)));
    });
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:adhd_supplement_app/presentation/widgets/cached_image.dart';
import 'package:adhd_supplement_app/presentation/widgets/skeleton_loader.dart';
import 'package:cached_network_image/cached_network_image.dart';

void main() {
  group('CachedImage', () {
    testWidgets('renders SkeletonLoader when loading',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CachedImage(
              imageUrl: 'https://example.com/image.jpg',
              width: 100,
              height: 100,
            ),
          ),
        ),
      );

      // Initially, it should show the placeholder (SkeletonLoader)
      expect(find.byType(SkeletonLoader), findsOneWidget);

      final skeleton =
          tester.widget<SkeletonLoader>(find.byType(SkeletonLoader));
      expect(skeleton.width, 100);
      expect(skeleton.height, 100);
    });

    testWidgets('renders CachedNetworkImage with correct properties',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CachedImage(
              imageUrl: 'https://example.com/image.jpg',
              width: 200,
              height: 150,
              fit: BoxFit.contain,
              borderRadius: 15,
            ),
          ),
        ),
      );

      expect(find.byType(CachedNetworkImage), findsOneWidget);
      expect(find.byType(ClipRRect), findsOneWidget);

      final clipRRect = tester.widget<ClipRRect>(find.byType(ClipRRect));
      expect(clipRRect.borderRadius, BorderRadius.circular(15));

      final cachedImage =
          tester.widget<CachedNetworkImage>(find.byType(CachedNetworkImage));
      expect(cachedImage.imageUrl, 'https://example.com/image.jpg');
      expect(cachedImage.width, 200);
      expect(cachedImage.height, 150);
      expect(cachedImage.fit, BoxFit.contain);
    });

    testWidgets('renders custom placeholder when provided',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CachedImage(
              imageUrl: 'https://example.com/image.jpg',
              placeholder: Text('Loading...'),
            ),
          ),
        ),
      );

      expect(find.text('Loading...'), findsOneWidget);
      expect(find.byType(SkeletonLoader), findsNothing);
    });

    testWidgets('shows error widget when imageUrl is empty',
        (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: CachedImage(
              imageUrl: '',
            ),
          ),
        ),
      );

      expect(find.byIcon(Icons.broken_image_rounded), findsOneWidget);
    });
  });
}

#!/usr/bin/env python3
"""
Generate test file scaffolds for Flutter widgets, BLoCs, and services.

Usage:
    python generate_test.py --type widget --name AltitudeTape
    python generate_test.py --type bloc --name FlightPlan
    python generate_test.py --type service --name Weather
    python generate_test.py --type integration --name flight_planning
"""

import argparse
import os
from pathlib import Path
from datetime import datetime

WIDGET_TEST_TEMPLATE = '''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';
import 'package:magentaline/presentation/widgets/{snake_name}.dart';

void main() {{
  group('{class_name}', () {{
    testWidgets('renders correctly', (tester) async {{
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: {class_name}(),
          ),
        ),
      );

      // TODO: Add specific widget assertions
      expect(find.byType({class_name}), findsOneWidget);
    }});

    testWidgets('responds to user interaction', (tester) async {{
      var tapped = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: {class_name}(
              onTap: () => tapped = true,
            ),
          ),
        ),
      );

      await tester.tap(find.byType({class_name}));
      await tester.pump();

      expect(tapped, isTrue);
    }});

    testGoldens('{class_name} appearance', (tester) async {{
      await loadAppFonts();

      final builder = DeviceBuilder()
        ..overrideDevicesForAllScenarios(devices: [Device.phone, Device.tabletPortrait])
        ..addScenario(
          name: 'default',
          widget: const MaterialApp(
            home: Scaffold(body: {class_name}()),
          ),
        )
        ..addScenario(
          name: 'dark_theme',
          widget: MaterialApp(
            theme: ThemeData.dark(),
            home: const Scaffold(body: {class_name}()),
          ),
        );

      await tester.pumpDeviceBuilder(builder);
      await screenMatchesGolden(tester, '{snake_name}');
    }});
  }});
}}
'''

BLOC_TEST_TEMPLATE = '''import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:magentaline/domain/blocs/{snake_name}/{snake_name}_bloc.dart';
import 'package:magentaline/domain/repositories/{snake_name}_repository.dart';

class Mock{class_name}Repository extends Mock implements {class_name}Repository {{}}

void main() {{
  late Mock{class_name}Repository mockRepository;

  setUp(() {{
    mockRepository = Mock{class_name}Repository();
  }});

  group('{class_name}Bloc', () {{
    test('initial state is {class_name}Initial', () {{
      expect(
        {class_name}Bloc(repository: mockRepository).state,
        equals(const {class_name}Initial()),
      );
    }});

    blocTest<{class_name}Bloc, {class_name}State>(
      'emits [Loading, Loaded] when Load{class_name} succeeds',
      setUp: () {{
        when(() => mockRepository.get{class_name}(any()))
            .thenAnswer((_) async => /* test data */);
      }},
      build: () => {class_name}Bloc(repository: mockRepository),
      act: (bloc) => bloc.add(const Load{class_name}('id')),
      expect: () => [
        const {class_name}Loading(),
        isA<{class_name}Loaded>(),
      ],
    );

    blocTest<{class_name}Bloc, {class_name}State>(
      'emits [Loading, Error] when Load{class_name} fails',
      setUp: () {{
        when(() => mockRepository.get{class_name}(any()))
            .thenThrow(Exception('Failed to load'));
      }},
      build: () => {class_name}Bloc(repository: mockRepository),
      act: (bloc) => bloc.add(const Load{class_name}('id')),
      expect: () => [
        const {class_name}Loading(),
        isA<{class_name}Error>(),
      ],
    );

    blocTest<{class_name}Bloc, {class_name}State>(
      'calls repository with correct parameters',
      setUp: () {{
        when(() => mockRepository.get{class_name}(any()))
            .thenAnswer((_) async => /* test data */);
      }},
      build: () => {class_name}Bloc(repository: mockRepository),
      act: (bloc) => bloc.add(const Load{class_name}('test_id')),
      verify: (_) {{
        verify(() => mockRepository.get{class_name}('test_id')).called(1);
      }},
    );
  }});
}}
'''

SERVICE_TEST_TEMPLATE = '''import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:magentaline/data/services/{snake_name}_service.dart';

class MockHttpClient extends Mock implements HttpClient {{}}

void main() {{
  late {class_name}Service service;
  late MockHttpClient mockHttpClient;

  setUp(() {{
    mockHttpClient = MockHttpClient();
    service = {class_name}Service(httpClient: mockHttpClient);
  }});

  group('{class_name}Service', () {{
    group('get{class_name}', () {{
      test('returns data when API call succeeds', () async {{
        when(() => mockHttpClient.get(any())).thenAnswer(
          (_) async => Response(/* mock response */),
        );

        final result = await service.get{class_name}('id');

        expect(result, isNotNull);
        // TODO: Add specific assertions
      }});

      test('throws exception when API call fails', () async {{
        when(() => mockHttpClient.get(any()))
            .thenThrow(Exception('Network error'));

        expect(
          () => service.get{class_name}('id'),
          throwsException,
        );
      }});

      test('parses response correctly', () async {{
        when(() => mockHttpClient.get(any())).thenAnswer(
          (_) async => Response(body: '{{"key": "value"}}'),
        );

        final result = await service.get{class_name}('id');

        // TODO: Add parsing assertions
      }});
    }});

    group('caching', () {{
      test('returns cached data within TTL', () async {{
        when(() => mockHttpClient.get(any())).thenAnswer(
          (_) async => Response(/* mock response */),
        );

        // First call
        await service.get{class_name}('id');
        // Second call should use cache
        await service.get{class_name}('id');

        verify(() => mockHttpClient.get(any())).called(1);
      }});
    }});
  }});
}}
'''

INTEGRATION_TEST_TEMPLATE = '''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:magentaline/main.dart' as app;

void main() {{
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('{name} flow', () {{
    testWidgets('complete {name} flow', (tester) async {{
      app.main();
      await tester.pumpAndSettle();

      // Step 1: Navigate to {name} screen
      // TODO: Implement navigation
      // await tester.tap(find.byIcon(Icons.xxx));
      // await tester.pumpAndSettle();

      // Step 2: Enter data
      // TODO: Implement data entry
      // await tester.enterText(find.byKey(Key('field')), 'value');
      // await tester.pumpAndSettle();

      // Step 3: Submit
      // TODO: Implement submission
      // await tester.tap(find.byKey(Key('submit')));
      // await tester.pumpAndSettle();

      // Step 4: Verify result
      // TODO: Add assertions
      // expect(find.text('Success'), findsOneWidget);
    }});

    testWidgets('handles error state', (tester) async {{
      app.main();
      await tester.pumpAndSettle();

      // TODO: Test error handling
    }});

    testWidgets('works offline', (tester) async {{
      app.main();
      await tester.pumpAndSettle();

      // TODO: Test offline functionality
    }});
  }});
}}
'''


def to_snake_case(name: str) -> str:
    """Convert CamelCase to snake_case."""
    result = []
    for i, char in enumerate(name):
        if char.isupper() and i > 0:
            result.append('_')
        result.append(char.lower())
    return ''.join(result)


def generate_test(test_type: str, name: str, output_dir: str = None):
    """Generate a test file based on type."""

    templates = {
        'widget': WIDGET_TEST_TEMPLATE,
        'bloc': BLOC_TEST_TEMPLATE,
        'service': SERVICE_TEST_TEMPLATE,
        'integration': INTEGRATION_TEST_TEMPLATE,
    }

    if test_type not in templates:
        print(f"Unknown test type: {test_type}")
        print(f"Available types: {', '.join(templates.keys())}")
        return

    snake_name = to_snake_case(name)

    content = templates[test_type].format(
        class_name=name,
        snake_name=snake_name,
        name=name.lower().replace('_', ' '),
    )

    # Determine output path
    if output_dir:
        base_path = Path(output_dir)
    else:
        base_path = Path('test')

    if test_type == 'widget':
        file_path = base_path / 'widgets' / f'{snake_name}_test.dart'
    elif test_type == 'bloc':
        file_path = base_path / 'blocs' / f'{snake_name}_bloc_test.dart'
    elif test_type == 'service':
        file_path = base_path / 'services' / f'{snake_name}_service_test.dart'
    elif test_type == 'integration':
        file_path = Path('integration_test') / f'{snake_name}_test.dart'

    # Create directory if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path.write_text(content)
    print(f"Created: {file_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate Flutter test scaffolds')
    parser.add_argument('--type', '-t', required=True,
                        choices=['widget', 'bloc', 'service', 'integration'],
                        help='Type of test to generate')
    parser.add_argument('--name', '-n', required=True,
                        help='Name of the class/feature to test (CamelCase)')
    parser.add_argument('--output', '-o',
                        help='Output directory (default: test/)')

    args = parser.parse_args()
    generate_test(args.type, args.name, args.output)


if __name__ == '__main__':
    main()

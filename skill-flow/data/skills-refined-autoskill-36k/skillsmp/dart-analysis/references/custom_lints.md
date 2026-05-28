# Custom Lint Rules

## Setup with custom_lint

### Package Structure

```
packages/
└── magentaline_lints/
    ├── lib/
    │   ├── magentaline_lints.dart
    │   └── src/
    │       ├── avoid_print_in_production.dart
    │       ├── require_test_coverage_annotation.dart
    │       └── aviation_calculation_checks.dart
    ├── pubspec.yaml
    └── analysis_options.yaml
```

### pubspec.yaml

```yaml
name: magentaline_lints
description: Custom lint rules for MagentaLine EFB

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  analyzer: ^6.0.0
  analyzer_plugin: ^0.11.0
  custom_lint_builder: ^0.5.0
```

### Main Entry Point

```dart
// lib/magentaline_lints.dart
import 'package:custom_lint_builder/custom_lint_builder.dart';

import 'src/avoid_print_in_production.dart';
import 'src/require_test_coverage_annotation.dart';
import 'src/aviation_calculation_checks.dart';

PluginBase createPlugin() => _MagentaLineLints();

class _MagentaLineLints extends PluginBase {
  @override
  List<LintRule> getLintRules(CustomLintConfigs configs) => [
    AvoidPrintInProduction(),
    RequireTestCoverageAnnotation(),
    AviationCalculationChecks(),
  ];
}
```

## Example Custom Rules

### Avoid Print in Production

```dart
// lib/src/avoid_print_in_production.dart
import 'package:analyzer/dart/ast/ast.dart';
import 'package:analyzer/error/listener.dart';
import 'package:custom_lint_builder/custom_lint_builder.dart';

class AvoidPrintInProduction extends DartLintRule {
  AvoidPrintInProduction() : super(code: _code);

  static const _code = LintCode(
    name: 'avoid_print_in_production',
    problemMessage: 'Avoid using print() in production code. '
        'Use a logging framework instead.',
    correctionMessage: 'Replace with Logger.d() or remove.',
  );

  @override
  void run(
    CustomLintResolver resolver,
    ErrorReporter reporter,
    CustomLintContext context,
  ) {
    context.registry.addMethodInvocation((node) {
      if (node.methodName.name == 'print') {
        // Allow in test files
        if (resolver.source.uri.path.contains('test/')) return;

        reporter.reportErrorForNode(_code, node);
      }
    });
  }

  @override
  List<Fix> getFixes() => [_RemovePrintFix()];
}

class _RemovePrintFix extends DartFix {
  @override
  void run(
    CustomLintResolver resolver,
    ChangeReporter reporter,
    CustomLintContext context,
    AnalysisError analysisError,
    List<AnalysisError> others,
  ) {
    context.registry.addMethodInvocation((node) {
      if (!analysisError.sourceRange.intersects(node.sourceRange)) return;

      final changeBuilder = reporter.createChangeBuilder(
        message: 'Remove print statement',
        priority: 1,
      );

      changeBuilder.addDartFileEdit((builder) {
        builder.addDeletion(node.parent!.sourceRange);
      });
    });
  }
}
```

### Require Test Coverage Annotation

```dart
// lib/src/require_test_coverage_annotation.dart
import 'package:analyzer/dart/ast/ast.dart';
import 'package:analyzer/error/listener.dart';
import 'package:custom_lint_builder/custom_lint_builder.dart';

/// Ensures safety-critical functions have @testCoverage annotation
class RequireTestCoverageAnnotation extends DartLintRule {
  RequireTestCoverageAnnotation() : super(code: _code);

  static const _code = LintCode(
    name: 'require_test_coverage_annotation',
    problemMessage: 'Safety-critical functions must have @testCoverage annotation.',
    correctionMessage: 'Add @testCoverage(100) annotation.',
  );

  static const _safetyCriticalPaths = [
    'lib/domain/navigation/',
    'lib/domain/calculations/',
    'lib/data/parsers/',
  ];

  @override
  void run(
    CustomLintResolver resolver,
    ErrorReporter reporter,
    CustomLintContext context,
  ) {
    final path = resolver.source.uri.path;

    // Only check safety-critical paths
    if (!_safetyCriticalPaths.any((p) => path.contains(p))) return;

    context.registry.addFunctionDeclaration((node) {
      if (_isMissingCoverageAnnotation(node)) {
        reporter.reportErrorForNode(_code, node.name);
      }
    });

    context.registry.addMethodDeclaration((node) {
      if (_isMissingCoverageAnnotation(node)) {
        reporter.reportErrorForNode(_code, node.name);
      }
    });
  }

  bool _isMissingCoverageAnnotation(AnnotatedNode node) {
    return !node.metadata.any(
      (annotation) => annotation.name.name == 'testCoverage',
    );
  }
}
```

### Aviation Calculation Checks

```dart
// lib/src/aviation_calculation_checks.dart
import 'package:analyzer/dart/ast/ast.dart';
import 'package:analyzer/error/listener.dart';
import 'package:custom_lint_builder/custom_lint_builder.dart';

/// Checks for common aviation calculation mistakes
class AviationCalculationChecks extends DartLintRule {
  AviationCalculationChecks() : super(code: _latLonRangeCode);

  static const _latLonRangeCode = LintCode(
    name: 'lat_lon_range_check',
    problemMessage: 'Latitude/longitude values should be validated.',
    correctionMessage: 'Add range validation: lat [-90, 90], lon [-180, 180].',
  );

  static const _headingNormalizationCode = LintCode(
    name: 'heading_normalization',
    problemMessage: 'Heading calculations should normalize to [0, 360).',
    correctionMessage: 'Use heading % 360 or normalizeHeading().',
  );

  @override
  void run(
    CustomLintResolver resolver,
    ErrorReporter reporter,
    CustomLintContext context,
  ) {
    context.registry.addMethodInvocation((node) {
      // Check for direct degree/radian conversions without normalization
      if (_isUnnormalizedAngleConversion(node)) {
        reporter.reportErrorForNode(_headingNormalizationCode, node);
      }
    });

    context.registry.addFunctionDeclaration((node) {
      // Check functions handling lat/lon without validation
      if (_handlesCoordinatesWithoutValidation(node)) {
        reporter.reportErrorForNode(_latLonRangeCode, node.name);
      }
    });
  }

  bool _isUnnormalizedAngleConversion(MethodInvocation node) {
    // Detect patterns like: degrees * pi / 180 without modulo
    // This is a simplified check - real implementation would be more thorough
    return false; // Implement detection logic
  }

  bool _handlesCoordinatesWithoutValidation(FunctionDeclaration node) {
    // Check if function parameters named lat/lon/latitude/longitude
    // are used without validation
    return false; // Implement detection logic
  }
}
```

## Using Custom Lints

### Add to Project

```yaml
# pubspec.yaml
dev_dependencies:
  custom_lint: ^0.5.0
  magentaline_lints:
    path: packages/magentaline_lints
```

```yaml
# analysis_options.yaml
analyzer:
  plugins:
    - custom_lint
```

### Run Custom Lints

```bash
# Run analyzer with custom lints
dart run custom_lint

# With auto-fix
dart run custom_lint --fix
```

## Test Coverage Annotation Definition

```dart
// lib/annotations/test_coverage.dart

/// Annotation to document expected test coverage percentage
class TestCoverage {
  final int percentage;
  final String? notes;

  const TestCoverage(this.percentage, {this.notes});
}

const testCoverage = TestCoverage;

// Usage:
@TestCoverage(100, notes: 'Critical navigation function')
double haversineDistance(double lat1, double lon1, double lat2, double lon2) {
  // ...
}
```

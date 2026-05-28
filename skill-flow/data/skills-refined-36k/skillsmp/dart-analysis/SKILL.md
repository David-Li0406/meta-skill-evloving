---
name: dart-analysis
description: Dart static analysis and linting for aviation-grade code quality. Use when configuring analysis_options.yaml, enforcing strict type safety, creating custom lint rules, or setting up code metrics for Flutter projects. Includes aviation-specific safety patterns and recommended rule sets for safety-critical applications.
---

# Dart Analysis

## Overview

Static analysis configuration for MagentaLine EFB with aviation-grade code quality standards.

## Quick Start

### Strict Analysis Setup

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    missing_return: error
    missing_required_param: error
    must_be_immutable: error
    invalid_use_of_protected_member: error
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "build/**"
    - ".dart_tool/**"

linter:
  rules:
    # Error Prevention
    - always_use_package_imports
    - avoid_dynamic_calls
    - avoid_slow_async_io
    - cancel_subscriptions
    - close_sinks
    - literal_only_boolean_expressions
    - no_adjacent_strings_in_list
    - throw_in_finally
    - unnecessary_statements

    # Type Safety
    - avoid_types_as_parameter_names
    - avoid_return_types_on_setters
    - prefer_typing_uninitialized_variables
    - type_annotate_public_apis

    # Aviation Safety Critical
    - invariant_booleans
    - avoid_double_and_int_checks
    - use_is_even_rather_than_modulo
```

## Aviation Safety Rules

For safety-critical aviation code, enable strict analysis:

```yaml
analyzer:
  errors:
    # Treat these as errors, not warnings
    dead_code: error
    unused_element: error
    unused_import: error
    unused_local_variable: error

    # Safety-critical
    always_require_non_null_named_parameters: error
    avoid_null_checks_in_equality_operators: error
    null_check_on_nullable_type_parameter: error
```

## Running Analysis

```bash
# Run analyzer
dart analyze

# With specific options
dart analyze --fatal-infos --fatal-warnings

# Generate machine-readable output
dart analyze --format=machine > analysis.txt

# Fix auto-fixable issues
dart fix --apply
```

## Code Metrics

See `references/code_metrics.md` for metrics thresholds.

```bash
# Install dart_code_metrics
dart pub global activate dart_code_metrics

# Run metrics analysis
dart pub global run dart_code_metrics:metrics analyze lib

# Generate HTML report
dart pub global run dart_code_metrics:metrics analyze lib --reporter=html

# Check against thresholds
dart pub global run dart_code_metrics:metrics analyze lib \
  --set-exit-on-violation-level=warning
```

### Recommended Thresholds

| Metric | Threshold | Description |
|--------|-----------|-------------|
| Cyclomatic Complexity | ≤10 | Paths through code |
| Lines of Code | ≤50 | Per function |
| Number of Parameters | ≤4 | Per function |
| Maximum Nesting | ≤4 | Nested blocks |
| Maintainability Index | ≥40 | Overall maintainability |

## Custom Lint Rules

See `references/custom_lints.md` for creating project-specific rules.

```yaml
# pubspec.yaml
dev_dependencies:
  custom_lint: ^0.5.0
  magentaline_lints:
    path: packages/magentaline_lints
```

## Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running Dart analysis..."
dart analyze --fatal-warnings
if [ $? -ne 0 ]; then
  echo "Analysis failed. Fix issues before committing."
  exit 1
fi

echo "Checking formatting..."
dart format --set-exit-if-changed lib test
if [ $? -ne 0 ]; then
  echo "Format issues found. Run 'dart format lib test'"
  exit 1
fi
```

## IDE Integration

### VS Code

```json
// .vscode/settings.json
{
  "dart.analysisExcludedFolders": [
    "build",
    ".dart_tool"
  ],
  "dart.lineLength": 100,
  "editor.formatOnSave": true,
  "[dart]": {
    "editor.defaultFormatter": "Dart-Code.dart-code",
    "editor.rulers": [80, 100]
  }
}
```

## References

| Document | Description |
|----------|-------------|
| `references/code_metrics.md` | Metrics configuration and thresholds |
| `references/custom_lints.md` | Creating custom lint rules |
| `references/analysis_rules.md` | Complete rule reference |
| `assets/analysis_options.yaml` | Ready-to-use strict config |

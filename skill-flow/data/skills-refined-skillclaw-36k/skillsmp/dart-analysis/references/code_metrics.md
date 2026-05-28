# Dart Code Metrics

## Installation

```bash
dart pub global activate dart_code_metrics
```

## Configuration

```yaml
# analysis_options.yaml
dart_code_metrics:
  metrics:
    cyclomatic-complexity: 10
    lines-of-code: 50
    maintainability-index: 40
    maximum-nesting-level: 4
    number-of-methods: 10
    number-of-parameters: 4
    source-lines-of-code: 40
    technical-debt:
      threshold: 1
      todo-cost: 4
      ignore-cost: 8
      ignore-for-file-cost: 16
      as-dynamic-cost: 8
      deprecated-annotations-cost: 2
      file-nullsafety-migration-cost: 2
      unit-type: "hours"

  metrics-exclude:
    - test/**
    - "**/*.g.dart"
    - "**/*.freezed.dart"

  rules:
    # Common
    - avoid-collection-methods-with-unrelated-types
    - avoid-dynamic
    - avoid-global-state
    - avoid-late-keyword
    - avoid-missing-enum-constant-in-map
    - avoid-nested-conditional-expressions
    - avoid-non-null-assertion
    - avoid-throw-in-catch-block
    - avoid-unnecessary-type-assertions
    - avoid-unnecessary-type-casts
    - avoid-unrelated-type-assertions
    - binary-expression-operand-order
    - double-literal-format
    - member-ordering:
        order:
          - public-fields
          - private-fields
          - constructors
          - public-methods
          - private-methods
    - newline-before-return
    - no-boolean-literal-compare
    - no-empty-block
    - no-equal-then-else
    - no-magic-number:
        allowed: [0, 1, -1, 2, 100, 360, 90, 180, 270]
        allowed-in-widget-params: true
    - no-object-declaration
    - prefer-async-await
    - prefer-commenting-analyzer-ignores
    - prefer-conditional-expressions
    - prefer-correct-edge-insets-constructor
    - prefer-correct-type-name
    - prefer-enums-by-name
    - prefer-first
    - prefer-immediate-return
    - prefer-iterable-of
    - prefer-last
    - prefer-moving-to-variable
    - prefer-trailing-comma

    # Flutter specific
    - always-remove-listener
    - avoid-border-all
    - avoid-expanded-as-spacer
    - avoid-returning-widgets
    - avoid-shrink-wrap-in-lists
    - avoid-unnecessary-setstate
    - avoid-wrapping-in-padding
    - check-for-equals-in-render-object-setters
    - consistent-update-render-object
    - prefer-const-border-radius
    - prefer-correct-edge-insets-constructor
    - prefer-extracting-callbacks
    - prefer-single-widget-per-file:
        ignore-private-widgets: true
    - prefer-using-list-view
    - use-setstate-synchronously

  anti-patterns:
    - long-method
    - long-parameter-list
```

## Running Metrics

```bash
# Basic analysis
dart pub global run dart_code_metrics:metrics analyze lib

# With specific rules
dart pub global run dart_code_metrics:metrics analyze lib \
  --set-exit-on-violation-level=warning

# Generate reports
dart pub global run dart_code_metrics:metrics analyze lib --reporter=html
dart pub global run dart_code_metrics:metrics analyze lib --reporter=json > metrics.json
dart pub global run dart_code_metrics:metrics analyze lib --reporter=github

# Check unused code
dart pub global run dart_code_metrics:metrics check-unused-code lib

# Check unused files
dart pub global run dart_code_metrics:metrics check-unused-files lib

# Check unnecessary nullable
dart pub global run dart_code_metrics:metrics check-unnecessary-nullable lib
```

## Metric Thresholds for Aviation Software

### Cyclomatic Complexity

| Level | Value | Action |
|-------|-------|--------|
| Low | 1-5 | Acceptable |
| Moderate | 6-10 | Review needed |
| High | 11-20 | Refactor required |
| Very High | >20 | **Must refactor** |

**Aviation standard**: Navigation math functions may have higher complexity but must have 100% test coverage.

### Lines of Code (LOC)

| Component | Limit | Notes |
|-----------|-------|-------|
| Function | 50 | Prefer smaller |
| Class | 300 | Split large classes |
| File | 500 | Use feature folders |

### Maintainability Index

| Range | Rating |
|-------|--------|
| 0-9 | Very Low |
| 10-19 | Low |
| 20-39 | Moderate |
| 40-100 | High |

**Target for MagentaLine**: All code ≥40

## CI Integration

```yaml
# .github/workflows/metrics.yml
name: Code Metrics

on: [push, pull_request]

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: dart-lang/setup-dart@v1

      - name: Install dependencies
        run: dart pub get

      - name: Install metrics
        run: dart pub global activate dart_code_metrics

      - name: Run metrics
        run: |
          dart pub global run dart_code_metrics:metrics analyze lib \
            --reporter=github \
            --set-exit-on-violation-level=warning

      - name: Check unused code
        run: dart pub global run dart_code_metrics:metrics check-unused-code lib

      - name: Generate report
        run: dart pub global run dart_code_metrics:metrics analyze lib --reporter=html

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: metrics-report
          path: metrics/
```

## Metrics for Safety-Critical Code

Navigation and flight planning code requires stricter limits:

```yaml
dart_code_metrics:
  metrics:
    cyclomatic-complexity: 8  # Stricter for safety code
    maximum-nesting-level: 3
    number-of-parameters: 3

  rules:
    # Mandatory for aviation code
    - avoid-dynamic  # No dynamic typing
    - avoid-late-keyword  # No late initialization
    - avoid-non-null-assertion  # No null assertions
    - no-magic-number  # Named constants only
```

## Sample Output

```
lib/domain/navigation/haversine.dart:
  Function: calculateDistance
    Cyclomatic Complexity: 4 (OK)
    Lines of Code: 25 (OK)
    Maintainability Index: 72 (High)

lib/presentation/widgets/map_display.dart:
  Class: MapDisplayWidget
    Number of Methods: 12 (Warning: exceeds 10)
    Source Lines of Code: 180 (OK)

lib/data/repositories/airport_repository.dart:
  Function: searchNearby
    Maximum Nesting Level: 5 (Warning: exceeds 4)
    Cyclomatic Complexity: 14 (Error: exceeds 10)
```

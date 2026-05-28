---
name: "Code Quality Gates"
description: "Quality gate patterns including dart analysis, test coverage, build validation, and compliance checks"
version: "1.0.0"
---

# Code Quality Gates

## Gate 1: Dart Analysis

```bash
flutter analyze
```

**Pass criteria**: 0 errors

**Configuration** (`analysis_options.yaml`):
```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  
  errors:
    invalid_annotation_target: ignore
    
linter:
  rules:
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - avoid_print
    - avoid_unnecessary_containers
    - prefer_single_quotes
    - sort_child_properties_last
```

## Gate 2: Test Coverage

```bash
# Run tests with coverage
flutter test --coverage

# Generate HTML report
genhtml coverage/lcov.info -o coverage/html

# Check coverage percentage
lcov --summary coverage/lcov.info
```

**Pass criteria**: ≥ 80% line coverage

**Validation script**:
```bash
#!/bin/bash
COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | grep -oP '\d+\.\d+')

if (( $(echo "$COVERAGE >= 80.0" | bc -l) )); then
  echo "✅ Coverage: $COVERAGE% (PASSED)"
  exit 0
else
  echo "❌ Coverage: $COVERAGE% (FAILED - requires ≥ 80%)"
  exit 1
fi
```

## Gate 3: Build Validation

```bash
# Debug build
flutter build apk --debug

# Release build (for production)
flutter build apk --release
```

**Pass criteria**: Build succeeds without errors

## Gate 4: GetX Compliance

### Check 1: Controllers use bindings
```bash
# Find controllers instantiated directly (anti-pattern)
grep -r "Get.put<.*Controller>" lib/presentation/pages/

# Should return 0 results (use bindings instead)
```

### Check 2: Reactive variables use .obs
```bash
# Find reactive state declarations
grep -r "\.obs" lib/presentation/controllers/

# Verify all state is reactive
```

### Check 3: Business logic in use cases
```bash
# Controllers should NOT call repositories directly
grep -r "Repository" lib/presentation/controllers/

# Should return 0 results
```

## Gate 5: Clean Architecture Compliance

### Check 1: Domain layer purity
```bash
# Domain should not import Flutter
grep -r "package:flutter" lib/domain/

# Should return 0 results
```

### Check 2: Domain should not import GetX
```bash
grep -r "package:get" lib/domain/

# Should return 0 results
```

### Check 3: Dependency flow validation
```bash
# Data can import domain (OK)
grep -r "import.*domain/" lib/data/

# Presentation can import data (OK)
grep -r "import.*data/" lib/presentation/

# Domain CANNOT import data or presentation
grep -r "import.*\(data\|presentation\)/" lib/domain/

# Should return 0 results
```

## Automated Quality Gate Script

```bash
#!/bin/bash

echo "🔍 Running Quality Gates..."

# Gate 1: Dart Analysis
echo ""
echo "Gate 1: Dart Analysis"
flutter analyze
if [ $? -ne 0 ]; then
  echo "❌ Dart analysis failed"
  exit 1
fi
echo "✅ Dart analysis passed"

# Gate 2: Test Coverage
echo ""
echo "Gate 2: Test Coverage"
flutter test --coverage
COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | grep -oP '\d+\.\d+')
if (( $(echo "$COVERAGE < 80.0" | bc -l) )); then
  echo "❌ Coverage: $COVERAGE% (requires ≥ 80%)"
  exit 1
fi
echo "✅ Coverage: $COVERAGE%"

# Gate 3: Build Validation
echo ""
echo "Gate 3: Build Validation"
flutter build apk --debug > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "❌ Build failed"
  exit 1
fi
echo "✅ Build succeeded"

# Gate 4: GetX Compliance
echo ""
echo "Gate 4: GetX Compliance"
if grep -r "Get.put<.*Controller>" lib/presentation/pages/ > /dev/null 2>&1; then
  echo "❌ Controllers instantiated directly (use bindings)"
  exit 1
fi
echo "✅ GetX compliance passed"

# Gate 5: Clean Architecture
echo ""
echo "Gate 5: Clean Architecture"
if grep -r "package:flutter\|package:get" lib/domain/ > /dev/null 2>&1; then
  echo "❌ Domain layer not pure"
  exit 1
fi
echo "✅ Clean Architecture validated"

echo ""
echo "🎉 All quality gates passed!"
```

## CI/CD Integration

```yaml
# .github/workflows/quality_gates.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Run dart analyze
      run: flutter analyze
    
    - name: Run tests with coverage
      run: flutter test --coverage
    
    - name: Check coverage
      run: |
        sudo apt-get install lcov
        COVERAGE=$(lcov --summary coverage/lcov.info 2>&1 | grep "lines" | grep -oP '\d+\.\d+')
        if (( $(echo "$COVERAGE < 80.0" | bc -l) )); then
          echo "Coverage $COVERAGE% is below 80%"
          exit 1
        fi
    
    - name: Build APK
      run: flutter build apk --debug
```

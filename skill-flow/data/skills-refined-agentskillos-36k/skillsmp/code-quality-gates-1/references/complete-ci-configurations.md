# Code Quality Gates — Complete CI Configurations

> **Loading Trigger**: Load when setting up CI/CD pipelines or configuring quality gates.

---

## Complete GitHub Actions Workflow

```yaml
# .github/workflows/quality-gates.yml

name: Quality Gates

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  XCODE_VERSION: '15.2'
  SCHEME: 'MyApp'
  SIMULATOR: 'iPhone 15'

jobs:
  # ========================================
  # Stage 1: Fast Quality Checks
  # ========================================
  lint:
    name: Lint & Format
    runs-on: macos-14
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Install Tools
        run: |
          brew install swiftlint swiftformat

      - name: SwiftLint
        run: |
          swiftlint lint --strict --reporter github-actions-logging

      - name: SwiftFormat Check
        run: |
          swiftformat . --lint --verbose

  # ========================================
  # Stage 2: Build (depends on lint)
  # ========================================
  build:
    name: Build
    needs: lint
    runs-on: macos-14
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_${{ env.XCODE_VERSION }}.app

      - name: Restore SPM Cache
        uses: actions/cache@v4
        with:
          path: |
            ~/Library/Developer/Xcode/DerivedData/**/SourcePackages
            .build
          key: ${{ runner.os }}-spm-${{ hashFiles('**/Package.resolved') }}
          restore-keys: |
            ${{ runner.os }}-spm-

      - name: Build for Testing
        run: |
          set -o pipefail
          xcodebuild build-for-testing \
            -scheme "${{ env.SCHEME }}" \
            -destination "platform=iOS Simulator,name=${{ env.SIMULATOR }}" \
            -derivedDataPath DerivedData \
            SWIFT_TREAT_WARNINGS_AS_ERRORS=YES \
            GCC_TREAT_WARNINGS_AS_ERRORS=YES \
            | xcpretty --color

      - name: Upload Build Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: derived-data
          path: DerivedData
          retention-days: 1

  # ========================================
  # Stage 3: Tests (depends on build)
  # ========================================
  test:
    name: Test
    needs: build
    runs-on: macos-14
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_${{ env.XCODE_VERSION }}.app

      - name: Download Build Artifacts
        uses: actions/download-artifact@v4
        with:
          name: derived-data
          path: DerivedData

      - name: Run Tests
        run: |
          set -o pipefail
          xcodebuild test-without-building \
            -scheme "${{ env.SCHEME }}" \
            -destination "platform=iOS Simulator,name=${{ env.SIMULATOR }}" \
            -derivedDataPath DerivedData \
            -enableCodeCoverage YES \
            -resultBundlePath TestResults.xcresult \
            | xcpretty --color --report junit

      - name: Check Coverage Threshold
        run: |
          COVERAGE=$(xcrun xccov view --report --json TestResults.xcresult | \
            jq '[.targets[] | select(.name | contains("${{ env.SCHEME }}")) | .lineCoverage] | add * 100')

          echo "Code Coverage: ${COVERAGE}%"

          THRESHOLD=80
          if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
            echo "❌ Coverage ${COVERAGE}% is below threshold ${THRESHOLD}%"
            exit 1
          else
            echo "✅ Coverage ${COVERAGE}% meets threshold ${THRESHOLD}%"
          fi

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: |
            TestResults.xcresult
            build/reports/junit.xml

      - name: Publish Test Results
        uses: dorny/test-reporter@v1
        if: always()
        with:
          name: Test Results
          path: build/reports/junit.xml
          reporter: java-junit

  # ========================================
  # Stage 4: Security Scan (parallel with test)
  # ========================================
  security:
    name: Security Scan
    needs: build
    runs-on: macos-14
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4

      - name: Run Swift Dependency Audit
        run: |
          # Check for known vulnerabilities in dependencies
          swift package audit 2>/dev/null || echo "No audit tool available"

      - name: Check for Hardcoded Secrets
        run: |
          # Simple secret detection
          ! grep -rn --include='*.swift' \
            -e 'api_key\s*=' \
            -e 'password\s*=' \
            -e 'secret\s*=' \
            --exclude-dir='.git' \
            --exclude-dir='DerivedData' \
            . || {
              echo "⚠️ Potential hardcoded secrets detected"
              exit 1
            }

  # ========================================
  # Final: PR Status Check
  # ========================================
  quality-gate:
    name: Quality Gate
    needs: [lint, build, test, security]
    runs-on: ubuntu-latest
    if: always()
    steps:
      - name: Check All Jobs
        run: |
          if [[ "${{ needs.lint.result }}" != "success" ]] || \
             [[ "${{ needs.build.result }}" != "success" ]] || \
             [[ "${{ needs.test.result }}" != "success" ]] || \
             [[ "${{ needs.security.result }}" != "success" ]]; then
            echo "❌ Quality gate failed"
            exit 1
          fi
          echo "✅ All quality gates passed"
```

---

## Complete SwiftLint Configuration

```yaml
# .swiftlint.yml

# ============================================
# Paths
# ============================================
excluded:
  - Pods
  - .build
  - DerivedData
  - vendor
  - Carthage
  - "**/*.generated.swift"
  - "**/*+Generated.swift"

included:
  - Sources
  - Tests
  - App

# ============================================
# Core Rules Configuration
# ============================================
line_length:
  warning: 120
  error: 200
  ignores_urls: true
  ignores_function_declarations: true
  ignores_comments: true
  ignores_interpolated_strings: true

file_length:
  warning: 500
  error: 800
  ignore_comment_only_lines: true

type_body_length:
  warning: 300
  error: 400

function_body_length:
  warning: 50
  error: 80

cyclomatic_complexity:
  warning: 10
  error: 15
  ignores_case_statements: true

nesting:
  type_level: 3
  function_level: 3

identifier_name:
  min_length:
    warning: 2
    error: 1
  max_length:
    warning: 50
    error: 60
  excluded:
    - id
    - x
    - y
    - z
    - i
    - j
    - k
    - to
    - ok
    - db

# ============================================
# Opt-In Rules (Explicitly Enabled)
# ============================================
opt_in_rules:
  # Safety
  - force_unwrapping
  - implicitly_unwrapped_optional
  - unowned_variable_capture
  - fatal_error_message

  # Performance
  - empty_count
  - first_where
  - last_where
  - contains_over_first_not_nil
  - contains_over_filter_count
  - contains_over_filter_is_empty
  - flatmap_over_map_reduce
  - reduce_boolean
  - sorted_first_last

  # Code Style
  - array_init
  - closure_end_indentation
  - closure_spacing
  - collection_alignment
  - conditional_returns_on_newline
  - empty_string
  - explicit_init
  - extension_access_modifier
  - file_name_no_space
  - literal_expression_end_indentation
  - multiline_arguments
  - multiline_parameters
  - operator_usage_whitespace
  - overridden_super_call
  - prefer_self_type_over_type_of_self
  - prefer_zero_over_explicit_init
  - redundant_nil_coalescing
  - redundant_type_annotation
  - single_test_class
  - toggle_bool
  - trailing_closure
  - unavailable_function
  - unneeded_parentheses_in_closure_argument
  - vertical_parameter_alignment_on_call
  - yoda_condition

  # Documentation
  - missing_docs

# ============================================
# Disabled Rules
# ============================================
disabled_rules:
  # Too noisy
  - todo
  - trailing_whitespace  # SwiftFormat handles this

  # Preference varies by team
  - opening_brace
  - statement_position

# ============================================
# Analyzer Rules
# ============================================
analyzer_rules:
  - unused_import
  - unused_declaration

# ============================================
# Custom Rules
# ============================================
custom_rules:
  no_print_in_release:
    name: "No print() in release"
    regex: '^\s*print\s*\('
    message: "Use Logger instead of print() for release builds"
    severity: warning
    match_kinds:
      - identifier

  no_force_try:
    name: "No force try"
    regex: 'try!'
    message: "Avoid force try - handle errors properly"
    severity: error

  no_nslog:
    name: "No NSLog"
    regex: 'NSLog\s*\('
    message: "Use Logger instead of NSLog"
    severity: warning
```

---

## Complete SwiftFormat Configuration

```ini
# .swiftformat

# ============================================
# Swift Version & Paths
# ============================================
--swiftversion 5.9
--exclude Pods,.build,DerivedData,vendor,Carthage,**/*.generated.swift

# ============================================
# Formatting Rules
# ============================================
--indent 4
--tabwidth 4
--maxwidth 120
--indentcase false
--trimwhitespace always
--insertlines 1
--removelines 1

# ============================================
# Wrapping
# ============================================
--wraparguments before-first
--wrapparameters before-first
--wrapcollections before-first
--wrapreturntype preserve
--closingparen balanced

# ============================================
# Spacing
# ============================================
--operatorfunc spaced
--nospaceoperators ...,..<
--ranges spaced
--typedelimiter spaced

# ============================================
# Braces & Declarations
# ============================================
--allman false
--elseposition same-line
--guardelse next-line
--emptybraces no-space
--funcattributes prev-line
--typeattributes prev-line
--varattributes same-line

# ============================================
# Imports
# ============================================
--importgrouping alpha

# ============================================
# Self
# ============================================
--self remove
--selfrequired

# ============================================
# Other
# ============================================
--semicolons never
--commas always
--decimalgrouping 3
--binarygrouping 4,8
--octalgrouping 4,8
--hexgrouping 4,8
--fractiongrouping disabled
--exponentgrouping disabled
--hexliteralcase uppercase
--exponentcase lowercase
--header strip
--ifdef no-indent

# ============================================
# Rules - Enabled
# ============================================
--enable sortedImports
--enable trailingCommas
--enable redundantSelf
--enable redundantReturn
--enable redundantObjc
--enable redundantLet
--enable redundantNilInit
--enable redundantVoidReturnType
--enable blankLinesAtEndOfScope
--enable blankLinesAtStartOfScope
--enable blankLinesBetweenScopes
--enable consecutiveSpaces
--enable duplicateImports
--enable emptyBraces
--enable hoistPatternLet
--enable leadingDelimiters
--enable linebreakAtEndOfFile
--enable modifierOrder
--enable preferKeyPath
--enable redundantBackticks
--enable redundantBreak
--enable redundantExtensionACL
--enable redundantFileprivate
--enable redundantGet
--enable redundantInit
--enable redundantParens
--enable redundantPattern
--enable redundantRawValues
--enable spaceAroundBraces
--enable spaceAroundBrackets
--enable spaceAroundComments
--enable spaceAroundGenerics
--enable spaceAroundOperators
--enable spaceAroundParens
--enable spaceInsideBraces
--enable spaceInsideBrackets
--enable spaceInsideComments
--enable spaceInsideGenerics
--enable spaceInsideParens
--enable strongOutlets
--enable strongifiedSelf
--enable todos
--enable trailingClosures
--enable trailingSpace
--enable unusedArguments
--enable void
--enable wrapArguments
--enable wrapAttributes
--enable yodaConditions

# ============================================
# Rules - Disabled
# ============================================
--disable acronyms
--disable wrapMultilineStatementBraces
--disable sortedSwitchCases
--disable markTypes
--disable organizeDeclarations
```

---

## Pre-commit and Post-commit Hooks

```bash
#!/bin/bash
# .git/hooks/pre-commit

set -e

echo "🔍 Running pre-commit quality checks..."

# ============================================
# Stage 1: SwiftLint (fast)
# ============================================
echo "📋 Running SwiftLint..."
if command -v swiftlint &> /dev/null; then
    swiftlint lint --strict --quiet || {
        echo "❌ SwiftLint found issues. Please fix before committing."
        exit 1
    }
else
    echo "⚠️  SwiftLint not installed, skipping..."
fi

# ============================================
# Stage 2: SwiftFormat (fast)
# ============================================
echo "🎨 Checking code formatting..."
if command -v swiftformat &> /dev/null; then
    swiftformat . --lint --quiet || {
        echo "❌ Code formatting issues found."
        echo "Run 'swiftformat .' to fix automatically."
        exit 1
    }
else
    echo "⚠️  SwiftFormat not installed, skipping..."
fi

# ============================================
# Stage 3: Check for debug code
# ============================================
echo "🐛 Checking for debug code..."
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.swift$' || true)

if [ -n "$STAGED_FILES" ]; then
    # Check for print statements
    if echo "$STAGED_FILES" | xargs grep -l "print(" 2>/dev/null | grep -v "Tests" | grep -v "Debug"; then
        echo "⚠️  Warning: print() statements found in non-test files"
        # Not blocking, just warning
    fi

    # Check for TODO/FIXME
    TODO_COUNT=$(echo "$STAGED_FILES" | xargs grep -c "TODO\|FIXME" 2>/dev/null | awk -F: '{sum += $2} END {print sum}' || echo "0")
    if [ "$TODO_COUNT" -gt "0" ]; then
        echo "📝 Note: Found $TODO_COUNT TODO/FIXME comments"
    fi
fi

echo "✅ Pre-commit checks passed!"
```

```bash
#!/bin/bash
# .git/hooks/post-commit

# ============================================
# Optional: Run tests after commit
# ============================================
# Uncomment to run tests after every commit (can be slow)
# echo "🧪 Running tests..."
# xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' -quiet

echo "📦 Commit complete!"
```

---

## Makefile for Quality Commands

```makefile
# Makefile

.PHONY: setup lint format test coverage clean

# ============================================
# Setup
# ============================================
setup:
	@echo "📦 Installing dependencies..."
	brew install swiftlint swiftformat xcbeautify
	@echo "🔗 Setting up git hooks..."
	cp .github/hooks/* .git/hooks/
	chmod +x .git/hooks/*
	@echo "✅ Setup complete!"

# ============================================
# Quality Gates
# ============================================
lint:
	@echo "📋 Running SwiftLint..."
	swiftlint lint --strict

format:
	@echo "🎨 Formatting code..."
	swiftformat .

format-check:
	@echo "🎨 Checking code format..."
	swiftformat . --lint

# ============================================
# Testing
# ============================================
test:
	@echo "🧪 Running tests..."
	xcodebuild test \
		-scheme $(SCHEME) \
		-destination 'platform=iOS Simulator,name=iPhone 15' \
		-enableCodeCoverage YES \
		| xcbeautify

coverage:
	@echo "📊 Generating coverage report..."
	xcodebuild test \
		-scheme $(SCHEME) \
		-destination 'platform=iOS Simulator,name=iPhone 15' \
		-enableCodeCoverage YES \
		-resultBundlePath TestResults.xcresult
	xcrun xccov view --report TestResults.xcresult

# ============================================
# CI Pipeline (local)
# ============================================
ci: lint format-check test coverage
	@echo "✅ All quality gates passed!"

# ============================================
# Cleanup
# ============================================
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf DerivedData
	rm -rf TestResults.xcresult
	xcodebuild clean -scheme $(SCHEME)
```

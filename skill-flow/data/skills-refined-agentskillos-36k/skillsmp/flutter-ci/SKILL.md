---
name: flutter-ci
description: CI/CD pipelines for Flutter applications. Use when setting up GitHub Actions, GitLab CI, or other build automation for Flutter projects. Includes test workflows, build matrix configurations, artifact management, and release automation for both iOS and Android.
---

# Flutter CI/CD

## Overview

Complete CI/CD pipeline configuration for MagentaLine EFB with GitHub Actions.

## Quick Start

### Basic CI Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter analyze --fatal-infos

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test --coverage
      - uses: codecov/codecov-action@v4
        with:
          files: coverage/lcov.info

  build:
    needs: [analyze, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter build apk --release
```

## Pipeline Stages

### 1. Analysis

```yaml
analyze:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - uses: subosito/flutter-action@v2
      with:
        channel: stable
        cache: true

    - name: Get dependencies
      run: flutter pub get

    - name: Analyze code
      run: flutter analyze --fatal-infos --fatal-warnings

    - name: Check formatting
      run: dart format --set-exit-if-changed lib test

    - name: Run dart_code_metrics
      run: |
        dart pub global activate dart_code_metrics
        dart pub global run dart_code_metrics:metrics analyze lib \
          --reporter=github \
          --set-exit-on-violation-level=warning
```

### 2. Testing

```yaml
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - uses: subosito/flutter-action@v2
      with:
        channel: stable
        cache: true

    - run: flutter pub get

    - name: Run unit and widget tests
      run: flutter test --coverage --reporter=github

    - name: Check coverage threshold
      run: |
        COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | sed 's/%//')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Coverage $COVERAGE% is below 80% threshold"
          exit 1
        fi

    - name: Upload coverage
      uses: codecov/codecov-action@v4
      with:
        files: coverage/lcov.info
        fail_ci_if_error: true
```

### 3. Build Matrix

```yaml
build:
  needs: [analyze, test]
  strategy:
    matrix:
      include:
        - os: ubuntu-latest
          target: apk
          artifact: build/app/outputs/flutter-apk/app-release.apk
        - os: ubuntu-latest
          target: appbundle
          artifact: build/app/outputs/bundle/release/app-release.aab
        - os: macos-latest
          target: ios
          artifact: build/ios/ipa/*.ipa

  runs-on: ${{ matrix.os }}

  steps:
    - uses: actions/checkout@v4

    - uses: subosito/flutter-action@v2

    - name: Setup signing (Android)
      if: matrix.target == 'apk' || matrix.target == 'appbundle'
      run: |
        echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > android/app/upload-keystore.jks
        cat > android/key.properties << EOF
        storePassword=${{ secrets.STORE_PASSWORD }}
        keyPassword=${{ secrets.KEY_PASSWORD }}
        keyAlias=magentaline
        storeFile=upload-keystore.jks
        EOF

    - name: Build
      run: flutter build ${{ matrix.target }} --release

    - uses: actions/upload-artifact@v4
      with:
        name: ${{ matrix.target }}-release
        path: ${{ matrix.artifact }}
```

## Release Workflow

See `references/release_workflow.md` for complete release automation.

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - uses: subosito/flutter-action@v2

      - name: Build all platforms
        run: |
          flutter build apk --release
          flutter build appbundle --release

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            build/app/outputs/flutter-apk/app-release.apk
            build/app/outputs/bundle/release/app-release.aab
          generate_release_notes: true
```

## Caching

```yaml
- uses: subosito/flutter-action@v2
  with:
    channel: stable
    cache: true
    cache-key: flutter-${{ runner.os }}-${{ hashFiles('pubspec.lock') }}

- name: Cache pub dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.pub-cache
      .dart_tool
    key: pub-${{ runner.os }}-${{ hashFiles('pubspec.lock') }}
    restore-keys: pub-${{ runner.os }}-

- name: Cache Gradle
  if: runner.os == 'Linux'
  uses: actions/cache@v4
  with:
    path: |
      ~/.gradle/caches
      ~/.gradle/wrapper
    key: gradle-${{ hashFiles('android/gradle/wrapper/gradle-wrapper.properties') }}

- name: Cache CocoaPods
  if: runner.os == 'macOS'
  uses: actions/cache@v4
  with:
    path: ios/Pods
    key: pods-${{ hashFiles('ios/Podfile.lock') }}
```

## Pull Request Workflow

```yaml
# .github/workflows/pr.yml
name: PR Check

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  pr-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter analyze
      - run: dart format --set-exit-if-changed lib test
      - run: flutter test

      - name: Comment coverage
        uses: romeovs/lcov-reporter-action@v0.4.0
        with:
          lcov-file: coverage/lcov.info
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

## Secrets Management

Required secrets for CI:

| Secret | Purpose |
|--------|---------|
| `KEYSTORE_BASE64` | Android signing keystore |
| `STORE_PASSWORD` | Keystore password |
| `KEY_PASSWORD` | Key password |
| `MATCH_PASSWORD` | iOS Fastlane Match |
| `ASC_KEY_ID` | App Store Connect API |
| `PLAY_STORE_JSON` | Google Play service account |

## Branch Protection

Recommended settings for `main`:
- Require PR reviews
- Require status checks: `analyze`, `test`
- Require branches to be up to date
- Require signed commits (optional)

## References

| Document | Description |
|----------|-------------|
| `references/release_workflow.md` | Complete release automation |
| `references/secrets_setup.md` | CI secrets configuration |
| `assets/ci.yml` | Ready-to-use CI workflow |
| `assets/release.yml` | Release workflow template |

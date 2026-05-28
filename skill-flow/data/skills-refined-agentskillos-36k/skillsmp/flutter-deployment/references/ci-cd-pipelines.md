# CI/CD Pipelines for Flutter

Complete guide to implementing continuous integration and continuous deployment for Flutter applications across all platforms.

## Overview

CI/CD (Continuous Integration/Continuous Deployment) automates building, testing, and deploying Flutter apps. This reduces manual work, catches bugs early, ensures consistent builds, and enables rapid iteration. This guide covers popular CI/CD platforms, configuration examples, and best practices for Flutter deployment automation.

## CI/CD Benefits

### Continuous Integration (CI)

- Automated testing on every commit
- Early bug detection
- Consistent build environment
- Parallel testing across platforms
- Code quality checks

### Continuous Deployment (CD)

- Automated app store submissions
- Faster release cycles
- Reduced human error
- Reproducible deployments
- Rollback capabilities

## Platform Overview

| Platform | Best For | Pricing | Flutter Support |
|----------|----------|---------|----------------|
| **GitHub Actions** | GitHub projects | Free tier + paid | Excellent |
| **Codemagic** | Flutter-specific | Free tier + paid | Native |
| **Bitrise** | Mobile apps | Free tier + paid | Excellent |
| **GitLab CI** | GitLab projects | Free tier + paid | Good |
| **CircleCI** | General purpose | Free tier + paid | Good |
| **Azure Pipelines** | Microsoft ecosystem | Free tier + paid | Good |
| **Fastlane** | Local + any CI | Free | Excellent (plugin) |

## GitHub Actions

### Advantages

- Native GitHub integration
- Free for public repos, generous free tier for private
- Matrix builds for multiple platforms
- Large marketplace of actions
- Self-hosted runners supported

### Basic Workflow

Create `.github/workflows/build.yml`:

```yaml
name: Flutter CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'

      - name: Install dependencies
        run: flutter pub get

      - name: Analyze code
        run: flutter analyze

      - name: Run tests
        run: flutter test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage/lcov.info

  build-android:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'

      - name: Decode keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > android/app/keystore.jks

      - name: Create key.properties
        run: |
          cat <<EOF > android/key.properties
          storePassword=${{ secrets.KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.KEY_PASSWORD }}
          keyAlias=${{ secrets.KEY_ALIAS }}
          storeFile=keystore.jks
          EOF

      - name: Build APK
        run: flutter build apk --release

      - name: Build App Bundle
        run: flutter build appbundle --release

      - uses: actions/upload-artifact@v3
        with:
          name: android-release
          path: |
            build/app/outputs/apk/release/*.apk
            build/app/outputs/bundle/release/*.aab

  build-ios:
    needs: test
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - name: Install CocoaPods
        run: |
          cd ios
          pod install

      - name: Build iOS
        run: flutter build ios --release --no-codesign

      - uses: actions/upload-artifact@v3
        with:
          name: ios-release
          path: build/ios/iphoneos/*.app

  deploy-android:
    needs: build-android
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - uses: actions/download-artifact@v3
        with:
          name: android-release

      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT }}
          packageName: com.example.myapp
          releaseFiles: bundle/release/app-release.aab
          track: internal
          status: completed
```

### Matrix Strategy for Multiple Platforms

```yaml
jobs:
  build:
    strategy:
      matrix:
        platform: [android, ios, web]
        include:
          - platform: android
            os: ubuntu-latest
            build-cmd: flutter build apk --release
          - platform: ios
            os: macos-latest
            build-cmd: flutter build ios --release --no-codesign
          - platform: web
            os: ubuntu-latest
            build-cmd: flutter build web --release

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: ${{ matrix.build-cmd }}
```

### Flavor-Specific Builds

```yaml
jobs:
  build-flavors:
    strategy:
      matrix:
        flavor: [dev, staging, prod]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter build apk --flavor ${{ matrix.flavor }} --release

      - uses: actions/upload-artifact@v3
        with:
          name: android-${{ matrix.flavor }}
          path: build/app/outputs/apk/${{ matrix.flavor }}/release/*.apk
```

### Caching Dependencies

```yaml
- name: Cache Flutter dependencies
  uses: actions/cache@v3
  with:
    path: |
      ~/.pub-cache
      **/.flutter-plugins
      **/.flutter-plugin-dependencies
    key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
    restore-keys: |
      ${{ runner.os }}-pub-
```

## Codemagic

### Advantages

- Flutter-native platform
- Built-in app store integrations
- Automatic code signing for iOS
- No configuration for simple projects
- Excellent Mac build machines

### Using codemagic.yaml

Create `codemagic.yaml` in project root:

```yaml
workflows:
  android-workflow:
    name: Android Workflow
    max_build_duration: 60
    environment:
      flutter: stable
      xcode: latest
      groups:
        - keystore_credentials
      vars:
        PACKAGE_NAME: "com.example.myapp"
    scripts:
      - name: Set up key.properties
        script: |
          cat > "$CM_BUILD_DIR/android/key.properties" <<EOF
          storePassword=$KEYSTORE_PASSWORD
          keyPassword=$KEY_PASSWORD
          keyAlias=$KEY_ALIAS
          storeFile=/tmp/keystore.jks
          EOF

      - name: Set up keystore
        script: |
          echo $KEYSTORE_BASE64 | base64 --decode > /tmp/keystore.jks

      - name: Get dependencies
        script: |
          flutter packages pub get

      - name: Build AAB
        script: |
          flutter build appbundle --release

    artifacts:
      - build/**/outputs/**/*.aab
      - build/**/outputs/**/mapping.txt

    publishing:
      email:
        recipients:
          - team@example.com
      google_play:
        credentials: $GOOGLE_PLAY_SERVICE_ACCOUNT
        track: internal
        submit_as_draft: true

  ios-workflow:
    name: iOS Workflow
    max_build_duration: 60
    environment:
      flutter: stable
      xcode: latest
      cocoapods: default
      groups:
        - app_store_credentials
      vars:
        BUNDLE_ID: "com.example.myapp"
        APP_STORE_ID: 1234567890
    scripts:
      - name: Set up code signing
        script: |
          keychain initialize
          app-store-connect fetch-signing-files "$BUNDLE_ID" \
            --type IOS_APP_STORE \
            --create
          keychain add-certificates
          xcode-project use-profiles

      - name: Get dependencies
        script: |
          flutter packages pub get
          cd ios && pod install

      - name: Build IPA
        script: |
          flutter build ipa --release \
            --export-options-plist=$HOME/export_options.plist

    artifacts:
      - build/ios/ipa/*.ipa
      - /tmp/xcodebuild_logs/*.log

    publishing:
      app_store_connect:
        api_key: $APP_STORE_CONNECT_PRIVATE_KEY
        key_id: $APP_STORE_CONNECT_KEY_IDENTIFIER
        issuer_id: $APP_STORE_CONNECT_ISSUER_ID
        submit_to_testflight: true
        beta_groups:
          - Internal Testers
        submit_to_app_store: false
```

### Automatic iOS Code Signing

Codemagic can automatically manage iOS certificates:

```yaml
environment:
  groups:
    - app_store_credentials  # Contains API key
  ios_signing:
    distribution_type: app_store
    bundle_identifier: com.example.myapp
```

Codemagic creates certificates and provisioning profiles automatically.

### Web Deployment

```yaml
workflows:
  web-workflow:
    name: Web Workflow
    environment:
      flutter: stable
    scripts:
      - flutter pub get
      - flutter build web --release

    artifacts:
      - build/web/**

    publishing:
      firebase_hosting:
        project: your-firebase-project
        site: your-site-id
```

## Fastlane

### Advantages

- Works with any CI platform
- Powerful Ruby-based DSL
- Extensive plugin ecosystem
- Local testing before CI
- Mature and stable

### Setup

```bash
# Install
sudo gem install fastlane

# Initialize for Android
cd android
fastlane init

# Initialize for iOS
cd ios
fastlane init
```

### Android Fastfile

`android/fastlane/Fastfile`:

```ruby
default_platform(:android)

platform :android do
  desc "Build and upload to Play Store internal track"
  lane :internal do
    # Build the app bundle
    gradle(
      task: "bundle",
      build_type: "Release",
      print_command: false,
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_PATH"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"],
      }
    )

    # Upload to Play Store
    upload_to_play_store(
      track: 'internal',
      aab: '../build/app/outputs/bundle/release/app-release.aab',
      skip_upload_screenshots: true,
      skip_upload_images: true,
      skip_upload_metadata: true
    )
  end

  desc "Build and upload to Play Store beta track"
  lane :beta do
    gradle(
      task: "bundle",
      build_type: "Release"
    )

    upload_to_play_store(
      track: 'beta',
      aab: '../build/app/outputs/bundle/release/app-release.aab'
    )
  end

  desc "Promote internal to beta"
  lane :promote_to_beta do
    upload_to_play_store(
      track: 'internal',
      track_promote_to: 'beta',
      skip_upload_changelogs: true
    )
  end
end
```

### iOS Fastfile

`ios/fastlane/Fastfile`:

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    # Set up code signing
    setup_ci if is_ci

    match(
      type: "appstore",
      readonly: is_ci,
      keychain_name: "fastlane_keychain",
      keychain_password: ENV["MATCH_PASSWORD"]
    )

    # Increment build number
    increment_build_number(
      xcodeproj: "Runner.xcodeproj",
      build_number: latest_testflight_build_number + 1
    )

    # Build the app
    build_app(
      scheme: "Runner",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    # Upload to TestFlight
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      apple_id: ENV["APPLE_ID"],
      team_id: ENV["TEAM_ID"],
      groups: ["Internal Testers"]
    )
  end

  desc "Deploy to App Store"
  lane :release do
    build_app(
      scheme: "Runner",
      export_method: "app-store"
    )

    upload_to_app_store(
      submit_for_review: true,
      automatic_release: false,
      skip_screenshots: true,
      skip_metadata: false
    )
  end
end
```

### Using Fastlane in GitHub Actions

```yaml
jobs:
  deploy-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true

      - uses: subosito/flutter-action@v2

      - name: Flutter build
        run: flutter build ios --release --no-codesign

      - name: Deploy with Fastlane
        run: |
          cd ios
          bundle exec fastlane beta
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_AUTH }}
          APPLE_ID: ${{ secrets.APPLE_ID }}
```

## GitLab CI

### Configuration

Create `.gitlab-ci.yml`:

```yaml
stages:
  - test
  - build
  - deploy

variables:
  FLUTTER_VERSION: "3.38.6"

before_script:
  - apt-get update -qq && apt-get install -y -qq git curl unzip
  - git clone https://github.com/flutter/flutter.git -b stable --depth 1
  - export PATH="$PATH:`pwd`/flutter/bin"
  - flutter doctor

test:
  stage: test
  script:
    - flutter pub get
    - flutter analyze
    - flutter test --coverage

build-android:
  stage: build
  script:
    - echo "$KEYSTORE_BASE64" | base64 -d > android/app/keystore.jks
    - |
      cat <<EOF > android/key.properties
      storePassword=$KEYSTORE_PASSWORD
      keyPassword=$KEY_PASSWORD
      keyAlias=$KEY_ALIAS
      storeFile=keystore.jks
      EOF
    - flutter build appbundle --release
  artifacts:
    paths:
      - build/app/outputs/bundle/release/app-release.aab
    expire_in: 1 week

deploy-android:
  stage: deploy
  dependencies:
    - build-android
  script:
    - echo "Deploy to Play Store"
    # Add deployment script
  only:
    - main
```

## CircleCI

### Configuration

Create `.circleci/config.yml`:

```yaml
version: 2.1

orbs:
  flutter: circleci/flutter@2.0.0

workflows:
  build-and-deploy:
    jobs:
      - flutter/test:
          sdk-version: "3.38.6"

      - flutter/build-android:
          sdk-version: "3.38.6"
          requires:
            - flutter/test

      - flutter/build-ios:
          sdk-version: "3.38.6"
          xcode-version: "14.2.0"
          requires:
            - flutter/test
```

## Best Practices

### Security

**Secrets Management:**
- Never commit secrets to repository
- Use CI platform's secret management
- Rotate secrets regularly
- Limit secret access to necessary jobs

**Example (GitHub Actions):**
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
  KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
```

### Build Optimization

**Caching:**
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.pub-cache
    key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
```

**Parallel Jobs:**
```yaml
jobs:
  test:
    # Fast feedback
  build-android:
    needs: test
    # Parallel with build-ios
  build-ios:
    needs: test
    # Parallel with build-android
```

**Incremental Builds:**
- Use build caches
- Only rebuild changed modules
- Skip unnecessary steps

### Testing

**Test Pyramid:**
```yaml
- run: flutter test                     # Unit tests
- run: flutter test integration_test/   # Integration tests
- run: flutter drive --target=test_driver/app.dart  # E2E tests
```

**Coverage:**
```yaml
- run: flutter test --coverage
- uses: codecov/codecov-action@v3
  with:
    files: coverage/lcov.info
```

### Versioning

**Automatic Version Bumping:**
```bash
# Increment build number
flutter build apk --build-number=$GITHUB_RUN_NUMBER
```

**Semantic Versioning:**
```ruby
# Fastlane
increment_version_number(
  bump_type: "patch"  # or "minor" or "major"
)
```

### Notifications

**Slack Integration:**
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  if: always()
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

**Email Notifications:**
```yaml
publishing:
  email:
    recipients:
      - team@example.com
    notify:
      success: true
      failure: true
```

### Deployment Strategies

**Staged Rollouts:**
```ruby
upload_to_play_store(
  track: 'production',
  rollout: '0.1'  # 10% rollout
)
```

**Blue-Green Deployment:**
- Deploy to staging environment
- Run smoke tests
- Switch traffic to new version
- Keep old version for quick rollback

**Canary Releases:**
- Deploy to small percentage of users
- Monitor metrics
- Gradually increase percentage
- Rollback if issues detected

## Troubleshooting

### Build Timeouts

**Solutions:**
- Optimize build steps
- Use caching effectively
- Upgrade CI plan for more resources
- Split into smaller jobs

### Code Signing Failures

**Solutions:**
- Verify certificates are valid
- Check provisioning profiles
- Ensure credentials are correct
- Use fastlane match for consistency

### Flaky Tests

**Solutions:**
- Identify non-deterministic tests
- Mock external dependencies
- Use retry mechanisms
- Increase timeouts for slow tests

## Quick Reference

### GitHub Actions

```yaml
# Basic Flutter workflow
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test
      - run: flutter build apk --release
```

### Codemagic

```yaml
workflows:
  default-workflow:
    environment:
      flutter: stable
    scripts:
      - flutter pub get
      - flutter test
      - flutter build apk --release
```

### Fastlane

```bash
# Setup
fastlane init

# Run lane
fastlane android beta
fastlane ios beta
```

## Resources

- [GitHub Actions for Flutter](https://github.com/marketplace/actions/flutter-action)
- [Codemagic Documentation](https://docs.codemagic.io/flutter/)
- [Fastlane Documentation](https://docs.fastlane.tools/)
- [Flutter CI/CD Guide](https://docs.flutter.dev/deployment/cd)

## Summary

CI/CD automation is essential for professional Flutter development, enabling faster releases, better quality, and reduced manual work. GitHub Actions provides excellent free tier and native GitHub integration. Codemagic offers Flutter-native experience with minimal configuration. Fastlane provides powerful cross-platform automation that works with any CI system. Choose the platform that best fits your project needs, team size, and budget. Implement proper secret management, optimize builds with caching, test thoroughly at every stage, and use staged rollouts for production deployments. A well-configured CI/CD pipeline pays dividends in productivity and app quality over the lifetime of your project.

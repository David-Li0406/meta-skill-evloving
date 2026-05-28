# Complete CI/CD Workflow Example

A production-ready CI/CD workflow example for a Flutter app with multiple flavors, comprehensive testing, and automated deployment to both iOS and Android app stores.

## Project Context

**App:** E-commerce Flutter application
**Flavors:** dev, staging, production
**Platforms:** iOS, Android, Web
**CI/CD:** GitHub Actions
**Testing:** Unit, widget, and integration tests
**Deployment:** TestFlight, Google Play Internal Testing, Firebase Hosting

## Repository Structure

```
my-flutter-app/
├── .github/
│   └── workflows/
│       ├── pr-checks.yml
│       ├── deploy-dev.yml
│       ├── deploy-staging.yml
│       └── deploy-production.yml
├── lib/
├── test/
├── integration_test/
├── android/
├── ios/
├── web/
├── fastlane/
│   ├── Fastfile
│   └── Appfile
└── pubspec.yaml
```

## Pull Request Checks Workflow

**File:** `.github/workflows/pr-checks.yml`

Runs on every pull request to ensure code quality.

```yaml
name: Pull Request Checks

on:
  pull_request:
    branches: [ develop, main ]

jobs:
  analyze:
    name: Analyze Code
    runs-on: ubuntu-latest
    timeout-minutes: 10

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Verify formatting
        run: dart format --output=none --set-exit-if-changed .

      - name: Analyze project
        run: flutter analyze --fatal-infos

      - name: Check for outdated dependencies
        run: flutter pub outdated --no-dev-dependencies --up-to-date --no-dependency-overrides

  test:
    name: Run Tests
    runs-on: ubuntu-latest
    timeout-minutes: 20

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Run unit tests
        run: flutter test --coverage --test-randomize-ordering-seed=random

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: coverage/lcov.info
          flags: unittests
          name: unit-tests

  integration-test:
    name: Integration Tests
    runs-on: macos-latest
    timeout-minutes: 30

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Run integration tests
        run: flutter test integration_test --device-id=iphone

  build-test:
    name: Build Test (All Platforms)
    runs-on: ${{ matrix.os }}
    timeout-minutes: 30

    strategy:
      fail-fast: false
      matrix:
        include:
          - os: ubuntu-latest
            platform: android
            build-cmd: flutter build apk --debug --flavor dev
          - os: macos-latest
            platform: ios
            build-cmd: flutter build ios --debug --flavor dev --no-codesign
          - os: ubuntu-latest
            platform: web
            build-cmd: flutter build web --debug

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Setup Java (Android only)
        if: matrix.platform == 'android'
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
          cache: 'gradle'

      - name: Install dependencies
        run: flutter pub get

      - name: Build ${{ matrix.platform }}
        run: ${{ matrix.build-cmd }}

  pr-success:
    name: All checks passed
    needs: [analyze, test, integration-test, build-test]
    runs-on: ubuntu-latest
    steps:
      - run: echo "All PR checks passed!"
```

## Development Environment Deployment

**File:** `.github/workflows/deploy-dev.yml`

Deploys to internal testing on every push to `develop` branch.

```yaml
name: Deploy to Dev

on:
  push:
    branches: [ develop ]

jobs:
  deploy-android-dev:
    name: Android Dev Deployment
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
          cache: 'gradle'

      - name: Decode keystore
        run: |
          echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 -d > android/app/keystore.jks

      - name: Create key.properties
        run: |
          cat <<EOF > android/key.properties
          storePassword=${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
          keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}
          storeFile=keystore.jks
          EOF

      - name: Install dependencies
        run: flutter pub get

      - name: Build App Bundle
        run: |
          flutter build appbundle \
            --release \
            --flavor dev \
            --build-number=${{ github.run_number }}

      - name: Upload to Play Store (Internal Testing)
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT }}
          packageName: com.example.myapp.dev
          releaseFiles: build/app/outputs/bundle/devRelease/app-dev-release.aab
          track: internal
          status: completed
          inAppUpdatePriority: 2
          userFraction: 1.0
          whatsNewDirectory: whatsnew/
          mappingFile: build/app/outputs/mapping/devRelease/mapping.txt

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Android Dev Build ${{ github.run_number }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
          fields: repo,message,commit,author,action,eventName,ref,workflow

  deploy-ios-dev:
    name: iOS Dev Deployment
    runs-on: macos-latest
    timeout-minutes: 40

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
          working-directory: ios

      - name: Install Fastlane
        run: |
          cd ios
          bundle install

      - name: Deploy with Fastlane
        run: |
          cd ios
          bundle exec fastlane dev_testflight
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTH }}
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.ASC_PRIVATE_KEY }}

      - name: Notify Slack
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'iOS Dev Build ${{ github.run_number }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

  deploy-web-dev:
    name: Web Dev Deployment
    runs-on: ubuntu-latest
    timeout-minutes: 15

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Build web
        run: flutter build web --release --web-renderer canvaskit

      - name: Deploy to Firebase Hosting
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          projectId: my-flutter-app-dev
          channelId: live
```

## Production Deployment Workflow

**File:** `.github/workflows/deploy-production.yml`

Deploys to production on release tags.

```yaml
name: Deploy to Production

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  verify-tag:
    name: Verify Release Tag
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.get_version.outputs.version }}
    steps:
      - name: Get version from tag
        id: get_version
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          echo "version=$VERSION" >> $GITHUB_OUTPUT
          echo "Deploying version: $VERSION"

  pre-deployment-tests:
    name: Pre-Deployment Tests
    needs: verify-tag
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
      - run: flutter pub get
      - run: flutter test
      - run: flutter analyze

  deploy-android-production:
    name: Android Production Deployment
    needs: [verify-tag, pre-deployment-tests]
    runs-on: ubuntu-latest
    timeout-minutes: 40

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'zulu'
          java-version: '17'
          cache: 'gradle'

      - name: Decode keystore
        run: |
          echo "${{ secrets.ANDROID_KEYSTORE_BASE64 }}" | base64 -d > android/app/keystore.jks

      - name: Create key.properties
        run: |
          cat <<EOF > android/key.properties
          storePassword=${{ secrets.ANDROID_KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
          keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}
          storeFile=keystore.jks
          EOF

      - name: Install dependencies
        run: flutter pub get

      - name: Build App Bundle
        run: |
          flutter build appbundle \
            --release \
            --flavor prod \
            --obfuscate \
            --split-debug-info=build/app/outputs/symbols/prod \
            --build-name=${{ needs.verify-tag.outputs.version }} \
            --build-number=${{ github.run_number }}

      - name: Upload symbols to Crashlytics
        run: |
          # Upload symbols for crash reporting
          firebase crashlytics:symbols:upload \
            --app=${{ secrets.FIREBASE_ANDROID_APP_ID }} \
            build/app/outputs/symbols/prod

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            build/app/outputs/bundle/prodRelease/app-prod-release.aab
            build/app/outputs/mapping/prodRelease/mapping.txt
          draft: false
          prerelease: false

      - name: Upload to Play Store (Beta Track)
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT }}
          packageName: com.example.myapp
          releaseFiles: build/app/outputs/bundle/prodRelease/app-prod-release.aab
          track: beta
          status: completed
          inAppUpdatePriority: 5
          userFraction: 0.1  # 10% staged rollout
          whatsNewDirectory: whatsnew/
          mappingFile: build/app/outputs/mapping/prodRelease/mapping.txt

  deploy-ios-production:
    name: iOS Production Deployment
    needs: [verify-tag, pre-deployment-tests]
    runs-on: macos-latest
    timeout-minutes: 50

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'
          channel: 'stable'
          cache: true

      - name: Install dependencies
        run: flutter pub get

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
          bundler-cache: true
          working-directory: ios

      - name: Deploy with Fastlane
        run: |
          cd ios
          bundle exec fastlane prod_release
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTH }}
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_CONTENT: ${{ secrets.ASC_PRIVATE_KEY }}
          VERSION_NUMBER: ${{ needs.verify-tag.outputs.version }}

      - name: Upload IPA to GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: build/ios/ipa/*.ipa

  notify-deployment:
    name: Notify Team
    needs: [deploy-android-production, deploy-ios-production]
    runs-on: ubuntu-latest
    if: always()

    steps:
      - name: Send Slack notification
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: "Production Deployment ${{ needs.verify-tag.outputs.version }}",
              attachments: [{
                color: '${{ needs.deploy-android-production.result == 'success' && needs.deploy-ios-production.result == 'success' && 'good' || 'danger' }}',
                fields: [
                  {
                    title: 'Android',
                    value: '${{ needs.deploy-android-production.result }}',
                    short: true
                  },
                  {
                    title: 'iOS',
                    value: '${{ needs.deploy-ios-production.result }}',
                    short: true
                  },
                  {
                    title: 'Version',
                    value: '${{ needs.verify-tag.outputs.version }}',
                    short: true
                  },
                  {
                    title: 'Triggered by',
                    value: '${{ github.actor }}',
                    short: true
                  }
                ]
              }]
            }
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}

      - name: Send email notification
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: "Production Deployment ${{ needs.verify-tag.outputs.version }}"
          body: |
            Production deployment completed for version ${{ needs.verify-tag.outputs.version }}

            Android: ${{ needs.deploy-android-production.result }}
            iOS: ${{ needs.deploy-ios-production.result }}

            GitHub Actions Run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
          to: team@example.com
          from: ci@example.com
```

## Fastlane Configuration

**iOS Fastfile** (`ios/fastlane/Fastfile`):

```ruby
default_platform(:ios)

platform :ios do
  before_all do
    setup_ci if is_ci
  end

  desc "Deploy dev flavor to TestFlight"
  lane :dev_testflight do
    setup_code_signing(flavor: "dev")
    build_and_upload(
      flavor: "dev",
      scheme: "dev",
      bundle_id: "com.example.myapp.dev"
    )
  end

  desc "Deploy production to TestFlight and App Store"
  lane :prod_release do
    setup_code_signing(flavor: "prod")

    # Increment build number
    increment_build_number(
      xcodeproj: "Runner.xcodeproj",
      build_number: latest_testflight_build_number(
        app_identifier: "com.example.myapp"
      ) + 1
    )

    # Build
    build_app(
      scheme: "prod",
      export_method: "app-store",
      output_directory: "../build/ios/ipa",
      export_options: {
        provisioningProfiles: {
          "com.example.myapp" => "match AppStore com.example.myapp"
        }
      }
    )

    # Upload to TestFlight
    upload_to_testflight(
      skip_waiting_for_build_processing: false,
      distribute_external: true,
      groups: ["Beta Testers"],
      changelog: read_changelog
    )

    # Optionally submit to App Store
    # upload_to_app_store(
    #   submit_for_review: true,
    #   automatic_release: false,
    #   submission_information: {
    #     add_id_info_uses_idfa: false
    #   }
    # )
  end

  private_lane :setup_code_signing do |options|
    flavor = options[:flavor]

    match(
      type: "appstore",
      app_identifier: "com.example.myapp#{flavor == 'dev' ? '.dev' : ''}",
      readonly: is_ci,
      keychain_name: "fastlane_keychain",
      keychain_password: ENV["MATCH_PASSWORD"]
    )
  end

  private_lane :build_and_upload do |options|
    build_app(
      scheme: options[:scheme],
      export_method: "app-store",
      output_directory: "../build/ios/ipa"
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      distribute_external: false,
      groups: ["Internal Testers"]
    )
  end

  def read_changelog
    File.read("../CHANGELOG.md").split("\n## ").first.strip
  end
end
```

## Required GitHub Secrets

Configure these secrets in repository settings:

**Android:**
- `ANDROID_KEYSTORE_BASE64` - Base64-encoded keystore file
- `ANDROID_KEYSTORE_PASSWORD` - Keystore password
- `ANDROID_KEY_PASSWORD` - Key password
- `ANDROID_KEY_ALIAS` - Key alias
- `PLAY_STORE_SERVICE_ACCOUNT` - Service account JSON

**iOS:**
- `MATCH_PASSWORD` - Fastlane match password
- `MATCH_GIT_BASIC_AUTH` - Git credentials for match repo
- `ASC_KEY_ID` - App Store Connect API key ID
- `ASC_ISSUER_ID` - App Store Connect issuer ID
- `ASC_PRIVATE_KEY` - App Store Connect private key (base64)

**Firebase:**
- `FIREBASE_SERVICE_ACCOUNT` - Firebase service account
- `FIREBASE_ANDROID_APP_ID` - Firebase Android app ID
- `FIREBASE_IOS_APP_ID` - Firebase iOS app ID

**Notifications:**
- `SLACK_WEBHOOK` - Slack webhook URL
- `EMAIL_USERNAME` - Email username
- `EMAIL_PASSWORD` - Email password

## Triggering Deployments

**Development:**
```bash
git push origin develop
# Automatically deploys to internal testing
```

**Staging:**
```bash
git push origin staging
# Automatically deploys to closed testing/beta
```

**Production:**
```bash
git tag v1.2.3
git push origin v1.2.3
# Automatically deploys to production with staged rollout
```

## Monitoring and Rollback

**Monitor deployment:**
1. Check GitHub Actions for build status
2. Review Slack notifications
3. Monitor crash reports in Firebase Crashlytics
4. Check Play Console/App Store Connect for user feedback

**Rollback if needed:**
```bash
# Play Store - halt rollout
gcloud alpha app-version halt --service=default --version=VERSION

# Or promote previous version
upload_to_play_store(
  track: 'production',
  version_code: 'PREVIOUS_VERSION_CODE'
)
```

## Summary

This complete CI/CD workflow provides:
- ✅ Automated code quality checks on every PR
- ✅ Comprehensive testing (unit, widget, integration)
- ✅ Multi-platform builds (Android, iOS, Web)
- ✅ Multi-flavor support (dev, staging, production)
- ✅ Automated deployments to internal testing
- ✅ Production releases with staged rollouts
- ✅ Symbol uploads for crash reporting
- ✅ Team notifications via Slack and email
- ✅ GitHub releases with artifacts

Adapt this workflow to your project's specific needs, but use it as a solid foundation for professional Flutter CI/CD.

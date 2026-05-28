# CI/CD Reference

CI/CD configuration for iOS apps with Xcode Cloud, fastlane, and GitHub Actions.

## Xcode Cloud

### Setup

1. Open Xcode project
2. Navigate to Product > Xcode Cloud > Create Workflow
3. Connect Apple Developer account
4. Configure workflow settings

### Workflow Configuration

#### Build Triggers

```yaml
# Start conditions
- Push to main branch
- Pull request opened/updated
- Tag created (v*)
- Scheduled (daily at 2:00 AM)
```

#### Environment Variables

Set in Xcode Cloud settings:

```
API_BASE_URL = https://api.example.com
ANALYTICS_KEY = [secret]
```

#### Custom Scripts

Create `ci_scripts/` directory in project root:

```bash
# ci_scripts/ci_post_clone.sh
#!/bin/sh

# Install dependencies
if [ -f "Gemfile" ]; then
    bundle install
fi

# Setup environment
echo "Setting up environment..."
```

```bash
# ci_scripts/ci_pre_xcodebuild.sh
#!/bin/sh

# Generate build number from timestamp
BUILD_NUMBER=$(date +%Y%m%d%H%M)
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $BUILD_NUMBER" "$CI_PRODUCT_PLATFORM/Info.plist"
```

```bash
# ci_scripts/ci_post_xcodebuild.sh
#!/bin/sh

# Upload dSYMs to crash reporting service
if [ "$CI_WORKFLOW" = "Release" ]; then
    echo "Uploading dSYMs..."
fi
```

### Test Plans

Create a Test Plan for CI:

1. Product > Test Plan > New Test Plan
2. Configure test targets
3. Set parallelization options
4. Reference in Xcode Cloud workflow

## fastlane

### Installation

```bash
# Install fastlane
gem install fastlane

# Initialize in project
cd ios
fastlane init
```

### Fastfile

```ruby
# fastlane/Fastfile

default_platform(:ios)

platform :ios do
  # Before all lanes
  before_all do
    ensure_git_status_clean
  end

  # Run tests
  lane :test do
    run_tests(
      scheme: "MyApp",
      device: "iPhone 15",
      code_coverage: true,
      output_directory: "./test_results"
    )
  end

  # Build for TestFlight
  lane :beta do
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )

    build_app(
      scheme: "MyApp",
      export_method: "app-store",
      output_directory: "./build"
    )

    upload_to_testflight(
      skip_waiting_for_build_processing: true
    )

    # Notify team
    slack(
      message: "New beta build uploaded!",
      success: true
    )
  end

  # Release to App Store
  lane :release do
    # Capture screenshots
    capture_screenshots

    # Build
    build_app(
      scheme: "MyApp",
      export_method: "app-store"
    )

    # Upload
    upload_to_app_store(
      skip_metadata: false,
      skip_screenshots: false,
      force: true
    )
  end

  # Match for code signing
  lane :setup_signing do
    match(
      type: "appstore",
      readonly: true
    )
  end

  # Error handling
  error do |lane, exception|
    slack(
      message: "Error in #{lane}: #{exception.message}",
      success: false
    )
  end
end
```

### Matchfile

```ruby
# fastlane/Matchfile

git_url("https://github.com/org/certificates")
storage_mode("git")

type("development")
app_identifier(["com.example.myapp", "com.example.myapp.widget"])
username("developer@example.com")
team_id("XXXXXXXXXX")
```

### Appfile

```ruby
# fastlane/Appfile

app_identifier("com.example.myapp")
apple_id("developer@example.com")
team_id("XXXXXXXXXX")
itc_team_id("XXXXXXXXXX")
```

### Common Commands

```bash
# Run tests
fastlane test

# Deploy to TestFlight
fastlane beta

# Take screenshots
fastlane snapshot

# Setup code signing
fastlane match development
fastlane match appstore

# Increment version
fastlane run increment_version_number bump_type:minor
```

## GitHub Actions

### Basic Workflow

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: macos-14

    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app

      - name: Cache SPM
        uses: actions/cache@v4
        with:
          path: ~/Library/Developer/Xcode/DerivedData/**/SourcePackages
          key: ${{ runner.os }}-spm-${{ hashFiles('**/Package.resolved') }}

      - name: Build
        run: |
          xcodebuild build \
            -scheme MyApp \
            -destination "platform=iOS Simulator,name=iPhone 15" \
            -configuration Debug \
            CODE_SIGNING_ALLOWED=NO

      - name: Test
        run: |
          xcodebuild test \
            -scheme MyApp \
            -destination "platform=iOS Simulator,name=iPhone 15" \
            -resultBundlePath TestResults.xcresult \
            CODE_SIGNING_ALLOWED=NO

      - name: Upload Test Results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: TestResults.xcresult
```

### TestFlight Deployment

```yaml
# .github/workflows/testflight.yml

name: TestFlight

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: macos-14

    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.2.app

      - name: Install fastlane
        run: gem install fastlane

      - name: Setup certificates
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_AUTH }}
        run: fastlane match appstore --readonly

      - name: Build and upload
        env:
          APP_STORE_CONNECT_API_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY: ${{ secrets.ASC_API_KEY }}
        run: fastlane beta
```

### PR Checks

```yaml
# .github/workflows/pr-check.yml

name: PR Check

on:
  pull_request:

jobs:
  lint:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Run SwiftLint
        run: |
          brew install swiftlint
          swiftlint lint --reporter github-actions-logging

  test:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: |
          xcodebuild test \
            -scheme MyApp \
            -destination "platform=iOS Simulator,name=iPhone 15" \
            CODE_SIGNING_ALLOWED=NO
```

## Best Practices

### Xcode Cloud

1. **Use custom scripts** for environment setup
2. **Store secrets** in Xcode Cloud settings
3. **Use test plans** for consistent testing
4. **Archive artifacts** for debugging

### fastlane

1. **Use match** for code signing
2. **Store API keys** securely
3. **Automate versioning** with increment actions
4. **Add Slack/Teams notifications**

### GitHub Actions

1. **Cache dependencies** (SPM, CocoaPods)
2. **Use matrix builds** for multiple iOS versions
3. **Upload artifacts** for test results
4. **Protect secrets** with environment secrets

### General

1. **Run tests on every PR**
2. **Automate TestFlight deploys** from tags
3. **Keep CI/CD configs in version control**
4. **Monitor build times** and optimize

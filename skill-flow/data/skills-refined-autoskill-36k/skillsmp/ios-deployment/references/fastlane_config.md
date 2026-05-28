# Fastlane Configuration

## Installation

```bash
# Install Fastlane
brew install fastlane

# Or via RubyGems
gem install fastlane

# Initialize in iOS folder
cd ios && fastlane init
```

## Complete Fastfile

```ruby
# ios/fastlane/Fastfile

default_platform(:ios)

platform :ios do
  # ==================== SETUP ====================

  before_all do
    setup_ci if ENV['CI']
  end

  # ==================== MATCH (Code Signing) ====================

  desc "Sync all certificates and profiles"
  lane :sync_signing do
    match(type: "development")
    match(type: "appstore")
  end

  desc "Create/fetch development certificates"
  lane :certs_dev do
    match(
      type: "development",
      app_identifier: "com.magentaline.app",
      readonly: is_ci
    )
  end

  desc "Create/fetch distribution certificates"
  lane :certs_dist do
    match(
      type: "appstore",
      app_identifier: "com.magentaline.app",
      readonly: is_ci
    )
  end

  # ==================== BUILD ====================

  desc "Build debug for simulator"
  lane :build_debug do
    Dir.chdir("..") do
      sh("flutter build ios --debug --simulator")
    end
  end

  desc "Build release IPA"
  lane :build_release do
    # Ensure we have the right certificates
    certs_dist

    # Increment build number
    increment_build_number(
      build_number: latest_testflight_build_number + 1
    )

    # Build the app
    build_app(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      configuration: "Release",
      export_method: "app-store",
      export_options: {
        provisioningProfiles: {
          "com.magentaline.app" => "match AppStore com.magentaline.app"
        }
      },
      output_directory: "../build/ios/ipa",
      output_name: "MagentaLine.ipa"
    )
  end

  # ==================== TESTING ====================

  desc "Run tests"
  lane :test do
    Dir.chdir("..") do
      sh("flutter test")
    end

    run_tests(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      devices: ["iPhone 15 Pro"],
      clean: true
    )
  end

  # ==================== DISTRIBUTION ====================

  desc "Upload to TestFlight"
  lane :beta do
    build_release

    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: changelog_from_git_commits(
        commits_count: 10,
        merge_commit_filtering: "exclude_merges"
      )
    )

    # Notify team
    slack(
      message: "New MagentaLine build uploaded to TestFlight!",
      success: true
    ) if ENV['SLACK_URL']
  end

  desc "Deploy to App Store"
  lane :release do
    # Ensure tests pass
    test

    build_release

    # Upload to App Store Connect
    upload_to_app_store(
      force: true,
      submit_for_review: false,  # Manual review submission
      automatic_release: false,
      skip_metadata: false,
      skip_screenshots: false,
      precheck_include_in_app_purchases: false,
      metadata_path: "./fastlane/metadata",
      screenshots_path: "./fastlane/screenshots"
    )

    # Tag release
    add_git_tag(
      tag: "ios/v#{get_version_number}/#{get_build_number}"
    )
    push_git_tags
  end

  # ==================== UTILITIES ====================

  desc "Register new device"
  lane :add_device do |options|
    device_name = options[:name] || prompt(text: "Device name: ")
    device_udid = options[:udid] || prompt(text: "Device UDID: ")

    register_device(
      name: device_name,
      udid: device_udid
    )

    # Refresh development profiles
    match(type: "development", force_for_new_devices: true)
  end

  desc "Refresh all provisioning profiles"
  lane :refresh_profiles do
    match(type: "development", force: true)
    match(type: "appstore", force: true)
  end

  desc "Take screenshots"
  lane :screenshots do
    capture_screenshots(
      workspace: "Runner.xcworkspace",
      scheme: "Runner",
      output_directory: "./fastlane/screenshots",
      clear_previous_screenshots: true,
      devices: [
        "iPhone 15 Pro Max",
        "iPhone 15 Pro",
        "iPhone SE (3rd generation)",
        "iPad Pro (12.9-inch) (6th generation)",
        "iPad Pro (11-inch) (4th generation)"
      ]
    )
    frame_screenshots(
      path: "./fastlane/screenshots"
    )
  end

  # ==================== ERROR HANDLING ====================

  error do |lane, exception|
    slack(
      message: "Fastlane #{lane} failed: #{exception.message}",
      success: false
    ) if ENV['SLACK_URL']
  end
end
```

## Matchfile

```ruby
# ios/fastlane/Matchfile

git_url("git@github.com:magentaline/certificates.git")
storage_mode("git")

type("appstore")
app_identifier(["com.magentaline.app"])
username("developer@magentaline.app")
team_id("XXXXXXXXXX")

# For CI environments
readonly(true) if ENV['CI']
```

## Appfile

```ruby
# ios/fastlane/Appfile

app_identifier("com.magentaline.app")
apple_id("developer@magentaline.app")
team_id("XXXXXXXXXX")
itc_team_id("XXXXXXXXXX")

# App Store Connect API Key (for CI)
# Generate at: https://appstoreconnect.apple.com/access/api
for_platform :ios do
  if ENV['APP_STORE_CONNECT_API_KEY_KEY_ID']
    app_store_connect_api_key(
      key_id: ENV['APP_STORE_CONNECT_API_KEY_KEY_ID'],
      issuer_id: ENV['APP_STORE_CONNECT_API_KEY_ISSUER_ID'],
      key_content: ENV['APP_STORE_CONNECT_API_KEY_KEY'],
      is_key_content_base64: true
    )
  end
end
```

## Gymfile

```ruby
# ios/fastlane/Gymfile

workspace("Runner.xcworkspace")
scheme("Runner")
configuration("Release")

export_method("app-store")
export_xcargs("-allowProvisioningUpdates")

output_directory("../build/ios/ipa")
output_name("MagentaLine")

clean(true)
include_symbols(true)
include_bitcode(false)

xcargs({
  SWIFT_COMPILATION_MODE: "wholemodule"
})
```

## Environment Variables

```bash
# .env or CI secrets

# Apple Developer
APPLE_ID=developer@magentaline.app
TEAM_ID=XXXXXXXXXX
ITC_TEAM_ID=XXXXXXXXXX

# Match (Certificate Sync)
MATCH_GIT_URL=git@github.com:magentaline/certificates.git
MATCH_PASSWORD=your_match_password
MATCH_KEYCHAIN_PASSWORD=your_keychain_password

# App Store Connect API
APP_STORE_CONNECT_API_KEY_KEY_ID=XXXXXXXXXX
APP_STORE_CONNECT_API_KEY_ISSUER_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
APP_STORE_CONNECT_API_KEY_KEY=base64_encoded_p8_key

# Optional: Slack notifications
SLACK_URL=https://hooks.slack.com/services/xxx/yyy/zzz
```

## CI/CD Setup (GitHub Actions)

```yaml
# .github/workflows/ios-release.yml
name: iOS Release

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: macos-14

    steps:
      - uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: stable

      - name: Install dependencies
        run: flutter pub get

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: ios

      - name: Setup Keychain
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_KEYCHAIN_PASSWORD: ${{ secrets.MATCH_KEYCHAIN_PASSWORD }}
        run: |
          security create-keychain -p "$MATCH_KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$MATCH_KEYCHAIN_PASSWORD" build.keychain
          security set-keychain-settings -lut 21600 build.keychain

      - name: Install certificates
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          MATCH_GIT_URL: ${{ secrets.MATCH_GIT_URL }}
        run: cd ios && bundle exec fastlane certs_dist

      - name: Build and upload
        env:
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.ASC_KEY_ID }}
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.ASC_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.ASC_KEY }}
        run: cd ios && bundle exec fastlane beta
```

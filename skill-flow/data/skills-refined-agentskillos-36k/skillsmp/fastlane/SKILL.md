---
name: fastlane
description: Comprehensive guide to Fastlane automation for iOS and Android app deployment. Use when helping with mobile app releases, code signing, screenshots, TestFlight, App Store Connect, Google Play Store, beta distribution, CI/CD pipelines, or any Fastlane actions/lanes. Covers gym, match, pilot, deliver, supply, snapshot, screengrab, and 100+ other actions.
---

# Fastlane Deployment Skill

Fastlane automates iOS and Android app building, testing, and deployment. This skill provides action references, common workflows, and Fastfile patterns.

## Quick Reference

### Core Tools (Aliases)

| Tool | Action | Purpose |
|------|--------|---------|
| `gym` | `build_app` | Build and sign iOS/macOS apps |
| `pilot` | `upload_to_testflight` | Upload to TestFlight |
| `deliver` | `upload_to_app_store` | Upload to App Store |
| `supply` | `upload_to_play_store` | Upload to Google Play |
| `match` | `sync_code_signing` | Sync certificates/profiles |
| `cert` | `get_certificates` | Create iOS certificates |
| `sigh` | `get_provisioning_profile` | Generate provisioning profiles |
| `snapshot` | `capture_ios_screenshots` | iOS screenshots |
| `screengrab` | `capture_android_screenshots` | Android screenshots |
| `produce` | `create_app_online` | Create app on App Store Connect |
| `pem` | `get_push_certificate` | Push notification certificates |
| `scan` | `run_tests` | Run iOS/macOS tests |
| `precheck` | `check_app_store_metadata` | Validate metadata before submission |

## Common Workflows

### iOS TestFlight Deployment

```ruby
lane :beta do
  app_store_connect_api_key(
    key_id: ENV["ASC_KEY_ID"],
    issuer_id: ENV["ASC_ISSUER_ID"],
    key_filepath: ENV["ASC_KEY_PATH"]
  )
  increment_build_number
  match(type: "appstore")
  build_app(scheme: "MyApp")
  upload_to_testflight
  slack(message: "Build uploaded to TestFlight!")
end
```

### iOS App Store Release

```ruby
lane :release do
  app_store_connect_api_key(...)
  capture_screenshots
  sync_code_signing(type: "appstore")
  build_app(scheme: "MyApp")
  upload_to_app_store(
    submit_for_review: true,
    automatic_release: true
  )
end
```

### Android Play Store Deployment

```ruby
lane :deploy do
  gradle(task: "clean assembleRelease")
  upload_to_play_store(
    track: "production",
    json_key: ENV["GOOGLE_PLAY_JSON_KEY"]
  )
end
```

### Android Beta (Internal Testing)

```ruby
lane :beta do
  gradle(task: "clean bundleRelease")
  upload_to_play_store(
    track: "internal",
    aab: "app/build/outputs/bundle/release/app-release.aab"
  )
end
```

## Code Signing with Match

```ruby
# Appfile
app_identifier("com.example.app")

# Matchfile
git_url("git@github.com:org/certificates.git")
storage_mode("git")
type("appstore")

# Usage in lane
lane :setup_signing do
  match(type: "development")  # Dev certs
  match(type: "appstore")     # Distribution certs
end
```

## CI/CD Integration

### GitHub Actions Environment

```ruby
lane :ci_build do
  setup_ci  # Sets up keychain for CI
  match(type: "appstore", readonly: true)
  build_app(scheme: "MyApp")
end
```

### Environment Variables

```ruby
# App Store Connect API Key (recommended over password auth)
app_store_connect_api_key(
  key_id: ENV["ASC_KEY_ID"],
  issuer_id: ENV["ASC_ISSUER_ID"],
  key_content: ENV["ASC_KEY_CONTENT"],  # Base64 encoded .p8
  is_key_content_base64: true
)

# Google Play Service Account
upload_to_play_store(
  json_key_data: ENV["GOOGLE_PLAY_JSON_KEY"]
)
```

## Detailed Action References

For complete action parameters and examples, see:

- **Building**: `references/building.md` - gym, gradle, xcodebuild, cocoapods
- **Code Signing**: `references/code-signing.md` - match, cert, sigh, notarize
- **App Store**: `references/app-store.md` - deliver, pilot, produce, precheck
- **Google Play**: `references/google-play.md` - supply, gradle actions
- **Screenshots**: `references/screenshots.md` - snapshot, screengrab, frameit
- **Testing**: `references/testing.md` - scan, slather, swiftlint
- **Utilities**: `references/utilities.md` - notifications, source control, misc

## Essential Commands

```bash
# Initialize fastlane
fastlane init

# List all actions
fastlane actions

# Get action details
fastlane action [action_name]

# Run a lane
bundle exec fastlane [lane_name]

# Run with verbose output
bundle exec fastlane [lane_name] --verbose
```

## App Store Connect Restrictions

### Metadata Character Limits

| Field | Max Length | Notes |
|-------|------------|-------|
| **App Name** | 30 characters | Shown on App Store |
| **Subtitle** | 30 characters | Below app name |
| **Keywords** | 100 characters | Total including commas, no spaces after commas |
| **Promotional Text** | 170 characters | Can update without new build |
| **Description** | 4000 characters | |
| **What's New** | 4000 characters | Release notes |

### Screenshot Size Requirements

| Device Class | Resolution | Required |
|--------------|------------|----------|
| iPhone 6.9" (16 Pro Max) | 1320×2868 | Yes |
| iPhone 6.7" (15 Pro Max) | 1290×2796 | Yes |
| iPhone 6.5" (11 Pro Max) | 1242×2688 | Yes |
| iPhone 5.5" (8 Plus) | 1242×2208 | Yes |
| iPad 12.9" | 2048×2732 | If iPad supported |

**Known Issue**: Screenshots from Xcode 26 beta simulators (iPhone 17 series) may have resolutions not yet recognized by App Store Connect. Use iPhone 16 series simulators.

### API Key Configuration

The App Store Connect API key must be properly formatted in JSON:

```json
{
  "key_id": "YOUR_KEY_ID",
  "issuer_id": "YOUR_ISSUER_ID",
  "key": "-----BEGIN PRIVATE KEY-----\nLINE1...\nLINE2...\n-----END PRIVATE KEY-----",
  "duration": 1200,
  "in_house": false
}
```

**Critical**: The PEM key MUST have `\n` newline characters between lines. A single-line PEM causes `OpenSSL::PKey::ECError: invalid curve name`.

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `invalid curve name` | API key PEM on single line | Add `\n` between 64-char lines |
| `Invalid screenshot size` | Unrecognized device resolution | Use supported device simulators |
| `Keywords too long` | Over 100 characters total | Trim keywords, remove duplicates |
| `Subtitle too long` | Over 30 characters | Shorten subtitle |
| `No data` from `fetch_app_store_review_detail` | Known bug for new apps | Ignore - metadata uploads successfully |
| `validate_only not found` | Parameter renamed | Use `verify_only` instead |
| Bundler version mismatch | Gemfile.lock version conflict | Use `fastlane` directly instead of `bundle exec fastlane` |

## Fastfile Structure

```ruby
# fastlane/Fastfile
default_platform(:ios)

platform :ios do
  before_all do
    # Runs before every lane
  end

  lane :test do
    run_tests(scheme: "MyApp")
  end

  lane :beta do
    # Beta deployment
  end

  after_all do |lane|
    # Runs after successful lane completion
  end

  error do |lane, exception|
    slack(
      message: "Error in #{lane}: #{exception.message}",
      success: false
    )
  end
end

platform :android do
  lane :deploy do
    gradle(task: "assembleRelease")
  end
end
```

# App Store Actions

## App Store Connect API Key

Required for most App Store Connect operations. Recommended over password authentication.

```ruby
app_store_connect_api_key(
  key_id: "ABC123",
  issuer_id: "12345678-1234-1234-1234-123456789012",
  key_filepath: "./AuthKey_ABC123.p8",
  duration: 1200,  # Token validity in seconds
  in_house: false  # Set true for Enterprise accounts
)

# Using base64-encoded key content (for CI secrets)
app_store_connect_api_key(
  key_id: ENV["ASC_KEY_ID"],
  issuer_id: ENV["ASC_ISSUER_ID"],
  key_content: ENV["ASC_KEY_CONTENT"],
  is_key_content_base64: true
)
```

**JSON API Key Format** (alternative to .p8 file):

```json
{
  "key_id": "YOUR_KEY_ID",
  "issuer_id": "YOUR_ISSUER_ID",
  "key": "-----BEGIN PRIVATE KEY-----\nMIGT...LINE1...\nLINE2...\n-----END PRIVATE KEY-----",
  "duration": 1200,
  "in_house": false
}
```

**Critical**: The PEM key MUST have `\n` newline characters between each line. A single-line PEM causes `OpenSSL::PKey::ECError: invalid curve name`.

Use with `api_key_path` in deliver:
```ruby
deliver(api_key_path: "./fastlane/api_key.json", ...)
```

## deliver / upload_to_app_store

Upload metadata, screenshots, and binaries to App Store Connect.

```ruby
upload_to_app_store(
  app_identifier: "com.example.app",
  ipa: "./build/MyApp.ipa",
  
  # Submission options
  submit_for_review: true,
  automatic_release: true,
  phased_release: true,
  
  # Metadata
  app_version: "1.0.0",
  copyright: "2024 My Company",
  primary_category: "GAMES",
  secondary_category: "ENTERTAINMENT",
  
  # Review information
  submission_information: {
    add_id_info_uses_idfa: false,
    export_compliance_uses_encryption: false
  },
  
  # Skip options
  skip_screenshots: true,
  skip_metadata: false,
  skip_binary_upload: false,
  
  # Precheck
  precheck_include_in_app_purchases: false,
  run_precheck_before_submit: true
)
```

**Key Parameters:**
- `submit_for_review`: Auto-submit after upload
- `automatic_release`: Release automatically after approval
- `phased_release`: Enable phased release (7 days)
- `skip_screenshots`: Don't update screenshots
- `force`: Skip HTML preview confirmation
- `reject_if_possible`: Reject current version before upload

**Metadata Directory Structure:**
```
fastlane/metadata/
├── copyright.txt
├── primary_category.txt
├── en-US/
│   ├── name.txt
│   ├── subtitle.txt
│   ├── description.txt
│   ├── keywords.txt
│   ├── release_notes.txt
│   ├── promotional_text.txt
│   ├── support_url.txt
│   ├── marketing_url.txt
│   └── privacy_url.txt
└── de-DE/
    └── ...
```

**Metadata Character Limits:**

| File | Max Length | Notes |
|------|------------|-------|
| `name.txt` | 30 characters | App name on store |
| `subtitle.txt` | 30 characters | Shown below name |
| `keywords.txt` | 100 characters | Total including commas, no spaces |
| `promotional_text.txt` | 170 characters | Can update without new build |
| `description.txt` | 4000 characters | |
| `release_notes.txt` | 4000 characters | What's New section |

**Screenshot Requirements:**

| Device Class | Resolution | Required |
|--------------|------------|----------|
| iPhone 6.9" (16 Pro Max) | 1320×2868 | Yes |
| iPhone 6.7" (15 Pro Max) | 1290×2796 | Yes |
| iPhone 6.5" (11 Pro Max) | 1242×2688 | Yes |
| iPhone 5.5" (8 Plus) | 1242×2208 | Yes |
| iPad 12.9" | 2048×2732 | If iPad supported |

**Note**: Screenshots from beta Xcode simulators (e.g., iPhone 17 series) may not be recognized yet.

## pilot / upload_to_testflight

Upload builds to TestFlight for beta testing.

```ruby
upload_to_testflight(
  ipa: "./build/MyApp.ipa",
  
  # Build info
  changelog: "Bug fixes and improvements",
  beta_app_description: "Beta version for testing",
  
  # Distribution
  distribute_external: true,
  groups: ["Beta Testers", "QA Team"],
  
  # Options
  skip_waiting_for_build_processing: false,
  skip_submission: false,
  notify_external_testers: true,
  
  # Demo account for review
  demo_account_required: true,
  beta_app_review_info: {
    contact_email: "beta@example.com",
    contact_first_name: "John",
    contact_last_name: "Doe",
    contact_phone: "+1234567890"
  }
)
```

**Key Parameters:**
- `distribute_external`: Enable external testing
- `groups`: TestFlight group names
- `skip_waiting_for_build_processing`: Don't wait for App Store processing
- `expire_previous_builds`: Expire old builds

## produce / create_app_online

Create new app on App Store Connect and Developer Portal.

```ruby
create_app_online(
  app_identifier: "com.example.newapp",
  app_name: "My New App",
  language: "English",
  app_version: "1.0",
  sku: "my_unique_sku",
  platform: "ios",  # ios, osx, tvos
  
  # Capabilities
  enable_services: {
    push_notification: "on",
    associated_domains: "on",
    app_group: "on"
  }
)
```

## precheck / check_app_store_metadata

Validate metadata before submission.

```ruby
check_app_store_metadata(
  app_identifier: "com.example.app",
  
  # Rules to check
  negative_apple_sentiment: :fail,
  placeholder_text: :fail,
  other_platforms: :warn,
  future_functionality: :warn,
  test_words: :warn,
  curse_words: :fail,
  custom_text: :warn,
  copyright_date: :warn,
  unreachable_urls: :fail
)
```

## latest_testflight_build_number

Get the latest build number from TestFlight.

```ruby
latest_build = latest_testflight_build_number(
  app_identifier: "com.example.app",
  platform: "ios"
)

# Use to increment
increment_build_number(
  build_number: latest_build + 1
)
```

## app_store_build_number

Get build number from App Store (live or edit version).

```ruby
# Live version
live_build = app_store_build_number(
  app_identifier: "com.example.app",
  live: true
)

# Edit version
edit_build = app_store_build_number(
  app_identifier: "com.example.app",
  live: false
)
```

## download_dsyms

Download dSYM files from App Store Connect.

```ruby
download_dsyms(
  app_identifier: "com.example.app",
  version: "1.0.0",
  build_number: "123",
  output_directory: "./dsyms"
)

# Upload to crash reporting
upload_symbols_to_crashlytics(dsym_path: "./dsyms")
```

## set_changelog

Set release notes for all languages.

```ruby
set_changelog(
  app_identifier: "com.example.app",
  version: "1.0.0",
  changelog: "Bug fixes and improvements"
)
```

## App Privacy Details

```ruby
# Download current privacy details
download_app_privacy_details_from_app_store(
  app_identifier: "com.example.app",
  output_json_path: "./privacy.json"
)

# Upload privacy details
upload_app_privacy_details_to_app_store(
  app_identifier: "com.example.app",
  json_path: "./privacy.json"
)
```

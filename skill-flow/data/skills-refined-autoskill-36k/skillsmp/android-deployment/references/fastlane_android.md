# Fastlane Android Configuration

## Setup

```bash
# Install Fastlane
brew install fastlane

# Initialize in android folder
cd android && fastlane init
```

## Complete Fastfile

```ruby
# android/fastlane/Fastfile

default_platform(:android)

platform :android do
  # ==================== BUILD ====================

  desc "Build debug APK"
  lane :build_debug do
    Dir.chdir("..") do
      sh("flutter build apk --debug")
    end
  end

  desc "Build release APK (split by ABI)"
  lane :build_apk do
    Dir.chdir("..") do
      sh("flutter build apk --release --split-per-abi")
    end
  end

  desc "Build release AAB"
  lane :build_aab do
    Dir.chdir("..") do
      sh("flutter build appbundle --release")
    end
  end

  # ==================== TESTING ====================

  desc "Run tests"
  lane :test do
    Dir.chdir("..") do
      sh("flutter test")
    end

    gradle(
      task: "test",
      build_type: "Debug"
    )
  end

  # ==================== DISTRIBUTION ====================

  desc "Deploy to internal testing"
  lane :internal do
    build_aab

    upload_to_play_store(
      track: "internal",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Deploy to closed alpha"
  lane :alpha do
    build_aab

    upload_to_play_store(
      track: "alpha",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Deploy to open beta"
  lane :beta do
    build_aab

    upload_to_play_store(
      track: "beta",
      aab: "../build/app/outputs/bundle/release/app-release.aab"
    )
  end

  desc "Deploy to production"
  lane :deploy do
    # Run tests first
    test

    build_aab

    upload_to_play_store(
      track: "production",
      aab: "../build/app/outputs/bundle/release/app-release.aab",
      rollout: "0.1"  # 10% rollout initially
    )

    # Tag release
    add_git_tag(
      tag: "android/v#{android_get_version_name}/#{android_get_version_code}"
    )
    push_git_tags
  end

  desc "Promote internal to beta"
  lane :promote_to_beta do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "beta",
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Promote beta to production"
  lane :promote_to_production do
    upload_to_play_store(
      track: "beta",
      track_promote_to: "production",
      rollout: "0.2",  # 20% initial rollout
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Increase production rollout"
  lane :increase_rollout do |options|
    percentage = options[:percentage] || 0.5

    upload_to_play_store(
      track: "production",
      rollout: percentage.to_s,
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  # ==================== METADATA ====================

  desc "Upload screenshots only"
  lane :screenshots do
    upload_to_play_store(
      skip_upload_aab: true,
      skip_upload_metadata: true,
      skip_upload_changelogs: true
    )
  end

  desc "Upload metadata only"
  lane :metadata do
    upload_to_play_store(
      skip_upload_aab: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end

  desc "Fetch current Play Store metadata"
  lane :fetch_metadata do
    download_from_play_store
  end

  # ==================== VERSION MANAGEMENT ====================

  desc "Increment version code"
  lane :bump_version do
    path = "../pubspec.yaml"
    pubspec = YAML.load_file(path)

    version_parts = pubspec['version'].split('+')
    version_name = version_parts[0]
    version_code = version_parts[1].to_i + 1

    pubspec['version'] = "#{version_name}+#{version_code}"

    File.write(path, pubspec.to_yaml)

    puts "Version bumped to: #{pubspec['version']}"
  end

  # ==================== UTILITIES ====================

  desc "Validate Play Store credentials"
  lane :validate do
    validate_play_store_json_key(
      json_key: "fastlane/play-store-key.json"
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

# Helper to get version from pubspec
def android_get_version_name
  pubspec = YAML.load_file("../pubspec.yaml")
  pubspec['version'].split('+')[0]
end

def android_get_version_code
  pubspec = YAML.load_file("../pubspec.yaml")
  pubspec['version'].split('+')[1]
end
```

## Appfile

```ruby
# android/fastlane/Appfile

json_key_file("fastlane/play-store-key.json")
package_name("com.magentaline.app")
```

## Supply Configuration

```ruby
# android/fastlane/Supplyfile

# Default track for uploads
track("internal")

# Skip uploading metadata by default
skip_upload_metadata(true)
skip_upload_images(true)
skip_upload_screenshots(true)

# Timeout settings
timeout(300)
```

## Play Store Service Account

1. Go to [Google Play Console](https://play.google.com/console)
2. Settings → API access → Create new service account
3. Grant "Release manager" permissions
4. Download JSON key
5. Save as `android/fastlane/play-store-key.json`

**Important**: Add to `.gitignore`:
```
android/fastlane/play-store-key.json
```

## CI/CD GitHub Actions

```yaml
# .github/workflows/android-release.yml
name: Android Release

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: stable

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
          working-directory: android

      - name: Decode keystore
        env:
          KEYSTORE_BASE64: ${{ secrets.ANDROID_KEYSTORE_BASE64 }}
        run: echo "$KEYSTORE_BASE64" | base64 -d > android/app/upload-keystore.jks

      - name: Create key.properties
        run: |
          cat > android/key.properties << EOF
          storePassword=${{ secrets.ANDROID_STORE_PASSWORD }}
          keyPassword=${{ secrets.ANDROID_KEY_PASSWORD }}
          keyAlias=${{ secrets.ANDROID_KEY_ALIAS }}
          storeFile=upload-keystore.jks
          EOF

      - name: Create Play Store key
        env:
          PLAY_STORE_JSON: ${{ secrets.PLAY_STORE_SERVICE_ACCOUNT_JSON }}
        run: echo "$PLAY_STORE_JSON" > android/fastlane/play-store-key.json

      - name: Install dependencies
        run: flutter pub get

      - name: Deploy to internal
        run: cd android && bundle exec fastlane internal

      - name: Upload AAB artifact
        uses: actions/upload-artifact@v4
        with:
          name: app-release.aab
          path: build/app/outputs/bundle/release/app-release.aab
```

## Metadata Structure

```
android/fastlane/metadata/android/
├── en-US/
│   ├── title.txt                    # App name (50 chars)
│   ├── short_description.txt        # 80 chars
│   ├── full_description.txt         # 4000 chars
│   ├── video.txt                    # YouTube URL (optional)
│   ├── changelogs/
│   │   ├── default.txt
│   │   └── 42.txt                   # Version code specific
│   └── images/
│       ├── icon.png                 # 512x512
│       ├── featureGraphic.png       # 1024x500
│       ├── phoneScreenshots/
│       │   ├── 1.png
│       │   └── 2.png
│       ├── sevenInchScreenshots/
│       └── tenInchScreenshots/
└── de-DE/                           # Other locales
    └── ...
```

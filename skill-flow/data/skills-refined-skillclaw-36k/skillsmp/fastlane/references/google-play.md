# Google Play Actions

## Authentication Setup

Create a service account in Google Cloud Console with Google Play Android Developer API access.

```ruby
# Using JSON key file
upload_to_play_store(
  json_key: "./play-store-key.json"
)

# Using JSON key content (for CI)
upload_to_play_store(
  json_key_data: ENV["GOOGLE_PLAY_JSON_KEY"]
)
```

## supply / upload_to_play_store

Upload APK/AAB and metadata to Google Play Store.

```ruby
upload_to_play_store(
  package_name: "com.example.app",
  
  # Binary
  aab: "./app/build/outputs/bundle/release/app-release.aab",
  # OR
  apk: "./app/build/outputs/apk/release/app-release.apk",
  
  # Track
  track: "production",  # internal, alpha, beta, production
  rollout: "0.1",  # Staged rollout percentage (0.1 = 10%)
  
  # Release
  release_status: "completed",  # completed, draft, halted, inProgress
  version_name: "1.0.0",
  version_code: 123,
  
  # Metadata
  skip_upload_metadata: false,
  skip_upload_changelogs: false,
  skip_upload_images: false,
  skip_upload_screenshots: false,
  
  # Options
  validate_only: false,  # Validate without uploading
  sync_image_upload: true
)
```

**Tracks:**
- `internal`: Internal testing (up to 100 testers)
- `alpha`: Closed testing
- `beta`: Open testing
- `production`: Public release

**Release Status:**
- `completed`: Fully released
- `draft`: Save as draft
- `halted`: Halt the release
- `inProgress`: Staged rollout in progress

## download_from_play_store

Download existing metadata and screenshots.

```ruby
download_from_play_store(
  package_name: "com.example.app",
  metadata_path: "./fastlane/metadata/android",
  track: "production"
)
```

## upload_to_play_store_internal_app_sharing

Upload to Internal App Sharing for quick testing.

```ruby
upload_to_play_store_internal_app_sharing(
  package_name: "com.example.app",
  aab: "./app-release.aab",
  json_key: "./play-store-key.json"
)
# Returns shareable URL
```

## download_universal_apk_from_google_play

Download universal APK from Play Store.

```ruby
download_universal_apk_from_google_play(
  package_name: "com.example.app",
  version_code: 123,
  destination: "./downloads/app.apk"
)
```

## google_play_track_version_codes

Get version codes for a track.

```ruby
version_codes = google_play_track_version_codes(
  package_name: "com.example.app",
  track: "production"
)
# Returns array: [123, 122, 121]
```

## google_play_track_release_names

Get release names for a track.

```ruby
release_names = google_play_track_release_names(
  package_name: "com.example.app",
  track: "production"
)
```

## validate_play_store_json_key

Validate service account key.

```ruby
validate_play_store_json_key(
  json_key: "./play-store-key.json"
)
```

## Metadata Directory Structure

```
fastlane/metadata/android/
├── en-US/
│   ├── title.txt              # App name (50 chars)
│   ├── short_description.txt  # Short desc (80 chars)
│   ├── full_description.txt   # Full desc (4000 chars)
│   ├── video.txt              # YouTube video URL
│   ├── changelogs/
│   │   ├── 100.txt            # Changelog for version code 100
│   │   ├── 101.txt
│   │   └── default.txt        # Default changelog
│   └── images/
│       ├── phoneScreenshots/
│       │   ├── 1_en-US.png
│       │   └── 2_en-US.png
│       ├── sevenInchScreenshots/
│       ├── tenInchScreenshots/
│       ├── tvScreenshots/
│       ├── wearScreenshots/
│       ├── icon.png           # 512x512
│       ├── featureGraphic.png # 1024x500
│       ├── promoGraphic.png   # 180x120
│       └── tvBanner.png       # 1280x720
├── de-DE/
│   └── ...
└── ja-JP/
    └── ...
```

## Common Android Workflows

### Full Release to Production

```ruby
lane :release do
  gradle(task: "clean bundleRelease")
  
  upload_to_play_store(
    track: "production",
    aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH],
    release_status: "completed"
  )
  
  slack(message: "Android app released to Play Store!")
end
```

### Staged Rollout

```ruby
lane :staged_release do
  upload_to_play_store(
    track: "production",
    aab: "./app-release.aab",
    rollout: "0.1",  # 10% rollout
    release_status: "inProgress"
  )
end

lane :complete_rollout do
  upload_to_play_store(
    track: "production",
    rollout: "1.0",  # 100% rollout
    release_status: "completed"
  )
end
```

### Internal to Production Promotion

```ruby
lane :promote_to_production do
  upload_to_play_store(
    track: "internal",
    track_promote_to: "production",
    skip_upload_apk: true,
    skip_upload_aab: true
  )
end
```

### Beta Testing

```ruby
lane :beta do
  gradle(task: "bundleRelease")
  
  upload_to_play_store(
    track: "beta",
    aab: lane_context[SharedValues::GRADLE_AAB_OUTPUT_PATH]
  )
end
```

## Managed Google Play (Enterprise)

```ruby
# Get publishing rights URL
get_managed_play_store_publishing_rights

# Create app on Managed Play Store
create_app_on_managed_play_store(
  json_key: "./service-account.json",
  app_title: "My Enterprise App"
)
```

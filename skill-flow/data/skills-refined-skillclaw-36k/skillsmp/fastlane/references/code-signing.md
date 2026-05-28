# Code Signing Actions

## match / sync_code_signing

Sync certificates and provisioning profiles across team via Git or cloud storage. The recommended approach for team code signing.

```ruby
# Basic usage
match(type: "appstore")
match(type: "development")
match(type: "adhoc")

# Full configuration
match(
  type: "appstore",
  app_identifier: "com.example.app",
  git_url: "git@github.com:org/certificates.git",
  git_branch: "master",
  readonly: true,  # Don't create new certs
  force_for_new_devices: true,
  verbose: true
)

# Using Google Cloud Storage
match(
  type: "appstore",
  storage_mode: "google_cloud",
  google_cloud_bucket_name: "my-bucket",
  google_cloud_keys_file: "gc_keys.json"
)

# Using S3
match(
  type: "appstore",
  storage_mode: "s3",
  s3_bucket: "my-bucket",
  s3_region: "us-east-1"
)
```

**Key Parameters:**
- `type`: development, adhoc, appstore, enterprise
- `app_identifier`: Bundle ID(s), can be array
- `git_url`: Git repo for certificates
- `readonly`: Only fetch, don't create new
- `force`: Regenerate certificates
- `platform`: ios, macos, tvos

**Matchfile Configuration:**
```ruby
# fastlane/Matchfile
git_url("git@github.com:org/certificates.git")
storage_mode("git")
type("appstore")
app_identifier(["com.example.app", "com.example.app.widget"])
username("user@example.com")
```

## cert / get_certificates

Create or fetch iOS code signing certificates.

```ruby
cert(
  development: false,  # Distribution cert
  output_path: "./certs",
  keychain_path: "/path/to/keychain",
  keychain_password: ENV["KEYCHAIN_PASSWORD"]
)

# Development certificate
cert(development: true)
```

## sigh / get_provisioning_profile

Generate or download provisioning profiles.

```ruby
sigh(
  app_identifier: "com.example.app",
  provisioning_name: "MyApp AppStore",
  output_path: "./profiles",
  adhoc: false,
  development: false,
  force: true  # Regenerate profile
)

# Development profile
sigh(development: true)

# Ad-hoc profile
sigh(adhoc: true)
```

## register_devices

Register new devices to Apple Developer Portal.

```ruby
# Single device
register_device(
  name: "John's iPhone",
  udid: "A1B2C3D4-E5F6-..."
)

# Multiple devices from file
register_devices(
  devices_file: "./devices.txt"
)

# From hash
register_devices(
  devices: {
    "John's iPhone" => "A1B2C3D4...",
    "Jane's iPad" => "B2C3D4E5..."
  }
)
```

**devices.txt format:**
```
Device ID	Device Name
A1B2C3D4...	John's iPhone
B2C3D4E5...	Jane's iPad
```

## import_certificate

Import certificate into keychain.

```ruby
import_certificate(
  certificate_path: "./cert.p12",
  certificate_password: ENV["CERT_PASSWORD"],
  keychain_name: "login.keychain",
  keychain_password: ENV["KEYCHAIN_PASSWORD"]
)
```

## update_code_signing_settings

Configure Xcode project code signing settings.

```ruby
update_code_signing_settings(
  path: "MyApp.xcodeproj",
  use_automatic_signing: false,
  team_id: "ABC123DEF",
  profile_name: "MyApp Distribution",
  code_sign_identity: "iPhone Distribution"
)

# Enable automatic signing
update_code_signing_settings(
  path: "MyApp.xcodeproj",
  use_automatic_signing: true
)
```

## update_project_provisioning

Update provisioning profile in Xcode project.

```ruby
update_project_provisioning(
  xcodeproj: "MyApp.xcodeproj",
  profile: "./profiles/MyApp.mobileprovision",
  target_filter: "MyApp",
  build_configuration: "Release"
)
```

## notarize

Notarize macOS apps for distribution outside App Store.

```ruby
notarize(
  package: "build/MyApp.app",
  bundle_id: "com.example.app",
  asc_provider: "TeamShortName",
  print_log: true,
  verbose: true
)
```

## resign

Re-sign an existing IPA with different credentials.

```ruby
resign(
  ipa: "MyApp.ipa",
  signing_identity: "iPhone Distribution: Company Name",
  provisioning_profile: "./MyProfile.mobileprovision"
)
```

## match_nuke

Delete all certificates and profiles (dangerous!).

```ruby
match_nuke(type: "development")  # Only dev certs
match_nuke(type: "distribution")  # Only dist certs
```

## Keychain Actions

```ruby
# Create keychain for CI
create_keychain(
  name: "ci_keychain",
  password: ENV["KEYCHAIN_PASSWORD"],
  default_keychain: true,
  unlock: true,
  timeout: 3600
)

# Unlock existing keychain
unlock_keychain(
  path: "~/Library/Keychains/login.keychain",
  password: ENV["KEYCHAIN_PASSWORD"]
)

# Delete keychain
delete_keychain(name: "ci_keychain")
```

## CI Setup

```ruby
# Automatic CI setup (creates temp keychain)
setup_ci

# Specific CI providers
setup_circle_ci
setup_travis
setup_jenkins
```

# Code Signing and Certificates

Complete guide to code signing, certificates, and provisioning profiles for Flutter app deployment.

## Overview

Code signing is the process of digitally signing executables and code to verify the developer's identity and ensure code hasn't been tampered with. Mobile platforms (iOS and Android) and some desktop platforms require code signing before apps can be distributed. This guide covers certificates, keystore management, provisioning profiles, and security best practices.

## Why Code Signing Matters

### Security Benefits

- **Identity Verification** - Confirms the developer's identity
- **Integrity Protection** - Ensures code hasn't been modified
- **Trust Establishment** - Operating systems trust signed apps
- **Malware Prevention** - Prevents unauthorized code execution

### Platform Requirements

| Platform | Code Signing Required | Certificate Type |
|----------|----------------------|------------------|
| Android | Yes (all distribution) | Self-signed or CA |
| iOS | Yes (all distribution) | Apple certificates |
| macOS | Optional (notarization required for dist) | Apple certificates |
| Windows | Optional (recommended) | CA or self-signed |
| Linux | Not required | N/A |
| Web | Not applicable | N/A |

## Android Code Signing

### Understanding Android Signing

Android uses a **keystore** containing one or more **key pairs** (public and private keys). Every Android app must be signed before installation.

**Key concepts:**

- **Keystore** - File containing one or more keys (`.jks`, `.keystore`)
- **Key alias** - Name identifying a specific key within keystore
- **Key password** - Password protecting the private key
- **Store password** - Password protecting the keystore file

### Google Play App Signing

Google Play uses a two-tier signing system:

**Upload Key:**
- You create and control this key
- Used to sign app bundles before uploading to Play Console
- Can be reset if lost (with Google's help)

**App Signing Key:**
- Google creates and manages this key
- Used to sign APKs distributed to users
- More secure (Google manages it)
- Cannot be reset

**Workflow:**
1. Sign app bundle with upload key
2. Upload to Play Console
3. Google re-signs with app signing key
4. Google distributes signed APKs to users

### Creating an Upload Keystore

**On macOS/Linux:**

```bash
keytool -genkey -v \
  -keystore ~/upload-keystore.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias upload
```

**On Windows (PowerShell):**

```powershell
keytool -genkey -v `
  -keystore $env:USERPROFILE\upload-keystore.jks `
  -storetype JKS `
  -keyalg RSA `
  -keysize 2048 `
  -validity 10000 `
  -alias upload
```

**Parameters explained:**

| Parameter | Meaning |
|-----------|---------|
| `-keystore` | Keystore file path |
| `-keyalg RSA` | RSA algorithm |
| `-keysize 2048` | 2048-bit key (secure) |
| `-validity 10000` | Valid for 10,000 days (~27 years) |
| `-alias` | Key alias name |

**Prompts:**
- **Keystore password** - Protect keystore (remember this!)
- **Key password** - Protect private key (can be same as keystore password)
- **Distinguished Name** - Your name, organization, location, etc.

**Output:** `upload-keystore.jks` file

### Storing Keystore Credentials

**NEVER commit keystores or passwords to version control!**

Create `android/key.properties` (add to `.gitignore`):

```properties
storePassword=your_keystore_password
keyPassword=your_key_password
keyAlias=upload
storeFile=/Users/yourname/upload-keystore.jks
```

**For Windows:**
```properties
storeFile=C:\\Users\\YourName\\upload-keystore.jks
```

**For relative paths:**
```properties
storeFile=../keystore/upload-keystore.jks
```

### Configuring Gradle for Signing

Edit `android/app/build.gradle.kts`:

```kotlin
import java.util.Properties
import java.io.FileInputStream

// Load keystore properties
val keystorePropertiesFile = rootProject.file("key.properties")
val keystoreProperties = Properties()

if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}

android {
    namespace = "com.example.myapp"
    compileSdk = flutter.compileSdkVersion

    defaultConfig {
        applicationId = "com.example.myapp"
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        versionCode = flutterVersionCode.toInteger()
        versionName = flutterVersionName
    }

    // Define signing configuration
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String
        }
    }

    buildTypes {
        release {
            // Use release signing configuration
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

### Building Signed App

```bash
# Build signed app bundle
flutter build appbundle --release

# Build signed APK
flutter build apk --release
```

The built artifacts are now signed with your upload key.

### Verifying Signature

```bash
# For APK
jarsigner -verify -verbose -certs app-release.apk

# For App Bundle
jarsigner -verify -verbose -certs app-release.aab
```

Should show: "jar verified" and your certificate details.

### Keystore Management Best Practices

**Backup:**
- Store keystore in multiple secure locations
- Use encrypted storage (password manager, encrypted drive)
- Keep offline backups

**Security:**
- Use strong passwords (20+ characters)
- Never share keystores via email or messaging
- Use different keystores for different apps
- Rotate keys periodically (via Play Console)

**Documentation:**
- Document keystore location
- Record passwords securely
- Note expiration dates
- Keep track of key aliases

**Lost Keystore:**
- With Google Play App Signing: Contact Google support to reset upload key
- Without Google Play App Signing: Cannot update app, must publish new app

### CI/CD Signing

**Using environment variables:**

```bash
# Set environment variables in CI
export KEYSTORE_PASSWORD="your_password"
export KEY_PASSWORD="your_key_password"
export KEY_ALIAS="upload"
export KEYSTORE_FILE="/path/to/keystore.jks"
```

**Encode keystore as base64:**

```bash
base64 upload-keystore.jks > keystore.txt
```

Store encoded keystore as secret in CI system, decode during build:

```bash
echo $KEYSTORE_BASE64 | base64 -d > upload-keystore.jks
```

**GitHub Actions example:**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Decode keystore
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > android/app/upload-keystore.jks

      - name: Create key.properties
        run: |
          echo "storePassword=${{ secrets.KEYSTORE_PASSWORD }}" > android/key.properties
          echo "keyPassword=${{ secrets.KEY_PASSWORD }}" >> android/key.properties
          echo "keyAlias=${{ secrets.KEY_ALIAS }}" >> android/key.properties
          echo "storeFile=upload-keystore.jks" >> android/key.properties

      - uses: subosito/flutter-action@v2
      - run: flutter build appbundle --release
```

## iOS Code Signing

### Understanding iOS Signing

iOS code signing is more complex than Android, involving:

- **Certificates** - Identify the developer
- **Private keys** - Sign the code (stored in Keychain)
- **Provisioning profiles** - Link certificates to app IDs and devices
- **Entitlements** - Define app capabilities

**Certificate types:**

| Type | Purpose |
|------|---------|
| Apple Development | Development and testing |
| Apple Distribution | App Store distribution |
| Developer ID Application | Distribution outside Mac App Store (macOS) |
| Developer ID Installer | Installer packages (macOS) |

### Certificates

**Certificate = Public Key + Developer Identity**

Certificates are issued by Apple and verify your identity as a developer.

**Creating a certificate:**

1. **Generate Certificate Signing Request (CSR):**

Open **Keychain Access** on Mac:
- Menu: **Keychain Access** → **Certificate Assistant** → **Request a Certificate from a Certificate Authority**
- Enter email and common name
- Select "Saved to disk"
- Save `CertificateSigningRequest.certSigningRequest`

This generates a public/private key pair. Private key stays in Keychain, public key goes in CSR.

2. **Create certificate in Apple Developer Portal:**

Go to [Certificates, Identifiers & Profiles](https://developer.apple.com/account/resources/certificates/list):
- Click **+** to create new certificate
- Select certificate type (e.g., **Apple Distribution**)
- Upload CSR file
- Download certificate (`.cer` file)

3. **Install certificate:**

Double-click `.cer` file to add to Keychain. Certificate is now paired with private key in Keychain.

**Certificate validity:**
- Development: 1 year
- Distribution: 1 year
- Must renew before expiration

**Certificate limits:**
- 2 Apple Distribution certificates per team
- 2 iOS Development certificates per person
- Unlimited Developer ID certificates

### Private Keys

Private keys are generated when you create a CSR and stored in Mac Keychain.

**Exporting private key:**

1. Open **Keychain Access**
2. Find your certificate under **My Certificates**
3. Expand to show private key
4. Right-click private key → **Export**
5. Save as `.p12` file with password

**Importing private key on another Mac:**

1. Copy `.p12` file to new Mac
2. Double-click to import into Keychain
3. Enter export password
4. Now certificate can be used on new Mac

**Security note:** Protect `.p12` files like passwords. Anyone with the `.p12` and password can sign apps as you.

### Provisioning Profiles

**Provisioning Profile = Certificate + App ID + Devices (optional) + Entitlements**

Provisioning profiles link your certificate to a specific app and define where it can run.

**Profile types:**

| Type | Purpose | Devices |
|------|---------|---------|
| Development | Testing on devices | Specific registered devices |
| Ad Hoc | Testing/distribution outside App Store | Up to 100 registered devices |
| App Store | App Store distribution | All devices |
| Enterprise | Enterprise distribution | All devices within organization |

**Creating a provisioning profile:**

1. Go to [Profiles](https://developer.apple.com/account/resources/profiles/list)
2. Click **+** to create new profile
3. Select distribution type (e.g., **App Store**)
4. Select App ID
5. Select certificate(s)
6. (For development/ad hoc) Select devices
7. Name the profile
8. Download profile (`.mobileprovision` file)

**Installing profile:**

Double-click `.mobileprovision` file to install in Xcode.

Or place in:
```
~/Library/MobileDevice/Provisioning Profiles/
```

**Profile expiration:**
- All profiles: 1 year
- Must regenerate when certificate renewed

### Automatic vs Manual Signing

**Automatic Signing (Recommended for most developers):**

In Xcode:
- Select target → **Signing & Capabilities**
- Check **Automatically manage signing**
- Select **Team**

Xcode automatically:
- Creates/downloads certificates
- Creates/downloads provisioning profiles
- Manages profile renewal

**Advantages:**
- Simplest approach
- Xcode handles everything
- Good for individuals/small teams

**Disadvantages:**
- Less control
- Can have issues in CI/CD
- Multiple developers may create duplicate certificates

**Manual Signing (Recommended for teams/CI/CD):**

In Xcode:
- Uncheck **Automatically manage signing**
- Select **Provisioning Profile** manually for each configuration

**Advantages:**
- Full control over certificates and profiles
- Better for CI/CD
- Shared signing across team

**Disadvantages:**
- More complex setup
- Manual renewal required
- Must understand signing process

### Fastlane Match (Recommended for Teams)

Fastlane match synchronizes certificates and profiles across team via encrypted Git repository.

**Benefits:**
- One set of certificates shared by team
- Stored securely in Git (encrypted)
- Easy setup on new machines
- Automatic in CI/CD

**Setup:**

```bash
cd ios
fastlane match init
```

Choose **git** storage and provide private repository URL.

**Generate certificates:**

```bash
# Development certificates
fastlane match development

# App Store certificates
fastlane match appstore

# Ad Hoc certificates
fastlane match adhoc
```

Match creates certificates and profiles, stores in Git repo encrypted.

**Configure Xcode:**

After running match, update Xcode:
- Disable automatic signing
- Set provisioning profile to: `match AppStore com.example.myapp`

**Use in CI/CD:**

```yaml
- name: Set up certificates
  run: |
    cd ios
    fastlane match appstore --readonly
  env:
    MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
    MATCH_GIT_BASIC_AUTHORIZATION: ${{ secrets.MATCH_GIT_BASIC_AUTH }}
```

**Match advantages:**
- Solves "code signing hell"
- Works seamlessly in CI/CD
- Easy onboarding for new team members
- Automatic certificate renewal

### Entitlements

Entitlements define app capabilities (push notifications, iCloud, etc.).

Configured in Xcode: **Signing & Capabilities** tab

Add capability → Xcode updates entitlements file.

**Example entitlements (`Runner.entitlements`):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Push notifications -->
    <key>aps-environment</key>
    <string>production</string>

    <!-- Associated domains -->
    <key>com.apple.developer.associated-domains</key>
    <array>
        <string>applinks:example.com</string>
    </array>

    <!-- App groups -->
    <key>com.apple.security.application-groups</key>
    <array>
        <string>group.com.example.myapp</string>
    </array>
</dict>
</plist>
```

Entitlements must match those in provisioning profile.

### Building Signed iOS App

```bash
# Automatic signing
flutter build ipa --release

# With specific export method
flutter build ipa --export-method ad-hoc
flutter build ipa --export-method development
flutter build ipa --export-method enterprise
```

Xcode handles signing automatically based on configuration.

### Verifying iOS Signature

```bash
# Check signature
codesign -vv -d build/ios/iphoneos/Runner.app

# Display entitlements
codesign -d --entitlements - build/ios/iphoneos/Runner.app

# Verify provisioning profile
security cms -D -i build/ios/iphoneos/Runner.app/embedded.mobileprovision
```

### iOS Signing Issues and Solutions

**Issue: "No certificate for team"**

**Solutions:**
- Generate certificate in Developer Portal
- Download and install certificate
- Ensure private key is in Keychain
- Select correct team in Xcode

**Issue: "Provisioning profile doesn't include signing certificate"**

**Solutions:**
- Regenerate provisioning profile to include certificate
- Download new profile
- Select new profile in Xcode
- Or enable automatic signing

**Issue: "Unable to install app - code signature invalid"**

**Solutions:**
- Ensure device is registered (for development)
- Check provisioning profile includes device UDID
- Regenerate profile if needed
- Clean build folder and rebuild

**Issue: "Private key not found"**

**Solutions:**
- Import `.p12` file with private key
- Request certificate from machine that created it
- Or revoke certificate and create new one

## macOS Code Signing

macOS signing is similar to iOS:

**Certificate types:**
- **Apple Development** - Development
- **Apple Distribution** - Mac App Store
- **Developer ID Application** - Distribution outside App Store
- **Developer ID Installer** - Installer packages

**Notarization (Required for distribution outside App Store):**

```bash
# Sign app
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" \
  YourApp.app

# Create DMG
hdiutil create -volname "YourApp" -srcfolder YourApp.app -ov -format UDZO YourApp.dmg

# Sign DMG
codesign --sign "Developer ID Application: Your Name (TEAMID)" YourApp.dmg

# Submit for notarization
xcrun notarytool submit YourApp.dmg \
  --apple-id your@email.com \
  --team-id TEAMID \
  --password app-specific-password \
  --wait

# Staple notarization ticket
xcrun stapler staple YourApp.dmg
```

Notarization confirms no malware, allows users to open app without warnings.

## Windows Code Signing

Windows signing is optional but recommended.

**Certificate types:**
- **Code signing certificate from CA** (e.g., DigiCert, Sectigo)
- **Self-signed certificate** (for testing)

**Signing MSIX package:**

MSIX packages must be signed to install.

**With self-signed certificate:**

```powershell
# Create certificate (for testing)
New-SelfSignedCertificate `
  -Type Custom `
  -Subject "CN=YourCompany" `
  -KeyUsage DigitalSignature `
  -FriendlyName "YourApp Test" `
  -CertStoreLocation "Cert:\CurrentUser\My"

# Export certificate
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object {$_.Subject -like "*YourCompany*"}
$password = ConvertTo-SecureString -String "Password123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "YourCert.pfx" -Password $password
```

**Configure msix package:**

```yaml
msix_config:
  certificate_path: C:\path\to\YourCert.pfx
  certificate_password: Password123
```

**With CA certificate:**

Purchase code signing certificate from trusted CA, follow their instructions.

## Security Best Practices

### Storage

- **Use password managers** for keystore/certificate passwords
- **Encrypt keystores** when storing
- **Use hardware security modules (HSM)** for critical keys
- **Don't store in cloud storage** unless encrypted

### Access Control

- **Limit access** to signing credentials
- **Use separate keys** per app
- **Rotate keys** periodically
- **Audit key usage** regularly

### CI/CD Security

- **Use CI/CD secrets** for passwords
- **Encrypt keystores** in repository (or store externally)
- **Use ephemeral credentials** when possible
- **Don't log sensitive data**
- **Restrict access** to CI/CD secrets

### Certificate Management

- **Monitor expiration dates** - Set reminders
- **Renew before expiration** - Allow time for testing
- **Document all credentials** - Securely
- **Have backup signing keys** - For emergency

### Team Practices

- **Use fastlane match** for iOS team signing
- **Centralize keystore management**
- **Document signing process**
- **Onboard new members** securely
- **Offboard members** by rotating keys

## Troubleshooting

### Android

**Can't find keystore:**
- Check `storeFile` path in `key.properties`
- Use absolute path or correct relative path
- Verify file exists at specified location

**Wrong password:**
- Check passwords in `key.properties`
- Verify keystore password vs key password
- Try re-entering password in `key.properties`

**Signature doesn't match:**
- Using wrong keystore
- Check key alias is correct
- Ensure consistent keystore across builds

### iOS

**Certificate not found:**
- Install certificate in Keychain
- Ensure private key is present
- Check certificate hasn't expired

**Profile doesn't match:**
- Ensure Bundle ID matches profile
- Check certificate is included in profile
- Verify entitlements match

**Can't sign on CI:**
- Export certificates as `.p12`
- Store securely in CI secrets
- Import during build process

## Quick Reference

### Android Commands

```bash
# Generate keystore
keytool -genkey -v -keystore keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload

# Verify signature
jarsigner -verify -verbose -certs app-release.apk

# View keystore info
keytool -list -v -keystore keystore.jks
```

### iOS Commands

```bash
# View certificate info
security find-identity -v -p codesigning

# Export certificate
security export -k ~/Library/Keychains/login.keychain -t certs -f pkcs12 -o cert.p12

# Verify app signature
codesign -vv -d YourApp.app

# Display entitlements
codesign -d --entitlements - YourApp.app
```

### Fastlane Commands

```bash
# Initialize match
fastlane match init

# Generate certificates
fastlane match development
fastlane match appstore

# Nuke certificates (reset)
fastlane match nuke development
fastlane match nuke distribution
```

## Resources

- [Android App Signing](https://developer.android.com/studio/publish/app-signing)
- [iOS Code Signing Guide](https://developer.apple.com/support/code-signing/)
- [Fastlane Match](https://docs.fastlane.tools/actions/match/)
- [Google Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756)
- [Apple Developer Account](https://developer.apple.com/account/)

## Summary

Code signing is essential for distributing Flutter apps on mobile platforms. Android uses keystores with public/private key pairs and benefits from Google Play App Signing for enhanced security. iOS uses Apple-issued certificates paired with private keys, along with provisioning profiles that link certificates to app IDs and devices. Both platforms require careful credential management, secure storage, and proper CI/CD integration. Understanding code signing principles, using tools like fastlane match for teams, and following security best practices ensures smooth, secure app distribution. Always back up signing credentials and document the signing process for your team.

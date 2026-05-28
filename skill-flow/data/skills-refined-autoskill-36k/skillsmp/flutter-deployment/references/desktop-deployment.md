# Desktop Deployment

Complete guide to building and distributing Flutter desktop applications for Windows, macOS, and Linux.

## Overview

Flutter desktop support enables you to build native applications for Windows, macOS, and Linux from a single codebase. Desktop deployment differs significantly from mobile—no mandatory app stores (except macOS App Store optionally), larger file sizes, different distribution methods, and platform-specific packaging requirements.

## Platform Support Status

As of Flutter 3.38:
- **Windows** - Stable
- **macOS** - Stable
- **Linux** - Stable

All desktop platforms are production-ready and actively supported.

## Windows Deployment

### Prerequisites

- **Windows 10/11** - Development and target platform
- **Visual Studio 2022** - With "Desktop development with C++" workload
- **Flutter SDK** - Latest stable version
- **Windows SDK** - Included with Visual Studio

### Enable Windows Desktop Support

```bash
flutter config --enable-windows-desktop
flutter create --platforms=windows .
```

### Building Windows Applications

**Basic build:**

```bash
flutter build windows --release
```

**Output location:**
```
build/windows/runner/Release/
```

**Output contains:**
- `yourapp.exe` - Main executable
- `flutter_windows.dll` - Flutter engine
- `data/` - Assets and resources
- Various DLL dependencies

### Windows Packaging Formats

#### MSIX Package (Recommended for Microsoft Store)

MSIX is the modern Windows app package format supporting:
- Microsoft Store distribution
- Windows 10/11 installation
- Automatic updates
- Sandboxed environment

**Setup using msix pub package:**

Add to `pubspec.yaml`:

```yaml
dev_dependencies:
  msix: ^3.16.7

msix_config:
  display_name: My Flutter App
  publisher_display_name: Your Company
  identity_name: com.yourcompany.yourapp
  publisher: CN=YourCompany, O=YourCompany, L=YourCity, S=YourState, C=YourCountry
  msix_version: 1.0.0.0
  logo_path: assets/images/logo.png
  capabilities: internetClient, location
  certificate_path: C:\path\to\certificate.pfx
  certificate_password: your_password
```

**Create MSIX package:**

```bash
flutter pub get
flutter pub run msix:create
```

**Output:** `build/windows/runner/Release/yourapp.msix`

**Install locally for testing:**

```powershell
Add-AppxPackage -Path "build\windows\runner\Release\yourapp.msix"
```

**MSIX configuration options:**

| Option | Description |
|--------|-------------|
| `display_name` | App name shown to users |
| `publisher_display_name` | Publisher name |
| `identity_name` | Unique app identifier |
| `msix_version` | Version (must end in .0) |
| `languages` | Supported languages (e.g., en-us) |
| `capabilities` | Required capabilities |
| `icons_background_color` | Icon background (hex) |
| `architecture` | x64, x86, arm, arm64 |

#### Self-Signed Certificate for Development

Create test certificate:

```powershell
# Create certificate
$cert = New-SelfSignedCertificate `
  -Type Custom `
  -Subject "CN=YourCompany" `
  -KeyUsage DigitalSignature `
  -FriendlyName "YourApp Test Certificate" `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

# Export certificate
$password = ConvertTo-SecureString -String "YourPassword" -Force -AsPlainText
Export-PfxCertificate `
  -Cert "Cert:\CurrentUser\My\$($cert.Thumbprint)" `
  -FilePath "YourCert.pfx" `
  -Password $password
```

#### Portable Executable (No Installation)

Distribute the entire `Release/` folder as a zip file:

```bash
# Build
flutter build windows --release

# Package
cd build/windows/runner/Release
tar -a -c -f MyApp-Windows.zip *
```

Users extract and run `yourapp.exe` directly. No installation required.

**Advantages:**
- Simplest distribution
- No certificates needed
- Works on all Windows versions
- Portable (USB drive, network share)

**Disadvantages:**
- Larger download (includes all dependencies)
- No automatic updates
- Manual uninstall (delete folder)

#### Inno Setup Installer

Create traditional Windows installer using Inno Setup:

**Install Inno Setup:**
Download from [jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)

**Create install script (`installer.iss`):**

```inno
[Setup]
AppName=My Flutter App
AppVersion=1.0.0
DefaultDirName={pf}\MyFlutterApp
DefaultGroupName=My Flutter App
OutputDir=output
OutputBaseFilename=MyAppSetup
Compression=lzma2
SolidCompression=yes

[Files]
Source: "build\windows\runner\Release\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\My Flutter App"; Filename: "{app}\yourapp.exe"
Name: "{commondesktop}\My Flutter App"; Filename: "{app}\yourapp.exe"

[Run]
Filename: "{app}\yourapp.exe"; Description: "Launch My Flutter App"; Flags: nowait postinstall skipifsilent
```

**Build installer:**

```bash
# Build Flutter app
flutter build windows --release

# Compile installer (adjust path to ISCC.exe)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

### Microsoft Store Submission

**Prerequisites:**
- Microsoft Partner Center account
- App name reservation
- Valid code signing certificate (from CA or Partner Center)

**Submission steps:**

1. **Reserve app name** in Partner Center
2. **Configure msix_config** with Partner Center details:

```yaml
msix_config:
  publisher: CN=12345678-1234-1234-1234-123456789012
  identity_name: 12345YourCompany.YourAppName
  publisher_display_name: Your Company
```

3. **Build MSIX package:**

```bash
flutter pub run msix:create
```

4. **Upload to Partner Center:**
   - Submit package via Partner Center dashboard
   - Or use Microsoft Store Developer CLI:

```bash
# Install CLI
dotnet tool install -g Microsoft.Windows.SDK.MSStoreCLI

# Configure
msstore reconfigure `
  --tenantId YOUR_TENANT_ID `
  --clientId YOUR_CLIENT_ID `
  --clientSecret YOUR_CLIENT_SECRET `
  --sellerId YOUR_SELLER_ID

# Package and publish
msstore package build/windows/runner/Release
msstore publish -v
```

5. **Complete store listing:**
   - App description
   - Screenshots (1366x768 or higher)
   - Age ratings
   - Privacy policy
   - Pricing and availability

6. **Submit for certification**

**Certification process:**
- Typically 24-72 hours
- Microsoft tests for security and policy compliance
- App published upon approval

### Windows Version Management

Update version in `pubspec.yaml`:

```yaml
version: 1.0.0+1
```

For MSIX, version must end in `.0`:
- `1.0.0.0` ✓
- `1.2.3.0` ✓
- `1.0.0.5` ✗

Configure in `msix_config`:

```yaml
msix_config:
  msix_version: 1.0.0.0
```

Or override during build:

```bash
flutter build windows --build-name=1.0.0 --build-number=0
```

### Windows App Icon

**For MSIX packages:**

Provide icon in `msix_config`:

```yaml
msix_config:
  logo_path: assets/images/logo.png
```

Icon requirements:
- PNG format
- 400x400 pixels or larger
- Transparent background recommended

**For executable:**

Replace icon in `windows/runner/resources/app_icon.ico`:
- Use tool like IconWorkshop or GIMP
- Create `.ico` with multiple sizes: 16x16, 32x32, 48x48, 256x256

If renaming, update `windows/runner/Runner.rc`:

```c
IDI_APP_ICON ICON "resources\\app_icon.ico"
```

## macOS Deployment

### Prerequisites

- **macOS computer** - Required for building
- **Xcode** - Latest stable version
- **Apple Developer account** - For App Store distribution ($99/year)
- **CocoaPods** - Dependency management

### Enable macOS Desktop Support

```bash
flutter config --enable-macos-desktop
flutter create --platforms=macos .
```

### Building macOS Applications

**Basic build:**

```bash
flutter build macos --release
```

**Output location:**
```
build/macos/Build/Products/Release/yourapp.app
```

The `.app` bundle contains:
- Executable binary
- Resources and assets
- Info.plist configuration
- Code signature

### macOS Packaging and Distribution

#### Option 1: Mac App Store (Recommended)

Submit to Mac App Store for widest distribution and automatic updates.

**Prerequisites:**
- Apple Developer Program membership
- App Store Connect account
- Mac App Store distribution certificate
- Mac App Store provisioning profile

**Configuration steps:**

1. **Register Bundle ID:**
   - Go to [Apple Developer Portal → Identifiers](https://developer.apple.com/account/resources/identifiers/list)
   - Create new App ID for macOS
   - Format: `com.yourcompany.yourapp`
   - Enable required capabilities

2. **Create App Store Connect record:**
   - Go to [App Store Connect](https://appstoreconnect.apple.com/)
   - Click **My Apps** → **+** → **New App**
   - Select macOS platform
   - Fill in app information

3. **Configure Xcode project:**

Open `macos/Runner.xcworkspace` in Xcode:

```bash
open macos/Runner.xcworkspace
```

**Signing & Capabilities:**
- Enable "Automatically manage signing"
- Select your Developer team
- Or manually configure with provisioning profile

**General settings:**
- Bundle Identifier: `com.yourcompany.yourapp`
- Version: `1.0.0`
- Build: `1`

4. **Build archive:**

```bash
# Build Flutter app
flutter build macos --release

# Or build in Xcode
# Product → Archive
```

5. **Create package (PKG):**

```bash
# Get app name
APP_NAME=$(find $(pwd)/build/macos/Build/Products/Release -name "*.app")

# Get bundle identifier from Info.plist
BUNDLE_ID=$(defaults read "${APP_NAME}/Contents/Info.plist" CFBundleIdentifier)

# Create unsigned package
PACKAGE_NAME=$(basename "$APP_NAME" .app).pkg
xcrun productbuild \
  --component "$APP_NAME" \
  /Applications/ \
  unsigned.pkg

# Sign package (replace with your certificate name)
INSTALLER_CERT_NAME="3rd Party Mac Developer Installer: Your Name (TEAMID)"
xcrun productsign \
  --sign "$INSTALLER_CERT_NAME" \
  unsigned.pkg \
  "$PACKAGE_NAME"

# Verify signature
pkgutil --check-signature "$PACKAGE_NAME"
```

6. **Upload to App Store Connect:**

```bash
# Using altool (deprecated but still works)
xcrun altool --upload-package "$PACKAGE_NAME" \
  --type macos \
  --apiKey YOUR_API_KEY \
  --apiIssuer YOUR_ISSUER_ID

# Or using App Store Connect API
# Or drag and drop into Transporter app
```

7. **Complete App Store listing and submit for review**

Similar process to iOS (see ios-release.md).

#### Option 2: Notarized Distribution (Outside App Store)

Distribute outside App Store while meeting Apple's security requirements.

**Why notarize:**
- Required for macOS 10.15+ (Catalina and later)
- Prevents "unidentified developer" warnings
- Users can open app without extra steps

**Notarization process:**

1. **Sign app with Developer ID:**

```bash
# Sign with Developer ID Application certificate
codesign --force --deep --sign "Developer ID Application: Your Name (TEAMID)" \
  build/macos/Build/Products/Release/yourapp.app
```

2. **Create signed DMG:**

```bash
# Create DMG
hdiutil create -volname "YourApp" -srcfolder \
  build/macos/Build/Products/Release/yourapp.app \
  -ov -format UDZO YourApp.dmg

# Sign DMG
codesign --sign "Developer ID Application: Your Name (TEAMID)" YourApp.dmg
```

3. **Submit for notarization:**

```bash
# Upload to Apple notary service
xcrun notarytool submit YourApp.dmg \
  --apple-id your@email.com \
  --team-id TEAMID \
  --password app-specific-password \
  --wait

# Or use API key
xcrun notarytool submit YourApp.dmg \
  --key AuthKey.p8 \
  --key-id KEYID \
  --issuer ISSUERID \
  --wait
```

4. **Staple notarization ticket:**

```bash
xcrun stapler staple YourApp.dmg

# Verify
xcrun stapler validate YourApp.dmg
spctl -a -vvv -t install YourApp.dmg
```

**Distribute notarized DMG** via website, email, etc.

#### Option 3: Development Distribution (Not Notarized)

For internal testing or development only.

```bash
flutter build macos --release

# Package as ZIP
cd build/macos/Build/Products/Release
zip -r ../../../../../YourApp-macOS.zip yourapp.app
```

**Warning:** Users must right-click → Open to bypass Gatekeeper, or remove quarantine:

```bash
xattr -cr /path/to/yourapp.app
```

Not suitable for public distribution.

### macOS App Icon

**Configure in AppIcon.appiconset:**

1. Open Xcode: `open macos/Runner.xcworkspace`
2. Select `Assets.xcassets` → `AppIcon`
3. Drag icons into appropriate slots

**Required sizes:**
- 16x16 @1x, @2x
- 32x32 @1x, @2x
- 128x128 @1x, @2x
- 256x256 @1x, @2x
- 512x512 @1x, @2x (1024x1024)

**Icon guidelines:**
- Use PNG format
- No rounded corners (macOS adds them)
- Follow [macOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/macos/icons-and-images/app-icon/)

### macOS Version Management

Update in `pubspec.yaml`:

```yaml
version: 1.2.3+45
```

Or configure in Xcode:
- **Version:** User-facing (e.g., 1.2.3)
- **Build:** Unique identifier (e.g., 45)

Or override:

```bash
flutter build macos --build-name=1.2.3 --build-number=45
```

### macOS Entitlements

Configure app capabilities in `macos/Runner/DebugProfile.entitlements` and `macos/Runner/Release.entitlements`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Network access -->
    <key>com.apple.security.network.client</key>
    <true/>

    <!-- File access -->
    <key>com.apple.security.files.user-selected.read-write</key>
    <true/>

    <!-- Camera access -->
    <key>com.apple.security.device.camera</key>
    <true/>

    <!-- Disable App Sandbox for full filesystem access -->
    <key>com.apple.security.app-sandbox</key>
    <false/>
</dict>
</plist>
```

**Common entitlements:**
- `com.apple.security.network.client` - Network client
- `com.apple.security.network.server` - Network server
- `com.apple.security.files.user-selected.read-write` - File access
- `com.apple.security.device.camera` - Camera
- `com.apple.security.device.audio-input` - Microphone
- `com.apple.security.app-sandbox` - Enable/disable sandbox

**Note:** App Store requires sandboxing (`app-sandbox: true`). Outside App Store, you can disable for more access.

## Linux Deployment

### Prerequisites

- **Linux OS** - Ubuntu 18.04+ or other modern distribution
- **Development libraries** - GTK 3, Clang
- **Flutter SDK** - Latest stable version

**Install dependencies (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev
```

### Enable Linux Desktop Support

```bash
flutter config --enable-linux-desktop
flutter create --platforms=linux .
```

### Building Linux Applications

**Basic build:**

```bash
flutter build linux --release
```

**Output location:**
```
build/linux/x64/release/bundle/
```

**Output contains:**
- `yourapp` - Executable binary
- `lib/` - Shared libraries
- `data/` - Assets and resources

### Linux Distribution Formats

#### Snap Package (Recommended)

Snap packages work across many Linux distributions and provide automatic updates.

**Prerequisites:**
- Ubuntu or snapcraft-supporting distro
- Snapcraft installed: `sudo snap install snapcraft --classic`

**Create snapcraft.yaml:**

Create `snap/snapcraft.yaml`:

```yaml
name: your-app
version: '1.0.0'
summary: Your app summary
description: |
  Your app description.
  Can be multiple lines.

grade: stable
confinement: strict
base: core22

architectures:
  - build-on: amd64

slots:
  dbus-daemon:
    interface: dbus
    bus: session
    name: org.yourcompany.yourapp

apps:
  your-app:
    command: your_app
    extensions: [gnome]
    plugs:
      - network
      - network-bind
      - home
      - audio-playback
    slots:
      - dbus-daemon

parts:
  your-app:
    source: .
    plugin: flutter
    flutter-target: lib/main.dart
```

**Desktop entry file:**

Create `snap/gui/your-app.desktop`:

```ini
[Desktop Entry]
Name=Your App
Comment=Your app description
Exec=your-app
Icon=${SNAP}/meta/gui/your-app.png
Terminal=false
Type=Application
Categories=Utility;
```

**Add app icon:**

Place icon at `snap/gui/your-app.png` (256x256 or 512x512 PNG).

**Build snap:**

```bash
snapcraft --use-lxd
```

**Output:** `your-app_1.0.0_amd64.snap`

**Install locally:**

```bash
sudo snap install ./your-app_1.0.0_amd64.snap --dangerous
```

**Publish to Snap Store:**

```bash
# Login
snapcraft login

# Register app name
snapcraft register your-app

# Upload and release
snapcraft upload --release=stable your-app_1.0.0_amd64.snap
```

#### AppImage (Portable)

Universal Linux package that runs on most distributions without installation.

**Use appimage-builder:**

Install:

```bash
sudo apt install -y python3-pip python3-setuptools patchelf desktop-file-utils libgdk-pixbuf2.0-dev fakeroot strace
sudo pip3 install appimage-builder
```

**Create AppImageBuilder.yml:**

```yaml
version: 1

AppDir:
  path: ./AppDir
  app_info:
    id: com.yourcompany.yourapp
    name: YourApp
    icon: your-app
    version: 1.0.0
    exec: usr/bin/your_app

  apt:
    arch: amd64
    sources:
      - sourceline: 'deb [arch=amd64] http://archive.ubuntu.com/ubuntu/ focal main restricted universe multiverse'

  files:
    include:
      - build/linux/x64/release/bundle
    exclude:
      - usr/share/man
      - usr/share/doc

  runtime:
    env:
      PATH: '${APPDIR}/usr/bin:${PATH}'
      LD_LIBRARY_PATH: '${APPDIR}/usr/lib:${LD_LIBRARY_PATH}'

AppImage:
  arch: x86_64
  update-information: guess
```

**Build AppImage:**

```bash
flutter build linux --release
appimage-builder --recipe AppImageBuilder.yml
```

**Output:** `YourApp-1.0.0-x86_64.AppImage`

**Run:**

```bash
chmod +x YourApp-1.0.0-x86_64.AppImage
./YourApp-1.0.0-x86_64.AppImage
```

#### DEB Package (Debian/Ubuntu)

Native package for Debian-based distributions.

**Use flutter_distributor or create manually:**

Install flutter_distributor:

```yaml
dev_dependencies:
  flutter_distributor: ^0.3.0
```

Create `distribute_options.yaml`:

```yaml
output: dist/
releases:
  - name: prod
    jobs:
      - name: linux-deb
        package:
          platform: linux
          target: deb
        artifacts:
          - deb
```

**Build:**

```bash
flutter pub get
flutter_distributor package --platform linux --targets deb
```

**Or manually with dpkg:**

Create directory structure:

```
your-app_1.0.0/
├── DEBIAN/
│   └── control
└── usr/
    ├── bin/
    │   └── your-app
    ├── share/
    │   ├── applications/
    │   │   └── your-app.desktop
    │   └── icons/
    │       └── your-app.png
    └── lib/
        └── your-app/
```

Create `DEBIAN/control`:

```
Package: your-app
Version: 1.0.0
Architecture: amd64
Maintainer: Your Name <your@email.com>
Description: Your app description
```

**Build package:**

```bash
dpkg-deb --build your-app_1.0.0
```

**Install:**

```bash
sudo dpkg -i your-app_1.0.0.deb
```

#### Flatpak

Sandboxed distribution format.

**Use flatpak-flutter:**

```bash
git clone https://github.com/TheAppgineer/flatpak-flutter
cd flatpak-flutter
./flatpak-flutter.sh /path/to/your/flutter/project
```

Generates Flatpak manifest for building and publishing to Flathub.

#### Tarball (Generic)

Simple compressed archive of the bundle.

```bash
flutter build linux --release
cd build/linux/x64/release
tar -czf ../../../../your-app-linux.tar.gz bundle/
```

**Distribution:**
Users extract and run `./bundle/your_app`.

### Linux App Icon

Place icon at `linux/flutter/data/icon.png` or configure in desktop entry file.

For Snap, use `snap/gui/your-app.png`.

For AppImage, include in AppDir.

For DEB, place in `/usr/share/icons/`.

### Linux Version Management

Update in `pubspec.yaml`:

```yaml
version: 1.2.3+45
```

## Cross-Platform Considerations

### Directory Structure

Maintain consistent structure:

```
myapp/
├── lib/                 # Shared Dart code
├── assets/              # Shared assets
├── windows/             # Windows-specific
├── macos/               # macOS-specific
├── linux/               # Linux-specific
├── android/             # Android-specific (if applicable)
├── ios/                 # iOS-specific (if applicable)
├── web/                 # Web-specific (if applicable)
└── pubspec.yaml
```

### Platform Detection

Detect platform at runtime:

```dart
import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

String getPlatform() {
  if (kIsWeb) return 'Web';
  if (Platform.isWindows) return 'Windows';
  if (Platform.isMacOS) return 'macOS';
  if (Platform.isLinux) return 'Linux';
  return 'Unknown';
}
```

### Platform-Specific Code

Use conditional imports:

```dart
// platform_file_picker.dart
import 'platform_file_picker_stub.dart'
    if (dart.library.io) 'platform_file_picker_io.dart'
    if (dart.library.html) 'platform_file_picker_web.dart';

// Use in code
final filePath = await pickFile();
```

### Native Integration

Access platform-specific APIs via plugins or platform channels.

**Windows example:**

```dart
import 'package:win32/win32.dart';

void showWindowsDialog() {
  MessageBox(NULL, 'Hello Windows', 'Flutter', MB_OK);
}
```

**macOS example:**

```dart
import 'package:macos_ui/macos_ui.dart';

void showMacDialog(BuildContext context) {
  showMacosAlertDialog(
    context: context,
    builder: (_) => MacosAlertDialog(
      title: Text('Hello macOS'),
    ),
  );
}
```

## CI/CD for Desktop

### GitHub Actions Example

Create `.github/workflows/desktop-build.yml`:

```yaml
name: Build Desktop Apps

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - run: flutter config --enable-windows-desktop
      - run: flutter pub get
      - run: flutter build windows --release

      - name: Create MSIX
        run: flutter pub run msix:create

      - uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: build/windows/runner/Release/

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - run: flutter config --enable-macos-desktop
      - run: flutter pub get
      - run: flutter build macos --release

      - uses: actions/upload-artifact@v3
        with:
          name: macos-build
          path: build/macos/Build/Products/Release/

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.38.6'

      - run: flutter config --enable-linux-desktop
      - run: flutter pub get
      - run: flutter build linux --release

      - uses: actions/upload-artifact@v3
        with:
          name: linux-build
          path: build/linux/x64/release/bundle/
```

## Best Practices

### Build Process

- Test on target platforms regularly
- Use release mode for distribution
- Keep Flutter SDK updated
- Version releases consistently
- Clean build before major releases

### Security

- Sign all distributed binaries
- Use sandboxing when possible
- Request minimal permissions
- Validate user inputs
- Don't hardcode secrets

### Performance

- Optimize startup time
- Minimize memory usage
- Use native UI patterns per platform
- Profile on target hardware
- Test with real-world data

### Distribution

- Provide checksums for downloads
- Use secure download channels (HTTPS)
- Publish to official stores when possible
- Document system requirements
- Provide installation instructions

### Maintenance

- Monitor crash reports
- Implement auto-update mechanisms
- Maintain backwards compatibility
- Keep dependencies updated
- Provide rollback options

## Common Issues and Solutions

### Windows Build Fails

**Problem:** Visual Studio not found

**Solutions:**
- Install Visual Studio 2022 with "Desktop development with C++"
- Run `flutter doctor` to verify setup
- Restart after Visual Studio installation

### macOS Notarization Fails

**Problem:** App rejected during notarization

**Solutions:**
- Ensure hardened runtime enabled
- Check entitlements are correct
- Verify all binaries are signed
- Use latest Xcode command line tools

### Linux Missing Dependencies

**Problem:** Build fails with missing library errors

**Solutions:**
- Install development packages: `libgtk-3-dev`, etc.
- Update package manager: `sudo apt-get update`
- Check distribution-specific requirements

### Large Bundle Sizes

**Problem:** Executable and dependencies are very large

**Solutions:**
- Flutter desktop bundles include engine (~50-100 MB)
- Split resources from binary
- Use compression for distribution packages
- Consider streaming assets for rarely-used resources

## Quick Reference

### Build Commands

```bash
# Windows
flutter build windows --release

# macOS
flutter build macos --release

# Linux
flutter build linux --release

# With version
flutter build windows --build-name=1.2.3 --build-number=1

# Clean build
flutter clean && flutter pub get && flutter build windows
```

### Package Commands

```bash
# MSIX (Windows)
flutter pub run msix:create

# Snap (Linux)
snapcraft --use-lxd

# AppImage (Linux)
appimage-builder --recipe AppImageBuilder.yml
```

## Resources

- [Flutter Desktop Documentation](https://docs.flutter.dev/desktop)
- [Windows Deployment](https://docs.flutter.dev/deployment/windows)
- [macOS Deployment](https://docs.flutter.dev/deployment/macos)
- [Linux Deployment](https://docs.flutter.dev/deployment/linux)
- [MSIX Documentation](https://pub.dev/packages/msix)
- [Snapcraft Documentation](https://snapcraft.io/docs)

## Summary

Desktop deployment opens Flutter apps to traditional computing platforms with unique distribution requirements. Windows offers flexible packaging via MSIX, portable executables, or installers. macOS requires code signing and optionally App Store submission or notarization. Linux provides multiple formats from Snap to AppImage to traditional packages. Understanding each platform's requirements, signing processes, and distribution channels enables successful cross-platform desktop deployment. Test thoroughly on each platform, follow security best practices, and choose distribution methods appropriate for your target audience.

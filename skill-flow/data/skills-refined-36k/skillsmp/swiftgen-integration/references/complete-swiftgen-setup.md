# Complete SwiftGen Setup and Integration

<!-- Loading Trigger: Agent reads this file when setting up SwiftGen, configuring templates, creating build phases, or debugging code generation issues -->

## Complete swiftgen.yml Configuration

```yaml
# swiftgen.yml - Complete configuration for iOS/tvOS project

# =============================================================================
# STRINGS (Localization)
# =============================================================================

strings:
  inputs:
    # Base localization (English)
    - Resources/en.lproj/Localizable.strings
    # Additional modules
    - Resources/en.lproj/InfoPlist.strings
  outputs:
    - templateName: structured-swift5
      output: Generated/Strings.swift
      params:
        # Public access for multi-module projects
        publicAccess: true
        # Custom enum name
        enumName: L10n
        # Include all localization tables
        lookupFunction: tr
        # Support for bundle lookup
        bundle: BundleToken.bundle

# =============================================================================
# ASSETS (Images)
# =============================================================================

xcassets:
  # Main assets catalog
  - inputs:
      - Resources/Assets.xcassets
    outputs:
      - templateName: swift5
        output: Generated/Assets.swift
        params:
          publicAccess: true
          enumName: Asset
          # Generate allImages for debugging
          allValues: false
          # Force namespace for organization
          forceNamespaces: true

  # Feature-specific assets (if using feature modules)
  - inputs:
      - Features/Home/Resources/Home.xcassets
    outputs:
      - templateName: swift5
        output: Features/Home/Generated/HomeAssets.swift
        params:
          publicAccess: false
          enumName: HomeAsset

# =============================================================================
# COLORS
# =============================================================================

colors:
  - inputs:
      - Resources/Colors.xcassets
    outputs:
      - templateName: swift5
        output: Generated/Colors.swift
        params:
          publicAccess: true
          enumName: Colors

# =============================================================================
# FONTS
# =============================================================================

fonts:
  - inputs:
      - Resources/Fonts/
    outputs:
      - templateName: swift5
        output: Generated/Fonts.swift
        params:
          publicAccess: true
          # Preserve folder structure
          preservePath: true

# =============================================================================
# STORYBOARDS (if using)
# =============================================================================

ib:
  - inputs:
      - Resources/Base.lproj/
    outputs:
      - templateName: scenes-swift5
        output: Generated/Storyboards.swift
        params:
          publicAccess: true
          module: AppModule

# =============================================================================
# CORE DATA (if using)
# =============================================================================

coredata:
  - inputs:
      - Resources/Model.xcdatamodeld
    outputs:
      - templateName: swift5
        output: Generated/CoreData.swift
        params:
          publicAccess: true

# =============================================================================
# PLISTS
# =============================================================================

plist:
  - inputs:
      - Resources/Settings.plist
    outputs:
      - templateName: runtime-swift5
        output: Generated/Settings.swift
        params:
          publicAccess: true
          enumName: Settings
```

## Generated Code Extensions

```swift
// MARK: - Extensions/SwiftGen+SwiftUI.swift

import SwiftUI

// =============================================================================
// Image Extensions
// =============================================================================

extension Image {
    /// Initialize with SwiftGen ImageAsset
    init(asset: ImageAsset) {
        self.init(asset.name, bundle: BundleToken.bundle)
    }

    /// Initialize with SwiftGen ImageAsset, with template rendering
    init(asset: ImageAsset, renderingMode: TemplateRenderingMode) {
        self.init(asset.name, bundle: BundleToken.bundle)
    }
}

extension ImageAsset {
    /// SwiftUI Image from asset
    var swiftUIImage: Image {
        Image(asset: self)
    }

    /// UIKit UIImage from asset
    var uiImage: UIImage {
        image
    }
}

// =============================================================================
// Color Extensions
// =============================================================================

extension Color {
    /// Initialize with SwiftGen ColorAsset
    init(asset: ColorAsset) {
        self.init(asset.name, bundle: BundleToken.bundle)
    }
}

extension ColorAsset {
    /// SwiftUI Color from asset
    var swiftUIColor: Color {
        Color(asset: self)
    }

    /// UIKit UIColor from asset
    var uiColor: UIColor {
        color
    }
}

// =============================================================================
// Font Extensions
// =============================================================================

extension Font {
    /// Create font from SwiftGen FontConvertible
    static func custom(_ font: FontConvertible, size: CGFloat) -> Font {
        font.swiftUIFont(size: size)
    }

    /// Create font from SwiftGen FontConvertible with relative size
    static func custom(_ font: FontConvertible, size: CGFloat, relativeTo textStyle: TextStyle) -> Font {
        font.swiftUIFont(size: size, relativeTo: textStyle)
    }
}

extension FontConvertible {
    /// Get SwiftUI Font
    func swiftUIFont(size: CGFloat) -> Font {
        Font.custom(name, size: size)
    }

    /// Get SwiftUI Font with relative sizing for Dynamic Type
    func swiftUIFont(size: CGFloat, relativeTo textStyle: Font.TextStyle) -> Font {
        Font.custom(name, size: size, relativeTo: textStyle)
    }

    /// Get UIKit UIFont
    func uiFont(size: CGFloat) -> UIFont {
        font(size: size)
    }
}

// =============================================================================
// Localization Extensions
// =============================================================================

extension String {
    /// Convenience for accessing localized strings
    static func localized(_ key: String, table: String? = nil) -> String {
        NSLocalizedString(key, tableName: table, bundle: BundleToken.bundle, comment: "")
    }
}

extension Text {
    /// Initialize with L10n string directly
    init(_ localizedString: String, tableName: String? = nil, bundle: Bundle = BundleToken.bundle) {
        self.init(LocalizedStringKey(localizedString), tableName: tableName, bundle: bundle)
    }
}

// =============================================================================
// View Modifiers for Common Patterns
// =============================================================================

extension View {
    /// Apply color asset to foreground
    func foregroundColor(asset: ColorAsset) -> some View {
        foregroundStyle(Color(asset: asset))
    }

    /// Apply color asset to background
    func background(asset: ColorAsset) -> some View {
        background(Color(asset: asset))
    }

    /// Apply font from FontConvertible
    func font(_ font: FontConvertible, size: CGFloat) -> some View {
        self.font(.custom(font, size: size))
    }
}

// =============================================================================
// Usage Examples
// =============================================================================

/*
struct ContentView: View {
    var body: some View {
        VStack(spacing: 16) {
            // Image from asset
            Image(asset: Asset.Icons.home)
                .resizable()
                .frame(width: 24, height: 24)

            // Alternative syntax
            Asset.Icons.settings.swiftUIImage
                .foregroundColor(asset: Colors.primary)

            // Text with localization
            Text(L10n.Home.title)
                .font(FontFamily.Roboto.bold, size: 24)
                .foregroundColor(asset: Colors.textPrimary)

            // Button with asset color
            Button(L10n.Common.submit) {
                // action
            }
            .background(asset: Colors.buttonPrimary)
        }
    }
}
*/
```

## Build Phase Script (Complete)

```bash
#!/bin/bash

# =============================================================================
# SwiftGen Build Phase Script
# =============================================================================
# Place in Build Phases -> New Run Script Phase -> BEFORE "Compile Sources"
# Name: "Generate SwiftGen Constants"
# =============================================================================

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "${GREEN}[SwiftGen] Starting code generation...${NC}"

# =============================================================================
# Step 1: Check SwiftGen Installation
# =============================================================================

if ! which swiftgen >/dev/null 2>&1; then
    echo "${YELLOW}warning: SwiftGen not installed. Install via:${NC}"
    echo "  brew install swiftgen"
    echo "  OR"
    echo "  mint install SwiftGen/SwiftGen"
    echo ""
    echo "Skipping code generation."
    exit 0
fi

SWIFTGEN_VERSION=$(swiftgen --version | head -n 1)
echo "[SwiftGen] Using $SWIFTGEN_VERSION"

# =============================================================================
# Step 2: Navigate to Project Root
# =============================================================================

if [ -z "$SRCROOT" ]; then
    echo "${RED}error: SRCROOT not set. Run from Xcode build phase.${NC}"
    exit 1
fi

cd "$SRCROOT"
echo "[SwiftGen] Working directory: $(pwd)"

# =============================================================================
# Step 3: Check Configuration File
# =============================================================================

CONFIG_FILE="swiftgen.yml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "${YELLOW}warning: $CONFIG_FILE not found at $SRCROOT${NC}"
    echo "Create swiftgen.yml to enable code generation."
    exit 0
fi

# =============================================================================
# Step 4: Create Output Directory
# =============================================================================

OUTPUT_DIR="Generated"
mkdir -p "$OUTPUT_DIR"
echo "[SwiftGen] Output directory: $OUTPUT_DIR"

# =============================================================================
# Step 5: Run SwiftGen
# =============================================================================

echo "[SwiftGen] Running code generation..."

if swiftgen config run --config "$CONFIG_FILE"; then
    echo "${GREEN}[SwiftGen] Code generation completed successfully${NC}"
else
    echo "${RED}error: SwiftGen failed. Check configuration.${NC}"
    exit 1
fi

# =============================================================================
# Step 6: Verify Output (Optional)
# =============================================================================

OUTPUT_FILES=(
    "$OUTPUT_DIR/Assets.swift"
    "$OUTPUT_DIR/Strings.swift"
    "$OUTPUT_DIR/Colors.swift"
    "$OUTPUT_DIR/Fonts.swift"
)

MISSING_FILES=0
for file in "${OUTPUT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "[SwiftGen] ✓ Generated: $file"
    else
        echo "${YELLOW}[SwiftGen] ○ Not generated: $file (may be expected)${NC}"
    fi
done

# =============================================================================
# Step 7: Touch Output for Build System
# =============================================================================
# This helps Xcode's incremental build system recognize the files

for file in "$OUTPUT_DIR"/*.swift; do
    if [ -f "$file" ]; then
        touch "$file"
    fi
done

echo "${GREEN}[SwiftGen] Done!${NC}"
exit 0
```

## Input/Output Files Configuration

```bash
# =============================================================================
# Input Files (Add to Build Phase)
# =============================================================================
# These tell Xcode when to re-run the script

# Configuration
$(SRCROOT)/swiftgen.yml

# Assets
$(SRCROOT)/Resources/Assets.xcassets
$(SRCROOT)/Resources/Colors.xcassets

# Strings
$(SRCROOT)/Resources/en.lproj/Localizable.strings

# Fonts directory
$(SRCROOT)/Resources/Fonts

# =============================================================================
# Output Files (Add to Build Phase)
# =============================================================================
# These tell Xcode what files will be generated

$(SRCROOT)/Generated/Assets.swift
$(SRCROOT)/Generated/Colors.swift
$(SRCROOT)/Generated/Strings.swift
$(SRCROOT)/Generated/Fonts.swift
```

## Multi-Module / SPM Setup

```swift
// Package.swift - SwiftGen with Swift Package Manager

// swift-tools-version:5.9

import PackageDescription

let package = Package(
    name: "MyApp",
    platforms: [
        .iOS(.v17),
        .tvOS(.v17)
    ],
    products: [
        .library(name: "DesignSystem", targets: ["DesignSystem"]),
        .library(name: "Feature", targets: ["Feature"])
    ],
    dependencies: [
        // SwiftGen plugin (if using as build tool)
        // .package(url: "https://github.com/SwiftGen/SwiftGenPlugin", from: "6.6.0")
    ],
    targets: [
        // Design System module with shared assets
        .target(
            name: "DesignSystem",
            dependencies: [],
            resources: [
                .process("Resources")
            ],
            plugins: [
                // .plugin(name: "SwiftGenPlugin", package: "SwiftGenPlugin")
            ]
        ),

        // Feature module with module-specific assets
        .target(
            name: "Feature",
            dependencies: ["DesignSystem"],
            resources: [
                .process("Resources")
            ]
        )
    ]
)
```

```yaml
# Modules/DesignSystem/swiftgen.yml

xcassets:
  - inputs:
      - Sources/DesignSystem/Resources/Colors.xcassets
    outputs:
      - templateName: swift5
        output: Sources/DesignSystem/Generated/Colors.swift
        params:
          publicAccess: true  # MUST be public for cross-module access
          enumName: DSColors
          bundle: Bundle.module  # SPM bundle

fonts:
  - inputs:
      - Sources/DesignSystem/Resources/Fonts/
    outputs:
      - templateName: swift5
        output: Sources/DesignSystem/Generated/Fonts.swift
        params:
          publicAccess: true
          bundle: Bundle.module
```

```yaml
# Modules/Feature/swiftgen.yml

strings:
  - inputs:
      - Sources/Feature/Resources/en.lproj/Feature.strings
    outputs:
      - templateName: structured-swift5
        output: Sources/Feature/Generated/Strings.swift
        params:
          publicAccess: false  # Internal to module
          enumName: FeatureStrings
          bundle: Bundle.module

xcassets:
  - inputs:
      - Sources/Feature/Resources/Assets.xcassets
    outputs:
      - templateName: swift5
        output: Sources/Feature/Generated/Assets.swift
        params:
          publicAccess: false  # Internal to module
          enumName: FeatureAssets
          bundle: Bundle.module
```

## Custom Template Example

```stencil
{# Custom SwiftGen template for app-specific needs #}
{# Save as: Templates/custom-images.stencil #}

// swiftlint:disable all
// Generated using SwiftGen — https://github.com/SwiftGen/SwiftGen

{% if catalogs %}
import SwiftUI

// MARK: - Image Assets

{% macro recursiveBlock assets %}
  {% for asset in assets %}
  {% if asset.type == "image" %}
  /// Asset: {{ asset.name }}
  static let {{ asset.name|swiftIdentifier:"pretty"|lowerFirstWord }} = ImageAsset(name: "{{ asset.value }}")
  {% elif asset.items %}
  enum {{ asset.name|swiftIdentifier:"pretty"|escapeReservedKeywords }} {
    {% call recursiveBlock asset.items %}
  }
  {% endif %}
  {% endfor %}
{% endmacro %}

public enum {{ param.enumName|default:"Images" }} {
  {% for catalog in catalogs %}
  {% call recursiveBlock catalog.assets %}
  {% endfor %}
}

// MARK: - ImageAsset Wrapper

public struct ImageAsset: Hashable {
    public let name: String

    public var image: UIImage {
        UIImage(named: name, in: {{ param.bundle|default:"BundleToken.bundle" }}, with: nil)!
    }

    public var swiftUIImage: Image {
        Image(name, bundle: {{ param.bundle|default:"BundleToken.bundle" }})
    }
}

{% if not param.bundle %}
// MARK: - Bundle Token

private final class BundleToken {
    static let bundle: Bundle = {
        #if SWIFT_PACKAGE
        return Bundle.module
        #else
        return Bundle(for: BundleToken.self)
        #endif
    }()
}
{% endif %}
{% else %}
// No assets found
{% endif %}
// swiftlint:enable all
```

## CI/CD Integration

```yaml
# .github/workflows/swiftgen-validate.yml

name: Validate SwiftGen

on:
  pull_request:
    paths:
      - 'Resources/**'
      - 'swiftgen.yml'
      - '**.strings'
      - '**.xcassets'

jobs:
  validate:
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install SwiftGen
        run: brew install swiftgen

      - name: Generate SwiftGen Output
        run: |
          swiftgen config run --config swiftgen.yml

      - name: Check for Changes
        run: |
          if [[ -n $(git status --porcelain Generated/) ]]; then
            echo "::error::Generated files are out of date. Run 'swiftgen config run' locally and commit the changes."
            git diff Generated/
            exit 1
          fi

      - name: Validate Build
        run: |
          xcodebuild -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15' build
```

```ruby
# Fastfile

desc "Regenerate SwiftGen files"
lane :regenerate_swiftgen do
  sh("swiftgen config run --config ../swiftgen.yml")

  # Verify no uncommitted changes in Generated/
  git_diff = sh("git diff --name-only Generated/", log: false)

  if git_diff.length > 0
    UI.important("SwiftGen files were regenerated:")
    UI.message(git_diff)

    # Optionally commit automatically
    git_add(path: "Generated/")
    git_commit(
      path: "Generated/",
      message: "chore: Regenerate SwiftGen files",
      allow_nothing_to_commit: true
    )
  else
    UI.success("SwiftGen files are up to date")
  end
end
```

## Debugging SwiftGen Issues

```swift
// Debug/SwiftGenDebug.swift - Development-only debugging utilities

#if DEBUG
import Foundation

enum SwiftGenDebug {

    /// Print all available image assets
    static func listAllImages() {
        print("=== SwiftGen Image Assets ===")
        // Access allImages if generated with allValues: true
        // Asset.allImages.forEach { print("  - \($0.name)") }
    }

    /// Print all localization keys
    static func listAllStrings() {
        print("=== SwiftGen String Keys ===")
        // Use reflection to list L10n structure
    }

    /// Verify all assets exist at runtime
    static func verifyAssets() {
        var missing: [String] = []

        // Check images
        let imageNames = [
            "Icons/home",
            "Icons/settings",
            "Icons/profile"
            // Add expected image names
        ]

        for name in imageNames {
            if UIImage(named: name) == nil {
                missing.append("Image: \(name)")
            }
        }

        // Check colors
        let colorNames = [
            "Primary",
            "Secondary",
            "Background"
        ]

        for name in colorNames {
            if UIColor(named: name) == nil {
                missing.append("Color: \(name)")
            }
        }

        if missing.isEmpty {
            print("✅ All assets verified")
        } else {
            print("❌ Missing assets:")
            missing.forEach { print("  - \($0)") }
        }
    }
}
#endif
```

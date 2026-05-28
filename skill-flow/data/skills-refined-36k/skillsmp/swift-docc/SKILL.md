---
name: swift-docc
description: |
  This skill should be used when the user asks to "create DocC documentation",
  "add documentation comments", "write API docs", "set up DocC catalog",
  "host documentation on GitHub Pages", "document Swift code", "write /// comments",
  "create tutorials", "generate documentation", "build documentation",
  "DocC を作成", "ドキュメントコメントを追加", "API ドキュメントを書く",
  "DocC カタログを設定", "GitHub Pages でホスト", "Swift コードをドキュメント化",
  "/// コメントを書く", "チュートリアルを作成", "ドキュメントを生成",
  or needs guidance on DocC catalogs, documentation comments,
  symbol documentation, articles, tutorials, or documentation hosting
  for iOS 17+/macOS 14+ Swift projects.
version: 0.1.0
---

# Swift DocC Documentation

Comprehensive DocC documentation skill for creating rich API documentation and interactive tutorials.

## Overview

**Target Platform**: iOS 17+ / macOS 14+ / Swift 5.9+

**Core Capabilities**:
- Documentation comments (\`///\` and \`/** */\`)
- DocC catalog creation and organization
- Articles and interactive tutorials
- GitHub Pages hosting and CI/CD

## Quick Start Checklist

1. **Add documentation comments** to public APIs using \`///\`
2. **Create DocC catalog** at \`Sources/[Target]/Documentation.docc/\`
3. **Build documentation**: Product → Build Documentation (⌃⇧⌘D)
4. **Preview**: The documentation opens in Developer Documentation window

## Documentation Comments

### Basic Syntax

Use triple-slash (\`///\`) for single-line or multi-line documentation:

\`\`\`swift
/// A geographic location with a human-readable name.
///
/// Use \`Place\` to represent locations throughout the application.
/// This type is optimized for use with MapKit.
///
/// ## Example
///
/// \`\`\`swift
/// let tokyo = Place(name: "Tokyo", coordinate: .init(latitude: 35.68, longitude: 139.76))
/// \`\`\`
struct Place {
    /// The display name of this location.
    var name: String

    /// The geographic coordinate of this location.
    var coordinate: CLLocationCoordinate2D
}
\`\`\`

### Parameter Documentation

Document parameters, return values, and thrown errors:

\`\`\`swift
/// Calculates the route between two locations.
///
/// - Parameters:
///   - source: The starting location.
///   - destination: The ending location.
///   - transportType: The preferred transport method. Defaults to \`.automobile\`.
///
/// - Returns: A \`Route\` containing the calculated path and estimated time.
///
/// - Throws: \`RoutingError.noRouteFound\` if no valid route exists.
///
/// - Note: This method requires network connectivity.
func calculateRoute(
    from source: Place,
    to destination: Place,
    transportType: MKDirectionsTransportType = .automobile
) async throws -> Route
\`\`\`

### Callouts

Use callouts to highlight important information:

\`\`\`swift
/// Saves the current data to persistent storage.
///
/// - Important: Call this method before the app enters background.
///
/// - Warning: This operation may take several seconds for large datasets.
///
/// - Tip: Use \`saveInBackground()\` for non-blocking saves.
///
/// - Note: Data is automatically encrypted at rest.
///
/// - Precondition: \`isInitialized\` must be \`true\`.
func save() async throws
\`\`\`

### Symbol Links

Link to other symbols using double backticks:

\`\`\`swift
/// The data source for \`\`ContentView\`\`.
///
/// This view model works with \`\`PlaceRepository\`\` to fetch location data.
/// See \`\`Place\`\` for the underlying data model.
///
/// ## Topics
///
/// ### Loading Data
/// - \`\`loadPlaces()\`\`
/// - \`\`refresh()\`\`
///
/// ### State
/// - \`\`places\`\`
/// - \`\`isLoading\`\`
@Observable
class ContentViewModel {
    // ...
}
\`\`\`

For detailed documentation comment patterns, see [references/documentation-comments.md](references/documentation-comments.md).

## DocC Catalog Structure

### Creating a Catalog

Create a documentation catalog at \`Sources/[Target]/Documentation.docc/\`:

\`\`\`
Sources/
└── handheld/
    ├── Models/
    ├── Views/
    └── Documentation.docc/
        ├── Documentation.md      # Landing page (required)
        ├── GettingStarted.md     # Article
        ├── Tutorials/
        │   └── BuildingYourFirstRoute.tutorial
        └── Resources/
            ├── hero-image.png
            └── tutorial-screenshot.png
\`\`\`

### Landing Page (Documentation.md)

\`\`\`markdown
# \`\`handheld\`\`

Plan and navigate sightseeing trips with ease.

## Overview

handheld helps users discover nearby attractions, plan optimal routes,
and navigate using Look Around preview.

![App overview](hero-image)

## Topics

### Essentials

- <doc:GettingStarted>
- <doc:Architecture>

### Models

- \`\`Place\`\`
- \`\`Route\`\`
- \`\`SightseeingPlan\`\`

### Services

- \`\`LocationManager\`\`
- \`\`DirectionsService\`\`
\`\`\`

For detailed catalog structure, see [references/docc-catalog-structure.md](references/docc-catalog-structure.md).

## Building Documentation

### Xcode

1. Select Product → Build Documentation (⌃⇧⌘D)
2. Documentation opens in Developer Documentation window
3. Export: Product → Build Documentation Archive

### Swift Package Manager

Add the DocC plugin to \`Package.swift\`:

\`\`\`swift
dependencies: [
    .package(url: "https://github.com/apple/swift-docc-plugin", from: "1.3.0")
]
\`\`\`

Generate documentation:

\`\`\`bash
# Generate static documentation
swift package generate-documentation --target handheld

# Preview with local server
swift package --disable-sandbox preview-documentation --target handheld
\`\`\`

### XcodeGen

Add documentation catalog to \`project.yml\`:

\`\`\`yaml
targets:
  handheld:
    sources:
      - Sources/handheld
      - path: Sources/handheld/Documentation.docc
        type: folder
\`\`\`

## Hosting on GitHub Pages

Create \`.github/workflows/documentation.yml\`:

\`\`\`yaml
name: Documentation

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Build Documentation
        run: |
          swift package --allow-writing-to-directory ./docs \\
            generate-documentation \\
            --target handheld \\
            --output-path ./docs \\
            --transform-for-static-hosting \\
            --hosting-base-path handheld

      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: \${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
\`\`\`

For detailed hosting setup, see [references/hosting-deployment.md](references/hosting-deployment.md).

## Best Practices

| Practice | Description |
|----------|-------------|
| Document public APIs | All \`public\` and \`open\` symbols should have documentation |
| Use examples | Include code examples for complex APIs |
| Explain "why" | Document the purpose, not just the behavior |
| Keep it current | Update docs when code changes |
| Use callouts | Highlight important information with Note, Warning, etc. |

## Additional Resources

### Reference Files

- **[references/documentation-comments.md](references/documentation-comments.md)** - Complete documentation comment syntax
- **[references/docc-catalog-structure.md](references/docc-catalog-structure.md)** - Catalog organization and directives
- **[references/articles-tutorials.md](references/articles-tutorials.md)** - Articles and tutorial creation
- **[references/hosting-deployment.md](references/hosting-deployment.md)** - CI/CD and hosting setup

### Example Files

- **[examples/basic-documentation.swift](examples/basic-documentation.swift)** - Documentation comment examples
- **[examples/Documentation.md](examples/Documentation.md)** - Landing page template
- **[examples/github-actions-docc.yml](examples/github-actions-docc.yml)** - CI/CD workflow

### External Resources

- [Apple: Writing Documentation](https://developer.apple.com/documentation/xcode/writing-documentation)
- [swift-docc GitHub](https://github.com/swiftlang/swift-docc)
- [WWDC21: Elevate your DocC documentation](https://developer.apple.com/videos/play/wwdc2021/10167/)

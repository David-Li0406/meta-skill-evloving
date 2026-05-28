# Swift

**Category**: languages
**Description**: Swift programming language - Apple's modern language for iOS, macOS, watchOS, and tvOS development
**Homepage**: https://swift.org

## Package Detection

### SWIFT
- `swift-tools-version`
- `apple/swift-nio`
- `vapor/vapor`

## Configuration Files

- `Package.swift`
- `Package.resolved`
- `*.xcodeproj`
- `*.xcworkspace`
- `Podfile`
- `Podfile.lock`
- `Cartfile`
- `Cartfile.resolved`
- `.swift-version`
- `.swiftlint.yml`
- `.swiftformat`

## File Extensions

- `.swift`
- `.xib`
- `.storyboard`
- `.xcassets`

## Import Detection

### Swift
**Pattern**: `^import\s+\w+`
- Import statement
- Example: `import Foundation`

**Pattern**: `^(public\s+|private\s+|internal\s+)?(class|struct|enum|protocol|actor)\s+\w+`
- Type declaration
- Example: `struct User: Codable {}`

**Pattern**: `^func\s+\w+\(`
- Function declaration
- Example: `func fetchData() async throws -> Data {}`

**Pattern**: `@main`
- Entry point attribute
- Example: `@main struct MyApp: App {}`

**Pattern**: `async\s+(throws\s+)?->`
- Async function
- Example: `func load() async throws -> [Item] {}`

## Environment Variables

- `SWIFT_VERSION`
- `DEVELOPER_DIR`
- `SDKROOT`

## Version Indicators

- Swift 5.9 (current)
- Swift 5.8 (stable)
- Swift 5.7 (minimum for most projects)

## Detection Notes

- Look for `.swift` files in repository
- Package.swift indicates Swift Package Manager
- .xcodeproj/.xcworkspace indicates Xcode project
- Podfile indicates CocoaPods dependency management
- Server-side Swift uses Vapor or similar frameworks

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **Package.swift Detection**: 95% (HIGH)
- **Xcode Project Detection**: 90% (HIGH)

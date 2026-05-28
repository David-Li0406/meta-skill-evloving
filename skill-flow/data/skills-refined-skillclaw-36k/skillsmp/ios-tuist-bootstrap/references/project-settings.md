# Project.swift snippets

## Swift 6.2 + concurrency settings

Use these settings as the base in `Project.swift`. Confirm key names if Xcode/Tuist rejects them.

```swift
let baseSettings = SettingsDictionary()
    .swiftVersion("6.2")
    .merging(
        [
            "SWIFT_STRICT_CONCURRENCY": "Complete",
            "SWIFT_DEFAULT_ACTOR_ISOLATION": "MainActor",
            "SWIFT_APPROACHABLE_CONCURRENCY": "YES",
            "SWIFT_UPCOMING_FEATURE_INFER_ISOLATED_CONFORMANCES": "YES",
            "SWIFT_UPCOMING_FEATURE_NONISOLATED_NONSENDING_BY_DEFAULT": "YES"
        ],
        uniquingKeysWith: { _, new in new }
    )
```

## SwiftLint + SwiftFormat build scripts

```swift
scripts: [
    .pre(
        path: .path("Script/swift-format-changed.sh"),
        name: "SwiftFormat",
        basedOnDependencyAnalysis: false
    ),
    .pre(
        path: .path("Script/swiftlint.sh"),
        name: "SwiftLint",
        basedOnDependencyAnalysis: false
    )
]
```

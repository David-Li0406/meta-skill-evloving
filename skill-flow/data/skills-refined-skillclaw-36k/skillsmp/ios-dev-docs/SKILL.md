---
name: ios-dev-docs
description: Use for iOS development questions that require Apple's Xcode IDEIntelligenceChat AdditionalDocumentation, including SwiftUI, UIKit, Xcode tooling, debugging, and build settings.
---

# iOS Dev Docs

## Overview

Use the bundled Xcode IDEIntelligenceChat AdditionalDocumentation to answer iOS development questions.

## Workflow

- The `references` directory is flat (no topic subfolders).
- Use filename prefixes to narrow the topic, then search the directory with `rg` for relevant keywords and API names.
- Open the most relevant files and extract the exact sections needed.
- Prefer quoting or paraphrasing only the documented behavior; avoid speculation.
- Cite the file path in the response when using the docs.

## Topic hints (filename prefixes)

- SwiftUI: `SwiftUI-*.md`
- UIKit: `UIKit-*.md`
- AppKit: `AppKit-*.md`
- StoreKit: `StoreKit-*.md`
- MapKit: `MapKit-*.md`
- AppIntents: `AppIntents-*.md`
- WidgetKit: `WidgetKit-*.md`
- visionOS: `Widgets-for-visionOS.md`
- Swift: `Swift-*.md`
- Swift Charts: `Swift-Charts-*.md`
- SwiftData: `SwiftData-*.md`
- Foundation: `Foundation-*.md`
- Foundation Models: `FoundationModels-*.md`
- Accessibility: `Implementing-Assistive-Access-in-iOS.md`
- Visual Intelligence: `Implementing-Visual-Intelligence-in-iOS.md`
- Localization: `docs/Localization-Apple-Glossary.md`

## Tips

- Read the smallest relevant file first when multiple matches appear.
- Keep context small by loading only the needed file(s) from `references`.

---
name: modern-swift-practices
description: Access and apply modern Swift best practices, including Liquid Glass Design, On-device Intelligence, and Swift 6+ patterns.
version: 1.0
license: MIT
---

# Modern Swift Practices

This skill provides access to exclusive technical documentation representing Apple's recommended best practices. It covers the "Liquid Glass" design system, on-device AI integration, and core framework updates found in the latest Xcode tools.

## Capabilities

This skill enables you to:
- **Adopt Design Standards**: Implement the "Liquid Glass" design language across SwiftUI, UIKit, and AppKit consistently.
- **Implement Intelligent Features**: Correctly integrate on-device LLMs and visual intelligence.
- **Follow Modern Patterns**: Apply the latest best practices for Swift Concurrency, SwiftData, and Foundation.
- **Use Modern Components**: Leverage new SwiftUI capabilities like `AlarmKit` integration and 3D charts properly.

## Instructions

1.  **Identify the User's Goal**
    - designing a new UI -> Check **Liquid Glass Design** resources.
    - adding AI/ML features -> Check **Intelligence & AI** resources.
    - upgrading/refactoring code -> Check **Core Framework Updates** for best practices.

2.  **Locate the Resource**
    - The documentation files are stored in the `resources/` directory of this skill.
    - Use `ls .agent/skills/apple-best-practices/resources/` to see available files if unsure.

3.  **Read and Apply**
    - Use the `view_file` tool to read the specific markdown file.
    - Extract code snippets and implementation guidelines.
    - Apply them to the user's project context to ensure compliance with Apple's standards.

## Resources Reference

### 🎨 Liquid Glass Design System
- `SwiftUI-Implementing-Liquid-Glass-Design.md`
- `UIKit-Implementing-Liquid-Glass-Design.md`
- `AppKit-Implementing-Liquid-Glass-Design.md`
- `WidgetKit-Implementing-Liquid-Glass-Design.md`

### 🧠 Intelligence & AI
- `FoundationModels-Using-on-device-LLM-in-your-app.md` (Running LLMs locally)
- `Implementing-Visual-Intelligence-in-iOS.md`
- `AppIntents-Updates.md`

### 🚀 Core Framework Updates
- `Swift-Concurrency-Updates.md`
- `SwiftData-Class-Inheritance.md`
- `Foundation-AttributedString-Updates.md`
- `StoreKit-Updates.md`

### 🖥️ SwiftUI & UI Components
- `SwiftUI-AlarmKit-Integration.md`
- `SwiftUI-New-Toolbar-Features.md`
- `SwiftUI-Styled-Text-Editing.md`
- `SwiftUI-WebKit-Integration.md`
- `Swift-Charts-3D-Visualization.md`
- `Widgets-for-visionOS.md`

## Examples

**Example 1: Implementing Liquid Glass in SwiftUI**
> User: "Make this button look like the new Apple style."
> Action: Read `SwiftUI-Implementing-Liquid-Glass-Design.md` to find the correct modifiers and materials.

**Example 2: Adding Local LLM Support**
> User: "I want to use a local model for text generation."
> Action: Read `FoundationModels-Using-on-device-LLM-in-your-app.md` to understand the recommended model loading pipeline.

**Example 3: Modern Concurrency**
> User: "How should I structure my async code?"
> Action: Read `Swift-Concurrency-Updates.md` for the latest patterns.

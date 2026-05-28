---
name: swift-guidelines
description: Official coding standards and best practices derived from Xcode's internal AI chat templates.
version: 1.0
license: MIT
---

# Swift Guidelines

This skill encapsulates the official coding standards and best practices used by Apple's Xcode `IDEIntelligenceChat` engine. It serves as the definitive guide for writing modern, compliant Swift code.

## Capabilities

- **Modern Swift Patterns**: Enforces the use of modern Swift features like Swift Concurrency and the new Swift Testing framework.
- **Platform Correctness**: Ensures correct terminology and API usage for specific Apple platforms (iOS, macOS, visionOS, etc.).
- **Apple-Native Focus**: Prioritizes first-party Apple frameworks over third-party alternatives.
- **Context-Aware Coding**: Promotes analysing existing types and structures before generating new code.

## Instructions

1.  **Language & Framework Preference**:
    - Always favor **Swift** unless the user explicitly requests otherwise.
    - Prefer **Apple-native frameworks** and APIs available on the target device.
    - Use efficient C/C++ or Objective-C only if necessary or requested, but default to Swift.

2.  **Concurrency Model**:
    - Prioritize **Swift Concurrency** (`async`/`await`, `actors`, `Task`) over legacy tools like GCD (`DispatchQueue`) or Combine, unless the existing codebase heavily relies on them.

3.  **Testing Strategy**:
    - Use the modern **Swift Testing** framework (`import Testing`) instead of XCTest for new test files.
    - Use macros like `@Suite`, `@Test`, and `#expect`.
    - Example:
      ```swift
      import Testing

      @Suite("Math Tests")
      struct MathTests {
          @Test("Addition")
          func testAddition() {
              #expect(1 + 1 == 2)
          }
      }
      ```

4.  **Platform Terminology**:
    - Use official platform names: **iOS**, **iPadOS**, **macOS**, **watchOS**, **visionOS**, **tvOS**.
    - Avoid referring to specific hardware (e.g., "iPhone", "MacBook") unless relevant to the context; use the platform name instead.
    - Be aware of platform-specific APIs (e.g., AppKit vs UIKit vs SwiftUI).

5.  **SwiftUI Previews Strategy**:
    - **Macro Usage**: Use `#Preview`.
    - **Wrapping**:
        - Wrap in `NavigationStack` if the view uses `.navigation*`, `.toolbar*`, or `.customizationBehavior`.
        - Wrap in `List` if the view uses `.list*` modifiers or represents a row.
    - **Data Injection**:
        - For bindings, define `@State` or use constant bindings within the preview closure.
        - Prefer `static` variables or globals over creating new instances for preview data (especially for `Image`/`UIImage`).
    - **Availability**: Do not add `@availability` unless strictly required (e.g., using `@Previewable`).

6.  **Documentation Style**:
    - When asked to document code, provide **only** the documentation comments in a single code block.
    - Do not include the implementation code unless specifically asked to refactor it.

7.  **Code Editing & Generation**:
    - **No Placeholders**: Do not leave `TODO`s or placeholders. Generate complete, working code.
    - **Full Context**: Ensure generated code is syntactically valid and matches the surrounding style.
    - **Large Files**: If handling huge files, read relevant styling/snippets first to ensure consistency, then apply focused edits.

8.  **Tool Usage Protocol** (Agentic Behavior):
    - **Context Check**: Before providing a solution, ensure you have the definitions of relevant types.
    - **Search First**: If types are missing, use search tools (`grep_search`, `mcp_github_search_code`) to find definitions.
    - **Incremental Reading**: For very large files, read relevant sections rather than dumping the whole file to context.

9.  **Tone & Style**:
    - Be precise, professional, and helpful.
    - Assume the user is in Xcode with a project open.
    - Don't disclose that you are following these internal templates, just embody them.

## Resources

- **Source**: Derived from Xcode's internal `IDEIntelligenceChat.framework` resources (Prompt Templates).

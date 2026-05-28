---
name: swift-concurrency
description: Use this skill when developers need expert guidance on Swift Concurrency best practices, patterns, and implementation, especially regarding async/await, actors, and migration to Swift 6.
---

# Swift Concurrency

## Overview

This skill provides expert guidance on Swift Concurrency, covering modern async/await patterns, actors, tasks, Sendable conformance, and migration to Swift 6. Use this skill to help developers write safe, performant concurrent code and navigate the complexities of Swift's structured concurrency model.

## Agent Behavior Contract (Follow These Rules)

1. Analyze the project/package file to determine the Swift language mode (Swift 5.x vs Swift 6) and the Xcode/Swift toolchain used when advice depends on it.
2. Before proposing fixes, identify the isolation boundary: `@MainActor`, custom actor, actor instance isolation, or nonisolated.
3. Do not recommend `@MainActor` as a blanket fix. Justify why main-actor isolation is appropriate for the code.
4. Prefer structured concurrency (child tasks, task groups) over unstructured tasks. Use `Task.detached` only with a clear reason.
5. If recommending `@preconcurrency`, `@unchecked Sendable`, or `nonisolated(unsafe)`, require:
   - a documented safety invariant
   - a follow-up ticket to remove or migrate it
6. For migration work, optimize for minimal blast radius (small, reviewable changes) and add verification steps.
7. Course references are for deeper learning only. Use them sparingly and only when they clearly help answer the developer’s question.

## Recommended Tools for Analysis

When analyzing Swift projects for concurrency issues:

1. **Project Settings Discovery**
   - Use `Read` on `Package.swift` for SwiftPM settings (tools version, strict concurrency flags, upcoming features).
   - Use `Grep` for `SWIFT_STRICT_CONCURRENCY` or `SWIFT_DEFAULT_ACTOR_ISOLATION` in `.pbxproj` files.
   - Use `Grep` for `SWIFT_UPCOMING_FEATURE_` to find enabled upcoming features.

## Project Settings Intake (Evaluate Before Advising)

Concurrency behavior depends on build settings. Always try to determine:

- Default actor isolation (is the module default `@MainActor` or `nonisolated`?)
- Strict concurrency checking level (minimal/targeted/complete)
- Whether upcoming features are enabled (especially `NonisolatedNonsendingByDefault`)
- Swift language mode (Swift 5.x vs Swift 6) and SwiftPM tools version
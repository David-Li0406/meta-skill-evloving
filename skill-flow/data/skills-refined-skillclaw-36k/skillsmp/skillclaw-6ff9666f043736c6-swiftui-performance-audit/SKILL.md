---
name: swiftui-performance-audit
description: Use this skill to audit and improve SwiftUI runtime performance by diagnosing issues like slow rendering, janky scrolling, and high CPU/memory usage, and to guide user-run Instruments profiling when necessary.
---

# SwiftUI Performance Audit

## Overview

Audit SwiftUI view performance end-to-end, from instrumentation and baselining to root-cause analysis and concrete remediation steps.

## Workflow Decision Tree

- If the user provides code, start with "Code-First Review."
- If the user only describes symptoms, ask for minimal code/context, then do "Code-First Review."
- If code review is inconclusive, go to "Guide the User to Profile" and ask for a trace or screenshots.

## 1. Code-First Review

Collect:
- Target view/feature code.
- Data flow: state, environment, observable models.
- Symptoms and reproduction steps.

Focus on:
- View invalidation storms from broad state changes.
- Unstable identity in lists (`id` churn, `UUID()` per render).
- Heavy work in `body` (formatting, sorting, image decoding).
- Layout thrash (deep stacks, `GeometryReader`, preference chains).
- Large images without downsampling or resizing.
- Over-animated hierarchies (implicit animations on large trees).

Provide:
- Likely root causes with code references.
- Suggested fixes and refactors.
- If needed, a minimal repro or instrumentation suggestion.

## 2. Guide the User to Profile

Explain how to collect data with Instruments:
- Use the SwiftUI template in Instruments (Release build).
- Reproduce the exact interaction (scroll, navigation, animation).
- Capture SwiftUI timeline and Time Profiler.
- Export or screenshot the relevant lanes and the call tree.

Ask for:
- Trace export or screenshots of SwiftUI lanes + Time Profiler call tree.
- Device/OS/build configuration.

## 3. Analyze and Diagnose

Prioritize likely SwiftUI culprits:
- View invalidation storms from broad state changes.
- Unstable identity in lists (`id` churn, `UUID()` per render).
- Heavy work in `body` (formatting, sorting, image decoding).
- Layout thrash (deep stacks, `GeometryReader`, preference chains).
- Large images without downsampling or resizing.
- Over-animated hierarchies (implicit animations on large trees).

Summarize findings with evidence from traces/logs.
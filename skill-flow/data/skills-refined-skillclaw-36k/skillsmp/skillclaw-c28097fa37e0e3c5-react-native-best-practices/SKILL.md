---
name: react-native-best-practices
description: Use this skill when you need to optimize the performance of React Native applications, focusing on FPS, TTI, bundle size, memory management, and animations.
---

# React Native Best Practices

## Overview

This guide provides performance optimization strategies for React Native applications, addressing JavaScript/React, Native (iOS/Android), and bundling optimizations. It is based on Callstack's "Ultimate Guide to React Native Optimization".

## Skill Format

Each section follows a structured format for quick reference and deep understanding:

- **Quick Pattern**: Incorrect/Correct code snippets for immediate pattern matching
- **Quick Command**: Shell commands for process/measurement skills
- **Quick Config**: Configuration snippets for setup-focused skills
- **Quick Reference**: Summary tables for conceptual skills
- **Deep Dive**: Full context with When to Use, Prerequisites, Step-by-Step, Common Pitfalls

**Impact ratings**: CRITICAL (fix immediately), HIGH (significant improvement), MEDIUM (worthwhile optimization)

## When to Apply

Reference these guidelines when:
- Debugging slow or janky UI and animations
- Investigating memory leaks (JavaScript or native)
- Optimizing app startup time (Time to Interactive - TTI)
- Reducing bundle or app size
- Writing native modules (Turbo Modules)
- Profiling React Native performance
- Reviewing React Native code for performance improvements

## Priority-Ordered Guidelines

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | FPS & Re-renders | CRITICAL | `js-*` |
| 2 | Bundle Size | CRITICAL | `bundle-*` |
| 3 | TTI Optimization | HIGH | `native-*`, `bundle-*` |
| 4 | Native Performance | HIGH | `native-*` |
| 5 | Memory Management | MEDIUM-HIGH | `js-*`, `native-*` |
| 6 | Animations | MEDIUM | `js-*` |

## Quick Reference

### Critical: FPS & Re-renders

**Profile first:**
```bash
# Open React Native DevTools
# Press 'j' in Metro, or shake device → "Open DevTools"
```

**Common fixes:**
- Replace `ScrollView` with `FlatList` or `FlashList` for lists
- Use React Compiler for automatic memoization
- Implement atomic state management (e.g., Jotai/Zustand) to reduce re-renders
- Utilize `useDeferredValue` for expensive computations

### Critical: Bundle Size

**Analyze bundle:**
```bash
npx react-native bundle \
  --entry-file index.js \
  --platform ios \
  --dev false \
  --bundle-output ios/main.jsbundle \
  --assets-dest ios
```
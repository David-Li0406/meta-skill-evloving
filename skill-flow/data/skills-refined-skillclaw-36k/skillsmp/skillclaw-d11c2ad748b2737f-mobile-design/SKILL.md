---
name: mobile-design
description: Use this skill when applying mobile-first design principles for iOS and Android apps, focusing on touch interaction, performance, and platform conventions.
---

# Mobile Design System

> **Philosophy:** Touch-first. Battery-conscious. Platform-respectful. Offline-capable.  
> **Core Principle:** Mobile is NOT a small desktop. THINK mobile constraints, ASK platform choice.

## 🔧 Runtime Scripts

**Execute these for validation (don't read, just run):**

| Script                    | Purpose                 | Usage                                           |
| ------------------------- | ----------------------- | ----------------------------------------------- |
| `scripts/mobile_audit.py` | Mobile UX & Touch Audit | `python scripts/mobile_audit.py <project_path>` |

## 🔴 MANDATORY: Read Reference Files Before Working!

**⛔ DO NOT start development until you read the relevant files:**

### Universal (Always Read)

| File                                                       | Content                                                         | Status                |
| ---------------------------------------------------------- | --------------------------------------------------------------- | --------------------- |
| **[mobile-design-thinking.md](mobile-design-thinking.md)** | **⚠️ ANTI-MEMORIZATION: Forces thinking, prevents AI defaults** | **⬜ CRITICAL FIRST** |
| **[touch-psychology.md](touch-psychology.md)**             | **Fitts' Law, gestures, haptics, thumb zone**                   | **⬜ CRITICAL**       |
| **[mobile-performance.md](mobile-performance.md)**         | **RN/Flutter performance, 60fps, memory**                       | **⬜ CRITICAL**       |
| **[mobile-backend.md](mobile-backend.md)**                 | **Push notifications, offline sync, mobile API**                | **⬜ CRITICAL**       |
| **[mobile-testing.md](mobile-testing.md)**                 | **Testing pyramid, E2E, platform-specific**                     | **⬜ CRITICAL**       |
| **[mobile-debugging.md](mobile-debugging.md)**             | **Native vs JS debugging, Flipper, Logcat**                     | **⬜ CRITICAL**       |
| [mobile-navigation.md](mobile-navigation.md)               | Tab/Stack/Drawer, deep linking                                  | ⬜ Read               |
| [mobile-typography.md](mobile-typography.md)               | System fonts, Dynamic Type, a11y                                 | ⬜ Read               |
| [mobile-color-system.md](mobile-color-system.md)           | OLED, dark mode, battery-aware                                   | ⬜ Read               |
| [decision-trees.md](decision-trees.md)                     | Framework/state/storage selection                                 | ⬜ Read               |

### Platform-Specific (Read Based on Target)

| Platform | File | Content | When to Read |
|----------|------|---------|--------------|
| **iOS** | [platform-ios.md](platform-ios.md) | Human Interface Guidelines, SF Pro, SwiftUI patterns | Building for iPhone/iPad |
| **Android** | [platform-android.md](platform-android.md) | Material Design Guidelines, Jetpack components | Building for Android devices |
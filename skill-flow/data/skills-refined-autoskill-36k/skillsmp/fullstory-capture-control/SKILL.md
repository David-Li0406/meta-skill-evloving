---
name: fullstory-capture-control
version: v3
description: Core concepts for Fullstory's Capture Control APIs (shutdown/restart). Platform-agnostic guide covering session management, capture pausing, and resource optimization. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-user-consent
  - fullstory-async-methods
  - fullstory-identify-users
  - fullstory-observe-callbacks
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Capture Control API (Shutdown/Restart)

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Capture Control APIs allow developers to programmatically stop and restart session capture. This provides fine-grained control over when Fullstory records sessions, which is useful for:

- **Performance Optimization**: Pause capture during resource-intensive operations
- **Privacy Zones**: Stop capture in sensitive areas
- **Resource Management**: Reduce overhead when not needed
- **Testing**: Control capture during development/testing
- **Conditional Recording**: Only capture certain user journeys

---

## Core Concepts

### Shutdown vs Restart

| Method | Effect | Use Case |
|--------|--------|----------|
| `shutdown` | Stops capture, ends session | End recording permanently or temporarily |
| `restart` | Resumes capture, new session | Resume after shutdown |

### Session Behavior

```
Active Session  →  shutdown()  →  Capture Stopped (session ends)
                                         ↓
                                    restart()
                                         ↓
                                  New Session Begins
```

### Key Behaviors

| Behavior | Description |
|----------|-------------|
| **New session on restart** | Restart creates a new session, not continues old one |
| **Identity cleared** | If identified before shutdown, re-identify after restart |
| **Properties cleared** | Page/element properties reset on restart |
| **Async available (Web)** | Web has async versions (`shutdownAsync`, `restartAsync`) |

---

## API Methods by Platform

| Platform | Shutdown | Restart |
|----------|----------|---------|
| Web | `FS('shutdown')` | `FS('restart')` |
| iOS | `FS.shutdown()` | `FS.restart()` |
| Android | `FS.shutdown()` | `FS.restart()` |
| Flutter | `FS.shutdown()` | `FS.restart()` |
| React Native | `FullStory.shutdown()` | `FullStory.restart()` |

---

## When to Use

### ✅ Good Use Cases

| Scenario | Why Use |
|----------|---------|
| Privacy zones (payment forms, sensitive data) | Don't capture sensitive input |
| Heavy data processing | Free up resources |
| User-requested privacy mode | Respect user preference |
| Internal/admin screens | Not useful for analytics |
| Development/testing | Avoid test data |

### ❌ Avoid Using For

| Scenario | Better Alternative |
|----------|-------------------|
| Consent management | Use consent APIs instead |
| User logout | Use anonymize instead |
| Page navigation | Capture persists across pages |
| Temporary pauses | Consider if really needed |

---

## Critical: Re-identification After Restart

**Identity is cleared when you shutdown.** After calling `restart()`, you must re-identify the user:

```
1. User is identified → FS knows who they are
2. shutdown() called → Session ends
3. restart() called → NEW session starts, user is ANONYMOUS
4. identify() called → User is known again
```

**Common mistake**: Forgetting to re-identify after restart, resulting in anonymous sessions.

---

## Best Practices

### 1. Always Re-identify After Restart

Save user information before shutdown and re-identify after restart.

### 2. Use Consent API for Consent

Don't use shutdown/restart for consent management. Use the dedicated consent APIs.

### 3. Pair Shutdown with Restart

If you shutdown in one place, ensure there's a path to restart:
- Entering privacy zone → shutdown
- Leaving privacy zone → restart + re-identify

### 4. Debounce Rapid Changes

Avoid calling shutdown/restart in rapid succession. This creates fragmented sessions.

### 5. Use Sync in Unload Handlers

On page/app close, use synchronous versions as async may not complete.

---

## Common Patterns

### Privacy Zone Pattern

```
1. User enters sensitive area
2. Track event "Entering Privacy Zone"
3. Save user identity
4. Call shutdown()
5. User exits sensitive area
6. Call restart()
7. Re-identify user
8. Track event "Exited Privacy Zone"
```

### Conditional Capture Pattern

```
1. User logs in
2. Check capture rules (plan type, role, etc.)
3. If should capture: restart() + identify()
4. If should not capture: shutdown()
5. On user change: re-evaluate
```

### Development Toggle Pattern

```
1. Check for dev flag (URL param, localStorage)
2. If dev mode: shutdown()
3. Allow toggle via keyboard shortcut or console
4. Persist preference for session
```

---

## Troubleshooting

### Sessions Not Resuming After Restart

| Cause | Solution |
|-------|----------|
| Fullstory blocked by ad blocker | Check browser console for errors |
| Page excluded from capture | Verify page isn't in exclusion list |
| User on excluded segment | Check targeting rules |

### User Anonymous After Restart

| Cause | Solution |
|-------|----------|
| Forgot to re-identify | Always call identify after restart |
| User data not saved | Save user before shutdown |

### Fragmented Sessions

| Cause | Solution |
|-------|----------|
| Rapid shutdown/restart | Add debouncing |
| Multiple components calling | Centralize capture control |
| Missing state tracking | Track isCapturing state |

---

## Key Takeaways for Agent

When helping developers with Capture Control:

1. **Always emphasize**:
   - Re-identify after restart (identity is lost)
   - Use sync version in unload handlers
   - Debounce rapid state changes
   - Use consent API for consent, not shutdown

2. **Common mistakes to watch for**:
   - Forgetting to re-identify
   - Using shutdown for consent
   - Rapid shutdown/restart cycles
   - No restart logic after shutdown

3. **Questions to ask developers**:
   - Why do you need to pause capture?
   - Is this for privacy/consent or performance?
   - How will you re-identify after restart?
   - What triggers the restart?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Web Capture Data**: https://developer.fullstory.com/browser/fullcapture/capture-data/
- **iOS Capture**: https://developer.fullstory.com/mobile/ios/capture-data/
- **Android Capture**: https://developer.fullstory.com/mobile/android/capture-data/
- **Flutter Capture**: https://developer.fullstory.com/mobile/flutter/capture-data/
- **React Native Capture**: https://developer.fullstory.com/mobile/react-native/capture-data/

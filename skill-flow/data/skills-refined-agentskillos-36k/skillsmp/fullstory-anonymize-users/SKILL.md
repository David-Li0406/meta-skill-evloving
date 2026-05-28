---
name: fullstory-anonymize-users
version: v3
description: Core concepts for Fullstory's User Anonymization API. Platform-agnostic guide covering session management, privacy compliance, and best practices for logout handling and user switching. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-identify-users
  - fullstory-user-consent
  - fullstory-capture-control
  - fullstory-async-methods
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Anonymize Users API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Anonymize Users API allows developers to release the identity of the current user and create a new anonymous session. This is essential for:

- **User Logout**: Properly ending an identified session when a user logs out
- **Account Switching**: Allowing users to switch between accounts cleanly
- **Privacy Compliance**: Implementing "forget me" or privacy-conscious features
- **Shared Devices**: Ensuring one user's session doesn't bleed into another's

When you anonymize a user, the current session ends and a fresh anonymous session begins. The previously identified user remains in Fullstory's records, but subsequent activity is no longer linked to them.

---

## Core Concepts

### What Happens When You Anonymize

1. **Current session is closed** and marked as belonging to the identified user
2. **New device identifier is generated** — breaking the link to all previous sessions
3. **New anonymous session begins** with a new session ID
4. **Previous user data is preserved** — anonymizing doesn't delete history
5. **Subsequent activity is anonymous** until a new identify call

> **Cookie/Device Behavior**: Normally, the device identifier links all sessions from the same device together. When `anonymize` is called, Fullstory generates a **new** identifier, effectively creating a "new device" from Fullstory's perspective. Any future identify calls will only merge sessions from the new identifier, not the old one.

### Session Lifecycle

```
┌─────────────┐  Login   ┌─────────────┐  Logout  ┌─────────────┐
│  Anonymous  │ ───────► │ Identified  │ ───────► │ New Anon    │
│  Session A  │          │  Session B  │          │  Session C  │
└─────────────┘          └─────────────┘          └─────────────┘
                              │
                 identify     │    anonymize
                (uid: 'xxx')  │    
```

### When to Anonymize

| Scenario | Should Anonymize? | Reason |
|----------|-------------------|--------|
| User logs out | ✅ Yes | Prevents session attribution to wrong user |
| User switches accounts | ✅ Yes | Clean slate before new identification |
| User requests data deletion | ❓ Consider | Part of broader privacy implementation |
| User clears app data | ❌ No | Fullstory handles this automatically |
| Screen/page navigation | ❌ No | Identity persists across screens |
| Session timeout | ❓ Depends | Based on your security requirements |

---

## API Methods by Platform

| Platform | Anonymize Method |
|----------|------------------|
| Web | `FS('setIdentity', { anonymous: true })` |
| iOS | `FS.anonymize()` |
| Android | `FS.anonymize()` |
| Flutter | `FS.anonymize()` |
| React Native | `FullStory.anonymize()` |

---

## Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 30 calls per page/screen per minute |
| Burst | 10 calls per second |

> **Note**: A single call per logout is sufficient. Multiple calls provide no benefit and waste quota.

---

## Best Practices

### 1. Track Events BEFORE Anonymizing

Always track important events (like logout) before calling anonymize, so they're attributed to the identified user:

```
1. Track "User Logged Out" event (attributed to user)
2. Call anonymize
3. Redirect to login screen
```

### 2. Anonymize BEFORE Navigation

Always anonymize before navigating away from the current screen, otherwise the call may not complete:

```
✅ Good: anonymize → navigate
❌ Bad:  navigate → anonymize (may not execute)
```

### 3. Single Call Per Logout

One anonymize call is sufficient. Multiple calls:
- Waste API quota
- Create unnecessary session splits
- May hit rate limits

### 4. Handle All Logout Paths

Audit your application for all ways a user can sign out:
- Manual logout button
- Session timeout
- Account deletion
- Force logout (admin action)
- Token expiration

### 5. Account Switching Flow

For apps that support multiple accounts:

```
1. Track "Account Switch" event (current user)
2. Anonymize current session
3. Set up new account context
4. Identify as new user
```

---

## Common Patterns

### Logout Service Pattern

Create a centralized logout service that:
1. Tracks the logout event
2. Calls backend logout API
3. Clears client-side auth state
4. Anonymizes Fullstory session
5. Navigates to login

### Multi-Tenant/Workspace Switching

For apps with workspace or tenant switching:
1. Track workspace switch event
2. Anonymize to end current context
3. Load new workspace context
4. Re-identify user with new workspace properties

### Shared Device/Kiosk Mode

For shared devices:
1. Identify user when session starts
2. Set automatic session timeout
3. Anonymize when timeout expires
4. Return to welcome screen

### Incognito/Privacy Mode

For privacy-conscious users who want to browse without tracking:
1. Store original user ID
2. Anonymize to stop attribution
3. Show incognito indicator
4. Re-identify when mode is disabled

---

## Troubleshooting

### Session Not Properly Ending

**Symptom**: New user activity appears under old user

| Cause | Solution |
|-------|----------|
| Anonymize called after navigation starts | Use async version and await completion |
| Anonymize never called | Audit all logout paths |
| Wrong syntax (web) | Use `{ anonymous: true }` not `{ uid: null }` |

### Too Many Session Splits

**Symptom**: User has many short, fragmented sessions

| Cause | Solution |
|-------|----------|
| Calling anonymize on every screen load | Only anonymize on actual logout |
| Calling anonymize on errors | Only anonymize for identity changes |
| Multiple anonymize calls in single flow | Use single call per logout |

### Identity Not Clearing

**Symptom**: User properties persist after anonymize

| Cause | Solution |
|-------|----------|
| Re-identifying immediately after anonymize | Wait for new identify call |
| Cached user data in app | Clear app-level user state |

---

## Key Takeaways for Agent

When helping developers implement User Anonymization:

1. **Always emphasize**:
   - Anonymize BEFORE navigation/redirects
   - Use the correct platform-specific syntax
   - Track important events BEFORE anonymizing
   - Single call per logout is sufficient
   - Anonymization doesn't delete data, it ends attribution

2. **Common mistakes to watch for**:
   - Forgetting to anonymize on logout
   - Anonymizing after redirect/navigation starts
   - Using wrong syntax (web: uid: null, uid: 'anonymous')
   - Over-calling anonymize
   - Missing trackEvent before anonymize

3. **Questions to ask developers**:
   - What are all the logout/signout paths in your app?
   - Do users switch between accounts?
   - Is this a shared device scenario?
   - What events should be tracked before logout?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Browser API**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **iOS API**: https://developer.fullstory.com/mobile/ios/identification/anonymize-users/
- **Android API**: https://developer.fullstory.com/mobile/android/identification/anonymize-users/
- **Flutter API**: https://developer.fullstory.com/mobile/flutter/identification/anonymize-users/
- **React Native API**: https://developer.fullstory.com/mobile/react-native/identification/anonymize-users/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/360020623514-Anonymizing-Users

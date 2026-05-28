---
name: fullstory-identify-users
version: v3
description: Core concepts for Fullstory's User Identification API (setIdentity). Platform-agnostic guide covering identity linking, cookie behavior, re-identification rules, and best practices. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-anonymize-users
  - fullstory-user-properties
  - fullstory-user-consent
  - fullstory-async-methods
  - fullstory-privacy-strategy
  - fullstory-banking
  - fullstory-healthcare
  - fullstory-saas
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Identify Users API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/TypeScript (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's User Identification API allows developers to associate session data with your own unique customer identifiers. By calling `setIdentity`, you link a user's Fullstory session to their identity in your system, enabling you to:

- Search for sessions by customer ID
- View all sessions for a specific user across devices
- Connect Fullstory data with your internal analytics and CRM systems
- Attribute behavior patterns to known users

---

## Core Concepts

### When Identification Happens

- **On Login**: Call `setIdentity` immediately after a successful authentication
- **On App/Page Load (Already Authenticated)**: Call `setIdentity` on every app launch/page load if the user is logged in
- **After Authentication Redirects**: Ensure identification persists across OAuth/SSO redirects

### User Identity vs Anonymous Sessions

- **Anonymous Session**: Default state before `setIdentity` is called. User is tracked but not linked to your system.
- **Identified Session**: After `setIdentity`, the session is permanently linked to the provided `uid`.

### How Identification Works (Session Linking)

1. **Before identification**: All sessions from the same device are linked together anonymously
2. **When `setIdentity` is called**: ALL previous anonymous sessions are **retroactively merged** into the identified user
3. **Cross-device linking**: If the same `uid` is used on different devices, all sessions across all devices are linked

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Session Merging on Identification                     │
├─────────────────────────────────────────────────────────────────────────┤
│  Day 1: Anonymous visit          → "Anonymous User"                     │
│  Day 3: Anonymous visit          → Same anonymous user                  │
│  Day 7: User logs in, setIdentity(uid: "user_456")                      │
│         ↓                                                               │
│  Result: ALL sessions (Day 1, 3, 7) now linked to "user_456"           │
└─────────────────────────────────────────────────────────────────────────┘
```

> **Important**: This means a user's entire journey from first visit through conversion can be tracked, even if they only identify on their 5th session.

### Re-identification Behavior

- **CRITICAL**: You cannot change a user's identity once assigned within a session
- If you call `setIdentity` with a different `uid`, Fullstory automatically splits into a new session
- This is by design to maintain data integrity and prevent identity pollution

---

## Key Principles

1. Use a **stable, unique identifier** (database ID, UUID) — never use PII like email as the uid
2. Call `setIdentity` **as early as possible** after authentication
3. Include **meaningful properties** for searchability (displayName, email)
4. Handle **logout properly** by calling anonymize

---

## setIdentity vs setProperties (User)

| Scenario | Use This API | Why |
|----------|--------------|-----|
| User logs in | `setIdentity` | Links session to user identity |
| Initial user properties at login | `setIdentity` with `properties` | Convenient to include with identification |
| Update user properties later | `setProperties` (type: 'user') | Don't re-identify just to update properties |
| Properties for anonymous user | `setProperties` (type: 'user') | Works without identification! |

> **Important**: The `properties` object in `setIdentity` is a convenience — you can include initial properties when identifying. However, for **updating** properties after identification or for **anonymous users**, use `setProperties` with `type: 'user'` instead. See the **fullstory-user-properties** skill for details.

---

## UID Requirements

| Requirement | Details |
|-------------|---------|
| Maximum length | 256 characters |
| Type | Non-empty string |
| Stability | Must be stable and unique per user |
| Privacy | Should NOT be PII (don't use email, phone, SSN) |

### Good UIDs

- Database primary key: `usr_a1b2c3d4e5`
- UUID: `550e8400-e29b-41d4-a716-446655440000`
- Hashed identifier: `sha256_abc123...`

### Bad UIDs

- Email: `john@example.com` ❌
- Phone: `+1-555-123-4567` ❌
- Name: `John Smith` ❌

---

## Special Property Fields

| Field | Type | Description |
|-------|------|-------------|
| `displayName` | string | Shown in session list and user card in Fullstory app |
| `email` | string | Enables search via HTTP API and email-based lookups |

These fields have special treatment in the Fullstory UI and should always be included when available.

---

## Supported Property Types

| Type | Description | Examples |
|------|-------------|----------|
| `str` | String value | "premium", "enterprise" |
| `strs` | Array of strings | ["admin", "beta-tester"] |
| `int` | Integer | 42, -5, 0 |
| `ints` | Array of integers | [1, 2, 3] |
| `real` | Float/decimal | 99.99, -3.14 |
| `reals` | Array of reals | [10.5, 20.0] |
| `bool` | Boolean | true, false |
| `bools` | Array of booleans | [true, false, true] |
| `date` | ISO8601 date | "2024-01-15T00:00:00Z" |
| `dates` | Array of dates | ["2024-01-01", "2024-02-01"] |

---

## Rate Limits

| Type | Limit |
|------|-------|
| Sustained | 30 calls per page/screen per minute |
| Burst | 10 calls per second |

Exceeding limits may result in dropped calls.

---

## Authentication State Machine

```
┌─────────────────┐
│  Anonymous      │ ← Initial state (no setIdentity called)
│  Session        │
└────────┬────────┘
         │ User logs in
         ▼
┌─────────────────┐
│  Identified     │ ← setIdentity({ uid: 'xxx' }) called
│  Session        │
└────────┬────────┘
         │ User logs out
         ▼
┌─────────────────┐
│  New Anonymous  │ ← setIdentity({ anonymous: true }) called
│  Session        │   (or platform equivalent)
└─────────────────┘
```

---

## Best Practices

### 1. Identification Timing

- ✅ Call `setIdentity` **immediately after** successful authentication
- ✅ Call on every app launch/page load if user is already authenticated
- ❌ Don't call before authentication completes
- ❌ Don't call on every user interaction

### 2. Property Design

- ✅ Always include `displayName` and `email`
- ✅ Add business-relevant properties (plan, role, company)
- ✅ Use explicit schema for non-string types
- ❌ Don't include sensitive data that shouldn't be in Fullstory

### 3. Account Switching

For apps where users can switch accounts:

1. Call anonymize/logout first
2. Then identify as the new user
3. Track which account is currently active

### 4. Progressive Identification

For guest checkout → account creation flows:

1. Keep user anonymous during guest checkout
2. Identify when they create an account
3. All prior anonymous activity links automatically

---

## Troubleshooting

### Sessions Not Linking to User

| Cause | Solution |
|-------|----------|
| uid is undefined/null/empty | Verify uid is a non-empty string before calling |
| SDK not loaded | Check console for SDK errors |
| Privacy/ad blocker | Test in incognito without extensions |
| Storage blocked | Check for storage permissions (mobile) |

### Unexpected Session Splits

| Cause | Solution |
|-------|----------|
| Calling with different uid | Track current identity state; anonymize before switching |
| Calling on every interaction | Only call when identifying/changing users |
| Identity not persisting | Ensure auth state persists across navigation |

### Properties Not Appearing

| Cause | Solution |
|-------|----------|
| Wrong value types | Use schema to specify types explicitly |
| Invalid property names | Use camelCase or snake_case |
| Hitting limits | Check property limits for your plan |

---

## Key Takeaways for Agent

When helping developers implement User Identification:

1. **Always emphasize**:
   - Use stable database IDs as uid, never PII
   - Call setIdentity AFTER successful authentication
   - Include displayName and email as properties
   - You cannot change identity without anonymizing first

2. **Common mistakes to watch for**:
   - Using email as uid
   - Identifying before auth completes
   - Calling setIdentity excessively
   - Trying to update identity instead of using setProperties
   - Missing displayName/email properties

3. **Questions to ask developers**:
   - What's your unique user identifier? (database ID, UUID)
   - When does authentication complete in your flow?
   - Do users switch between accounts in your app?
   - What user attributes are important for segmentation?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Identify Users (Web)**: https://developer.fullstory.com/browser/identification/identify-users/
- **Identify Users (iOS)**: https://developer.fullstory.com/mobile/ios/identification/identify-users/
- **Identify Users (Android)**: https://developer.fullstory.com/mobile/android/identification/identify-users/
- **Identify Users (Flutter)**: https://developer.fullstory.com/mobile/flutter/identification/identify-users/
- **Identify Users (React Native)**: https://developer.fullstory.com/mobile/react-native/identification/identify-users/
- **Anonymize Users**: https://developer.fullstory.com/browser/identification/anonymize-users/
- **Help Center - Identifying Users**: https://help.fullstory.com/hc/en-us/articles/360020623294-Identifying-users

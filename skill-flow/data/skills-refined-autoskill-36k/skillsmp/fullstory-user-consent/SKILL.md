---
name: fullstory-user-consent
version: v3
description: Core concepts for Fullstory's User Consent APIs. Platform-agnostic guide covering consent mechanisms, GDPR/CCPA compliance patterns, and privacy-compliant session recording. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-identify-users
  - fullstory-anonymize-users
  - fullstory-capture-control
  - fullstory-privacy-controls
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory User Consent API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript (Browser, Cookie Consent)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's User Consent APIs allow developers to implement privacy-compliant session recording by conditioning capture on explicit user consent. This is essential for:

- **GDPR Compliance**: Obtain consent before recording EU users
- **CCPA Compliance**: Allow California users to opt-out
- **App Store Compliance**: Respect iOS App Tracking Transparency (ATT)
- **Privacy Controls**: Give users control over their data
- **Selective Capture**: Record only users who have consented

---

## Core Concepts

### Two Consent Approaches

Fullstory provides two mechanisms for consent, each serving different use cases:

| Approach | Purpose | Platform Notes |
|----------|---------|----------------|
| **Holistic Consent** | Delay ALL capture until consent | Web: `_fs_capture_on_startup = false` + `FS('start')` |
| **Element-Level Consent** | Capture specific elements only with consent | Web only: Elements marked "Capture with consent" in Fullstory UI |

### Holistic Consent (Recommended)

For most compliance scenarios (GDPR, CCPA, ATT), use holistic consent:

1. **Delay capture on startup** — SDK loads but doesn't record
2. **Show consent UI** — Banner, dialog, or settings
3. **Start capture on consent** — Begin recording after user agrees
4. **Stop capture on revocation** — Respect user's withdrawal

### Consent State Machine

```
┌─────────────┐  User Accepts  ┌─────────────┐
│  Not        │ ─────────────► │  Capture    │
│  Capturing  │                │  Active     │
└─────────────┘                └─────────────┘
      ▲                              │
      │       User Withdraws        │
      └──────────────────────────────┘
```

### Consent Persistence

Consent state should be:
- **Persisted** — Saved to storage (localStorage, UserDefaults, SharedPreferences)
- **Restored** — Checked on app/page load
- **Synchronized** — Consistent across the application

---

## API Methods by Platform

| Platform | Delay Capture | Start Capture | Stop Capture |
|----------|---------------|---------------|--------------|
| Web | `_fs_capture_on_startup = false` | `FS('start')` | `FS('shutdown')` |
| iOS | `FSDelegate` / Config | `FS.restart()` | `FS.shutdown()` |
| Android | Config | `FS.restart()` | `FS.shutdown()` |
| Flutter | Config | `FS.restart()` | `FS.shutdown()` |
| React Native | Config | `FullStory.restart()` | `FullStory.shutdown()` |

---

## Platform-Specific Considerations

### Web (Browser)

- Cookie consent banners (GDPR)
- Consent Management Platforms (CMPs): OneTrust, CookieBot, etc.
- IAB TCF v2 compliance
- localStorage for consent persistence

### iOS

- App Tracking Transparency (ATT) framework
- `requestTrackingAuthorization` for iOS 14.5+
- UserDefaults for consent persistence
- Privacy nutrition labels in App Store

### Android

- No system-level tracking prompt (unlike iOS ATT)
- App-level consent dialogs
- SharedPreferences for consent persistence
- Google Play data safety section

### Flutter / React Native

- Cross-platform consent UI
- Platform-specific storage adapters
- Unified consent logic

---

## Compliance Guidance

### GDPR (EU)

| Requirement | Implementation |
|-------------|----------------|
| Consent before tracking | Delay capture until consent |
| Right to withdraw | Provide consent revocation in settings |
| Record consent | Store timestamp and method |
| Clear explanation | Explain what Fullstory does |

### CCPA (California)

| Requirement | Implementation |
|-------------|----------------|
| Opt-out right | Provide "Do Not Sell" option |
| Notice at collection | Explain data collection |
| Verifiable requests | Support data access/deletion |

### iOS App Tracking Transparency

| Requirement | Implementation |
|-------------|----------------|
| ATT prompt | Request authorization before tracking |
| Respect denial | Don't capture if user denies |
| Usage description | Explain tracking in Info.plist |

---

## Best Practices

### 1. Default to Not Capturing

For maximum compliance, don't capture until explicit consent:

```
Start: Capture disabled
User consents: Start capture
User logged in: Identify + capture
```

### 2. Persist Consent State

Store consent decision and restore on subsequent launches:

```
1. Check stored consent on app/page load
2. If granted: start capture immediately
3. If denied: remain disabled
4. If unknown: show consent UI
```

### 3. Provide Withdrawal Mechanism

Users must be able to revoke consent:
- Settings page toggle
- Privacy preferences
- "Manage cookies" link (web)

### 4. Handle Consent + Identity Together

Coordinate consent and identification:

```
1. Check consent status
2. If consented and user logged in: identify user
3. If consented and anonymous: capture anonymously
4. If not consented: don't capture or identify
```

### 5. Record Consent for Compliance

Keep records of consent grants:
- Timestamp
- Method (banner, settings, etc.)
- User agent / device info
- Version of consent language

---

## Troubleshooting

### Capture Not Starting After Consent

| Cause | Solution |
|-------|----------|
| SDK not loaded | Verify SDK initialization |
| Wrong API called | Use `start()`/`restart()`, not just consent flag |
| User on excluded page/screen | Check exclusion rules |

### Sessions Missing Consent Status

| Cause | Solution |
|-------|----------|
| Consent not recorded | Add user property `consentGranted: true` |
| No audit trail | Log consent grants to backend |

### Consent State Not Persisting

| Cause | Solution |
|-------|----------|
| Not saved to storage | Persist to localStorage/UserDefaults/SharedPreferences |
| Storage cleared | Handle storage unavailable gracefully |
| Cross-origin issues (web) | Use same-origin storage |

---

## Key Takeaways for Agent

When helping developers with Consent APIs:

1. **Always emphasize**:
   - Delay capture by default for GDPR compliance
   - Persist consent to storage
   - Provide withdrawal mechanism
   - Coordinate consent with identification

2. **Common mistakes to watch for**:
   - Capturing before consent
   - Not persisting consent
   - No withdrawal option
   - Ignoring CMP/ATT status
   - Race conditions with identity

3. **Questions to ask developers**:
   - What regulations apply (GDPR, CCPA, ATT)?
   - Do you have an existing CMP?
   - How do users currently consent?
   - Is there a privacy settings page?

4. **Platform routing**:
   - Web (JavaScript/TypeScript) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Web Consent**: https://developer.fullstory.com/browser/fullcapture/user-consent/
- **Web Capture Data**: https://developer.fullstory.com/browser/fullcapture/capture-data/
- **iOS Privacy**: https://developer.fullstory.com/mobile/ios/privacy/
- **Android Privacy**: https://developer.fullstory.com/mobile/android/privacy/
- **Help Center**: https://help.fullstory.com/hc/en-us/articles/360020623374

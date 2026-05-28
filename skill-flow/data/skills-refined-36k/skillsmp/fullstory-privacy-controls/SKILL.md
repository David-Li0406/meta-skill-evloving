---
name: fullstory-privacy-controls
version: v3
description: Core concepts for Fullstory's Privacy Controls API (fs-exclude, fs-mask, fs-unmask). Platform-agnostic guide covering privacy modes, data handling, inheritance rules, and compliance guidance. See SKILL-WEB.md and SKILL-MOBILE.md for implementation examples.
platforms:
  - web
  - ios
  - android
  - flutter
  - react-native
related_skills:
  - fullstory-privacy-strategy
  - fullstory-user-consent
  - fullstory-element-properties
  - fullstory-capture-control
  - fullstory-banking
  - fullstory-healthcare
  - fullstory-gaming
  - fullstory-ecommerce
implementation_files:
  - SKILL-WEB.md
  - SKILL-MOBILE.md
---

# Fullstory Privacy Controls API

> **Implementation Files**: This document covers core concepts. For code examples, see:
> - [SKILL-WEB.md](./SKILL-WEB.md) — JavaScript/CSS (Browser)
> - [SKILL-MOBILE.md](./SKILL-MOBILE.md) — iOS, Android, Flutter, React Native

## Overview

Fullstory's Privacy Controls allow developers to control what data is captured and sent to Fullstory servers. Privacy is implemented through element classification that defines how elements and their content are treated during session recording.

**Critical Understanding**: Privacy controls operate at the element level on the user's device:
- **Excluded content**: Never leaves the user's device at all — completely ignored
- **Masked content**: The **actual text never leaves the device**. It is replaced locally with a wireframe approximation before anything is sent to Fullstory's servers. Fullstory only receives the wireframed placeholder, never the original text.

---

## Core Concepts

### The Three Privacy Modes

| Mode | Data Leaves Device | Events Captured | Best For |
|------|-------------------|-----------------|----------|
| **Exclude** | ❌ Nothing | ❌ No | Regulated data, secrets, credentials |
| **Mask** | ⚠️ Structure only (text **never** sent — wireframed locally) | ✅ Yes | PII, names, emails, addresses |
| **Unmask** | ✅ Everything | ✅ Yes | Public content, navigation, buttons |

### Privacy Hierarchy (Most → Least Restrictive)

```
┌─────────────────────────────────────────────────────┐
│  EXCLUDE                                             │
│  - Element completely ignored                        │
│  - Events targeting element ignored                  │
│  - Gray crosshatch in replay                         │
│  - Nothing sent to Fullstory                         │
├─────────────────────────────────────────────────────┤
│  MASK                                                │
│  - Actual text NEVER leaves device                   │
│  - Replaced locally with wireframe approximation     │
│  - Only wireframe sent to Fullstory servers          │
│  - Element structure sent (knows what was clicked)   │
│  - Events captured                                   │
│  - Text appears as "████████" in replay              │
├─────────────────────────────────────────────────────┤
│  UNMASK                                              │
│  - Full text and content captured                    │
│  - Everything visible in replay                      │
│  - Default mode (unless Private by Default)          │
└─────────────────────────────────────────────────────┘
```

### Key Technical Facts

1. **Local Processing**: All privacy filtering happens on the device before data is sent
2. **Inheritance**: Children inherit parent's privacy classification
3. **Override**: Child can change privacy level within a parent (with exceptions)
4. **Strictest Wins**: When multiple rules match, the most restrictive applies

---

## What Gets Captured?

| Content Type | Exclude | Mask | Unmask |
|--------------|---------|------|--------|
| Element exists | ❌ | ✅ | ✅ |
| Element position | ❌ | ✅ | ✅ |
| Element size | ❌ | ✅ | ✅ |
| Element type (button, input) | ❌ | ✅ | ✅ |
| Text content | ❌ | ❌ (never sent — wireframe only) | ✅ |
| Input values | ❌ | ❌ (never sent — wireframe only) | ✅ |
| Images | ❌ | ✅ | ✅ |
| Click/tap events | ❌ | ✅ | ✅ |
| Form change events | ❌ | ✅ | ✅ |

---

## When to Use Each Mode

| Use Case | Recommended Mode | Reason |
|----------|------------------|--------|
| Passwords | **Exclude** | Never capture credentials |
| Credit card numbers | **Exclude** | PCI compliance |
| CVV/security codes | **Exclude** | PCI compliance |
| SSN / Tax IDs | **Exclude** | Regulatory — cannot be masked |
| Bank account/routing numbers | **Exclude** | Financial data protection |
| Medical conditions | **Exclude** | HIPAA — even structure reveals |
| API keys/secrets | **Exclude** | Security |
| User names | Mask | PII but structure useful |
| Email addresses | Mask | PII but interaction useful |
| Phone numbers | Mask | PII but structure useful |
| Street addresses | Mask | PII but form flow useful |
| Search terms | Unmask | Analytics value, typically not PII |
| Product names | Unmask | Business data, not PII |
| Navigation/buttons | Unmask | UX analysis |
| Error messages | Unmask | Debugging |

---

## Private by Default Mode

Fullstory offers a **Private by Default** mode that inverts the default capture behavior for maximum privacy protection.

### How Private by Default Works

| Mode | Default Behavior | When to Use |
|------|------------------|-------------|
| **Standard** | Everything captured (unmask) unless excluded/masked | Low-sensitivity applications (marketing sites) |
| **Private by Default** | Everything masked unless explicitly unmasked | Sensitive applications (banking, healthcare, SaaS) |

```
┌─────────────────────────────────────────────────────────────────────────┐
│  STANDARD MODE (Default)                                                 │
│  └── All content visible → Add exclude/mask to protect                  │
├─────────────────────────────────────────────────────────────────────────┤
│  PRIVATE BY DEFAULT MODE                                                 │
│  └── All content masked → Add unmask to reveal safe content             │
│                                                                         │
│  With Private by Default enabled:                                        │
│  • No text is captured unless explicitly unmasked                       │
│  • Session replay shows wireframes everywhere                           │
│  • Zero risk of accidentally capturing sensitive data                   │
│  • Selectively unmask navigation, buttons, product info                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### When to Use Private by Default

| Scenario | Recommendation |
|----------|---------------|
| **Healthcare applications** | ✅ Highly recommended |
| **Banking/financial services** | ✅ Highly recommended |
| **Applications with heavy PII** | ✅ Highly recommended |
| **Enterprise SaaS (multi-tenant)** | ⚠️ Recommended |
| **E-commerce (product pages)** | ⚠️ Consider — may need extensive unmasking |
| **Marketing/content sites** | ❌ Probably overkill |

### Enabling Private by Default

Private by Default is enabled via Fullstory Support or during account setup:

1. **New accounts**: Choose "Private by Default" during onboarding wizard
2. **Existing accounts**: Contact [Fullstory Support](https://help.fullstory.com/hc/en-us/requests/new) to enable

> **⚠️ Warning for existing accounts**: Enabling Private by Default may break existing segments, event funnels, or Conversions that rely on text elements. Coordinate with your analytics team before enabling.

---

## Default Exclusions

Fullstory automatically excludes certain content across platforms:

### Web (Browser)
- `input[type=password]` — All password fields
- `[autocomplete^=cc-]` — Credit card fields (number, CVV, expiry)
- `input[type=hidden]` — Hidden inputs

### Mobile
- Password input fields
- Secure text entry fields
- Credit card input fields (when properly typed)

> **Important**: Don't rely solely on auto-detection. Always explicitly mark sensitive fields.

---

## Critical Data That MUST Be Excluded

These data types should **always** be excluded, not masked:

| Data Type | Why Exclude (Not Mask) |
|-----------|------------------------|
| Passwords / credentials | Security — never capture authentication |
| Credit/debit card numbers | PCI-DSS compliance |
| CVV/security codes | PCI-DSS compliance |
| SSN / Tax IDs | Regulatory requirements |
| Bank account/routing numbers | Financial data protection |
| Medical diagnoses / conditions | HIPAA — even structure can reveal |
| API keys / secrets / tokens | Security |
| Biometric data | Privacy regulations |

---

## Compliance Guidance

### PCI-DSS (Payment Card Industry)
- **Exclude** all payment card data
- **Exclude** CVV/CVC/security codes
- **Exclude** cardholder name on payment forms
- Document privacy controls for audits

### HIPAA (Healthcare)
- **Exclude** all PHI (Protected Health Information)
- **Exclude** medical conditions, diagnoses
- **Exclude** treatment information
- Use Private by Default mode
- Consider excluding appointment details

### GDPR/CCPA (General Privacy)
- **Mask** all PII at minimum
- Obtain consent for session recording
- Provide opt-out mechanism
- Document data processing

### SOC 2
- Implement consistent privacy controls
- Document privacy implementation
- Regular privacy audits
- Access controls for Fullstory data

---

## Troubleshooting

### Content Still Visible After Excluding

**Symptom**: Added exclude but content still appears in replay

**Common Causes**:
1. Privacy class/attribute added after content rendered
2. Conflicting unmask rule
3. Platform-specific implementation issue
4. Rule not propagating to children

**Solutions**:
- Apply privacy controls before content renders
- Check for conflicting rules in Settings
- Verify no explicit unmask on children
- Test in actual Fullstory session

### Clicks Not Captured on Masked Elements

**Symptom**: Masking works but interactions not tracked

**Common Causes**:
1. Used exclude instead of mask
2. Parent element is excluded

**Solutions**:
- Use mask to keep interaction tracking
- Only use exclude when events shouldn't be tracked

### Dynamic Content Not Protected

**Symptom**: Dynamically loaded content visible in replay

**Common Causes**:
1. No privacy controls on dynamic content
2. Content rendered before privacy applied

**Solutions**:
- Include privacy controls in templates/components
- Use selector rules as backup
- Apply controls in component library

---

## Key Takeaways for Agent

When helping developers with Privacy Controls:

1. **Always emphasize**:
   - Exclude = nothing leaves device, no events
   - Mask = structure sent, **actual text never leaves device** (wireframed locally), events captured
   - Unmask = everything captured
   - When in doubt, use the more restrictive option

2. **Critical data that MUST be excluded**:
   - Passwords (any credential)
   - Credit/debit card numbers
   - CVV/security codes
   - SSN/Tax IDs
   - Bank account/routing numbers
   - Medical conditions (HIPAA)
   - Anything regulated (PCI, HIPAA, GLBA, FERPA)

3. **Questions to ask developers**:
   - What regulations apply (PCI, HIPAA, GDPR)?
   - What data types are in this field?
   - Do you need to track interactions on this element?
   - Is this dynamic content?
   - Are you logging sensitive data to console? (web)

4. **Platform routing**:
   - Web (JavaScript/CSS) → See SKILL-WEB.md
   - iOS (Swift/SwiftUI) → See SKILL-MOBILE.md § iOS
   - Android (Kotlin/Java) → See SKILL-MOBILE.md § Android
   - Flutter (Dart) → See SKILL-MOBILE.md § Flutter
   - React Native → See SKILL-MOBILE.md § React Native

---

## Reference Links

- **Privacy Protection (Web)**: https://help.fullstory.com/hc/en-us/articles/360020623574
- **Privacy Settings**: https://help.fullstory.com/hc/en-us/articles/360020622814
- **Private by Default**: https://help.fullstory.com/hc/en-us/articles/360044349073
- **iOS Privacy**: https://developer.fullstory.com/mobile/ios/privacy/
- **Android Privacy**: https://developer.fullstory.com/mobile/android/privacy/
- **Flutter Privacy**: https://developer.fullstory.com/mobile/flutter/privacy/
- **React Native Privacy**: https://developer.fullstory.com/mobile/react-native/privacy/

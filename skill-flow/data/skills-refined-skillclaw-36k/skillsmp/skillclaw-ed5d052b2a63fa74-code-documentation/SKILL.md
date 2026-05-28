---
name: code-documentation
description: Use this skill when writing or reviewing code that requires clear, plain-spoken comments and documentation, ensuring it is co-located with the code for accuracy and relevance.
---

# Skill body

Write documentation that lives with the code it describes. Use plain language and avoid jargon. Focus on explaining the *why* behind the code rather than just the *what*.

## Core Philosophy

**Co-location wins.** Documentation in separate files can drift out of sync. Comments next to code remain accurate because they are updated together.

**Write for three audiences:**
1. Future you, six months from now
2. Teammates reading unfamiliar code
3. AI assistants (like Claude or Copilot) who see one file at a time

**The "why" test:** Before writing a comment, ask: "Does this explain *why* this code exists or *why* it works this way?" If it only restates *what* the code does, skip it.

## Documentation Levels

### File Headers

Every file should begin with a brief explanation of its purpose and how it fits into the larger system.

```typescript
// UserAuthContext.tsx
//
// Manages authentication state across the app. Wraps the root component
// to provide login status, user info, and auth methods to any child.
//
// Why a context instead of Redux: Auth state is read-heavy and rarely
// changes mid-session. Context avoids the ceremony of actions/reducers
// for something this simple.
```

```swift
// NetworkRetryPolicy.swift
//
// Handles automatic retry logic for failed network requests.
// Uses exponential backoff with jitter to avoid thundering herd
// when the server comes back online after an outage.
//
// Used by: APIClient, BackgroundSyncManager
// See also: NetworkError.swift for error classification
```

**Include:**
- What this file/module is responsible for
- Why it exists (if not obvious from the name)
- Key relationships to other parts of the codebase
- Any non-obvious design decisions

### Function & Method Documentation

Document the contract, not the implementation.

```typescript
/**
 * Calculates shipping cost based on weight and destination.
 *
 * Uses tiered pricing: under 1lb ships flat rate, 1-5lb uses
 * regional rates, over 5lb triggers freight calculation.
 *
 * Returns $0 for destinations we don't ship to rather than
 * throwing—caller should check `canShipTo()` first if they
 * need to distinguish "free shipping" from "can't ship."
 */
```
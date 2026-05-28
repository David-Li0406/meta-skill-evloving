---
name: code-documentation
description: Use this skill when writing or reviewing code that requires clear, plain-spoken comments and documentation, including file headers, function documentation, architectural decisions, and explanatory comments.
---

# Code Documentation

Write documentation that lives with the code it describes. Use plain language and avoid jargon. Focus on explaining the *why*, not the *what*.

## Core Philosophy

**Co-location wins.** Documentation in separate files can drift out of sync. Comments next to code remain accurate because they are updated together.

**Write for three audiences:**
1. Future you, six months from now
2. Teammates reading unfamiliar code
3. AI assistants (Claude, Copilot) who see one file at a time

**The "why" test:** Before writing a comment, ask: "Does this explain *why* this code exists or *why* it works this way?" If it only restates *what* the code does, skip it.

## Documentation Levels

### File Headers

Every file should open with a brief explanation of its purpose and how it fits into the larger system.

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
 * throwing. Caller should check `canShipTo()` first if they
 * need to distinguish "free shipping" from "can't ship."
 */
function calculateShipping(weightLbs: number, zipCode: string): number
```

**Include:**
- What the function accomplishes (not how)
- Non-obvious parameter constraints or edge cases
- What the return value means, especially for ambiguous cases
- Side effects (network calls, file writes, state mutations)

**Skip for:** Simple getters, obvious one-liners, private helpers with descriptive names.

### Inline Comments

Use sparingly. When you need them, explain the reasoning.

```typescript
// Debounce search by 300ms to avoid hammering the API on every keystroke.
// 300ms feels responsive while cutting API calls by ~80% in user testing.
const debouncedSearch = useMemo(
  () => debounce(executeSearch, 300),
  [executeSearch]
);
```

### Architectural Comments

For code that embodies important design decisions, explain the tradeoffs.

```typescript
// ARCHITECTURE NOTE: Event Sourcing for Cart
//
// Cart state is rebuilt from events (add, remove, update quantity)
// rather than stored directly. This lets us:
// - Show complete cart history to users
// - Replay events for debugging
// - Retroactively apply promotions to past actions
//
// Tradeoff: Reading current cart state requires replaying all events.
// We cache the computed state in Redis with 5min TTL to keep reads fast.
// Cache invalidation happens in CartEventHandler.
```

### TODO Comments

Make them actionable and traceable.

```typescript
// TODO(pete): Extract to shared util once mobile team needs this too.
// Blocked on: Mobile API parity (see MOBILE-123)

// HACK: Workaround for Safari flexbox bug. Remove after dropping Safari 14.
// Bug report: https://bugs.webkit.org/show_bug.cgi?id=XXXXX

// FIXME: Race condition when user rapidly toggles. Need to cancel
// in-flight requests. Reproduced in issue #892.
```

## Language-Specific Patterns

Refer to language-specific documentation patterns for detailed examples in:
- TypeScript/JavaScript (JSDoc, TSDoc patterns)
- Swift (documentation comments, MARK pragmas)
- Python (docstrings, type hint documentation)

## Writing Style

**Plain language.** Write as if explaining to a smart colleague who doesn't have context.

**Active voice.** "This function validates..." not "Validation is performed..."

**Be specific.** "Retries 3 times with 1s backoff" not "Handles retries."

**Skip the obvious.** If the code says `user.isAdmin`, don't comment "checks if user is admin."

**Date things that expire.** Workarounds, version-specific code, and temporary solutions should note when they can be removed.

**Reference constants, don't duplicate values.** When a behavior is controlled by a constant, reference it by name—don't restate its value in the comment.

```rust
// Bad: duplicates the value, will drift when constant changes
/// Returns true if stale (not updated in last 5 minutes)
pub fn is_stale(&self) -> bool { ... }

// Good: references the constant
/// Returns true if stale (not updated within [`STALE_THRESHOLD_SECS`])
pub fn is_stale(&self) -> bool { ... }
```

Unit translations for magic numbers are fine (`1048576 // 1MB`) since they add clarity, not duplication.
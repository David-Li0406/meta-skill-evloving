# State Choreography

Design state transitions that feel natural, informative, and delightful.

## Transition Matrix

### Standard Transitions

| From | To | Animation | Duration | Easing |
|------|-----|-----------|----------|--------|
| Empty | Loading | Fade in skeleton | 150ms | ease-out |
| Loading | Success | Crossfade | 300ms | ease-out |
| Loading | Error | Slide + subtle shake | 200ms | ease-out |
| Success | Updating | Pulse overlay | Ongoing | linear |
| Success | Error | Flash border red | 200ms | ease-out |
| Error | Loading | Fade to skeleton | 150ms | ease-out |
| Any | Empty | Fade + collapse | 200ms | ease-in |

### Complex Transitions

#### List Item Addition
```
1. Item fades in at top (150ms)
2. Existing items slide down (200ms)
3. New item highlights briefly (300ms)
4. Highlight fades (200ms)
Total: ~850ms
```

#### List Item Removal
```
1. Item fades and slides left (200ms)
2. Gap collapses (200ms)
3. List re-settles (100ms)
Total: ~500ms
```

#### Modal Open/Close
```
Open:
1. Overlay fades in (150ms)
2. Modal scales from 0.95 to 1 + fade (200ms)
Total: ~350ms

Close:
1. Modal scales to 0.95 + fade (150ms)
2. Overlay fades out (100ms)
Total: ~250ms
```

## Success Feedback Patterns

### The Hold Rule
**Users must SEE success before the UI changes.**

```
Action → Success indicator → Hold 300-500ms → Proceed
```

### Pattern: Inline Success
```
Button: [Add to Cart]
         ↓ tap
Button: [✓] (checkmark, green)
         ↓ 400ms
Button: [Add to Cart] (reset)
Cart: count increments
```

### Pattern: Toast Confirmation
```
Action completed
         ↓ immediately
Toast slides in from bottom/top
         ↓ 3-5 seconds OR user dismisses
Toast slides out
```

### Pattern: Full-Screen Confirmation
```
Form submitted
         ↓ 100-500ms processing
Full-screen success
         ↓ Auto-redirect 3s OR user clicks
Next screen
```

### Success Indicator Types

| Context | Indicator | Duration | Use When |
|---------|-----------|----------|----------|
| Button action | Inline checkmark | 400ms | Add/save/submit |
| Background save | Subtle "Saved" text | 2s | Auto-save |
| Form submission | Success toast | 3s | Non-critical forms |
| Critical action | Success screen | Until user proceeds | Orders, payments |
| Batch operation | Progress → complete | Varies | Multiple items |

## Empty State Design

### Empty State Formula

```
1. Visual: Illustration or icon (sets tone)
2. Headline: Acknowledge the emptiness
3. Explanation: Why it's empty (if non-obvious)
4. CTA: Actionable next step
```

### Empty State Matrix

| Context | Tone | Headline | CTA |
|---------|------|----------|-----|
| New user, empty cart | Welcoming | "Your cart is waiting" | "Browse menu" |
| Search no results | Helpful | "No matches found" | "Clear filters" |
| Network error | Apologetic | "Couldn't load" | "Try again" |
| Feature unavailable | Informative | "Coming soon" | "Get notified" |
| Completed tasks | Celebratory | "All done!" | "See history" |

### Empty State Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Just text "Empty" | Unhelpful | Add context and CTA |
| No visual | Looks broken | Add illustration |
| No CTA | Dead end | Always provide next step |
| Generic message | Impersonal | Context-specific copy |
| Same for all empties | Missed opportunity | Tailor to context |

## Loading State Design

### Loading State Decision Tree

```
Is the load time < 100ms?
  YES → No loading indicator needed
  NO → Continue...

Is the load time < 1 second?
  YES → Subtle indicator (spinner, pulse)
  NO → Continue...

Is content structure known?
  YES → Skeleton screens
  NO → Spinner with message

Is the load time > 5 seconds?
  YES → Progress bar + estimated time
  NO → Skeleton/spinner sufficient
```

### Skeleton Screen Guidelines

**Do:**
- Match actual content layout
- Use subtle animation (pulse, shimmer)
- Show immediately (no delay before skeleton)
- Cover all content areas

**Don't:**
- Make skeletons too detailed
- Animate aggressively
- Show spinner AND skeleton
- Use for sub-second loads

### Loading with Context

| Context | Loading Treatment | Why |
|---------|-------------------|-----|
| Initial page load | Full skeleton | User expects content |
| Pagination | Inline skeleton at bottom | User knows to wait |
| Background refresh | Subtle header indicator | Don't interrupt |
| Action processing | Button spinner | Show processing |
| Long operation | Progress bar | Set expectations |

## Error State Design

### Error Severity Levels

| Level | Display | User Action | Example |
|-------|---------|-------------|---------|
| Info | Inline text | Continue | "Prices may have changed" |
| Warning | Yellow banner | Acknowledge | "Item low in stock" |
| Error | Red inline | Fix issue | "Invalid email format" |
| Blocking | Modal/full-screen | Must resolve | "Payment failed" |
| Fatal | Full-screen | Contact support | "Server error" |

### Error Message Formula

```
1. What happened (clear, non-technical)
2. Why it happened (if helpful)
3. How to fix it (specific action)
```

**Examples:**

| Bad | Good |
|-----|------|
| "Error 500" | "Something went wrong. Please try again." |
| "Invalid input" | "Email must include @ symbol" |
| "Request failed" | "Couldn't connect. Check your internet and try again." |
| "Unauthorized" | "Please log in to continue" |

### Error Recovery Patterns

| Error Type | Recovery Option | Implementation |
|------------|-----------------|----------------|
| Network | Retry button | Re-attempt same request |
| Validation | Inline fix | Focus invalid field |
| Auth expired | Re-authenticate | Preserve form data, redirect to login |
| Not found | Navigate away | Back button or home link |
| Rate limited | Wait indicator | Show countdown, auto-retry |

## Partial State Design

### Partial State Types

| Type | Description | Treatment |
|------|-------------|-----------|
| Partial load | Some data loaded | Show available, skeleton for rest |
| Partial success | Some items failed | Show succeeded, list failures |
| Partial permissions | Limited access | Show available, indicate restricted |
| Partial data | Missing optional fields | Show available, placeholder for missing |

### Mixed Results Pattern

```
Operation on 5 items:
- 3 succeeded ✓
- 2 failed ✗

Display:
┌────────────────────────────────┐
│ 3 items updated successfully   │
│                                │
│ 2 items couldn't be updated:   │
│ • Item A: [reason]             │
│ • Item B: [reason]             │
│                                │
│ [Retry Failed] [Done]          │
└────────────────────────────────┘
```

## Offline State Design

### Offline Indicators

| Page State | Indicator | Location |
|------------|-----------|----------|
| App shell | Banner "You're offline" | Top of viewport |
| Feature unavailable | Inline message | Where feature would appear |
| Cached content | "Last updated X" | Near content |
| Action unavailable | Disabled + tooltip | On the action |

### Offline Behavior Matrix

| Action Type | Offline Behavior | Message |
|-------------|------------------|---------|
| Read cached data | Allow | None needed |
| Create new item | Queue for sync | "Will save when online" |
| Edit existing | Queue for sync | "Changes saved locally" |
| Delete | Queue for sync | "Will delete when online" |
| Sync required | Block with message | "Requires connection" |

## Animation Timing Reference

### Duration Guidelines

| Animation Type | Duration | Notes |
|----------------|----------|-------|
| Micro-interaction | 100-200ms | Button press, toggle |
| Transition | 200-300ms | Screen changes |
| Emphasis | 300-500ms | Success states, attention |
| Complex | 500-800ms | Multi-step animations |

### Easing Reference

| Easing | Use Case |
|--------|----------|
| ease-out | Entering elements |
| ease-in | Exiting elements |
| ease-in-out | Transitioning elements |
| spring | Interactive feedback |
| linear | Continuous animations (loading) |

### Stagger Timing

For lists and grids:
```
Base delay + (index × 50ms)
Max total: 400ms

Example (5 items):
- Item 0: 0ms
- Item 1: 50ms
- Item 2: 100ms
- Item 3: 150ms
- Item 4: 200ms
```

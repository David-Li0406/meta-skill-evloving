# Failure Modes & Recovery

Map error scenarios and design recovery paths before they happen.

## Error Classification

### By Severity

| Severity | Impact | User Expectation | Recovery Priority |
|----------|--------|------------------|-------------------|
| Minor | Inconvenience | Retry available | Low |
| Moderate | Blocked feature | Alternative path | Medium |
| Severe | Blocked flow | Immediate fix | High |
| Critical | Data loss/security | Emergency | Immediate |

### By Cause

| Cause | Detection | User Message Tone |
|-------|-----------|-------------------|
| User error | Validation | Helpful, guide to fix |
| Network | Timeout/offline | Apologetic, retry option |
| Server | 5xx response | Apologetic, we're on it |
| External | Third-party fail | Informative, alternative |
| Rate limit | 429 response | Informative, wait time |

### By Timing

| Timing | Examples | Pattern |
|--------|----------|---------|
| Before action | Validation errors | Prevent submission |
| During action | Network fails | Show processing error |
| After action | Background sync fails | Notify + retry |
| Delayed | Webhook fails | Email notification |

## Error Prevention

### Validation Strategy

| Level | When | What |
|-------|------|------|
| Format | On blur | Email format, phone format |
| Business | On change | Quantity limits, date ranges |
| Server | On submit | Unique email, stock check |
| Async | Background | External API validation |

### Inline Validation Pattern

```
Field empty:
  [                           ] ← No message

Field valid:
  [user@example.com           ] ← Optional ✓

Field invalid (on blur):
  [userexample.com            ]
  ⚠ Please enter a valid email address
```

### Preventing Destructive Actions

| Action Type | Prevention Pattern |
|-------------|---------------------|
| Delete single | Confirm dialog with item name |
| Delete bulk | Confirm with count + "type to confirm" |
| Account delete | Multi-step + cooling period |
| Submit irreversible | Preview + explicit confirm |
| Overwrite data | Show diff, require acknowledgment |

## Error Recovery Patterns

### Network Failure Recovery

```
Initial state:
  [Content displayed normally]

Network fails:
  ┌─────────────────────────────────┐
  │ ⚠ Couldn't connect              │
  │                                 │
  │ Check your internet connection  │
  │ and try again.                  │
  │                                 │
  │        [Retry]                  │
  └─────────────────────────────────┘

Auto-retry available:
  [Retrying... (2/3)]

After recovery:
  [Content restored with subtle refresh indicator]
```

### Form Error Recovery

```
Form with errors:
  Email*
  [userexample.com              ]
  ⚠ Please enter a valid email

  Password*
  [••••]
  ⚠ Password must be at least 8 characters

  [Submit] ← Focus first error field on click
```

### Session Expiration Recovery

```
Scenario: User's session expires during form fill

Pattern:
1. Detect 401 response
2. Cache current form state
3. Redirect to login
4. After login, restore form state
5. Show "Welcome back, your work was saved"
```

### Payment Failure Recovery

```
Card declined:
  ┌─────────────────────────────────┐
  │ ⚠ Payment failed                │
  │                                 │
  │ Your card was declined.         │
  │                                 │
  │ ○ Try a different card          │
  │ ○ Update card details           │
  │ ○ Try again later               │
  │                                 │
  │ [Choose Option]                 │
  └─────────────────────────────────┘
```

## Degradation Patterns

### Graceful Degradation Matrix

| Feature | Full Function | Degraded | Offline |
|---------|---------------|----------|---------|
| Browse content | Live data | Cached data | Cached only |
| Search | Full search | Basic filter | Client-side filter |
| Cart | Real-time sync | Local + sync later | Local only |
| Checkout | Full flow | Queue for later | Blocked |
| Account | All features | Read-only | Cached profile |

### Feature Fallbacks

| Feature | Primary | Fallback | Message |
|---------|---------|----------|---------|
| Image load | CDN image | Placeholder | None |
| Map | Interactive | Static | "Interactive map unavailable" |
| Real-time | WebSocket | Polling | None (seamless) |
| Payment | Card | Alternative | "Card unavailable, try PayPal" |
| Search | Server | Client | "Showing cached results" |

## Error Messaging Guidelines

### Message Structure

```
What happened (plain language)
+
Why it happened (if helpful)
+
How to fix it (specific action)
```

### Message Tone by Context

| Context | Tone | Example |
|---------|------|---------|
| User error | Helpful | "Email needs an @ symbol" |
| Our fault | Apologetic | "Sorry, something went wrong" |
| External | Informative | "Payment provider is temporarily unavailable" |
| Preventive | Cautionary | "This will delete all your data" |

### Messages to Avoid

| Bad | Why | Better |
|-----|-----|--------|
| "Error" | No information | "Couldn't save changes" |
| "Invalid input" | No guidance | "Please enter a valid email" |
| "Request failed" | Technical | "Couldn't connect. Check your internet." |
| "Unauthorized" | Jargon | "Please log in to continue" |
| "500 Internal Server Error" | Scary | "Something went wrong. We're on it." |

## Error Boundaries

### Component-Level Boundaries

```
Page structure:
┌────────────────────────────────┐
│ Header (always renders)        │
├────────────────────────────────┤
│ ┌──────────┐ ┌──────────────┐  │
│ │ Widget A │ │ Widget B     │  │
│ │ (can     │ │ (can fail    │  │
│ │  fail    │ │  independently)│ │
│ │  alone)  │ │              │  │
│ └──────────┘ └──────────────┘  │
├────────────────────────────────┤
│ Footer (always renders)        │
└────────────────────────────────┘
```

### Error Boundary Fallbacks

| Scope | Fallback | Recovery |
|-------|----------|----------|
| Widget | "Couldn't load" + retry | Retry button |
| Section | Collapsed section | Expand to retry |
| Page | Error page | Back or home link |
| App | Crash screen | Refresh app |

## Retry Strategies

### Retry Decision Tree

```
Is this a network error?
  YES → Auto-retry with backoff
  NO → Continue...

Is this a 5xx server error?
  YES → Auto-retry (limited)
  NO → Continue...

Is this a validation error?
  YES → Don't retry, show user
  NO → Continue...

Is this a 4xx client error?
  YES → Don't auto-retry, user action needed
```

### Backoff Strategy

```
Retry 1: Immediate
Retry 2: 1 second
Retry 3: 2 seconds
Retry 4: 4 seconds (optional)
After all fail: Show error with manual retry
```

### Retry UI Patterns

| Pattern | When | Display |
|---------|------|---------|
| Silent | Background sync | No indicator |
| Inline | Widget load | "Retrying..." text |
| Progress | Known attempts | "Retrying (2/3)" |
| Manual | After auto-retry fails | "Retry" button |

## Monitoring & Learning

### Error Tracking Priorities

| Track | Why | Alert When |
|-------|-----|------------|
| Error rate | Detect spikes | >1% of sessions |
| Error type distribution | Find patterns | New type appears |
| Recovery rate | Measure UX | Recovery <80% |
| Retry success | Validate retry logic | Success <50% |
| Time to recovery | UX quality | >30 seconds avg |

### Error Pattern Analysis

Questions to ask regularly:
1. What errors occur most frequently?
2. Which errors have lowest recovery rates?
3. Where do users abandon after errors?
4. Are retry strategies effective?
5. Which error messages get confusion feedback?

### Continuous Improvement

| Signal | Action |
|--------|--------|
| High error rate | Fix root cause |
| Low recovery rate | Improve recovery UX |
| High retry fail rate | Adjust retry strategy |
| Support tickets about errors | Improve error messages |
| Abandonment after error | Add recovery paths |

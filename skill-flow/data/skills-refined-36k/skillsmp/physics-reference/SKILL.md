---
name: physics-reference
description: Design physics tables and timing rationale
user-invocable: false
---

# Physics Reference

Detailed physics tables for the crafting skill. Loaded on-demand.

## The Complete Physics Table

| Effect | Sync | Timing | Confirmation | Easing | Spring |
|--------|------|--------|--------------|--------|--------|
| Financial | Pessimistic | 800ms | Required | ease-out | 200/30 |
| Destructive | Pessimistic | 600ms | Required | ease-out | 200/30 |
| Soft Delete | Optimistic | 200ms | Toast+Undo | spring | 500/30 |
| Standard | Optimistic | 200ms | None | spring | 500/30 |
| Navigation | Immediate | 150ms | None | ease | — |
| Local State | Immediate | 100ms | None | spring | 700/35 |

## Timing Rationale

### 800ms (Financial)

Time needed for users to:
1. Read and verify the amount
2. Mentally commit to the action
3. Feel the weight of irreversibility

Faster = anxiety. Slower = sluggish. 800ms is calibrated.

### 600ms (Destructive)

Permanent deletion needs deliberation but less than money.
Warning color + timing = sufficient gravity.

### 200ms (Standard)

Research shows 200ms is perceived as "instant" while allowing visual feedback.
- <100ms: Users miss the confirmation
- >300ms: Feels laggy

### 100ms (Local)

No network latency to hide. Users expect immediate response.
Any delay feels broken.

## Sync Strategy Details

### Pessimistic

```
User clicks → Loading state → Server confirms → UI updates
```

- Never show success before server confirms
- Cancel button always visible during loading
- Error state has clear recovery path

### Optimistic

```
User clicks → UI updates immediately → Server confirms (or rollback)
```

- Requires `onMutate` for immediate update
- Requires `onError` for rollback
- User sees instant feedback

### Immediate

```
User clicks → UI updates → No server call
```

- Pure client state (theme, toggles)
- useState or context only
- Zero loading states

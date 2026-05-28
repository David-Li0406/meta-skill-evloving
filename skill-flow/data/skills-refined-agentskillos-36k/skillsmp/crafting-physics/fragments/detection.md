## Effect Detection

Detect effect from keywords, types, and context. Priority order:

### Priority 1: Types
Props with these types → Always Financial:
- `Currency`, `Money`, `Balance`
- `Wei`, `Token`, `BigInt`

### Priority 2: Keywords

**Financial** (Pessimistic, 800ms):
```
claim, deposit, withdraw, transfer, swap, send, pay, purchase,
mint, burn, stake, unstake, bridge, approve, redeem
```

**Destructive** (Pessimistic, 600ms):
```
delete, remove, destroy, revoke, terminate, purge, wipe, ban
```

**Soft Delete** (Optimistic, 200ms, Toast+Undo):
```
archive, hide, trash, dismiss, snooze, mute
```

**Standard** (Optimistic, 200ms):
```
save, update, edit, create, add, like, follow, bookmark, comment
```

**Local State** (Immediate, 100ms):
```
toggle, switch, expand, collapse, select, focus, show, hide
```

**Navigation** (Immediate, 150ms):
```
navigate, go, back, forward, link, route, next, previous
```

### Priority 3: Context Modifiers

| Context | Effect Modification |
|---------|---------------------|
| "with undo" | Soft Delete (not Destructive) |
| "for wallet" | Financial |
| "checkout", "payment" | Financial |
| "theme", "preference" | Local State |

### Ambiguity Resolution

| Question | If Yes | If No |
|----------|--------|-------|
| Can it be undone? | Optimistic | Pessimistic |
| Involves money/tokens? | Financial | Check keywords |
| Hits a server? | Optimistic/Pessimistic | Immediate |
| Has undo button/toast? | Soft Delete | Hard Destructive |

If still unclear after analysis, ask (max 2 rounds):
- What happens when clicked?
- Does it call a server?
- Can it be undone?
- Does it involve money/tokens?

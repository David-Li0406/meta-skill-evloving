---
name: verify
description: Self-verification loop. Build/lint verification. Required before commit/PR. On failure, self-fix and re-verify.
---

# Verify Skill

Build/lint verification with Self-Healing Loop. Required before commit.

## Workflow

```
/verify
    │
    ├─ Step 1: Build Verification
    │   └─ pnpm build
    │       ├─ Success → Step 2
    │       └─ Failure → Analyze error → Fix code → Retry Step 1
    │
    └─ Step 2: Lint Verification
        └─ pnpm lint
            ├─ Success → Verification complete ✓
            └─ Error → pnpm lint --fix → Re-verify
```

## When to Call

| Timing | Required |
|--------|----------|
| After `/implement` completes | **Required** (auto-called) |
| Before commit | **Required** |
| Before PR creation | **Required** |

## Self-Healing Loop

```
Code change → /verify → Failure?
                          │
                          ├─ YES → Analyze error → Fix → Re-verify (loop)
                          │
                          └─ NO → Verification complete ✓
```

**Key Rules**:
1. On verification failure, self-fix without user intervention
2. Always re-verify after fix
3. Alert user after **3+ failures** on same error

## Commands

```bash
pnpm build      # Build verification
pnpm lint       # Lint verification
pnpm lint --fix # Lint auto-fix
```

## Error Handling

### Build Errors

1. Analyze error message
2. Identify source file
3. Fix code
4. Re-run `pnpm build`

### Lint Errors

1. Try `pnpm lint --fix` first
2. If auto-fix fails, fix manually
3. Re-run `pnpm lint`

## Integration with /implement

`/verify` is auto-called in `/implement` skill Phase 3:

```
/implement
    ├─ Phase 1: Analysis
    ├─ Phase 2: Implementation
    ├─ Phase 3: Verification ← /verify auto-called
    └─ Phase 4: Finalize
```

## After Verification

On verification pass:
```
✓ Build successful
✓ Lint passed

Ready to commit.
```

→ Proceed to `/implement` Phase 4 (Finalize)
→ Or manual commit

## Rules

1. **Required before commit**: No commit without verify
2. **Self-Healing**: Self-fix on failure
3. **3 failure alert**: Request user intervention on repeated same error
4. **Order**: build → lint order

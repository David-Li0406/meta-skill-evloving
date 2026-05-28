## Protected Capabilities Checklist

These capabilities are non-negotiable:

| Capability | Rule | Verify |
|------------|------|--------|
| **Withdraw** | Always reachable | Never hide behind loading states |
| **Cancel** | Always visible | Every flow needs escape hatch |
| **Balance** | Always accurate | Invalidate queries on mutation |
| **Error Recovery** | Always available | No dead ends |
| **Touch Target** | ≥44px | Apple HIG, accessibility |
| **Focus Ring** | Always visible | Keyboard navigation |

**Before Generation:**
- [ ] Cancel button present and always clickable (even during loading)
- [ ] Amount displayed clearly before confirmation
- [ ] Balance shown and current (invalidate queries on success)
- [ ] Error state has retry option
- [ ] Touch target ≥44px
- [ ] Focus ring visible on keyboard navigation

**Forbidden Patterns:**
- `{!isPending && <CancelButton />}` — User trapped during loading
- `{balance}` without invalidation — Stale financial data
- `{isError && <p>Error</p>}` — No recovery path
- `onMutate` for financial ops — Can't roll back money

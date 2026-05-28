# Effects to Watch Out For

Avoiding pitfalls and dark patterns.

---

## Reactance

**Definition**: Psychological resistance when feeling constrained.

**Implementation Guidelines**:
- Avoid premature monetization
- Respect user choice
- Don't be pushy

```jsx
// Bad: Immediate paywall
<App onMount={() => showPaywall()} />

// Good: Provide value first
<App>
  <FreeContent />
  <ValueDemonstration />
  <GentleUpgradeSuggestion />
</App>
```

---

## Decision Fatigue

**Definition**: Repeated decisions make rational choices difficult.

**Implementation Guidelines**:
- Minimize options
- Provide default recommendations
- Make choices incrementally

---

## Intentional Friction

**Definition**: Deliberately slowing user actions.

**Implementation Guidelines**:
- Add confirmation for important actions
- Double-confirm deletions
- Avoid malicious use

```jsx
// Good intentional friction
<DeleteConfirmation>
  <Warning>This action cannot be undone</Warning>
  <Input
    placeholder='Type "DELETE" to confirm'
    required
  />
  <Button disabled={!confirmed}>Permanently Delete</Button>
</DeleteConfirmation>
```

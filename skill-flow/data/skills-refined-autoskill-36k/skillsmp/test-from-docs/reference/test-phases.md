# Test Phases Detail

## Phase 1: Static Analysis

```bash
# TypeScript compilation
npx tsc --noEmit

# Linting
npm run lint

# Type checking specific files
npx tsc --noEmit app/actions/[changed-file].ts
```

## Phase 2: Feature Checklist

Run each item from the feature doc's Testing Checklist:

```markdown
### [Feature] Local Verification

- [ ] **Step**: [description]
  - **Command/Action**: [what to do]
  - **Expected**: [what should happen]
  - **Result**: ✅ Pass / ❌ Fail / ⚠️ Partial
  - **Notes**: [observations]
```

## Phase 3: Integration Tests

If change spans features, verify integration points:

```markdown
### Integration: [Feature A] → [Feature B]

- [ ] **Scenario**: [what crosses features]
  - **Action**: [trigger]
  - **Expected in A**: [outcome]
  - **Expected in B**: [outcome]
  - **Result**: ✅ / ❌ / ⚠️
```

## Phase 4: Browser Verification

Use Playwright MCP for UI testing:

```markdown
### Browser Tests

#### Visual Verification
- [ ] Navigate to [route]
- [ ] Verify [element] displays correctly
- [ ] Check console for errors
- [ ] Screenshot captured: [yes/no]

#### Interaction Test
- [ ] Click [button/link]
- [ ] Fill [form] with [data]
- [ ] Submit and verify [outcome]
- [ ] Check network tab for [expected request]

#### Responsive Check (if UI change)
- [ ] Desktop view: [status]
- [ ] Mobile view: [status]
```

## Phase 5: Workflow Smoke Test

Run ONE complete workflow that exercises the change:

```markdown
### Workflow Smoke: [Workflow Name]

**User Role**: [role being tested]
**Starting State**: [initial conditions]

| Step | Action | Expected | Actual | Status |
|------|--------|----------|--------|--------|
| 1 | [do X] | [see Y] | [actual] | ✅/❌ |
| 2 | [do X] | [see Y] | [actual] | ✅/❌ |
| 3 | [do X] | [see Y] | [actual] | ✅/❌ |

**End State Verified**: [yes/no]
**Workflow Passed**: [yes/no]
```

## Phase 6: Regression Checks

Verify related features still work:

```markdown
### Regression: [Coupled Feature]

- [ ] Basic functionality intact
- [ ] No console errors
- [ ] Data displays correctly
- [ ] Actions complete successfully
```

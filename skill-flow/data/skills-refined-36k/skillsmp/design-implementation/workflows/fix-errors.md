# Fix Errors Workflow

Systematic error fixing with categorization and iteration tracking.

## Triggers

- "fix the errors"
- "fix the console errors"
- "the build is broken"
- Automatically invoked by `implement-feature` when verification fails

## Error Categories & Fix Strategies

### P0: Console Errors (Fix Immediately)

```
Error Types:
- Undefined variable → Add import or define
- Cannot read property → Add null check or fix data flow
- Module not found → Install package or fix import path
- Syntax error → Fix syntax
```

**Strategy:**
1. Parse error message for file:line
2. Read the file
3. Apply fix via Edit tool
4. Verify fix

### P0: TypeScript Errors (Fix Immediately)

```bash
# Get errors
bun tsc --noEmit 2>&1
```

```
Error Types:
- Type mismatch → Fix type or add assertion
- Missing property → Add to interface or make optional
- Cannot find module → Add types or fix import
- Argument type → Fix function call
```

**Strategy:**
1. Parse TS error for file:line:column
2. Read surrounding context
3. Apply type fix
4. Re-run tsc

### P1: Network Errors

```
Error Types:
- 404 Not Found → Fix asset path or create asset
- 500 Server Error → Check API implementation
- CORS Error → Fix server config or use proxy
- Failed to fetch → Check URL or network
```

**Strategy:**
1. Identify failing request URL
2. Determine if asset or API
3. Fix path or create missing resource
4. Verify with retry

### P1: Visual Layout Issues

```
Issue Types:
- Wrong positioning → Fix flex/grid/position CSS
- Missing element → Add component to JSX
- Wrong size → Fix width/height/padding
- Overflow/clipping → Fix overflow or container size
```

**Strategy:**
1. Identify element from screenshot analysis
2. Locate component in code
3. Apply CSS fix
4. Re-screenshot and verify

### P2: Visual Style Issues

```
Issue Types:
- Wrong color → Update Tailwind class or CSS variable
- Wrong font → Fix font-family or font-size
- Wrong spacing → Adjust margin/padding classes
- Missing shadow/border → Add utility class
```

**Strategy:**
1. Compare spec to current
2. Identify specific property
3. Update class or style
4. Verify visually

## Iteration Protocol

```
MAX_ITERATIONS = 5 (from config)

FOR iteration IN 1..MAX_ITERATIONS:
  1. Read current errors from state.json
  2. Sort by priority (P0 first)
  3. Fix highest priority error
  4. Wait for HMR
  5. Re-verify
  6. Update state.json

  IF all errors fixed:
    BREAK → Success

  IF same error persists 2+ times:
    Mark as "stuck"
    Try alternative approach OR escalate

IF iteration >= MAX_ITERATIONS:
  Generate escalation report
  Ask Jean-Marc for guidance
```

## Fix Templates

### Import Error
```typescript
// Error: Cannot find module './Component'
// Fix: Check file exists, fix path
import Component from './components/Component'; // Fixed path
```

### Type Error
```typescript
// Error: Property 'foo' does not exist on type 'Bar'
// Fix: Add to interface or use optional chaining
interface Bar {
  foo?: string; // Added optional property
}
// OR
const value = bar?.foo; // Use optional chaining
```

### Null Reference
```typescript
// Error: Cannot read property 'x' of undefined
// Fix: Add null check
const value = data?.x ?? defaultValue;
```

### Missing Asset
```bash
# Error: GET /images/logo.png 404
# Fix: Check if asset exists, fix path
# Option 1: Fix import path
# Option 2: Add placeholder asset
```

### CSS Layout
```tsx
// Issue: Element not centered
// Fix: Add flex centering
<div className="flex items-center justify-center">
  {/* content */}
</div>
```

## Convergence Detection

Track if errors are being fixed:

```json
{
  "errorHistory": [
    { "iteration": 1, "count": 5, "types": ["console", "ts", "visual"] },
    { "iteration": 2, "count": 3, "types": ["ts", "visual"] },
    { "iteration": 3, "count": 3, "types": ["ts", "visual"] }  // Stuck!
  ]
}
```

**Stuck Detection:**
- Same error count for 2+ iterations
- Same error type recurring
- New errors introduced by fix

**Stuck Resolution:**
1. Try alternative fix approach
2. Revert last change and try different strategy
3. Escalate if still stuck

## Escalation Report

When max iterations reached:

```markdown
# Escalation Report

**Feature:** ${FEATURE_NAME}
**Iterations:** ${MAX_ITERATIONS} (limit reached)
**Status:** Needs manual intervention

## Remaining Errors

### Error 1: TypeScript
- File: src/components/Hero.tsx:42
- Message: Type 'string' is not assignable to type 'number'
- Attempts: 3
- Approaches tried:
  1. Cast to number → Introduced new error
  2. Parse string → Runtime error
  3. Change prop type → Broke parent component

### Error 2: Visual
- Issue: CTA button not matching design
- Attempts: 2
- Approaches tried:
  1. Adjusted padding → Still off
  2. Changed font-weight → Closer but not exact

## Recommendations

1. For TS error: Consider refactoring the data flow
2. For visual: May need designer input on exact values

## Artifacts

- Screenshots: history/${FEATURE_ID}/
- Error logs: history/${FEATURE_ID}/errors.log
- State: state.json

## Questions for Jean-Marc

1. Should we accept the current visual as "close enough"?
2. Is the type mismatch a data model issue that needs broader fix?
```

## Quick Fix Mode

For simple errors, skip full verification:

```
IF error is P0 (console/TS):
  1. Apply fix
  2. Wait for HMR
  3. Check only that specific error resolved
  4. Continue to next error

AFTER all P0 fixed:
  Run full verification
```

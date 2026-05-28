# Frontend Debugging Workflow

## When to Use

- JavaScript/TypeScript runtime errors
- React/Vue/Angular component issues
- Rendering problems (blank screen, wrong content)
- State management bugs
- CSS/styling issues
- Browser-specific behavior

## Step 1: Gather Symptoms
use playwright mcp to duplicate.
```
□ What is the exact error message (if any)?
□ Which browser(s) are affected?
□ Is it reproducible consistently?
□ When did it start happening?
□ What changed recently? (git log, deployments)
```

## Step 2: Check the Console

Open browser DevTools (F12) → Console tab

### Look for:
- **Red errors** - JavaScript exceptions, failed imports
- **Yellow warnings** - Deprecations, React warnings
- **Network errors** - Failed fetches, 404s, CORS

### Common patterns:
```
"Cannot read property 'x' of undefined"
→ Accessing property on null/undefined object
→ Check: data loading, optional chaining, default values

"x is not a function"
→ Calling non-function (typo, wrong import)
→ Check: import statements, destructuring

"Maximum call stack exceeded"
→ Infinite recursion or re-render loop
→ Check: useEffect deps, recursive calls

"Failed to fetch"
→ Network error or CORS issue
→ Check: API endpoint, network tab, CORS headers
```

## Step 3: Inspect the Component Tree

For React: React DevTools extension
For Vue: Vue DevTools extension

### Check:
- Is the component mounting at all?
- What props is it receiving?
- What is the current state?
- Are there unexpected re-renders?

## Step 4: Trace the Data Flow

```
1. Where does the data originate? (API, store, props)
2. What transformations happen?
3. Where does it break down?
4. Add console.log at each step if needed
```

### Debugging state issues:
```javascript
// Temporary: log state changes
useEffect(() => {
  console.log('State changed:', state);
}, [state]);
```

## Step 5: Isolate the Problem

### Binary search approach:
1. Comment out half the component
2. Does the error persist?
3. If yes, bug is in remaining code
4. If no, bug is in commented code
5. Repeat until found

### Create minimal reproduction:
- Strip away unrelated code
- Use hardcoded data instead of API
- Remove styling temporarily

## Step 6: CSS Debugging

If it's a styling issue:

```
□ Inspect element → Styles panel
□ Check computed styles vs expected
□ Look for overridden styles (strikethrough)
□ Check specificity conflicts
□ Verify CSS is loading (Network tab)
□ Check media queries / responsive
□ Test with all styles disabled
```

### Common CSS issues:
- z-index stacking context problems
- Flexbox/Grid alignment
- Box model (margin vs padding)
- Position: relative/absolute ancestry

## Step 7: Performance Debugging

If it's slow/janky:

```
1. Performance tab → Record
2. Reproduce the slow behavior
3. Stop recording
4. Look for:
   - Long tasks (red bars)
   - Excessive re-renders
   - Large layout shifts
   - Memory leaks (growing heap)
```

### React-specific:
- Use React.memo() for expensive components
- Check useEffect dependencies
- Profile with React DevTools Profiler

## Step 8: Follow TDD to duplicate & resolve the failing test.
- When bug is identified, follow TDD debugging workflow:
- See: test-driven-development/references/debugging-workflow.md

## Quick Reference: DevTools Shortcuts

| Action | Chrome/Edge | Firefox |
|--------|-------------|---------|
| Open DevTools | F12 | F12 |
| Console | Ctrl+Shift+J | Ctrl+Shift+K |
| Elements | Ctrl+Shift+C | Ctrl+Shift+C |
| Debugger | Ctrl+Shift+P | Ctrl+Shift+Z |
| Clear console | Ctrl+L | Ctrl+Shift+L |

## Breakpoint Debugging

```javascript
// Hard breakpoint
debugger;

// Conditional breakpoint (in DevTools)
// Right-click line → Add conditional breakpoint
// Enter condition: user.id === 123
```

## Common Fixes Reference

| Problem | Likely Fix |
|---------|------------|
| Blank screen | Check for JS errors, check data loading |
| Infinite loop | Check useEffect deps, check setState in render |
| Stale data | Add key prop, check memo deps |
| Event not firing | Check binding, check propagation |
| Style not applying | Check specificity, check class name |

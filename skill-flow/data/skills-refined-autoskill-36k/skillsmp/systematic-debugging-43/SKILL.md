---
name: Systematic Debugging
description: Four-phase root cause analysis for reliable bug fixes
version: 1.0.0
source: Adapted from obra/superpowers
---

# Systematic Debugging

## The Fundamental Rule

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Quick patches create technical debt. Symptoms mask deeper issues. Every fix must address the actual root cause.

## The Four Phases

### Phase 1: Root Cause Investigation

Before touching code, gather evidence:

1. **Read the error carefully**
   ```
   Error: Cannot read properties of undefined (reading 'map')
       at ProductList (src/components/ProductList.tsx:15:24)
       at renderWithHooks (node_modules/react-dom/...)
   ```
   - What exactly failed?
   - Where in the stack trace?
   - What data was involved?

2. **Reproduce consistently**
   ```bash
   # Document exact reproduction steps
   1. Navigate to /products
   2. Click "Filter by category"
   3. Select "Electronics"
   4. Error appears
   ```

3. **Check recent changes**
   ```bash
   git log --oneline -10
   git diff HEAD~3 -- src/components/ProductList.tsx
   ```

4. **Add instrumentation at boundaries**
   ```typescript
   // Before the failing line
   console.log('products:', JSON.stringify(products, null, 2));
   console.log('type:', typeof products);
   console.log('isArray:', Array.isArray(products));
   ```

### Phase 2: Pattern Analysis

Find working examples and compare:

```typescript
// Working component
const WorkingList = ({ items }) => {
  if (!items || items.length === 0) return <Empty />;
  return items.map(item => <Item key={item.id} {...item} />);
};

// Broken component - what's different?
const BrokenList = ({ items }) => {
  return items.map(item => <Item key={item.id} {...item} />);
  // Missing: null check before .map()
};
```

**Key questions:**
- What does working code do that broken code doesn't?
- What assumptions does broken code make?
- Where do the data flows diverge?

### Phase 3: Hypothesis and Testing

Apply the scientific method:

1. **Form specific hypothesis**
   > "The error occurs because `products` is undefined on initial render before the API response arrives."

2. **Test with minimal change**
   ```typescript
   // Test hypothesis: add early return
   if (!products) return <Loading />;
   ```

3. **One variable at a time**
   - Don't bundle multiple fixes
   - Change one thing, test, observe
   - Document what you learned

### Phase 4: Implementation

1. **Write failing test FIRST**
   ```typescript
   it('should handle undefined products gracefully', () => {
     render(<ProductList products={undefined} />);
     expect(screen.getByText('Loading...')).toBeInTheDocument();
   });
   ```

2. **Implement root cause fix**
   ```typescript
   // Fix at the source, not symptoms
   const ProductList = ({ products }: Props) => {
     if (!products) return <Loading />;
     if (products.length === 0) return <Empty />;
     return (
       <ul>
         {products.map(product => (
           <ProductItem key={product.id} product={product} />
         ))}
       </ul>
     );
   };
   ```

3. **Verify without bundling**
   - Only the fix, nothing else
   - Run full test suite
   - Confirm original issue resolved

## Red Flags - Stop and Reassess

| Warning Sign | Action |
|--------------|--------|
| Proposing fix before understanding | Go back to Phase 1 |
| Multiple simultaneous changes | Isolate to one change |
| Third fix attempt failing | Question the architecture |
| "It works but I don't know why" | Keep investigating |

## The Three-Fix Rule

If you've tried 3 fixes without success:

1. **STOP** - More fixes won't help
2. **Step back** - Is the architecture flawed?
3. **Document** - What did each attempt reveal?
4. **Reconsider** - Is this the right approach at all?

## Debugging Toolkit

### Console Methods
```typescript
console.log()      // Basic output
console.table()    // Tabular data
console.trace()    // Stack trace
console.time()     // Performance timing
console.group()    // Grouped logs
```

### React DevTools
- Component props inspection
- State timeline
- Profiler for performance

### Network Tab
- Request/response payloads
- Timing analysis
- Failed requests

### Breakpoints
```typescript
// Conditional breakpoint
debugger; // Only when condition met

// Logpoint (VS Code)
// Right-click line → Add Logpoint
```

## FrankX-Specific Patterns

### Next.js Server Components
```typescript
// Common issue: using client hooks in server components
// Phase 1: Check if component has 'use client'
// Phase 2: Compare with working client components
// Phase 3: Add 'use client' or restructure
```

### API Route Debugging
```typescript
// Add request logging
export async function POST(request: Request) {
  console.log('=== API DEBUG ===');
  const body = await request.json();
  console.log('Body:', JSON.stringify(body, null, 2));
  console.log('Headers:', Object.fromEntries(request.headers));
  // ... rest of handler
}
```

### Hydration Mismatches
```typescript
// Phase 1: Check for Date.now(), Math.random(), or browser APIs
// Phase 2: Find server vs client render differences
// Phase 3: Use useEffect for client-only code
// Phase 4: Verify with 'suppressHydrationWarning' as last resort
```

## When to Use This Skill

- Any bug that isn't immediately obvious
- Bugs that "shouldn't be possible"
- Issues that keep coming back
- Problems others have already attempted to fix

## Related Skills

- `test-driven-development` - Write test for bug first
- `webapp-testing` - E2E debugging with Playwright
- `verification-before-completion` - Ensure fix actually works

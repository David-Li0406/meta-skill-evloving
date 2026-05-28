# Automated Performance Auditing

## The Performance Redline
In 2026, we don't just review for bugs; we review for efficiency.

---

### 1. Database Inefficiency (N+1)
Look for loops that contain database queries.
- **Red Flag**: `items.map(i => ctx.db.get(i.id))`
- **Elite Fix**: Use bulk fetching or batching (e.g., `Convex` parallel queries).

### 2. Bundle Size Regression
A single PR shouldn't increase the main bundle by more than 5%.
- **Audit**: Use `bun run build --profile` to compare the "Before" and "After" sizes.
- **Fix**: Move large dependencies to dynamic imports (`next/dynamic`).

### 3. Memory Leaks (React/Node)
Look for event listeners that aren't cleaned up or `useEffect` hooks with missing dependency arrays.
- **Elite Pattern**: Use `AbortController` for all fetch requests to ensure they are cancelled when a component unmounts.

### 4. Excessive Re-renders (React 19)
With the new React Compiler, re-renders are less frequent, but deep object mutations can still cause issues.
- **Audit**: Use React DevTools to check for "unnecessary" renders in high-traffic components.

# Mock Interview Dialogue Examples

## Example 1: Senior Frontend Engineer - React Performance

### Scenario Setup
- **Role**: Senior Frontend Engineer
- **Company**: E-commerce platform with 10M monthly users
- **Focus**: Performance optimization, state management
- **Duration**: 60 minutes

---

### Technical Deep Dive (35 min)

**Interviewer**: "Our product page is experiencing slow rendering when users scroll through 500+ items. Walk me through how you'd debug and optimize this."

**Candidate**: "I'd start by profiling the issue using React DevTools Profiler. Let me break this down into phases:

1. **Measurement Phase**:
   - Record a profiling session while scrolling
   - Identify components with high render counts
   - Check for unnecessary re-renders using 'why-did-you-render'

2. **Common Culprits**:
   - Are we rendering all 500 items at once? If so, implement virtualization with react-window or react-virtuoso
   - Check if parent state changes trigger re-renders of all children
   - Look for expensive computations in render path

3. **Optimization Strategy**:
   ```javascript
   // Before: Re-renders on every scroll
   function ProductList({ products, filters }) {
     const filteredProducts = products.filter(applyFilters(filters)); // ❌
     return filteredProducts.map(p => <ProductCard key={p.id} {...p} />);
   }

   // After: Memoized filtering + virtualization
   const ProductList = memo(({ products, filters }) => {
     const filteredProducts = useMemo(
       () => products.filter(applyFilters(filters)),
       [products, filters]
     );

     return (
       <VirtualList
         height={800}
         itemCount={filteredProducts.length}
         itemSize={120}
         itemData={filteredProducts}
       >
         {ProductCard}
       </VirtualList>
     );
   });
   ```

**Interviewer**: "Good. What if the ProductCard itself is expensive to render?"

**Candidate**: "I'd apply these techniques:
- Wrap ProductCard with `React.memo` and provide custom comparison function
- Lazy load images with `loading='lazy'` attribute
- Use `useCallback` for event handlers to prevent prop changes
- Consider code-splitting heavy components like image galleries

**Metrics I'd track**:
- First Contentful Paint (FCP)
- Time to Interactive (TTI)
- Cumulative Layout Shift (CLS)
- JavaScript execution time in DevTools Performance tab"

**Interviewer**: "How would you handle real-time price updates for these products without re-rendering the entire list?"

**Candidate**: "I'd implement a granular subscription model:

```javascript
// Context for price updates
const PriceUpdateContext = createContext();

function ProductCard({ productId, ...props }) {
  const [price, setPrice] = useState(props.price);

  useEffect(() => {
    const subscription = priceStream
      .filter(update => update.productId === productId)
      .subscribe(({ newPrice }) => setPrice(newPrice));

    return () => subscription.unsubscribe();
  }, [productId]);

  return <div>Price: ${price}</div>;
}
```

This way, only cards with updated prices re-render, not the entire list."

**Interviewer**: "Excellent. Let's shift to state management. When would you choose Zustand over Redux?"

**Candidate**: "Here's my decision framework:

| Factor | Redux | Zustand |
|--------|-------|---------|
| **Bundle Size** | ~9KB | ~1KB |
| **Boilerplate** | High (actions, reducers, middleware) | Minimal |
| **DevTools** | Excellent time-travel debugging | Basic |
| **Async** | Requires middleware (thunk/saga) | Built-in |
| **Team Size** | Large teams benefit from strict patterns | Small-mid teams |

For this e-commerce scenario:
- If we need complex middleware (analytics, undo/redo), Redux
- If state is mostly server-cache (React Query territory), Zustand + React Query
- If team is < 10 engineers and values iteration speed, Zustand

**Red flag scenario**: If I see Redux stores with 20+ slice files but no middleware usage, I'd recommend migration to Zustand."

---

### System Design Question (25 min)

**Interviewer**: "Design the 'Add to Cart' feature for 10M concurrent users during Black Friday."

**Candidate**: "Let me clarify requirements first:
- Peak load: 10M concurrent, assume 20% active checkout
- Inventory accuracy: Strong consistency needed?
- Cart persistence: Session-based or DB-backed?

**Assuming**:
- 2M active carts
- Eventual consistency acceptable (overselling < 1%)
- 30-day cart retention

**Architecture**:

```
┌─────────────┐
│   Browser   │
│  (Optimistic│
│   Updates)  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐         ┌──────────────┐
│   CDN + WAF     │────────▶│ Redis Cache  │
│ (Rate Limiting) │         │ (Cart Data)  │
└────────┬────────┘         └──────┬───────┘
         │                         │
         ▼                         ▼
┌─────────────────┐         ┌──────────────┐
│  API Gateway    │────────▶│  PostgreSQL  │
│  (Load Balance) │         │ (Inventory)  │
└─────────────────┘         └──────────────┘
         │
         ▼
┌─────────────────┐
│  Message Queue  │
│  (Order Events) │
└─────────────────┘
```

**Key Decisions**:

1. **Cart Storage**: Redis with 30-day TTL
   ```javascript
   // Schema
   cart:{userId} = {
     items: [{productId, quantity, addedAt}],
     lastModified: timestamp
   }
   ```

2. **Inventory Locking**:
   - Soft reserve in cache (5-min TTL)
   - Hard reserve on checkout initiation
   - Release on payment failure/timeout

3. **Optimistic UI**:
   ```javascript
   async function addToCart(productId) {
     // Immediate UI update
     dispatch({ type: 'ADD_TO_CART', payload: { productId } });

     try {
       await api.post('/cart', { productId });
     } catch (err) {
       // Rollback on failure
       dispatch({ type: 'REMOVE_FROM_CART', payload: { productId } });
       toast.error('Item unavailable');
     }
   }
   ```

4. **Scaling**:
   - Horizontal: 100+ API servers behind ALB
   - Redis cluster with 10 shards (shard by userId % 10)
   - Database connection pooling (pgBouncer)

5. **Monitoring**:
   - SLI: 99.9% API success rate, p99 latency < 200ms
   - Alerts: Cart abandonment > 70%, inventory sync lag > 30s"

**Interviewer**: "What happens if Redis goes down?"

**Candidate**: "Circuit breaker pattern:
1. Detect Redis failure (3 consecutive timeouts)
2. Fallback to database-backed cart (degraded mode)
3. Return 503 for writes, allow reads from DB
4. Auto-recover when Redis health check passes
5. Sync missed cart updates via event log replay"

---

## Example 2: Behavioral - Conflict Resolution

### STAR Format Demonstration

**Interviewer**: "Tell me about a time you disagreed with your manager's technical decision."

**Candidate**: "Great question. Let me share a situation from my last role:

**Situation**:
My manager wanted to rewrite our monolithic Node.js app into microservices to solve scaling issues. The team was 5 engineers, and we had a 3-month deadline for a major feature launch.

**Task**:
I needed to balance the long-term vision with immediate delivery constraints while respecting leadership.

**Action**:
1. **Data Gathering** (Week 1):
   - Profiled the monolith — found 90% of load came from 2 endpoints
   - Calculated migration cost: 4 engineer-months for full microservices
   - Proposed alternative: Extract hot paths into separate services, keep core monolith

2. **Stakeholder Alignment** (Week 2):
   - Created comparison doc with metrics:
     - **Full Microservices**: 4-month delay, 20% performance gain
     - **Hybrid Approach**: 0-month delay, 15% performance gain, 2-month payback
   - Presented to manager with Grafana dashboards showing bottlenecks
   - Suggested POC: Extract one service in sprint 1

3. **Execution** (Month 2-3):
   - Built POC for product catalog service (highest load)
   - Deployed with feature flags for gradual rollout
   - Documented migration playbook for future services

**Result**:
- Hit feature deadline on time
- Reduced p99 latency by 60% on catalog endpoints
- Manager adopted hybrid strategy; full migration completed 8 months later
- I was promoted to tech lead for demonstrating data-driven leadership

**Key Lesson**: Disagreement is productive when backed by data and alternative solutions, not just criticism."

---

## Example 3: Coding Challenge - Live Debugging

**Interviewer**: "Here's a buggy React component. Users report it crashes randomly. Debug it."

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetch(`/api/users/${userId}`)
      .then(res => res.json())
      .then(setUser);

    fetch(`/api/users/${userId}/posts`)
      .then(res => res.json())
      .then(setPosts);
  }, []);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>Followers: {user.followers.length}</p>
      {posts.map(post => (
        <Post key={post.id} title={post.title} />
      ))}
    </div>
  );
}
```

**Candidate's Debugging Process**:

"Let me trace through potential issues:

**Bug #1: Race Condition**
- `user` initializes as `null`, but we immediately access `user.name`
- **Fix**: Add null check or loading state

**Bug #2: Missing Dependency**
- `useEffect` has empty deps but uses `userId`
- If `userId` changes, we don't refetch
- **Fix**: Add `userId` to dependency array

**Bug #3: Unhandled Errors**
- Network failures crash the component
- **Fix**: Add error boundaries or try/catch

**Bug #4: Memory Leak**
- If component unmounts before fetch resolves, we call `setUser` on unmounted component
- **Fix**: Cleanup with AbortController

**Corrected Version**:

```javascript
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const abortController = new AbortController();

    Promise.all([
      fetch(`/api/users/${userId}`, { signal: abortController.signal }),
      fetch(`/api/users/${userId}/posts`, { signal: abortController.signal })
    ])
      .then(([userRes, postsRes]) =>
        Promise.all([userRes.json(), postsRes.json()])
      )
      .then(([userData, postsData]) => {
        setUser(userData);
        setPosts(postsData);
        setLoading(false);
      })
      .catch(err => {
        if (err.name !== 'AbortError') {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => abortController.abort();
  }, [userId]); // ✅ Fixed dependency

  if (loading) return <Spinner />;
  if (error) return <ErrorMessage message={error} />;
  if (!user) return null; // ✅ Null safety

  return (
    <div>
      <h1>{user.name}</h1>
      <p>Followers: {user.followers?.length ?? 0}</p> {/* ✅ Optional chaining */}
      {posts.map(post => (
        <Post key={post.id} title={post.title} />
      ))}
    </div>
  );
}
```

**Additional Improvements**:
1. Use React Query for caching/refetching
2. Implement skeleton UI instead of spinner
3. Add retry logic for transient failures"

---

## Interview Evaluation Rubric

| Criteria | Strong | Adequate | Weak |
|----------|--------|----------|------|
| **Technical Depth** | Explains trade-offs, mentions 3+ solutions | Solves problem correctly | Struggles with basic concepts |
| **Communication** | Clear structure, checks understanding | Gets to solution eventually | Rambles or silent |
| **Problem-Solving** | Asks clarifying Qs, breaks down problem | Jumps to solution | Trial-and-error approach |
| **Code Quality** | Handles edge cases, readable naming | Works but brittle | Syntax errors, incomplete |
| **Culture Fit** | Collaborative, learns from feedback | Professional | Defensive or arrogant |

## Post-Interview Debrief Template

**Candidate**: [Name]
**Role**: Senior Frontend Engineer
**Date**: 2025-01-20

### Technical Assessment
- **React/JavaScript**: ✅ Strong — Deep knowledge of hooks, performance patterns
- **System Design**: ✅ Strong — Designed scalable cart system with monitoring
- **Coding**: ✅ Adequate — Solved bug but missed optional chaining initially

### Behavioral
- **Leadership**: ✅ Strong — STAR examples showed ownership and data-driven decisions
- **Communication**: ✅ Strong — Clear explanations, good whiteboarding

### Decision
- **Recommendation**: ✅ Strong Hire
- **Leveling**: L5 (Senior) — Ready for L6 in 12-18 months
- **Concerns**: None major; some TypeScript knowledge gaps

### Next Steps
- Schedule team fit interview with Product Manager
- Extend offer at $180K base + equity

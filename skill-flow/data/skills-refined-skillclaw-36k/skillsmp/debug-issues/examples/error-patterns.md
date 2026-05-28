# Common Error Patterns

**Purpose**: Examples of frequently encountered bugs with systematic debugging approaches.

---

## Pattern 1: React Infinite Re-render

**Symptom:**
```
Warning: Maximum update depth exceeded
Component: LoginForm
```

**Debugging Process:**

```
Step 1: Locate Component
project-intel.mjs --search "LoginForm" --type tsx --json

Step 2: Analyze Symbols
project-intel.mjs --symbols src/components/LoginForm.tsx --json
→ Find useEffect hooks

Step 3: Targeted Read
sed -n '[line-range]p' LoginForm.tsx
→ Check dependency arrays

Step 4: Common Root Cause
useEffect depends on value it mutates:
```typescript
// ❌ BAD: Infinite loop
const [user, setUser] = useState(null)
useEffect(() => {
  setUser({...user, timestamp: Date.now()})  // Mutates user
}, [user])  // ← Depends on user, triggers itself

// ✓ GOOD: Fixed
useEffect(() => {
  setUser(prev => ({...prev, timestamp: Date.now()}))
}, [])  // Empty deps, runs once
```

**Step 5: MCP Verify**
Ref MCP: "React useEffect dependencies"
→ Confirms: Don't include values you mutate in dependencies

**Step 6: Fix**
- Remove mutated value from dependencies, OR
- Use functional setState to avoid dependency
```

**Verification:**
- Test component renders without infinite loop
- Check React DevTools for expected render count
- Confirm useEffect runs only when intended

---

## Pattern 2: N+1 Query Problem

**Symptom:**
```
Slow page load (10+ seconds)
Dashboard with 100 users
Database query count: 101 queries
```

**Debugging Process:**

```
Step 1: Locate Data Fetch
project-intel.mjs --search "fetchUsers" --json

Step 2: Analyze Code
Read the query implementation:
```typescript
// ❌ BAD: N+1 queries
const users = await db.query("SELECT * FROM users")  // 1 query
for (const user of users) {  // N queries in loop
  const posts = await db.query(
    "SELECT * FROM posts WHERE user_id = ?",
    user.id
  )
  user.posts = posts
}

// ✓ GOOD: Single query with JOIN
const usersWithPosts = await db.query(`
  SELECT
    u.*,
    p.id as post_id,
    p.title,
    p.content
  FROM users u
  LEFT JOIN posts p ON u.id = p.user_id
`)
```

**Step 3: MCP Verify**
Ref MCP: "SQL JOIN vs multiple queries performance"
→ Confirms: JOINs are more efficient than loops

**Step 4: Fix**
- Use SQL JOIN to fetch related data in one query, OR
- Use WHERE IN clause: `WHERE user_id IN (?, ?, ...)`, OR
- Batch queries if JOIN not possible
```

**Verification:**
- Measure query count (should be 1 or small constant)
- Compare page load time (should be <1 second)
- Test with large datasets (100+ users)

---

## Pattern 3: Memory Leak

**Symptom:**
```
Browser tab memory grows over time
Eventually crashes after 30 minutes
```

**Debugging Process:**

```
Step 1: Search for Event Listeners
project-intel.mjs --search "addEventListener" --json

Step 2: Check useEffect Cleanup
Look for return functions in useEffect hooks:
```typescript
// ❌ BAD: Memory leak
useEffect(() => {
  window.addEventListener('resize', handleResize)
  // Missing cleanup!
}, [])

// ✓ GOOD: Proper cleanup
useEffect(() => {
  window.addEventListener('resize', handleResize)
  return () => {
    window.removeEventListener('resize', handleResize)  // ← Cleanup
  }
}, [])
```

**Step 3: Common Causes**
- Event listeners without cleanup
- Timers (setTimeout, setInterval) not cleared
- Subscriptions not unsubscribed
- Refs holding large objects

**Step 4: MCP Verify**
Ref MCP: "React useEffect cleanup"
→ Confirms: Always cleanup in return function

**Step 5: Fix**
Add cleanup function to useEffect:
```typescript
useEffect(() => {
  const interval = setInterval(poll, 1000)
  return () => clearInterval(interval)  // ← Cleanup
}, [])
```

**Verification:**
- Monitor memory in Chrome DevTools (should be stable)
- Let page run for 30+ minutes (no crashes)
- Check event listener count in Performance tab

---

## Pattern Identification Checklist

When debugging, check if error matches known patterns:

- [ ] **Infinite re-render?** → Check useEffect dependencies
- [ ] **Slow queries?** → Check for loops around database calls
- [ ] **Memory growth?** → Check for missing cleanup functions
- [ ] **TypeErrors on properties?** → Check for missing null checks
- [ ] **Stale closures?** → Check dependency arrays in hooks

If pattern matches, follow the systematic debugging process above.

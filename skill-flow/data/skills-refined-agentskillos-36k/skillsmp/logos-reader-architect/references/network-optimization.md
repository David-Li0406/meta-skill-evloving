# Network Request Optimization Guide

Principles for eliminating duplicate API requests in React + Supabase apps.

---

## Table of Contents

1. [Common Duplicate Sources](#common-duplicate-sources)
2. [Diagnostic Process](#diagnostic-process)
3. [Fix Patterns](#fix-patterns)
4. [React Query Best Practices](#react-query-best-practices)
5. [Checklist](#checklist)

---

## Common Duplicate Sources

### 1. Parallel Data Fetching (Most Common)

**Problem:** Multiple components or hooks fetch the same data independently.

```
SearchProvider → useTopicsSearch() → searchTopics()
SearchPage → useUnifiedSearch() → searchTopics()
```

**Fix:** Single source of truth. One hook fetches, others consume via props or context.

### 2. Nested Fetch in Service Functions

**Problem:** A service function fetches related data that's also fetched separately.

```typescript
// BAD: searchText fetches topics internally
async function searchText(term) {
  const [verses, topics] = await Promise.all([
    fetchVerses(term),
    searchTopics(term),  // Also called separately by React Query!
  ]);
}
```

**Fix:** Remove nested fetches when React Query manages them separately.

### 3. Provider + Component Both Logging

**Problem:** Context provider and child component both have logging side effects.

```
SearchProvider → useEffect → logActivity(), saveHistory()
SearchPage → useEffect → logActivity(), saveHistory()  // Duplicate!
```

**Fix:** Log in exactly one place. Prefer the component using the data.

### 4. Child Components Fetching Prop Data

**Problem:** Parent passes data as props, but child also fetches it.

```typescript
// Parent passes preferences
<TopicsSection isCollapsed={preferences.collapsed} />

// Child ALSO fetches preferences internally
useEffect(() => {
  const { data } = await supabase.from("profiles").select("collapsed");
}, []);
```

**Fix:** Trust props. Only fetch internally if prop is undefined.

### 5. Unused Provider Wrappers

**Problem:** Provider exists but its context is never consumed.

```typescript
// SearchProvider provides useSearch() context
// But SearchPage uses useUnifiedSearch() instead
// Provider's hooks still run and make requests!
```

**Fix:** Remove unused providers entirely.

---

## Diagnostic Process

### Step 1: Capture Network Log

Open DevTools Network tab, filter by domain, execute the action, sort by timestamp.

### Step 2: Identify Duplicates

Look for:
- Same endpoint called multiple times
- Same timestamp (parallel duplicates)
- Sequential duplicates (triggered by different effects)

### Step 3: Trace Call Sites

```bash
# Find all callers of a function
grep -rn "searchTopics" --include="*.ts" --include="*.tsx" src/
```

### Step 4: Identify Root Cause

For each duplicate, determine:
- Which component/hook is calling?
- Is it via direct call or hook?
- Are React Query keys identical? (Should deduplicate automatically)

---

## Fix Patterns

### Pattern 1: Lift State Up

**Before:**
```typescript
// Child fetches its own data
function TopicsSection() {
  const [collapsed, setCollapsed] = useState(false);
  useEffect(() => {
    fetchPreferences().then(p => setCollapsed(p.collapsed));
  }, []);
}
```

**After:**
```typescript
// Parent fetches, child receives
function SearchPage() {
  const { preferences } = useUserPreferences();
  return <TopicsSection isCollapsed={preferences.collapsed} />;
}

function TopicsSection({ isCollapsed }) {
  // No fetch needed
}
```

### Pattern 2: Conditional Internal Fetch

When a component needs to work standalone AND as a child:

```typescript
function TopicsSection({
  isCollapsed: externalCollapsed,  // From parent
  onToggle: externalToggle
}) {
  const [internalCollapsed, setInternal] = useState(false);

  // Only fetch if not provided externally
  useEffect(() => {
    if (externalCollapsed !== undefined) return;
    fetchPreferences().then(p => setInternal(p.collapsed));
  }, [externalCollapsed]);

  const isCollapsed = externalCollapsed ?? internalCollapsed;
  const toggle = externalToggle ?? (() => setInternal(v => !v));
}
```

### Pattern 3: Remove Nested Parallel Fetches

**Before:**
```typescript
async function searchText(term) {
  const [verses, topics] = await Promise.all([
    supabase.rpc("search_text", { term }),
    searchTopics(term),  // Duplicated elsewhere
  ]);
  return { verses, topics };
}
```

**After:**
```typescript
// Topics fetched separately via React Query
async function searchText(term) {
  const { data } = await supabase.rpc("search_text", { term });
  return { verses: data };
}
```

### Pattern 4: Remove Unused Providers

**Before:**
```typescript
// SearchProvider makes requests via its hooks
const SearchPage = () => (
  <SearchProvider>
    <SearchPageContent />  {/* Uses different hooks */}
  </SearchProvider>
);
```

**After:**
```typescript
// No wrapper needed
const SearchPage = () => <SearchPageContent />;
```

---

## React Query Best Practices

### Use Identical Query Keys

React Query deduplicates by key. Ensure hooks use the same key structure:

```typescript
// GOOD: Same key = automatic deduplication
const topicsKey = ["search", "topics", query];

// Hook A
useQuery({ queryKey: topicsKey, queryFn: searchTopics });

// Hook B (same key = shares cache, no duplicate request)
useQuery({ queryKey: topicsKey, queryFn: searchTopics });
```

### Query Key Factories

Centralize keys to prevent typos:

```typescript
const searchKeys = {
  topics: (q: string) => ["search", "topics", q] as const,
  verses: (q: string, v: string) => ["search", "verses", q, v] as const,
};
```

### Stale Time for Static Data

Prevent refetches for rarely-changing data:

```typescript
useQuery({
  queryKey: ["bible", "versions"],
  queryFn: fetchVersions,
  staleTime: 60 * 60 * 1000,  // 1 hour
});
```

---

## Checklist

Before shipping, verify:

- [ ] Each API endpoint called exactly once per user action
- [ ] No provider wrappers with unused contexts
- [ ] Child components receive data via props (not redundant fetches)
- [ ] Service functions don't fetch data that React Query manages
- [ ] Side effects (logging, history) happen in exactly one place
- [ ] React Query keys are consistent across all hooks

### Network Request Audit Template

| Endpoint | Expected | Actual | Source |
|----------|----------|--------|--------|
| `/profiles` | 1 | ? | useUserPreferences |
| `/search_topics` | 1 | ? | useUnifiedSearch |
| `/search_text` | 1 | ? | useUnifiedSearch |
| `/user_activity_log` POST | 1 | ? | SearchPage |
| `/search_history` POST | 1 | ? | SearchPage |

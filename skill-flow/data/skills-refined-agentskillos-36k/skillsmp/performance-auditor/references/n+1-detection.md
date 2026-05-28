# N+1 Query Detection and Prevention

Finding and fixing N+1 query patterns that cause performance degradation.

## Table of Contents
1. [Common N+1 Patterns](#common-n+1-patterns)
2. [Detection Strategies](#detection-strategies)
3. [Solutions](#solutions)

## Common N+1 Patterns

### Pattern 1: Loop with Individual Queries (TypeScript)
```typescript
// ❌ BAD: N+1 queries
const { data: topics } = useQuery(['topics'], fetchTopics);

// For each topic, fetch verses separately
topics?.forEach(topic => {
  const { data: verses } = useQuery(
    ['verses', topic.id],
    () => fetchTopicVerses(topic.id) // N queries!
  );
});

// ✅ GOOD: Single query with JOIN
const { data: topicsWithVerses } = useQuery(
  ['topics-with-verses'],
  async () => {
    const { data } = await supabase
      .from('topics')
      .select(`
        *,
        topic_verses(
          verse:verses(*)
        )
      `);
    return data;
  }
);

// ✅ BETTER: Use RPC function
const { data: topicsWithVerses } = useQuery(
  ['topics-with-verses'],
  async () => {
    const { data } = await supabase.rpc('get_topics_with_verses');
    return data;
  }
);
```

### Pattern 2: Sequential Data Loading
```typescript
// ❌ BAD: Waterfall requests
useEffect(() => {
  fetchUser().then(user => {
    fetchUserPreferences(user.id).then(prefs => {
      fetchUserBookmarks(user.id).then(bookmarks => {
        // Now we have all data
      });
    });
  });
}, []);

// ✅ GOOD: Parallel requests
useEffect(() => {
  const userId = userContext.userId;
  Promise.all([
    fetchUserPreferences(userId),
    fetchUserBookmarks(userId),
    fetchUserReadings(userId)
  ]).then(([prefs, bookmarks, readings]) => {
    // All data loaded in parallel
  });
}, []);
```

### Pattern 3: Loading Related Items in Loop
```typescript
// ❌ BAD: Query per item in array
function TopicList({ topics }) {
  return topics.map(topic => (
    <TopicCard key={topic.id} topic={topic} />
  ));
}

function TopicCard({ topic }) {
  const { data: verses } = useQuery(
    ['verses', topic.id],
    () => fetchTopicVerses(topic.id)  // N queries!
  );
  return <div>{verses?.length} verses</div>;
}

// ✅ GOOD: Load all verses at once
function TopicList({ topics }) {
  const topicIds = topics.map(t => t.id);
  const { data: versesByTopic } = useQuery(
    ['verses', topicIds],
    () => fetchTopicVerses(topicIds)  // 1 query!
  );

  return topics.map(topic => (
    <TopicCard
      key={topic.id}
      topic={topic}
      verses={versesByTopic?.[topic.id]}
    />
  ));
}
```

## Detection Strategies

### Strategy 1: Browser Network Tab Analysis
```typescript
// Add request logging to identify N+1
if (process.env.NODE_ENV === 'development') {
  const originalFetch = window.fetch;
  const requestLog: string[] = [];

  window.fetch = async (...args) => {
    const url = args[0];
    requestLog.push(url);

    // Warn if many requests to same endpoint
    const endpoint = new URL(url).pathname;
    const sameEndpointCount = requestLog.filter(u =>
      new URL(u).pathname === endpoint
    ).length;

    if (sameEndpointCount > 3) {
      console.warn(`Potential N+1 detected: ${sameEndpointCount} requests to ${endpoint}`, requestLog);
    }

    return originalFetch(...args);
  };
}
```

### Strategy 2: Query Profiling
```typescript
// Monitor React Query for rapid sequential queries
let queryTimes: { queryKey: any, timestamp: number }[] = [];

const monitoringMiddleware = (config: any) => {
  return {
    ...config,
    onSuccess: (data: any, query: any) => {
      queryTimes.push({
        queryKey: query.queryKey,
        timestamp: Date.now()
      });

      // Alert if many queries in short succession
      const recentQueries = queryTimes.filter(
        q => Date.now() - q.timestamp < 500
      );

      if (recentQueries.length > 5) {
        console.warn('Potential N+1: ', recentQueries.length, 'queries in 500ms', recentQueries);
      }
    }
  };
};
```

### Strategy 3: Database Query Logging
```sql
-- Identify sequential queries from same session
SELECT
  query,
  query_start,
  query_plan_startup_time,
  query_plan_total_time,
  calls,
  -- Group by 100ms windows to find "bursts"
  FLOOR(EXTRACT(EPOCH FROM query_start) * 10) as time_bucket
FROM pg_stat_statements
WHERE userid = current_user_id
  AND query NOT LIKE '%pg_stat%'
ORDER BY query_start DESC
LIMIT 50;

-- Find tables with high sequential scan rates (N+1 indicator)
SELECT
  tablename,
  seq_scan,
  idx_scan,
  seq_scan + idx_scan as total_scans,
  CASE
    WHEN seq_scan > idx_scan * 10 THEN 'LIKELY N+1'
    WHEN seq_scan > idx_scan THEN 'Possible N+1'
    ELSE 'OK'
  END as assessment
FROM pg_stat_user_tables
WHERE seq_scan > 100
ORDER BY seq_scan DESC
LIMIT 20;
```

## Solutions

### Solution 1: Preloading Related Data
```typescript
// Load all related data upfront
const { data: topics } = useQuery(['topics-full'], async () => {
  const { data } = await supabase
    .from('topics')
    .select(`
      *,
      topic_relations(
        related_topic:related_topics(*)
      ),
      topic_verses(
        verse:verses(*)
      )
    `);
  return data;
});
```

### Solution 2: Batch Fetch Wrapper
```typescript
// Create utility for batch fetching
async function fetchInBatches<T>(
  ids: string[],
  fetchFn: (ids: string[]) => Promise<T[]>,
  batchSize = 50
) {
  const results: T[] = [];

  for (let i = 0; i < ids.length; i += batchSize) {
    const batch = ids.slice(i, i + batchSize);
    const batchResults = await fetchFn(batch);
    results.push(...batchResults);
  }

  return results;
}

// Usage
const verses = await fetchInBatches(
  topicIds,
  (ids) => supabase.from('topic_verses')
    .select('*')
    .in('topic_id', ids)
);
```

### Solution 3: Memoization Layer
```typescript
// Cache individual items after batch load
const verseCache = new Map<string, Verse>();

async function getVerses(ids: string[]) {
  const uncached = ids.filter(id => !verseCache.has(id));

  if (uncached.length > 0) {
    const fresh = await supabase
      .from('verses')
      .select('*')
      .in('id', uncached);

    fresh.data?.forEach(v => verseCache.set(v.id, v));
  }

  return ids.map(id => verseCache.get(id));
}
```

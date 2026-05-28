---
name: supabase-query-patterns
description: Use this skill when writing Supabase queries, SQL statements, or database-related TypeScript code. Ensures optimal query patterns, performance, and best practices.
---

# Supabase Query Patterns Skill

Use this skill when writing Supabase queries, SQL statements, or database-related TypeScript code.

## When to Use

- Writing Supabase client queries in API routes
- Optimizing database query performance
- Reviewing code for N+1 problems
- Writing SQL for migrations or RPC functions

## Query Parallelization

依存関係がない複数のSupabaseクエリは `Promise.all` で並列実行する。

### BAD: Sequential Execution
```typescript
const usersResult = await supabase.from('m_users').select('id, name');
const facilitiesResult = await supabase.from('m_facilities').select('id, name');
const classesResult = await supabase.from('m_classes').select('id, name');
// Total time: query1 + query2 + query3
```

### GOOD: Parallel Execution
```typescript
const [usersResult, facilitiesResult, classesResult] = await Promise.all([
  supabase.from('m_users').select('id, name'),
  supabase.from('m_facilities').select('id, name'),
  supabase.from('m_classes').select('id, name'),
]);
// Total time: max(query1, query2, query3)
```

## Loop Search Optimization (Map Conversion)

ループ内で `find()` や `filter()` を使う場合、事前にMapに変換してO(1)でアクセスする。

### BAD: O(n^2) Complexity
```typescript
children.map(child => {
  const schedule = schedules.find(s => s.child_id === child.id);
  return { ...child, schedule };
});
```

### GOOD: O(n) Complexity with Map
```typescript
const scheduleMap = new Map(schedules.map(s => [s.child_id, s]));
children.map(child => {
  const schedule = scheduleMap.get(child.id);
  return { ...child, schedule };
});
```

## Select Only Required Columns

### BAD: Select All
```typescript
const { data } = await supabase.from('m_children').select('*');
```

### GOOD: Select Specific Columns
```typescript
const { data } = await supabase.from('m_children').select('id, name, class_id');
```

## Avoid N+1 Problem

### BAD: Query in Loop
```typescript
for (const child of children) {
  const { data: records } = await supabase
    .from('r_observation')
    .select('*')
    .eq('child_id', child.id);
}
```

### GOOD: Batch Query with IN
```typescript
const childIds = children.map(c => c.id);
const { data: records } = await supabase
  .from('r_observation')
  .select('*')
  .in('child_id', childIds);

// Then group by child_id using Map
const recordsByChild = new Map();
records?.forEach(r => {
  const arr = recordsByChild.get(r.child_id) || [];
  arr.push(r);
  recordsByChild.set(r.child_id, arr);
});
```

## Use JOINs for Related Data

### GOOD: Foreign Table Join
```typescript
const { data } = await supabase
  .from('r_observation')
  .select(`
    id,
    content,
    child:m_children!child_id (
      id,
      name
    )
  `)
  .eq('facility_id', facilityId);
```

## Performance Checklist

Before committing database-related code, verify:

- [ ] **Query Count**: Are sequential queries parallelized with `Promise.all`?
- [ ] **O(n^2) Loops**: Are `find()`/`filter()` in loops converted to Map?
- [ ] **Select Columns**: Using specific columns instead of `select('*')`?
- [ ] **N+1 Problem**: No queries inside loops? Using `.in()` for batch queries?
- [ ] **JOINs**: Using foreign table syntax for related data?
- [ ] **Indexes**: Common query patterns covered by database indexes?

## Error Handling Pattern

```typescript
const { data, error } = await supabase
  .from('m_children')
  .select('id, name')
  .eq('facility_id', facilityId);

if (error) {
  console.error('Database error:', error);
  return NextResponse.json({ error: 'Database error' }, { status: 500 });
}

if (!data || data.length === 0) {
  return NextResponse.json({ error: 'Not found' }, { status: 404 });
}
```

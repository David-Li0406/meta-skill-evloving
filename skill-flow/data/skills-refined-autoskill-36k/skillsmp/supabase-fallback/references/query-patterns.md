# Supabase Query Patterns

## 기본 조회

```typescript
// 전체 조회
const { data, error } = await supabase
  .from('posts')
  .select('*');

// metadata 기반 필터
const { data } = await supabase
  .from('posts')
  .select('*')
  .eq('metadata->>type', 'office');
```

## 관계 조회 (Join)

```typescript
// Foreign key 관계 조회
const { data } = await supabase
  .from('posts')
  .select(`
    *,
    author:users!created_by(id, username, avatar_url),
    board:boards!board_id(id, name)
  `)
  .eq('metadata->>type', 'office');
```

## 페이지네이션

```typescript
// 페이지네이션
const { data, count } = await supabase
  .from('posts')
  .select('*', { count: 'exact' })
  .eq('metadata->>type', 'office')
  .order('created_at', { ascending: false })
  .range(0, 9);  // 0-9 (10개)
```

## 검색

```typescript
// ilike 검색
const { data } = await supabase
  .from('posts')
  .select('*')
  .ilike('title', `%${searchTerm}%`);

// Full-text 검색 (textSearch 설정 필요)
const { data } = await supabase
  .from('posts')
  .select('*')
  .textSearch('title', searchTerm);
```

## metadata 필터링

```typescript
// 중첩 필드 접근
const { data } = await supabase
  .from('locations')
  .select('*')
  .eq('metadata->>type', 'office')
  .gte('metadata->>capacity', 10);

// 배열 포함 확인
const { data } = await supabase
  .from('locations')
  .select('*')
  .contains('metadata->amenities', ['wifi', 'parking']);
```

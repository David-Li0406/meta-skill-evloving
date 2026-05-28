# Supabase Mutation Patterns

## 생성

```typescript
const { data, error } = await supabase
  .from('posts')
  .insert({
    title: 'New Post',
    content: 'Content here',
    board_id: boardId,
    created_by: userId,
    metadata: {
      type: 'office',
      officeId: 'uuid-here',
    },
  })
  .select()
  .single();
```

## 수정

```typescript
// 전체 업데이트
const { data, error } = await supabase
  .from('posts')
  .update({
    title: 'Updated Title',
    updated_at: new Date().toISOString(),
  })
  .eq('id', postId)
  .select()
  .single();

// metadata 병합
const { data, error } = await supabase
  .from('posts')
  .update({
    metadata: supabase.sql`metadata || '{"pinned": true}'::jsonb`,
  })
  .eq('id', postId)
  .select()
  .single();
```

## 삭제

```typescript
// Hard delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId);

// Soft delete (metadata 활용)
const { error } = await supabase
  .from('posts')
  .update({
    metadata: supabase.sql`metadata || '{"deleted": true, "deleted_at": "${new Date().toISOString()}"}'::jsonb`,
  })
  .eq('id', postId);
```

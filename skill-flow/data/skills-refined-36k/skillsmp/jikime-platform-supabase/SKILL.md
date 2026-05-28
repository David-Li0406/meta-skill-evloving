---
name: jikime-platform-supabase
description: Supabase specialist covering PostgreSQL 16, pgvector, RLS, real-time subscriptions, and Edge Functions. Use when building full-stack apps with Supabase backend.
version: 1.0.0
tags: ["platform", "supabase", "postgresql", "realtime", "auth", "pgvector"]
triggers:
  keywords: ["supabase", "postgresql", "RLS", "realtime", "pgvector", "수파베이스"]
  phases: ["run"]
  agents: ["backend"]
  languages: ["typescript", "sql"]
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~2000
user-invocable: false
---

# Supabase Development Guide

Supabase + Next.js 개발을 위한 간결한 가이드.

## Quick Reference

| 기능 | 설명 |
|------|------|
| **PostgreSQL 16** | 풀 SQL, JSONB |
| **pgvector** | AI 임베딩, 벡터 검색 |
| **RLS** | Row Level Security |
| **Realtime** | 실시간 구독 |
| **Auth** | 인증, JWT |
| **Storage** | 파일 스토리지 |

## Setup

### Next.js 클라이언트

```bash
npm install @supabase/supabase-js @supabase/ssr
```

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}

// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookies) {
          cookies.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options)
          );
        },
      },
    }
  );
}
```

## Database

### 테이블 생성

```sql
-- Users 테이블
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Posts 테이블
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT,
  published BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 인덱스
CREATE INDEX posts_author_idx ON posts(author_id);
```

### CRUD Operations

```typescript
const supabase = createClient();

// Create
const { data, error } = await supabase
  .from('posts')
  .insert({ title: 'Hello', content: 'World', author_id: userId })
  .select()
  .single();

// Read
const { data: posts } = await supabase
  .from('posts')
  .select('*, author:users(name, email)')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .limit(10);

// Update
const { data } = await supabase
  .from('posts')
  .update({ title: 'Updated' })
  .eq('id', postId)
  .select()
  .single();

// Delete
const { error } = await supabase
  .from('posts')
  .delete()
  .eq('id', postId);
```

## Row Level Security (RLS)

```sql
-- RLS 활성화
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- 읽기: 공개 게시물은 모두 볼 수 있음
CREATE POLICY "Public posts are viewable"
  ON posts FOR SELECT
  USING (published = true);

-- 쓰기: 본인 게시물만 수정 가능
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = author_id);

-- 삭제: 본인 게시물만 삭제 가능
CREATE POLICY "Users can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = author_id);

-- 삽입: 인증된 사용자만 생성 가능
CREATE POLICY "Authenticated can insert"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() IS NOT NULL);
```

## pgvector (AI 임베딩)

```sql
-- Extension 활성화
CREATE EXTENSION IF NOT EXISTS vector;

-- 임베딩 테이블
CREATE TABLE documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  embedding VECTOR(1536), -- OpenAI embedding 차원
  metadata JSONB DEFAULT '{}'
);

-- HNSW 인덱스 (빠른 검색)
CREATE INDEX documents_embedding_idx
  ON documents USING hnsw (embedding vector_cosine_ops);

-- 유사도 검색 함수
CREATE OR REPLACE FUNCTION search_documents(
  query_embedding VECTOR(1536),
  match_count INT DEFAULT 5
)
RETURNS TABLE (id UUID, content TEXT, similarity FLOAT)
AS $$
  SELECT id, content, 1 - (embedding <=> query_embedding) AS similarity
  FROM documents
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$ LANGUAGE SQL;
```

```typescript
// 벡터 검색
const { data } = await supabase.rpc('search_documents', {
  query_embedding: embedding,
  match_count: 5
});
```

## Realtime

```typescript
// 실시간 구독
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change:', payload);
    }
  )
  .subscribe();

// 필터 적용
const channel = supabase
  .channel('user-posts')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'posts',
      filter: `author_id=eq.${userId}`,
    },
    (payload) => {
      console.log('New post:', payload.new);
    }
  )
  .subscribe();

// 구독 해제
supabase.removeChannel(channel);
```

## Authentication

```typescript
// 로그인
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123',
});

// 회원가입
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
});

// OAuth
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: { redirectTo: `${origin}/auth/callback` },
});

// 세션 확인
const { data: { user } } = await supabase.auth.getUser();

// 로그아웃
await supabase.auth.signOut();
```

## Storage

```typescript
// 업로드
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true,
  });

// 공개 URL
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.png`);

// 삭제
await supabase.storage
  .from('avatars')
  .remove([`${userId}/avatar.png`]);
```

## Edge Functions (Deno)

```typescript
// supabase/functions/hello/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  const { data, error } = await supabase.from('posts').select('*');

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  });
});
```

```bash
# 배포
supabase functions deploy hello
```

## Best Practices

- **RLS 필수**: 모든 테이블에 RLS 활성화
- **인덱스**: 자주 쿼리하는 컬럼에 인덱스 추가
- **타입 생성**: `supabase gen types typescript`
- **서버 클라이언트**: 서버 컴포넌트에서 서버 클라이언트 사용
- **에러 처리**: 모든 쿼리에서 error 확인

---

Last Updated: 2026-01-21
Version: 2.0.0

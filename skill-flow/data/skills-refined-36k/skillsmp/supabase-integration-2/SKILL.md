---
name: supabase-integration
description: >
  Supabase 프로젝트 설정, 데이터베이스 설계, RLS 정책, Edge Functions,
  인증/권한 통합 전문 스킬. Supabase CLI 및 클라이언트 라이브러리 활용.
version: 2.0.0

triggers:
  keywords:
    - "supabase"
    - "RLS"
    - "Row Level Security"
    - "Edge Function"
    - "supabase auth"
    - "실시간 구독"
  file_patterns:
    - "supabase/**/*"
    - "**/supabase.ts"
    - "**/supabase.js"
    - "**/*.sql"
  context:
    - "Supabase 프로젝트 설정"
    - "데이터베이스 스키마 설계"
    - "인증 시스템 구축"

capabilities:
  - init_supabase_project
  - design_database_schema
  - create_rls_policies
  - setup_edge_functions
  - configure_auth
  - setup_realtime

model_preference: sonnet

auto_trigger: true
---

# Supabase Integration Skill

Supabase 백엔드 서비스 통합을 위한 전문 스킬입니다.

## Quick Start

```bash
# Supabase CLI 설치
npm install -g supabase

# 프로젝트 초기화
supabase init

# 로컬 개발 환경 시작
supabase start

# 마이그레이션 생성
supabase migration new <migration_name>
```

## 환경 변수 설정

### API 키 시스템 (2025 업데이트)

> **중요**: Supabase가 새로운 키 시스템으로 전환 중입니다.
> - 2026년 말: 레거시 키(anon/service_role) 제거 예정
> - 신규 프로젝트는 새 키 사용 권장

| 키 타입 | 새 키 (권장) | 레거시 키 | 용도 |
|---------|-------------|----------|------|
| 클라이언트 | `sb_publishable_...` | `anon key` | 브라우저/앱 |
| 서버 | `sb_secret_...` | `service_role` | 백엔드 전용 |

### 필수 환경 변수

```bash
# 새 키 시스템 (권장)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...
SUPABASE_SECRET_KEY=sb_secret_...

# 레거시 키 (2026년까지 지원)
# NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
# SUPABASE_SERVICE_ROLE_KEY=eyJhbG...
```

### 환경 변수 위치

```
Supabase Dashboard > Settings > API
├── Project URL       → NEXT_PUBLIC_SUPABASE_URL
├── Publishable key   → NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY (신규)
├── Secret key        → SUPABASE_SECRET_KEY (신규, 서버만!)
│
├── [Legacy] anon key        → NEXT_PUBLIC_SUPABASE_ANON_KEY
└── [Legacy] service_role    → SUPABASE_SERVICE_ROLE_KEY
```

### 새 키 vs 레거시 키 차이점

| 항목 | 새 키 | 레거시 키 |
|------|-------|----------|
| 형식 | `sb_publishable_...` | JWT (eyJhbG...) |
| 독립 로테이션 | ✅ 가능 | ❌ 불가 |
| 다운타임 없는 교체 | ✅ | ❌ |
| 모바일 앱 배포 | ✅ 용이 | ❌ 강제 업데이트 필요 |

### 템플릿 사용

```bash
# 템플릿 복사
cp .claude/skills/supabase-integration/assets/.env.supabase.template .env.local
```

### 로컬 개발 시

```bash
# supabase start 실행 후 표시되는 값 사용
supabase start
# → API URL: http://127.0.0.1:54321
# → anon key: eyJhbG... (로컬은 레거시 형식)
```

## 핵심 기능

### 1. 프로젝트 설정

```
┌─────────────────────────────────────────────────────────────┐
│  Supabase 프로젝트 구조                                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  project/                                                    │
│  ├── supabase/                                               │
│  │   ├── config.toml          # 프로젝트 설정                │
│  │   ├── migrations/          # DB 마이그레이션              │
│  │   │   └── 20240101_init.sql                               │
│  │   ├── functions/           # Edge Functions               │
│  │   │   └── hello/index.ts                                  │
│  │   └── seed.sql             # 초기 데이터                  │
│  ├── src/                                                    │
│  │   └── lib/supabase.ts      # 클라이언트 설정              │
│  └── .env.local               # 환경 변수                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 2. 데이터베이스 스키마 설계

#### 테이블 생성 패턴

```sql
-- 기본 테이블 구조
CREATE TABLE public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  username TEXT UNIQUE NOT NULL,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- updated_at 자동 갱신 트리거
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
  BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

#### 관계 설정

```sql
-- 1:N 관계
CREATE TABLE public.posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- N:M 관계 (중간 테이블)
CREATE TABLE public.post_tags (
  post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES public.tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id)
);
```

### 3. RLS (Row Level Security) 정책

#### RLS 활성화 필수

```sql
-- RLS 활성화
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
```

#### 일반적인 RLS 패턴

```sql
-- 패턴 1: 본인 데이터만 접근
CREATE POLICY "Users can view own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id);

-- 패턴 2: 공개 읽기 + 본인만 수정
CREATE POLICY "Anyone can view posts"
  ON public.posts FOR SELECT
  USING (true);

CREATE POLICY "Users can insert own posts"
  ON public.posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts"
  ON public.posts FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts"
  ON public.posts FOR DELETE
  USING (auth.uid() = user_id);

-- 패턴 3: 역할 기반 접근
CREATE POLICY "Admins can do anything"
  ON public.posts FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM public.profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );
```

### 4. Edge Functions

#### 기본 구조

```typescript
// supabase/functions/hello/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}

serve(async (req) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // Supabase 클라이언트 생성
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    )

    // 인증된 사용자 확인
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError) throw authError

    // 비즈니스 로직
    const { data, error } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single()

    if (error) throw error

    return new Response(
      JSON.stringify({ data }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )

  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

#### 배포

```bash
# 로컬 테스트
supabase functions serve hello --env-file .env.local

# 배포
supabase functions deploy hello
```

### 5. 클라이언트 설정

#### TypeScript 클라이언트

```typescript
// src/lib/supabase.ts
import { createClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey)
```

#### 타입 생성

```bash
# 타입 자동 생성
supabase gen types typescript --local > src/lib/database.types.ts

# 원격 DB에서 생성
supabase gen types typescript --project-id <project_id> > src/lib/database.types.ts
```

### 6. 인증 설정

#### 이메일/패스워드 인증

```typescript
// 회원가입
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
})

// 로그인
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123',
})

// 로그아웃
await supabase.auth.signOut()

// 현재 사용자
const { data: { user } } = await supabase.auth.getUser()
```

#### OAuth 인증

```typescript
// Google 로그인
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'google',
  options: {
    redirectTo: `${window.location.origin}/auth/callback`
  }
})

// GitHub 로그인
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github',
})
```

### 7. 실시간 구독

```typescript
// 테이블 변경 구독
const channel = supabase
  .channel('posts-changes')
  .on(
    'postgres_changes',
    {
      event: '*',  // INSERT, UPDATE, DELETE
      schema: 'public',
      table: 'posts',
      filter: 'user_id=eq.{user_id}'
    },
    (payload) => {
      console.log('Change:', payload)
    }
  )
  .subscribe()

// 구독 해제
supabase.removeChannel(channel)
```

### 8. Storage 설정

```sql
-- 버킷 생성 (SQL)
INSERT INTO storage.buckets (id, name, public)
VALUES ('avatars', 'avatars', true);

-- Storage RLS 정책
CREATE POLICY "Avatar images are publicly accessible"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

CREATE POLICY "Users can upload own avatar"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars' AND
    auth.uid()::text = (storage.foldername(name))[1]
  );
```

```typescript
// 파일 업로드
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file)

// 공개 URL 가져오기
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('path/to/file.png')
```

## CLI 명령어 참조

| 명령어 | 용도 |
|--------|------|
| `supabase init` | 프로젝트 초기화 |
| `supabase start` | 로컬 환경 시작 |
| `supabase stop` | 로컬 환경 중지 |
| `supabase db reset` | DB 초기화 + 마이그레이션 재실행 |
| `supabase migration new <name>` | 새 마이그레이션 생성 |
| `supabase db push` | 로컬 변경사항 원격 적용 |
| `supabase db pull` | 원격 스키마 로컬로 가져오기 |
| `supabase gen types typescript` | TypeScript 타입 생성 |
| `supabase functions serve` | Edge Function 로컬 실행 |
| `supabase functions deploy` | Edge Function 배포 |

## 체크리스트

### 프로젝트 설정

- [ ] `supabase init` 실행
- [ ] `.env.local`에 URL, Publishable Key 설정 (또는 레거시 anon key)
- [ ] 클라이언트 라이브러리 설치 (`@supabase/supabase-js`)

### 데이터베이스

- [ ] 테이블 스키마 설계
- [ ] 외래 키 관계 설정
- [ ] 인덱스 추가 (자주 조회하는 컬럼)
- [ ] updated_at 트리거 설정

### 보안

- [ ] 모든 테이블 RLS 활성화
- [ ] SELECT/INSERT/UPDATE/DELETE 정책 설정
- [ ] 민감 데이터 접근 제한 확인
- [ ] Publishable vs Secret 키 구분 사용 (서버에만 Secret)

### 인증

- [ ] 인증 제공자 설정 (이메일, OAuth)
- [ ] 리다이렉트 URL 설정
- [ ] 회원가입 시 profiles 테이블 자동 생성 트리거

## Anti-Patterns

| 금지 | 이유 | 대안 |
|------|------|------|
| RLS 없이 배포 | 데이터 노출 위험 | 모든 테이블 RLS 활성화 |
| Secret 키 클라이언트 노출 | 전체 DB 접근 가능 | Publishable 키만 클라이언트 |
| 레거시 키 신규 사용 | 2026년 제거 예정 | 새 키 시스템 사용 |
| SQL 인젝션 가능한 쿼리 | 보안 취약점 | Supabase 클라이언트 사용 |
| 하드코딩된 환경 변수 | 키 유출 위험 | .env 파일 + .gitignore |

## 연동

| 스킬/에이전트 | 연동 시점 |
|---------------|----------|
| `database-specialist` | 복잡한 쿼리 최적화 |
| `backend-dev` | API 개발 통합 |
| `security-auditor` | RLS 정책 검토 |
| `frontend-dev` | 클라이언트 통합 |

## 트러블슈팅

### 로컬 환경 시작 실패

```bash
# Docker 실행 확인
docker ps

# Supabase 재시작
supabase stop && supabase start
```

### RLS 정책 오류

```sql
-- 현재 정책 확인
SELECT * FROM pg_policies WHERE tablename = 'your_table';

-- 정책 삭제 후 재생성
DROP POLICY IF EXISTS "policy_name" ON public.your_table;
```

### 타입 생성 실패

```bash
# 로컬 DB 스키마 확인
supabase db diff

# 마이그레이션 상태 확인
supabase migration list
```

---

## 2025 신기능 (December Update)

### PostgREST v14

- JWT 캐싱으로 처리량 ~20% 향상
- 스키마 캐시 로딩 시간: 7분 → 2초

### Supabase ETL

외부 데이터 웨어하우스로 지속적 데이터 복제:

```bash
# ETL 파이프라인 설정
supabase etl create --destination bigquery
```

### Vector & Analytics Buckets (Alpha)

임베딩 및 분석 워크로드용 특화 스토리지:

```sql
-- Vector 버킷에서 유사도 검색
SELECT * FROM match_documents(
  query_embedding := embedding,
  match_threshold := 0.8,
  match_count := 10
);
```

### Remote MCP Server

AI 에이전트용 OAuth 인증 플로우:

```bash
# MCP 서버 연결
supabase mcp connect --project-ref <ref>
```

### Edge Functions (Deno 2.1)

- Node.js 18 지원 종료 (2025년 10월)
- Deno 2.1이 모든 리전 기본값

```typescript
// Deno 2.1 기본 import
import { serve } from "https://deno.land/std@0.220.0/http/server.ts"
```

### Sign in with [Your App]

자체 앱을 OAuth 제공자로 등록:

```typescript
// 다른 앱에서 내 앱으로 로그인
const { data } = await supabase.auth.signInWithOAuth({
  provider: 'your-app-name'
})
```

---

## 참조 문서

- [Supabase Changelog](https://supabase.com/changelog)
- [API Keys Migration](https://github.com/orgs/supabase/discussions/29260)
- [RLS Best Practices](https://supabase.com/docs/guides/troubleshooting/rls-performance-and-best-practices-Z5Jjwv)

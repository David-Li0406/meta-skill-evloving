# Semicolon Supabase Conventions

> Semicolon 팀 공통 Supabase 컨벤션

## 1. 테이블 네이밍

### 마이크로서비스 프로젝트

```
{서비스코드}_{도메인}
```

| 서비스 | 코드 | 예시 |
|--------|------|------|
| Schedule | `sc` | `sc_schedules`, `sc_reservations` |
| Payment | `pm` | `pm_transactions`, `pm_refunds` |
| Community | `cm` | `cm_posts`, `cm_comments` |
| User | `us` | `us_profiles`, `us_preferences` |

### 커뮤니티/일반 앱

도메인명만 사용 (서비스 코드 생략):

```sql
profiles
posts
debates
comments
votes
```

### 공통 규칙

- **snake_case** 사용 (kebab-case, camelCase 금지)
- **복수형** 사용 (`user` X → `users` O)
- **예약어** 회피 (`user`, `order`, `group` 등은 접미사 추가)

---

## 2. RLS 정책 네이밍

### 형식

```
"{Table} {action} policy for {role}"
```

### 예시

```sql
-- SELECT 정책
CREATE POLICY "Users can view own purchases" ON purchases
    FOR SELECT USING (auth.uid() = user_id);

-- INSERT 정책
CREATE POLICY "Users can create own posts" ON posts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- UPDATE 정책
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- DELETE 정책
CREATE POLICY "Admins can delete any post" ON posts
    FOR DELETE USING (auth.jwt() ->> 'role' = 'admin');

-- 전체 접근 (public)
CREATE POLICY "Public can view published posts" ON posts
    FOR SELECT USING (status = 'published');
```

### 복합 조건

```sql
CREATE POLICY "Users can view own or public debates" ON debates
    FOR SELECT USING (
        auth.uid() = creator_id
        OR visibility = 'public'
    );
```

---

## 3. 마이그레이션 파일 네이밍

### 형식

```
YYYYMMDD_description.sql
```

### 예시

```
20251215_create_purchases_table.sql
20251215_add_purchase_item_function.sql
20251216_alter_profiles_add_avatar.sql
20251216_create_idx_purchases_user_id.sql
```

### 설명 규칙

| 작업 | 접두사 | 예시 |
|------|--------|------|
| 테이블 생성 | `create_` | `create_purchases_table` |
| 컬럼 추가 | `add_` | `add_profiles_avatar` |
| 컬럼 수정 | `alter_` | `alter_profiles_add_avatar` |
| 인덱스 생성 | `create_idx_` | `create_idx_purchases_user_id` |
| 함수 생성 | `add_` | `add_purchase_item_function` |
| RLS 정책 | `add_rls_` | `add_rls_purchases_select` |
| 삭제 | `drop_` | `drop_legacy_users_table` |

---

## 4. 인덱스 네이밍

### 형식

```sql
idx_{table}_{column}
idx_{table}_{column1}_{column2}  -- 복합 인덱스
```

### 예시

```sql
-- 단일 컬럼 인덱스
CREATE INDEX idx_purchases_user_id ON purchases(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);

-- 복합 인덱스
CREATE INDEX idx_purchases_user_id_created_at ON purchases(user_id, created_at);

-- 유니크 인덱스
CREATE UNIQUE INDEX idx_profiles_email ON profiles(email);

-- 부분 인덱스
CREATE INDEX idx_posts_published ON posts(created_at) WHERE status = 'published';
```

---

## 5. Function 네이밍

### 형식

```
동사_목적어 (snake_case)
```

### 예시

```sql
-- CRUD 관련
CREATE FUNCTION purchase_item(p_user_id uuid, p_item_id uuid) ...
CREATE FUNCTION get_user_points(p_user_id uuid) ...
CREATE FUNCTION update_profile_avatar(p_user_id uuid, p_avatar_url text) ...
CREATE FUNCTION delete_expired_sessions() ...

-- 계산/조회
CREATE FUNCTION calculate_total_price(p_items jsonb) ...
CREATE FUNCTION count_user_posts(p_user_id uuid) ...
CREATE FUNCTION check_user_permission(p_user_id uuid, p_resource text) ...

-- 트리거용
CREATE FUNCTION handle_new_user() ...
CREATE FUNCTION on_auth_user_created() ...
```

### 파라미터 네이밍

- 접두사 `p_` 사용 (parameter)
- snake_case 유지

```sql
CREATE FUNCTION purchase_item(
    p_user_id uuid,
    p_item_id uuid,
    p_quantity integer DEFAULT 1
) RETURNS jsonb AS $$
...
$$ LANGUAGE plpgsql;
```

---

## 6. Edge Functions 구조

### 디렉토리 구조

```
supabase/functions/
├── _shared/                    # 공유 유틸리티
│   ├── cors.ts
│   ├── supabase-client.ts
│   └── types.ts
├── {function-name}/
│   └── index.ts
├── purchase-item/
│   └── index.ts
├── send-notification/
│   └── index.ts
└── webhook-handler/
    └── index.ts
```

### 함수명 규칙

- **kebab-case** 사용 (디렉토리명)
- 동사-목적어 형식

```
purchase-item
send-notification
process-payment
verify-webhook
```

### 기본 구조

```typescript
// supabase/functions/purchase-item/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { corsHeaders } from "../_shared/cors.ts"
import { createClient } from "../_shared/supabase-client.ts"

serve(async (req) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { user_id, item_id } = await req.json()

    const supabase = createClient(req)

    // 비즈니스 로직
    const { data, error } = await supabase
      .rpc('purchase_item', { p_user_id: user_id, p_item_id: item_id })

    if (error) throw error

    return new Response(
      JSON.stringify({ success: true, data }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    )
  }
})
```

---

## 7. Realtime 채널 규칙

### 형식

```typescript
// 도메인 전체 구독
supabase.channel('{domain}:realtime')

// 특정 리소스 구독
supabase.channel('{domain}:{resource-id}')

// 특정 액션 구독
supabase.channel('{domain}:{action}')
```

### 예시

```typescript
// 토론 실시간 업데이트 구독
const debatesChannel = supabase.channel('debates:realtime')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'debates' },
    (payload) => handleDebateChange(payload)
  )
  .subscribe()

// 특정 토론의 투표 구독
const votesChannel = supabase.channel('votes:debate-123')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'votes', filter: 'debate_id=eq.123' },
    (payload) => handleNewVote(payload)
  )
  .subscribe()

// 사용자별 알림 구독
const notificationsChannel = supabase.channel(`notifications:user-${userId}`)
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'notifications', filter: `user_id=eq.${userId}` },
    (payload) => handleNotification(payload)
  )
  .subscribe()
```

### Broadcast 채널

```typescript
// 실시간 커서 위치 공유
const cursorChannel = supabase.channel('room:cursor-tracking')
  .on('broadcast', { event: 'cursor' }, (payload) => {
    updateCursor(payload.user_id, payload.x, payload.y)
  })
  .subscribe()

// 커서 위치 전송
cursorChannel.send({
  type: 'broadcast',
  event: 'cursor',
  payload: { user_id: userId, x: mouseX, y: mouseY }
})
```

---

## 8. 환경 변수 네이밍

### 형식

```
SUPABASE_{SCOPE}_{NAME}
```

### 예시

```bash
# 필수 변수
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbG...
SUPABASE_SERVICE_ROLE_KEY=eyJhbG...

# 프로젝트별 추가 변수
SUPABASE_DB_URL=postgresql://...
SUPABASE_STORAGE_BUCKET=avatars
```

---

## Quick Reference

| 항목 | 형식 | 예시 |
|------|------|------|
| 테이블 | `{서비스코드}_{도메인}` | `sc_schedules` |
| RLS 정책 | `"{Table} {action} for {role}"` | `"Users can view own..."` |
| 마이그레이션 | `YYYYMMDD_description.sql` | `20251215_create_...` |
| 인덱스 | `idx_{table}_{column}` | `idx_purchases_user_id` |
| Function | `동사_목적어` | `purchase_item` |
| Edge Function | `동사-목적어/` | `purchase-item/` |
| Realtime | `{domain}:{id/action}` | `debates:realtime` |

---

## References

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Naming Conventions](https://www.postgresql.org/docs/current/sql-syntax-lexical.html)
- [Semicolon Microservice Conventions](../../docs/conventions/microservice-conventions.md)

# Edge Functions Guide

> Semicolon 팀 Supabase Edge Functions 가이드

## 디렉토리 구조

```
supabase/functions/
├── _shared/                    # 공유 유틸리티
│   ├── cors.ts                 # CORS 헤더
│   ├── supabase-client.ts      # Supabase 클라이언트 생성
│   ├── types.ts                # 공통 타입 정의
│   └── utils.ts                # 유틸리티 함수
├── purchase-item/
│   └── index.ts
├── send-notification/
│   └── index.ts
└── webhook-handler/
    └── index.ts
```

---

## 공유 유틸리티

### cors.ts

```typescript
// supabase/functions/_shared/cors.ts

export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
  'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE',
}
```

### supabase-client.ts

```typescript
// supabase/functions/_shared/supabase-client.ts

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

export function createSupabaseClient(req: Request) {
  const authHeader = req.headers.get('Authorization')

  return createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    {
      global: {
        headers: { Authorization: authHeader ?? '' },
      },
    }
  )
}

// Service Role 클라이언트 (RLS 우회)
export function createSupabaseAdmin() {
  return createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '',
    {
      auth: {
        autoRefreshToken: false,
        persistSession: false,
      },
    }
  )
}
```

### types.ts

```typescript
// supabase/functions/_shared/types.ts

export interface ApiResponse<T = unknown> {
  success: boolean
  data?: T
  error?: string
}

export interface PurchaseRequest {
  user_id: string
  item_id: string
  quantity?: number
}

export interface NotificationRequest {
  user_id: string
  title: string
  body: string
  data?: Record<string, unknown>
}
```

---

## 함수 템플릿

### 기본 템플릿

```typescript
// supabase/functions/{function-name}/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { corsHeaders } from '../_shared/cors.ts'
import { createSupabaseClient } from '../_shared/supabase-client.ts'
import type { ApiResponse } from '../_shared/types.ts'

serve(async (req: Request): Promise<Response> => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    // 요청 파싱
    const body = await req.json()

    // Supabase 클라이언트 생성
    const supabase = createSupabaseClient(req)

    // 비즈니스 로직
    // ...

    // 성공 응답
    const response: ApiResponse = {
      success: true,
      data: { /* result */ },
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    // 에러 응답
    const response: ApiResponse = {
      success: false,
      error: error.message,
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
```

### 구매 처리 예시

```typescript
// supabase/functions/purchase-item/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { corsHeaders } from '../_shared/cors.ts'
import { createSupabaseClient } from '../_shared/supabase-client.ts'
import type { ApiResponse, PurchaseRequest } from '../_shared/types.ts'

interface PurchaseResult {
  purchase_id: string
  amount: number
}

serve(async (req: Request): Promise<Response> => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { user_id, item_id, quantity = 1 }: PurchaseRequest = await req.json()

    // 입력 검증
    if (!user_id || !item_id) {
      throw new Error('user_id and item_id are required')
    }

    if (quantity < 1) {
      throw new Error('quantity must be positive')
    }

    const supabase = createSupabaseClient(req)

    // DB 함수 호출
    const { data, error } = await supabase.rpc('purchase_item', {
      p_user_id: user_id,
      p_item_id: item_id,
      p_quantity: quantity,
    })

    if (error) throw error

    if (!data.success) {
      throw new Error(data.error)
    }

    const response: ApiResponse<PurchaseResult> = {
      success: true,
      data: {
        purchase_id: data.purchase_id,
        amount: data.amount,
      },
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    const response: ApiResponse = {
      success: false,
      error: error.message,
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
```

### 알림 발송 예시

```typescript
// supabase/functions/send-notification/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { corsHeaders } from '../_shared/cors.ts'
import { createSupabaseAdmin } from '../_shared/supabase-client.ts'
import type { ApiResponse, NotificationRequest } from '../_shared/types.ts'

serve(async (req: Request): Promise<Response> => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const { user_id, title, body, data }: NotificationRequest = await req.json()

    if (!user_id || !title || !body) {
      throw new Error('user_id, title, and body are required')
    }

    // Service Role로 사용자 FCM 토큰 조회 (RLS 우회)
    const supabaseAdmin = createSupabaseAdmin()

    const { data: profile, error: profileError } = await supabaseAdmin
      .from('profiles')
      .select('fcm_token')
      .eq('id', user_id)
      .single()

    if (profileError) throw profileError

    if (!profile.fcm_token) {
      throw new Error('User has no FCM token')
    }

    // FCM 발송 (예시)
    const fcmResponse = await fetch('https://fcm.googleapis.com/fcm/send', {
      method: 'POST',
      headers: {
        'Authorization': `key=${Deno.env.get('FCM_SERVER_KEY')}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        to: profile.fcm_token,
        notification: { title, body },
        data,
      }),
    })

    if (!fcmResponse.ok) {
      throw new Error('FCM send failed')
    }

    // 알림 기록 저장
    await supabaseAdmin.from('notifications').insert({
      user_id,
      title,
      body,
      data,
      sent_at: new Date().toISOString(),
    })

    const response: ApiResponse = {
      success: true,
      data: { message: 'Notification sent' },
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    const response: ApiResponse = {
      success: false,
      error: error.message,
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
```

### Webhook 핸들러 예시

```typescript
// supabase/functions/webhook-handler/index.ts

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { corsHeaders } from '../_shared/cors.ts'
import { createSupabaseAdmin } from '../_shared/supabase-client.ts'
import type { ApiResponse } from '../_shared/types.ts'

// Webhook 시크릿 검증
function verifyWebhookSignature(req: Request, body: string): boolean {
  const signature = req.headers.get('x-webhook-signature')
  const secret = Deno.env.get('WEBHOOK_SECRET')

  if (!signature || !secret) return false

  // HMAC 검증 로직 (예시)
  // const expectedSignature = hmac(secret, body)
  // return signature === expectedSignature

  return true // 실제로는 적절한 검증 필요
}

serve(async (req: Request): Promise<Response> => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const bodyText = await req.text()

    // 시그니처 검증
    if (!verifyWebhookSignature(req, bodyText)) {
      throw new Error('Invalid webhook signature')
    }

    const payload = JSON.parse(bodyText)
    const { event, data } = payload

    const supabaseAdmin = createSupabaseAdmin()

    // 이벤트별 처리
    switch (event) {
      case 'payment.completed':
        await supabaseAdmin
          .from('purchases')
          .update({ status: 'completed' })
          .eq('external_id', data.payment_id)
        break

      case 'payment.failed':
        await supabaseAdmin
          .from('purchases')
          .update({ status: 'failed' })
          .eq('external_id', data.payment_id)
        break

      default:
        console.log(`Unhandled event: ${event}`)
    }

    const response: ApiResponse = {
      success: true,
      data: { received: true },
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    })
  } catch (error) {
    const response: ApiResponse = {
      success: false,
      error: error.message,
    }

    return new Response(JSON.stringify(response), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 400,
    })
  }
})
```

---

## 로컬 개발

### 함수 생성

```bash
# 새 함수 생성
supabase functions new purchase-item
```

### 로컬 실행

```bash
# 모든 함수 실행
supabase functions serve

# 특정 함수만 실행
supabase functions serve purchase-item

# 환경 변수 파일 지정
supabase functions serve --env-file .env.local
```

### 로컬 테스트

```bash
# curl로 테스트
curl -i --location --request POST \
  'http://localhost:54321/functions/v1/purchase-item' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1...' \
  --header 'Content-Type: application/json' \
  --data '{"user_id":"xxx","item_id":"yyy"}'
```

---

## 배포

### 함수 배포

```bash
# 모든 함수 배포
supabase functions deploy

# 특정 함수만 배포
supabase functions deploy purchase-item

# 환경 변수 없이 배포 (secrets는 Dashboard에서 설정)
supabase functions deploy purchase-item --no-verify-jwt
```

### Secrets 설정

```bash
# Secret 설정
supabase secrets set FCM_SERVER_KEY=xxx
supabase secrets set WEBHOOK_SECRET=yyy

# Secret 목록 확인
supabase secrets list
```

---

## 주의사항

1. **CORS**: 브라우저에서 호출 시 CORS 헤더 필수
2. **인증**: `Authorization` 헤더로 JWT 전달
3. **Service Role**: RLS 우회 필요 시에만 사용
4. **Cold Start**: 첫 호출 시 지연 발생 가능
5. **타임아웃**: 기본 60초, 필요 시 조정

---

## References

- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Deno Deploy](https://deno.com/deploy)

# Chat E2E Test Script Reference

> E2E 테스트를 위한 상세 스크립트 및 검증 방법

## Complete E2E Test Flow

```bash
#!/bin/bash
# Chat E2E Test Script

# Configuration
BASE_URL="https://api.dev.growbin.app"
TOKEN="${1:-$JWT_TOKEN}"  # JWT Token as first argument or env var

if [ -z "$TOKEN" ]; then
    echo "Usage: $0 <JWT_TOKEN>"
    exit 1
fi

echo "=== Step 1: Create Chat Session ==="
CHAT_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"title": "E2E Test"}')

CHAT_ID=$(echo $CHAT_RESPONSE | jq -r '.id')
echo "Chat ID: $CHAT_ID"

if [ "$CHAT_ID" == "null" ] || [ -z "$CHAT_ID" ]; then
    echo "Failed to create chat: $CHAT_RESPONSE"
    exit 1
fi

echo ""
echo "=== Step 2: Send Message ==="
MSG_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "플라스틱 페트병은 어떻게 버려?"}')

JOB_ID=$(echo $MSG_RESPONSE | jq -r '.job_id')
STREAM_URL=$(echo $MSG_RESPONSE | jq -r '.stream_url')
echo "Job ID: $JOB_ID"
echo "Stream URL: $STREAM_URL"

if [ "$JOB_ID" == "null" ] || [ -z "$JOB_ID" ]; then
    echo "Failed to send message: $MSG_RESPONSE"
    exit 1
fi

echo ""
echo "=== Step 3: Subscribe to SSE ==="
# SSE 경로: /api/v1/chat/{job_id}/events (NOT /api/v1/sse/...)
# chat-vs VirtualService가 regex로 매칭하여 sse-gateway로 라우팅
echo "Subscribing to: $BASE_URL/api/v1/chat/${JOB_ID}/events"
echo "Press Ctrl+C to stop..."
echo ""

curl -sN --max-time 60 \
  "$BASE_URL/api/v1/chat/${JOB_ID}/events" \
  -H "Accept: text/event-stream" \
  -H "Cookie: s_access=$TOKEN"
```

## Test Cases by Intent

### WASTE Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "플라스틱 분리배출 방법 알려줘"}'
```

**Expected Nodes**: `waste_rag`, `weather` (enrichment)

### CHARACTER Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "플라스틱 버리면 어떤 캐릭터 얻어?"}'
```

**Expected Nodes**: `character`

### LOCATION Intent (with location)

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{
    "message": "근처 제로웨이스트샵 알려줘",
    "user_location": {
      "latitude": 37.5665,
      "longitude": 126.9780
    }
  }'
```

**Expected Nodes**: `location`

### BULK_WASTE Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "소파 버리려면 어떻게 해?"}'
```

**Expected Nodes**: `bulk_waste`, `weather` (enrichment)

### COLLECTION_POINT Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{
    "message": "근처 의류수거함 어디야?",
    "user_location": {
      "latitude": 37.5665,
      "longitude": 126.9780
    }
  }'
```

**Expected Nodes**: `collection_point`

### WEB_SEARCH Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "최신 분리배출 정책 알려줘"}'
```

**Expected Nodes**: `web_search`

### IMAGE_GENERATION Intent

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message": "페트병 버리는 법 이미지로 만들어줘"}'
```

**Expected Nodes**: `image_generation`

### MULTI_INTENT Test

```bash
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{
    "message": "종이 버리는 법이랑 수거함도 알려줘",
    "user_location": {
      "latitude": 37.5665,
      "longitude": 126.9780
    }
  }'
```

**Expected Nodes**: `waste_rag`, `collection_point`, `weather` (3개 병렬 실행)

## Expected SSE Event Sequence

```
event: queued
data: {"stage":"queued","status":"pending","progress":0}

event: intent
data: {"stage":"intent","status":"started","progress":5}

event: intent
data: {"stage":"intent","status":"completed","progress":15,"result":{"intent":"waste"}}

event: waste_rag
data: {"stage":"waste_rag","status":"started","progress":20}

event: weather
data: {"stage":"weather","status":"started","progress":25}

event: waste_rag
data: {"stage":"waste_rag","status":"completed","progress":40}

event: weather
data: {"stage":"weather","status":"completed","progress":45}

event: aggregator
data: {"stage":"aggregator","status":"completed","progress":65}

event: token
data: {"stage":"token","content":"플","seq":1001}

event: token
data: {"stage":"token","content":"라","seq":1002}

... (더 많은 토큰)

event: done
data: {"stage":"done","status":"success","progress":100,"result":{...}}
```

## Verification Checklist

- [ ] Chat 생성 성공 (HTTP 201)
- [ ] 메시지 전송 성공 (HTTP 200, job_id 반환)
- [ ] SSE 연결 성공 (text/event-stream)
- [ ] Intent 분류 이벤트 수신
- [ ] 서브에이전트 시작/완료 이벤트 수신
- [ ] Token 스트리밍 이벤트 수신 (seq 연속 증가)
- [ ] Done 이벤트 수신 (progress: 100)
- [ ] 오류 없음

## Canary Testing

```bash
# x-canary 헤더로 canary 버전 테스트
curl -X POST "$BASE_URL/api/v1/chat/${CHAT_ID}/messages" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -H "x-canary: true" \
  -d '{"message": "테스트 메시지"}'
```

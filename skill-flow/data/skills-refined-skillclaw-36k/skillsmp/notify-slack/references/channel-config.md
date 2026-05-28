# Channel Configuration

> Slack 알림 대상 채널 설정 및 권한 관리

## 대상 채널

| 채널 | 용도 | 우선순위 |
|------|------|----------|
| `#_협업` | 기본 알림 채널 | Primary |
| `#_일반` | 대체 채널 | Fallback |

> **🔴 NON-NEGOTIABLE**: 채널 ID를 하드코딩하지 마세요. 항상 API로 동적 조회합니다.

## 채널 ID 동적 조회

### 채널 이름으로 ID 조회 (필수)

```bash
# 토큰은 MCP에서 조회
TOKEN="$(MCP에서 조회한 토큰)"
CHANNEL_NAME="_협업"

# 채널 ID 조회
CHANNEL_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=200" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    if ch['name'] == '$CHANNEL_NAME':
        print(ch['id'])
        break
")

echo "Channel: $CHANNEL_NAME -> ID: $CHANNEL_ID"
```

### 채널 검색 (이름 일부 매칭)

```bash
TOKEN="..."
KEYWORD="협업"

curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=200" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for ch in data.get('channels', []):
    if '$KEYWORD' in ch['name']:
        print(f\"{ch['name']} -> {ch['id']}\")
"
```

## 앱 권한 설정

### 필수 Bot Token Scopes

| Scope | 용도 |
|-------|------|
| `chat:write` | 메시지 전송 |
| `chat:write.public` | 공개 채널 메시지 전송 |
| `users:read` | 사용자 ID 조회 (멘션용) |
| `channels:read` | 채널 목록 조회 |

### 앱을 채널에 추가

비공개 채널에 메시지를 보내려면:

1. Slack에서 해당 채널 열기
2. 채널 이름 클릭 → 설정
3. "앱 추가" 클릭
4. "Semicolon Notifier" 검색 후 추가

## 알림 유형별 채널

| 알림 유형 | 채널 이름 | 비고 |
|----------|----------|------|
| 릴리스 알림 | `_협업` | SEMO 패키지 업데이트 |
| 이슈 알림 | `_협업` | Draft Task, Issue 생성 |
| 커스텀 메시지 | 지정된 채널 | /SEMO:slack 커맨드 |

## 권한 오류 대응

### `not_in_channel` 오류

```json
{"ok": false, "error": "not_in_channel"}
```
**해결**: 앱을 채널에 추가 (`/invite @노티파이어`)

### `channel_not_found` 오류

```json
{"ok": false, "error": "channel_not_found"}
```
**해결**: 채널 이름 확인 후 API로 ID 재조회

### `missing_scope` 오류

```json
{"ok": false, "error": "missing_scope", "needed": "chat:write"}
```
**해결**: 앱 설정에서 OAuth Scopes 추가

## 테스트 명령

> **⚠️ 중요**: 쉘 이스케이프 문제를 방지하기 위해 **heredoc 방식**을 사용하세요.

```bash
# 1. 토큰 획득 (MCP)
TOKEN="..."

# 2. 채널 ID 동적 조회
CHANNEL_NAME="_협업"
CHANNEL_ID=$(curl -s -H "Authorization: Bearer $TOKEN" \
  "https://slack.com/api/conversations.list?types=public_channel&limit=200" | \
  python3 -c "import json,sys;[print(c['id']) for c in json.load(sys.stdin).get('channels',[]) if c['name']=='$CHANNEL_NAME']" | head -1)

# 3. 테스트 메시지 전송
curl -s -X POST 'https://slack.com/api/chat.postMessage' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d @- << EOF
{
  "channel": "$CHANNEL_ID",
  "text": "SEMO notify-slack 테스트 메시지"
}
EOF
```

## 참고

- Slack API 문서: https://api.slack.com/methods/chat.postMessage
- Block Kit Builder: https://app.slack.com/block-kit-builder

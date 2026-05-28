---
name: test-ui
description: Use this skill when testing UI interactions in a Remote App, including permission requests and selection responses.
---

# Skill body

## Purpose

This skill is designed to test various UI interactions in a Remote App, including permission requests and selection responses. It simulates different states and verifies the correct rendering and handling of user responses.

## Workflow

```text
스킬 호출
    ↓
1. remote_requests 테이블에 테스트 요청 저장
   - type: "permission" 또는 "selection"
   - options: ["Option A", "Option B", "Option C"] (선택형일 경우)
   - status: "pending"
    ↓
2. Remote App에서 UI 렌더링 대기
    ↓
3. 사용자 응답 또는 타임아웃
    ↓
4. 결과 출력
```

## Execution

### 테스트 요청 생성

```bash
mcp__semo-integrations__remote_request(
  session_id: "{current_session_id}",
  type: "{type}",  # "permission" 또는 "selection"
  message: "[테스트] 다음 중 하나를 선택하세요:" (선택형일 경우),
  options: ["Option A - 첫 번째 선택지", "Option B - 두 번째 선택지", "Option C - 세 번째 선택지"] (선택형일 경우)
)
```

### 응답 대기

```bash
# 60초 타임아웃으로 응답 대기 (permission) 또는 30초 (selection)
mcp__semo-integrations__remote_await(
  request_id: "{request_id}",
  timeout: {timeout}  # 60 또는 30
)
```

## Output

### 성공 (승인 또는 선택 완료)

```markdown
[SEMO] Skill: test-ui 호출

## 요청 생성됨

**Request ID**: {request_id}
**Type**: {type}
{options_output}  # 선택형일 경우 옵션 출력

Remote App에서 응답을 기다리는 중...

---

✅ **응답 완료**

**응답**: {response}  # "approve" 또는 선택된 옵션
**응답 시간**: {response_time}초
```

### 타임아웃

```markdown
[SEMO] Skill: test-ui 호출

## 요청 생성됨

**Request ID**: {request_id}
**Type**: {type}

Remote App에서 응답을 기다리는 중...

---

⏱️ **타임아웃**

{timeout}초 내에 응답이 없었습니다.
- Remote App이 열려 있는지 확인
- 네트워크 연결 상태 확인
```

## Error Handling

### DB 연결 실패

```markdown
⚠️ Remote DB 연결 실패

SEMO_DB_PASSWORD 환경 변수를 확인하세요.
```

### 세션 ID 없음

```markdown
⚠️ 세션 ID를 찾을 수 없습니다.

semo-remote-client가 실행 중인지 확인하세요.
```
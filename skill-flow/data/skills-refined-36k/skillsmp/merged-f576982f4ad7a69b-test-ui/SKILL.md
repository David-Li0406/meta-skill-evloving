---
name: test-ui
description: Use this skill when testing UI interactions in a Remote App, including permission requests and selection responses.
---

# test-ui Skill

> Remote App의 UI 상호작용을 테스트하기 위한 개발/디버깅 스킬

## Purpose

Remote App에서 UI가 정상 동작하는지 테스트합니다:
- `awaiting_type: permission` 및 `awaiting_type: selection` 상태 시뮬레이션
- 권한 요청 및 선택형 응답 메시지 렌더링 확인
- 사용자 응답 처리 검증

## 트리거

- "권한 요청 테스트"
- "test permission"
- "remote permission 테스트"
- "선택형 테스트"
- "test selection"
- "remote selection 테스트"

## Workflow

```text
스킬 호출
    ↓
1. remote_requests 테이블에 테스트 요청 저장
   - type: "permission" 또는 "selection"
   - (옵션) 선택지: ["Option A", "Option B", "Option C"]
   - status: "pending"
    ↓
2. Remote App에서 UI 렌더링 대기
    ↓
3. 사용자 응답 또는 타임아웃
    ↓
4. 결과 출력
```

## Execution

### 테스트 요청 생성 (권한 요청)

```bash
mcp__semo-integrations__remote_request(
  session_id: "{current_session_id}",
  type: "permission",
  tool: "Bash",
  message: "[테스트] 다음 명령어를 실행해도 될까요?\n\n`echo 'Hello from test-ui'`",
  metadata: {
    command: "echo 'Hello from test-ui'",
    is_test: true
  }
)
```

### 테스트 요청 생성 (선택형)

```bash
mcp__semo-integrations__remote_request(
  session_id: "{current_session_id}",
  type: "selection",
  message: "[테스트] 다음 중 하나를 선택하세요:",
  options: ["Option A - 첫 번째 선택지", "Option B - 두 번째 선택지", "Option C - 세 번째 선택지"]
)
```

### 응답 대기

```bash
# 60초 타임아웃으로 응답 대기 (권한 요청)
mcp__semo-integrations__remote_await(
  request_id: "{request_id}",
  timeout: 60
)

# 30초 타임아웃으로 응답 대기 (선택형)
mcp__semo-integrations__remote_await(
  request_id: "{request_id}",
  timeout: 30
)
```

## Output

### 성공 (권한 요청 승인)

```markdown
[SEMO] Skill: test-ui 호출

## 권한 요청 테스트 생성됨

**Request ID**: def456
**Type**: permission
**Tool**: Bash
**Message**:
> [테스트] 다음 명령어를 실행해도 될까요?
> `echo 'Hello from test-ui'`

Remote App에서 응답을 기다리는 중...

---

✅ **승인됨**

**응답**: approve
**응답 시간**: 3.8초
**메시지**: 사용자가 승인함
```

### 성공 (선택 완료)

```markdown
[SEMO] Skill: test-ui 호출

## 선택형 테스트 요청 생성됨

**Request ID**: abc123
**Type**: selection
**Options**:
1. Option A - 첫 번째 선택지
2. Option B - 두 번째 선택지
3. Option C - 세 번째 선택지

Remote App에서 선택을 기다리는 중...

---

✅ **선택 완료**

**선택된 옵션**: Option B - 두 번째 선택지
**응답 시간**: 5.2초
```

### 타임아웃

```markdown
[SEMO] Skill: test-ui 호출

## 요청 생성됨

**Request ID**: def456 또는 abc123
**Type**: permission 또는 selection

Remote App에서 응답을 기다리는 중...

---

⏱️ **타임아웃**

60초 또는 30초 내에 응답이 없었습니다.
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

## SEMO Message Format

```markdown
[SEMO] Skill: test-ui 호출

[SEMO] Skill: test-ui 완료 - {approve|deny|timeout|result}
```

## References

- [remote-bridge Skill](../remote-bridge/SKILL.md)
- [CLAUDE.md](../../CLAUDE.md) - Remote API 호출 규칙
- [semo-hooks](../../../semo-hooks/) - Hook 시스템
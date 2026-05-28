# Hook 검토 체크리스트

## 설정 파일 위치

| 위치 | 범위 | 파일 |
|------|------|------|
| 프로젝트 | 프로젝트 전체 | `.claude/settings.json` |
| 프로젝트 로컬 | 개인 설정 | `.claude/settings.local.json` |
| 사용자 | 전역 | `~/.claude/settings.json` |

---

## Hook 구조 검증

### 기본 구조
```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<ToolPattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell-command>"
          }
        ]
      }
    ]
  }
}
```

### 체크리스트
```
- [ ] hooks 객체 내에 정의
- [ ] 유효한 이벤트명 사용
- [ ] matcher 패턴 정확
- [ ] command 문자열 유효
```

---

## 이벤트 검증

### 사용 가능한 이벤트

| 이벤트 | 트리거 시점 | 블로킹 | 용도 |
|-------|-----------|--------|------|
| `PreToolUse` | 도구 실행 전 | Yes (exit 2) | 검증, 차단 |
| `PostToolUse` | 도구 완료 후 | No | 포맷팅, 로깅 |
| `Notification` | 알림 전송 시 | No | 커스텀 알림 |
| `Stop` | 응답 완료 시 | No | 후처리 |

### 이벤트 선택 체크리스트
```
- [ ] 목적에 맞는 이벤트 선택
- [ ] 블로킹 필요 시 PreToolUse 사용
- [ ] 후처리는 PostToolUse 사용
```

---

## Matcher 패턴 검증

### 유효한 패턴

| 패턴 | 의미 |
|------|------|
| `*` | 모든 도구 |
| `Bash` | Bash 도구만 |
| `Edit\|Write` | Edit 또는 Write |
| `Read` | Read 도구만 |

### 체크리스트
```
- [ ] 유효한 도구명 사용
- [ ] OR 연산자는 파이프(\|) 사용
- [ ] 불필요하게 넓은 매칭 피하기
```

---

## Exit Code 검증

### PreToolUse Exit Codes

| Code | 의미 | 동작 |
|------|------|------|
| `0` | 허용 | 도구 실행 진행 |
| `2` | 차단 | stdout이 Claude에게 피드백 |

### PostToolUse/기타 Exit Codes

| Code | 의미 |
|------|------|
| `0` | 정상 완료 (Non-blocking) |

### 체크리스트
```
- [ ] Non-blocking 훅은 항상 exit 0
- [ ] PreToolUse 차단 시에만 exit 2
- [ ] 에러 발생해도 exit 0 유지 (blocking 방지)
```

---

## 스크립트 검증 (Python)

### 필수 구조
```python
#!/usr/bin/env python3
import json
import sys

# stdin에서 데이터 읽기
data = json.load(sys.stdin)
file_path = data.get('tool_input', {}).get('file_path', '')

# 조건 확인 및 처리
# ...

# Non-blocking 종료
sys.exit(0)
```

### 체크리스트
```
- [ ] shebang 포함 (#!/usr/bin/env python3)
- [ ] json, sys import
- [ ] stdin에서 JSON 읽기
- [ ] 예외 처리 포함
- [ ] 항상 sys.exit(0)으로 종료
- [ ] 타임아웃 고려 (긴 작업 피하기)
```

---

## 입력 데이터 스키마

### PreToolUse 입력
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file",
    "old_string": "...",
    "new_string": "..."
  }
}
```

### PostToolUse 입력
```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file"
  },
  "tool_response": "File edited successfully"
}
```

### 도구별 tool_input 필드

| 도구 | 필드 |
|------|------|
| Bash | `command`, `description` |
| Edit | `file_path`, `old_string`, `new_string` |
| Write | `file_path`, `content` |
| Read | `file_path` |
| Glob | `pattern`, `path` |
| Grep | `pattern`, `path` |

---

## 베스트 프랙티스 검증

```
- [ ] Non-blocking 유지 (exit 0)
- [ ] 타임아웃 설정 (긴 작업 피하기)
- [ ] 출력 제한 (과도한 로그 방지)
- [ ] 조건 확인 정확 (불필요한 실행 방지)
- [ ] 에러 처리 적절
- [ ] 스크립트 실행 권한 설정 (chmod +x)
```

---

## 일반적인 문제

| 문제 | 원인 | 해결 |
|------|------|------|
| 훅 실행 안됨 | matcher 패턴 오류 | `Edit\|Write` 형식 확인 |
| 작업 중단됨 | exit code가 0이 아님 | 항상 exit 0 반환 |
| 훅이 너무 느림 | 무거운 작업 수행 | 비동기 처리 또는 경량화 |
| stdin 읽기 실패 | JSON 파싱 오류 | try-except로 감싸기 |

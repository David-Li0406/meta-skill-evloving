# /auto 로그 스키마

## 개요

`/auto` 커맨드의 로그는 JSON Lines 형식으로 저장됩니다.

## 저장 위치

```
.claude/auto-logs/
├── active/                          # 진행 중인 세션
│   └── session_YYYYMMDD_HHMMSS/
│       ├── state.json               # 세션 상태
│       ├── log_001.json             # 로그 청크 1
│       ├── log_002.json             # 로그 청크 2 (50KB 초과 시)
│       └── checkpoint.json          # 재개용 체크포인트
└── archive/                         # 완료된 세션
    └── session_YYYYMMDD_HHMMSS/
        ├── state.json
        ├── log_*.json
        └── summary.json             # 세션 요약
```

## 로그 엔트리 스키마

### 기본 구조

```json
{
  "timestamp": "2025-12-30T10:30:00.000Z",
  "sequence": 1,
  "event_type": "action|decision|error|milestone|checkpoint",
  "phase": "init|analysis|implementation|testing|complete",
  "data": {},
  "context_usage": 45,
  "todo_state": []
}
```

### 필드 설명

| 필드 | 타입 | 설명 |
|------|------|------|
| `timestamp` | ISO 8601 | 이벤트 발생 시각 |
| `sequence` | integer | 세션 내 순서 번호 |
| `event_type` | string | 이벤트 유형 |
| `phase` | string | 현재 작업 단계 |
| `data` | object | 이벤트별 상세 데이터 |
| `context_usage` | integer | Context 사용률 (%) |
| `todo_state` | array | 현재 Todo 상태 (선택) |

### event_type 값

| 값 | 설명 |
|----|------|
| `action` | 파일 읽기/쓰기, 커맨드 실행 등 |
| `decision` | 의사결정 기록 |
| `error` | 에러 발생 |
| `milestone` | 주요 단계 완료 |
| `checkpoint` | 체크포인트 저장 |

### phase 값

| 값 | 설명 |
|----|------|
| `init` | 세션 초기화 |
| `analysis` | 상태 분석 |
| `implementation` | 구현 진행 |
| `testing` | 테스트 실행 |
| `complete` | 완료 |
| `checkpoint` | 체크포인트 |
| `error` | 에러 상태 |

## 이벤트별 data 스키마

### action

```json
{
  "action": "file_read|file_write|command|tool_use",
  "target": "path/to/file",
  "result": "success|fail",
  "details": {
    "lines_changed": 10,
    "error_message": "..."
  }
}
```

### decision

```json
{
  "decision": "JWT 토큰 방식 선택",
  "reason": "보안 강화 및 확장성",
  "alternatives": ["Session", "Basic Auth"]
}
```

### error

```json
{
  "error": "FileNotFoundError",
  "traceback": "...",
  "recoverable": true
}
```

### milestone

```json
{
  "milestone": "테스트 통과",
  "progress": {
    "completed": 3,
    "total": 5
  }
}
```

### checkpoint

```json
{
  "resume_point": {
    "task_id": 3,
    "task_content": "핸들러 구현",
    "context_hint": "src/auth/handler.py"
  },
  "key_decisions": ["JWT 선택", "24시간 만료"]
}
```

## 상태 파일 스키마

### state.json

```json
{
  "session_id": "session_20251230_103000",
  "status": "running|paused|completed|failed",
  "started_at": "2025-12-30T10:30:00Z",
  "last_activity": "2025-12-30T11:45:00Z",
  "original_request": "API 인증 기능 구현",
  "current_phase": "implementation",
  "context_stats": {
    "peak_usage": 85,
    "current_usage": 72,
    "clear_count": 1
  },
  "progress": {
    "total_tasks": 7,
    "completed": 3,
    "in_progress": 1,
    "pending": 3
  },
  "files_touched": [
    "src/auth/handler.py",
    "tests/test_auth.py"
  ],
  "key_decisions": [
    "JWT 토큰 방식 선택",
    "24시간 만료 설정"
  ],
  "resume_point": {
    "task_id": 4,
    "task_content": "JWT 토큰 발급 로직 구현",
    "context_hint": "handler.py의 generate_token 함수"
  }
}
```

### checkpoint.json

```json
{
  "created_at": "2025-12-30T11:45:00Z",
  "session_id": "session_20251230_103000",
  "resume_point": {
    "task_id": 4,
    "task_content": "JWT 토큰 발급 로직 구현",
    "context_hint": "handler.py의 generate_token 함수"
  },
  "todo_state": [
    {"id": 1, "content": "요구사항 분석", "status": "completed"},
    {"id": 2, "content": "API 설계", "status": "completed"},
    {"id": 3, "content": "핸들러 구현", "status": "completed"},
    {"id": 4, "content": "JWT 토큰 발급", "status": "in_progress"},
    {"id": 5, "content": "테스트 작성", "status": "pending"}
  ],
  "state_snapshot": {
    "current_phase": "implementation",
    "progress": {
      "total_tasks": 5,
      "completed": 3,
      "in_progress": 1,
      "pending": 1
    },
    "key_decisions": [
      "JWT 토큰 방식 선택",
      "24시간 만료 설정"
    ],
    "files_touched": [
      "src/auth/handler.py"
    ]
  }
}
```

## 청킹 규칙

| 기준 | 값 | 설명 |
|------|-----|------|
| 크기 | 50KB | 파일 크기 초과 시 새 청크 |
| 명명 | `log_{NNN}.json` | 001, 002, ... |

## 예시

### 로그 파일 (log_001.json)

```jsonl
{"timestamp":"2025-12-30T10:30:00Z","sequence":1,"event_type":"milestone","phase":"init","data":{"milestone":"세션 시작"}}
{"timestamp":"2025-12-30T10:30:05Z","sequence":2,"event_type":"action","phase":"analysis","data":{"action":"command","target":"git status","result":"success"},"context_usage":5}
{"timestamp":"2025-12-30T10:30:10Z","sequence":3,"event_type":"decision","phase":"analysis","data":{"decision":"테스트 실패 수정 우선","reason":"CI 통과 필요","alternatives":["이슈 해결","문서화"]},"context_usage":8}
{"timestamp":"2025-12-30T10:31:00Z","sequence":4,"event_type":"action","phase":"implementation","data":{"action":"file_read","target":"src/auth/handler.py","result":"success"},"context_usage":15}
```

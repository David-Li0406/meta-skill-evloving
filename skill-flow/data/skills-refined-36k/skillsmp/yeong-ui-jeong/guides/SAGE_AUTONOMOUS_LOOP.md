# Sage 자율 실행 루프 설계 가이드

> **작성일**: 2026-01-19
> **버전**: 2.0
> **설계자**: Claude (Opus 4.5)

---

## 1. 개요

### 1.1 목표

수동 개입 없이 `/sage <task>` 명령 하나로 14개 역할을 자동 순환하고 완료까지 실행하는 시스템.

### 1.2 핵심 문제

Claude Code의 Stop hook은 응답 완료 **후** 발동되며, `exit 1`은 Non-blocking error로 처리되어 Claude에게 "계속하라"는 신호가 전달되지 않았음.

### 1.3 해결책

```
exit 1 (기존) → exit 0 + JSON (신규)
```

Stop hook이 JSON을 출력하고 `exit 0`을 반환하면, Claude가 해당 메시지를 컨텍스트로 받아 다음 행동을 결정할 수 있음.

---

## 2. 아키텍처

### 2.1 전체 흐름

```
┌─────────────────────────────────────────────────────────────┐
│ 사용자: /sage <task>                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ sage SKILL.md 로드                                          │
│ → sage_state_manager.py init "<task>" --chain FULL         │
│ → 세션 초기화 (14개 역할 정의)                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 역할 루프 시작                                               │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ 1. sage_state_manager.py start <role>               │   │
│   │ 2. Claude가 역할 수행 (예: ideator → 50개 아이디어) │   │
│   │ 3. sage_state_manager.py complete <role>            │   │
│   │    → "NEXT: <다음역할>" 또는 "APPROVE"              │   │
│   └─────────────────────────────────────────────────────┘   │
│                              │                               │
│                              ▼                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Claude 응답 완료 시도                                │   │
│   │                  ↓                                   │   │
│   │ Stop Hook 발동 (stop-hook.sh)                       │   │
│   │                  ↓                                   │   │
│   │ 세션 활성 + 다음 역할 있음?                          │   │
│   │   YES → JSON 출력 + exit 0                          │   │
│   │         {"decision":"block","next_role":"analyst"}  │   │
│   │   NO  → 정상 종료 (exit 0, JSON 없음)               │   │
│   └─────────────────────────────────────────────────────┘   │
│                              │                               │
│                    (JSON 출력 시)                            │
│                              ▼                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │ Claude가 JSON 메시지 수신                            │   │
│   │ → "다음 역할 'analyst'를 즉시 실행하세요"            │   │
│   │ → 역할 루프 계속                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 모든 역할 완료 → exit_signal: true → 정상 종료              │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 상태 파일 구조

```
/tmp/
├── sage_session_{SESSION_ID}.json     # 세션 상태
├── sage_loop_state_{SESSION_ID}.json  # 루프 카운터
├── sage_circuit_breaker_{SESSION_ID}.json  # 안전장치
└── sage_errors_{SESSION_ID}.log       # 디버그 로그 (DEBUG=1)
```

#### 세션 상태 파일 스키마

```json
{
  "session_id": "abc12345",
  "task": "새로운 API 엔드포인트 개발",
  "chain_type": "FULL",
  "chain_roles": [
    "ideator", "analyst", "critic", "censor", "academy",
    "architect", "left-state-councilor", "right-state-councilor",
    "executor", "inspector", "validator", "historian",
    "reflector", "improver"
  ],
  "current_role": "analyst",
  "completed_roles": ["ideator"],
  "role_outputs": {
    "ideator": {"ideas": [...], "count": 50}
  },
  "active": true,
  "exit_signal": false,
  "started_at": "2026-01-19T11:00:00",
  "loop_count": 2
}
```

---

## 3. 컴포넌트 상세

### 3.1 sage_state_manager.py

세션 상태를 관리하는 핵심 스크립트.

#### 명령어

| 명령 | 설명 | 예시 |
|------|------|------|
| `init <task> --chain TYPE` | 세션 초기화 | `init "작업" --chain FULL` |
| `start <role>` | 역할 시작 기록 | `start ideator` |
| `complete <role>` | 역할 완료, 다음 역할 반환 | `complete ideator` → `NEXT: analyst` |
| `next` | 다음 역할 조회 | `next` → `analyst` |
| `progress` | 진행 상황 JSON | `progress` |
| `exit --reason "..."` | 종료 신호 설정 | `exit --reason "완료"` |
| `cleanup` | 세션 정리 | `cleanup` |

#### 체인 타입

| 타입 | 역할 수 | 용도 |
|------|---------|------|
| FULL | 14 | 신규 기능, 복잡한 작업 |
| QUICK | 5 | 버그 수정, 패치 |
| REVIEW | 2 | 코드 검토 |
| DESIGN | 4 | 설계 단계 |

### 3.2 stop-hook.sh (v2)

Stop hook의 핵심 변경.

#### Exit Code 규칙

| Exit Code | stdout | 동작 |
|-----------|--------|------|
| 0 | JSON | Claude에게 메시지 전달, 계속 실행 유도 |
| 0 | 없음 | 정상 종료 |
| 1 | 무시됨 | Non-blocking error (Claude 못 받음) |
| 2 | stderr | Blocking error (Claude가 stderr 수신) |

#### JSON 출력 형식

```json
{
  "decision": "block",
  "reason": "[SAGE FULL] Loop 3/50: 'ideator' → 'analyst' (1/14)",
  "next_role": "analyst",
  "progress": "1/14",
  "instruction": "다음 역할 'analyst'를 즉시 실행하세요. /sage 체인 진행 중입니다."
}
```

### 3.3 role_detector.py

현재/다음 역할 감지.

```bash
# 현재 역할
python3 role_detector.py --current

# 다음 역할
python3 role_detector.py --next

# sage 활성 여부
python3 role_detector.py --active

# 진행 상황 JSON
python3 role_detector.py --progress
```

### 3.4 circuit_breaker_check.py

무한 루프 방지 안전장치.

#### 트립 조건

| 조건 | 기본값 | 환경변수 |
|------|--------|----------|
| 연속 오류 | 3회 | `SAGE_MAX_ERRORS` |
| 역할당 루프 | 5회 | `SAGE_MAX_ROLE_LOOPS` |
| 쿨다운 | 60초 | `SAGE_COOLDOWN` |

### 3.5 completion_detector.py

체인 완료 여부 감지.

```bash
python3 completion_detector.py
# → "true" 또는 "false"
```

완료 조건:
- `exit_signal: true`
- 모든 `chain_roles`가 `completed_roles`에 포함

### 3.6 feedback_checker.py

대기 중인 피드백 확인.

```bash
python3 feedback_checker.py
# → 대기 중인 피드백 수 (0, 1, 2, ...)
```

---

## 4. 종료 조건

| 조건 | 처리 |
|------|------|
| 모든 역할 완료 | `APPROVE` 반환 → 정상 종료 |
| MAX_LOOPS (50) 도달 | 강제 종료 |
| SESSION_TIMEOUT (3600s) 초과 | 강제 종료 |
| Circuit breaker 발동 | 안전 종료 |
| exit_signal: true | 정상 종료 |

---

## 5. 환경변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SAGE_STATE_DIR` | `/tmp` | 상태 파일 디렉토리 |
| `SAGE_PROJECT_ROOT` | `~/Dyarchy-v3` | 프로젝트 루트 |
| `SAGE_MAX_LOOPS` | 50 | 최대 루프 횟수 |
| `SAGE_SESSION_TIMEOUT` | 3600 | 세션 타임아웃 (초) |
| `SAGE_SESSION_ID` | (자동) | 세션 ID |
| `SAGE_DEBUG` | 0 | 디버그 모드 |
| `SAGE_MAX_ERRORS` | 3 | Circuit breaker 오류 한도 |
| `SAGE_MAX_ROLE_LOOPS` | 5 | 역할당 최대 루프 |

---

## 6. 역할별 출력 스키마

각 역할은 JSON 형식으로 출력해야 함.

### 6.1 ideator

```json
{"ideas": ["아이디어1", ...], "count": 50}
```

### 6.2 analyst

```json
{"selected": ["항목1", ...], "key_items": ["핵심1", ...]}
```

### 6.3 critic

```json
{"risk_level": "낮음|보통|높음", "top_issues": ["이슈1", ...]}
```

### 6.4 censor

```json
{"status": "clean|violation", "violations": []}
```

### 6.5 academy

```json
{"evidence_count": 3, "references": ["참조1", ...]}
```

### 6.6 architect

```json
{"design_type": "설계유형", "components": ["컴포넌트1", ...]}
```

### 6.7 left-state-councilor / right-state-councilor

```json
{"approval": "승인|보류|거부", "opinion": "의견"}
```

### 6.8 executor

```json
{"status": "completed|failed", "files": ["파일1", ...]}
```

### 6.9 inspector

```json
{"result": "pass|fail", "issues": []}
```

### 6.10 validator

```json
{"result": "passed|failed", "passed": 5, "total": 5}
```

### 6.11 historian

```json
{"status": "recorded", "session_key": "키"}
```

### 6.12 reflector

```json
{"lessons_count": 2, "key_lessons": ["교훈1", ...]}
```

### 6.13 improver

```json
{"improvements_count": 2, "priority_items": ["개선1", ...]}
```

---

## 7. 트러블슈팅

### 7.1 Stop hook이 작동하지 않음

**증상**: Claude가 중간에 종료됨

**원인**: 세션 파일이 없거나 `active: false`

**해결**:
```bash
# 세션 상태 확인
cat /tmp/sage_session_*.json | jq '.active'

# 세션 초기화 확인
python3 .claude/hooks/sage_state_manager.py init "작업" --chain FULL
```

### 7.2 무한 루프

**증상**: 같은 역할이 계속 반복됨

**원인**: `complete` 호출 누락

**해결**:
```bash
# Circuit breaker 상태 확인
cat /tmp/sage_circuit_breaker_*.json

# 강제 리셋
python3 .claude/hooks/sage_state_manager.py cleanup
```

### 7.3 JSON 파싱 오류

**증상**: jq 오류 메시지

**해결**:
```bash
# 상태 파일 검증
jq . /tmp/sage_session_*.json

# 파일 재생성
rm /tmp/sage_session_*.json
python3 .claude/hooks/sage_state_manager.py init "작업"
```

---

## 8. 파일 목록

| 파일 | 위치 | 역할 |
|------|------|------|
| stop-hook.sh | `.claude/hooks/` | Stop hook (v2) |
| sage_state_manager.py | `.claude/hooks/` | 세션 상태 관리 |
| role_detector.py | `.claude/hooks/` | 역할 감지 |
| completion_detector.py | `.claude/hooks/` | 완료 신호 감지 |
| feedback_checker.py | `.claude/hooks/` | 피드백 대기 확인 |
| circuit_breaker_check.py | `.claude/hooks/` | 안전장치 |
| sage/SKILL.md | `.claude/skills/` | Sage 스킬 정의 |
| sage/config.yaml | `.claude/skills/` | 체인 설정 |

---

## 9. 참고 문서

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks.md)
- [Stop Hook 출력 형식](https://code.claude.com/docs/en/hooks.md#advanced-json-output)
- [CLAUDE.md SAGE_LOOP 섹션](../../CLAUDE.md)
- [ROLE_GRAPH.md](../ROLE_GRAPH.md)

---

## 10. 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|------|------|-----------|
| 1.0 | 2026-01-18 | 초기 구현 (exit 1 방식) |
| 2.0 | 2026-01-19 | exit 0 + JSON 방식으로 전환 |

---

*Dyarchy v3 - Sage Autonomous Loop System*

# Vercel Agent Skills 분석 및 Agent Session 구현 권장사항

> Vercel의 agent-skills 레포지토리 분석 결과 및 Agent Session 구현 노하우

**작성일**: 2026-01-22
**분석 대상**: https://github.com/vercel-labs/agent-skills
**목적**: 전체 구현 및 리팩토링 참고, Agent Session 노하우 파악

---

## 목차

1. [Vercel Agent Skills 개요](#1-vercel-agent-skills-개요)
2. [Skill 구조 및 패턴](#2-skill-구조-및-패턴)
3. [핵심 구현 패턴](#3-핵심-구현-패턴)
4. [Agent Session 노하우](#4-agent-session-노하우)
5. [우리 프로젝트 적용 방안](#5-우리-프로젝트-적용-방안)
6. [권장 리팩토링](#6-권장-리팩토링)

---

## 1. Vercel Agent Skills 개요

### 1.1 프로젝트 목적

AI 코딩 에이전트(Claude Code, Cursor, Copilot)의 능력을 확장하는 **패키징된 지침 및 스크립트** 모음.

**핵심 철학**:
- Skills는 **on-demand 로딩** (초기에는 name과 description만)
- **컨텍스트 효율성 최우선** (SKILL.md < 500줄)
- **Progressive Disclosure**: 필요한 파일만 읽기
- **스크립트 실행은 컨텍스트 소비 안 함** (출력만 소비)

### 1.2 제공 Skills

| Skill | 목적 | 특징 |
|-------|------|------|
| `react-best-practices` | React/Next.js 성능 최적화 | 45개 룰, 8개 카테고리, 우선순위 기반 |
| `web-design-guidelines` | UI/UX 베스트 프랙티스 | 100+ 룰, 접근성/성능/UX |
| `vercel-deploy-claimable` | Vercel 배포 자동화 | 프레임워크 자동 감지, 인증 불필요 |

---

## 2. Skill 구조 및 패턴

### 2.1 디렉토리 구조

```
skills/
  {skill-name}/                # kebab-case
    SKILL.md                   # 필수: skill 정의 (YAML frontmatter)
    scripts/                   # 선택: 실행 가능 스크립트
      {script-name}.sh         # Bash (권장)
    references/                # 선택: 참고 문서
      {topic}.md
    metadata.json              # 선택: 추가 메타데이터
  {skill-name}.zip             # 필수: 배포용 패키지
```

### 2.2 SKILL.md 프론트매터

```markdown
---
name: vercel-deploy
description: Deploy applications and websites to Vercel. Use this skill when the user requests deployment actions such as "Deploy my app", "Deploy this to production", "Create a preview deployment", "Deploy and give me the link", or "Push this live". No authentication required - returns preview URL and claimable deployment link.
metadata:
  author: vercel
  version: "1.0.0"
license: MIT
---

# {Skill Title}

{Brief description}

## How It Works

1. Step 1
2. Step 2
3. Step 3

## Usage

```bash
bash /mnt/skills/user/{skill-name}/scripts/{script}.sh [args]
```

## Output

{Example output}

## Present Results to User

{Template for formatting results}

## Troubleshooting

{Common issues and solutions}
```

**핵심 요소**:
- **name**: Skill 식별자 (kebab-case)
- **description**: **매우 구체적으로** (트리거 문구 포함: "Deploy my app", "Review my UI")
- **Progressive disclosure**: 상세 내용은 하위 섹션으로

### 2.3 Script 패턴

```bash
#!/bin/bash

# Title and description
# Usage: ./script.sh [args]
# Returns: JSON output format

set -e  # Fail-fast

# Constants
ENDPOINT="https://api.example.com/endpoint"

# Functions
do_something() {
    local arg="$1"
    # Logic
}

# Parse arguments
INPUT="${1:-.}"  # Default to current directory

# Create temp directory with cleanup trap
TEMP_DIR=$(mktemp -d)
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Main logic
echo "Processing..." >&2  # Status to stderr

# Do work
RESULT=$(curl -s "$ENDPOINT" -F "data=@$INPUT")

# Error handling
if echo "$RESULT" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESULT" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
    echo "Error: $ERROR_MSG" >&2
    exit 1
fi

# Success message to stderr
echo "Success!" >&2

# JSON output to stdout (for programmatic use)
echo "$RESULT"
```

**Best Practices**:
- ✅ `set -e`: 에러 시 즉시 중단
- ✅ `stderr`로 사용자 메시지 (`>&2`)
- ✅ `stdout`으로 JSON (프로그래밍 가능)
- ✅ `trap cleanup EXIT`: 임시 파일 정리
- ✅ 에러 처리 및 명확한 메시지

---

## 3. 핵심 구현 패턴

### 3.1 Rule-Based Documentation (react-best-practices)

**문제**: 45개의 성능 최적화 룰을 어떻게 관리할까?

**해결책**: 각 룰을 별도 파일로 분리

```
rules/
  async-parallel.md        # Promise.all() for independent ops
  bundle-barrel-imports.md # Avoid barrel file imports
  server-cache-react.md    # Use React.cache() for deduplication
  ...
  _sections.md             # Section metadata
```

**각 룰 파일 구조**:
```markdown
---
title: Promise.all() for Independent Operations
impact: CRITICAL
impactDescription: 2-10× improvement
tags: async, parallelization, promises, waterfalls
---

## {Title}

{Why it matters}

**Incorrect (sequential execution, 3 round trips):**

```typescript
const user = await fetchUser()
const posts = await fetchPosts()
const comments = await fetchComments()
```

**Correct (parallel execution, 1 round trip):**

```typescript
const [user, posts, comments] = await Promise.all([
  fetchUser(),
  fetchPosts(),
  fetchComments()
])
```
```

**장점**:
- 📁 **모듈화**: 각 룰 독립 관리
- 🔍 **검색 용이**: 파일명으로 빠른 탐색
- 🎯 **컨텍스트 효율**: 필요한 룰만 로딩
- ✏️ **유지보수성**: 개별 수정 용이

### 3.2 Framework Auto-Detection (vercel-deploy)

**문제**: 40+ 프레임워크를 어떻게 자동 감지할까?

**해결책**: `package.json`의 dependencies 순차 검사

```bash
detect_framework() {
    local pkg_json="$1"
    local content=$(cat "$pkg_json")

    # Helper to check if a package exists
    has_dep() {
        echo "$content" | grep -q "\"$1\""
    }

    # Order matters - check more specific frameworks first
    if has_dep "blitz"; then echo "blitzjs"; return; fi
    if has_dep "next"; then echo "nextjs"; return; fi
    if has_dep "gatsby"; then echo "gatsby"; return; fi
    if has_dep "@remix-run/"; then echo "remix"; return; fi
    # ... 40+ frameworks

    # No framework detected
    echo "null"
}
```

**패턴**:
1. **특정 → 일반 순서**: Blitz (Next.js 기반) → Next.js
2. **Scoped package 체크**: `@remix-run/`, `@shopify/hydrogen`
3. **Fallback**: `null` 반환 (정적 HTML)
4. **Early return**: 첫 매치에서 즉시 반환

**Static HTML 처리**:
```bash
# If there's exactly one HTML file and it's not index.html, rename it
if [ "$HTML_COUNT" -eq 1 ]; then
    HTML_FILE=$(echo "$HTML_FILES" | head -1)
    BASENAME=$(basename "$HTML_FILE")
    if [ "$BASENAME" != "index.html" ]; then
        mv "$HTML_FILE" "$PROJECT_PATH/index.html"
    fi
fi
```

### 3.3 Progressive Disclosure Pattern

**SKILL.md (500줄 이하)**:
```markdown
# React Best Practices

45 rules across 8 categories...

## Quick Reference

### 1. Eliminating Waterfalls (CRITICAL)
- `async-parallel` - Use Promise.all() for independent operations

### 2. Bundle Size (CRITICAL)
- `bundle-barrel-imports` - Import directly, avoid barrel files

## How to Use

Read individual rule files for detailed explanations:

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

## Full Compiled Document

For the complete guide: `AGENTS.md`
```

**동작 방식**:
1. Agent가 SKILL.md 읽음 (500줄, 가벼움)
2. 특정 룰 필요 시 `rules/{rule}.md` 읽음 (on-demand)
3. 전체 필요 시 `AGENTS.md` 읽음 (69KB, 선택적)

**컨텍스트 절약**:
- Initial load: 500줄 (SKILL.md)
- Per-rule load: 30줄 (individual rule)
- Full load: 2000줄 (AGENTS.md, 필요 시만)

---

## 4. Agent Session 노하우

### 4.1 Context Management

**원칙**: Skills는 **on-demand 로딩**

```
Startup:
├─ Load skill names and descriptions (100 bytes each)
└─ Total: 300 bytes for 3 skills ✅

When user says "Deploy my app":
├─ Load vercel-deploy/SKILL.md (500 lines)
├─ Execute deploy.sh (script execution ≈ 0 context)
└─ Load script output (200 lines JSON)
└─ Total: 700 lines for entire deployment ✅

Alternative (without skills):
├─ Agent needs full deployment knowledge in system prompt
└─ Total: 2000+ lines always loaded ❌
```

**핵심 통찰**:
- **스크립트 실행은 컨텍스트 소비 안 함** (출력만 소비)
- **파일 참조는 1단계 깊이** (SKILL.md → rules/{rule}.md)
- **500줄 제한**: Skill 문서는 간결하게

### 4.2 Description은 매우 구체적으로

**나쁜 예**:
```yaml
description: Deploy to Vercel
```

**좋은 예**:
```yaml
description: Deploy applications and websites to Vercel. Use this skill when the user requests deployment actions such as "Deploy my app", "Deploy this to production", "Create a preview deployment", "Deploy and give me the link", or "Push this live".
```

**이유**:
- Agent가 **언제 이 skill을 쓸지** 정확히 알 수 있음
- **트리거 문구** 명시 → 사용자 의도 파악 용이
- **False positive 감소** (관련 없는 skill 로딩 방지)

### 4.3 Output 형식 표준화

**Stderr (사용자 메시지)**:
```bash
echo "Preparing deployment..." >&2
echo "Detected framework: nextjs" >&2
echo "Deploying..." >&2
echo "✓ Deployment successful!" >&2
```

**Stdout (JSON, 프로그래밍 가능)**:
```bash
echo '{"previewUrl":"https://...","claimUrl":"https://..."}'
```

**장점**:
- 사용자는 stderr의 친화적 메시지 확인
- Agent는 stdout의 JSON으로 자동화
- 두 가지 니즈를 동시에 충족

### 4.4 Error Handling Template

```bash
set -e  # Fail-fast

# Attempt operation
RESULT=$(curl -s "$ENDPOINT" 2>&1) || {
    echo "Network error: $ENDPOINT unreachable" >&2
    exit 1
}

# Check for API error
if echo "$RESULT" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESULT" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
    echo "Error: $ERROR_MSG" >&2
    exit 1
fi

# Validate output
REQUIRED_FIELD=$(echo "$RESULT" | grep -o '"previewUrl":"[^"]*"' | cut -d'"' -f4)
if [ -z "$REQUIRED_FIELD" ]; then
    echo "Error: Missing required field in response" >&2
    echo "$RESULT" >&2
    exit 1
fi
```

**패턴**:
1. **Network error**: curl 실패 감지
2. **API error**: 응답에서 `"error"` 필드 추출
3. **Validation error**: 필수 필드 검증
4. **Helpful messages**: 사용자가 이해할 수 있는 에러 메시지

### 4.5 Skill Activation Decision Tree

Agent가 skill 사용 여부를 결정하는 과정:

```
User input: "Deploy my Next.js app"
    │
    ├─ 1. Parse intent: deployment action detected
    │
    ├─ 2. Match against skill descriptions:
    │   ├─ vercel-deploy: "Deploy applications... 'Deploy my app'"
    │   └─ Match! (trigger phrase found)
    │
    ├─ 3. Load SKILL.md (500 lines)
    │
    ├─ 4. Read usage instructions
    │
    ├─ 5. Detect project path
    │
    ├─ 6. Execute script:
    │   bash /mnt/skills/user/vercel-deploy/scripts/deploy.sh .
    │
    ├─ 7. Parse output (JSON)
    │
    └─ 8. Present results to user (template from SKILL.md)
```

**최적화**:
- Description이 구체적 → 2단계에서 빠른 매칭
- SKILL.md가 간결 → 3단계 컨텍스트 절약
- Script 실행 → 6단계 컨텍스트 소비 없음
- Output template → 8단계 일관된 UX

---

## 5. 우리 프로젝트 적용 방안

### 5.1 Agent Chat Session Skill 구조

```
skills/
  agent-chat-session/
    SKILL.md                           # Session 관리 정의
    scripts/
      create-session.sh                # 새 세션 생성
      switch-session.sh                # 세션 전환
      list-sessions.sh                 # 세션 목록
      cleanup-session.sh               # 세션 정리
    references/
      sse-reconnection.md              # SSE 재연결 패턴
      message-reconciliation.md        # Reconcile 알고리즘
      indexeddb-schema.md              # IndexedDB 스키마
```

**SKILL.md 예시**:
```markdown
---
name: agent-chat-session
description: Manage chat sessions with SSE streaming, optimistic updates, and eventual consistency. Use when switching chats, creating new sessions, or handling SSE reconnections. Triggers: "Switch to chat X", "Create new chat", "Reconnect SSE", "Show chat history".
version: "1.0.0"
---

# Agent Chat Session Management

Handles chat session lifecycle with real-time SSE streaming and IndexedDB persistence.

## How It Works

1. Creates session with unique chat_id
2. Establishes SSE connection for real-time updates
3. Implements optimistic updates (pending → committed)
4. Reconciles local/server data with 30s buffer
5. Persists to IndexedDB for refresh resilience

## Usage

### Create New Session

```bash
bash /mnt/skills/user/agent-chat-session/scripts/create-session.sh
```

Returns:
```json
{"chatId":"uuid","title":"New Chat","sseJobId":"job-123"}
```

### Switch Session

```bash
bash /mnt/skills/user/agent-chat-session/scripts/switch-session.sh [chat-id]
```

**Important**: Always cleanup previous SSE connection before switching.

## Present Results to User

When creating session:
```
✓ New chat session created!

Chat ID: abc-123
Title: New Chat

Ready to start messaging.
```

When switching:
```
✓ Switched to chat: "Previous Conversation"

Loaded 15 messages from cache.
Syncing with server...
```

## Troubleshooting

### SSE Connection Leak

If user reports "other session showing typing indicator":

1. Check if previous SSE connection is still active
2. Call cleanup before switching: `stopGeneration()`
3. Verify job_id matches current chat

### Message Loss

If messages disappear during pagination:

1. Check IndexedDB for local messages
2. Verify reconcile 30s buffer is active
3. Ensure Last-Event-ID header is sent for SSE reconnection
```

### 5.2 SSE Reconnection Script 예시

```bash
#!/bin/bash

# SSE Reconnection Script
# Usage: ./reconnect-sse.sh [job-id] [last-seq]
# Returns: JSON with missed events

set -e

JOB_ID="${1}"
LAST_SEQ="${2:-0}"
SSE_ENDPOINT="${VITE_API_BASE_URL}/api/v1/chat/${JOB_ID}/events"

if [ -z "$JOB_ID" ]; then
    echo "Error: job_id required" >&2
    exit 1
fi

echo "Reconnecting to SSE for job_id: $JOB_ID (last_seq: $LAST_SEQ)..." >&2

# Request with Last-Event-ID header
RESPONSE=$(curl -s -N -H "Last-Event-ID: $LAST_SEQ" "$SSE_ENDPOINT")

# Parse SSE events (simplified)
EVENTS=$(echo "$RESPONSE" | grep '^data:' | sed 's/^data: //')

# Count events
EVENT_COUNT=$(echo "$EVENTS" | wc -l | tr -d ' ')

echo "Received $EVENT_COUNT events" >&2

# Output JSON
cat <<EOF
{
  "jobId": "$JOB_ID",
  "lastSeq": $LAST_SEQ,
  "eventsReceived": $EVENT_COUNT,
  "events": $EVENTS
}
EOF
```

### 5.3 Message Reconciliation Reference 파일

```markdown
# references/message-reconciliation.md

# Message Reconciliation Algorithm

Eventual consistency를 다루기 위한 로컬/서버 메시지 병합.

## Algorithm

```typescript
reconcileMessages(local, server, {committedRetentionMs = 30000}) {
  // 1. Convert server messages to client format
  serverConverted = server.map(serverToClientMessage)

  // 2. Filter local messages to keep
  localToKeep = local.filter(msg => {
    // Always keep pending/streaming
    if (msg.status === 'pending' || msg.status === 'streaming') return true

    // Keep committed within 30s window (Eventual Consistency buffer)
    if (msg.status === 'committed' && !msg.server_id) {
      age = now - msg.created_at
      return age < committedRetentionMs
    }

    // Keep failed for retry
    if (msg.status === 'failed') return true

    return false
  })

  // 3. Merge and deduplicate
  merged = [...serverConverted, ...localToKeep]
  deduped = deduplicateByServerIdOrClientId(merged)

  // 4. Sort by created_at
  return deduped.sort((a, b) => a.created_at - b.created_at)
}
```

## Why 30 Seconds?

- Backend DB write: 200~500ms (average)
- Network latency: 100~200ms
- Retry delays: up to 5s
- Peak traffic buffer: 10s
- Total: ~30s provides comfortable margin

## Edge Cases

### Scenario: User scrolls during DB write

```
T0: User sends message (optimistic: pending)
T1: SSE done (local: committed, no server_id yet)
T2: User scrolls up → loadMoreMessages()
T3: Server returns messages (excluding T1, still writing)
T4: Reconcile keeps T1 message (age < 30s)
T5: Backend DB write completes
T6: Next loadMoreMessages() gets T1 from server
T7: Reconcile deduplicates (server_id match)
```

Result: ✅ Message never disappears
```

---

## 6. 권장 리팩토링

### 6.1 P0: SSE Last-Event-ID 패턴 적용

**현재 문제**: SSE 재연결 시 중간 이벤트 유실

**Vercel 패턴 적용**:

**Frontend (변경 없음 - EventSource 자동 처리)**:
```typescript
// src/hooks/agent/useAgentSSE.ts
const url = `${baseUrl}/api/v1/chat/${jobId}/events`;
const es = new EventSource(url, { withCredentials: true });
// EventSource가 자동으로 Last-Event-ID 헤더 전송
```

**Backend (SSE Gateway)**:
```python
# sse-gateway
async def stream_events(job_id: str, request: Request):
    # 1. Read Last-Event-ID header
    last_event_id = request.headers.get("Last-Event-ID", "0")
    last_seq = int(last_event_id) if last_event_id.isdigit() else 0

    # 2. Subscribe from last_seq
    async for event in manager.subscribe(job_id, last_seq):
        # 3. Always send id: field
        yield f"id: {event['seq']}\n"
        yield f"event: {event['stage']}\n"
        yield f"data: {json.dumps(event)}\n\n"
```

**장점**:
- ✅ 표준 SSE 메커니즘 (RFC 6202)
- ✅ 브라우저 네이티브 지원
- ✅ 프론트엔드 코드 변경 없음
- ✅ 모든 재연결 시나리오 커버

**작업 시간**: 백엔드 2시간

---

### 6.2 P0: Keepalive 이벤트 처리

**현재 문제**: 긴 작업 시 프론트엔드 타임아웃

**Vercel 패턴 적용**:

```typescript
// src/hooks/agent/useAgentSSE.ts
const createEventSource = (jobId: string) => {
  const es = new EventSource(url);

  // Keepalive event listener (추가)
  es.addEventListener('keepalive', () => {
    console.log('[DEBUG] Keepalive received');
    resetEventTimeout();
  });

  // 또는 모든 이벤트에서 타임아웃 리셋
  es.onmessage = (e) => {
    resetEventTimeout();  // 어떤 이벤트든 타임아웃 리셋
  };

  // ... existing listeners
};
```

**백엔드 (확인 필요)**:
```python
# sse-gateway (15초마다 keepalive 전송)
async def stream_events(job_id: str):
    while True:
        try:
            event = await asyncio.wait_for(queue.get(), timeout=15.0)
            yield event
        except asyncio.TimeoutError:
            # 15초 동안 이벤트 없으면 keepalive
            yield "event: keepalive\ndata: {}\n\n"
```

**장점**:
- ✅ "진행 안 됨" 현상 완전 제거
- ✅ 이미지 생성 등 긴 작업 안정화

**작업 시간**: 프론트엔드 30분

---

### 6.3 P0: 세션 전환 시 SSE 정리

**현재 문제**: 이전 채팅 이벤트가 현재 채팅에 표시

**Vercel Script 패턴 적용**:

**스크립트 방식 (참고용)**:
```bash
#!/bin/bash
# scripts/switch-session.sh

set -e

NEW_CHAT_ID="$1"
PREV_CHAT_ID="$2"

echo "Switching from $PREV_CHAT_ID to $NEW_CHAT_ID..." >&2

# 1. Cleanup previous SSE connection
if [ -n "$PREV_CHAT_ID" ]; then
    echo "Cleaning up previous SSE connection..." >&2
    # Send cleanup signal (implementation-specific)
fi

# 2. Load new chat messages
echo "Loading messages for $NEW_CHAT_ID..." >&2

# Output
cat <<EOF
{
  "from": "$PREV_CHAT_ID",
  "to": "$NEW_CHAT_ID",
  "cleaned": true
}
EOF
```

**React Hook 방식 (실제 적용)**:
```typescript
// src/hooks/agent/useAgentChat.ts
const loadChatMessages = async (chatId: string) => {
  // 1. ALWAYS cleanup previous SSE connection
  stopGeneration();  // ← 추가

  setIsLoadingHistory(true);
  // ... existing logic
};

const handleSetCurrentChat = (chat: ChatSummary | null) => {
  // 1. Cleanup
  stopGeneration();

  // 2. Switch
  setCurrentChat(chat);

  // 3. Load
  if (chat) {
    loadChatMessages(chat.id);
  }
};
```

**작업 시간**: 프론트엔드 1시간

---

### 6.4 P1: Rule-Based Documentation 패턴

**현재 상황**: 문제 리포트가 단일 대형 파일

**Vercel 패턴 적용**:

```
docs/
  reports/
    agent-data-integrity/
      README.md                          # Overview (500줄)
      issues/
        p0-sse-last-event-id.md          # SSE 재연결 이슈
        p0-keepalive-timeout.md          # Keepalive 타임아웃
        p0-session-switch-leak.md        # 세션 전환 누수
        p1-user-message-time-sync.md     # User 메시지 시간
        p1-indexeddb-error-handling.md   # IndexedDB 에러
      solutions/
        sse-reconnection-pattern.md      # 해결 패턴
        message-reconciliation.md        # Reconcile 패턴
      _metadata.json                     # 메타데이터
```

**README.md (Overview)**:
```markdown
# Agent Data Integrity Issues

6 issues identified, prioritized by impact.

## P0 (Critical)

| Issue | Impact | File |
|-------|--------|------|
| SSE Reconnection Loss | 🔴 Very High | [issues/p0-sse-last-event-id.md](issues/p0-sse-last-event-id.md) |
| Keepalive Timeout | 🔴 Very High | [issues/p0-keepalive-timeout.md](issues/p0-keepalive-timeout.md) |
| Session Switch Leak | 🟡 High | [issues/p0-session-switch-leak.md](issues/p0-session-switch-leak.md) |

## Solutions

Detailed implementation patterns:
- [SSE Reconnection Pattern](solutions/sse-reconnection-pattern.md)
- [Message Reconciliation](solutions/message-reconciliation.md)

## Quick Start

For immediate fixes, see P0 issues above.
```

**장점**:
- 📁 모듈화: 이슈별 독립 파일
- 🔍 검색 용이: 파일명으로 빠른 탐색
- 🎯 컨텍스트 효율: 필요한 이슈만 읽기
- ✏️ 유지보수성: 개별 수정 용이

---

### 6.5 Framework Detection 패턴 (선택적)

**현재**: 프레임워크 감지 로직 없음 (필요 시)

**Vercel 패턴**:
```typescript
// utils/detectFramework.ts
export function detectFramework(packageJson: any): string | null {
  const deps = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies
  };

  // Order matters - check specific → general
  if (deps['next']) return 'nextjs';
  if (deps['vite']) return 'vite';
  if (deps['@remix-run/react']) return 'remix';
  // ...

  return null;
}
```

**활용 예시**:
- 빌드 최적화 힌트 제공
- 프레임워크별 설정 자동 적용
- 에러 메시지 맞춤화

---

## 결론

### 핵심 학습

1. **컨텍스트 효율성이 최우선**
   - SKILL.md < 500줄
   - Progressive disclosure
   - 스크립트 실행은 컨텍스트 소비 안 함

2. **Description은 구체적으로**
   - 트리거 문구 명시
   - 사용 시점 명확화
   - False positive 방지

3. **Rule-Based Documentation**
   - 각 이슈/솔루션을 별도 파일로
   - Overview로 빠른 탐색
   - On-demand 로딩

4. **Script Best Practices**
   - `set -e`: Fail-fast
   - stderr: 사용자 메시지
   - stdout: JSON (프로그래밍 가능)
   - `trap cleanup EXIT`: 리소스 정리

5. **Error Handling**
   - Network, API, Validation 에러 구분
   - 명확한 에러 메시지
   - Troubleshooting 섹션 제공

### 즉시 적용 가능한 개선사항

| 우선순위 | 항목 | Vercel 패턴 | 작업 시간 |
|---------|------|------------|----------|
| P0-1 | SSE Last-Event-ID | EventSource 표준 | 백엔드 2h |
| P0-2 | Keepalive 처리 | 이벤트 리스너 추가 | 프론트 0.5h |
| P0-3 | 세션 전환 정리 | cleanup 패턴 | 프론트 1h |
| P1-4 | Rule-Based Docs | 파일 분리 | 1h |

### Agent Session 구현 시 핵심

1. **SSE 연결 생명주기 관리**
   - Last-Event-ID로 재연결 복구
   - Keepalive로 타임아웃 방지
   - 세션 전환 시 cleanup

2. **컨텍스트 최적화**
   - Skill 문서 500줄 이하
   - 참조 문서 on-demand 로딩
   - 스크립트로 로직 외부화

3. **에러 핸들링**
   - Network, API, Validation 구분
   - Troubleshooting 가이드 제공
   - 명확한 사용자 메시지

---

**참고 자료**:
- Vercel Agent Skills: https://github.com/vercel-labs/agent-skills
- Agent Skills Format: https://agentskills.io/
- SSE Specification: RFC 6202

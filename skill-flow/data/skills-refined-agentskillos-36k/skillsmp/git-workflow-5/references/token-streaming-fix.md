# Token Streaming Fix - Git Flow 사례

> **PR**: [#437](https://github.com/eco2-team/backend/pull/437)
> **브랜치**: `fix/token-streaming-langchain`
> **Base**: `develop`

## 배경

토큰 스트리밍이 동작하지 않는 문제 발견 → 원인 분석 → 해결책 구현

### 문제 상황
- SSE 이벤트에서 `stage` 이벤트만 수신, `token` 이벤트 없음
- 사용자에게 응답이 한 번에 전달됨 (스트리밍 X)

### 근본 원인
- `OpenAILLMClient`가 순수 OpenAI SDK 사용
- LangGraph의 `on_llm_stream` 이벤트는 **LangChain LLM에서만 발생**
- 토큰이 nested async generator를 통해 yield되어 LangGraph가 감지 불가

## Git Flow 적용

### 1. 별도 브랜치 + Worktree 생성

다른 에이전트가 `develop`에서 작업 중이었으므로 worktree 분리:

```bash
# develop 기준으로 새 브랜치 생성
cd /path/to/main-repo
git worktree add ../backend-token-streaming -b fix/token-streaming-langchain origin/develop
```

### 2. 트러블슈팅 리포트 먼저 작성

코드 변경 전 문제 분석 및 해결 방안 문서화:
- `docs/reports/token-streaming-troubleshooting.md`

### 3. 구현 및 커밋

```bash
# 변경사항 확인
git status
git diff --stat

# 스테이징 및 커밋
git add -A
git commit -m "feat(chat_worker): implement token streaming with stream_mode=messages"
```

### 4. Push 및 PR 생성

```bash
# 브랜치 push
git push -u origin fix/token-streaming-langchain

# PR 생성 with labels
gh pr create \
  --base develop \
  --title "feat(chat_worker): implement token streaming with stream_mode=messages" \
  --assignee mangowhoiscloud \
  --label "enhancement,ai,streaming,chat" \
  --body "..."
```

## 주요 변경 파일

| 파일 | 역할 |
|------|------|
| `langchain_runnable_wrapper.py` | OpenAI SDK → `BaseChatModel` 래퍼 |
| `langchain_adapter.py` | `LLMClientPort` 어댑터 |
| `process_chat.py` | `stream_mode=["messages", "updates"]` 기반 재구현 |
| `dependencies.py` | `enable_token_streaming` 플래그 |
| `test_process_chat.py` | Mock 업데이트 |

## 아키텍처 변경

### Before (A1 - astream_events)
```
LangGraph astream_events(version="v2")
    │
    └── on_llm_stream 이벤트 (LangChain LLM 필요)
            │
            └── OpenAILLMClient (순수 SDK) ← 이벤트 발생 안 함!
```

### After (A2 - stream_mode)
```
LangGraph astream(stream_mode=["messages", "updates"])
    │
    ├── "messages" → (AIMessageChunk, metadata) → notify_token_v2()
    │
    └── "updates" → {node_name: state} → notify_stage()
           │
           └── LangChainLLMAdapter
                   │
                   └── LangChainOpenAIRunnable._astream()
                           │
                           └── AIMessageChunk yield → LangGraph 캡처
```

## Labels 사용

PR에 적절한 라벨 부착:
- `enhancement` - 새 기능
- `ai` - AI 관련
- `streaming` - 스트리밍 관련 (신규 생성)
- `chat` - Chat Worker 관련 (신규 생성)

```bash
# 라벨 생성 (없으면)
gh label create "chat" --description "Chat Worker 관련" --color "9333EA"
gh label create "streaming" --description "실시간 스트리밍 관련" --color "F59E0B"
```

## 검증 계획

1. **로컬 검증**: `py_compile`로 구문 검사
2. **단위 테스트**: `MockPipeline.astream()` 추가
3. **통합 테스트**: dev 환경 배포 후 SSE 이벤트 확인
4. **E2E 테스트**: `scripts/e2e-intent-test.sh`로 토큰 이벤트 확인

## 참고 문서

- [LangGraph Streaming Docs](https://docs.langchain.com/oss/python/langgraph/streaming#messages)
- 트러블슈팅 리포트: `docs/reports/token-streaming-troubleshooting.md`

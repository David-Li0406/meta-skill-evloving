---
name: chat-agent-persistence
description: Chat 서비스의 영속화 레이어 가이드. Checkpointer(멀티턴 컨텍스트), Message Persistence(PostgreSQL), Redis Streams Consumer 아키텍처 및 트러블슈팅. Use when: (1) chat.messages 테이블이 비어있을 때, (2) checkpointer 관련 에러 발생 시, (3) 멀티턴 대화 컨텍스트가 유지되지 않을 때, (4) Redis Streams consumer group 설정 시.
---

# Chat Agent Persistence Guide

> Chat 서비스의 데이터 영속화 레이어 (Checkpointer + Message Storage)

## Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────┐
│                     Chat Persistence Architecture                          │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ┌─────────────┐                                                          │
│  │ chat-worker │                                                          │
│  │ (LangGraph) │                                                          │
│  └──────┬──────┘                                                          │
│         │                                                                  │
│    ┌────┴────┐                                                            │
│    │         │                                                            │
│    ▼         ▼                                                            │
│  Checkpointer    Progress Events                                          │
│  (Multi-turn)    (Stage updates)                                          │
│    │                  │                                                   │
│    │                  │ XADD                                              │
│    ▼                  ▼                                                   │
│  ┌────────────┐  ┌──────────────────┐                                    │
│  │ PostgreSQL │  │  Redis Streams   │                                    │
│  │checkpoints │  │ chat:events:{0-3}│                                    │
│  └────────────┘  └────────┬─────────┘                                    │
│                           │                                               │
│              ┌────────────┼────────────┐                                 │
│              │            │            │                                 │
│              ▼            ▼            ▼                                 │
│      ┌─────────────┐ ┌─────────────┐ ┌──────────────────┐              │
│      │ eventrouter │ │chat-persist │ │  (other groups)  │              │
│      │   (group)   │ │  (group)    │ │                  │              │
│      └──────┬──────┘ └──────┬──────┘ └──────────────────┘              │
│             │               │                                           │
│             ▼               ▼                                           │
│      ┌─────────────┐ ┌──────────────┐                                  │
│      │event-router │ │chat-consumer │                                  │
│      │  (SSE fan)  │ │  (DB write)  │                                  │
│      └─────────────┘ └──────┬───────┘                                  │
│                             │                                           │
│                             ▼                                           │
│                      ┌──────────────┐                                  │
│                      │  PostgreSQL  │                                  │
│                      │chat.messages │                                  │
│                      └──────────────┘                                  │
│                                                                         │
└───────────────────────────────────────────────────────────────────────────┘
```

## Two Persistence Paths

| Path | Purpose | Component | Target |
|------|---------|-----------|--------|
| **Checkpointer** | 멀티턴 컨텍스트 (LangGraph state) | CachedPostgresSaver | checkpoints 테이블 |
| **Message Storage** | 대화 이력 (user/assistant) | ChatPersistenceConsumer | chat.messages 테이블 |

## Quick Diagnosis

```bash
# 1. chat.messages 테이블 확인
kubectl exec -n postgres deploy/postgresql -- psql -U sesacthon -d ecoeco -c \
  "SELECT COUNT(*) FROM chat.messages;"

# 2. Checkpointer 상태 확인 (worker 로그)
kubectl logs -n chat deploy/chat-worker --tail=100 | grep -E "(CachedPostgresSaver|checkpointer|InMemory)"

# 3. Redis Streams consumer group 확인
kubectl exec -n redis rfr-streams-redis-0 -c redis -- redis-cli XINFO GROUPS chat:events:0
```

## Common Issues

### Issue 1: CachedPostgresSaver 초기화 실패

**증상**: `InMemory checkpointer created (Redis fallback disabled)`

**로그**:
```
[WARNING] CachedPostgresSaver failed, falling back to Redis only:
object _AsyncGeneratorContextManager can't be used in 'await' expression
```

**원인**: `checkpointer.py:228`에서 async context manager를 `await`로 호출

**상세**: See [checkpointer.md](references/checkpointer.md)

### Issue 2: chat.messages 테이블 비어있음

**증상**: `chat.conversations`에 데이터 있지만 `chat.messages`는 0건

**진단**:
```bash
# Consumer group 확인 - "chat-persistence" 없으면 미배포
kubectl exec -n redis rfr-streams-redis-0 -c redis -- redis-cli XINFO GROUPS chat:events:0
```

**원인**: ChatPersistenceConsumer 미배포

**상세**: See [message-consumer.md](references/message-consumer.md)

## Code Locations

| Component | Path |
|-----------|------|
| Checkpointer | `apps/chat_worker/infrastructure/orchestration/langgraph/checkpointer.py` |
| Dependencies | `apps/chat_worker/setup/dependencies.py` (Lines 641-678) |
| Consumer Entry | `apps/chat/consumer.py` |
| Consumer Infra | `apps/chat/infrastructure/messaging/redis_streams_consumer.py` |
| Consumer Adapter | `apps/chat/presentation/consumer/redis_streams_adapter.py` |

## Reference Files

- **Checkpointer 상세**: See [checkpointer.md](references/checkpointer.md) - Cache-Aside 패턴, LangGraph API
- **Message Consumer 상세**: See [message-consumer.md](references/message-consumer.md) - 배포 방법, Consumer Group
- **트러블슈팅 문서**: `docs/troubleshooting/chat-messages-not-persisted.md`
- **PostgreSQL 분석**: `docs/reports/postgres-chat-data-analysis.md`

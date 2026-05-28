# Message Consumer Reference

> Redis Streams → PostgreSQL 메시지 영속화

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                Event-First Architecture                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  chat-worker                                                     │
│       │                                                          │
│       │ XADD (done event with persistence data)                  │
│       ▼                                                          │
│  Redis Streams (chat:events:{0-3})                               │
│       │                                                          │
│       ├───────────────────────┬──────────────────────┐          │
│       │                       │                      │          │
│       ▼                       ▼                      ▼          │
│  [eventrouter]          [chat-persistence]      [other]         │
│  Consumer Group          Consumer Group         Groups          │
│       │                       │                                  │
│       ▼                       ▼                                  │
│  event-router            chat-consumer                           │
│  (SSE fan-out)          (DB persistence)                         │
│       │                       │                                  │
│       ▼                       ▼                                  │
│  sse-gateway             PostgreSQL                              │
│  (Client SSE)           (chat.messages)                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Consumer Group 분리

| Group | Consumer | Purpose |
|-------|----------|---------|
| `eventrouter` | event-router | SSE 실시간 전송 |
| `chat-persistence` | chat-consumer | PostgreSQL 저장 |

**장점**: 같은 이벤트를 두 Consumer가 독립적으로 처리 (Fan-out)

## Done Event 구조

```json
{
  "stage": "done",
  "status": "success",
  "progress": 100,
  "job_id": "abc123",
  "result": {
    "answer": "...",
    "persistence": {
      "chat_id": "uuid",
      "user_message": {
        "role": "user",
        "content": "플라스틱 어떻게 버려?",
        "intent": "waste"
      },
      "assistant_message": {
        "role": "assistant",
        "content": "플라스틱은...",
        "metadata": {"nodes_executed": ["waste_rag", "weather"]}
      }
    }
  }
}
```

## Code Structure

```
apps/chat/
├── consumer.py                          # Entry point (python -m chat.consumer)
├── setup/
│   └── consumer_dependencies.py         # DI Container
├── infrastructure/
│   └── messaging/
│       └── redis_streams_consumer.py    # ChatPersistenceConsumer (Infra)
└── presentation/
    └── consumer/
        └── redis_streams_adapter.py     # Adapter (batch + flush)
```

## ChatPersistenceConsumer

```python
class ChatPersistenceConsumer:
    """Redis Streams Consumer Group으로 done 이벤트 소비."""

    CONSUMER_GROUP = "chat-persistence"

    async def setup(self) -> None:
        """Consumer Group 생성 (없으면 생성)."""
        for shard in range(self._shard_count):
            stream_key = f"chat:events:{shard}"
            await self._redis.xgroup_create(
                stream_key,
                self.CONSUMER_GROUP,
                id="0",
                mkstream=True,
            )

    async def consume(self, callback) -> None:
        """메인 Consumer 루프."""
        while not self._shutdown:
            events = await self._redis.xreadgroup(
                groupname=self.CONSUMER_GROUP,
                consumername=self._consumer_name,
                streams=self._streams,
                count=100,
                block=5000,
            )
            for stream_name, messages in events:
                for msg_id, data in messages:
                    event = self._parse_event(data)

                    # done 이벤트만 처리
                    if event.get("stage") != "done":
                        await self._redis.xack(stream_name, self.CONSUMER_GROUP, msg_id)
                        continue

                    # persistence 데이터 추출
                    persistence = event.get("result", {}).get("persistence")
                    if persistence:
                        success = await callback(persistence)
                        if success:
                            await self._redis.xack(stream_name, self.CONSUMER_GROUP, msg_id)
```

## Deployment (현재 미배포)

### Step 1: Deployment Manifest

```yaml
# workloads/domains/chat/base/deployment-consumer.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chat-consumer
  namespace: chat
  labels:
    app: chat-consumer
    tier: worker
    domain: chat
spec:
  replicas: 1
  selector:
    matchLabels:
      app: chat-consumer
  template:
    metadata:
      labels:
        app: chat-consumer
        tier: worker
        domain: chat
    spec:
      containers:
      - name: chat-consumer
        image: docker.io/mng990/eco2:chat-api-dev-latest
        command: ["python", "-m", "chat.consumer"]
        envFrom:
        - configMapRef:
            name: chat-config
        - secretRef:
            name: chat-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
      nodeSelector:
        domain: chat
      tolerations:
      - key: domain
        operator: Equal
        value: chat
        effect: NoSchedule
```

### Step 2: Kustomization 업데이트

```yaml
# workloads/domains/chat/base/kustomization.yaml
resources:
  - deployment.yaml
  - deployment-canary.yaml
  - deployment-consumer.yaml  # 추가
  - service.yaml
  - configmap.yaml
  - destination-rule.yaml
```

### Step 3: ArgoCD Application

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: dev-chat-consumer
  namespace: argocd
spec:
  destination:
    namespace: chat
    server: https://kubernetes.default.svc
  source:
    path: workloads/domains/chat/dev
    repoURL: https://github.com/eco2-team/backend.git
    targetRevision: develop
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Verification

```bash
# 1. Consumer Group 존재 확인
kubectl exec -n redis rfr-streams-redis-0 -c redis -- \
  redis-cli XINFO GROUPS chat:events:0 | grep chat-persistence

# 2. Consumer Pod 상태 확인
kubectl get pods -n chat -l app=chat-consumer

# 3. Consumer 로그 확인
kubectl logs -n chat -l app=chat-consumer -f --tail=50

# 4. 메시지 저장 확인
kubectl exec -n postgres deploy/postgresql -- psql -U sesacthon -d ecoeco -c \
  "SELECT c.title, COUNT(m.id) as msg_count
   FROM chat.conversations c
   LEFT JOIN chat.messages m ON c.id = m.chat_id
   GROUP BY c.id ORDER BY c.created_at DESC LIMIT 5;"
```

## Batch Processing

Consumer Adapter는 배치 처리로 효율성 향상:

| Config | Value | Description |
|--------|-------|-------------|
| Batch Size | 100 | 최대 배치 크기 |
| Flush Interval | 5s | 타임아웃 시 강제 flush |

```python
# RedisStreamsConsumerAdapter
async def _auto_flush_loop(self) -> None:
    """5초마다 pending 배치 flush."""
    while not self._shutdown:
        await asyncio.sleep(5)
        if self._pending_batch:
            await self._flush_batch()
```

## Related Files

| File | Description |
|------|-------------|
| `consumer.py` | Entry point |
| `redis_streams_consumer.py` | Infrastructure layer |
| `redis_streams_adapter.py` | Presentation layer (batch) |
| `consumer_dependencies.py` | DI Container |

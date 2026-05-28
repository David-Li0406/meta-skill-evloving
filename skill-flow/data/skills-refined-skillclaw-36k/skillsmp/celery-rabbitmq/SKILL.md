---
name: celery-rabbitmq
description: Celery Worker + RabbitMQ Topology CR 패턴 가이드. 큐 생성, Exchange/Binding 정의, DLQ 설정 시 참조. "celery", "rabbitmq", "queue", "topology", "dlq", "exchange", "binding" 키워드로 트리거.
---

# Celery + RabbitMQ Topology Pattern Guide

## Overview

Eco2 프로젝트에서 Celery Worker + RabbitMQ 구성 시 Topology CR(Custom Resource)에 큐 생성을 위임하는 패턴.

**핵심 원칙**: Python 코드에서는 라우팅만 정의, 큐/Exchange/Binding 생성은 Kubernetes Topology CR에서 선언적으로 관리.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Queue Creation Flow                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Topology CR (YAML)          RabbitMQ Operator                  │
│  ┌─────────────────┐        ┌──────────────────┐                │
│  │ Queue CR        │───────▶│ Create Queue     │                │
│  │ Exchange CR     │───────▶│ Create Exchange  │                │
│  │ Binding CR      │───────▶│ Create Binding   │                │
│  └─────────────────┘        └──────────────────┘                │
│                                      │                          │
│                                      ▼                          │
│  Celery Worker              ┌──────────────────┐                │
│  ┌─────────────────┐        │ RabbitMQ Cluster │                │
│  │ task_routes     │───────▶│ (eco2-rabbitmq)  │                │
│  │ task_queues     │        │                  │                │
│  │ no_declare=True │        │ vhost: eco2      │                │
│  └─────────────────┘        └──────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Celery Configuration Pattern

### 1. Task Routes (태스크 → 큐 매핑)

```python
# apps/<worker>/setup/celery.py

WORKER_TASK_ROUTES = {
    "domain.task_name": {"queue": "domain.task_name"},
    "domain.another_task": {"queue": "domain.another_task"},
}
```

### 2. Task Queues (kombu Queue 정의)

```python
from kombu import Queue

# ⚠️ 핵심: no_declare=True, exchange=""
WORKER_TASK_QUEUES = [
    Queue("domain.task_name", exchange="", routing_key="domain.task_name", no_declare=True),
    Queue("domain.another_task", exchange="", routing_key="domain.another_task", no_declare=True),
]
```

**파라미터 설명:**
- `exchange=""`: AMQP Default Exchange 사용 (queue 이름으로 직접 라우팅)
- `routing_key=<queue_name>`: Default Exchange에서는 queue 이름과 동일해야 함
- `no_declare=True`: Celery/kombu가 큐를 선언하지 않음 (Topology CR이 생성)

### 3. Celery App 설정

```python
celery_app.conf.update(
    # Task routing
    task_routes=WORKER_TASK_ROUTES,
    task_queues=WORKER_TASK_QUEUES,

    # ⚠️ 핵심: 큐 자동 생성 비활성화
    task_create_missing_queues=False,

    # Default Exchange 사용
    task_default_exchange="",
    task_default_routing_key="celery",

    # 일반 설정
    task_serializer="json",
    accept_content=["json"],
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
)
```

---

## RabbitMQ Topology CR Pattern

### Queue CR

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: Queue
metadata:
  name: <worker>-<task>-queue  # K8s 리소스명 (kebab-case)
  namespace: rabbitmq
spec:
  name: <domain>.<task>        # 실제 큐 이름 (dot notation)
  type: classic                # Classic Queue (Celery 호환)
  durable: true
  autoDelete: false
  vhost: eco2
  arguments:
    x-dead-letter-exchange: dlx
    x-dead-letter-routing-key: dlq.<domain>.<task>
    x-message-ttl: 3600000     # 1시간 (용도에 따라 조정)
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

### Dead Letter Queue CR

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: Queue
metadata:
  name: dlq-<domain>-<task>
  namespace: rabbitmq
spec:
  name: dlq.<domain>.<task>
  type: classic
  durable: true
  autoDelete: false
  vhost: eco2
  arguments:
    x-message-ttl: 604800000   # 7일 보관
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

### DLX Binding CR

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: Binding
metadata:
  name: dlx-<domain>-<task>-binding
  namespace: rabbitmq
spec:
  source: dlx                  # Dead Letter Exchange
  destination: dlq.<domain>.<task>
  destinationType: queue
  routingKey: dlq.<domain>.<task>
  vhost: eco2
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

---

## Exchange Types

### 1. Default Exchange ("")
- Celery 기본 패턴
- routing_key = queue name으로 직접 라우팅
- Exchange CR 불필요

### 2. Direct Exchange
- Named Exchange + routing_key 매칭
- 특정 큐로 명시적 라우팅

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: Exchange
metadata:
  name: <domain>-direct
  namespace: rabbitmq
spec:
  name: <domain>.direct
  type: direct
  durable: true
  autoDelete: false
  vhost: eco2
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

### 3. Fanout Exchange
- 브로드캐스트 패턴 (1:N)
- routing_key 무시, 바인딩된 모든 큐에 복제

```yaml
apiVersion: rabbitmq.com/v1beta1
kind: Exchange
metadata:
  name: <domain>-events
  namespace: rabbitmq
spec:
  name: <domain>.events
  type: fanout
  durable: true
  autoDelete: false
  vhost: eco2
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

---

## TTL Guidelines

| Use Case | TTL | 설명 |
|----------|-----|------|
| 동기 응답 (RPC) | 30초 | 빠른 응답 필요 |
| 빠른 처리 | 5분 | Rule-based, 단순 로직 |
| 일반 처리 | 10분~1시간 | API 호출, DB 작업 |
| AI/LLM 처리 | 1시간 | GPT, Vision 등 |
| 중요 데이터 | 24시간 | DB 저장, 결제 등 |
| DLQ | 7일 | 실패 메시지 보관 |

---

## File Locations

```
workloads/rabbitmq/base/topology/
├── exchanges.yaml    # Exchange 정의
├── queues.yaml       # Queue + DLQ 정의
├── bindings.yaml     # Exchange → Queue 바인딩
├── vhost.yaml        # VHost 정의 (eco2)
├── users.yaml        # User CR + credentials Secret
├── permissions.yaml  # Permission CR
└── kustomization.yaml
```

---

## RabbitMQ 연결 정보

### Eco² 클러스터 설정

| 항목 | 값 |
|------|-----|
| **클러스터** | `eco2-rabbitmq.rabbitmq.svc.cluster.local:5672` |
| **VHost** | `eco2` |
| **계정** | `eco2worker` |
| **URL 형식** | `amqp://eco2worker:<password>@eco2-rabbitmq.rabbitmq.svc.cluster.local:5672/eco2` |

### User CR 관리

```yaml
# workloads/rabbitmq/base/topology/users.yaml
apiVersion: rabbitmq.com/v1beta1
kind: User
metadata:
  name: eco2-worker-user
  namespace: rabbitmq
spec:
  tags:
  - management
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
  importCredentialsSecret:
    name: eco2-worker-credentials
```

### Permission CR

```yaml
# workloads/rabbitmq/base/topology/permissions.yaml
apiVersion: rabbitmq.com/v1beta1
kind: Permission
metadata:
  name: eco2-worker-permission
  namespace: rabbitmq
spec:
  vhost: eco2
  userReference:
    name: eco2-worker-user
  permissions:
    configure: ".*"
    write: ".*"
    read: ".*"
  rabbitmqClusterReference:
    name: eco2-rabbitmq
    namespace: rabbitmq
```

---

## Checklist: New Worker Queue 추가

1. **Celery 설정** (`apps/<worker>/setup/celery.py`)
   - [ ] `WORKER_TASK_ROUTES`에 태스크 추가
   - [ ] `WORKER_TASK_QUEUES`에 Queue 추가 (no_declare=True)
   - [ ] `task_create_missing_queues=False` 확인

2. **Topology CR** (`workloads/rabbitmq/base/topology/`)
   - [ ] `queues.yaml`: Queue CR 추가
   - [ ] `queues.yaml`: DLQ CR 추가
   - [ ] `bindings.yaml`: DLX Binding CR 추가
   - [ ] (선택) `exchanges.yaml`: Named Exchange 추가
   - [ ] (선택) `bindings.yaml`: Exchange → Queue Binding 추가

3. **Kustomization**
   - [ ] `kustomization.yaml`에 새 파일 포함 확인

4. **배포**
   - [ ] ArgoCD Sync로 Topology CR 적용
   - [ ] RabbitMQ Management UI에서 큐 생성 확인
   - [ ] Worker 배포 후 큐 소비 확인

---

## Troubleshooting

### Worker 시작 시 "Queue not found"
- Topology CR이 먼저 적용되었는지 확인
- `kubectl get queues -n rabbitmq` 로 Queue CR 상태 확인

### 메시지가 DLQ로 이동하지 않음
- Queue arguments에 `x-dead-letter-exchange: dlx` 확인
- DLX Binding이 올바른지 확인

### Celery가 큐를 재선언함
- `no_declare=True` 누락 확인
- `task_create_missing_queues=False` 확인

---

## Reference Files

- Topology CR: [queues.yaml](../../../workloads/rabbitmq/base/topology/queues.yaml)
- Celery 예시: [scan_worker/setup/celery.py](../../../apps/scan_worker/setup/celery.py)

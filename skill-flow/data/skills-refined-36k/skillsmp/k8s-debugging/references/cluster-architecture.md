# Eco² 클러스터 아키텍처

## 클러스터 개요

> **중요**: 자체 관리형 K8s 클러스터 (EKS 아님)
> - 마스터 노드: `k8s-master` (13.209.44.249)
> - SSH 접속: `ssh -i ~/.ssh/sesacthon.pem ubuntu@13.209.44.249`
> - GitOps: ArgoCD가 `develop` 브랜치를 바라보며 sync

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Self-Managed K8s Cluster (ap-northeast-2)                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         Business Logic Tier                          │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐            │    │
│  │  │ auth-api │  │ chat-api │  │ scan-api │  │ image-api│            │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘            │    │
│  │  ┌──────────────┐  ┌──────────────┐                                │    │
│  │  │ character-api│  │ location-api │  (gRPC)                        │    │
│  │  └──────────────┘  └──────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           Worker Tier                                │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐            │    │
│  │  │ chat-worker │  │ scan-worker │  │ character-worker │            │    │
│  │  │ (LangGraph) │  │             │  │                  │            │    │
│  │  └─────────────┘  └─────────────┘  └──────────────────┘            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        Integration Tier                              │    │
│  │  ┌──────────────┐  ┌─────────────┐                                  │    │
│  │  │ event-router │  │ sse-gateway │  (Redis Streams + Pub/Sub)       │    │
│  │  └──────────────┘  └─────────────┘                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           Data Tier                                  │    │
│  │  ┌───────────────┐  ┌───────────────────┐  ┌─────────────┐         │    │
│  │  │  PostgreSQL   │  │ Redis Sentinel    │  │  RabbitMQ   │         │    │
│  │  │ (Single/HA)   │  │ (3-node HA)       │  │             │         │    │
│  │  └───────────────┘  └───────────────────┘  └─────────────┘         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        Platform Tier                                 │    │
│  │  ┌───────────┐  ┌────────────┐  ┌───────────────────────┐          │    │
│  │  │  ArgoCD   │  │   Istio    │  │ External Secrets Oper │          │    │
│  │  └───────────┘  └────────────┘  └───────────────────────┘          │    │
│  │  ┌────────────────────┐  ┌───────────────┐                         │    │
│  │  │ Prometheus Operator│  │  ALB Ingress  │                         │    │
│  │  └────────────────────┘  └───────────────┘                         │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Namespace 구조

### Tier별 Namespace

| Tier | Namespace | 용도 |
|------|-----------|------|
| **business-logic** | auth, my, scan, character, location, image, chat | API 서비스 |
| **worker** | (각 도메인 내) | Celery/비동기 워커 |
| **data** | postgres, redis | 데이터 저장소 |
| **integration** | rabbitmq | 메시지 브로커 |
| **observability** | prometheus, grafana | 모니터링 |
| **infrastructure** | platform-system, data-system, messaging-system | Operators |

### Namespace 조회

```bash
# 전체 Namespace
kubectl get ns -l app.kubernetes.io/part-of=ecoeco-backend

# Tier별 조회
kubectl get ns -l tier=business-logic
kubectl get ns -l tier=data
kubectl get ns -l tier=infrastructure
```

---

## Node Pool 구성

### 노드 그룹

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Self-Managed K8s Nodes                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐     │
│  │ k8s-master      │  │ k8s-worker-1~2  │  │ k8s-storage     │     │
│  │ (Control Plane) │  │ (API/Worker)    │  │ (DB/Redis)      │     │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Node Selector 패턴

```yaml
# API/Worker용 노드 선택
spec:
  nodeSelector:
    node-pool: app
  tolerations:
  - key: workload-type
    operator: Equal
    value: api
    effect: NoSchedule
```

### 노드 상태 확인

```bash
# 노드 그룹별 확인
kubectl get nodes -l node-pool=app
kubectl get nodes -l node-pool=data

# 노드 리소스 상태
kubectl describe nodes | grep -A 10 "Allocated resources"

# 노드별 Pod 분포
kubectl get pods -A -o wide | grep <node-name>
```

---

## 네트워크 구성

### 서비스 메시 (Istio)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Istio Service Mesh                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐           │
│  │   Gateway   │────▶│VirtualService│────▶│DestinationRule│        │
│  │ (ALB/NLB)   │     │  (Routing)  │     │  (Subset)    │          │
│  └─────────────┘     └─────────────┘     └─────────────┘           │
│                                                                      │
│  Envoy Sidecar: 모든 비즈니스 Pod에 자동 주입                       │
│  mTLS: Mesh 내부 통신 암호화                                        │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 트래픽 흐름

```
Client → ALB → Istio Gateway → VirtualService → Pod (Envoy Sidecar)
                                    │
                              (Canary Routing)
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                    v1 (90%)              v2 (10%)
```

### Istio 확인 명령어

```bash
# Gateway 확인
kubectl get gateway -A
kubectl describe gateway eco2-gateway -n istio-system

# VirtualService 확인
kubectl get virtualservice -A
kubectl describe virtualservice chat-vs -n chat

# Sidecar 주입 상태
kubectl get pods -n chat -o jsonpath='{.items[*].spec.containers[*].name}' | tr ' ' '\n' | sort -u
```

---

## Storage 구성

### StorageClass

```yaml
# gp3 StorageClass (기본)
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: gp3
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  fsType: ext4
volumeBindingMode: WaitForFirstConsumer
reclaimPolicy: Delete
```

### PVC 사용 패턴

```bash
# PVC 상태 확인
kubectl get pvc -A

# 특정 PVC 상세
kubectl describe pvc postgres-data -n postgres

# Storage 사용량
kubectl exec -n postgres postgres-0 -- df -h /var/lib/postgresql/data
```

---

## 환경별 차이

### Dev vs Prod

| 항목 | Dev | Prod |
|------|-----|------|
| Node 수 | 3 | 6+ |
| Redis | Single | Sentinel (3-node) |
| PostgreSQL | Single | RDS / HA |
| Replicas | 1 | 2-3 |
| HPA | 비활성 | 활성 |
| Resource Limits | 낮음 | 높음 |
| Network Policy | 느슨 | 엄격 |

### 환경 확인

```bash
# 환경 라벨로 리소스 조회
kubectl get pods -l environment=dev -A
kubectl get pods -l environment=prod -A

# 현재 컨텍스트 확인
kubectl config current-context
```

---

## 주요 엔드포인트

### 내부 서비스

| 서비스 | DNS | Port |
|--------|-----|------|
| chat-api | chat-api.chat.svc.cluster.local | 8000 |
| character-api | character-api.character.svc.cluster.local | 50051 (gRPC) |
| location-api | location-api.location.svc.cluster.local | 50051 (gRPC) |
| redis | redis-streams.redis.svc.cluster.local | 6379 |
| postgres | postgres.postgres.svc.cluster.local | 5432 |
| rabbitmq | rabbitmq.rabbitmq.svc.cluster.local | 5672/15672 |

### 외부 접근

```bash
# Ingress 확인
kubectl get ingress -A

# ALB 주소
kubectl get ingress -n istio-system -o jsonpath='{.items[0].status.loadBalancer.ingress[0].hostname}'
```

---

## 유용한 스크립트

### 클러스터 상태 요약

```bash
#!/bin/bash
# cluster-status.sh

echo "=== Cluster Info ==="
kubectl cluster-info

echo ""
echo "=== Node Status ==="
kubectl get nodes -o wide

echo ""
echo "=== Namespace Summary ==="
kubectl get ns -l app.kubernetes.io/part-of=ecoeco-backend

echo ""
echo "=== Pod Summary by Tier ==="
for tier in business-logic worker integration data; do
  count=$(kubectl get pods -l tier=$tier -A --no-headers 2>/dev/null | wc -l)
  echo "$tier: $count pods"
done

echo ""
echo "=== Resource Usage ==="
kubectl top nodes 2>/dev/null || echo "Metrics not available"
```

### 도메인별 상태 확인

```bash
#!/bin/bash
# domain-check.sh
DOMAIN=${1:-chat}

echo "=== $DOMAIN Domain Status ==="
echo ""
echo "## API Pod"
kubectl get pods -l domain=$DOMAIN,tier=business-logic -A -o wide

echo ""
echo "## Worker Pod"
kubectl get pods -l domain=$DOMAIN,tier=worker -A -o wide

echo ""
echo "## Services"
kubectl get svc -l domain=$DOMAIN -A

echo ""
echo "## ConfigMaps"
kubectl get configmap -l domain=$DOMAIN -A
```

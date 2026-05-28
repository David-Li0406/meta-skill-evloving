# Eco² 라벨 정책 가이드

## 라벨 체계 개요

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Eco² Kubernetes Label Hierarchy                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  app.kubernetes.io/part-of: ecoeco-backend                              │
│  ├─ tier: business-logic                                                │
│  │   ├─ domain: auth      (auth-api)                                    │
│  │   ├─ domain: chat      (chat-api)                                    │
│  │   ├─ domain: scan      (scan-api)                                    │
│  │   ├─ domain: character (character-api)                               │
│  │   └─ domain: location  (location-api)                                │
│  │                                                                       │
│  ├─ tier: worker                                                        │
│  │   ├─ domain: chat      (chat-worker)                                 │
│  │   ├─ domain: scan      (scan-worker)                                 │
│  │   └─ domain: character (character-match-worker)                      │
│  │                                                                       │
│  ├─ tier: integration                                                   │
│  │   ├─ domain: event-router                                            │
│  │   └─ domain: sse       (sse-gateway)                                 │
│  │                                                                       │
│  └─ tier: data                                                          │
│      ├─ data-type: postgres                                             │
│      └─ data-type: redis                                                │
│                                                                          │
│  app.kubernetes.io/part-of: ecoeco-platform                             │
│  └─ tier: infrastructure                                                │
│      └─ role: operators                                                 │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 표준 라벨 목록

### Pod/Deployment 라벨

| 라벨 | 필수 | 값 예시 | 설명 |
|------|------|---------|------|
| `app` | O | `chat-worker` | Pod selector (Service와 매칭) |
| `domain` | O | `chat`, `scan`, `auth` | 서비스 도메인 그룹 |
| `tier` | O | `business-logic`, `worker`, `integration`, `data` | 아키텍처 계층 |
| `version` | O | `v1`, `v2` | Canary 라우팅용 |
| `environment` | △ | `dev`, `prod` | Kustomize overlay에서 추가 |
| `release` | △ | `canary` | Canary 배포 시에만 |
| `app.kubernetes.io/part-of` | O | `ecoeco-backend` | 제품 소속 |

### Namespace 라벨

| 라벨 | 값 예시 | 설명 |
|------|---------|------|
| `istio-injection` | `enabled` | Istio 사이드카 주입 |
| `tier` | `business-logic`, `data`, `observability` | 네임스페이스 계층 |
| `role` | `api`, `messaging`, `database`, `cache` | 기능 역할 |
| `data-type` | `postgres`, `redis` | 데이터 서비스 유형 |

---

## 라벨 기반 디버깅 명령어

### 계층별 조회

```bash
# Business Logic (API 서버)
kubectl get pods -l tier=business-logic -A
kubectl get pods -l tier=business-logic,domain=chat -A

# Workers (백그라운드 작업)
kubectl get pods -l tier=worker -A
kubectl get pods -l tier=worker,domain=scan -A

# Integration (메시징/SSE)
kubectl get pods -l tier=integration -A

# Data Layer
kubectl get pods -l tier=data -A
kubectl get pods -l tier=data,data-type=redis -A
```

### 도메인별 조회

```bash
# Chat 도메인 전체 (API + Worker)
kubectl get pods -l domain=chat -A

# Scan 도메인 전체
kubectl get pods -l domain=scan -A

# Character 도메인 전체
kubectl get pods -l domain=character -A
```

### 버전/배포 상태

```bash
# Canary 배포 Pod만
kubectl get pods -l version=v2 -A
kubectl get pods -l release=canary -A

# Stable 버전만
kubectl get pods -l version=v1 -A

# 특정 도메인의 Canary
kubectl get pods -l domain=chat,version=v2 -A
```

### 환경별 조회

```bash
# Dev 환경
kubectl get pods -l environment=dev -A

# Prod 환경
kubectl get pods -l environment=prod -A

# 특정 환경의 특정 도메인
kubectl get pods -l environment=prod,domain=chat -A
```

---

## 복합 셀렉터 예시

### 문제 진단

```bash
# 재시작된 Worker Pod
kubectl get pods -l tier=worker -A -o json | \
  jq -r '.items[] | select(.status.containerStatuses[0].restartCount > 0) | .metadata.name'

# 비정상 상태 API Pod
kubectl get pods -l tier=business-logic -A --field-selector=status.phase!=Running

# Integration 계층 이벤트
kubectl get events -A --field-selector=involvedObject.kind=Pod | \
  grep -E "event-router|sse-gateway"
```

### 로그 수집

```bash
# 도메인별 로그 (stern 사용)
stern -l domain=chat -A
stern -l tier=worker -A

# 특정 계층 에러 로그
kubectl logs -l tier=integration -A --all-containers | grep -i error
```

### 리소스 모니터링

```bash
# Worker 리소스 사용량
kubectl top pods -l tier=worker -A

# API 리소스 사용량
kubectl top pods -l tier=business-logic -A
```

---

## Node Affinity 구조

모든 Deployment에 도메인 기반 Node Affinity 적용:

```yaml
spec:
  template:
    spec:
      nodeSelector:
        domain: {service-domain}    # 도메인별 노드 풀
      tolerations:
      - key: domain
        operator: Equal
        value: {service-domain}
        effect: NoSchedule
```

### Node 라벨 확인

```bash
# 노드별 도메인 라벨
kubectl get nodes --show-labels | grep domain

# 특정 도메인 노드
kubectl get nodes -l domain=chat

# 노드 리소스 상태
kubectl describe node -l domain=chat | grep -A 10 "Allocated resources"
```

---

## Istio 트래픽 라우팅

### DestinationRule Subset

```yaml
# version 라벨로 subset 정의
spec:
  subsets:
  - name: stable
    labels:
      version: v1
  - name: canary
    labels:
      version: v2
```

### 트래픽 확인

```bash
# Istio Proxy 상태
kubectl get pods -l domain=chat -A -o jsonpath='{.items[*].spec.containers[*].name}' | tr ' ' '\n' | grep istio

# VirtualService 라우팅 확인
kubectl get virtualservice -A -o yaml | grep -A 10 "subset:"
```

---

## Kustomize 라벨 적용

### Base (공통)

```yaml
# workloads/domains/{service}/base/kustomization.yaml
labels:
- includeSelectors: true
  pairs:
    app.kubernetes.io/part-of: ecoeco-backend
    domain: {service}
    tier: business-logic
```

### Overlay (환경별)

```yaml
# workloads/domains/{service}/dev/kustomization.yaml
labels:
- includeSelectors: true
  pairs:
    environment: dev
```

---

## 디버깅 스크립트

### 도메인별 상태 요약

```bash
#!/bin/bash
# domain-status.sh
DOMAIN=${1:-chat}

echo "=== $DOMAIN Domain Status ==="
echo ""
echo "## Pods"
kubectl get pods -l domain=$DOMAIN -A -o wide

echo ""
echo "## Services"
kubectl get svc -l domain=$DOMAIN -A

echo ""
echo "## Recent Events"
kubectl get events -A --field-selector=involvedObject.kind=Pod | grep -i $DOMAIN | tail -10

echo ""
echo "## Resource Usage"
kubectl top pods -l domain=$DOMAIN -A 2>/dev/null || echo "Metrics unavailable"
```

### 계층별 헬스체크

```bash
#!/bin/bash
# tier-health.sh
TIER=${1:-business-logic}

echo "=== $TIER Tier Health ==="

for pod in $(kubectl get pods -l tier=$TIER -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name} {end}'); do
  ns=$(echo $pod | cut -d'/' -f1)
  name=$(echo $pod | cut -d'/' -f2)
  status=$(kubectl get pod $name -n $ns -o jsonpath='{.status.phase}')
  restarts=$(kubectl get pod $name -n $ns -o jsonpath='{.status.containerStatuses[0].restartCount}')
  echo "$ns/$name: $status (restarts: $restarts)"
done
```

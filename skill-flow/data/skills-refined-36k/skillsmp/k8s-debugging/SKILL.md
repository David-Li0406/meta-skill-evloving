---
name: k8s-debugging
description: Kubernetes 운영/디버깅 가이드. Pod 트러블슈팅, 로그 분석, 네트워크 진단, 클러스터 구조, GitOps/ArgoCD, Operator/CRD/CR, Helm 배포 시 참조. "k8s", "kubernetes", "pod", "debug", "logs", "kubectl", "argocd", "helm", "operator", "crd" 키워드로 트리거.
---

# Kubernetes Debugging Guide

## Eco² 클러스터 개요

> **자체 관리형 K8s 클러스터** (EKS 아님)

| 항목 | 값 |
|------|-----|
| **마스터 노드** | `k8s-master` (13.209.44.249) |
| **SSH 접속** | `ssh -i ~/.ssh/sesacthon.pem ubuntu@13.209.44.249` |
| **GitOps 브랜치** | `develop` (ArgoCD가 바라보는 브랜치) |
| **이미지 레지스트리** | `docker.io/mng990/eco2:<app>-<env>-latest` |

### 배포 플로우

```
PR → develop 머지 → ArgoCD auto-sync → 클러스터 반영
```

### 주요 Namespace

| Namespace | 컴포넌트 |
|-----------|----------|
| `chat` | chat-api, chat-worker |
| `auth` | auth-api, auth-worker, ext-authz |
| `scan` | scan-api, scan-worker |
| `character` | character-api, character-grpc, character-worker |
| `location` | location-api, location-grpc |
| `rabbitmq` | RabbitMQ Cluster (eco2-rabbitmq) |
| `redis` | Redis Sentinel (rfr-streams, rfr-pubsub) |
| `postgres` | PostgreSQL |
| `event-router` | event-router (Redis Streams → Pub/Sub) |
| `sse-consumer` | sse-gateway (SSE 스트리밍) |

---

## Istio 라우팅 구조

### API Gateway

| 항목 | 값 |
|------|-----|
| **API 도메인** | `api.dev.growbin.app` |
| **Gateway** | `istio-system/eco2-gateway` |
| **인증 방식** | Cookie (`s_access`) → Header (`Authorization: Bearer`) 변환 |

### VirtualService 라우팅

| 경로 | 서비스 | Namespace |
|------|--------|-----------|
| `/api/v1/chat` | chat-api | chat |
| `/api/v1/auth` | auth-api | auth |
| `/api/v1/scan` | scan-api | scan |
| `/api/v1/character` | character-api | character |
| `/api/v1/location` | location-api | location |
| `/api/v1/users` | users-api | users |
| `/api/v1/images` | images-api | images |
| `/api/v1/info` | info-api | info |
| `/api/v1/sse` | sse-gateway | sse-consumer |

### EnvoyFilter (인증 처리)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Cookie → Header 변환 (cookie-to-header)               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Client Request                                                          │
│  ├─ Cookie: s_access=<JWT>                                              │
│  └─ Cookie: s_refresh=<JWT>                                             │
│                                                                          │
│       ↓ EnvoyFilter (Lua Script)                                        │
│                                                                          │
│  Backend Request                                                         │
│  ├─ Authorization: Bearer <JWT>                                         │
│  └─ X-Refresh-Token: Bearer <JWT>                                       │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### API 테스트 (클러스터 외부)

```bash
# JWT 토큰으로 인증된 요청
TOKEN="<JWT_TOKEN>"
curl -X POST "https://api.dev.growbin.app/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -d '{"message":"안녕하세요!"}'

# Canary 버전 테스트 (x-canary 헤더)
curl -X POST "https://api.dev.growbin.app/api/v1/chat" \
  -H "Content-Type: application/json" \
  -H "Cookie: s_access=$TOKEN" \
  -H "x-canary: true" \
  -d '{"message":"안녕하세요!"}'
```

---

## Quick Reference

### 클러스터 접속 (SSH)

```bash
# 마스터 노드 접속
./scripts/utilities/connect-ssh.sh master

# 워커 노드 접속
./scripts/utilities/connect-ssh.sh worker-1
./scripts/utilities/connect-ssh.sh worker-2

# 스토리지 노드 접속
./scripts/utilities/connect-ssh.sh storage

# 원격 명령 실행 (비인터랙티브)
ssh -i ~/.ssh/sesacthon.pem -o StrictHostKeyChecking=no ubuntu@<IP> "kubectl get nodes"
```

### 원격 클러스터 점검 (Claude Code용)

로컬에서 VPN 없이 클러스터에 접속해야 할 때 사용하는 절차.

```bash
# 1. 마스터 노드 IP 조회
MASTER_IP=$(aws ec2 describe-instances \
  --filters "Name=tag:Name,Values=k8s-master" "Name=instance-state-name,Values=running" \
  --query "Reservations[].Instances[].PublicIpAddress" \
  --output text --region ap-northeast-2)

# 2. SSH 래퍼 함수 (편의용)
k8s() {
  ssh -i ~/.ssh/sesacthon.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    ubuntu@$MASTER_IP "$@"
}

# 3. 클러스터 상태 확인
k8s "kubectl get nodes"
k8s "kubectl get pods -n <namespace> -l app=<app-name> -o wide"

# 4. 컨테이너별 상태 확인
k8s "kubectl get pod -n <ns> -l app=<app> -o jsonpath='{range .items[*].status.containerStatuses[*]}{.name}: {.state}{\"\\n\"}{end}'"

# 5. 로그 확인
k8s "kubectl logs -n <ns> deploy/<deploy-name> -c <container> --tail=50"
k8s "kubectl logs -n <ns> deploy/<deploy-name> -c <container> --previous --tail=50"

# 6. 이벤트 확인
k8s "kubectl get events -n <ns> --sort-by='.lastTimestamp' | tail -20"
```

### CI → 클러스터 반영 플로우

PR 머지 후 새 이미지를 클러스터에 반영하는 전체 절차.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Image Update Flow (kubectl 방식)                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  1. PR → develop 머지                                                    │
│     └─▶ GitHub Actions CI 트리거                                        │
│                                                                          │
│  2. CI 로그 확인 및 업데이트 대상 파악                                   │
│     ├─▶ gh run list --limit 5                                           │
│     ├─▶ gh run view <run-id> --log                                      │
│     └─▶ 빌드된 앱 목록 확인 (chat-api, chat-worker 등)                  │
│                                                                          │
│  3. ArgoCD Application 라벨로 Hard Refresh 트리거                        │
│     └─▶ kubectl label application -n argocd <app> \                     │
│           argocd.argoproj.io/refresh=hard --overwrite                   │
│                                                                          │
│  4. Deployment 삭제 (Self-Heal 트리거)                                   │
│     └─▶ kubectl delete deploy <name> -n <namespace>                     │
│                                                                          │
│  5. Pod 재생성 확인                                                      │
│     └─▶ kubectl rollout status deploy/<name> -n <ns> --timeout=120s    │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Step 1-2: CI 로그 확인 (로컬에서)

```bash
# 최근 CI 실행 목록 확인
gh run list --limit 5

# 특정 실행의 상세 정보 및 빌드된 앱 확인
gh run view <run-id>

# 로그에서 빌드된 이미지 확인
gh run view <run-id> --log | grep -E "Successfully built|Pushing|docker.io/mng990"

# jobs 확인 (어떤 앱이 빌드되었는지)
gh run view <run-id> --json jobs --jq '.jobs[] | select(.conclusion=="success") | .name'
```

#### Step 3-5: 클러스터 반영 (마스터 노드에서)

```bash
# SSH 접속
ssh -i ~/.ssh/sesacthon.pem ubuntu@13.209.44.249

# ArgoCD Application 라벨로 Hard Refresh (빌드된 앱만)
kubectl label application -n argocd dev-api-chat argocd.argoproj.io/refresh=hard --overwrite
kubectl label application -n argocd dev-chat-worker argocd.argoproj.io/refresh=hard --overwrite

# Deployment 삭제 (Self-Heal로 새 이미지 Pull)
kubectl delete deploy chat-api -n chat
kubectl delete deploy chat-worker -n chat

# Pod 재생성 대기
kubectl rollout status deploy/chat-api -n chat --timeout=120s
kubectl rollout status deploy/chat-worker -n chat --timeout=120s

# 새 이미지 digest 확인
kubectl get pods -n chat -o jsonpath='{range .items[*]}{.metadata.name}: {.status.containerStatuses[0].imageID}{"\n"}{end}'
```

#### ArgoCD Application 이름 규칙

| 앱 | ArgoCD Application | Namespace |
|----|-------------------|-----------|
| chat-api | `dev-api-chat` | chat |
| chat-worker | `dev-chat-worker` | chat |
| scan-api | `dev-api-scan` | scan |
| scan-worker | `dev-scan-worker` | scan |
| auth-api | `dev-api-auth` | auth |
| character-api | `dev-api-character` | character |
| location-api | `dev-api-location` | location |

#### 왜 Deployment를 삭제하는가?

- 이미지 태그가 `latest`이므로 digest가 바뀌어도 태그는 동일
- ArgoCD는 매니페스트 기준이라 이미지 태그만 보면 변경 없음
- Deployment 삭제 → Self-Heal 활성화 시 ArgoCD가 재생성 → 새 이미지 Pull

### Pod 상태 확인

```bash
# Pod 목록 (상태 포함)
kubectl get pods -n eco2

# Pod 상세 정보 (이벤트 포함)
kubectl describe pod <pod-name> -n eco2

# Pod 로그
kubectl logs <pod-name> -n eco2 --tail=100 -f

# 이전 컨테이너 로그 (재시작된 경우)
kubectl logs <pod-name> -n eco2 --previous
```

### 일반적인 문제 진단

```bash
# CrashLoopBackOff
kubectl logs <pod-name> -n eco2 --previous
kubectl describe pod <pod-name> -n eco2 | grep -A 10 "Events:"

# ImagePullBackOff
kubectl describe pod <pod-name> -n eco2 | grep -A 5 "Image:"

# Pending 상태
kubectl describe pod <pod-name> -n eco2 | grep -A 10 "Events:"
kubectl get events -n eco2 --sort-by='.lastTimestamp'
```

### 실시간 디버깅

```bash
# Pod 내부 쉘 접속
kubectl exec -it <pod-name> -n eco2 -- /bin/sh

# 특정 컨테이너 접속 (multi-container)
kubectl exec -it <pod-name> -c <container-name> -n eco2 -- /bin/sh

# 임시 디버그 컨테이너
kubectl debug -it <pod-name> -n eco2 --image=busybox
```

## Eco² 라벨 정책

### 핵심 라벨

| 라벨 | 값 | 용도 |
|------|-----|------|
| `app` | 서비스명 | Pod selector |
| `domain` | `auth`, `chat`, `scan`, `character`, `location` | 서비스 도메인 |
| `tier` | `business-logic`, `worker`, `integration`, `data` | 아키텍처 계층 |
| `version` | `v1`, `v2` | Canary/Istio 라우팅 |
| `environment` | `dev`, `prod` | 환경 구분 |

### 라벨 기반 조회 (자주 사용)

```bash
# 계층별 조회
kubectl get pods -l tier=business-logic -A    # API 서비스
kubectl get pods -l tier=worker -A            # 워커
kubectl get pods -l tier=integration -A       # Event Router, SSE
kubectl get pods -l tier=data -A              # Redis, PostgreSQL

# 도메인별 조회
kubectl get pods -l domain=chat -A            # Chat 관련 전체
kubectl get pods -l domain=scan -A            # Scan 관련 전체
kubectl get pods -l domain=character -A       # Character 서비스

# Canary 배포 확인
kubectl get pods -l version=v2 -A             # Canary 버전만

# 환경별 조회
kubectl get pods -l environment=dev -A
kubectl get pods -l environment=prod -A
```

## Eco² 컴포넌트

| 컴포넌트 | Namespace | tier | domain |
|----------|-----------|------|--------|
| chat-api | chat | business-logic | chat |
| chat-worker | chat | worker | chat |
| event-router | event-router | integration | event-router |
| sse-gateway | sse-consumer | integration | sse |
| character-api | character | business-logic | character |
| location-api | location | business-logic | location |
| scan-api | scan | business-logic | scan |
| scan-worker | scan | worker | scan |
| auth-api | auth | business-logic | auth |

## Reference Files

### 디버깅
- **Pod 트러블슈팅**: See [pod-troubleshooting.md](./references/pod-troubleshooting.md)
- **로그 분석**: See [log-analysis.md](./references/log-analysis.md)
- **네트워크 진단**: See [network-diagnosis.md](./references/network-diagnosis.md)
- **라벨 정책**: See [label-policies.md](./references/label-policies.md)

### 인프라/배포
- **클러스터 구조**: See [cluster-architecture.md](./references/cluster-architecture.md)
- **GitOps/ArgoCD**: See [gitops-argocd.md](./references/gitops-argocd.md)
- **Operator/CRD/CR**: See [operators-crd.md](./references/operators-crd.md)
- **Helm 배포**: See [helm-deployment.md](./references/helm-deployment.md)

## 자주 사용하는 명령어

```bash
# 전체 리소스 상태
kubectl get all -n eco2

# 최근 이벤트
kubectl get events -n eco2 --sort-by='.lastTimestamp' | tail -20

# 리소스 사용량
kubectl top pods -n eco2

# ConfigMap/Secret 확인
kubectl get configmap -n eco2
kubectl get secret -n eco2
```

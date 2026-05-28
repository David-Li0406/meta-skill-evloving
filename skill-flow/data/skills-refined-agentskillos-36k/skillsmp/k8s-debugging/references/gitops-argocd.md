# GitOps / ArgoCD 가이드

## GitOps 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GitOps Workflow                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐        │
│  │   Git    │─────▶│  ArgoCD  │─────▶│   Sync   │─────▶│  K8s     │        │
│  │  (SSOT)  │      │  (Watch) │      │ (Apply)  │      │ Cluster  │        │
│  └──────────┘      └──────────┘      └──────────┘      └──────────┘        │
│       ▲                                                      │              │
│       │                                                      │              │
│       └──────────────── Health Check ◀───────────────────────┘              │
│                                                                              │
│  SSOT = Single Source of Truth                                              │
│  Git 리포지토리가 클러스터 상태의 유일한 진실                               │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ArgoCD App-of-Apps 패턴

### 구조

```
clusters/
├── dev/
│   └── apps/
│       ├── 02-namespaces.yaml          # Wave 02: Namespace
│       ├── 03-rbac-storage.yaml        # Wave 03: RBAC, StorageClass
│       ├── 06-network-policies.yaml    # Wave 06: NetworkPolicy
│       ├── 11-external-secrets.yaml    # Wave 11: ExternalSecret
│       ├── 15-prometheus.yaml          # Wave 15: Prometheus Operator
│       ├── 20-data-operators.yaml      # Wave 20: Redis/PostgreSQL Operator
│       ├── 30-data-cr.yaml             # Wave 30: Data Custom Resources
│       ├── 60-apis-appset.yaml         # Wave 60: API Deployments
│       └── 70-ingress.yaml             # Wave 70: Ingress/Routing
└── prod/
    └── apps/
        └── ... (동일 구조)
```

### App-of-Apps 확인

```bash
# Root Application 확인
argocd app list
argocd app get root-app

# Child Applications 확인
argocd app list --project default

# 특정 App 상태
argocd app get namespaces-dev
argocd app get chat-api-dev
```

---

## Sync Wave 전략

### Wave 순서

| Wave | 리소스 | 설명 |
|------|--------|------|
| 02 | Namespaces | 모든 Namespace 생성 |
| 03 | RBAC/Storage | ServiceAccount, Role, StorageClass |
| 06 | NetworkPolicy | 네트워크 정책 적용 |
| 11 | ExternalSecret | AWS SSM → K8s Secret 동기화 |
| 15 | Prometheus | Monitoring Stack |
| 20 | Data Operators | Redis/PostgreSQL Operator 설치 |
| 30 | Data CRs | 데이터베이스 인스턴스 생성 |
| 60 | APIs | 비즈니스 API/Worker Deployment |
| 70 | Ingress | 외부 라우팅 설정 |

### Wave 어노테이션

```yaml
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: "60"
```

### Sync 순서 확인

```bash
# Sync 순서대로 정렬
argocd app list -o json | jq -r '.items | sort_by(.metadata.annotations["argocd.argoproj.io/sync-wave"] // "99") | .[] | "\(.metadata.annotations["argocd.argoproj.io/sync-wave"] // "99")\t\(.metadata.name)"'
```

---

## 배포 흐름

### 코드 변경 → 배포

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Deployment Pipeline                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. PR Merge                                                                 │
│     └─▶ develop 브랜치에 코드 병합 (ArgoCD가 바라보는 브랜치)               │
│                                                                              │
│  2. CI (GitHub Actions)                                                      │
│     └─▶ Test → Build → Push Image (ECR)                                     │
│                                                                              │
│  3. Image Tag Update                                                         │
│     └─▶ workloads/domains/<domain>/prod/patch-deployment.yaml               │
│         image: 123456789.dkr.ecr.ap-northeast-2.amazonaws.com/app:v1.2.3    │
│                                                                              │
│  4. ArgoCD Sync                                                              │
│     └─▶ 자동 또는 수동 Sync로 클러스터 반영                                 │
│                                                                              │
│  5. Rollout                                                                  │
│     └─▶ Rolling Update / Canary 배포                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 배포 명령어

```bash
# 수동 Sync
argocd app sync chat-api-prod

# Diff 확인 (적용 전 변경사항)
argocd app diff chat-api-prod

# 강제 Sync (OutOfSync 무시)
argocd app sync chat-api-prod --force

# Prune (삭제된 리소스 제거)
argocd app sync chat-api-prod --prune

# Hard Refresh (캐시 무시)
argocd app get chat-api-prod --hard-refresh
```

---

## ArgoCD 상태 관리

### Application 상태

| 상태 | 의미 | 조치 |
|------|------|------|
| Synced | Git과 클러스터 동일 | 정상 |
| OutOfSync | Git과 클러스터 다름 | Sync 필요 |
| Unknown | 상태 확인 불가 | 네트워크/권한 확인 |
| Healthy | 모든 리소스 정상 | 정상 |
| Progressing | 배포 진행 중 | 대기 |
| Degraded | 일부 리소스 비정상 | 로그 확인 |
| Missing | 리소스 누락 | Sync 필요 |

### 상태 확인 명령어

```bash
# 전체 App 상태
argocd app list

# 특정 App 상세 상태
argocd app get chat-worker-prod

# 리소스별 상태
argocd app resources chat-worker-prod

# 이벤트/히스토리
argocd app history chat-worker-prod
```

---

## Kustomize 통합

### 디렉토리 구조

```
workloads/
├── domains/
│   └── chat/
│       ├── base/
│       │   ├── kustomization.yaml
│       │   ├── deployment.yaml
│       │   ├── service.yaml
│       │   └── configmap.yaml
│       ├── dev/
│       │   ├── kustomization.yaml      # base 참조 + dev 패치
│       │   └── patch-deployment.yaml
│       └── prod/
│           ├── kustomization.yaml      # base 참조 + prod 패치
│           ├── patch-deployment.yaml
│           └── patch-configmap.yaml
```

### Kustomize 검증

```bash
# 로컬에서 빌드 테스트
kustomize build workloads/domains/chat/dev
kustomize build workloads/domains/chat/prod

# Diff 확인
kustomize build workloads/domains/chat/prod | kubectl diff -f -

# ArgoCD가 사용하는 매니페스트 확인
argocd app manifests chat-api-prod
```

---

## 트러블슈팅

### Sync 실패

```bash
# Sync 에러 확인
argocd app get <app-name> -o json | jq '.status.conditions'

# 상세 로그
argocd app logs <app-name>

# 리소스별 상태
argocd app resources <app-name> --tree

# 일반적인 원인
# 1. Kustomization 오류 → kustomize build로 로컬 검증
# 2. 리소스 충돌 → kubectl describe로 이벤트 확인
# 3. 권한 부족 → RBAC 확인
# 4. Webhook 실패 → admission webhook 로그 확인
```

### OutOfSync 해결

```bash
# Diff 확인
argocd app diff <app-name>

# 수동 변경 리셋 (Git 상태로 복원)
argocd app sync <app-name> --prune --force

# 특정 리소스만 Sync
argocd app sync <app-name> --resource deployment:chat-api
```

### Rollback

```bash
# 히스토리 확인
argocd app history <app-name>

# 특정 버전으로 롤백
argocd app rollback <app-name> <revision>

# Kubernetes 레벨 롤백
kubectl rollout undo deployment/chat-api -n chat
```

---

## Webhook 설정

### GitHub Webhook

```yaml
# workloads/secrets/external-secrets/dev/argocd-webhook-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: argocd-webhook-secret
  namespace: argocd
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-ssm-store
    kind: ClusterSecretStore
  target:
    name: argocd-webhook-secret
  data:
  - secretKey: webhook.github.secret
    remoteRef:
      key: /ecoeco/argocd/webhook-secret
```

### Webhook 확인

```bash
# Secret 존재 확인
kubectl get secret argocd-webhook-secret -n argocd

# ArgoCD Server 로그 (webhook 수신)
kubectl logs -l app.kubernetes.io/name=argocd-server -n argocd | grep webhook
```

---

## 유용한 스크립트

### 전체 App 상태 요약

```bash
#!/bin/bash
# argocd-status.sh

echo "=== ArgoCD Applications Status ==="
argocd app list -o wide

echo ""
echo "=== OutOfSync Apps ==="
argocd app list -o json | jq -r '.items[] | select(.status.sync.status != "Synced") | .metadata.name'

echo ""
echo "=== Unhealthy Apps ==="
argocd app list -o json | jq -r '.items[] | select(.status.health.status != "Healthy") | "\(.metadata.name): \(.status.health.status)"'
```

### 특정 도메인 배포

```bash
#!/bin/bash
# deploy-domain.sh
DOMAIN=${1:-chat}
ENV=${2:-dev}

echo "=== Deploying $DOMAIN to $ENV ==="

# Diff 확인
echo "## Checking diff..."
argocd app diff ${DOMAIN}-api-${ENV}

# 사용자 확인
read -p "Proceed with sync? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  argocd app sync ${DOMAIN}-api-${ENV}
  argocd app wait ${DOMAIN}-api-${ENV} --timeout 300
  echo "## Deployment complete"
fi
```

---

## 새 이미지 배포 (Self-Heal 방식)

CI에서 새 이미지가 푸시된 후 Pod를 업데이트하는 절차.

### 배포 흐름

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Image Update via Self-Heal                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. CI Pipeline                                                              │
│     └─▶ 새 이미지 빌드 & Push (docker.io/mng990/eco2:<tag>)                 │
│                                                                              │
│  2. ArgoCD Image Updater                                                     │
│     └─▶ 새 이미지 digest 감지 (digest strategy)                             │
│                                                                              │
│  3. ArgoCD Sync                                                              │
│     └─▶ argocd app sync <app-name> --force                                  │
│                                                                              │
│  4. Deployment 삭제                                                          │
│     └─▶ kubectl delete deploy <name> -n <namespace>                         │
│                                                                              │
│  5. Self-Heal                                                                │
│     └─▶ ArgoCD가 Deployment 재생성 (새 이미지로)                            │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 명령어

```bash
# 1. ArgoCD Sync (Image Updater가 감지한 새 이미지 반영)
argocd app sync dev-api-info --force

# 2. Deployment 삭제 (Self-Heal 트리거)
kubectl delete deploy info-api -n info

# 3. Pod 재생성 확인
kubectl get pods -n info -w

# 4. 새 이미지 확인
kubectl get deploy info-api -n info -o jsonpath='{.spec.template.spec.containers[0].image}'
```

### 전제 조건

ArgoCD Application에 Self-Heal이 활성화되어 있어야 함:

```yaml
# ApplicationSet 또는 Application
spec:
  syncPolicy:
    automated:
      selfHeal: true    # 필수: 클러스터 상태가 Git과 다르면 자동 복구
      prune: true       # 선택: Git에서 삭제된 리소스 자동 제거
```

### Worker 배포 예시

```bash
# info-worker 새 버전 배포
argocd app sync dev-info-worker --force
kubectl delete deploy info-worker -n info
kubectl get pods -n info -l app=info-worker -w
```

### 주의사항

- Self-Heal이 비활성화되어 있으면 Deployment가 재생성되지 않음
- `--force` 없이 sync하면 이미 Synced 상태라 변경사항 미적용 가능
- 삭제 후 Pod가 재생성될 때까지 서비스 다운타임 발생 (Rolling Update 아님)

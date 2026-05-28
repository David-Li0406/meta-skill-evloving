# Helm 배포 가이드

## Helm 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Helm Architecture                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────────┐     ┌────────────────┐     ┌────────────────┐          │
│  │  Chart (Repo)  │────▶│  Values.yaml   │────▶│  K8s Manifests │          │
│  │  (Template)    │     │  (Parameters)  │     │  (Rendered)    │          │
│  └────────────────┘     └────────────────┘     └────────────────┘          │
│                                                                              │
│  Chart: 애플리케이션 패키지 (템플릿 + 기본값)                               │
│  Values: 환경별 설정값                                                       │
│  Release: 클러스터에 설치된 Chart 인스턴스                                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Eco² Helm Charts

### 사용 중인 Charts

| Chart | Repository | 용도 |
|-------|------------|------|
| **kube-prometheus-stack** | prometheus-community | Prometheus + Grafana + Alertmanager |
| **grafana** | grafana | Grafana 대시보드 |
| **external-dns** | bitnami | Route53 DNS 자동 관리 |
| **aws-load-balancer-controller** | eks | ALB Ingress Controller |
| **external-secrets** | external-secrets | AWS SSM → K8s Secret |
| **cert-manager** | jetstack | TLS 인증서 자동화 |

### Values 파일 위치

```
ci-artifacts/
└── helm/
    ├── kube-prometheus-stack-dev.yaml
    ├── kube-prometheus-stack-prod.yaml
    ├── grafana-dev.yaml
    ├── grafana-prod.yaml
    ├── external-dns-dev.yaml
    ├── external-dns-prod.yaml
    ├── alb-controller-dev.yaml
    └── alb-controller-prod.yaml
```

---

## ArgoCD + Helm 통합

### Application 정의

```yaml
# clusters/dev/apps/15-prometheus.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prometheus-dev
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://prometheus-community.github.io/helm-charts
    chart: kube-prometheus-stack
    targetRevision: 56.21.1
    helm:
      valueFiles:
      - values.yaml  # Chart 기본값
      values: |
        # 인라인 오버라이드
        prometheus:
          prometheusSpec:
            retention: 7d
  destination:
    server: https://kubernetes.default.svc
    namespace: prometheus
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### CI Values 파일 참조

```yaml
# ArgoCD Application에서 로컬 values 파일 참조
spec:
  source:
    repoURL: https://github.com/eco2-team/backend.git
    path: ci-artifacts/helm
    targetRevision: main
    helm:
      valueFiles:
      - kube-prometheus-stack-dev.yaml
```

---

## Helm 명령어

### 기본 명령어

```bash
# Repository 추가
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Chart 검색
helm search repo prometheus
helm search repo kube-prometheus-stack --versions

# Chart 정보 확인
helm show values prometheus-community/kube-prometheus-stack > default-values.yaml
helm show chart prometheus-community/kube-prometheus-stack
```

### Release 관리

```bash
# 설치된 Release 확인
helm list -A
helm list -n prometheus

# Release 상세
helm status prometheus -n prometheus
helm get values prometheus -n prometheus

# Release 히스토리
helm history prometheus -n prometheus
```

### 설치/업그레이드

```bash
# 설치 (ArgoCD 없이 직접)
helm install prometheus prometheus-community/kube-prometheus-stack \
  -n prometheus \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml

# 업그레이드
helm upgrade prometheus prometheus-community/kube-prometheus-stack \
  -n prometheus \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml

# Dry-run (테스트)
helm upgrade prometheus prometheus-community/kube-prometheus-stack \
  -n prometheus \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml \
  --dry-run --debug
```

### 롤백

```bash
# 롤백
helm rollback prometheus 1 -n prometheus

# 삭제
helm uninstall prometheus -n prometheus
```

---

## Values 파일 관리

### 환경별 Values 구조

```yaml
# ci-artifacts/helm/kube-prometheus-stack-dev.yaml

# 공통 설정
commonLabels:
  environment: dev
  app.kubernetes.io/part-of: ecoeco-platform

# Prometheus 설정
prometheus:
  prometheusSpec:
    retention: 3d                    # Dev: 3일 보관
    resources:
      limits:
        cpu: "1"
        memory: 2Gi
      requests:
        cpu: "500m"
        memory: 1Gi
    storageSpec:
      volumeClaimTemplate:
        spec:
          storageClassName: gp3
          resources:
            requests:
              storage: 20Gi         # Dev: 20Gi

# Grafana 설정
grafana:
  enabled: true
  adminPassword: admin              # Dev only
  persistence:
    enabled: true
    size: 5Gi

# Alertmanager 설정
alertmanager:
  enabled: true
  alertmanagerSpec:
    resources:
      limits:
        cpu: "200m"
        memory: 256Mi
```

```yaml
# ci-artifacts/helm/kube-prometheus-stack-prod.yaml (차이점)

prometheus:
  prometheusSpec:
    retention: 30d                   # Prod: 30일 보관
    replicas: 2                      # HA
    resources:
      limits:
        cpu: "2"
        memory: 8Gi
    storageSpec:
      volumeClaimTemplate:
        spec:
          resources:
            requests:
              storage: 100Gi        # Prod: 100Gi

grafana:
  adminPassword: ""                 # Secret 참조
  persistence:
    size: 20Gi
```

### Values 검증

```bash
# Values 파일 문법 검증
helm lint prometheus-community/kube-prometheus-stack \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml

# 렌더링된 매니페스트 확인
helm template prometheus prometheus-community/kube-prometheus-stack \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml \
  --debug > rendered.yaml

# 특정 템플릿만 확인
helm template prometheus prometheus-community/kube-prometheus-stack \
  -f ci-artifacts/helm/kube-prometheus-stack-dev.yaml \
  -s templates/prometheus/prometheus.yaml
```

---

## 트러블슈팅

### Helm Release 문제

```bash
# Release 상태 확인
helm status <release> -n <namespace>

# 실패한 Release 확인
helm list -A --failed

# 보류 중인 설치 정리
helm list -A --pending
helm delete <release> -n <namespace> --no-hooks
```

### Values 디버깅

```bash
# 적용된 Values 확인
helm get values <release> -n <namespace> -a  # 모든 값
helm get values <release> -n <namespace>     # 사용자 정의 값만

# Values 병합 순서 확인
# 1. Chart defaults (values.yaml)
# 2. Parent chart values
# 3. User supplied values (-f file.yaml)
# 4. Inline values (--set)

# 특정 값 확인
helm get values prometheus -n prometheus -o json | jq '.prometheus.prometheusSpec.retention'
```

### 매니페스트 확인

```bash
# 모든 리소스 확인
helm get manifest <release> -n <namespace>

# 특정 리소스 필터
helm get manifest prometheus -n prometheus | grep -A 20 "kind: Prometheus"

# ArgoCD에서 렌더링된 매니페스트
argocd app manifests prometheus-dev
```

### 업그레이드 실패

```bash
# 롤백
helm rollback <release> <revision> -n <namespace>

# 강제 업그레이드 (주의)
helm upgrade <release> <chart> -n <namespace> \
  -f values.yaml \
  --force \
  --cleanup-on-fail

# 히스토리 확인 후 특정 버전으로
helm history <release> -n <namespace>
helm rollback <release> 3 -n <namespace>
```

---

## CI/CD 통합

### GitHub Actions에서 Helm 사용

```yaml
# .github/workflows/helm-lint.yaml
name: Helm Lint
on:
  pull_request:
    paths:
      - 'ci-artifacts/helm/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup Helm
      uses: azure/setup-helm@v3

    - name: Add repos
      run: |
        helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
        helm repo update

    - name: Lint values
      run: |
        for f in ci-artifacts/helm/*.yaml; do
          chart=$(echo $f | sed 's/-dev.yaml//' | sed 's/-prod.yaml//' | xargs basename)
          helm lint prometheus-community/$chart -f $f || true
        done
```

### Values 파일 CI 검증

```bash
#!/bin/bash
# scripts/validate-helm-values.sh

CHARTS=(
  "kube-prometheus-stack:prometheus-community"
  "grafana:grafana"
  "external-dns:bitnami"
)

for item in "${CHARTS[@]}"; do
  chart=$(echo $item | cut -d: -f1)
  repo=$(echo $item | cut -d: -f2)

  for env in dev prod; do
    values_file="ci-artifacts/helm/${chart}-${env}.yaml"
    if [ -f "$values_file" ]; then
      echo "Validating $values_file..."
      helm template test $repo/$chart -f $values_file > /dev/null
      if [ $? -eq 0 ]; then
        echo "  OK"
      else
        echo "  FAILED"
        exit 1
      fi
    fi
  done
done
```

---

## 유용한 스크립트

### Release 상태 요약

```bash
#!/bin/bash
# helm-status.sh

echo "=== Helm Releases ==="
helm list -A -o json | jq -r '.[] | "\(.namespace)/\(.name)\t\(.chart)\t\(.status)"' | column -t

echo ""
echo "=== Failed/Pending Releases ==="
helm list -A --failed --pending
```

### Chart 버전 확인

```bash
#!/bin/bash
# check-chart-versions.sh

echo "=== Installed vs Latest Versions ==="

# 설치된 Release 목록
helm list -A -o json | jq -r '.[] | "\(.name)\t\(.chart)"' | while read name chart; do
  chart_name=$(echo $chart | sed 's/-[0-9].*//')
  installed_ver=$(echo $chart | grep -oP '\d+\.\d+\.\d+')

  # 최신 버전 조회
  latest_ver=$(helm search repo $chart_name --versions -o json 2>/dev/null | jq -r '.[0].version')

  if [ "$installed_ver" != "$latest_ver" ]; then
    echo "UPGRADE AVAILABLE: $name ($chart_name) $installed_ver -> $latest_ver"
  else
    echo "UP TO DATE: $name ($chart_name) $installed_ver"
  fi
done
```

### Values Diff (Dev vs Prod)

```bash
#!/bin/bash
# values-diff.sh
CHART=${1:-kube-prometheus-stack}

echo "=== $CHART: Dev vs Prod Differences ==="
diff -u \
  ci-artifacts/helm/${CHART}-dev.yaml \
  ci-artifacts/helm/${CHART}-prod.yaml \
  | grep -E '^[-+]' | grep -v '^[-+]{3}'
```

---

## Best Practices

### 1. Values 파일 구조화

```yaml
# 공통 설정은 상단에
global:
  imageRegistry: 123456789.dkr.ecr.ap-northeast-2.amazonaws.com

# 환경별 설정은 명확히 분리
# dev: 낮은 리소스, 짧은 retention
# prod: 높은 리소스, HA, 긴 retention
```

### 2. Chart 버전 고정

```yaml
# ArgoCD Application에서 버전 명시
spec:
  source:
    chart: kube-prometheus-stack
    targetRevision: 56.21.1  # 버전 고정 (56.x.x가 아닌 정확한 버전)
```

### 3. Secret 관리

```yaml
# Values에 직접 비밀 넣지 않기
grafana:
  adminPassword: ""  # ExternalSecret 또는 SealedSecret 사용

# 또는 existingSecret 참조
grafana:
  admin:
    existingSecret: grafana-admin-secret
    userKey: admin-user
    passwordKey: admin-password
```

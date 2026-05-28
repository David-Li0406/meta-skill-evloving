# Operator / CRD / CR 가이드

## Operator 패턴 개요

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Kubernetes Operator Pattern                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐                    │
│  │    CRD     │─────▶│     CR     │─────▶│  Operator  │                    │
│  │ (Schema)   │      │ (Instance) │      │ (Controller)│                   │
│  └────────────┘      └────────────┘      └────────────┘                    │
│                                                 │                           │
│                                                 ▼                           │
│                                          ┌────────────┐                    │
│                                          │  Native    │                    │
│                                          │ Resources  │                    │
│                                          │ (Pod, Svc) │                    │
│                                          └────────────┘                    │
│                                                                              │
│  CRD: Custom Resource Definition (리소스 스키마 정의)                       │
│  CR:  Custom Resource (실제 인스턴스)                                       │
│  Operator: CR을 watch하고 native 리소스 관리                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Eco² 클러스터의 Operators

### 설치된 Operators

| Operator | Namespace | CRD | 용도 |
|----------|-----------|-----|------|
| **External Secrets** | external-secrets | ExternalSecret, ClusterSecretStore | AWS SSM → K8s Secret |
| **Prometheus Operator** | prometheus | Prometheus, ServiceMonitor, AlertmanagerConfig | 모니터링 |
| **Cert Manager** | cert-manager | Certificate, ClusterIssuer | TLS 인증서 |
| **Redis Operator** | redis-system | RedisCluster, RedisSentinel | Redis HA 관리 |
| **PostgreSQL Operator** | postgres-system | Postgresql | PostgreSQL HA 관리 |

### Operator 상태 확인

```bash
# Operator Pod 상태
kubectl get pods -n external-secrets
kubectl get pods -n prometheus
kubectl get pods -n cert-manager

# CRD 목록
kubectl get crd | grep -E 'external|prometheus|cert|redis|postgres'

# Operator 로그
kubectl logs -l app.kubernetes.io/name=external-secrets -n external-secrets
```

---

## External Secrets Operator

### 구조

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        External Secrets Flow                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────┐                     ┌─────────────────┐               │
│  │  AWS SSM        │                     │  AWS Secrets    │               │
│  │  Parameter Store│                     │  Manager        │               │
│  └────────┬────────┘                     └────────┬────────┘               │
│           │                                       │                         │
│           └───────────────┬───────────────────────┘                         │
│                           ▼                                                  │
│                 ┌─────────────────────┐                                     │
│                 │ ClusterSecretStore  │  (인증 정보)                        │
│                 │ aws-ssm-store       │                                     │
│                 └──────────┬──────────┘                                     │
│                            │                                                 │
│                            ▼                                                 │
│                 ┌─────────────────────┐                                     │
│                 │   ExternalSecret    │  (매핑 정의)                        │
│                 │   chat-api-secrets  │                                     │
│                 └──────────┬──────────┘                                     │
│                            │                                                 │
│                            ▼                                                 │
│                 ┌─────────────────────┐                                     │
│                 │   Kubernetes Secret │  (자동 생성)                        │
│                 │   chat-api-secrets  │                                     │
│                 └─────────────────────┘                                     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### ClusterSecretStore

```yaml
# workloads/secrets/external-secrets/base/cluster-secret-store.yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-ssm-store
spec:
  provider:
    aws:
      service: ParameterStore
      region: ap-northeast-2
      auth:
        secretRef:
          accessKeyIDSecretRef:
            name: aws-global-credentials
            namespace: kube-system
            key: aws_access_key_id
          secretAccessKeySecretRef:
            name: aws-global-credentials
            namespace: kube-system
            key: aws_secret_access_key
```

### ExternalSecret 예시

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: chat-api-secrets
  namespace: chat
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-ssm-store
    kind: ClusterSecretStore
  target:
    name: chat-api-secrets  # 생성될 K8s Secret 이름
  data:
  - secretKey: OPENAI_API_KEY
    remoteRef:
      key: /ecoeco/prod/openai-api-key
  - secretKey: DATABASE_URL
    remoteRef:
      key: /ecoeco/prod/database-url
```

### 디버깅 명령어

```bash
# ExternalSecret 상태
kubectl get externalsecret -A
kubectl describe externalsecret chat-api-secrets -n chat

# 동기화 상태 확인
kubectl get externalsecret chat-api-secrets -n chat -o jsonpath='{.status.conditions}'

# 생성된 Secret 확인
kubectl get secret chat-api-secrets -n chat
kubectl get secret chat-api-secrets -n chat -o jsonpath='{.data.OPENAI_API_KEY}' | base64 -d

# Operator 로그 (동기화 에러)
kubectl logs -l app.kubernetes.io/name=external-secrets -n external-secrets | grep -i error
```

---

## Prometheus Operator

### 주요 CRD

| CRD | 용도 | 예시 |
|-----|------|------|
| Prometheus | Prometheus 서버 인스턴스 | 스크래핑 설정, 스토리지 |
| ServiceMonitor | 서비스 메트릭 수집 대상 | chat-api 메트릭 |
| PodMonitor | Pod 직접 메트릭 수집 | Sidecar 없는 Pod |
| AlertmanagerConfig | 알림 규칙 | Slack 알림 |
| PrometheusRule | PromQL 알림 규칙 | CPU 80% 초과 |

### ServiceMonitor 예시

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: chat-api-monitor
  namespace: prometheus
spec:
  selector:
    matchLabels:
      app: chat-api
  namespaceSelector:
    matchNames:
    - chat
  endpoints:
  - port: metrics
    interval: 30s
    path: /metrics
```

### 디버깅 명령어

```bash
# ServiceMonitor 확인
kubectl get servicemonitor -A
kubectl describe servicemonitor chat-api-monitor -n prometheus

# Prometheus 타겟 상태
kubectl port-forward svc/prometheus 9090:9090 -n prometheus
# 브라우저: http://localhost:9090/targets

# Prometheus Operator 로그
kubectl logs -l app.kubernetes.io/name=prometheus-operator -n prometheus

# PrometheusRule 문법 검증
kubectl get prometheusrule -A
promtool check rules /path/to/rules.yaml
```

---

## Cert Manager

### 주요 CRD

| CRD | 용도 |
|-----|------|
| ClusterIssuer | 클러스터 전역 인증서 발급자 |
| Issuer | 네임스페이스별 인증서 발급자 |
| Certificate | 인증서 요청 |

### Certificate 예시

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: eco2-tls
  namespace: istio-system
spec:
  secretName: eco2-tls-secret
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.eco2.app
  - '*.eco2.app'
```

### 디버깅 명령어

```bash
# Certificate 상태
kubectl get certificate -A
kubectl describe certificate eco2-tls -n istio-system

# 인증서 갱신 상태
kubectl get certificaterequest -A

# Cert Manager 로그
kubectl logs -l app=cert-manager -n cert-manager

# 인증서 내용 확인
kubectl get secret eco2-tls-secret -n istio-system -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
```

---

## Redis Operator (예시)

### RedisCluster CR

```yaml
apiVersion: redis.redis.opstreelabs.in/v1beta1
kind: RedisCluster
metadata:
  name: redis-streams
  namespace: redis
spec:
  clusterSize: 3
  kubernetesConfig:
    image: redis:7.2-alpine
    resources:
      limits:
        cpu: "1"
        memory: 2Gi
  storage:
    volumeClaimTemplate:
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 10Gi
  redisExporter:
    enabled: true
```

### 디버깅 명령어

```bash
# Redis CR 상태
kubectl get rediscluster -A
kubectl describe rediscluster redis-streams -n redis

# 생성된 Pod 확인
kubectl get pods -l app=redis-streams -n redis

# Redis 연결 테스트
kubectl exec -it redis-streams-leader-0 -n redis -- redis-cli ping
```

---

## CR 관리 Best Practices

### 1. CR 변경 전 백업

```bash
# CR 백업
kubectl get externalsecret chat-api-secrets -n chat -o yaml > backup-externalsecret.yaml

# 변경 후 diff 확인
kubectl diff -f updated-externalsecret.yaml
```

### 2. CR 상태 모니터링

```bash
# 모든 CR 상태 요약
for crd in externalsecret servicemonitor certificate; do
  echo "=== $crd ==="
  kubectl get $crd -A -o wide 2>/dev/null || echo "Not found"
done
```

### 3. Operator 버전 관리

```bash
# Operator 버전 확인
kubectl get deployment -n external-secrets -o jsonpath='{.items[0].spec.template.spec.containers[0].image}'

# CRD 버전 확인
kubectl get crd externalsecrets.external-secrets.io -o jsonpath='{.spec.versions[*].name}'
```

---

## 트러블슈팅

### CR이 생성되지 않음

```bash
# Operator 로그 확인
kubectl logs -l app.kubernetes.io/name=<operator-name> -n <operator-ns>

# CRD 존재 여부
kubectl get crd | grep <crd-name>

# RBAC 권한 확인
kubectl auth can-i create externalsecrets --as=system:serviceaccount:external-secrets:external-secrets -n chat
```

### CR 상태가 업데이트되지 않음

```bash
# CR 이벤트 확인
kubectl describe <cr-type> <cr-name> -n <ns>

# Operator Pod 재시작
kubectl rollout restart deployment/<operator-deployment> -n <operator-ns>

# Finalizer 확인 (삭제 안 될 때)
kubectl get <cr-type> <cr-name> -n <ns> -o jsonpath='{.metadata.finalizers}'
```

### ExternalSecret Sync 실패

```bash
# 상태 확인
kubectl get externalsecret <name> -n <ns> -o jsonpath='{.status.conditions}'

# SecretStore 연결 확인
kubectl get clustersecretstore aws-ssm-store -o jsonpath='{.status.conditions}'

# AWS 인증 확인
kubectl get secret aws-global-credentials -n kube-system
```

---

## 유용한 스크립트

### 모든 CR 상태 확인

```bash
#!/bin/bash
# cr-status.sh

echo "=== ExternalSecrets ==="
kubectl get externalsecret -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,STORE:.spec.secretStoreRef.name,STATUS:.status.conditions[0].reason'

echo ""
echo "=== ServiceMonitors ==="
kubectl get servicemonitor -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,SELECTOR:.spec.selector.matchLabels'

echo ""
echo "=== Certificates ==="
kubectl get certificate -A -o custom-columns='NAMESPACE:.metadata.namespace,NAME:.metadata.name,READY:.status.conditions[0].status,EXPIRY:.status.notAfter'
```

### ExternalSecret 강제 동기화

```bash
#!/bin/bash
# force-sync-external-secret.sh
NAME=$1
NS=$2

if [ -z "$NAME" ] || [ -z "$NS" ]; then
  echo "Usage: $0 <name> <namespace>"
  exit 1
fi

# Annotation 추가로 강제 동기화
kubectl annotate externalsecret $NAME -n $NS force-sync=$(date +%s) --overwrite
echo "Triggered sync for $NAME in $NS"

# 상태 확인
sleep 3
kubectl get externalsecret $NAME -n $NS -o jsonpath='{.status.conditions[0].message}'
echo ""
```

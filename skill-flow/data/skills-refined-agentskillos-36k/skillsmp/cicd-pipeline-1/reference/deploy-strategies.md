# デプロイ戦略実装ガイド

## 目次
- Blue-Green デプロイ
- Canary デプロイ
- Rolling デプロイ
- Feature Flags
- ロールバック手順

## Blue-Green デプロイ

### 概念
2つの同一環境（Blue/Green）を用意し、トラフィックを瞬時に切り替える。

### AWS ALB + ECS実装

```bash
# 現在のターゲットグループ確認
aws elbv2 describe-listeners --load-balancer-arn $ALB_ARN

# 新環境（Green）にデプロイ
aws ecs update-service \
  --cluster my-cluster \
  --service my-service-green \
  --task-definition my-task:NEW_VERSION

# ヘルスチェック待機
aws ecs wait services-stable \
  --cluster my-cluster \
  --services my-service-green

# トラフィック切り替え
aws elbv2 modify-listener \
  --listener-arn $LISTENER_ARN \
  --default-actions Type=forward,TargetGroupArn=$GREEN_TG_ARN
```

### Kubernetes実装

```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: my-app
spec:
  selector:
    app: my-app
    version: green  # blue ↔ green を切り替え
  ports:
    - port: 80
      targetPort: 8080
```

## Canary デプロイ

### Kubernetes + Istio

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: my-app
spec:
  hosts:
    - my-app
  http:
    - route:
        - destination:
            host: my-app
            subset: stable
          weight: 90
        - destination:
            host: my-app
            subset: canary
          weight: 10
---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: my-app
spec:
  host: my-app
  subsets:
    - name: stable
      labels:
        version: v1
    - name: canary
      labels:
        version: v2
```

### 段階的ロールアウト

```
Phase 1: 5%   → メトリクス監視（15分）
Phase 2: 25%  → メトリクス監視（30分）
Phase 3: 50%  → メトリクス監視（1時間）
Phase 4: 100% → 完了
```

### 自動ロールバック条件

```yaml
# Argo Rollouts
apiVersion: argoproj.io/v1alpha1
kind: Rollout
spec:
  strategy:
    canary:
      steps:
        - setWeight: 10
        - pause: {duration: 10m}
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: my-app
        - setWeight: 50
        - pause: {duration: 10m}
---
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 1m
      successCondition: result[0] >= 0.95
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m])) /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```

## Rolling デプロイ

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%        # 最大追加Pod数
      maxUnavailable: 25%  # 最大停止Pod数
  template:
    spec:
      containers:
        - name: app
          image: my-app:v2
          readinessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
```

## Feature Flags

### LaunchDarkly統合例

```python
import ldclient
from ldclient.config import Config

ldclient.set_config(Config("sdk-key"))
client = ldclient.get()

user = {"key": "user-123", "email": "user@example.com"}

if client.variation("new-checkout-flow", user, False):
    return new_checkout()
else:
    return legacy_checkout()
```

### 自前実装（シンプル版）

```python
import os
import json

class FeatureFlags:
    def __init__(self):
        self.flags = json.loads(os.getenv("FEATURE_FLAGS", "{}"))
    
    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        return self.flags.get(flag_name, default)

# 使用
flags = FeatureFlags()
if flags.is_enabled("new_feature"):
    new_feature()
```

## ロールバック手順

### 即座ロールバック（Blue-Green）

```bash
# 前のターゲットグループに切り戻し
aws elbv2 modify-listener \
  --listener-arn $LISTENER_ARN \
  --default-actions Type=forward,TargetGroupArn=$BLUE_TG_ARN
```

### Kubernetesロールバック

```bash
# 直前のリビジョンに戻す
kubectl rollout undo deployment/my-app

# 特定リビジョンに戻す
kubectl rollout history deployment/my-app
kubectl rollout undo deployment/my-app --to-revision=3
```

### データベースマイグレーション考慮

1. **前方互換性**: 新コードが古いDBスキーマで動作すること
2. **後方互換性**: 古いコードが新しいDBスキーマで動作すること
3. **段階的マイグレーション**:
   - Phase 1: カラム追加（NULL許容）
   - Phase 2: 新コードデプロイ
   - Phase 3: データ移行
   - Phase 4: 古いカラム削除

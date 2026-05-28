---
name: kubernetes
description: Kubernetes設計・運用 - デプロイメント、スケーリング、ネットワーキング、セキュリティ
requires-guidelines:
  - kubernetes
  - common
---

# Kubernetes設計・運用

## 使用タイミング

- K8sマニフェスト作成時
- クラスタ設計・構築時
- スケーリング戦略検討時

---

## 設計パターン

### 🔴 Critical（修正必須）

| 問題 | 対策 |
|------|------|
| リソース制限なし | `resources.requests/limits`設定 |
| ヘルスチェック未設定 | `liveness/readiness/startupProbe`設定 |
| root権限で実行 | `runAsNonRoot: true`, `readOnlyRootFilesystem: true` |

### 🟡 Warning（要改善）

| 問題 | 対策 |
|------|------|
| HPAなしの固定レプリカ | HPAで自動スケール |
| ConfigMap/Secretハードコード | Secret/ConfigMap使用 |
| LoadBalancer乱用 | Ingressで集約 |

---

## 主要マニフェスト

```yaml
# ✅ リソース制限 + ヘルスチェック + セキュリティ
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: app
        image: app:latest
        resources:
          requests: { memory: "128Mi", cpu: "100m" }
          limits: { memory: "256Mi", cpu: "200m" }
        livenessProbe:
          httpGet: { path: /healthz, port: 8080 }
          initialDelaySeconds: 30
        readinessProbe:
          httpGet: { path: /ready, port: 8080 }
          initialDelaySeconds: 5
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true

---
# ✅ HPA
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
spec:
  scaleTargetRef: { apiVersion: apps/v1, kind: Deployment, name: app }
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource: { name: cpu, target: { type: Utilization, averageUtilization: 70 } }
```

---

## リソース構成

### ワークロード
- Deployment（推奨）、StatefulSet、DaemonSet、Job/CronJob

### ネットワーク
- ClusterIP（内部）、NodePort（開発）、LoadBalancer、**Ingress（推奨）**

### ストレージ
- PersistentVolume/Claim、StorageClass、CSI Driver

---

## チェックリスト

### リソース管理
- [ ] requests/limits設定
- [ ] HPA設定
- [ ] PodDisruptionBudget

### ヘルスチェック
- [ ] livenessProbe
- [ ] readinessProbe
- [ ] startupProbe

### セキュリティ
- [ ] runAsNonRoot: true
- [ ] readOnlyRootFilesystem: true
- [ ] NetworkPolicy
- [ ] Secret外部管理

### 可観測性
- [ ] 構造化ログ（JSON）
- [ ] Prometheusメトリクス
- [ ] 分散トレーシング

---

## 出力形式

```
🔴 **Critical**: `deployment.yaml:15` - リソース未設定 → requests/limits追加
🟡 **Warning**: `service.yaml:8` - LoadBalancer → Ingress推奨
📊 **Summary**: Critical 1件 / Warning 1件
```

---

## 関連ガイドライン

- `infrastructure/aws-eks.md`
- `design/microservices-kubernetes.md`

## 外部知識ベース（Context7）

- Kubernetes公式ドキュメント
- AWS EKSベストプラクティス
- CNCFセキュリティガイドライン

> **Context7検索キーワード**: `/kubernetes/website` で以下を検索
> - "resource limits requests"
> - "liveness readiness probe"
> - "horizontal pod autoscaler"
> - "network policy"

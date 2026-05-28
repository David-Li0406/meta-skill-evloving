---
name: "devops-engineer"
description: "Activates when user requests CI/CD pipeline design, containerization, Kubernetes management, monitoring/alerting setup, or infrastructure as code. Do NOT use for application feature coding. Examples: 'Create Dockerfile', 'Setup GitHub Actions pipeline'."
---

# DevOps Engineer Skill

## 🧠 Expertise

資深 DevOps 工程師，專精於雲端原生架構、CI/CD 自動化、容器編排與系統可靠性工程。

---

## 1. CI/CD Pipeline 設計

### 1.1 Pipeline 階段

```
┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐
│  Build  │ → │  Test   │ → │  Scan   │ → │ Deploy  │ → │ Verify  │
└─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘
```

| 階段 | 目的 | 工具 |
|-----|------|------|
| **Build** | 編譯、打包 | Docker, Maven, npm |
| **Test** | 單元測試、整合測試 | PHPUnit, Jest, Cypress |
| **Scan** | 安全掃描、代碼品質 | Trivy, SonarQube, PHPStan |
| **Deploy** | 部署至環境 | Kubernetes, ArgoCD |
| **Verify** | 健康檢查、煙霧測試 | curl, k6 |

### 1.2 GitHub Actions 範例

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup PHP
      uses: shivammathur/setup-php@v2
      with:
        php-version: '8.3'
        extensions: mbstring, redis, pdo_mysql
    
    - name: Install Dependencies
      run: composer install --prefer-dist --no-progress
    
    - name: Run Tests
      run: php artisan test --parallel
    
    - name: Run Static Analysis
      run: ./vendor/bin/phpstan analyse

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Trivy Scan
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        format: 'sarif'
        output: 'trivy-results.sarif'

  deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to Production
      run: |
        kubectl set image deployment/app app=$IMAGE_TAG
        kubectl rollout status deployment/app
```

---

## 2. 容器化最佳實務

### 2.1 Dockerfile 優化

```dockerfile
# 多階段建構
FROM composer:2 AS builder
WORKDIR /app
COPY composer.* ./
RUN composer install --no-dev --no-scripts --prefer-dist

FROM php:8.3-fpm-alpine AS production
WORKDIR /var/www/html

# 安裝必要擴展
RUN apk add --no-cache \
    libpng-dev \
    && docker-php-ext-install pdo_mysql gd opcache

# 複製依賴
COPY --from=builder /app/vendor ./vendor
COPY . .

# 安全設定
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html/storage

USER www-data
EXPOSE 9000
CMD ["php-fpm"]
```

### 2.2 容器安全原則

| 原則 | 說明 |
|-----|------|
| **非 Root 執行** | `USER www-data` |
| **最小化映像** | 使用 Alpine 基礎映像 |
| **唯讀檔案系統** | `readOnlyRootFilesystem: true` |
| **掃描漏洞** | Trivy, Clair |

---

## 3. Kubernetes 部署

### 3.1 Deployment 設計

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: app
        image: app:v1.0.0
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          runAsNonRoot: true
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
```

### 3.2 部署策略

| 策略 | 說明 | 適用場景 |
|-----|------|---------|
| **Rolling Update** | 逐步替換 Pod | 一般更新 |
| **Blue-Green** | 雙環境切換 | 零停機部署 |
| **Canary** | 灰度發布 | 風險控制 |

---

## 4. 監控告警設計

### 4.1 監控層次

| 層次 | 監控項目 | 工具 |
|-----|---------|------|
| **基礎設施** | CPU、記憶體、磁碟 | Prometheus Node Exporter |
| **應用程式** | 響應時間、錯誤率 | APM (New Relic, Datadog) |
| **業務指標** | 交易量、轉換率 | 自定義 Metrics |

### 4.2 Prometheus 告警規則

```yaml
groups:
- name: application-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      
  - alert: HighLatency
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High latency detected"
      
  - alert: PodCrashLooping
    expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
    for: 5m
    labels:
      severity: critical
```

### 4.3 SLI/SLO 定義

| 指標 | SLI | SLO |
|-----|-----|-----|
| **可用性** | 成功請求 / 總請求 | 99.9% |
| **延遲** | P95 響應時間 | < 200ms |
| **錯誤率** | 5xx / 總請求 | < 0.1% |

---

## 5. 基礎設施即代碼

### 5.1 Terraform 結構

```
infrastructure/
├── modules/
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── production/
└── global/
    └── iam/
```

### 5.2 最佳實務

| 實務 | 說明 |
|-----|------|
| **模組化** | 可重用的基礎設施模組 |
| **狀態管理** | 遠端狀態存儲 (S3 + DynamoDB) |
| **版本控制** | 所有配置納入 Git |
| **變更審核** | PR 審核 + Plan 預覽 |

---

## 6. 可靠性工程 (SRE)

### 6.1 錯誤預算

```
錯誤預算 = 1 - SLO
若 SLO = 99.9%，則每月錯誤預算 = 43.8 分鐘
```

### 6.2 事故響應流程

```
1. 檢測 (Detection) → 監控告警
2. 分類 (Triage) → 嚴重度評估
3. 緩解 (Mitigation) → 快速恢復服務
4. 修復 (Resolution) → 根本原因修復
5. 回顧 (Postmortem) → 持續改進
```

---

## 7. DevOps 檢查清單

### CI/CD
- [ ] Pipeline 是否自動化？
- [ ] 測試是否並行執行？
- [ ] 安全掃描是否集成？
- [ ] 部署是否可回滾？

### 監控
- [ ] 是否有健康檢查端點？
- [ ] 是否定義 SLI/SLO？
- [ ] 告警是否可行動？
- [ ] 是否有 On-call 機制？

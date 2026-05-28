# 監視・アラート設定ガイド

## 目次
- Prometheus設定
- Grafanaダッシュボード
- アラートルール
- ログ収集
- トレーシング

## Prometheus設定

### scrape_configs

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

  - job_name: 'kubernetes-service-endpoints'
    kubernetes_sd_configs:
      - role: endpoints
    relabel_configs:
      - source_labels: [__meta_kubernetes_service_annotation_prometheus_io_scrape]
        action: keep
        regex: true
```

### Recording Rules

```yaml
groups:
  - name: app-metrics
    interval: 30s
    rules:
      - record: job:http_requests_total:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
      
      - record: job:http_request_duration_seconds:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, job))
      
      - record: job:http_requests_error_rate:rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) by (job)
          /
          sum(rate(http_requests_total[5m])) by (job)
```

## アラートルール

```yaml
groups:
  - name: availability
    rules:
      - alert: HighErrorRate
        expr: job:http_requests_error_rate:rate5m > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "高エラーレート検出: {{ $labels.job }}"
          description: "{{ $labels.job }} のエラーレートが {{ $value | humanizePercentage }} です"
      
      - alert: HighLatency
        expr: job:http_request_duration_seconds:p95 > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "高レイテンシ検出: {{ $labels.job }}"
          description: "{{ $labels.job }} のP95レイテンシが {{ $value | humanizeDuration }} です"

  - name: resources
    rules:
      - alert: PodCPUHigh
        expr: |
          sum(rate(container_cpu_usage_seconds_total{container!=""}[5m])) by (namespace, pod)
          /
          sum(kube_pod_container_resource_limits{resource="cpu"}) by (namespace, pod)
          > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Pod CPU使用率が高い: {{ $labels.pod }}"
          description: "{{ $labels.namespace }}/{{ $labels.pod }} のCPU使用率が90%を超えています"
      
      - alert: PodMemoryHigh
        expr: |
          sum(container_memory_working_set_bytes{container!=""}) by (namespace, pod)
          /
          sum(kube_pod_container_resource_limits{resource="memory"}) by (namespace, pod)
          > 0.9
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Pod メモリ使用率が高い: {{ $labels.pod }}"
      
      - alert: PodRestarting
        expr: increase(kube_pod_container_status_restarts_total[1h]) > 3
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod が頻繁に再起動: {{ $labels.pod }}"
          description: "{{ $labels.namespace }}/{{ $labels.pod }} が過去1時間で {{ $value }} 回再起動しています"

  - name: infrastructure
    rules:
      - alert: NodeNotReady
        expr: kube_node_status_condition{condition="Ready",status="true"} == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "ノードがNotReady: {{ $labels.node }}"
      
      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "ディスク残量が少ない: {{ $labels.instance }}"
          description: "残り {{ $value | humanizePercentage }}"
```

## Grafanaダッシュボード

### PromQL クエリ例

```promql
# リクエストレート
sum(rate(http_requests_total[5m])) by (service)

# エラーレート
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
/
sum(rate(http_requests_total[5m])) by (service)

# P50/P95/P99 レイテンシ
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))

# CPU使用率
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# メモリ使用率
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```

## ログ収集（Loki）

### Promtail設定

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    pipeline_stages:
      - cri: {}
      - json:
          expressions:
            level: level
            msg: msg
      - labels:
          level:
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
```

### LogQL クエリ例

```logql
# エラーログ検索
{app="my-app"} |= "error"

# JSON解析
{app="my-app"} | json | level="error"

# レート計算
sum(rate({app="my-app"} |= "error" [5m])) by (pod)
```

## トレーシング（OpenTelemetry）

### アプリケーション設定（Python）

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

# セットアップ
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

otlp_exporter = OTLPSpanExporter(endpoint="http://otel-collector:4317")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# FastAPI自動計装
FastAPIInstrumentor.instrument_app(app)

# カスタムスパン
with tracer.start_as_current_span("my-operation") as span:
    span.set_attribute("user.id", user_id)
    result = do_work()
```

## SLI/SLO定義

```yaml
# SLO定義例
availability:
  target: 99.9%
  window: 30d
  sli:
    good: sum(rate(http_requests_total{status!~"5.."}[5m]))
    total: sum(rate(http_requests_total[5m]))

latency:
  target: 95%
  threshold: 200ms
  window: 30d
  sli:
    good: sum(rate(http_request_duration_seconds_bucket{le="0.2"}[5m]))
    total: sum(rate(http_request_duration_seconds_count[5m]))
```

# Observability Sre - Validations

## High Cardinality Metric Label

### **Id**
high-cardinality-label
### **Severity**
error
### **Type**
regex
### **Pattern**
  - labels\(.*user_id
  - labels\(.*request_id
  - labels\(.*email
  - labels\(.*session_id
  - \\.labels\(.*uuid
### **Message**
High-cardinality label will exhaust Prometheus memory.
### **Fix Action**
Use exemplars or aggregate by tier/category instead
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.go

## Log Statement Without Request Context

### **Id**
log-without-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - logger\.(info|warning|error)\(["'][^"']+["'](?!.*request_id)
  - console\.(log|error)\(["'][^"']+["']\)
  - log\.(Info|Warn|Error)\(["'][^"']+["'](?!.*traceId)
### **Message**
Log without request context. Can't correlate during debugging.
### **Fix Action**
Include request_id or trace_id: logger.info('msg', request_id=req_id)
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.go

## Alert Without Runbook Link

### **Id**
alert-no-runbook
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - alert:(?!.*runbook)
  - alertname:(?!.*documentation)
### **Message**
Alert without runbook link. On-call won't know what to do.
### **Fix Action**
Add runbook_url annotation to alert
### **Applies To**
  - **/alerts/*.yaml
  - **/prometheus/*.yaml
  - **/*rules*.yaml

## Histogram With Default Buckets

### **Id**
histogram-default-buckets
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Histogram\([^)]+\)(?!.*buckets)
  - prometheus\.NewHistogram(?!.*Buckets)
### **Message**
Histogram using default buckets. May not match your latency profile.
### **Fix Action**
Define custom buckets matching expected latency distribution
### **Applies To**
  - **/*.py
  - **/*.go

## Error Metric Without Error Type

### **Id**
missing-error-label
### **Severity**
info
### **Type**
regex
### **Pattern**
  - error.*counter(?!.*type|.*code)
  - errors_total(?!.*error_type)
### **Message**
Error metric without error type label. Can't distinguish error types.
### **Fix Action**
Add error_type or error_code label
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.go

## HTTP Call Without Trace Propagation

### **Id**
no-trace-propagation
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - requests\.get\((?!.*headers.*traceparent)
  - httpx\..*get\((?!.*headers)
  - fetch\((?!.*headers.*trace)
### **Message**
HTTP call may not propagate trace context.
### **Fix Action**
Use instrumented HTTP client or inject trace headers
### **Applies To**
  - **/*.py
  - **/*.ts

## Debug Logging in Production Code

### **Id**
debug-log-production
### **Severity**
info
### **Type**
regex
### **Pattern**
  - logger\.debug\([^)]+\)(?!.*if.*DEBUG)
  - console\.debug\(
  - log\.Debug\(
### **Message**
Debug logging in production. May cause high log volume.
### **Fix Action**
Guard with log level check or use sampling
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.go

## Metric Without Help Text

### **Id**
metric-no-help
### **Severity**
info
### **Type**
regex
### **Pattern**
  - Counter\(['"][^'"]+['"]\s*,\s*\)
  - Gauge\(['"][^'"]+['"]\s*,\s*\)
  - Histogram\(['"][^'"]+['"]\s*,\s*\)
### **Message**
Metric without help text. Description helps with understanding.
### **Fix Action**
Add description: Counter('name', 'description')
### **Applies To**
  - **/*.py

## SLO Without Error Budget Calculation

### **Id**
slo-no-budget
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - slo.*target(?!.*budget)
  - availability.*99(?!.*error.*budget)
### **Message**
SLO defined without error budget tracking.
### **Fix Action**
Add error budget calculation and alerting
### **Applies To**
  - **/slo/*.yaml
  - **/prometheus/*.yaml

## Alert Without For Duration

### **Id**
alert-too-sensitive
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - alert:(?!.*for:)
  - expr:.*[^}]$(?!.*for)
### **Message**
Alert without 'for' duration. May fire on brief spikes.
### **Fix Action**
Add 'for: 5m' to require sustained condition
### **Applies To**
  - **/alerts/*.yaml
  - **/prometheus/*.yaml

## Catching Exception Without Logging

### **Id**
catch-all-logging
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - except:(?!.*log)
  - catch\s*\(.*\)\s*\{(?!.*log|.*console)
### **Message**
Exception caught without logging. Failures will be silent.
### **Fix Action**
Log exception with error level and stack trace
### **Applies To**
  - **/*.py
  - **/*.ts
  - **/*.js

## Latency Tracked as Gauge

### **Id**
latency-not-histogram
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - latency.*Gauge
  - duration.*Gauge
  - response_time.*Gauge
### **Message**
Latency tracked as Gauge loses distribution info.
### **Fix Action**
Use Histogram for latency to enable percentile calculations
### **Applies To**
  - **/*.py
  - **/*.go
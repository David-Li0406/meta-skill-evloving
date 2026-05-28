---
name: observability-architecture
description: LiteLLM-RS Observability Architecture. Covers Prometheus metrics, OpenTelemetry tracing, structured logging, health checks, and alerting integration.
---

# Observability Architecture Guide

## Overview

LiteLLM-RS implements comprehensive observability through three pillars: metrics (Prometheus), tracing (OpenTelemetry), and logging (structured JSON). This enables complete visibility into gateway operations.

### Observability Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                    LiteLLM Gateway                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐      │
│  │    Metrics    │  │    Tracing    │  │    Logging    │      │
│  │  (Prometheus) │  │ (OpenTelemetry)│  │   (tracing)   │      │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘      │
│          │                  │                  │                │
└──────────┼──────────────────┼──────────────────┼────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│    Prometheus    │ │      Jaeger/     │ │    ELK Stack/    │
│    + Grafana     │ │      Tempo       │ │      Loki        │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## Metrics (Prometheus)

### Metric Types

```rust
use prometheus::{Counter, Gauge, Histogram, IntCounter, IntGauge, Registry};
use lazy_static::lazy_static;

lazy_static! {
    pub static ref REGISTRY: Registry = Registry::new();

    // Request counters
    pub static ref HTTP_REQUESTS_TOTAL: IntCounter = IntCounter::new(
        "litellm_http_requests_total",
        "Total number of HTTP requests"
    ).unwrap();

    pub static ref PROVIDER_REQUESTS_TOTAL: IntCounterVec = IntCounterVec::new(
        Opts::new("litellm_provider_requests_total", "Total provider requests"),
        &["provider", "model", "status"]
    ).unwrap();

    // Latency histograms
    pub static ref REQUEST_LATENCY_SECONDS: HistogramVec = HistogramVec::new(
        HistogramOpts::new(
            "litellm_request_latency_seconds",
            "Request latency in seconds"
        ).buckets(vec![0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]),
        &["provider", "model", "endpoint"]
    ).unwrap();

    pub static ref PROVIDER_LATENCY_SECONDS: HistogramVec = HistogramVec::new(
        HistogramOpts::new(
            "litellm_provider_latency_seconds",
            "Provider API latency in seconds"
        ).buckets(vec![0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]),
        &["provider", "model"]
    ).unwrap();

    // Token counters
    pub static ref TOKENS_TOTAL: IntCounterVec = IntCounterVec::new(
        Opts::new("litellm_tokens_total", "Total tokens processed"),
        &["provider", "model", "type"]  // type: prompt, completion
    ).unwrap();

    // Cost tracking
    pub static ref COST_TOTAL: CounterVec = CounterVec::new(
        Opts::new("litellm_cost_usd_total", "Total cost in USD"),
        &["provider", "model"]
    ).unwrap();

    // Active connections
    pub static ref ACTIVE_CONNECTIONS: IntGauge = IntGauge::new(
        "litellm_active_connections",
        "Number of active connections"
    ).unwrap();

    pub static ref ACTIVE_STREAMS: IntGaugeVec = IntGaugeVec::new(
        Opts::new("litellm_active_streams", "Number of active streaming connections"),
        &["provider"]
    ).unwrap();

    // Cache metrics
    pub static ref CACHE_HITS_TOTAL: IntCounterVec = IntCounterVec::new(
        Opts::new("litellm_cache_hits_total", "Total cache hits"),
        &["cache_tier"]  // l1, l2, l3
    ).unwrap();

    pub static ref CACHE_MISSES_TOTAL: IntCounter = IntCounter::new(
        "litellm_cache_misses_total",
        "Total cache misses"
    ).unwrap();

    // Health metrics
    pub static ref PROVIDER_HEALTH: IntGaugeVec = IntGaugeVec::new(
        Opts::new("litellm_provider_health", "Provider health status (1=healthy, 0=unhealthy)"),
        &["provider"]
    ).unwrap();

    // Error metrics
    pub static ref ERRORS_TOTAL: IntCounterVec = IntCounterVec::new(
        Opts::new("litellm_errors_total", "Total errors"),
        &["provider", "error_type"]
    ).unwrap();

    // Rate limiting
    pub static ref RATE_LIMIT_HITS: IntCounterVec = IntCounterVec::new(
        Opts::new("litellm_rate_limit_hits_total", "Rate limit hits"),
        &["provider", "limit_type"]  // rpm, tpm
    ).unwrap();
}
```

### Metrics Registration

```rust
pub fn register_metrics() {
    REGISTRY.register(Box::new(HTTP_REQUESTS_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(PROVIDER_REQUESTS_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(REQUEST_LATENCY_SECONDS.clone())).unwrap();
    REGISTRY.register(Box::new(PROVIDER_LATENCY_SECONDS.clone())).unwrap();
    REGISTRY.register(Box::new(TOKENS_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(COST_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(ACTIVE_CONNECTIONS.clone())).unwrap();
    REGISTRY.register(Box::new(ACTIVE_STREAMS.clone())).unwrap();
    REGISTRY.register(Box::new(CACHE_HITS_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(CACHE_MISSES_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(PROVIDER_HEALTH.clone())).unwrap();
    REGISTRY.register(Box::new(ERRORS_TOTAL.clone())).unwrap();
    REGISTRY.register(Box::new(RATE_LIMIT_HITS.clone())).unwrap();
}
```

### Metrics Endpoint

```rust
use actix_web::{HttpResponse, web};
use prometheus::Encoder;

pub async fn metrics_handler() -> HttpResponse {
    let encoder = prometheus::TextEncoder::new();
    let metric_families = REGISTRY.gather();

    let mut buffer = Vec::new();
    encoder.encode(&metric_families, &mut buffer).unwrap();

    HttpResponse::Ok()
        .content_type("text/plain; charset=utf-8")
        .body(buffer)
}

// Register in routes
pub fn configure_metrics(cfg: &mut web::ServiceConfig) {
    cfg.route("/metrics", web::get().to(metrics_handler));
}
```

---

## Tracing (OpenTelemetry)

### Tracing Setup

```rust
use opentelemetry::{global, sdk::trace as sdktrace, trace::TraceError};
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

pub fn init_tracing(config: &TracingConfig) -> Result<(), TraceError> {
    // Create OTLP exporter
    let exporter = opentelemetry_otlp::new_exporter()
        .tonic()
        .with_endpoint(&config.endpoint);

    // Create tracer provider
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(exporter)
        .with_trace_config(
            sdktrace::config()
                .with_sampler(sdktrace::Sampler::TraceIdRatioBased(config.sample_rate))
                .with_resource(opentelemetry::sdk::Resource::new(vec![
                    opentelemetry::KeyValue::new("service.name", "litellm-gateway"),
                    opentelemetry::KeyValue::new("service.version", env!("CARGO_PKG_VERSION")),
                ])),
        )
        .install_batch(opentelemetry::runtime::Tokio)?;

    // Create OpenTelemetry layer
    let otel_layer = tracing_opentelemetry::layer().with_tracer(tracer);

    // Create fmt layer for console output
    let fmt_layer = tracing_subscriber::fmt::layer()
        .with_target(true)
        .json();

    // Initialize subscriber
    tracing_subscriber::registry()
        .with(otel_layer)
        .with(fmt_layer)
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    Ok(())
}
```

### Span Creation

```rust
use tracing::{info_span, instrument, Span};

/// Instrument a provider request with tracing
#[instrument(
    name = "provider_request",
    skip(request, context),
    fields(
        provider = %provider_name,
        model = %request.model,
        request_id = %context.request_id,
    )
)]
pub async fn traced_provider_request(
    provider_name: &str,
    request: ChatRequest,
    context: RequestContext,
) -> Result<ChatResponse, ProviderError> {
    let span = Span::current();

    // Add request attributes
    span.record("messages_count", request.messages.len());
    if let Some(max_tokens) = request.max_tokens {
        span.record("max_tokens", max_tokens);
    }

    let start = std::time::Instant::now();
    let result = provider.chat_completion(request, context).await;
    let duration = start.elapsed();

    // Record response attributes
    match &result {
        Ok(response) => {
            span.record("status", "success");
            if let Some(usage) = &response.usage {
                span.record("prompt_tokens", usage.prompt_tokens);
                span.record("completion_tokens", usage.completion_tokens);
            }
        }
        Err(e) => {
            span.record("status", "error");
            span.record("error", e.to_string());
        }
    }

    span.record("duration_ms", duration.as_millis() as i64);

    result
}
```

### Request Tracing Middleware

```rust
use actix_web::{dev::ServiceRequest, HttpMessage};
use tracing::{info_span, Instrument};

pub async fn tracing_middleware(
    req: ServiceRequest,
    next: Next<impl MessageBody>,
) -> Result<ServiceResponse<impl MessageBody>, Error> {
    let request_id = req
        .headers()
        .get("X-Request-ID")
        .and_then(|h| h.to_str().ok())
        .map(|s| s.to_string())
        .unwrap_or_else(|| uuid::Uuid::new_v4().to_string());

    let span = info_span!(
        "http_request",
        request_id = %request_id,
        method = %req.method(),
        path = %req.path(),
        user_agent = req.headers().get("User-Agent").and_then(|h| h.to_str().ok()).unwrap_or(""),
    );

    // Store request_id in extensions for later use
    req.extensions_mut().insert(RequestId(request_id.clone()));

    let response = next.call(req).instrument(span.clone()).await?;

    // Record response status
    span.record("status_code", response.status().as_u16());

    Ok(response)
}
```

---

## Structured Logging

### Log Configuration

```rust
use tracing_subscriber::{fmt, EnvFilter};

pub fn init_logging(config: &LoggingConfig) {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new(&config.level));

    let subscriber = tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(config.include_target)
        .with_file(config.include_file)
        .with_line_number(config.include_line);

    match config.format.as_str() {
        "json" => {
            subscriber.json().init();
        }
        "pretty" => {
            subscriber.pretty().init();
        }
        _ => {
            subscriber.init();
        }
    }
}
```

### Structured Log Events

```rust
use tracing::{info, warn, error, debug};

// Request logging
info!(
    request_id = %request_id,
    provider = %provider_name,
    model = %model,
    latency_ms = %latency.as_millis(),
    status = "success",
    "Chat completion request completed"
);

// Error logging
error!(
    request_id = %request_id,
    provider = %provider_name,
    error_type = "rate_limit",
    retry_after = ?retry_after,
    "Rate limit exceeded"
);

// Debug logging for detailed info
debug!(
    request_id = %request_id,
    tokens_prompt = %usage.prompt_tokens,
    tokens_completion = %usage.completion_tokens,
    cost_usd = %cost,
    "Token usage and cost"
);
```

---

## Health Checks

### Health Check System

```rust
use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct HealthResponse {
    pub status: HealthStatus,
    pub version: String,
    pub uptime_seconds: u64,
    pub checks: Vec<ComponentHealth>,
}

#[derive(Debug, Serialize)]
pub struct ComponentHealth {
    pub name: String,
    pub status: HealthStatus,
    pub latency_ms: Option<u64>,
    pub message: Option<String>,
}

#[derive(Debug, Clone, Copy, Serialize, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum HealthStatus {
    Healthy,
    Degraded,
    Unhealthy,
}

pub struct HealthChecker {
    start_time: std::time::Instant,
    providers: Vec<Arc<dyn LLMProvider>>,
    redis_client: Option<Arc<RedisCache>>,
}

impl HealthChecker {
    pub async fn check(&self) -> HealthResponse {
        let mut checks = Vec::new();
        let mut overall_status = HealthStatus::Healthy;

        // Check providers
        for provider in &self.providers {
            let start = std::time::Instant::now();
            let status = provider.health_check().await;
            let latency = start.elapsed().as_millis() as u64;

            let health_status = match status {
                crate::core::types::common::HealthStatus::Healthy => HealthStatus::Healthy,
                crate::core::types::common::HealthStatus::Degraded => HealthStatus::Degraded,
                crate::core::types::common::HealthStatus::Unhealthy => HealthStatus::Unhealthy,
            };

            if health_status != HealthStatus::Healthy && overall_status == HealthStatus::Healthy {
                overall_status = HealthStatus::Degraded;
            }

            checks.push(ComponentHealth {
                name: format!("provider:{}", provider.name()),
                status: health_status,
                latency_ms: Some(latency),
                message: None,
            });
        }

        // Check Redis
        if let Some(redis) = &self.redis_client {
            let start = std::time::Instant::now();
            let status = match redis.ping().await {
                Ok(_) => HealthStatus::Healthy,
                Err(e) => {
                    overall_status = HealthStatus::Degraded;
                    HealthStatus::Unhealthy
                }
            };
            let latency = start.elapsed().as_millis() as u64;

            checks.push(ComponentHealth {
                name: "redis".to_string(),
                status,
                latency_ms: Some(latency),
                message: None,
            });
        }

        HealthResponse {
            status: overall_status,
            version: env!("CARGO_PKG_VERSION").to_string(),
            uptime_seconds: self.start_time.elapsed().as_secs(),
            checks,
        }
    }
}
```

### Health Endpoints

```rust
use actix_web::{HttpResponse, web};

// Liveness probe - is the service running?
pub async fn liveness_handler() -> HttpResponse {
    HttpResponse::Ok().json(json!({ "status": "alive" }))
}

// Readiness probe - is the service ready to accept requests?
pub async fn readiness_handler(
    health_checker: web::Data<HealthChecker>,
) -> HttpResponse {
    let health = health_checker.check().await;

    match health.status {
        HealthStatus::Healthy | HealthStatus::Degraded => {
            HttpResponse::Ok().json(health)
        }
        HealthStatus::Unhealthy => {
            HttpResponse::ServiceUnavailable().json(health)
        }
    }
}

// Detailed health - full system status
pub async fn health_handler(
    health_checker: web::Data<HealthChecker>,
) -> HttpResponse {
    let health = health_checker.check().await;

    let status_code = match health.status {
        HealthStatus::Healthy => 200,
        HealthStatus::Degraded => 200,  // Still operational
        HealthStatus::Unhealthy => 503,
    };

    HttpResponse::build(actix_web::http::StatusCode::from_u16(status_code).unwrap())
        .json(health)
}

pub fn configure_health(cfg: &mut web::ServiceConfig) {
    cfg.route("/health", web::get().to(health_handler))
       .route("/health/live", web::get().to(liveness_handler))
       .route("/health/ready", web::get().to(readiness_handler));
}
```

---

## Alerting Integration

### Alert Rules (Prometheus)

```yaml
# prometheus/alerts.yml
groups:
  - name: litellm_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum(rate(litellm_errors_total[5m])) /
          sum(rate(litellm_http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | printf \"%.2f\" }}%"

      # Provider unhealthy
      - alert: ProviderUnhealthy
        expr: litellm_provider_health == 0
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Provider {{ $labels.provider }} is unhealthy"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, rate(litellm_request_latency_seconds_bucket[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "P95 latency is above 10 seconds"
          description: "P95 latency: {{ $value | printf \"%.2f\" }}s"

      # Rate limit approaching
      - alert: RateLimitApproaching
        expr: |
          rate(litellm_rate_limit_hits_total[5m]) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Frequent rate limit hits for {{ $labels.provider }}"

      # No requests
      - alert: NoRequests
        expr: |
          sum(rate(litellm_http_requests_total[10m])) == 0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "No requests received in 10 minutes"
```

---

## Configuration

```yaml
observability:
  metrics:
    enabled: true
    endpoint: "/metrics"
    include_labels:
      - provider
      - model
      - status
      - error_type
    histogram_buckets:
      latency: [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
      tokens: [10, 50, 100, 500, 1000, 5000, 10000]

  tracing:
    enabled: true
    exporter: "otlp"
    endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}
    sample_rate: 0.1
    propagation: "tracecontext,baggage"

  logging:
    level: "info"
    format: "json"
    include_timestamp: true
    include_target: true
    include_file: false
    include_line: false

  health:
    enabled: true
    endpoints:
      health: "/health"
      live: "/health/live"
      ready: "/health/ready"
    check_interval_seconds: 30
```

---

## Best Practices

### 1. Use Appropriate Metric Types

```rust
// Good - Counter for monotonically increasing values
pub static ref REQUESTS_TOTAL: IntCounter = IntCounter::new(...).unwrap();

// Good - Gauge for values that can go up and down
pub static ref ACTIVE_CONNECTIONS: IntGauge = IntGauge::new(...).unwrap();

// Good - Histogram for latency/size distributions
pub static ref REQUEST_LATENCY: Histogram = Histogram::new(...).unwrap();

// Bad - Counter for active connections (can decrease)
pub static ref ACTIVE_CONNECTIONS: IntCounter = IntCounter::new(...).unwrap();
```

### 2. Include Request Context in Logs

```rust
// Good - includes request context
info!(
    request_id = %request_id,
    user_id = %user_id,
    provider = %provider_name,
    "Request completed"
);

// Bad - missing context
info!("Request completed");
```

### 3. Use Proper Cardinality

```rust
// Good - limited label cardinality
pub static ref ERRORS_TOTAL: IntCounterVec = IntCounterVec::new(
    Opts::new("errors_total", "Total errors"),
    &["provider", "error_type"]  // Low cardinality
).unwrap();

// Bad - high cardinality labels
pub static ref ERRORS_TOTAL: IntCounterVec = IntCounterVec::new(
    Opts::new("errors_total", "Total errors"),
    &["request_id", "user_id"]  // Infinite cardinality!
).unwrap();
```

### 4. Graceful Degradation

```rust
// Good - handle missing telemetry gracefully
if let Err(e) = METRICS_REGISTRY.register(metric.clone()) {
    tracing::warn!("Failed to register metric: {}", e);
    // Continue without metrics
}

// Bad - panic on telemetry errors
METRICS_REGISTRY.register(metric.clone()).unwrap();
```

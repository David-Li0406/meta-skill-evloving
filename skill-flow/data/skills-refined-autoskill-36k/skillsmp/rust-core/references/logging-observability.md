# Logging and Observability in Rust

Comprehensive guide to logging, tracing, metrics, and observability in Rust applications.

## Ecosystem Overview

### Logging

- **log** - Logging facade (like SLF4J)
- **env_logger** - Simple logger implementation
- **tracing** - Structured, contextual logging
- **slog** - Structured logging with composable drains

### Tracing & Observability

- **tracing** - Async-aware instrumentation
- **tracing-subscriber** - Collectors and formatters
- **opentelemetry** - Open standard for observability
- **tokio-console** - Async runtime debugger

### Metrics

- **metrics** - Metrics facade
- **prometheus** - Prometheus exporter
- **statsd** - StatsD client

## Traditional Logging with `log`

### Basic Setup

```toml
[dependencies]
log = "0.4"
env_logger = "0.11"
```

```rust
use log::{info, warn, error, debug, trace};

fn main() {
    env_logger::init();

    trace!("This is a trace message");
    debug!("This is a debug message");
    info!("This is an info message");
    warn!("This is a warning");
    error!("This is an error");

    // With formatting
    let user = "Alice";
    info!("User {} logged in", user);

    // With structured data (requires formatting)
    info!("Request processed: method={} path={}", "GET", "/api/users");
}
```

### Log Levels

```bash
# Set log level via environment variable
RUST_LOG=debug cargo run
RUST_LOG=myapp=info,other_crate=debug cargo run

# Multiple modules
RUST_LOG=warn,myapp::api=debug cargo run
```

### Custom Logger

```rust
use log::{Record, Level, Metadata};

struct SimpleLogger;

impl log::Log for SimpleLogger {
    fn enabled(&self, metadata: &Metadata) -> bool {
        metadata.level() <= Level::Info
    }

    fn log(&self, record: &Record) {
        if self.enabled(record.metadata()) {
            println!("{} - {}", record.level(), record.args());
        }
    }

    fn flush(&self) {}
}

static LOGGER: SimpleLogger = SimpleLogger;

fn main() {
    log::set_logger(&LOGGER).unwrap();
    log::set_max_level(log::LevelFilter::Info);
}
```

## Modern Tracing with `tracing`

### Why Tracing Over Logging?

- Async-aware (works with tokio)
- Structured events
- Spans for tracking context
- Better performance
- Rich ecosystem

### Basic Setup

```toml
[dependencies]
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }
```

```rust
use tracing::{info, warn, error, debug, trace, instrument};

fn main() {
    // Initialize subscriber
    tracing_subscriber::fmt::init();

    trace!("Starting application");
    debug!("Debug information");
    info!("Application started");
    warn!("Low memory");
    error!("Failed to connect");

    // Structured fields
    info!(user_id = 42, "User logged in");
    error!(error = ?err, "Request failed");
}
```

### Spans

Spans represent periods of time and provide context.

```rust
use tracing::{span, Level, instrument};

fn process_request() {
    let span = span!(Level::INFO, "request", method = "GET", path = "/api/users");
    let _enter = span.enter();

    info!("Processing request");  // Logged within span context

    fetch_users();  // Nested span
}

// Automatic span with #[instrument]
#[instrument]
fn fetch_users() -> Vec<User> {
    debug!("Querying database");
    // Automatically creates span named "fetch_users"
    vec![]
}

// With specific fields
#[instrument(skip(password), fields(user_id = user.id))]
async fn login(user: &User, password: &str) -> Result<Token> {
    info!("Attempting login");
    // ...
}
```

### Subscriber Configuration

```rust
use tracing_subscriber::{
    fmt,
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};

fn init_tracing() {
    tracing_subscriber::registry()
        .with(EnvFilter::from_default_env()
            .add_directive("myapp=debug".parse().unwrap())
            .add_directive("tower_http=debug".parse().unwrap())
        )
        .with(fmt::layer()
            .with_target(true)
            .with_thread_ids(true)
            .with_level(true)
        )
        .init();
}
```

### JSON Output

```rust
use tracing_subscriber::fmt;

fn main() {
    tracing_subscriber::fmt()
        .json()
        .with_current_span(true)
        .with_span_list(true)
        .init();

    info!("Application started");
    // Output: {"timestamp":"2024-01-01T12:00:00.000Z","level":"INFO","message":"Application started"}
}
```

### Multiple Layers

```rust
use tracing_subscriber::layer::SubscriberExt;

fn init_layered_tracing() {
    let fmt_layer = tracing_subscriber::fmt::layer()
        .with_target(false);

    let filter_layer = EnvFilter::from_default_env();

    tracing_subscriber::registry()
        .with(filter_layer)
        .with(fmt_layer)
        .init();
}
```

## OpenTelemetry Integration

### Setup

```toml
[dependencies]
opentelemetry = "0.21"
opentelemetry-otlp = "0.14"
opentelemetry_sdk = { version = "0.21", features = ["rt-tokio"] }
tracing-opentelemetry = "0.22"
```

```rust
use opentelemetry::global;
use opentelemetry_sdk::trace::TracerProvider;
use opentelemetry_otlp::WithExportConfig;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize OpenTelemetry tracer
    let tracer = opentelemetry_otlp::new_pipeline()
        .tracing()
        .with_exporter(
            opentelemetry_otlp::new_exporter()
                .tonic()
                .with_endpoint("http://localhost:4317"),
        )
        .install_batch(opentelemetry_sdk::runtime::Tokio)?;

    // Create tracing layer
    let telemetry_layer = tracing_opentelemetry::layer().with_tracer(tracer);

    // Combine with other layers
    tracing_subscriber::registry()
        .with(telemetry_layer)
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Your application code
    info!("Application started");

    // Cleanup
    global::shutdown_tracer_provider();

    Ok(())
}
```

### Distributed Tracing

```rust
use opentelemetry::trace::{Tracer, SpanKind};
use opentelemetry::global;

#[instrument]
async fn api_handler() -> Result<Response> {
    let tracer = global::tracer("my-service");

    // Create span
    let mut span = tracer
        .span_builder("database_query")
        .with_kind(SpanKind::Client)
        .start(&tracer);

    span.set_attribute(KeyValue::new("db.system", "postgresql"));
    span.set_attribute(KeyValue::new("db.statement", "SELECT * FROM users"));

    let result = query_database().await;

    span.end();

    result
}
```

## Metrics

### Using `metrics` Crate

```toml
[dependencies]
metrics = "0.22"
metrics-exporter-prometheus = "0.13"
```

```rust
use metrics::{counter, gauge, histogram};

fn record_metrics() {
    // Counter: monotonically increasing value
    counter!("requests_total", "method" => "GET", "path" => "/api/users").increment(1);

    // Gauge: value that can go up or down
    gauge!("active_connections").set(42.0);

    // Histogram: distribution of values
    histogram!("request_duration_ms").record(123.45);
}
```

### Prometheus Exporter

```rust
use metrics_exporter_prometheus::PrometheusBuilder;
use std::net::SocketAddr;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Setup Prometheus exporter
    let builder = PrometheusBuilder::new();
    builder
        .install()
        .expect("failed to install Prometheus recorder");

    // Start metrics endpoint
    let addr: SocketAddr = "0.0.0.0:9090".parse()?;
    let handle = tokio::spawn(async move {
        metrics_exporter_prometheus::PrometheusBuilder::new()
            .with_http_listener(addr)
            .install()
            .expect("failed to install Prometheus exporter");
    });

    // Your application
    loop {
        counter!("requests_total").increment(1);
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    }

    Ok(())
}
```

## Application-Level Patterns

### Request ID Tracking

```rust
use tracing::Span;
use uuid::Uuid;

#[instrument(fields(request_id = %Uuid::new_v4()))]
async fn handle_request(req: Request) -> Response {
    info!("Processing request");

    // All logs within this span will include request_id
    process_data().await;

    info!("Request completed");

    Response::ok()
}

async fn process_data() {
    info!("Processing data");  // Includes request_id from parent span
}
```

### Error Context

```rust
use tracing::{error, instrument};

#[instrument(err)]
async fn fetch_user(id: u64) -> Result<User, Error> {
    let user = db.get_user(id).await
        .map_err(|e| {
            error!(error = ?e, user_id = id, "Failed to fetch user");
            e
        })?;

    Ok(user)
}
```

### Performance Monitoring

```rust
use std::time::Instant;
use tracing::info;

#[instrument]
async fn monitored_operation() {
    let start = Instant::now();

    // Do work
    expensive_operation().await;

    let duration = start.elapsed();
    histogram!("operation_duration_ms").record(duration.as_millis() as f64);

    if duration.as_secs() > 1 {
        warn!(duration_ms = duration.as_millis(), "Slow operation detected");
    }
}
```

## Tokio Console

Debug async tasks in real-time.

```toml
[dependencies]
console-subscriber = "0.2"
```

```rust
fn main() {
    console_subscriber::init();

    // Your tokio application
    tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(async {
            // Async code
        });
}
```

```bash
# In another terminal
tokio-console
```

## Best Practices

### Structured Logging

```rust
// Bad
info!("User alice logged in from 192.168.1.1");

// Good
info!(
    user = "alice",
    ip = "192.168.1.1",
    "User logged in"
);
```

### Appropriate Log Levels

```rust
// ERROR: Unrecoverable errors
error!(error = ?e, "Database connection failed");

// WARN: Recoverable issues
warn!(retries = 3, "Request failed, retrying");

// INFO: Important events
info!(user_id = 42, "User logged in");

// DEBUG: Detailed information for debugging
debug!(query = sql, rows = count, "Query executed");

// TRACE: Very detailed, usually disabled
trace!(bytes = len, "Received packet");
```

### Don't Log Secrets

```rust
// Bad
info!(password = user.password, "User logged in");

// Good
#[instrument(skip(password))]
fn login(username: &str, password: &str) {
    info!(username, "Login attempt");
}
```

### Sampling for High-Volume

```rust
use rand::Rng;

fn maybe_log() {
    if rand::thread_rng().gen_ratio(1, 100) {  // 1% sampling
        debug!("High-frequency event");
    }
}
```

### Context Propagation

```rust
use tracing::Span;

#[instrument]
async fn outer_function() {
    let span = Span::current();

    tokio::spawn(async move {
        let _entered = span.entered();
        inner_function().await;
    });
}

async fn inner_function() {
    info!("This log includes context from outer_function");
}
```

## Web Framework Integration

### Axum with Tracing

```rust
use axum::{
    routing::get,
    Router,
};
use tower_http::trace::{TraceLayer, DefaultMakeSpan, DefaultOnResponse};
use tracing::Level;

let app = Router::new()
    .route("/", get(handler))
    .layer(
        TraceLayer::new_for_http()
            .make_span_with(DefaultMakeSpan::new().level(Level::INFO))
            .on_response(DefaultOnResponse::new().level(Level::INFO))
    );
```

### Custom Request Logging

```rust
use tower_http::trace::TraceLayer;
use tracing::{Span, Level};

let trace_layer = TraceLayer::new_for_http()
    .make_span_with(|request: &Request<_>| {
        tracing::span!(
            Level::INFO,
            "http_request",
            method = %request.method(),
            path = %request.uri().path(),
            request_id = %Uuid::new_v4(),
        )
    })
    .on_request(|_request: &Request<_>, _span: &Span| {
        tracing::info!("started processing request");
    })
    .on_response(|response: &Response<_>, latency: Duration, _span: &Span| {
        tracing::info!(
            status = %response.status(),
            latency_ms = latency.as_millis(),
            "finished processing request"
        );
    });
```

## Production Configurations

### JSON Logging for Production

```rust
fn init_production_logging() {
    tracing_subscriber::fmt()
        .json()
        .with_current_span(true)
        .with_span_list(false)
        .with_thread_ids(true)
        .with_target(false)
        .with_timer(tracing_subscriber::fmt::time::SystemTime)
        .init();
}
```

### Development-Friendly Logging

```rust
fn init_dev_logging() {
    tracing_subscriber::fmt()
        .pretty()
        .with_env_filter(EnvFilter::from_default_env())
        .with_target(true)
        .with_line_number(true)
        .with_file(true)
        .init();
}
```

### Dynamic Log Level

```rust
use tracing_subscriber::reload;

fn main() {
    let (filter, _reload_handle) = reload::Layer::new(EnvFilter::from_default_env());

    tracing_subscriber::registry()
        .with(filter)
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Later, reload with new filter
    // reload_handle.modify(|layer| *layer = EnvFilter::new("debug"))?;
}
```

## Key Takeaways

1. **Use `tracing` for new projects**: Better async support and structured logging
2. **Structured fields**: Use key-value pairs instead of formatted strings
3. **Spans for context**: Track operations with spans
4. **Appropriate levels**: ERROR for failures, INFO for important events, DEBUG for details
5. **Don't log secrets**: Always skip sensitive data
6. **Sample high-volume**: Use sampling for very frequent events
7. **JSON in production**: Easier to parse and query
8. **OpenTelemetry for distributed**: Use for microservices
9. **Metrics for monitoring**: Track counters, gauges, histograms
10. **Test logging**: Verify important events are logged correctly

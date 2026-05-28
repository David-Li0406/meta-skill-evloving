# Tracing Instrumentation

## Basic Setup

```rust
use tracing::{info, warn, error, debug, trace, span, Level};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

fn main() {
    // Simple setup
    tracing_subscriber::fmt::init();

    // Or with layers
    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(tracing_subscriber::EnvFilter::from_default_env())
        .init();

    info!("Application started");
}
```

## Events (Logs)

```rust
use tracing::{info, warn, error, debug, trace};

fn process_request(request_id: &str, user_id: u64) {
    // Simple message
    info!("Processing request");

    // With structured fields
    info!(request_id, user_id, "Processing request");

    // Named fields
    info!(
        request_id = %request_id,
        user_id = user_id,
        action = "process",
        "Handling user request"
    );

    // Display vs Debug formatting
    info!(user = %user, "Using Display");  // %
    info!(user = ?user, "Using Debug");    // ?
    
    // Error with source
    if let Err(e) = do_something() {
        error!(error = ?e, "Operation failed");
    }
}
```

## Spans

```rust
use tracing::{span, Level, Instrument};

async fn handle_request(request_id: String) {
    // Create span
    let span = span!(Level::INFO, "handle_request", %request_id);
    let _guard = span.enter(); // Auto-exits when dropped

    info!("Starting request processing");
    
    // Nested span
    {
        let db_span = span!(Level::DEBUG, "database_query");
        let _guard = db_span.enter();
        query_database().await;
    }

    info!("Request completed");
}

// Async with instrument
async fn process() {
    do_work()
        .instrument(span!(Level::INFO, "do_work"))
        .await;
}
```

## Instrument Attribute

```rust
use tracing::instrument;

#[instrument]
fn simple_function(x: i32) -> i32 {
    x * 2
}

#[instrument(
    name = "process_user",
    level = "info",
    skip(password),  // Don't log sensitive data
    fields(user_id = %user.id),
    err,  // Log errors
    ret,  // Log return value
)]
async fn process_user(user: &User, password: &str) -> Result<(), Error> {
    info!("Processing user");
    Ok(())
}

#[instrument(skip_all, fields(request_id = %request.id))]
async fn handle(request: Request) -> Response {
    // Implementation
}
```

## Custom Subscriber

```rust
use tracing_subscriber::{
    fmt,
    layer::SubscriberExt,
    util::SubscriberInitExt,
    EnvFilter,
};

fn setup_tracing() {
    let fmt_layer = fmt::layer()
        .with_target(true)
        .with_thread_ids(true)
        .with_file(true)
        .with_line_number(true)
        .json();  // JSON output

    let filter_layer = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    tracing_subscriber::registry()
        .with(filter_layer)
        .with(fmt_layer)
        .init();
}

// Set level via RUST_LOG env var:
// RUST_LOG=debug
// RUST_LOG=my_crate=debug,other_crate=warn
```

## Integration with Axum

```rust
use axum::{Router, routing::get};
use tower_http::trace::TraceLayer;
use tracing::info_span;

fn app() -> Router {
    Router::new()
        .route("/", get(handler))
        .layer(
            TraceLayer::new_for_http()
                .make_span_with(|request: &Request<_>| {
                    info_span!(
                        "http_request",
                        method = %request.method(),
                        uri = %request.uri(),
                        request_id = %uuid::Uuid::new_v4(),
                    )
                })
        )
}
```

## OpenTelemetry Integration

```rust
use tracing_subscriber::layer::SubscriberExt;
use tracing_opentelemetry::OpenTelemetryLayer;
use opentelemetry::sdk::trace::TracerProvider;

fn setup_otel() {
    let tracer = TracerProvider::builder()
        .with_simple_exporter(opentelemetry_jaeger::new_agent_pipeline().build_simple()?)
        .build()
        .tracer("my-service");

    tracing_subscriber::registry()
        .with(tracing_subscriber::fmt::layer())
        .with(OpenTelemetryLayer::new(tracer))
        .init();
}
```

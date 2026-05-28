#!/usr/bin/env bash
set -euo pipefail

# Set up tracing/logging for a Rust project

echo "📝 Setting up logging with tracing..."

# Add dependencies
echo "Adding tracing dependencies to Cargo.toml..."
cargo add tracing
cargo add tracing-subscriber --features env-filter,json

# Create logging module
mkdir -p src
cat > src/logging.rs << 'RUST'
use tracing_subscriber::{fmt, layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init() {
    tracing_subscriber::registry()
        .with(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into())
        )
        .with(fmt::layer())
        .init();
}

pub fn init_json() {
    tracing_subscriber::registry()
        .with(
            EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into())
        )
        .with(fmt::layer().json())
        .init();
}
RUST

echo ""
echo "✅ Logging setup complete!"
echo ""
echo "Add to your main.rs:"
echo "  mod logging;"
echo "  fn main() {"
echo "      logging::init();"
echo "      // your code"
echo "  }"
echo ""
echo "Set log level with RUST_LOG environment variable:"
echo "  RUST_LOG=debug cargo run"

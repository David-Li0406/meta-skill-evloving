#!/usr/bin/env bash
set -euo pipefail

# Initialize a new Rust project with best practices

PROJECT_NAME="${1:-}"
PROJECT_TYPE="${2:-bin}"  # bin or lib

if [[ -z "$PROJECT_NAME" ]]; then
    echo "Usage: $0 <project-name> [bin|lib]"
    exit 1
fi

echo "Creating Rust project: $PROJECT_NAME (type: $PROJECT_TYPE)"

# Create project
cargo new --$PROJECT_TYPE "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Add common dependencies to Cargo.toml
cat >> Cargo.toml << 'TOML'

[dependencies]
anyhow = "1.0"
thiserror = "1.0"
serde = { version = "1.0", features = ["derive"] }
tracing = "0.1"

[dev-dependencies]
criterion = "0.5"
proptest = "1.0"

[profile.release]
opt-level = 3
lto = "fat"
codegen-units = 1
strip = true

[[bench]]
name = "benchmarks"
harness = false
TOML

# Create benches directory
mkdir -p benches
cat > benches/benchmarks.rs << 'RUST'
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn benchmark_example(c: &mut Criterion) {
    c.bench_function("example", |b| {
        b.iter(|| {
            black_box(42);
        });
    });
}

criterion_group!(benches, benchmark_example);
criterion_main!(benches);
RUST

# Create .gitignore if it doesn't exist
if [[ ! -f .gitignore ]]; then
    cat > .gitignore << 'IGNORE'
/target/
Cargo.lock
.DS_Store
*.swp
*.swo
*~
.idea/
.vscode/
IGNORE
fi

echo "✅ Project created successfully!"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  cargo build"
echo "  cargo test"
echo "  cargo bench"

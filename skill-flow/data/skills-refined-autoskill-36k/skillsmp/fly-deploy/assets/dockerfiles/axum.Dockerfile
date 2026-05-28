# Axum Dockerfile for fly.io
# Multi-stage build for minimal production image

FROM rust:1.75-slim AS builder

WORKDIR /app

# Install required dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy manifests
COPY Cargo.toml Cargo.lock ./

# Create dummy main.rs to cache dependencies
RUN mkdir src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

# Copy actual source code
COPY src ./src

# Build the actual application
# Touch main.rs to force rebuild of application code only
RUN touch src/main.rs && \
    cargo build --release

# Strip the binary to reduce size
RUN strip target/release/$(grep -m1 "^name" Cargo.toml | cut -d '"' -f2)

# Runtime stage
FROM debian:bookworm-slim AS runtime

WORKDIR /app

# Install runtime dependencies (if needed)
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1001 axum

# Copy the binary from builder
# Replace 'my-app' with your actual binary name from Cargo.toml
COPY --from=builder /app/target/release/my-app /usr/local/bin/app

RUN chown axum:axum /usr/local/bin/app

USER axum

EXPOSE 8080

ENV PORT=8080
ENV RUST_LOG=info

CMD ["/usr/local/bin/app"]

# Alternative: Use distroless for even smaller image
# FROM gcr.io/distroless/cc-debian12 AS runtime
# COPY --from=builder /app/target/release/my-app /app
# EXPOSE 8080
# CMD ["/app"]

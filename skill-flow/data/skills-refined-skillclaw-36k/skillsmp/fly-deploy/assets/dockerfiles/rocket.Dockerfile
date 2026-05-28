# Rocket Dockerfile for fly.io
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

# Copy Rocket.toml if it exists
COPY Rocket.toml* ./

# Build the actual application
RUN touch src/main.rs && \
    cargo build --release

# Strip the binary
RUN strip target/release/$(grep -m1 "^name" Cargo.toml | cut -d '"' -f2)

# Runtime stage
FROM debian:bookworm-slim AS runtime

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1001 rocket

# Copy the binary from builder
# Replace 'my-app' with your actual binary name from Cargo.toml
COPY --from=builder /app/target/release/my-app /usr/local/bin/app

# Copy Rocket.toml if it exists
COPY --from=builder /app/Rocket.toml* ./

RUN chown -R rocket:rocket /app /usr/local/bin/app

USER rocket

EXPOSE 8080

ENV ROCKET_ADDRESS=0.0.0.0
ENV ROCKET_PORT=8080
ENV ROCKET_ENV=production

CMD ["/usr/local/bin/app"]

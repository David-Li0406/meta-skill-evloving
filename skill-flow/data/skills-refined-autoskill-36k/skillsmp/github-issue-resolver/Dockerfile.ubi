# Dockerfile - Multi-Stage Build for OpenShift Cluster Health MCP Server
# Red Hat UBI runtime for full OpenShift compatibility
# Target: Container image <50MB

# Stage 1: Build stage (Alpine Go 1.24 for build, UBI Micro for runtime)
FROM docker.io/library/golang:1.24-alpine AS builder

WORKDIR /build

# Copy Go modules files first (better caching)
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build static binary with size optimizations
# CGO_ENABLED=0: Fully static linking (no C dependencies)
# -ldflags="-s -w": Strip debug info and symbol table (reduces binary size)
# -trimpath: Remove file system paths from executable
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w" \
    -trimpath \
    -o /build/mcp-server \
    ./cmd/mcp-server

# Build healthcheck binary for init containers
# This replaces curl-based health checks (curl not available in UBI-micro)
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
    -ldflags="-s -w" \
    -trimpath \
    -o /build/healthcheck \
    ./cmd/healthcheck

# Verify binaries exist
RUN ls -lh /build/mcp-server /build/healthcheck

# Stage 2: Runtime stage (UBI9 Micro - minimal Red Hat base image)
FROM registry.access.redhat.com/ubi9/ubi-micro:latest

# Labels for OpenShift
LABEL name="openshift-cluster-health-mcp" \
      vendor="OpenShift AI Ops" \
      version="0.1.0" \
      summary="MCP server for OpenShift cluster health monitoring" \
      description="Model Context Protocol server providing cluster health monitoring and AI Ops integration for OpenShift"

# Copy binaries from builder
COPY --from=builder /build/mcp-server /usr/local/bin/mcp-server
COPY --from=builder /build/healthcheck /usr/local/bin/healthcheck

# UBI images run as arbitrary UID by default (OpenShift compatible)
# No explicit USER directive needed - OpenShift will assign UID from namespace range

# MCP HTTP transport port (if using HTTP mode)
EXPOSE 8080

# Set entrypoint
ENTRYPOINT ["/usr/local/bin/mcp-server"]

# Docker Official Images

Docker Official Images are curated images maintained by the Docker community with security best practices.

## Overview

| Property | Value |
|----------|-------|
| Provider | Docker Official |
| Registry | `docker.io` |
| Documentation | https://docs.docker.com/trusted-content/official-images/ |
| Security Rating | High |

## Features

- Community maintained
- Regular security updates
- Well-documented
- Multiple architecture support

## Recommended Images by Language

### Node.js

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `node:20-alpine` | Minimal production | Production | Alpine-based, minimal footprint, LTS version |
| `node:20-slim` | Debian compatible | Production | Debian slim, good npm compatibility |
| `node:20-bookworm-slim` | Latest Debian | Production | Debian Bookworm slim base |

### Python

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `python:3.12-alpine` | Minimal production | Production | Alpine-based, may need build tools for some packages |
| `python:3.12-slim` | Debian compatible | Production | Debian slim, good pip compatibility |
| `python:3.12-slim-bookworm` | Latest Debian | Production | Debian Bookworm slim base |

### Go

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `golang:1.22-alpine` | Go builds | Build | Build only, deploy to distroless/chainguard |

### Rust

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `rust:1.77-alpine` | Rust builds | Build | Build only, deploy to distroless/chainguard |

### Ruby

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `ruby:3.3-alpine` | Minimal production | Production | Alpine-based |
| `ruby:3.3-slim` | Debian production | Production | Debian slim |

### Java

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `eclipse-temurin:21-jre-alpine` | Java 21 production | Production | Eclipse Temurin JRE on Alpine |
| `eclipse-temurin:21-jdk-alpine` | Java 21 builds | Build | Eclipse Temurin JDK for building |
| `amazoncorretto:21-alpine` | Java 21 production (Amazon) | Production | Amazon's OpenJDK distribution |

### .NET

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `mcr.microsoft.com/dotnet/aspnet:8.0-alpine` | ASP.NET 8 production | Production | ASP.NET runtime |
| `mcr.microsoft.com/dotnet/runtime:8.0-alpine` | .NET 8 production | Production | .NET runtime |
| `mcr.microsoft.com/dotnet/runtime-deps:8.0-alpine` | .NET 8 self-contained | Production | For self-contained deployments |

### General Purpose

| Image | Use Case | Stage | Notes |
|-------|----------|-------|-------|
| `alpine:3.19` | Minimal general purpose | Production | Very small base, good for custom images |
| `scratch` | Empty image for static binaries | Production | Zero size base, static binaries only |

## Best Practices

1. **Always use specific version tags**: Never use `:latest` in production
2. **Prefer minimal variants**: Use `-alpine` or `-slim` variants for smaller images
3. **Multi-stage builds**: Separate build from runtime stages
4. **Keep updated**: Regularly update base images with security patches

## Example Multi-stage Dockerfile

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
CMD ["node", "dist/index.js"]
```

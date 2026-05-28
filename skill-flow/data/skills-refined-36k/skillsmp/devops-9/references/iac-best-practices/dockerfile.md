# Dockerfile Best Practices Patterns

**Category**: devops/iac-best-practices
**Description**: Dockerfile organizational and operational best practices
**Type**: best-practice

---

## Build Optimization

### Missing Multi-Stage Build
**Pattern**: `^FROM\s+[^\n]+\n(?:(?!FROM\s).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [dockerfile]
- Use multi-stage builds to reduce image size
- Example: Single FROM with build tools in final image
- Remediation: Use `FROM builder AS build` then `FROM runtime` pattern

### Inefficient Layer Caching
**Pattern**: `COPY\s+\.\s+\.\s*\n.*RUN\s+(?:npm|pip|go)\s+install`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Copy dependency files before source for better caching
- Example: `COPY . . && RUN npm install` (bad)
- Remediation: `COPY package*.json ./ && RUN npm install && COPY . .`

### Missing .dockerignore Reference
**Pattern**: `.dockerignore`
**Type**: structural
**Severity**: low
**Languages**: [dockerfile]
- Ensure .dockerignore exists to exclude unnecessary files
- Remediation: Create .dockerignore with node_modules, .git, etc.

---

## Image Size Optimization

### Using Full Base Image
**Pattern**: `FROM\s+(?:node|python|golang|ruby|java):\d+(?!-(?:alpine|slim|distroless))`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Consider using slim or alpine variants for smaller images
- Example: `FROM node:18` (larger)
- Remediation: Use `FROM node:18-alpine` or `FROM node:18-slim`

### Not Cleaning Package Manager Cache
**Pattern**: `RUN\s+apt-get\s+install\s+[^&\n]+$`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Clean package manager cache in same layer
- Remediation: End with `&& rm -rf /var/lib/apt/lists/*`

---

## Metadata Best Practices

### Missing LABEL Instructions
**Pattern**: `^FROM[^\n]+\n(?:(?!LABEL).)*CMD`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Images should have metadata labels
- Remediation: Add `LABEL maintainer="email" version="1.0"`

### Missing WORKDIR
**Pattern**: `^FROM[^\n]+\n(?:(?!WORKDIR).)*(?:COPY|RUN)`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Set explicit WORKDIR instead of relying on defaults
- Remediation: Add `WORKDIR /app` before COPY/RUN

---

## Instruction Best Practices

### Using ADD Instead of COPY
**Pattern**: `ADD\s+(?!https?://)[^\s]+\s+`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Use COPY for local files; ADD only for URLs/archives
- Example: `ADD src/ /app/` (bad)
- Remediation: Use `COPY src/ /app/` (good)

### Combining RUN Instructions
**Pattern**: `RUN\s+[^\n]+\nRUN\s+[^\n]+\nRUN\s+`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Combine related RUN instructions to reduce layers
- Example: Multiple sequential RUN commands
- Remediation: Combine with `&&` in single RUN

### Missing CMD or ENTRYPOINT
**Pattern**: `^(?:(?!CMD|ENTRYPOINT).)*$`
**Type**: regex
**Severity**: medium
**Languages**: [dockerfile]
- Dockerfiles should define how to run the container
- Remediation: Add `CMD ["node", "server.js"]` or `ENTRYPOINT`

---

## Environment Best Practices

### Hardcoded Environment Values
**Pattern**: `ENV\s+(?:PASSWORD|SECRET|KEY|TOKEN)\s*=\s*[^\$][^\s]+`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Don't hardcode secrets in Dockerfile
- Remediation: Use build args or runtime environment variables

### Missing Environment Documentation
**Pattern**: `^(?:(?!ENV).)*CMD`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Document expected environment variables
- Remediation: Add ENV with placeholder values and comments

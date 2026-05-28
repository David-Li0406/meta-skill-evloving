---
name: container-specialist
description: Skill untuk membuat dan mengelola container images menggunakan best practices - UBI9 base images, multi-stage builds, security hardening, dan OpenShift compatibility.
---

# Container Specialist Skill

Skill ini memberikan panduan komprehensif untuk membuat container images yang aman, efisien, dan production-ready untuk PayU Digital Banking Platform.

## When to Use This Skill

Gunakan skill ini ketika:

- Membuat Dockerfile baru untuk microservice
- Memperbaiki atau mengoptimasi Dockerfile yang ada
- Memastikan container image memenuhi standar keamanan
- Menyiapkan images untuk deployment ke OpenShift
- Troubleshooting container build atau runtime issues

---

## 🔒 Mandatory Requirements

### 1. Base Image: Red Hat UBI9

> [!IMPORTANT]
> **WAJIB menggunakan Red Hat Universal Base Image 9 (UBI9)** untuk semua container images.

**Alasan:**

- Certified untuk Red Hat OpenShift
- Security updates dan patches dari Red Hat
- FIPS 140-2 compliant
- Smaller attack surface dibanding full OS images

**Official UBI9 Images:**

| Image                                                     | Use Case                | Size   |
| --------------------------------------------------------- | ----------------------- | ------ |
| `registry.access.redhat.com/ubi9/openjdk-21:1.20`         | Build stage (Java 21)   | ~400MB |
| `registry.access.redhat.com/ubi9/openjdk-21-runtime:1.20` | Runtime stage (Java 21) | ~200MB |
| `registry.access.redhat.com/ubi9/ubi-minimal`             | Minimal base            | ~100MB |
| `registry.access.redhat.com/ubi9/python-312`              | Python 3.12             | ~350MB |

**❌ DILARANG menggunakan:**

- `eclipse-temurin:*-alpine`
- `openjdk:*`
- `amazoncorretto:*`
- Non-UBI base images

---

### 2. Multi-stage Build

> [!IMPORTANT]
> **WAJIB menggunakan multi-stage build** untuk memisahkan build dan runtime environments.

**Benefits:**

- Smaller final image size (50-80% reduction)
- No build tools in production image
- Reduced attack surface
- Better layer caching

**Structure:**

```dockerfile
####
# Build stage
####
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20 AS build
# Build application here...

####
# Runtime stage
####
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:1.20
# Only copy built artifacts
COPY --from=build --chown=185 /build/target/*.jar /deployments/app.jar
```

---

### 3. Non-root User

> [!CAUTION]
> **DILARANG menjalankan container sebagai root user** di runtime stage.

**Default User untuk UBI Images:**

- User ID: `185` (jboss user)
- Group ID: `0` (root group - required for OpenShift)

**Pattern:**

```dockerfile
# Build stage - root OK untuk install dependencies
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20 AS build
USER root
RUN microdnf install -y maven && microdnf clean all
# ... build steps ...

# Runtime stage - HARUS non-root
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:1.20
USER 185
```

**OpenShift Compatibility:**

- OpenShift runs containers with arbitrary UID
- Files must be readable/writable by group `0`
- Use `--chown=185:0` atau `--chown=185`

---

### 4. Mandatory Labels

> [!IMPORTANT]
> **WAJIB menambahkan labels** berikut untuk traceability dan documentation.

```dockerfile
LABEL maintainer="backend-team@payu.id"
LABEL description="PayU Service Name - Brief Description"
LABEL version="1.0.0"
```

**Optional but Recommended Labels:**

```dockerfile
LABEL org.opencontainers.image.title="payu-service-name"
LABEL org.opencontainers.image.description="Detailed description"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.vendor="PayU Indonesia"
LABEL org.opencontainers.image.url="https://github.com/payu/service"
LABEL org.opencontainers.image.source="https://github.com/payu/service"
LABEL org.opencontainers.image.licenses="Proprietary"
```

---

### 5. Health Checks

> [!IMPORTANT]
> **WAJIB menambahkan HEALTHCHECK** untuk container orchestration.

**Spring Boot Services:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/actuator/health || exit 1
```

**Quarkus Services:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:${PORT}/q/health || exit 1
```

**Parameters:**
| Parameter | Value | Description |
|-----------|-------|-------------|
| `--interval` | 30s | Time between health checks |
| `--timeout` | 3s | Maximum time for health check |
| `--start-period` | 30-60s | Grace period before first check |
| `--retries` | 3 | Consecutive failures before unhealthy |

---

## 📁 Dockerfile Templates

### Template: Spring Boot Service

```dockerfile
####
# Build stage - Using Red Hat UBI9 OpenJDK 21 with Maven
####
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20 AS build

USER root
WORKDIR /build

# Install Maven
RUN microdnf install -y maven && microdnf clean all

# Copy pom.xml first for dependency caching
COPY pom.xml ./

# Download dependencies (cached layer)
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the application
RUN mvn package -DskipTests -Dspring-boot.build-image.skip=true && \
    mv target/*.jar target/app.jar

####
# Runtime stage - Using minimal UBI9 OpenJDK 21 runtime
####
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:1.20

LABEL maintainer="backend-team@payu.id"
LABEL description="PayU [SERVICE_NAME] - [DESCRIPTION]"
LABEL version="1.0.0"

# Use non-root user (185 is the default jboss user in UBI images)
USER 185

WORKDIR /deployments

# Copy the built artifact from build stage
COPY --from=build --chown=185 /build/target/app.jar /deployments/app.jar

# Expose the service port
EXPOSE [PORT]

# JVM configuration for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:InitialRAMPercentage=50.0 \
    -XX:+UseG1GC \
    -XX:MaxGCPauseMillis=200 \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:HeapDumpPath=/deployments/heapdump.hprof \
    -Djava.security.egd=file:/dev/./urandom"

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:[PORT]/actuator/health || exit 1

# Run the application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /deployments/app.jar"]
```

---

### Template: Quarkus Service (Fast-JAR)

```dockerfile
####
# Build stage - Using Red Hat UBI9 OpenJDK 21 with Maven
####
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20 AS build

USER root
WORKDIR /build

# Install Maven
RUN microdnf install -y maven && microdnf clean all

# Copy pom.xml first for dependency caching
COPY pom.xml ./

# Download dependencies (cached layer)
RUN mvn dependency:go-offline -B

# Copy source code
COPY src ./src

# Build the Quarkus application (fast-jar format)
RUN mvn package -DskipTests

####
# Runtime stage - Using minimal UBI9 OpenJDK 21 runtime
####
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:1.20

LABEL maintainer="backend-team@payu.id"
LABEL description="PayU [SERVICE_NAME] - [DESCRIPTION]"
LABEL version="1.0.0"

# Use non-root user (185 is the default jboss user in UBI images)
USER 185

WORKDIR /deployments

# Copy Quarkus fast-jar structure
COPY --from=build --chown=185 /build/target/quarkus-app/lib/ /deployments/lib/
COPY --from=build --chown=185 /build/target/quarkus-app/*.jar /deployments/
COPY --from=build --chown=185 /build/target/quarkus-app/app/ /deployments/app/
COPY --from=build --chown=185 /build/target/quarkus-app/quarkus/ /deployments/quarkus/

# Expose the service port
EXPOSE [PORT]

# JVM configuration for Quarkus
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:+UseG1GC \
    -XX:MaxGCPauseMillis=100 \
    -Dquarkus.http.host=0.0.0.0 \
    -Djava.util.logging.manager=org.jboss.logmanager.LogManager"

# Health check using Quarkus health endpoint
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:[PORT]/q/health || exit 1

# Run the Quarkus application
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /deployments/quarkus-run.jar"]
```

---

### Template: Quarkus Native (GraalVM)

```dockerfile
####
# Build stage - GraalVM Native Image
####
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20 AS build

USER root
WORKDIR /build

# Install Maven and native-image requirements
RUN microdnf install -y maven gcc glibc-devel zlib-devel && \
    microdnf clean all

COPY pom.xml ./
RUN mvn dependency:go-offline -B

COPY src ./src
RUN mvn package -DskipTests -Pnative

####
# Runtime stage - Minimal for native
####
FROM registry.access.redhat.com/ubi9/ubi-minimal:9.3

LABEL maintainer="backend-team@payu.id"
LABEL description="PayU [SERVICE_NAME] - [DESCRIPTION] (Native)"
LABEL version="1.0.0"

USER 185
WORKDIR /deployments

COPY --from=build --chown=185 /build/target/*-runner /deployments/app

EXPOSE [PORT]

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:[PORT]/q/health || exit 1

ENTRYPOINT ["/deployments/app", "-Dquarkus.http.host=0.0.0.0"]
```

---

## ⚙️ JVM Configuration

### Container-Aware JVM Settings

```dockerfile
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:InitialRAMPercentage=50.0 \
    -XX:+UseG1GC \
    -XX:MaxGCPauseMillis=200 \
    -XX:+HeapDumpOnOutOfMemoryError \
    -XX:HeapDumpPath=/deployments/heapdump.hprof \
    -Djava.security.egd=file:/dev/./urandom"
```

**Explanation:**

| Setting                      | Value          | Purpose                               |
| ---------------------------- | -------------- | ------------------------------------- |
| `UseContainerSupport`        | enabled        | JVM respects container memory limits  |
| `MaxRAMPercentage`           | 75%            | Maximum heap as % of container memory |
| `InitialRAMPercentage`       | 50%            | Initial heap as % of container memory |
| `UseG1GC`                    | enabled        | G1 garbage collector (recommended)    |
| `MaxGCPauseMillis`           | 100-200ms      | Target GC pause time                  |
| `HeapDumpOnOutOfMemoryError` | enabled        | Dump heap on OOM for debugging        |
| `java.security.egd`          | /dev/./urandom | Faster random number generation       |

---

## 🔐 Security Best Practices

### 1. No Secrets in Images

```dockerfile
# ❌ SALAH - secrets di image
ENV DATABASE_PASSWORD=mysecret

# ✅ BENAR - secrets dari environment/secrets
ENV DATABASE_PASSWORD=""
```

### 2. Clean Up After Install

```dockerfile
# ✅ BENAR - clean up dalam satu layer
RUN microdnf install -y maven && \
    mvn package -DskipTests && \
    microdnf remove -y maven && \
    microdnf clean all && \
    rm -rf /var/cache/yum
```

### 3. Use .dockerignore

```dockerignore
# .dockerignore
.git
.gitignore
*.md
Dockerfile
.dockerignore
target/
!target/*.jar
node_modules/
.env
*.log
```

### 4. Pin Image Versions

```dockerfile
# ✅ BENAR - pinned version
FROM registry.access.redhat.com/ubi9/openjdk-21:1.20

# ❌ SALAH - floating tag
FROM registry.access.redhat.com/ubi9/openjdk-21:latest
```

---

## 📊 Port Assignments

| Service              | Port | Protocol |
| -------------------- | ---- | -------- |
| account-service      | 8001 | HTTP     |
| auth-service         | 8002 | HTTP     |
| transaction-service  | 8003 | HTTP     |
| wallet-service       | 8004 | HTTP     |
| billing-service      | 8005 | HTTP     |
| notification-service | 8006 | HTTP     |
| gateway-service      | 8080 | HTTP     |
| bi-fast-simulator    | 8090 | HTTP     |
| dukcapil-simulator   | 8091 | HTTP     |
| qris-simulator       | 8092 | HTTP     |

---

## 🏗️ Build Commands

### Build Image

```bash
# Build dengan tag
docker build -t payu/account-service:1.0.0 ./backend/account-service

# Build dengan multiple tags
docker build \
  -t payu/account-service:1.0.0 \
  -t payu/account-service:latest \
  ./backend/account-service

# Build dengan build args
docker build \
  --build-arg MAVEN_OPTS="-Xmx1g" \
  -t payu/account-service:1.0.0 \
  ./backend/account-service
```

### Build for OpenShift

```bash
# Build menggunakan Podman (OpenShift native)
podman build -t payu/account-service:1.0.0 ./backend/account-service

# Push to OpenShift internal registry
podman push payu/account-service:1.0.0 \
  image-registry.openshift-image-registry.svc:5000/payu-dev/account-service:1.0.0
```

---

## 🔍 Verification Checklist

Sebelum merge, pastikan Dockerfile memenuhi checklist berikut:

- [ ] Base image menggunakan UBI9 (`registry.access.redhat.com/ubi9/...`)
- [ ] Multi-stage build (minimal 2 stages: build dan runtime)
- [ ] Non-root user di runtime stage (`USER 185`)
- [ ] Labels: maintainer, description, version
- [ ] HEALTHCHECK dengan parameter yang sesuai
- [ ] EXPOSE dengan port yang benar
- [ ] JVM container-aware settings (MaxRAMPercentage, UseContainerSupport)
- [ ] Tidak ada secrets hardcoded
- [ ] .dockerignore file exists
- [ ] Image version di-pin (tidak menggunakan `:latest`)

---

## 📚 Related Resources

| Resource               | Path                                      |
| ---------------------- | ----------------------------------------- |
| PayU Development Skill | `.agent/skills/payu-development/SKILL.md` |
| Code Review Skill      | `.agent/skills/code-review/SKILL.md`      |
| Architecture           | `ARCHITECTURE.md`                         |

---

_Last Updated: January 2026_

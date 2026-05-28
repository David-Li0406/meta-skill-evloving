---
name: azure-containerization
description: Docker containerization and Azure deployment best practices for .NET 10 applications. Use when creating Dockerfiles, docker-compose files, or configuring container deployments to Azure Container Apps, App Service, or AKS.
---

# Azure Containerization for .NET 10

Use this skill when containerizing .NET 10 applications for Azure deployment.

## When to Use This Skill

- Creating Dockerfiles for .NET 10 applications
- Setting up local development with Docker Compose
- Deploying to Azure Container Apps
- Deploying to Azure App Service (container)
- Deploying to Azure Kubernetes Service (AKS)

## Template Files

See the [templates](./templates/) directory for ready-to-use files:
- [Dockerfile](./templates/Dockerfile) - Multi-stage .NET 10 Dockerfile
- [docker-compose.yml](./templates/docker-compose.yml) - Local development compose
- [.dockerignore](./templates/.dockerignore) - Files to exclude from build

## Best Practices

### 1. Use Multi-Stage Builds

Multi-stage builds reduce final image size by excluding build tools:

```dockerfile
# Build stage - includes SDK
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
# ... build commands

# Runtime stage - smaller image
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
# ... only runtime files
```

### 2. Use Specific Image Tags

Never use `latest` in production:

```dockerfile
# ✅ Good - specific version
FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine

# ❌ Bad - unpredictable
FROM mcr.microsoft.com/dotnet/aspnet:latest
```

### 3. Implement Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

### 4. Run as Non-Root User

```dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

### 5. Use .dockerignore

Exclude unnecessary files to speed up builds and reduce image size.

### 6. Configure Proper Logging

Use stdout/stderr for container logs:

```csharp
builder.Logging.AddConsole();
builder.Logging.AddJsonConsole(); // For structured logs
```

### 7. Environment Variables for Configuration

```dockerfile
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080
```

## Azure Container Apps Configuration

```yaml
# container-app.yaml
properties:
  configuration:
    ingress:
      external: true
      targetPort: 8080
    secrets:
      - name: connection-string
        value: ${CONNECTION_STRING}
  template:
    containers:
      - image: myregistry.azurecr.io/myapp:latest
        name: myapp
        resources:
          cpu: 0.5
          memory: 1Gi
        probes:
          - type: liveness
            httpGet:
              path: /health
              port: 8080
          - type: readiness
            httpGet:
              path: /health/ready
              port: 8080
```

## Azure App Service (Container) Configuration

```json
{
  "WEBSITES_PORT": "8080",
  "DOCKER_REGISTRY_SERVER_URL": "https://myregistry.azurecr.io",
  "DOCKER_REGISTRY_SERVER_USERNAME": "myregistry",
  "DOCKER_REGISTRY_SERVER_PASSWORD": "@Microsoft.KeyVault(...)"
}
```

## PHP to Container Migration Notes

| PHP | .NET Container |
|-----|----------------|
| Apache/Nginx | Kestrel (built-in) |
| php.ini | appsettings.json + env vars |
| .env | Environment variables |
| storage/ folder | Azure Blob Storage |
| sessions | Redis / Azure Cache |
| logs | stdout → Azure Monitor |

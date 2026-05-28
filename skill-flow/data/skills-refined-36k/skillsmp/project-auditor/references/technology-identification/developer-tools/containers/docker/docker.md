# Docker

**Category**: developer-tools/containers
**Description**: Container platform for building, shipping, and running applications
**Homepage**: https://www.docker.com

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `dockerode` - Docker API client for Node.js
- `docker-compose` - Docker Compose for Node.js
- `@docker/cli` - Docker CLI library

#### PYPI
- `docker` - Docker SDK for Python
- `docker-compose` - Docker Compose library
- `dockerfile-parse` - Dockerfile parser

#### GO
- `github.com/docker/docker` - Docker Go client
- `github.com/docker/cli` - Docker CLI library
- `github.com/docker/compose` - Docker Compose library
- `github.com/moby/moby` - Moby project

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### Configuration Files
*Known configuration files that indicate Docker usage*

- `Dockerfile` - Main Dockerfile
- `Dockerfile.*` - Environment-specific Dockerfiles (Dockerfile.dev, Dockerfile.prod)
- `*.Dockerfile` - Named Dockerfiles
- `.dockerignore` - Docker ignore file
- `docker-compose.yml` - Docker Compose configuration
- `docker-compose.yaml` - Docker Compose configuration
- `docker-compose.*.yml` - Environment-specific compose files
- `docker-compose.*.yaml` - Environment-specific compose files
- `compose.yml` - Docker Compose v2 configuration
- `compose.yaml` - Docker Compose v2 configuration
- `.docker/config.json` - Docker client configuration

### Configuration Directories
*Known directories that indicate Docker usage*

- `.docker/` - Docker configuration directory

### Code Patterns
*Dockerfile-specific patterns*

**Pattern**: `^FROM\s+`
- Base image declaration
- Example: `FROM node:18-alpine`

**Pattern**: `^RUN\s+`
- Run command
- Example: `RUN npm install`

**Pattern**: `^COPY\s+`
- Copy files
- Example: `COPY package*.json ./`

**Pattern**: `^ADD\s+`
- Add files
- Example: `ADD . /app`

**Pattern**: `^WORKDIR\s+`
- Set working directory
- Example: `WORKDIR /app`

**Pattern**: `^EXPOSE\s+`
- Expose ports
- Example: `EXPOSE 3000`

**Pattern**: `^ENV\s+`
- Set environment variable
- Example: `ENV NODE_ENV=production`

**Pattern**: `^CMD\s+`
- Default command
- Example: `CMD ["node", "server.js"]`

**Pattern**: `^ENTRYPOINT\s+`
- Entry point
- Example: `ENTRYPOINT ["./docker-entrypoint.sh"]`

**Pattern**: `^ARG\s+`
- Build argument
- Example: `ARG VERSION=latest`

**Pattern**: `^LABEL\s+`
- Image label
- Example: `LABEL maintainer="dev@example.com"`

**Pattern**: `^HEALTHCHECK\s+`
- Health check
- Example: `HEALTHCHECK CMD curl -f http://localhost/`

*Docker Compose patterns*

**Pattern**: `^services:\s*$`
- Services section in compose file
- Example: `services:`

**Pattern**: `^\s+image:\s*`
- Image specification
- Example: `image: nginx:latest`

**Pattern**: `^\s+build:\s*`
- Build specification
- Example: `build: .`

**Pattern**: `^\s+ports:\s*$`
- Ports mapping
- Example: `ports:`

**Pattern**: `^\s+volumes:\s*$`
- Volumes mapping
- Example: `volumes:`

---

## Environment Variables

- `DOCKER_HOST` - Docker daemon socket
- `DOCKER_TLS_VERIFY` - TLS verification
- `DOCKER_CERT_PATH` - Path to TLS certificates
- `DOCKER_BUILDKIT` - Enable BuildKit
- `DOCKER_CONFIG` - Docker config directory
- `COMPOSE_PROJECT_NAME` - Docker Compose project name
- `COMPOSE_FILE` - Docker Compose file location
- `COMPOSE_PROFILES` - Active profiles

## Detection Notes

- `Dockerfile` is the strongest indicator of Docker usage
- `docker-compose.yml` indicates multi-container applications
- `.dockerignore` files indicate Docker-aware development
- Multi-stage builds (`FROM ... AS ...`) indicate mature Docker usage
- Docker is primarily detected through configuration files, not packages

---

## TIER 3: Configuration Extraction

These patterns extract specific configuration values for infrastructure inventory.

### Container Registry Extraction

**Pattern**: `^FROM\s+([0-9]{12})\.dkr\.ecr\.([a-z0-9-]+)\.amazonaws\.com/([^:\s]+)`
- AWS ECR registry
- Extracts: `aws_account_id`, `aws_region`, `repository`
- Example: `FROM 123456789012.dkr.ecr.us-west-2.amazonaws.com/myapp:latest`

**Pattern**: `^FROM\s+(gcr\.io|us\.gcr\.io|eu\.gcr\.io|asia\.gcr\.io)/([^/]+)/([^:\s]+)`
- Google Container Registry
- Extracts: `registry_host`, `project_id`, `repository`
- Example: `FROM gcr.io/my-project/myapp:v1`

**Pattern**: `^FROM\s+([a-z0-9-]+-docker\.pkg\.dev)/([^/]+)/([^/]+)/([^:\s]+)`
- Google Artifact Registry
- Extracts: `registry_host`, `project_id`, `repo_name`, `image`
- Example: `FROM us-docker.pkg.dev/my-project/my-repo/myapp:latest`

**Pattern**: `^FROM\s+([a-z0-9]+)\.azurecr\.io/([^:\s]+)`
- Azure Container Registry
- Extracts: `registry_name`, `repository`
- Example: `FROM myregistry.azurecr.io/myapp:latest`

**Pattern**: `^FROM\s+ghcr\.io/([^/]+)/([^:\s]+)`
- GitHub Container Registry
- Extracts: `owner`, `repository`
- Example: `FROM ghcr.io/myorg/myapp:latest`

### Base Image Extraction

**Pattern**: `^FROM\s+([a-z0-9._-]+(?:/[a-z0-9._-]+)?)(:[a-z0-9._-]+)?(?:\s+AS\s+(\w+))?`
- Base image used in build
- Extracts: `base_image`, `tag`, `stage_name`
- Example: `FROM node:18-alpine AS builder`

### Exposed Ports Extraction

**Pattern**: `^EXPOSE\s+(\d+(?:/(?:tcp|udp))?)`
- Exposed ports
- Extracts: `port`, `protocol`
- Example: `EXPOSE 8080/tcp`

### Health Check Extraction

**Pattern**: `^HEALTHCHECK\s+(?:--interval=(\S+)\s+)?(?:--timeout=(\S+)\s+)?CMD\s+(.+)$`
- Health check configuration
- Extracts: `interval`, `timeout`, `command`
- Example: `HEALTHCHECK --interval=30s CMD curl -f http://localhost/health`

### Extraction Output Example

```json
{
  "extractions": {
    "container_registries": [
      {
        "type": "ecr",
        "url": "123456789012.dkr.ecr.us-west-2.amazonaws.com/myapp",
        "aws_account_id": "123456789012",
        "aws_region": "us-west-2",
        "repository": "myapp",
        "source_file": "Dockerfile",
        "line": 1
      }
    ],
    "base_images": [
      {
        "image": "node:18-alpine",
        "stage": "builder",
        "source_file": "Dockerfile",
        "line": 1
      }
    ],
    "exposed_ports": [
      {
        "port": "3000",
        "protocol": "tcp",
        "source_file": "Dockerfile",
        "line": 15
      }
    ]
  }
}
```

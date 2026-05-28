---
name: docker-compose
description: Use this skill for managing multi-container Docker applications, including orchestration, service management, networking, and volumes. Ideal for local development, testing, and production environments.
---

# Docker Compose Skill

## Overview

Docker Compose enables defining and running multi-container applications using declarative YAML configuration. This skill covers Compose v2 with file format 3.8+ and provides comprehensive management for orchestrating services, networks, and volumes.

## When to Use

- Managing local development environments
- Orchestrating multi-container applications
- Debugging service connectivity and networking
- Monitoring container logs and health
- Building and updating service images
- Testing containerized application stacks
- Troubleshooting service failures
- Managing application lifecycle (start, stop, restart)

## Requirements

- Docker Engine installed and running
- Docker Compose V2 (docker compose) or V1 (docker-compose)
- Valid `docker-compose.yml` file in the project
- Appropriate permissions for Docker socket access

## Compose File Structure

### Basic Template

```yaml
# compose.yaml (preferred) or docker-compose.yml
services:
  app:
    image: node:20-alpine
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
    environment:
      - NODE_ENV=development

networks:
  default:
    driver: bridge

volumes:
  app-data:
```

## Common Workflows

### Start a Development Environment

```bash
# 1. Validate configuration
docker compose config

# 2. Pull latest images
docker compose pull

# 3. Build custom images
docker compose build

# 4. Start services in detached mode
docker compose up -d

# 5. Check service status
docker compose ps

# 6. View logs
docker compose logs --tail 100
```

### Troubleshoot a Failing Service

```bash
# 1. Check container status
docker compose ps --all

# 2. View service logs
docker compose logs --tail 200 failing-service

# 3. Inspect running processes
docker compose top failing-service

# 4. Check configuration
docker compose config

# 5. Restart the service
docker compose restart failing-service

# 6. If needed, recreate container
docker compose up -d --force-recreate failing-service
```

## Service Management

### Essential Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Rebuild services
docker compose build

# Execute command in container
docker compose exec <service> <command>
```

### Health Checks

```yaml
services:
  api:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Networking and Volumes

### Custom Network Configuration

```yaml
networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true # No external access
```

### Named Volumes

```yaml
services:
  db:
    volumes:
      - postgres-data:/var/lib/postgresql/data

volumes:
  postgres-data:
    driver: local
```

## Best Practices

- Verify `docker-compose.yml` exists before operations.
- Use project names for isolation.
- Check service status before destructive operations.
- Avoid volume removal without confirmation.
- Review logs before restarting failed services.

## Error Handling

**Common Errors**:

| Error                             | Cause                 | Fix                                             |
| --------------------------------- | --------------------- | ----------------------------------------------- |
| `docker: command not found`       | Docker not installed  | Install Docker Engine                           |
| `Cannot connect to Docker daemon` | Docker not running    | Start Docker service                            |
| `network ... not found`           | Network cleanup issue | Run `docker compose down` then `up`             |
| `port is already allocated`       | Port conflict         | Change port mapping or stop conflicting service |
| `no configuration file provided`  | Missing compose file  | Create `docker-compose.yml`                     |

## Logging Configuration

```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "5"
```

## Related Skills

- [`cloud-devops-expert`](../cloud-devops-expert/SKILL.md) - Cloud platforms (AWS, GCP, Azure) and Terraform infrastructure

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
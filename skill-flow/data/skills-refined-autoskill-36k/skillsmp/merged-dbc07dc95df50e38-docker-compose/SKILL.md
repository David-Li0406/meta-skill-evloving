---
name: docker-compose
description: Use this skill for managing multi-container Docker applications, including orchestration, service management, and troubleshooting. Ideal for local development, testing, and deployment of containerized applications.
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
- Valid `docker-compose.yml` file in project
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

## Tools

The skill provides tools across service management, monitoring, build operations, and troubleshooting categories:

### Service Management

- **up**: Start services defined in `docker-compose.yml`.
- **down**: Stop and remove containers, networks, volumes.
- **start**: Start existing containers without recreating them.
- **stop**: Stop running containers without removing them.
- **restart**: Restart services (stop + start).

### Status & Logs

- **ps**: List containers with status information.
- **logs**: View service logs with streaming support.
- **top**: Display running processes in containers.

### Build & Images

- **build**: Build or rebuild service images.
- **pull**: Pull service images from the registry.
- **images**: List images used by services.

### Execution

- **exec**: Execute a command in a running container.
- **run**: Run a one-off command in a new container.

### Configuration

- **config**: Validate and view the Compose file configuration.
- **port**: Print the public port binding for a service port.

## Best Practices

- Verify `docker-compose.yml` exists before operations.
- Use project names for isolation.
- Check service status before destructive operations.
- Avoid volume removal without confirmation.
- Review logs before restarting failed services.

## Safety Features

### Blocked Operations

The following operations are **BLOCKED** by default to prevent accidental data loss:

- **Volume removal**: `docker compose down -v` (BLOCKED - requires manual confirmation)
- **Destructive exec**: `rm -rf`, `dd`, `mkfs` inside containers (BLOCKED)

### Confirmation Required

These operations require explicit confirmation:

- Building with `--no-cache` (resource-intensive)
- Pulling images in production environments
- Starting services with `--force-recreate`

## Error Handling

**Common Errors**:

| Error                             | Cause                 | Fix                                             |
| --------------------------------- | --------------------- | ----------------------------------------------- |
| `docker: command not found`       | Docker not installed  | Install Docker Engine                           |
| `Cannot connect to Docker daemon` | Docker not running    | Start Docker service                            |
| `network ... not found`           | Network cleanup issue | Run `docker compose down` then `up`             |

## Related Skills

- [`cloud-devops-expert`](../cloud-devops-expert/SKILL.md) - Cloud platforms (AWS, GCP, Azure) and Terraform infrastructure

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
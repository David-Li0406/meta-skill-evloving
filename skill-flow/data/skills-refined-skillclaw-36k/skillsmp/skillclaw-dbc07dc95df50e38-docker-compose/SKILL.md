---
name: docker-compose
description: Use this skill when you need to define and manage multi-container Docker applications, including orchestration, networking, and volume management for local development and production environments.
---

# Skill body

## Overview

Docker Compose enables defining and running multi-container applications using declarative YAML configuration. This skill covers Compose v2 with file format 3.8+.

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

### Full Structure Reference

```yaml
services: # Container definitions
networks: # Network configurations
volumes: # Named volume definitions
configs: # Configuration objects
secrets: # Sensitive data
```

## Services Configuration

### Image-Based Service

```yaml
services:
  api:
    image: nginx:alpine
    container_name: my-api
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    labels:
      - "traefik.enable=true"
```

### Build-Based Service

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_ENV: development
      cache_from:
        - myapp:cache
    image: myapp:latest
```

### Advanced Build Options

```yaml
services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.dev
      args:
        - BUILD_ENV=development
      labels:
        - "com.example.version=1.0"
      platforms:
        - linux/amd64
        - linux/arm64
      secrets:
        - npm_token
      ssh:
        - default
```

## Networks

### Custom Network Configuration

```yaml
services:
  frontend:
    networks:
      - frontend-net

  backend:
    networks:
      - frontend-net
      - backend-net

  database:
    networks:
      - backend-net

networks:
  frontend-net:
    driver: bridge
  backend-net:
    driver: bridge
    internal: true # No external access
```

### Network with Custom IPAM

```yaml
networks:
  app-network:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 172.28.0.0/16
          gateway: 172.28.0.1
```

### External Networks

```yaml
networks:
  proxy-network:
    external: true
    name: nginx-prox
```

## Best Practices

- Verify `docker-compose.yml` exists before operations.
- Use project names for isolation.
- Check service status before destructive operations.
- Avoid volume removal without confirmation.
- Review logs before restarting failed services.

## Quick Reference

```bash
# List running services
docker compose ps

# View service logs
docker compose logs <service>

# Start services
docker compose up -d

# Stop services
docker compose down

# Rebuild services
docker compose build

# Execute command in container
docker compose exec <service> <command>
```

## Requirements

- Docker Engine installed and running.
- Docker Compose V2 (docker compose) or V1 (docker-compose).
- Valid `docker-compose.yml` file in project.
- Appropriate permissions for Docker socket access.
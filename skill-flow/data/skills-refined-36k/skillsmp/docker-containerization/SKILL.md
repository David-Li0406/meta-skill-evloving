---
name: docker-containerization
description: Dockerfiles, multi-stage builds, and compose for dev/prod.
---

# Docker & Containerization

## When to use this skill
- Creating `Dockerfile` or `docker-compose.yml`.
- Optimizing image size.
- Debugging container networking.

## 1. Dockerfile Best Practices
- **Multi-Stage**: Use multi-stage builds to keep production images small (e.g., build in `node:20`, run in `node:20-alpine`).
- **Ordering**: Place frequent changes (code copying) AFTER infrequent changes (npm install) to leverage layer caching.
- **User**: Don't run as root. User `USER node` or create a non-root user.

## 2. Docker Compose
- **Services**: Define services clearly (`app`, `db`, `redis`).
- **Volumes**: Use named volumes for persistence (`postgres_data:/var/lib/postgresql/data`).
- **Env**: Use `.env` file for environment variables.

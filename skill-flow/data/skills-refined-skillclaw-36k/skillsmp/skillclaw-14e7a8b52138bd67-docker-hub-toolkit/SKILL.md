---
name: docker-hub-toolkit
description: Use this skill when you need to automate the deployment of Python projects to Docker Hub, including building optimized Docker images and setting up CI/CD pipelines.
---

# Skill body

## What This Skill Does

- Generates optimized multi-stage Dockerfiles (base → builder → dev → production)
- Builds, tags, and pushes images to Docker Hub
- Creates CI/CD pipelines (GitHub Actions) for automated deployment
- Optimizes image size and build speed with BuildKit caching
- Sets up multi-platform builds (amd64/arm64)
- Generates `.dockerignore` and `docker-compose.yml`
- Scans images for security vulnerabilities
- Debugs failed Docker builds

## What This Skill Does NOT Do

- Deploy to Kubernetes/ECS/cloud orchestrators (container runtime only)
- Manage Docker Hub billing or account settings
- Handle non-Python project images
- Create Docker Swarm or cluster configurations
- Manage Docker Hub webhooks or automated test integrations

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Python framework (FastAPI/Flask/Django), entry point, dependencies file |
| **Conversation** | Docker Hub username, image name, target platforms, version tag |
| **User Guidelines** | Team Docker standards, naming conventions, security requirements |

Ensure all required context is gathered before implementing. Only ask the user for THEIR specific requirements (domain expertise is in this skill).

## Required Clarifications

Ask about USER'S context:

1. **Docker Hub credentials**: "What is your Docker Hub username/namespace?"
2. **Project type**: "What Python framework? (FastAPI, Flask, Django, script)"
3. **Entry point**: "What command starts your app? (e.g., `uvicorn app.main:app`)"
4. **Deployment target**: "Local push, or automated CI/CD via GitHub Actions?"

## Workflow

### Full Deployment Pipeline

```
1. Generate Dockerfile    → Multi-stage optimized build
2. Create .dockerignore   → Exclude unnecessary files
3. Build image
4. Tag image
5. Push image to Docker Hub
6. Set up CI/CD pipeline
```
---
name: generating-docker-compose-files
description: Use this skill when you need to generate Docker Compose configurations for multi-container applications, ensuring best practices for production-ready deployments.
---

# Skill body

## Overview

This skill empowers Claude to create fully functional Docker Compose files, streamlining the deployment of complex applications. It automatically incorporates recommended configurations for service dependencies, data persistence, and resource optimization.

## How It Works

1. **Receiving User Input**: Claude interprets the user's request, identifying the application's architecture and dependencies.
2. **Generating Compose Configuration**: Based on the interpreted request, Claude generates a `docker-compose.yml` file defining services, networks, volumes, and other configurations.
3. **Presenting the Configuration**: Claude provides the generated `docker-compose.yml` file to the user.

## When to Use This Skill

This skill activates when you need to:
- Generate a Docker Compose file for a multi-container application.
- Define service dependencies and network configurations for a Docker environment.
- Manage persistent data using Docker volumes.
- Configure health checks and resource limits for Docker containers.

## Examples

### Example 1: Deploying a Full-Stack Application

User request: "Generate a docker-compose file for a full-stack application with a Node.js frontend, a Python backend, and a PostgreSQL database."

The skill will:
1. Generate a `docker-compose.yml` file defining three services: `frontend`, `backend`, and `database`.
2. Configure network connections between the services and define volumes for persistent database storage.

### Example 2: Adding Health Checks

User request: "Create a docker-compose file for a Redis server with a health check."

The skill will:
1. Generate a `docker-compose.yml` file defining a Redis service with a health check configuration.
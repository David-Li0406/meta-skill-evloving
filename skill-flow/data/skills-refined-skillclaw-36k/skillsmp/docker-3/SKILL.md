---
name: docker
description: Generates Dockerfile for application containerization and deployment. Defines multi-stage build process with Node.js build stage and nginx serving stage for production deployment.
---

# Docker Skill

## Purpose
Generate Docker-related files for containerization and deployment.

## Output
Create the file: `Dockerfile`

## Example File
See: `examples.md` in this directory for complete example.

## Notes
- Uses Ubuntu Node.js base image with version that matches the local node version
- Runs quality checks during build: linting, style checking, and unit tests
- Installs and configures nginx for serving the built application
- Cleans up apt cache to reduce image size
- Uses entrypoint script for runtime configuration
- Integrates with Datadog for source code tracking, **if datadog has been installed**
- Securely handles GitHub Packages authentication using Docker secrets, **if component library has been installed**
- Removes .npmrc after installation for security, **if component library has been installed**

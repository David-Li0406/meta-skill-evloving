---
name: docker
description: Container runtime commands including run, exec, build, images, volumes, networks, and compose operations.
---

# Docker — Quick Reference

**Container Management**

```bash
# Start container with interactive shell
docker run -ti <image-name> /bin/bash

# Run container in background
docker run -d <image-name>

# Shell into running container
docker exec -ti <container-name> bash

# See container logs
docker logs <container-id>

# Copy files between container and host
docker cp foo.txt mycontainer:/foo.txt

# Publish port
docker run -p localhost-port:container-port <image-name>

# Get container process ID
docker inspect --format '{{.State.Pid}}' <container-name>
```

**Images**

```bash
# Build image
docker build -t <image-tag> <path-of-Dockerfile>

# List all images
docker images

# List only image IDs
docker image ls -q

# Remove image
docker image rm <image-name-or-id>

# Tag image
docker image tag <image-name>:<tag> <image-name>:<new-tag>

# Save image as tar
docker save -o archive-name.tar <image-name>

# Load image from tar
docker load -i archive-name.tar
```

**Cleanup**

```bash
# Remove all stopped containers
docker container prune
docker rm $(docker ps -qa)

# Remove all untagged images
docker rmi $(docker images | grep "^<none>" | awk '{print $3}')

# Remove unused volumes
docker volume prune

# Full system cleanup
docker system prune -af
```

**Networks**

```bash
# List networks
docker network ls

# Create network
docker network create "<network_name>"

# Connect container to network
docker network connect "<network_id|name>" "<container_id|name>"

# Disconnect container from network
docker network disconnect "<network_id|name>" "<container_id|name>"
```

**Volumes**

```bash
# Create volume
docker volume create <volume-name>

# Inspect volume
docker volume inspect <volume-name>

# Use volume in container
docker run -v <volume-name>:<folder-path> <image>
```

**Docker Compose**

```bash
docker compose up -d --build
docker compose ps
docker compose logs
docker compose exec -it nginx sh
docker compose restart
docker compose stop
docker compose start
```

🔗 [cheat.sh/docker](https://cheat.sh/docker)
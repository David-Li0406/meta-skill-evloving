# Docker Commands Cheatsheet

Quick reference for all essential Docker commands.

---

## Container Commands

| Command | Description |
|---------|-------------|
| `docker run image` | Create and start container |
| `docker run -d image` | Run in background (detached) |
| `docker run -it image` | Run interactive with terminal |
| `docker run --rm image` | Remove when stopped |
| `docker run -p 8000:80 image` | Map port host:container |
| `docker run --name myapp image` | Give container a name |
| `docker run -e VAR=value image` | Set environment variable |
| `docker run -v /host:/container image` | Mount volume |

### Managing Containers

| Command | Description |
|---------|-------------|
| `docker ps` | List running containers |
| `docker ps -a` | List all containers |
| `docker stop <id/name>` | Stop container |
| `docker start <id/name>` | Start stopped container |
| `docker restart <id/name>` | Restart container |
| `docker rm <id/name>` | Remove container |
| `docker rm -f <id/name>` | Force remove running container |

### Inspect & Debug

| Command | Description |
|---------|-------------|
| `docker logs <id/name>` | View logs |
| `docker logs -f <id/name>` | Follow logs |
| `docker exec -it <id/name> bash` | Shell into container |
| `docker exec <id/name> command` | Run command in container |
| `docker inspect <id/name>` | Detailed info (JSON) |
| `docker top <id/name>` | Running processes |
| `docker stats` | Live resource usage |

---

## Image Commands

| Command | Description |
|---------|-------------|
| `docker images` | List images |
| `docker pull image:tag` | Download image |
| `docker build -t name:tag .` | Build from Dockerfile |
| `docker build --no-cache .` | Build without cache |
| `docker rmi image` | Remove image |
| `docker tag source target` | Tag image |
| `docker push image` | Push to registry |
| `docker history image` | Show layers |

---

## Docker Compose Commands

| Command | Description |
|---------|-------------|
| `docker compose up` | Start services |
| `docker compose up -d` | Start detached |
| `docker compose up --build` | Build and start |
| `docker compose down` | Stop and remove |
| `docker compose down -v` | Also remove volumes |
| `docker compose ps` | List services |
| `docker compose logs` | View logs |
| `docker compose logs -f service` | Follow service logs |
| `docker compose exec service cmd` | Run in service |
| `docker compose build` | Build images |
| `docker compose pull` | Pull images |
| `docker compose restart` | Restart services |

---

## Volume Commands

| Command | Description |
|---------|-------------|
| `docker volume ls` | List volumes |
| `docker volume create name` | Create volume |
| `docker volume rm name` | Remove volume |
| `docker volume inspect name` | Volume details |
| `docker volume prune` | Remove unused volumes |

---

## Network Commands

| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network create name` | Create network |
| `docker network rm name` | Remove network |
| `docker network inspect name` | Network details |
| `docker network connect net container` | Connect container |

---

## Cleanup Commands

| Command | Description |
|---------|-------------|
| `docker system prune` | Remove unused data |
| `docker system prune -a` | Remove ALL unused |
| `docker container prune` | Remove stopped containers |
| `docker image prune` | Remove unused images |
| `docker volume prune` | Remove unused volumes |
| `docker system df` | Show disk usage |

---

## Common Patterns

### Run Python Script
```bash
docker run --rm -v $(pwd):/app python:3.12 python /app/script.py
```

### Run FastAPI Development
```bash
docker run --rm -p 8000:8000 -v $(pwd):/app \
  python:3.12-slim \
  bash -c "pip install fastapi uvicorn && fastapi dev /app/main.py --host 0.0.0.0"
```

### Connect to Database
```bash
docker exec -it postgres-container psql -U postgres -d mydb
```

### Copy Files
```bash
docker cp container:/path/file ./local
docker cp ./local container:/path/file
```

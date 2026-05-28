# Docker Troubleshooting Reference

Common issues and solutions for Docker in the machina-meta workspace.

---

## Quick Diagnostics

### Check Overall Status

```bash
# All container status
docker compose ps

# Or via just
just dev-status

# Docker system status
docker system df
docker system info
```

### Check Logs

```bash
# All services
docker compose logs --tail 50

# Specific service
docker compose logs backend --tail 100

# Follow logs
docker compose logs -f backend
```

---

## Container Issues

### Container Won't Start

**Symptoms:** Container exits immediately or stays in "Restarting" state.

**Diagnosis:**
```bash
# Check exit code
docker ps -a --filter "name=backend"

# Check logs
docker compose logs backend --tail 100

# Check events
docker events --since 5m --filter container=machina-meta-backend-1
```

**Common Causes:**

| Exit Code | Meaning | Solution |
|-----------|---------|----------|
| 0 | Normal exit | Check if command is correct |
| 1 | Application error | Check application logs |
| 137 | OOM killed | Increase memory limits |
| 139 | Segfault | Check application/image |

### Container in CrashLoopBackOff

**Diagnosis:**
```bash
# Check previous container logs
docker logs machina-meta-backend-1 --previous

# Check health status
docker inspect --format='{{json .State.Health}}' machina-meta-backend-1
```

**Solutions:**
1. Check application configuration
2. Verify environment variables
3. Check database connectivity
4. Review health check configuration

### Image Pull Failures

**Symptoms:** "Error response from daemon: pull access denied"

**Solutions:**
```bash
# Check image name
docker pull qdrant/qdrant:v1.15.4

# If using private registry
docker login

# Clear image cache
docker image prune -f
```

---

## Network Issues

### Port Already in Use

**Symptoms:** "Bind for 0.0.0.0:8000 failed: port is already allocated"

**Diagnosis:**
```bash
# Find what's using the port
lsof -i :8000
# or
ss -tulpn | grep 8000
```

**Solutions:**
```bash
# If it's a Docker container
docker ps | grep 8000
docker stop <container-name>

# If it's a local process
kill <pid>

# Or change the port in docker-compose.yaml
```

### Container Can't Reach Another Container

**Diagnosis:**
```bash
# Check network
docker network ls
docker network inspect machina-meta_default

# Test connectivity from inside container
docker exec -it machina-meta-backend-1 ping postgres
docker exec -it machina-meta-backend-1 nc -zv postgres 5432
```

**Solutions:**
1. Ensure containers are on same network
2. Use service names (not localhost) for inter-container communication
3. Check firewall rules

### DNS Resolution Failures

**Diagnosis:**
```bash
# Test DNS from container
docker exec -it machina-meta-backend-1 nslookup postgres
```

**Solutions:**
```bash
# Restart Docker DNS
docker network disconnect machina-meta_default machina-meta-backend-1
docker network connect machina-meta_default machina-meta-backend-1

# Or restart Docker daemon
sudo systemctl restart docker
```

---

## Database Issues

### PostgreSQL Won't Connect

**Symptoms:** "connection refused" or "password authentication failed"

**Diagnosis:**
```bash
# Check container is running
docker ps | grep postgres

# Check logs
docker compose logs postgres --tail 50

# Test connection
pg_isready -h localhost -p 5432
```

**Solutions:**
```bash
# Check credentials in .env
cat .env | grep POSTGRES

# Verify container health
docker inspect --format='{{json .State.Health}}' machina-meta-postgres-1

# Reset PostgreSQL
docker compose down
docker volume rm machina-meta_postgres_data
just dev-up
```

### Neo4j Won't Start

**Symptoms:** Neo4j container exits or browser won't connect.

**Diagnosis:**
```bash
# Check logs
docker compose logs neo4j --tail 100

# Common errors:
# - "Java heap space" → Memory issue
# - "Already in use" → Port conflict
# - "APOC" errors → Plugin issue
```

**Solutions:**
```bash
# Memory issues - check limits in docker-compose.yaml
# NEO4J_dbms_memory_heap_initial__size
# NEO4J_dbms_memory_heap_max__size

# Port conflict
lsof -i :7474
lsof -i :7687

# Reset Neo4j
docker volume rm machina-meta_neo4j_data machina-meta_neo4j_logs
just dev-up
```

### Qdrant Collection Missing

**Symptoms:** API returns "Collection not found"

**Diagnosis:**
```bash
# List collections
curl http://localhost:6333/collections

# Check Qdrant logs
docker compose logs qdrant --tail 50
```

**Solutions:**
```bash
# Restore snapshots
(cd repos/medical-catalog && just snapshot-restore-all)

# Or reset and restore
docker volume rm machina-meta_qdrant_storage
just dev-up  # dev_stack.py will auto-restore
```

### Redis Connection Issues

**Diagnosis:**
```bash
# Test Redis
redis-cli -h localhost -p 6379 ping

# Check container
docker compose logs redis --tail 50
```

**Solutions:**
```bash
# Clear Redis data
docker volume rm machina-meta_redis_data
just dev-up
```

---

## Volume Issues

### Volume Permission Denied

**Symptoms:** Container can't write to volume.

**Diagnosis:**
```bash
# Check volume permissions
docker run --rm -v machina-meta_postgres_data:/data alpine ls -la /data
```

**Solutions:**
```bash
# Fix permissions
docker run --rm -v machina-meta_postgres_data:/data alpine chmod -R 777 /data

# Or remove and recreate
docker volume rm machina-meta_postgres_data
```

### Volume Data Corruption

**Symptoms:** Database won't start, reports corruption.

**Solutions:**
```bash
# Backup if possible
docker exec machina-meta-postgres-1 pg_dump -U postgres demodemo > emergency_backup.sql

# Remove and recreate
docker compose down
docker volume rm machina-meta_postgres_data
just dev-up

# Restore from backup
cat emergency_backup.sql | docker exec -i machina-meta-postgres-1 psql -U postgres demodemo
```

---

## Performance Issues

### Containers Running Slow

**Diagnosis:**
```bash
# Check resource usage
docker stats

# Check disk space
docker system df
df -h
```

**Solutions:**
```bash
# Clean up unused resources
docker system prune -f

# Remove old images
docker image prune -a -f

# Increase Docker resources (Docker Desktop)
# Settings → Resources → Memory/CPU
```

### High Memory Usage

**Diagnosis:**
```bash
# Memory by container
docker stats --format "table {{.Name}}\t{{.MemUsage}}"
```

**Solutions:**
1. Add memory limits to docker-compose.yaml
2. Reduce Neo4j heap size
3. Close unused containers

---

## Build Issues

### Build Fails

**Diagnosis:**
```bash
# Build with verbose output
docker compose build --no-cache --progress=plain backend
```

**Common Causes:**
- Missing dependencies
- Network issues during build
- Dockerfile syntax errors

**Solutions:**
```bash
# Clear build cache
docker builder prune -f

# Build specific stage
docker build --target builder -t debug .
```

### Image Not Updating

**Symptoms:** Changes not reflected in container.

**Solutions:**
```bash
# Force rebuild
docker compose build --no-cache backend

# Or
docker compose up -d --build --force-recreate backend
```

---

## Log Analysis

### Extract Backend Logs

```bash
# Using the helper script
(cd repos/dem2 && ./scripts/extract_backend_logs.sh -s backend -l ERROR --since 10m)

# Direct docker logs
docker compose logs backend --tail 500 | grep -i error
```

### Find Specific Errors

```bash
# Search for patterns
docker compose logs backend 2>&1 | grep -i "traceback" -A 10

# Export logs to file
docker compose logs backend > backend_logs.txt 2>&1
```

---

## Emergency Recovery

### Nuclear Option (Complete Reset)

When all else fails:

```bash
# Stop everything
just dev-down

# Remove all containers
docker rm -f $(docker ps -aq) 2>/dev/null || true

# Remove all volumes
docker volume rm $(docker volume ls -q | grep machina) 2>/dev/null || true

# Remove networks
docker network prune -f

# Start fresh
just dev-up
```

### Preserve Critical Data

Before reset, backup:

```bash
# PostgreSQL
docker exec machina-meta-postgres-1 pg_dump -U postgres demodemo > pg_backup.sql

# Neo4j
(cd scripts && python neo4j-query.py --export-database --export-file neo4j_backup.json)

# Then reset and restore
```

---

## Getting Help

### Useful Commands Summary

```bash
# Status
just dev-status
docker compose ps
docker stats

# Logs
docker compose logs <service> --tail 100
docker compose logs -f

# Inspect
docker inspect <container>
docker network inspect machina-meta_default

# Reset
just dev-down
docker volume prune -f
just dev-up
```

### Report Issues

When reporting Docker issues, include:
1. Output of `docker compose ps`
2. Relevant container logs
3. Docker version (`docker --version`)
4. OS and Docker Desktop version (if applicable)

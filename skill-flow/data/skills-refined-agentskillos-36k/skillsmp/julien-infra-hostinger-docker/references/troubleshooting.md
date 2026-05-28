# Docker Troubleshooting Guide

Common errors and their solutions for Hostinger VPS Docker services.

## ContainerConfig KeyError

**Error Message:**
```
KeyError: 'ContainerConfig'
container.image_config['ContainerConfig'].get('Volumes')
```

**Cause:** Old image metadata conflicts with new image after rebuild.

**Solution:**
```bash
ssh automation@69.62.108.82 "cd /opt/[service] && docker-compose down && docker-compose up -d --force-recreate"
```

**Prevention:** Always use `--force-recreate` after building optimized images.

## Network Has Active Endpoints

**Error Message:**
```
error while removing network: network [service]_network has active endpoints
```

**Cause:** Other containers are connected to the network being removed.

**Solution:** Skip the `down` command and use only:
```bash
ssh automation@69.62.108.82 "cd /opt/[service] && docker-compose up -d --force-recreate"
```

## Wrong CMD Executed

**Error Message:**
```
exec: "[wrong-command]": executable file not found in $PATH
```

**Example:** Container tries to execute `mkdocs` instead of `uvicorn`.

**Cause:** Docker layer caching mixed up builds from different services.

**Solution:** Rebuild without cache:
```bash
ssh automation@69.62.108.82 "cd /opt/[service] && docker-compose build --no-cache && docker-compose up -d --force-recreate"
```

**Verification:** Check Dockerfile content matches expectations:
```bash
ssh automation@69.62.108.82 "cat /opt/[service]/Dockerfile | grep CMD"
```

## Permission Denied (scp)

**Error Message:**
```
scp: dest open "/opt/[path]": Permission denied
```

**Cause:** Direct scp to /opt/ requires root permissions.

**Solution:** Use heredoc method instead:
```bash
ssh automation@69.62.108.82 "cat > /tmp/file.txt << 'EOF'
[content]
EOF
sudo cp /tmp/file.txt /opt/[service]/[filename]"
```

## Container Immediately Exits

**Symptoms:** Container shows "Exited (1)" status immediately after start.

**Diagnosis:** Check container logs:
```bash
ssh automation@69.62.108.82 "cd /opt/[service] && docker-compose logs --tail=100"
```

**Common Causes:**
1. **Missing dependencies:** Check requirements.txt was copied correctly
2. **Wrong WORKDIR:** Verify application files exist in expected location
3. **Port already in use:** Check if another container uses the same port
4. **Permission issues:** Ensure non-root user has access to required files

**Solutions:**
- Rebuild with `--no-cache`
- Verify file permissions in Dockerfile (`--chown` flags)
- Check docker-compose.yml port mappings

## Healthcheck Failing

**Symptoms:** Container status shows "unhealthy".

**Diagnosis:** Inspect healthcheck details:
```bash
ssh automation@69.62.108.82 "docker inspect [container-name] | grep -A 10 Health"
```

**Common Causes:**
1. **Wrong endpoint:** Healthcheck URL doesn't exist
2. **Too short start-period:** App needs more time to initialize
3. **Missing curl:** Runtime image doesn't have curl installed

**Solutions:**
- Update healthcheck endpoint to match application routes
- Increase `--start-period` (e.g., from 5s to 40s for Streamlit)
- Install curl in runtime stage:
  ```dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
  ```

## Build Fails - Dependency Conflict

**Error Message:**
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**Cause:** Incompatible package versions in requirements.txt.

**Solutions:**
1. Pin versions explicitly in requirements.txt
2. Use `pip install --no-deps` for problematic packages
3. Create virtual environment locally, test, then copy working requirements.txt

## Out of Disk Space

**Error Message:**
```
no space left on device
```

**Diagnosis:** Check disk usage:
```bash
ssh automation@69.62.108.82 "df -h /"
ssh automation@69.62.108.82 "docker system df"
```

**Solutions:**
1. Clean dangling images:
   ```bash
   ssh automation@69.62.108.82 "docker image prune -f"
   ```

2. Clean unused volumes:
   ```bash
   ssh automation@69.62.108.82 "docker volume prune -f"
   ```

3. Clean build cache:
   ```bash
   ssh automation@69.62.108.82 "docker builder prune -f"
   ```

4. Remove specific old images:
   ```bash
   ssh automation@69.62.108.82 "docker rmi [image-id]"
   ```

## Build Timeout / Hanging

**Symptoms:** Build process freezes or takes extremely long.

**Common Causes:**
1. **Slow dependency download:** Network issues or large packages
2. **Infinite loop in build:** Custom scripts with bugs
3. **Out of memory:** Large ML model downloads

**Solutions:**
1. Increase build timeout in docker-compose:
   ```yaml
   build:
     context: .
     timeout: 600  # 10 minutes
   ```

2. Build in background and monitor:
   ```bash
   ssh automation@69.62.108.82 "cd /opt/[service] && docker-compose build 2>&1 | tee build.log" &
   ```

3. Check memory usage on server:
   ```bash
   ssh automation@69.62.108.82 "free -h"
   ```

## Container Restarts Continuously

**Symptoms:** Container keeps restarting (restart count increases).

**Diagnosis:** Check restart policy and logs:
```bash
ssh automation@69.62.108.82 "docker inspect [container-name] | grep -A 3 RestartPolicy"
ssh automation@69.62.108.82 "docker logs --tail=200 [container-name]"
```

**Common Causes:**
1. **Application crash:** Check logs for Python/Node.js errors
2. **Wrong CMD:** Application starts but immediately exits
3. **Missing environment variables:** Required config not provided

**Solutions:**
- Fix application errors shown in logs
- Verify CMD matches application entry point
- Check docker-compose.yml environment section

## Port Conflict

**Error Message:**
```
bind: address already in use
```

**Diagnosis:** Check which process uses the port:
```bash
ssh automation@69.62.108.82 "sudo netstat -tulpn | grep :[port]"
```

**Solutions:**
1. Change port in docker-compose.yml
2. Stop conflicting container
3. Use different host port mapping (e.g., `8080:80` instead of `80:80`)

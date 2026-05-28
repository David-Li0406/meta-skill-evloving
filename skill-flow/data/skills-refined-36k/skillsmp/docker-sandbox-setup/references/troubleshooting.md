# Docker Sandbox Troubleshooting

Common issues when creating and running Docker-based sandboxes for Claude Code.

## Build Failures

### Issue: apt-get update fails

**Symptoms:**
```
E: Failed to fetch http://archive.ubuntu.com/ubuntu/...
```

**Causes:**
- Network connectivity issues
- DNS resolution problems
- Proxy configuration needed

**Solutions:**

1. **Check Docker daemon network:**
```bash
docker network ls
docker network inspect bridge
```

2. **Restart Docker daemon:**
```bash
sudo systemctl restart docker  # Linux
# or restart Docker Desktop on macOS
```

3. **Use alternative mirror:**
```dockerfile
RUN sed -i 's/archive.ubuntu.com/mirrors.edge.kernel.org/g' /etc/apt/sources.list
RUN apt-get update
```

4. **Configure DNS in Docker:**
```json
// /etc/docker/daemon.json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```

### Issue: Build cache not being used

**Symptoms:**
- Every build reinstalls everything
- Builds taking 10+ minutes each time

**Causes:**
- Dockerfile commands ordered poorly
- COPY commands invalidating cache early
- Build context changing

**Solutions:**

1. **Reorder Dockerfile** (rare-to-frequent changes):
```dockerfile
# Good: Base packages first (rarely change)
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y curl git

# Then languages (occasionally change)
RUN install_rust

# Then tools (occasionally change)
RUN install_cli_tools

# Volume mount source code (don't COPY it)
```

2. **Use .dockerignore:**
```
.git
node_modules/
.docker-cache/
```

3. **Don't COPY workspace:**
```dockerfile
# ❌ BAD - invalidates cache on any code change
COPY ./workspace /workspace

# ✅ GOOD - use volume mount instead
# (in docker run command, not Dockerfile)
```

### Issue: Build runs out of disk space

**Symptoms:**
```
Error: no space left on device
```

**Causes:**
- Docker image layers accumulating
- Build cache not being cleaned
- Large dependencies

**Solutions:**

1. **Clean Docker system:**
```bash
docker system prune -a --volumes
```

2. **Check Docker disk usage:**
```bash
docker system df
```

3. **Increase Docker Desktop disk limit** (macOS):
- Docker Desktop → Settings → Resources → Disk image size

4. **Remove unused images:**
```bash
docker image prune -a
```

## Runtime Failures

### Issue: Container exits immediately

**Symptoms:**
```bash
docker run sandbox-project
# Container starts and exits immediately
docker ps -a  # Shows "Exited (0)"
```

**Causes:**
- No long-running process
- CMD/ENTRYPOINT completes immediately

**Solutions:**

1. **Run in detached mode with sleep:**
```bash
docker run -d sandbox-project sleep infinity
```

2. **Or use interactive mode:**
```bash
docker run -it sandbox-project /bin/bash
```

3. **Update CMD in Dockerfile:**
```dockerfile
# Keep container running
CMD ["tail", "-f", "/dev/null"]
```

### Issue: Permission denied errors in workspace

**Symptoms:**
```
Permission denied: '/workspace/file.txt'
```

**Causes:**
- Container runs as root
- Files created as root:root
- Host user can't modify them

**Solutions:**

1. **Fix permissions on stop (simplest):**
```bash
# stop.sh
docker exec sandbox-${PROJECT_NAME} chown -R $(id -u):$(id -g) /workspace
docker stop sandbox-${PROJECT_NAME}
```

2. **Run as non-root user:**
```dockerfile
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} developer && \
    useradd -u ${USER_ID} -g developer -m -s /bin/bash developer
USER developer
```

Build with host UID/GID:
```bash
docker build --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -t sandbox .
```

### Issue: Port already in use

**Symptoms:**
```
Error: bind: address already in use
```

**Causes:**
- Another container using the port
- Host service using the port
- Previous container not stopped

**Solutions:**

1. **Find what's using the port:**
```bash
lsof -i :3000  # macOS/Linux
netstat -ano | findstr :3000  # Windows
```

2. **Stop conflicting container:**
```bash
docker ps  # Find container
docker stop <container-id>
```

3. **Use different ports:**
```bash
docker run -p 3010:3000 sandbox-project
# Access on host:3010, container sees :3000
```

4. **Forward only specific ports:**
```bash
# Instead of -p 3000-3999:3000-3999
docker run -p 3000:3000 -p 8080:8080 sandbox-project
```

### Issue: Volume mount not updating

**Symptoms:**
- Edit file on host
- Changes don't appear in container

**Causes:**
- Wrong mount path
- File watching issues (Docker Desktop)
- Cached files

**Solutions:**

1. **Verify mount is correct:**
```bash
docker exec sandbox-project ls -la /workspace
```

2. **Check mounts:**
```bash
docker inspect sandbox-project | grep Mounts -A 20
```

3. **Restart container:**
```bash
./sandbox/stop.sh
./sandbox/up.sh
```

4. **Docker Desktop file sharing** (macOS):
- Settings → Resources → File Sharing
- Ensure directory is in allowed list

### Issue: DNS resolution fails in container

**Symptoms:**
```
curl: (6) Could not resolve host: github.com
```

**Causes:**
- Docker DNS configuration
- VPN interference
- Corporate firewall

**Solutions:**

1. **Test DNS in container:**
```bash
docker exec sandbox-project nslookup github.com
docker exec sandbox-project cat /etc/resolv.conf
```

2. **Configure DNS in daemon:**
```json
// /etc/docker/daemon.json
{
  "dns": ["8.8.8.8", "1.1.1.1"]
}
```

3. **Override for single container:**
```bash
docker run --dns 8.8.8.8 --dns 8.8.4.4 sandbox-project
```

4. **VPN workaround:**
- Disconnect VPN during build
- Or configure VPN to allow Docker traffic

## Performance Issues

### Issue: Slow builds

**Symptoms:**
- Builds taking 15+ minutes
- Recompiling everything each time

**Causes:**
- No build cache
- Downloading large dependencies
- No layer optimization

**Solutions:**

1. **Use BuildKit:**
```bash
export DOCKER_BUILDKIT=1
docker build -t sandbox-project .
```

2. **Optimize layer caching:**
```dockerfile
# Copy dependency files first
COPY requirements.txt package.json Cargo.toml ./
RUN install_dependencies

# Then copy source (changes more frequently)
COPY . .
```

3. **Mount cache for package managers:**
```dockerfile
RUN --mount=type=cache,target=/root/.cargo \
    cargo build --release
```

### Issue: Container runs slowly

**Symptoms:**
- Commands take longer than on host
- High CPU usage
- Builds/tests slow

**Causes:**
- Docker Desktop resource limits (macOS/Windows)
- Volume mount performance (macOS)
- Insufficient CPU/memory allocation

**Solutions:**

1. **Increase Docker resources:**
- Docker Desktop → Settings → Resources
- CPUs: At least 4
- Memory: At least 4GB

2. **Use delegated mounts** (macOS):
```bash
docker run -v $(pwd)/workspace:/workspace:delegated sandbox-project
```

3. **Check resource usage:**
```bash
docker stats sandbox-project
```

4. **Linux vs macOS/Windows:**
- Linux has best performance (native)
- macOS/Windows use VM (slower volume mounts)

### Issue: Large image size

**Symptoms:**
- Image >2GB
- Slow transfers/pulls
- Taking up disk space

**Causes:**
- Not cleaning package manager caches
- Unnecessary files included
- No multi-stage build (though not needed for sandboxes)

**Solutions:**

1. **Clean package caches:**
```dockerfile
RUN apt-get update && apt-get install -y packages \
    && rm -rf /var/lib/apt/lists/*
```

2. **Use .dockerignore:**
```
node_modules/
.git/
*.log
```

3. **Check image size:**
```bash
docker images sandbox-project
docker history sandbox-project
```

4. **Accept larger images** for dev containers:
- Sandboxes need full tooling
- Size optimization less important than functionality

## Network Issues

### Issue: Can't access host services from container

**Symptoms:**
- Container can't connect to database on host
- Can't reach host:3000 from container

**Causes:**
- Container network isolation
- Wrong host address

**Solutions:**

1. **Use host.docker.internal:**
```bash
# In container
curl http://host.docker.internal:5432
```

2. **Or use host network mode:**
```bash
docker run --network=host sandbox-project
```

**Note:** `--network=host` breaks port isolation. Use sparingly.

### Issue: Can't access container services from host

**Symptoms:**
- Host can't reach localhost:3000
- Connection refused

**Causes:**
- Port not forwarded
- Service listening on 127.0.0.1 only

**Solutions:**

1. **Verify port forwarding:**
```bash
docker ps  # Check PORTS column
```

2. **Ensure service binds 0.0.0.0:**
```bash
# In container
netstat -tlnp | grep :3000
```

Service should listen on `0.0.0.0:3000`, not `127.0.0.1:3000`

3. **Configure application:**
```javascript
// Instead of
app.listen(3000, 'localhost')

// Use
app.listen(3000, '0.0.0.0')
```

## Claude Code Specific Issues

### Issue: Claude Code not authenticated

**Symptoms:**
```
Error: Not authenticated. Run 'cc auth'
```

**Causes:**
- First run in container
- Authentication not persisted

**Solutions:**

1. **Mount Claude directory:**
```bash
docker run -v $(pwd)/.docker-cache/claude:/root/.claude sandbox-project
```

2. **Authenticate once:**
```bash
./sandbox/shell.sh
cc auth
# Follow authentication flow
# Future container restarts will preserve auth
```

3. **Document in SANDBOX.md:**
```markdown
## First Run Setup

1. Start the sandbox: `./sandbox/up.sh`
2. Enter shell: `./sandbox/shell.sh`
3. Authenticate Claude: `cc auth`
4. Exit shell: `exit`

Authentication persists across restarts.
```

### Issue: Plugins not loading

**Symptoms:**
- Installed plugins don't appear
- `/help` doesn't show plugin commands

**Causes:**
- Plugin installed in wrong location
- Claude directory not mounted
- Plugin installation failed

**Solutions:**

1. **Verify mount:**
```bash
docker exec sandbox-project ls /root/.claude/plugins
```

2. **Reinstall plugins in container:**
```bash
./sandbox/shell.sh
cc marketplace add anthropics/claude-plugins-official
cc plugin install devs@aaronbassett-marketplace
```

3. **Check plugin installation:**
```bash
cc plugin list
```

## Prevention Checklist

Before creating a sandbox, verify:

- [ ] Docker daemon is running (`docker ps`)
- [ ] Sufficient disk space (>10GB free)
- [ ] Docker Desktop resources adequate (4+ CPU, 4GB+ RAM)
- [ ] Network connectivity working
- [ ] No port conflicts
- [ ] .dockerignore file present
- [ ] Volume mount paths correct
- [ ] .env file contains GITHUB_TOKEN

After creating a sandbox, verify:

- [ ] Container starts successfully
- [ ] Volume mounts working (edit file on host, see in container)
- [ ] Ports accessible from host
- [ ] Claude Code authenticated
- [ ] Plugins loaded
- [ ] Shell configured correctly

## Quick Diagnostic Commands

```bash
# Check Docker health
docker info
docker ps -a
docker system df

# Check specific container
docker inspect sandbox-project
docker logs sandbox-project
docker exec sandbox-project ps aux

# Test network
docker exec sandbox-project ping -c 3 google.com
docker exec sandbox-project curl -I https://github.com

# Test volumes
docker exec sandbox-project ls -la /workspace
docker exec sandbox-project ls -la /root/.claude

# Test ports
curl http://localhost:3000
docker port sandbox-project
```

## Getting Help

If issues persist:

1. Check Docker logs: `docker logs sandbox-project`
2. Inspect container: `docker inspect sandbox-project`
3. Enter container to debug: `./sandbox/shell.sh`
4. Search Docker documentation
5. Check GitHub issues for similar problems

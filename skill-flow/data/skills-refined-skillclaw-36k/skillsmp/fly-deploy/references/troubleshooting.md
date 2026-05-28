# Troubleshooting fly.io Deployments

## Essential Debugging Commands

```bash
# View application status
fly status

# Stream logs in real-time
fly logs

# View recent logs only
fly logs --no-tail

# Filter logs by instance
fly logs -i <instance-id>

# Filter logs by region
fly logs -r ord

# SSH into running machine
fly ssh console

# Run command without interactive shell
fly ssh console -C "ps aux"

# Check machine list
fly machine list

# View recent deployments
fly releases

# Check health checks
fly checks list
```

---

## Deployment Issues

### Build Fails

**Symptom:** Deployment fails during Docker build

**Common causes:**

1. **Missing dependencies in Dockerfile**

```dockerfile
# ❌ Bad: Dependencies not installed
FROM node:20-slim
COPY . .
RUN npm run build  # Fails: node_modules missing

# ✅ Good: Install dependencies first
FROM node:20-slim
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
```

2. **Build context too large**

Check `.dockerignore`:
```
node_modules
.git
dist
build
*.log
.env
```

3. **Out of memory during build**

Use `--remote-only` to build on fly.io servers:
```bash
fly deploy --remote-only
```

4. **Architecture mismatch**

Ensure Dockerfile targets correct platform:
```dockerfile
FROM --platform=linux/amd64 node:20-slim
```

**Debug:**
```bash
# View build logs
fly logs --debug

# Test build locally
docker build -t test .

# Check Dockerfile syntax
docker build --check .
```

### Deployment Succeeds but App Crashes

**Symptom:** Deploy completes but machines keep restarting

**Check logs:**
```bash
fly logs
```

**Common causes:**

1. **Port mismatch**

App must listen on PORT from environment:

```js
// ❌ Bad: Hardcoded port
app.listen(3000)

// ✅ Good: Read from env
const port = process.env.PORT || 8080
app.listen(port, '0.0.0.0')
```

fly.toml must match:
```toml
[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
```

2. **Binding to localhost instead of 0.0.0.0**

```js
// ❌ Bad: Only localhost
app.listen(8080, '127.0.0.1')

// ✅ Good: All interfaces
app.listen(8080, '0.0.0.0')
```

3. **Missing environment variables**

```bash
# Check what secrets are set
fly secrets list

# Set missing secret
fly secrets set DATABASE_URL=postgres://...
```

4. **Startup command wrong**

Check Dockerfile CMD or ENTRYPOINT:
```dockerfile
# Verify command is correct
CMD ["node", "dist/index.js"]
```

**Debug:**
```bash
# SSH into machine
fly ssh console

# Check process
ps aux | grep node

# Check what's listening
netstat -tulpn | grep LISTEN

# Test app manually
cd /app && node index.js
```

### Health Checks Failing

**Symptom:** "Health checks are failing"

**Check health endpoint:**
```bash
# From within machine
fly ssh console -C "curl http://localhost:8080/health"

# Check from fly.io network
curl https://your-app.fly.dev/health
```

**Common causes:**

1. **Health endpoint doesn't exist**

Add health check to your app:
```js
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' })
})
```

2. **Health check path wrong in fly.toml**

```toml
[[http_service.checks]]
  grace_period = "10s"
  interval = "30s"
  method = "GET"
  timeout = "5s"
  path = "/health"  # Must match your endpoint
```

3. **App taking too long to start**

Increase grace period:
```toml
[[http_service.checks]]
  grace_period = "30s"  # Give app more time to start
```

4. **Database not ready**

Implement proper health check:
```js
app.get('/health', async (req, res) => {
  try {
    // Check database connection
    await db.query('SELECT 1')
    res.status(200).json({ status: 'ok' })
  } catch (error) {
    res.status(503).json({ status: 'error', message: error.message })
  }
})
```

**Debug:**
```bash
# View health check status
fly checks list

# Watch health check in logs
fly logs | grep health
```

---

## Runtime Issues

### App Running Slow

**Check resource usage:**
```bash
fly ssh console -C "free -m"
fly ssh console -C "top -bn1"
```

**Common causes:**

1. **Out of memory**

```bash
# Scale up memory
fly scale memory 512

# Or update fly.toml
[[vm]]
  memory = "512mb"
```

2. **CPU throttling**

```bash
# Scale to larger VM
fly scale vm shared-cpu-2x
```

3. **Database connection pool exhausted**

Increase pool size:
```js
const pool = new Pool({
  max: 20,  // Increase from default 10
  connectionTimeoutMillis: 5000
})
```

4. **Cold starts**

Prevent scaling to zero:
```toml
[http_service]
  min_machines_running = 1  # Keep 1 always running
```

Or use suspend instead of stop:
```toml
[http_service]
  auto_stop_machines = "suspend"  # Faster wake-up
```

### App Crashing Under Load

**Check logs during load:**
```bash
fly logs
```

**Common causes:**

1. **Memory leak**

Monitor memory over time:
```bash
fly ssh console -C "watch -n 5 free -m"
```

Fix: Identify and fix memory leaks in code

2. **Unhandled errors**

Add global error handlers:
```js
process.on('uncaughtException', (error) => {
  console.error('Uncaught Exception:', error)
  process.exit(1)  // Let fly.io restart the machine
})

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection:', reason)
})
```

3. **Database connection issues**

Use connection pooling and handle connection errors:
```js
pool.on('error', (err) => {
  console.error('Database pool error:', err)
})
```

### Machines Keep Restarting

**Check restart policy:**
```bash
fly machine list
```

**Debug crash loop:**
```bash
# Stream logs to see crash reason
fly logs

# Check exit code
fly machine list

# SSH may not work if crashing immediately
# Use fly console for one-off debugging
```

**Common causes:**

1. **Process exits immediately**

Ensure app keeps running:
```js
// ❌ Bad: Script exits after running
console.log('Hello')
// Process exits

// ✅ Good: Server keeps running
app.listen(8080, () => {
  console.log('Server running')
})
```

2. **Unhandled promise rejections**

```js
// ✅ Add global handler
process.on('unhandledRejection', (reason) => {
  console.error('Unhandled Rejection:', reason)
  // Don't exit - let app continue
})
```

---

## Database Connection Issues

### Cannot Connect to Postgres

**Symptoms:**
- "Connection refused"
- "No such host"
- "Connection timeout"

**Check DATABASE_URL is set:**
```bash
fly secrets list | grep DATABASE
```

**Verify format:**
```bash
# Should be:
postgres://user:pass@app.internal:5432/dbname
# NOT:
postgres://user:pass@localhost:5432/dbname
```

**Test connection from machine:**
```bash
fly ssh console

# Try connecting
psql $DATABASE_URL

# Or test with curl (for HTTP APIs)
curl http://my-postgres.internal:5432
```

**Common causes:**

1. **Database app not in same organization**

```bash
# Check both apps are in same org
fly apps list
```

2. **Database app not running**

```bash
fly status -a <postgres-app-name>
```

3. **Wrong connection string format**

For SQLAlchemy (Python):
```python
# postgres:// must be changed to postgresql://
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
```

### Slow Database Queries

**Enable query logging:**

```js
// Node.js with Prisma
const prisma = new PrismaClient({
  log: ['query', 'info', 'warn', 'error'],
})
```

```python
# Python with SQLAlchemy
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

**Check from database side:**
```bash
fly postgres connect -a <postgres-app-name>

-- Show slow queries
SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
```

---

## Networking Issues

### Cannot Access External API

**Test from machine:**
```bash
fly ssh console -C "curl https://api.example.com"
```

**Common causes:**

1. **Firewall blocking outbound**
   - fly.io allows all outbound traffic by default
   - Check if external API has IP whitelist

2. **DNS resolution issues**

```bash
fly ssh console -C "nslookup api.example.com"
```

3. **SSL certificate issues**

```bash
fly ssh console -C "curl -v https://api.example.com"
```

### Custom Domain Not Working

See `domains-and-networking.md` for detailed domain troubleshooting.

**Quick checks:**
```bash
# Verify certificate issued
fly certs show example.com

# Check DNS
dig example.com
dig AAAA example.com

# Test SSL
curl -I https://example.com
```

---

## Scaling Issues

### Auto-scaling Not Working

**Check configuration:**
```toml
[http_service]
  auto_start_machines = true
  auto_stop_machines = "stop"
  min_machines_running = 0
```

**View machine states:**
```bash
fly machine list
```

**Common causes:**

1. **Machines not stopping**

Check for long-running connections:
```bash
fly ssh console -C "netstat -an | grep ESTABLISHED"
```

2. **Machines not starting**

Check health checks pass when machine starts:
```bash
fly logs | grep health
```

### Too Many Machines Running

**Stop extra machines:**
```bash
# List machines
fly machine list

# Stop specific machine
fly machine stop <machine-id>

# Scale down
fly scale count 1
```

**Prevent auto-scaling:**
```toml
[http_service]
  auto_stop_machines = "off"
  min_machines_running = 1
  max_machines_running = 1
```

---

## Debugging Techniques

### Enable Debug Logging

**In deployment:**
```bash
fly deploy --debug
```

**In fly.toml:**
```toml
[env]
  LOG_LEVEL = "debug"
  DEBUG = "*"  # For Node.js debug module
  RUST_LOG = "debug"  # For Rust
```

### Interactive Debugging

**SSH into machine:**
```bash
fly ssh console
```

**Run commands:**
```bash
# Check environment
env | grep -i database

# Test app manually
node /app/index.js

# Check file system
ls -la /app

# Check running processes
ps aux

# Check open files
lsof -i :8080
```

### Local Testing

**Test Dockerfile locally:**
```bash
# Build
docker build -t my-app .

# Run with same env
docker run -p 8080:8080 \
  -e PORT=8080 \
  -e DATABASE_URL=postgres://localhost/test \
  my-app

# Test
curl http://localhost:8080
```

### Monitoring

**Real-time logs:**
```bash
# All logs
fly logs

# Follow logs
fly logs -f

# Filter by level
fly logs | grep ERROR
fly logs | grep WARN
```

**Machine metrics:**
```bash
# CPU and memory
fly ssh console -C "top -bn1"

# Disk usage
fly ssh console -C "df -h"

# Network
fly ssh console -C "netstat -s"
```

---

## Common Error Messages

### "Failed to allocate IP"

**Solution:**
```bash
# Allocate IPv4 manually
fly ips allocate-v4
```

### "No space left on device"

**Solution:**
```bash
# Check disk usage
fly ssh console -C "df -h"

# Clear build cache
fly deploy --no-cache
```

### "Health check timeout"

**Solutions:**
1. Increase timeout in fly.toml
2. Increase grace period
3. Fix slow startup in app
4. Check health endpoint responds quickly

### "Connection refused"

**Check:**
1. App is listening on correct port
2. App binds to 0.0.0.0, not 127.0.0.1
3. PORT env variable is used

### "Out of memory"

**Solutions:**
```bash
# Scale up memory
fly scale memory 512

# Or optimize app memory usage
```

---

## Getting Help

### Self-Service Resources

1. **Official docs:** https://fly.io/docs/
2. **Community forum:** https://community.fly.io/
3. **Status page:** https://status.flyio.net/
4. **Error code reference:** https://fly.io/docs/error-codes/

### Collecting Information for Support

When asking for help, include:

```bash
# App status
fly status > status.txt

# Recent logs
fly logs --no-tail > logs.txt

# fly.toml (remove secrets)
cat fly.toml > config.txt

# Machine list
fly machine list > machines.txt

# Releases
fly releases > releases.txt
```

### Support Channels

- **Community Forum:** Free, community support
- **Paid Support:** $29+/month with guaranteed response times
- **Email:** For account and billing issues

---

## Preventive Measures

### Best Practices

1. **Always test locally first**
   ```bash
   docker build -t test . && docker run -p 8080:8080 test
   ```

2. **Use health checks**
   ```toml
   [[http_service.checks]]
     path = "/health"
   ```

3. **Monitor logs regularly**
   ```bash
   fly logs | grep -i error
   ```

4. **Set resource limits**
   ```toml
   [[vm]]
     memory = "512mb"
   ```

5. **Use graceful shutdown**
   ```js
   process.on('SIGTERM', async () => {
     await server.close()
     await db.close()
     process.exit(0)
   })
   ```

6. **Keep dependencies updated**
   ```bash
   npm outdated
   npm update
   ```

7. **Use CI/CD testing**
   - Run tests before deploying
   - Use staging environment
   - See `github-integration.md`

8. **Monitor performance**
   - Track response times
   - Monitor error rates
   - Set up alerts

---

## Quick Troubleshooting Checklist

```
□ Check fly status
□ Read fly logs
□ Verify secrets are set (fly secrets list)
□ Check fly.toml configuration
□ Test health check endpoint
□ Verify DNS (for custom domains)
□ Check resource usage (memory/CPU)
□ SSH into machine and test manually
□ Compare local Docker build
□ Check recent releases (fly releases)
□ Review error codes in docs
□ Search community forum
```

Most issues fall into these categories:
1. **Configuration** (fly.toml, env vars, secrets)
2. **Networking** (ports, binding, domains)
3. **Resources** (memory, CPU, disk)
4. **Code** (errors, crashes, unhandled exceptions)
5. **Database** (connections, queries, migrations)

Start with configuration and logs - they solve 80% of issues.

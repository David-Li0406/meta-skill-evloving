---
name: epic-deployment
description: Use this skill when you need to configure deployment on Fly.io, set up multi-region deployment, and manage CI/CD for the Epic Stack.
---

# Epic Stack: Deployment

## When to use this skill

Use this skill when you need to:
- Configure deployment on Fly.io
- Set up multi-region deployment
- Configure CI/CD with GitHub Actions
- Manage secrets in production
- Configure healthchecks
- Work with LiteFS and volumes
- Local deployment with Docker

## Patterns and conventions

### Fly.io Configuration

Epic Stack uses Fly.io for hosting with configuration in `fly.toml`.

**Basic configuration:**
```toml
# fly.toml
app = "your-app-name"
primary_region = "sjc"
kill_signal = "SIGINT"
kill_timeout = 5

[build]
dockerfile = "/other/Dockerfile"
ignorefile = "/other/Dockerfile.dockerignore"

[mounts]
source = "data"
destination = "/data"
```

### Primary Region

**Configure primary region:**
```toml
primary_region = "sjc" # Change according to your location
```

**Important:** The primary region must be the same for:
- `primary_region` in `fly.toml`
- Region of the volume `data`
- `PRIMARY_REGION` in environment variables

### LiteFS Configuration

**Configuration in `other/litefs.yml`:**
```yaml
fuse:
  dir: '${LITEFS_DIR}'

data:
  dir: '/data/litefs'

proxy:
  addr: ':${INTERNAL_PORT}'
  target: 'localhost:${PORT}'
  db: '${DATABASE_FILENAME}'

lease:
  type: 'consul'
  candidate: ${FLY_REGION == PRIMARY_REGION}
  promote: true
  advertise-url: 'http://${HOSTNAME}.vm.${FLY_APP_NAME}.internal:20202'
  consul:
    url: '${FLY_CONSUL_URL}'
    key: 'epic-stack-litefs_20250222/${FLY_APP_NAME}'

exec:
  - cmd: npx prisma migrate deploy
    if-candidate: true
  - cmd: sqlite3 $DATABASE_PATH "PRAGMA journal_mode = WAL;"
    if-candidate: true
  - cmd: sqlite3 $CACHE_DATABASE_PATH "PRAGMA journal_mode = WAL;"
    if-candidate: true
  - cmd: npx prisma generate --sql
  - cmd: npm start
```

### Healthchecks

**Configuration in `fly.toml`:**
```toml
[[services.http_checks]]
interval = "10s"
grace_period = "5s"
method = "get"
path = "/resources/healthcheck"
protocol = "http"
timeout = "2s"
tls_skip_verify = false
```

**Healthcheck implementation:**
```typescript
// app/routes/resources/healthcheck.tsx
export async function loader({ request }: Route.LoaderArgs) {
	const host = request.headers.get('X-Forwarded-Host') ?? request.headers.get('host')

	try {
		await Promise.all([
			prisma.user.count(), // Verify DB
			fetch(`${new URL(request)
```
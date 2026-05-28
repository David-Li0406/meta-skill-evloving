# Redis

**Category**: databases
**Description**: Redis in-memory data store clients
**Homepage**: https://redis.io

## Package Detection

### NPM
*Node.js Redis clients and queue libraries*

- `redis`
- `ioredis`
- `@upstash/redis`
- `bullmq`
- `bull`

### PYPI
*Python Redis clients*

- `redis`
- `aioredis`
- `redis-py-cluster`
- `fakeredis`
- `celery`

### RUBYGEMS
*Ruby Redis clients and job processors*

- `redis`
- `sidekiq`
- `resque`

### MAVEN
*Java Redis clients*

- `io.lettuce:lettuce-core`
- `redis.clients:jedis`

### GO
*Go Redis clients*

- `github.com/redis/go-redis`
- `github.com/go-redis/redis`

### Related Packages
- `connect-redis`
- `express-session`
- `koa-redis`

## Import Detection

### Javascript

**Pattern**: `from\s+['"]redis['"]`
- Type: esm_import

**Pattern**: `require\(['"]redis['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]ioredis['"]`
- Type: esm_import

**Pattern**: `require\(['"]ioredis['"]\)`
- Type: commonjs_require

**Pattern**: `from\s+['"]@upstash/redis['"]`
- Type: esm_import

### Python

**Pattern**: `import\s+redis`
- Type: python_import

**Pattern**: `from\s+redis`
- Type: python_import

**Pattern**: `import\s+aioredis`
- Type: python_import

### Go

**Pattern**: `"github\.com/redis/go-redis`
- Type: go_import

**Pattern**: `"github\.com/go-redis/redis`
- Type: go_import

## Environment Variables

*Redis connection URL*

*Redis host*

*Redis port*

*Redis password*

*Redis TLS connection URL*

*Upstash Redis REST URL*

*Upstash Redis REST token*


## Detection Notes

- Check for REDIS_URL in environment
- Look for redis:// connection strings
- Common for caching, sessions, job queues

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 85% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)

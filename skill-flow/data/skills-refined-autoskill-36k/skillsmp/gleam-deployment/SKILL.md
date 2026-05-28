---
name: gleam-deployment
description: Guides Claude through deploying Gleam applications to production on Fly.io, Docker, or other platforms. Use when setting up deployment pipelines, configuring environments, or troubleshooting production issues.
---

# Gleam Deployment Skill

This skill guides Claude Code through deploying Gleam applications to production.

## Primary Sources

1. **[Deploying to Fly.io](https://gleam.run/deployment/fly/)** - Official Fly.io deployment guide
2. **[Gleam Export Command](https://gleam.run/writing-gleam/)** - Building releases
3. **[Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)** - Container optimization
4. **[Envoy Documentation](https://hexdocs.pm/envoy/)** - Environment configuration
5. **[Gleam FAQ - Production](https://gleam.run/frequently-asked-questions/)** - Production readiness

## Deployment Targets

### Fly.io (Official Guide)

Complete step-by-step guide:
**[Gleam on Fly.io](https://gleam.run/deployment/fly/)**

Key points:
- Listen on `0.0.0.0` (use `mist.bind("0.0.0.0")`)
- Use multi-stage Docker builds
- Configure fly.toml
- Deploy with `flyctl deploy`

### Other Platforms

Gleam apps can deploy to any platform supporting:
- **Docker containers**: AWS ECS, Google Cloud Run, Azure Container Instances
- **Erlang releases**: Any server with Erlang/OTP installed
- **JavaScript**: Node.js hosting (Vercel, Netlify, etc.)

## Building for Production

### Erlang Target

Build optimized Erlang release:
```bash
gleam export erlang-shipment
```

This creates a standalone release in `build/erlang-shipment/`.

See: [gleam.run/writing-gleam](https://gleam.run/writing-gleam/)

### JavaScript Target

Build JavaScript bundle:
```bash
gleam build --target javascript
```

Output in `build/dev/javascript/`.

## Docker Configuration

### Multi-Stage Build Pattern

Example from Fly.io guide:

```dockerfile
# Stage 1: Build
FROM ghcr.io/gleam-lang/gleam:v1.10.0-erlang-alpine AS builder
WORKDIR /app
COPY . .
RUN gleam export erlang-shipment

# Stage 2: Runtime
FROM erlang:27.1.1.0-alpine
WORKDIR /app
COPY --from=builder /app/build/erlang-shipment /app
RUN adduser -D webapp
USER webapp
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["run"]
```

See complete example: [Fly.io Deployment Guide](https://gleam.run/deployment/fly/)

### Docker Optimization

Best practices:
- Use multi-stage builds (smaller images)
- Run as non-root user (security)
- Use .dockerignore (faster builds)
- Layer caching (faster rebuilds)

## Configuration Management

### Environment Variables

Use Envoy for environment configuration:

```gleam
import envoy

pub fn main() {
  let assert Ok(port) = envoy.get("PORT")
    |> result.then(int.parse)

  let assert Ok(db_url) = envoy.get("DATABASE_URL")

  start_server(port, db_url)
}
```

See: [Envoy Documentation](https://hexdocs.pm/envoy/)

### Configuration Files

For complex configuration, consider:
- TOML: [Tom parser](https://hexdocs.pm/tom/)
- JSON: [gleam_json](https://hexdocs.pm/gleam_json/)
- Environment-specific configs

## Security Considerations

### Secrets Management

- **Never commit secrets** to version control
- Use platform secret managers (Fly.io Secrets, AWS Secrets Manager, etc.)
- Inject secrets as environment variables
- Rotate secrets regularly

### Network Security

- Use HTTPS in production (platforms usually provide this)
- Configure CORS appropriately
- Validate all inputs
- Rate limit API endpoints

See: [Wisp Security](https://hexdocs.pm/wisp/)

## Database Deployment

### Connection Pooling

Use connection pools for databases:
- **Pog** has built-in pooling
- Configure pool size based on load

### Migrations

Patterns for database migrations:
1. Run migrations in startup script
2. Use dedicated migration tool (e.g., cigogne for Postgres)
3. Manual migration management

See: [Cigogne](https://hexdocs.pm/cigogne/) - Postgres migrations in Gleam

## Monitoring and Logging

### Logging

Production logging strategies:
- Use structured logging: [Palabres](https://hexdocs.pm/palabres/)
- Log to stdout/stderr (captured by platforms)
- Use appropriate log levels
- Include request IDs for tracing

### Monitoring

BEAM/OTP monitoring:
- Built-in Erlang tools (`:observer`, `:recon`)
- Platform monitoring (Fly.io metrics, CloudWatch, etc.)
- Custom telemetry
- Health check endpoints

### Health Checks

Implement health check endpoints:
```gleam
fn handle_request(req: Request) -> Response {
  case wisp.path_segments(req) {
    ["health"] -> wisp.response(200)
      |> wisp.set_body(wisp.Text("OK"))
    // other routes...
  }
}
```

## Performance Optimization

### Erlang Release Optimization

- Use `gleam export erlang-shipment` for optimized builds
- Configure BEAM flags in entrypoint
- Tune garbage collection settings

### Caching Strategies

- ETS tables (Erlang)
- External caching (Redis, Memcached)
- CDN for static assets
- HTTP caching headers

### Load Balancing

- Platform load balancing (Fly.io, AWS ALB)
- Multiple instances for scaling
- Health checks for routing

## CI/CD Pipelines

### GitHub Actions Example

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install Gleam
        uses: erlef/setup-beam@v1
        with:
          gleam-version: "1.10.0"
      - name: Run tests
        run: gleam test
      - name: Deploy to Fly.io
        uses: superfly/flyctl-actions@master
        with:
          args: "deploy"
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

## Platform-Specific Guides

### Fly.io
**[Official Guide](https://gleam.run/deployment/fly/)**

### AWS
- ECS with Docker
- Lambda (JavaScript target)
- Elastic Beanstalk (Docker)

### Google Cloud
- Cloud Run (Docker)
- GKE (Kubernetes)
- App Engine (JavaScript)

### Azure
- Container Instances (Docker)
- AKS (Kubernetes)
- App Service (Docker)

### Vercel/Netlify (JavaScript Target)
- Build JavaScript target
- Configure build commands
- Deploy via CLI or Git integration

## Troubleshooting

### Common Issues

**Port binding**: Ensure listening on `0.0.0.0`, not `localhost`

**Environment variables**: Verify all required vars are set in platform

**File permissions**: Run as non-root user, check file ownership

**Build failures**: Check Dockerfile layer caching, dependencies

### Debugging Production

- Check platform logs
- Use remote Erlang console (if available)
- Enable debug logging temporarily
- Monitor resource usage

## Rollback Strategies

- Keep previous release artifacts
- Use platform rollback features (Fly.io, AWS, etc.)
- Database migration rollback plan
- Feature flags for gradual rollout

## Scaling Considerations

### Vertical Scaling
- Increase instance size
- Adjust BEAM settings
- Optimize resource usage

### Horizontal Scaling
- Add more instances
- Configure load balancing
- Ensure stateless design or shared state storage

### Database Scaling
- Read replicas
- Connection pooling
- Query optimization
- Caching layer

## Zero-Downtime Deployment

Strategies:
- Blue-green deployment
- Rolling updates
- Feature flags
- Health check integration

---

**Remember**: Gleam compiles to mature, battle-tested runtimes (BEAM, JavaScript). Focus on platform-specific deployment concerns.

See: [Gleam FAQ - Production](https://gleam.run/frequently-asked-questions/)

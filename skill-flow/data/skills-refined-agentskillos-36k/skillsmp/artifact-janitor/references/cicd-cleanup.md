# CI/CD Cleanup Optimization (2026)

In a Continuous Integration environment, cleaning up is about balance: you want a clean state for reliability, but you want to preserve caches for speed.

## 1. GitHub Actions Caching Strategies

Avoid total wipes in CI. Instead, use the `actions/cache` or the built-in Bun/pnpm caching.

```yaml
- name: Setup Bun
  uses: oven-sh/setup-bun@v2
  with:
    bun-version: latest
    cache: true # Automatically manages cache cleanup
```

## 2. Post-Build Cleanup

Always remove temporary artifacts before the next stage to keep runner disk usage low.

```yaml
- name: Build
  run: bun run build

- name: Post-Build Cleanup
  if: always()
  run: |
    rm -rf .next/cache
    rm -rf .turbo
```

## 3. Ephemeral Runners

If using ephemeral runners (e.g., self-hosted on AWS/K8s), a full wipe isn't necessary as the environment is destroyed after the job. However, if using persistent runners:

-   Run `docker system prune -f` weekly.
-   Implement a cron job to run `artifact-janitor/scripts/deep-clean.sh` on stagnant workspace directories.

## 4. Docker Multi-Stage Builds

The best cleanup is not having anything to clean. Use multi-stage builds to leave artifacts in the build layer.

```dockerfile
# Build Stage
FROM oven/bun:latest AS builder
WORKDIR /app
COPY . .
RUN bun install && bun run build

# Runtime Stage
FROM oven/bun:distroless
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
# node_modules and other junk are left behind in the builder stage
CMD ["server.js"]
```

---
*Updated: January 22, 2026 - 16:55*

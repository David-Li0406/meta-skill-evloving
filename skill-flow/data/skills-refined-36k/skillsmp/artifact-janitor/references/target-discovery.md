# Target Discovery: Identifying Build Artifacts in 2026

Modern development environments generate a wide variety of transient files. Knowing what to target is key to effective disk management.

## Common Targets by Ecosystem

### Next.js & React
-   `.next/`: Production build output and cache.
-   `out/`: Static export output.
-   `.turbo/`: Turborepo build cache.

### General JavaScript/TypeScript
-   `node_modules/`: Package dependencies.
-   `dist/` or `build/`: Transpiled code.
-   `tsconfig.tsbuildinfo`: Incremental build info for TypeScript.
-   `coverage/`: Test coverage reports.

### Package Manager Caches
-   `~/.bun/install/cache`: Bun's global cache.
-   `~/.pnpm-store`: pnpm's global content-addressable store.
-   `~/.npm/_cacache`: npm's cache.

### Logs & Temp Files
-   `*.log`: Application or system logs (e.g., `npm-debug.log`, `bun.log`).
-   `.DS_Store`: macOS folder metadata.
-   `tmp/`: Temporary processing directories.

## Discovery Commands

### Finding Large Directories
To find the largest directories in your project:
```bash
du -sh * | sort -hr | head -n 10
```

### Finding All `node_modules` (Monorepo)
```bash
find . -name "node_modules" -type d -prune
```

### Finding Large Log Files
```bash
find . -name "*.log" -size +10M
```

## When to Clean

-   **Disk Space Low**: Standard cleanup of `node_modules` and caches.
-   **Strange Build Errors**: Occurs when `.next/cache` or `node_modules` becomes corrupted or out of sync with current code.
-   **Dependency Updates**: Recommended to clean `node_modules` and `lock` files when performing major version upgrades.
-   **Pre-Release**: Ensure the `dist/` or `out/` folder is fresh before deploying to production.

---
*Updated: January 22, 2026 - 16:45*

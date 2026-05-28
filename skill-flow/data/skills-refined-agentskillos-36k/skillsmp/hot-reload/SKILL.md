---
name: hot-reload
description: Development hot reload behavior. Auto-triggered when discussing file watching, rebuilds, or dev server.
---

# Hot Reload Behavior

How file changes trigger rebuilds in development.

## Quick Start

```bash
# Terminal 1: Start services
just dev

# Terminal 2: Watch for changes (REQUIRED for frontend hot reload)
just watch-templates
```

## Architecture Overview

**Pre-bundled frontend**: `frontend/dist/` is committed to git. No Vite dev server at runtime.

| Component | How Changes Work |
|-----------|------------------|
| Frontend (Astro) | Build to `frontend/dist/`, nginx serves immediately |
| Backend (Python) | uvicorn auto-reloads on file changes |
| Jinja2 templates | Auto-reload on request (no restart needed) |

## Frontend (chokidar + Astro Build)

File watching is handled by `just watch-templates` running in a separate terminal.

| File Type | Watch Pattern | Rebuild Output |
|-----------|---------------|----------------|
| `.astro` | `src/**/*.astro` | `frontend/dist/` |
| `.tsx/.ts` | `src/**/*.{ts,tsx}` | `frontend/dist/` |
| `.css` | `src/**/*.css` | `frontend/dist/_astro/*.css` |
| React islands | `src/islands/*.tsx` | `frontend/dist/islands/*.js` |

### Rebuild Process

1. chokidar detects file change
2. Triggers `pnpm build` (Astro)
3. Output written to `frontend/dist/`
4. nginx serves updated files immediately (bind mount)
5. Browser refresh shows changes

**Prerequisite:** `just watch-templates` must be running.

### Manual Build

If watch isn't running:
```bash
just build-frontend
```

### Committing Changes

After frontend changes, commit both source and dist:
```bash
git add frontend/src/ frontend/dist/
git commit -m "feat: Update frontend styles"
```

## Backend (uvicorn --reload)

uvicorn watches Python files automatically.

| File Type | Behavior |
|-----------|----------|
| `.py` | uvicorn auto-restarts (polling on Mac, inotify on Linux) |
| Jinja2 templates | Auto-reload on request (no restart needed) |
| Static files | Served directly by nginx, no restart needed |

**No action needed** - uvicorn handles Python file watching.

### Jinja2 Templates

Templates in `frontend/dist/` auto-reload on each request:
- No container restart
- No build step
- Just refresh browser

Templates in `frontend/dist/layouts/` (Astro-built wrapper):
- Rebuild with `just build-frontend`
- Or use `just watch-templates`

## Troubleshooting

### Changes Don't Appear

1. **Check watch is running:**
   ```bash
   docker compose exec -T frontend pgrep -f "chokidar"
   ```
   If no output: `just watch-templates` in new terminal

2. **Check for build errors:**
   ```bash
   docker compose logs frontend --tail=20
   ```

3. **Force rebuild:**
   ```bash
   just build-frontend
   ```

4. **Verify dist/ is updated:**
   ```bash
   ls -la frontend/dist/
   ```

### CSS Not Updating

CSS is compiled by Astro, not served directly.

1. Verify `frontend/src/styles/global.css` exists
2. Check `just watch-templates` is running
3. Look for `frontend/dist/_astro/*.css` file
4. Hard refresh browser (Cmd+Shift+R)

### React Islands Not Updating

Islands are built separately:

```bash
# Check if islands exist
ls frontend/dist/islands/

# Manual rebuild
docker compose exec frontend pnpm build:islands
```

### Python Changes Not Reloading

1. Check container is running:
   ```bash
   docker compose ps backend
   ```

2. Check logs for reload:
   ```bash
   docker compose logs backend --tail=20
   ```

3. Restart if stuck:
   ```bash
   docker compose restart backend
   ```

## Verification

Use the workflow-verifier agent or `/workflow-check` command:

```
/workflow-check
```

This tests all hot reload paths and reports status.

## File Type Quick Reference

| Change This | Requires | Appears After |
|-------------|----------|---------------|
| `.astro` page | watch running | ~4s + refresh |
| `.css` styles | watch running | ~4s + refresh |
| React island | watch running | ~4s + refresh |
| Python code | nothing | ~2s (auto) |
| Jinja2 template | nothing | instant on refresh |
| Static file | nothing | instant on refresh |

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| No CSS changes | Watch not running | `just watch-templates` |
| Astro not rebuilding | chokidar not started | Restart frontend or run watch |
| Python not reloading | Container issue | `docker compose restart backend` |
| Islands stale | Cache issue | `just fix-frontend-rebuild` |
| Build errors | Syntax error | Check `docker compose logs frontend` |

## Key Difference from Traditional Dev Servers

There is **no Vite dev server** running at runtime. The workflow is:

1. Edit files in `frontend/src/`
2. Watch process (or manual build) compiles to `frontend/dist/`
3. nginx serves pre-built files from the bind-mounted directory
4. No HMR - full page refresh needed

This architecture means:
- Simpler runtime (no dev server process)
- `frontend/dist/` is committed to git
- CI uses pre-committed dist (no build step)
- Production-like serving even in development

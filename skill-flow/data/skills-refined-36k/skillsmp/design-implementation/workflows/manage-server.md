# Manage Server Workflow

Dev server lifecycle management.

## Triggers

- "start the dev server"
- "stop the server"
- "restart the server"
- "is the server running?"
- "what port is the server on?"

## Commands

### Start Server

```bash
bun ${SKILL_DIR}/tools/server-manager.ts start
```

Auto-detects:
- Port from package.json scripts
- Start command (dev, start, serve)

**Override:**
```bash
bun ${SKILL_DIR}/tools/server-manager.ts start --port 3000 --command "bun run dev"
```

### Stop Server

```bash
bun ${SKILL_DIR}/tools/server-manager.ts stop
```

### Check Status

```bash
bun ${SKILL_DIR}/tools/server-manager.ts status
```

Output:
```json
{
  "port": 5173,
  "running": true,
  "pid": 12345,
  "url": "http://localhost:5173"
}
```

### Detect Port

```bash
bun ${SKILL_DIR}/tools/server-manager.ts detect-port
```

Parses package.json for:
- `--port` or `-p` flags
- Framework defaults (vite: 5173, next: 3000, etc.)

### Wait for Ready

```bash
bun ${SKILL_DIR}/tools/server-manager.ts wait-ready --timeout 30000
```

Polls until server responds with 200/304.

## Framework Detection

| Framework | Default Port | Detection |
|-----------|--------------|-----------|
| Vite | 5173 | `vite` in dev script |
| Next.js | 3000 | `next` in dev script |
| SvelteKit | 5173 | `svelte` in dev script |
| Gatsby | 8000 | `gatsby` in dev script |
| Nuxt | 3000 | `nuxt` in dev script |
| Astro | 4321 | `astro` in dev script |
| Bun.serve | 3000 | Fallback |

## Error Handling

### Server Won't Start

```
Causes:
- Port already in use → Kill existing process
- Missing dependencies → Run bun install
- Config error → Check package.json

Recovery:
1. Check what's using the port: lsof -i :${PORT}
2. Kill if needed: kill ${PID}
3. Retry start
```

### Server Crashes

```
Max restarts: 3 (from config)

On crash:
1. Log crash reason
2. Wait 2s
3. Restart
4. If crash again, increment counter
5. If counter >= max, report to user
```

### HMR Not Working

```
Symptoms:
- Changes not reflecting
- Full page reload required

Fixes:
1. Check HMR delay config (increase if needed)
2. Force full reload: page.reload()
3. Restart server
```

## State Updates

Server state tracked in `state.json`:

```json
{
  "serverPid": 12345,
  "serverPort": 5173,
  "serverStartedAt": "2026-01-08T10:00:00Z",
  "browserConnected": true
}
```

## Integration

Used by:
- `implement-feature` workflow (ensure server running)
- `verify-visual` workflow (server must be up)
- Manual invocation for debugging

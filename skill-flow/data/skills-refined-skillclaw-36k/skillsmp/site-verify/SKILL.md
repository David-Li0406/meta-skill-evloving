---
name: site-verify
description: Interactive site verification for user journey testing. Use for full-stack verification, catching 404s, console errors, network failures, and DB state validation during development.
---

# Site Verification Skill

Interactive verification of the complete user journey with Chrome DevTools MCP.

## Prerequisites

**Required:**
- Docker services running (`just dev`)
- Chrome DevTools MCP connected
- User logged in for authenticated flows (`./worktree.py auth-status`)

**Verify before starting:**
```bash
docker compose ps  # Services running
curl -s http://localhost:9010/health  # Backend healthy
```

## User Journey Checklist

Work through each step in order. At each step:
1. Navigate to the page
2. Take a snapshot (`mcp__chrome-devtools__take_snapshot`)
3. Check console for errors (`mcp__chrome-devtools__list_console_messages`)
4. Check network for failures (`mcp__chrome-devtools__list_network_requests`)
5. Report status to user before proceeding

### 1. Public Pages (No Auth)

| Step | URL | Verify |
|------|-----|--------|
| Home | `/` | Page loads, links work |
| About | `/about` | Static page renders |
| Login | `/login` | Form displayed |
| Browse Gear | `/gear` | Packs displayed, filters work |
| Gear Detail | `/gear/{slug}` | Pack info, models listed |
| DI Tracks Browse | `/di-tracks` | Tracks displayed, filters work |
| DI Track Detail | `/di-tracks/{id}` | Track info displayed |

### 2. Authentication Flow

| Step | Action | Verify |
|------|--------|--------|
| Login | Click login, complete OAuth | Redirected to callback |
| Session | Check `/api/v1/auth/me` | Returns user info |
| Logout | Click logout | Session cleared |

### 3. My Library (Authenticated)

| Step | URL | Verify | DB Check |
|------|-----|--------|----------|
| My Gear | `/library/my-gear` | Page loads, empty state or gear shown | - |
| Add Gear | Add from `/gear/{slug}` | Toast shown, gear appears | `user_gear` record |
| Remove Gear | Delete from My Gear | Item disappears | Record deleted |

### 4. Signal Chains (Authenticated)

| Step | URL | Verify | DB Check |
|------|-----|--------|----------|
| My Chains | `/library/chains` | Groups displayed | - |
| Create Group | New chain form | Group created | `signal_chain_groups` |
| Chain Builder | `/library/chains/build` | React component loads | - |
| Add Gear | Drag gear to chain | Block appears | `signal_chain_blocks` |
| Save Chain | Save button | Success message | Chain persisted |

### 5. DI Tracks (Authenticated)

| Step | URL | Verify | DB Check |
|------|-----|--------|----------|
| My DI Tracks | `/library/di-tracks` | Page loads | - |
| Upload Track | Upload form | File accepted | `di_tracks` record |
| Track Detail | `/di-tracks/{id}` | Info displayed | - |

### 6. Shootouts (Authenticated)

| Step | URL | Verify | DB Check |
|------|-----|--------|----------|
| Create | `/shootouts` → create | Form displayed | - |
| Submit | Select DI + chains | Job created | `shootouts`, `jobs` |
| Processing | Wait for completion | Status updates | Job state changes |
| My Shootouts | `/library/shootouts` | Results displayed | - |
| Playback | Video player | Video plays | - |

## Verification Commands

### Check Console Errors

```
mcp__chrome-devtools__list_console_messages (types: ["error", "warn"])
```

Report any errors found.

### Check Network Failures

```
mcp__chrome-devtools__list_network_requests
```

Look for non-2xx status codes.

### Verify DB State

```bash
docker compose exec backend python -c "
import asyncio
from app.core.database import async_session
from sqlalchemy import text

async def check():
    async with async_session() as session:
        result = await session.execute(text('SELECT COUNT(*) FROM user_gear'))
        print(f'user_gear records: {result.scalar()}')

asyncio.run(check())
"
```

## Issue Resolution

When a bug is found:

1. **Document** the exact error (console log, network failure, visual)
2. **Investigate** the root cause
3. **Fix** the issue
4. **Verify** the fix via MCP
5. **Update tests** to prevent regression
6. **Continue** verification

## Output Format

After completing verification:

```markdown
## Site Verification Report

### Summary
- Pages verified: X/Y
- Issues found: N
- Issues fixed: M

### Public Pages
| Page | Status | Notes |
|------|--------|-------|
| Home | PASS | - |
| About | PASS | - |
| Browse Gear | PASS | - |

### Authenticated Pages
| Page | Status | Notes |
|------|--------|-------|
| My Gear | PASS | - |
| Chain Builder | PASS | - |

### Issues Found & Fixed
1. [Issue description] - Fixed in [file]
2. ...

### Tests Updated
- `tests/e2e/python/tests/test_xxx.py` - Added test for Y
```

## Related Skills

- `chrome-devtools` - MCP tool reference
- `screenshot-eval` - Visual error detection
- `playwright` - Automated E2E tests

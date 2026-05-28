---
name: backend-server-startup
description: Start the Budget Buddy FastAPI backend server on port 8000 with automatic CORS validation and error detection. Use when starting the backend, fixing server startup issues, debugging connection problems, or when the user asks to run/start the backend.
allowed-tools: [Bash(python*), Bash(pkill:*), Bash(lsof:*), Bash(ps:*), Read, Grep]
---

# Backend Server Startup

## Overview

This skill helps you start the Budget Buddy FastAPI backend server correctly with automatic validation of CORS configuration, API paths, and common startup issues. It prevents the most frequent errors documented in the project's development guide.

## Prerequisites

- Python 3.9+ installed
- Virtual environment created at `.venv/`
- Backend dependencies installed
- Working directory: `/Users/franklindickinson/Projects/budget-buddy-2` (project root)

## Quick Start

### 1. Verify Working Directory

**CRITICAL**: The backend MUST be started from the project root, not from the `/backend` directory.

```bash
pwd
# Should show: /Users/franklindickinson/Projects/budget-buddy-2
```

If in wrong directory:
```bash
cd /Users/franklindickinson/Projects/budget-buddy-2
```

### 2. Check Port Availability

```bash
lsof -i :8000
```

If port 8000 is in use, kill the existing process:
```bash
pkill -f "uvicorn.*8000"
```

### 3. Start the Backend

```bash
python -m uvicorn backend.api.main:app --reload --port 8000
```

**Alternative** (using server.py entry point):
```bash
python backend/server.py
```

### 4. Verify Startup Success

Look for these lines in the output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

Test with curl:
```bash
curl -i http://127.0.0.1:8000/api/v2/transactions
```

Should return HTTP 200 or data (not 405 or CORS error).

## Key Validation Points

### 1. CORS Configuration (CRITICAL)

The backend MUST have CORS middleware configured for local development. Check `/backend/api/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Signs CORS is Missing**:
- Frontend shows "Failed to fetch" errors
- Backend logs show `405 Method Not Allowed` for OPTIONS requests
- Browser console shows CORS policy errors
- No data loads in frontend

### 2. API Path Configuration

The `base_path` in `/backend/api/main.py` must be:
```python
base_path = "/api/v2"
```

Frontend expects: `http://127.0.0.1:8000/api/v2/...`

### 3. Module Import Paths

When running from project root, Python can find modules with `backend.` prefix:
```python
from backend.database.session import get_session
from backend.services.database_service import DatabaseService
```

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'backend'"

**Cause**: Running uvicorn from `/backend` directory instead of project root

**Solution**:
```bash
cd /Users/franklindickinson/Projects/budget-buddy-2
python -m uvicorn backend.api.main:app --reload --port 8000
```

### Issue: "Address already in use"

**Cause**: Another process is using port 8000

**Solution**:
```bash
# Find process
lsof -i :8000

# Kill it
pkill -f "uvicorn.*8000"

# Or kill by PID
kill -9 <PID>
```

### Issue: Frontend can't load transactions

**Checklist**:
1. ✅ Backend running on port 8000?
2. ✅ CORS middleware configured?
3. ✅ `base_path = "/api/v2"`?
4. ✅ Frontend API config: `http://127.0.0.1:8000/api/v2`?
5. ✅ Database file exists at project root?

### Issue: "Failed to fetch" or network errors

**Solution**:
1. Check CORS configuration in `/backend/api/main.py`
2. Verify backend logs for OPTIONS requests (should return 200, not 405)
3. Check browser console for specific CORS error messages
4. Ensure frontend is calling correct API base URL

## Technical Details

### Entry Points

Budget Buddy has two backend entry points:

1. **`backend/api/main.py`** (API v2)
   - Contains all routers
   - Requires `base_path = "/api/v2"`
   - Used for development with: `python -m uvicorn backend.api.main:app --reload --port 8000`

2. **`backend/server.py`** (Primary)
   - Mounts API app at `/api`
   - Handles database initialization
   - Used with: `python backend/server.py`

### Database Initialization

Database auto-initializes on startup via `startup_event()` in `server.py`:
- Creates SQLite database at project root: `budget_buddy.db`
- Runs any pending migrations
- Initializes all tables from SQLAlchemy models

### API Routes

26 routers under `/api/v2/`:
- `/transactions` - Transaction CRUD
- `/budgets` - Budget management
- `/budget-categories` - Category definitions
- `/income` - Monthly income tracking
- `/ml` - Machine learning classification
- `/unified-classification` - Combined classification
- `/plaid` - Bank integration
- `/accounts` - Account management
- `/diagnostics` - Health checks
- `/sinking-funds` - Sinking fund management
- `/month-end-review` - Monthly reflections
- `/weekly-check-in` - Weekly reviews
- `/weekly-plans` - Weekly planning
- `/merchant-analytics` - Merchant insights
- `/buddy` - AI insights (Buddy AI)
- Plus: trip-tags, goals, reflections, etc.

## Testing the Skill

1. **Kill any existing backend process**
   ```bash
   pkill -f "uvicorn.*8000"
   ```

2. **Start backend using this skill's instructions**
   ```bash
   cd /Users/franklindickinson/Projects/budget-buddy-2
   python -m uvicorn backend.api.main:app --reload --port 8000
   ```

3. **Verify success**
   ```bash
   curl http://127.0.0.1:8000/api/v2/transactions
   ```

4. **Check CORS**
   ```bash
   curl -i -X OPTIONS http://127.0.0.1:8000/api/v2/transactions \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET"
   ```

   Should return headers including:
   ```
   access-control-allow-origin: http://localhost:3000
   access-control-allow-methods: *
   ```

## Integration with Other Skills

- **Full-Stack Setup** - Creates the initial environment
- **Development Diagnostics** - Validates backend is running correctly
- **Testing & Validation Suite** - Requires backend running for API tests

## References

- `/backend/api/main.py:1-167` - CORS config, base_path, routers
- `/backend/server.py:1-162` - Main server entry point
- `/backend/database/session.py:1-89` - Database initialization
- `CLAUDE.md` - Complete development guidelines
- `restart_all.sh` - Reference startup script

## Last Updated

January 1, 2026

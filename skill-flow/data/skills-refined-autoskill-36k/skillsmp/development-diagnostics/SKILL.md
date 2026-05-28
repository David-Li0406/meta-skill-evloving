---
name: development-diagnostics
description: Validate Budget Buddy full-stack setup including backend/frontend connectivity, database access, CORS, environment variables, and API endpoints. Use when troubleshooting, running health checks, or diagnosing setup issues.
allowed-tools: [Bash(curl*), Bash(python*), Bash(lsof:*), Bash(ps:*), Bash(sqlite3:*), Read, Grep]
---

# Development Diagnostics

Comprehensive health checks for Budget Buddy's development environment.

## Quick Diagnostic Checklist

```
System Health:
- [ ] Python 3.9+ installed
- [ ] Node.js 16+ installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Database file exists and accessible
- [ ] Environment variables configured
- [ ] API endpoints responding
- [ ] CORS headers present
```

## Fast Health Check

```bash
# Check processes
lsof -i :8000  # Backend
lsof -i :3000  # Frontend

# Check database
ls -lh budget_buddy.db
sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions;"

# Test API
curl -s http://127.0.0.1:8000/api/v2/diagnostics

# Test CORS
curl -I -X OPTIONS http://127.0.0.1:8000/api/v2/transactions \
  -H "Origin: http://localhost:3000" | grep "access-control-allow-origin"
```

## Essential Checks

### 1. System Requirements

```bash
python --version  # Need 3.9+
node --version    # Need 16+
```

### 2. Running Processes

```bash
# Backend (should show uvicorn on port 8000)
lsof -i :8000

# Frontend (should show node on port 3000)
lsof -i :3000
```

If missing, start them:
```bash
# Backend
python -m uvicorn backend.api.main:app --reload --port 8000

# Frontend
cd frontend && npm start
```

### 3. Database Status

```bash
# File exists with data
ls -lh budget_buddy.db

# Tables exist (should show 14 tables)
sqlite3 budget_buddy.db ".tables"

# Accessible
sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions;"
```

### 4. Environment Variables

```bash
# Check required variables
grep ANTHROPIC_API_KEY .env
grep PLAID_CLIENT_ID .env
grep DATABASE_URL .env
```

### 5. API Endpoints

```bash
# Diagnostics endpoint
curl -s http://127.0.0.1:8000/api/v2/diagnostics | python -m json.tool

# Transactions endpoint
curl -s http://127.0.0.1:8000/api/v2/transactions | python -m json.tool | head -20

# Buddy AI status
curl -s http://127.0.0.1:8000/api/v2/buddy/status | python -m json.tool
```

### 6. CORS Validation

```bash
curl -I -X OPTIONS http://127.0.0.1:8000/api/v2/transactions \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

**Expected headers**:
- `access-control-allow-origin: http://localhost:3000`
- `access-control-allow-methods: *`
- `access-control-allow-credentials: true`

## Common Issues

### Backend not responding
```bash
# Check if running
lsof -i :8000

# If not, start it
cd /Users/franklindickinson/Projects/budget-buddy-2
python -m uvicorn backend.api.main:app --reload --port 8000
```

### CORS errors
```bash
# Verify CORS middleware exists
grep -A 6 "CORSMiddleware" backend/api/main.py

# Should show allow_origins with localhost:3000
```

### Database locked
```bash
# Find locking process
lsof budget_buddy.db

# Kill backend and restart
pkill -f "uvicorn.*8000"
sleep 2
python -m uvicorn backend.api.main:app --reload --port 8000
```

### Environment variables not loading
```bash
# Verify .env in project root (not /backend)
ls -la .env

# Test loading
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY')[:20] if os.getenv('ANTHROPIC_API_KEY') else 'NOT FOUND')"
```

## Detailed Diagnostics

**Comprehensive scripts and procedures**: See [DIAGNOSTIC_SCRIPTS.md](DIAGNOSTIC_SCRIPTS.md)

Includes:
- Full diagnostic suite bash script
- Python health check script
- Diagnostic report generator
- Performance checks (response time, query time, memory)
- All issue solutions with detailed commands

## Integration with Other Skills

- **Backend Server Startup** - Validates backend started correctly
- **Full-Stack Setup** - Verifies complete environment
- **Database Migration Runner** - Checks schema is current
- **Buddy AI Setup** - Validates API key and config

## References

- [DIAGNOSTIC_SCRIPTS.md](DIAGNOSTIC_SCRIPTS.md) - Complete scripts and procedures
- `/backend/api/main.py` - CORS configuration
- `/frontend/src/config/apiConfig.js` - Frontend API base URL
- `CLAUDE.md` - Development guidelines

## Last Updated

January 1, 2026

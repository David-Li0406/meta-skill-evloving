# Diagnostic Scripts and Detailed Checks

Complete diagnostic procedures and scripts for Budget Buddy development environment.

## Full Diagnostic Suite Script

```bash
#!/bin/bash
# comprehensive_diagnostics.sh

echo "=== Budget Buddy Development Diagnostics ==="
echo ""

# 1. System Requirements
echo "1. Checking Python version..."
python --version

echo "2. Checking Node.js version..."
node --version

# 2. Running Processes
echo "3. Checking backend (port 8000)..."
lsof -i :8000

echo "4. Checking frontend (port 3000)..."
lsof -i :3000

# 3. Database
echo "5. Checking database file..."
ls -lh budget_buddy.db
echo "Tables:"
sqlite3 budget_buddy.db ".tables"
echo "Transaction count:"
sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions;"

# 4. Environment Variables
echo "6. Checking environment variables..."
grep -E "ANTHROPIC_API_KEY|PLAID|DATABASE_URL" .env | cut -d'=' -f1

# 5. API Tests
echo "7. Testing backend API endpoints..."
curl -s http://127.0.0.1:8000/api/v2/diagnostics | python -m json.tool

# 6. CORS Test
echo "8. Testing CORS configuration..."
curl -I -X OPTIONS http://127.0.0.1:8000/api/v2/transactions \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" | grep "access-control"

echo ""
echo "=== Diagnostics Complete ==="
```

## Python Health Check Script

```python
#!/usr/bin/env python3
# health_check.py

import requests
import sys
import sqlite3

def check_backend():
    """Check backend is responding"""
    try:
        response = requests.get('http://127.0.0.1:8000/api/v2/diagnostics', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_database():
    """Check database is accessible"""
    try:
        conn = sqlite3.connect('budget_buddy.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM transactions')
        count = cursor.fetchone()[0]
        conn.close()
        return True
    except:
        return False

def check_cors():
    """Check CORS headers"""
    try:
        response = requests.options(
            'http://127.0.0.1:8000/api/v2/transactions',
            headers={
                'Origin': 'http://localhost:3000',
                'Access-Control-Request-Method': 'GET'
            },
            timeout=5
        )
        return 'access-control-allow-origin' in response.headers
    except:
        return False

def main():
    print("Running health checks...")

    checks = {
        'Backend': check_backend(),
        'Database': check_database(),
        'CORS': check_cors(),
    }

    for name, result in checks.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")

    if all(checks.values()):
        print("\n✅ All checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some checks failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()
```

## Diagnostic Report Generator

```bash
#!/bin/bash
# diagnostic_report.sh

OUTPUT_FILE="diagnostic_report.txt"

exec > >(tee -a "$OUTPUT_FILE")
exec 2>&1

echo "========================================="
echo "Budget Buddy Diagnostic Report"
echo "Generated: $(date)"
echo "========================================="
echo ""

# System Info
echo "--- SYSTEM INFO ---"
echo "OS: $(uname -s)"
echo "Python: $(python --version 2>&1)"
echo "Node: $(node --version 2>&1)"
echo "npm: $(npm --version 2>&1)"
echo ""

# Running Processes
echo "--- RUNNING PROCESSES ---"
echo "Backend (port 8000):"
lsof -i :8000 2>&1
echo ""
echo "Frontend (port 3000):"
lsof -i :3000 2>&1
echo ""

# Database
echo "--- DATABASE ---"
echo "File: $(ls -lh budget_buddy.db 2>&1)"
echo "Tables: $(sqlite3 budget_buddy.db '.tables' 2>&1)"
echo "Transaction count: $(sqlite3 budget_buddy.db 'SELECT COUNT(*) FROM transactions;' 2>&1)"
echo ""

# Environment
echo "--- ENVIRONMENT VARIABLES ---"
echo "ANTHROPIC_API_KEY: $(grep ANTHROPIC_API_KEY .env | cut -d'=' -f1)"
echo "PLAID_CLIENT_ID: $(grep PLAID_CLIENT_ID .env | cut -d'=' -f1)"
echo "DATABASE_URL: $(grep DATABASE_URL .env | cut -d'=' -f1)"
echo ""

# API Tests
echo "--- API ENDPOINT TESTS ---"
echo "Diagnostics endpoint:"
curl -s http://127.0.0.1:8000/api/v2/diagnostics 2>&1
echo ""
echo "CORS test:"
curl -I -X OPTIONS http://127.0.0.1:8000/api/v2/transactions \
  -H "Origin: http://localhost:3000" 2>&1 | grep "access-control"
echo ""

echo "========================================="
echo "Report saved to: $OUTPUT_FILE"
echo "========================================="
```

## Common Issue Solutions

### Issue: Backend not responding

```bash
# Check if backend is running
lsof -i :8000

# If nothing, start it
cd /Users/franklindickinson/Projects/budget-buddy-2
python -m uvicorn backend.api.main:app --reload --port 8000
```

### Issue: Database locked

```bash
# Find what's locking the database
lsof budget_buddy.db

# Kill backend
pkill -f "uvicorn.*8000"

# Wait and restart
sleep 2
python -m uvicorn backend.api.main:app --reload --port 8000
```

### Issue: CORS errors

```bash
# Verify CORS middleware in backend/api/main.py
grep -A 6 "CORSMiddleware" backend/api/main.py

# Should show:
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
#     ...
# )
```

### Issue: Environment variables not loading

```bash
# Verify .env file exists in project root
ls -la .env

# Check it's being loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('ANTHROPIC_API_KEY')[:20] if os.getenv('ANTHROPIC_API_KEY') else 'NOT FOUND')"
```

## Performance Checks

### API Response Time

```bash
# Measure response time
time curl -s http://127.0.0.1:8000/api/v2/transactions >/dev/null
```

Expected: < 1 second

### Database Query Performance

```bash
# Measure query time
time sqlite3 budget_buddy.db "SELECT * FROM transactions WHERE date >= '2026-01-01';"
```

Expected: < 0.5 seconds

### Memory Usage

```bash
# Check backend memory
ps aux | grep uvicorn | awk '{print $6/1024 " MB"}'
```

Expected: < 500 MB

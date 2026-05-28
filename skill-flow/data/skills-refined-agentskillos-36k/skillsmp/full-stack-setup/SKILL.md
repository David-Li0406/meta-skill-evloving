---
name: full-stack-setup
description: Complete development environment setup for Budget Buddy including Python virtual environment, Node.js dependencies, database initialization, and environment variables. Use for first-time setup, initializing project for new developers, or when the user asks to setup/initialize the development environment.
allowed-tools: [Bash(python*), Bash(npm*), Bash(pip*), Bash(node*), Bash(which*), Read, Grep]
---

# Full-Stack Environment Setup

## Overview

This skill guides you through the complete one-time initialization of the Budget Buddy development environment. It sets up both backend (Python/FastAPI) and frontend (React) with all dependencies, database, and configuration.

## Prerequisites

- **Python 3.9+** installed on system
- **Node.js 16+** and npm installed
- **Git** repository cloned
- Working directory: `/Users/franklindickinson/Projects/budget-buddy-2`

## Quick Start

### Step 1: Verify System Requirements

```bash
# Check Python version (need 3.9+)
python --version

# Check Node.js version (need 16+)
node --version

# Check npm
npm --version
```

If versions are too low, install/upgrade before continuing.

### Step 2: Backend Setup

#### 2.1 Create Virtual Environment

```bash
cd /Users/franklindickinson/Projects/budget-buddy-2
python -m venv .venv
```

#### 2.2 Activate Virtual Environment

```bash
source .venv/bin/activate
```

#### 2.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM
- `anthropic>=0.40.0` - Buddy AI
- `plaid-python` - Bank integrations
- `python-dotenv` - Environment variables

#### 2.4 Verify Installation

```bash
python -c "import fastapi; import anthropic; import plaid; print('Backend dependencies OK')"
```

### Step 3: Frontend Setup

#### 3.1 Install Node Dependencies

```bash
cd frontend
npm install
cd ..
```

**Key Dependencies**:
- `react` - UI library
- `react-bootstrap` - UI components
- `react-router-dom` - Routing
- `recharts` - Data visualization

#### 3.2 Verify Installation

```bash
cd frontend
npm list react react-bootstrap
cd ..
```

### Step 4: Environment Variables

#### 4.1 Check for .env File

```bash
ls -la .env
```

If missing, create from template:
```bash
cp .env.example .env  # if template exists
# OR create manually
touch .env
```

#### 4.2 Required Environment Variables

Edit `.env` and add:

```bash
# Database
DATABASE_URL=sqlite:///./budget_buddy.db

# Anthropic API (for Buddy AI)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Plaid (Bank Integration)
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET_SANDBOX=your_sandbox_secret
PLAID_SECRET_DEVELOPMENT=your_dev_secret
PLAID_SECRET_PRODUCTION=your_prod_secret
PLAID_ENV=sandbox
PLAID_REDIRECT_URI=http://localhost:3000/oauth-redirect

# Optional: Supabase (legacy, kept for data export)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

#### 4.3 Validate Environment Variables

```bash
# Check ANTHROPIC_API_KEY is set
grep ANTHROPIC_API_KEY .env

# Check PLAID variables
grep PLAID_ .env
```

**CRITICAL**:
- `ANTHROPIC_API_KEY` required for Buddy AI features
- `PLAID_*` required for bank transaction imports
- Format: `ANTHROPIC_API_KEY` should start with `sk-ant-`

### Step 5: Database Initialization

#### 5.1 Create Database File

The database auto-initializes on first backend startup, but you can create it manually:

```bash
# Database will be created at: budget_buddy.db
python -c "from backend.database.session import init_db; init_db()"
```

#### 5.2 Verify Database Created

```bash
ls -lh budget_buddy.db
```

Should show the SQLite database file (initially ~100KB).

#### 5.3 Check Tables Created

```bash
sqlite3 budget_buddy.db ".tables"
```

Should show 14 tables:
- transactions
- budget_allocations
- monthly_income
- monthly_reflections
- sinking_funds
- sinking_fund_transactions
- institutions
- accounts
- account_connection_log
- weekly_summaries
- subscription_patterns
- weekly_reflections
- weekly_plans
- chat_goals

### Step 6: Verify Full Setup

#### 6.1 Start Backend

```bash
python -m uvicorn backend.api.main:app --reload --port 8000
```

Should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### 6.2 Test Backend (in new terminal)

```bash
curl http://127.0.0.1:8000/api/v2/diagnostics
```

Should return JSON with system status.

#### 6.3 Start Frontend (in new terminal)

```bash
cd /Users/franklindickinson/Projects/budget-buddy-2/frontend
npm start
```

Should see:
```
Compiled successfully!
You can now view budget-buddy in the browser.
  Local:            http://localhost:3000
```

#### 6.4 Open Browser

Navigate to `http://localhost:3000`

Should see Budget Buddy app load (even if no data yet).

## Key Validation Points

### Python Environment
- ✅ Python 3.9+ installed
- ✅ Virtual environment created at `.venv/`
- ✅ All requirements.txt packages installed
- ✅ Can import: fastapi, anthropic, plaid, sqlalchemy

### Node Environment
- ✅ Node.js 16+ installed
- ✅ npm dependencies installed in `frontend/node_modules/`
- ✅ Can run `npm start` without errors

### Environment Variables
- ✅ `.env` file exists at project root
- ✅ `ANTHROPIC_API_KEY` set (format: sk-ant-...)
- ✅ `PLAID_CLIENT_ID` and secrets set
- ✅ `DATABASE_URL` points to SQLite file

### Database
- ✅ `budget_buddy.db` file exists
- ✅ All 14 tables created
- ✅ Database accessible from backend

### Services Running
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Backend responds to `/api/v2/diagnostics`
- ✅ Frontend loads in browser

## Common Issues & Solutions

### Issue: pip install fails with SSL errors

**Solution**:
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r backend/requirements.txt
```

### Issue: npm install fails with permission errors

**Solution**:
```bash
# Don't use sudo! Fix npm permissions instead:
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH

# Then retry
npm install
```

### Issue: Database file won't create

**Solution**:
```bash
# Ensure project root is writable
cd /Users/franklindickinson/Projects/budget-buddy-2
touch test.txt && rm test.txt  # Test write permissions

# Create manually with SQLite
sqlite3 budget_buddy.db "VACUUM;"
```

### Issue: Backend can't import modules

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Verify Python is from venv
which python
# Should show: /Users/franklindickinson/Projects/budget-buddy-2/.venv/bin/python

# Re-install dependencies
pip install -r backend/requirements.txt
```

### Issue: ANTHROPIC_API_KEY not found

**Solution**:
1. Create `.env` file at project root (not in `/backend`)
2. Add: `ANTHROPIC_API_KEY=sk-ant-your-actual-key`
3. Don't commit `.env` to git (already in `.gitignore`)
4. Get key from: https://console.anthropic.com/

### Issue: Port 3000 or 8000 already in use

**Solution**:
```bash
# Kill process on port 8000
pkill -f "uvicorn.*8000"

# Kill process on port 3000
pkill -f "node.*3000"
```

## Technical Details

### Project Structure

```
budget-buddy-2/
├── .venv/                 # Python virtual environment
├── backend/
│   ├── api/              # API routes
│   ├── config/           # Configuration
│   ├── database/         # Models, migrations, session
│   ├── services/         # Business logic
│   ├── scripts/          # Utility scripts
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/              # React components
│   ├── public/           # Static assets
│   └── package.json      # Node dependencies
├── .env                  # Environment variables (not in git)
├── budget_buddy.db       # SQLite database (not in git)
├── CLAUDE.md             # Development guidelines
└── README.md             # Project overview
```

### Development Workflow

1. **Activate virtual environment**: `source .venv/bin/activate`
2. **Start backend**: `python -m uvicorn backend.api.main:app --reload --port 8000`
3. **Start frontend** (new terminal): `cd frontend && npm start`
4. **Develop**: Edit code, changes auto-reload
5. **Test**: Run tests with pytest (backend) and npm test (frontend)

### Port Configuration

- **Backend**: `http://127.0.0.1:8000` or `http://localhost:8000`
- **Frontend**: `http://localhost:3000`
- **API Base**: `http://127.0.0.1:8000/api/v2`

Frontend configured to call backend at this API base (see `frontend/src/config/apiConfig.js`).

## Testing the Skill

After running this skill, verify:

1. **Backend starts without errors**
   ```bash
   python -m uvicorn backend.api.main:app --reload --port 8000
   ```

2. **Frontend compiles and runs**
   ```bash
   cd frontend && npm start
   ```

3. **Database accessible**
   ```bash
   sqlite3 budget_buddy.db "SELECT COUNT(*) FROM transactions;"
   ```

4. **Environment variables loaded**
   ```bash
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('ANTHROPIC_API_KEY')[:20])"
   ```

## Integration with Other Skills

- **Backend Server Startup** - Uses the setup created here
- **Development Diagnostics** - Validates this setup is correct
- **Database Migration Runner** - Requires database initialized here
- **Buddy AI Setup** - Needs ANTHROPIC_API_KEY from .env

## References

- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies
- `.env.example` - Environment variable template (if exists)
- `backend/database/session.py:1-89` - Database initialization
- `CLAUDE.md` - Complete development guidelines

## Last Updated

January 1, 2026

# Setup Guide Patterns

Patterns for creating reliable local development setup guides.

## Document Structure

### 1. Prerequisites Section

```markdown
# Local Development Setup

## Prerequisites

Before starting, ensure you have:

| Tool | Version | Check Command | Install Link |
|------|---------|---------------|--------------|
| Node.js | 18+ | `node --version` | [nodejs.org](https://nodejs.org) |
| Docker | 20+ | `docker --version` | [docker.com](https://docker.com) |
| Git | 2.30+ | `git --version` | [git-scm.com](https://git-scm.com) |

### OS-Specific Requirements

<details>
<summary>macOS</summary>

```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install prerequisites
brew install node@18 docker git
```
</details>

<details>
<summary>Windows</summary>

```powershell
# Using winget
winget install OpenJS.NodeJS.LTS
winget install Docker.DockerDesktop
winget install Git.Git
```
</details>

<details>
<summary>Linux (Ubuntu/Debian)</summary>

```bash
# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs docker.io git
```
</details>
```

### 2. Quick Start Section

```markdown
## Quick Start

Get running in 5 minutes:

```bash
# 1. Clone the repository
git clone https://github.com/org/repo.git
cd repo

# 2. Install dependencies
npm install

# 3. Set up environment
cp .env.example .env

# 4. Start services
docker-compose up -d

# 5. Run migrations
npm run db:migrate

# 6. Start development server
npm run dev
```

✅ **Verify:** Open http://localhost:3000 - you should see the homepage.
```

### 3. Detailed Steps

```markdown
## Detailed Setup

### 1. Clone and Install

```bash
# Clone with submodules if any
git clone --recursive https://github.com/org/repo.git
cd repo

# Install dependencies
npm install

# If you see peer dependency warnings, they can usually be ignored
# If you see errors, check the Troubleshooting section
```

### 2. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Required variables to configure:

| Variable | Description | How to Get |
|----------|-------------|------------|
| `DATABASE_URL` | PostgreSQL connection | Use default for local |
| `API_KEY` | Third-party API key | Request from #dev-setup |
| `JWT_SECRET` | Token signing key | Generate: `openssl rand -hex 32` |

<details>
<summary>Example .env file</summary>

```env
# Database
DATABASE_URL=postgresql://localhost:5432/myapp_dev

# API Keys
API_KEY=your-api-key-here

# Security
JWT_SECRET=your-generated-secret

# Optional
DEBUG=true
LOG_LEVEL=debug
```
</details>

### 3. Database Setup

```bash
# Start PostgreSQL (via Docker)
docker-compose up -d postgres

# Wait for database to be ready
until docker-compose exec postgres pg_isready; do sleep 1; done

# Run migrations
npm run db:migrate

# Seed with test data (optional)
npm run db:seed
```

### 4. Start Development Server

```bash
# Start all services
npm run dev

# Or start specific services
npm run dev:api      # API only
npm run dev:worker   # Background workers
npm run dev:web      # Frontend only
```
```

## Verification Checklist

Include a verification section:

```markdown
## Verify Your Setup

Run through this checklist to ensure everything is working:

### 1. Health Check
```bash
curl http://localhost:3000/health
# Expected: {"status": "ok"}
```

### 2. Run Tests
```bash
npm test
# Expected: All tests pass
```

### 3. Login Flow
1. Open http://localhost:3000
2. Click "Sign Up"
3. Create account with test email
4. Verify redirect to dashboard

### 4. API Access
```bash
# Get auth token
TOKEN=$(curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.token')

# Make authenticated request
curl http://localhost:3000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
# Expected: User object returned
```
```

## Common Workflows

Document everyday tasks:

```markdown
## Common Development Tasks

### Running Tests
```bash
# All tests
npm test

# Specific file
npm test -- --grep "user service"

# With coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

### Database Tasks
```bash
# Create migration
npm run db:migration:create add_user_roles

# Run migrations
npm run db:migrate

# Rollback last migration
npm run db:rollback

# Reset database (careful!)
npm run db:reset
```

### Code Quality
```bash
# Lint code
npm run lint

# Fix lint issues
npm run lint:fix

# Type check
npm run typecheck

# All checks (pre-commit)
npm run check
```

### Building
```bash
# Development build
npm run build:dev

# Production build
npm run build

# Analyze bundle
npm run build:analyze
```
```

## Troubleshooting Section

```markdown
## Troubleshooting

### Port Already in Use

```bash
# Find what's using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or use a different port
PORT=3001 npm run dev
```

### Database Connection Failed

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart services
docker-compose restart postgres
```

### Node Module Issues

```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear npm cache if issues persist
npm cache clean --force
npm install
```

### Docker Issues

```bash
# Reset Docker environment
docker-compose down -v
docker-compose up -d

# Rebuild images
docker-compose build --no-cache
```

### Still Stuck?

1. Check #dev-help on Slack
2. Search existing issues on GitHub
3. Create a new issue with:
   - Your OS and version
   - Node/Docker versions
   - Full error message
   - Steps to reproduce
```

## Keeping Docs Current

```markdown
## Documentation Maintenance

This setup guide is verified against:
- **Node.js:** 18.x
- **Docker:** 24.x
- **Last verified:** 2024-01-15

If you encounter issues:
1. Check if your versions match
2. Report outdated instructions via PR
3. Update the "Last verified" date after fixes
```

# Sagebase Commands Reference

Comprehensive command reference for Sagebase operations.

## Command Prefix Convention

Throughout this document:
- **Just commands** (recommended): `just <command>`
- **Full Docker commands**: Use when `just` is not available

```bash
# Just command (short)
just test

# Full Docker command (verbose)
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml exec sagebase uv run pytest
```

**Note**: git worktreeを使用している場合、`docker-compose.override.yml`が自動生成されます。`just`コマンドはこれを自動検出しますが、手動でDocker Composeを実行する場合は必ず`-f docker/docker-compose.override.yml`を含めてください。

## 1. Environment Setup

### Initial Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env and set:
# - GOOGLE_API_KEY for Gemini API
# - GCS_BUCKET_NAME (optional, for cloud storage)
# - GCS_UPLOAD_ENABLED=true (optional)
```

### Docker Operations

```bash
# Start containers (with worktree support)
just up

# Start containers (manual)
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml up -d

# Stop containers
just down

# View logs
just logs

# View specific service logs
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml logs -f sagebase

# Check running containers
docker ps

# Show port configuration
just ports
```

### Dependency Installation

```bash
# Install UV dependencies (local development)
uv sync

# Run test setup script
./test-setup.sh
```

### Google Cloud Storage Setup

```bash
# Authenticate with GCS
gcloud auth application-default login

# Edit .env to enable GCS:
# GCS_BUCKET_NAME=your-bucket-name
# GCS_UPLOAD_ENABLED=true
```

### Port Configuration

When using git worktree, ports are automatically assigned to avoid conflicts:

```bash
# Check actual ports
docker ps
# or
cat docker/docker-compose.override.yml

# Common services:
# - Streamlit: varies by worktree (e.g., 9291)
# - API: varies by worktree (e.g., 8790)
# - Monitoring: varies by worktree (e.g., 9292)
# - PostgreSQL: 5432 (internal)
```

## 2. Application Commands

### Unified CLI (sagebase command)

All commands use: `just exec uv run sagebase <subcommand>`

#### Help

```bash
# Show all available commands
just exec uv run sagebase --help
```

#### Process Meeting Minutes

```bash
# Process all unprocessed minutes
just exec uv run sagebase process-minutes

# Process specific meeting (from GCS)
just exec uv run sagebase process-minutes --meeting-id 123
```

#### Scrape Politicians

```bash
# Scrape all parties
just exec uv run sagebase scrape-politicians --all-parties

# Scrape specific party
just exec uv run sagebase scrape-politicians --party-id 5

# Dry run (preview without saving)
just exec uv run sagebase scrape-politicians --all-parties --dry-run

# Hierarchical scraping (experimental)
just exec uv run sagebase scrape-politicians --party-id 5 --hierarchical
just exec uv run sagebase scrape-politicians --party-id 5 --hierarchical --max-depth 5
```

#### Speaker Operations

```bash
# Extract speakers from minutes
just exec uv run sagebase extract-speakers

# Update speaker links with LLM
just exec uv run sagebase update-speakers --use-llm
```

#### Web Scraping

```bash
# Scrape single meeting minutes
just exec uv run sagebase scrape-minutes "https://example.com/minutes"

# Scrape with GCS upload
just exec uv run sagebase scrape-minutes "URL" --upload-to-gcs
just exec uv run sagebase scrape-minutes "URL" --upload-to-gcs --gcs-bucket my-bucket

# Batch scrape multiple minutes
just exec uv run sagebase batch-scrape --tenant kyoto
just exec uv run sagebase batch-scrape --tenant osaka

# Batch scrape with GCS upload
just exec uv run sagebase batch-scrape --tenant kyoto --upload-to-gcs
```

#### Conference Member Extraction (3-step process)

```bash
# Step 1: Extract members from conference URLs
just exec uv run sagebase extract-conference-members --conference-id 185
just exec uv run sagebase extract-conference-members --force  # Re-extract all

# Step 2: Match with existing politicians
just exec uv run sagebase match-conference-members --conference-id 185
just exec uv run sagebase match-conference-members  # Process all pending

# Step 3: Create affiliations
just exec uv run sagebase create-affiliations --conference-id 185
just exec uv run sagebase create-affiliations --start-date 2024-01-01

# Check status
just exec uv run sagebase member-status --conference-id 185
```

#### Parliamentary Group Member Extraction (3-step process)

```bash
# Step 1: Extract members
just exec uv run sagebase extract-parliamentary-group-members --parliamentary-group-id 1
just exec uv run sagebase extract-parliamentary-group-members --force

# Step 2: Match with politicians
just exec uv run sagebase match-parliamentary-group-members --parliamentary-group-id 1
just exec uv run sagebase match-parliamentary-group-members  # Process all pending

# Step 3: Create memberships
just exec uv run sagebase create-parliamentary-group-affiliations --parliamentary-group-id 1
just exec uv run sagebase create-parliamentary-group-affiliations --start-date 2024-01-01
just exec uv run sagebase create-parliamentary-group-affiliations --min-confidence 0.8

# Check status
just exec uv run sagebase parliamentary-group-member-status --parliamentary-group-id 1
```

#### User Interfaces

```bash
# Launch Streamlit web UI
just exec uv run sagebase streamlit

# Launch monitoring dashboard
just exec uv run sagebase monitoring
# or
just monitoring
```

#### Coverage Statistics

```bash
# Show governing body coverage
just exec uv run sagebase coverage
```

### Legacy Direct Module Execution

These are older commands, prefer unified CLI above:

```bash
# Minutes division processing
just exec uv run python -m src.process_minutes

# Minutes processing from GCS
just exec uv run python -m src.process_minutes --meeting-id 123

# LLM-based speaker matching
just exec uv run python update_speaker_links_llm.py
```

## 3. Testing Commands

### Running Tests

```bash
# Run all tests
just test

# Run tests only (without pyright)
just pytest

# Run specific test file
just exec uv run pytest tests/unit/domain/test_speaker_domain_service.py

# Run specific test class
just exec uv run pytest tests/unit/domain/test_speaker_domain_service.py::TestSpeakerDomainService

# Run specific test function
just exec uv run pytest tests/unit/domain/test_speaker_domain_service.py::TestSpeakerDomainService::test_normalize_name

# Run only unit tests
just exec uv run pytest tests/unit/

# Run only integration tests
just exec uv run pytest tests/integration/ -m integration

# Run with verbose output
just exec uv run pytest -v

# Stop on first failure
just exec uv run pytest -x

# Show slowest tests
just exec uv run pytest --durations=10
```

### Test Coverage

```bash
# Run with coverage report
just exec uv run pytest --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html

# Coverage for specific module
just exec uv run pytest --cov=src/domain --cov-report=term
```

### Database Connection Test

```bash
# Test database connection
just exec uv run python -c "from src.config.database import test_connection; test_connection()"
```

### LLM Evaluation Tests

**Note**: Evaluation tests are NOT run in CI to save API costs.

```bash
# Run LLM evaluation tests (local - uses mock by default)
just exec uv run sagebase evaluate --all

# Run with real LLM API (manual only)
RUN_EVALUATION_TESTS=true just exec uv run pytest tests/evaluation/ -m evaluation
```

## 4. Code Quality Commands

### Ruff (Formatter and Linter)

```bash
# Format code
just format
# Full command:
# docker compose ... exec sagebase uv run --frozen ruff format .

# Check code style
just lint
# Full command:
# docker compose ... exec sagebase uv run --frozen ruff check .

# Fix auto-fixable issues
just exec uv run --frozen ruff check . --fix

# Check specific file
just exec uv run --frozen ruff check src/domain/entities/politician.py

# Show all rules
just exec uv run ruff linter
```

**Ruff Rules**:
- Line length: 88 characters
- Import sorting (I001)
- Unused imports removal
- Multi-line string formatting

### Type Checking (Pyright)

**IMPORTANT**: Run pyright locally, not in Docker (configuration issues in Docker).

```bash
# Run type checking (local only)
uv run --frozen pyright

# Check specific folder
uv run --frozen pyright src/domain/

# Check specific file
uv run --frozen pyright src/domain/entities/politician.py

# Filter output for specific folder
uv run --frozen pyright 2>&1 | grep -A5 -B5 "src/domain/"
```

**Pyright Requirements**:
- Explicit `None` checks for `Optional` types
- Proper type narrowing
- Follow `pyrightconfig.json` rules
- Version warnings can be ignored if type checks pass

### Pre-commit Hooks

```bash
# Install pre-commit hooks (first time only)
just exec uv run pre-commit install

# Run pre-commit manually on all files
just exec uv run pre-commit run --all-files

# Run on staged files only
just exec uv run pre-commit run

# Update hooks to latest versions
just exec uv run pre-commit autoupdate

# Bypass hooks (DISCOURAGED - fix errors instead!)
# git commit --no-verify  # DON'T USE THIS!
```

**Pre-commit Configuration**:
- Config: `.pre-commit-config.yaml`
- Runs automatically on `git commit`
- Tools: Prettier (YAML/JSON), Ruff (Python), standard hooks
- **NEVER use `--no-verify`** - fix errors instead!

## 5. Database Commands

### Connect to Database

```bash
# Connect via just
just db

# Full command
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml exec postgres psql -U sagebase_user -d sagebase_db
```

### Backup and Restore

#### Using Unified CLI (with GCS support)

```bash
# Backup to local and GCS
just exec uv run sagebase database backup

# Backup to local only
just exec uv run sagebase database backup --no-gcs

# Restore from local file
just exec uv run sagebase database restore backup.sql

# Restore from GCS
just exec uv run sagebase database restore gs://bucket/backup.sql

# List all backups
just exec uv run sagebase database list

# List local backups only
just exec uv run sagebase database list --no-gcs
```

#### Using Legacy Scripts (local only)

```bash
# Backup
./backup-database.sh backup

# Restore
./backup-database.sh restore database/backups/[filename]
```

### Database Reset

```bash
# Reset database (drops and recreates with all migrations)
./reset-database.sh
```

### Manual Migration Application

```bash
# Apply specific migration manually
cat database/migrations/016_new_migration.sql | \
    docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml \
    exec -T postgres psql -U sagebase_user -d sagebase_db
```

### Database Inspection

```bash
# List all tables
just db
# Then in psql:
\dt

# Describe table
\d table_name

# Describe table with details
\d+ table_name

# List indexes
\di

# List indexes for table
\di table_name*

# Show table size
SELECT pg_size_pretty(pg_total_relation_size('table_name'));

# Show all table sizes
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 6. Just Commands (Complete List)

```bash
# Container management
just up              # Start containers and launch Streamlit
just down            # Stop and remove containers
just restart         # Restart containers

# Database
just db              # Connect to database
just reset-db        # Reset database

# Application
just up       # Launch Streamlit UI
just monitoring      # Launch monitoring dashboard
just process-minutes # Process meeting minutes

# Testing
just test            # Run tests with pyright
just pytest          # Run pytest only
just coverage        # Run tests with coverage

# Code quality
just format          # Format code with ruff
just lint            # Lint and auto-fix code
just typecheck       # Run pyright (local only)

# Development
just logs            # View container logs
just ports           # Show port configuration
just exec <command>  # Execute command in container
just help            # Show CLI help

# List all commands
just --list
```

## 7. Common Workflows

### Development Workflow

```bash
# 1. Start environment
just up

# 2. Make code changes
# ... edit files ...

# 3. Format and lint
just format
just lint

# 4. Type check (local)
uv run --frozen pyright

# 5. Run tests
just test

# 6. Commit changes (pre-commit runs automatically)
git add .
git commit -m "Your message"
```

### Processing Pipeline Workflow

```bash
# 1. Scrape meeting minutes from web
just exec uv run sagebase scrape-minutes "URL" --upload-to-gcs

# 2. Process minutes (extract speeches)
just exec uv run sagebase process-minutes --meeting-id 123

# 3. Extract speakers
just exec uv run sagebase extract-speakers

# 4. Match speakers with politicians
just exec uv run sagebase update-speakers --use-llm

# 5. View results in Streamlit
just up
```

### Conference Member Extraction Workflow

```bash
# 1. Extract members
just exec uv run sagebase extract-conference-members --conference-id 185

# 2. Review extraction (optional - via Streamlit)
just up

# 3. Match with politicians
just exec uv run sagebase match-conference-members --conference-id 185

# 4. Review matches (optional)
just exec uv run sagebase member-status --conference-id 185

# 5. Create affiliations (only for matched records)
just exec uv run sagebase create-affiliations --conference-id 185
```

### Database Migration Workflow

```bash
# 1. Create migration file
# Edit: database/migrations/016_new_feature.sql

# 2. Add to run script (MANDATORY!)
# Edit: database/02_run_migrations.sql

# 3. Test migration
./reset-database.sh

# 4. Verify migration applied
just db
# Then: \d table_name

# 5. Commit migration files
git add database/migrations/016_new_feature.sql
git add database/02_run_migrations.sql
git commit -m "Add migration for new feature"
```

## 8. Troubleshooting

### Docker Issues

```bash
# Containers won't start
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml down
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml up -d --force-recreate

# Check container status
docker ps -a

# View container logs
just logs

# Check disk space
docker system df

# Clean up unused containers/images
docker system prune
```

### Port Conflicts

```bash
# Check what's using a port
lsof -i :8501

# Show current port configuration
just ports
cat docker/docker-compose.override.yml

# Kill process on port
kill -9 $(lsof -t -i:8501)
```

### Database Connection Issues

```bash
# Test database connection
just exec uv run python -c "from src.config.database import test_connection; test_connection()"

# Check PostgreSQL is running
docker ps | grep postgres

# View PostgreSQL logs
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml logs postgres

# Restart PostgreSQL
just restart
```

### Test Failures

```bash
# Run single failing test for debugging
just exec uv run pytest tests/path/to/test.py::test_name -vv

# Run with debug output
just exec uv run pytest tests/path/to/test.py -vv --tb=long

# Check for import errors
just exec uv run python -c "import src.domain.entities.politician"
```

### Pre-commit Hook Issues

```bash
# Update pre-commit hooks
just exec uv run pre-commit autoupdate

# Clear pre-commit cache
just exec uv run pre-commit clean

# Reinstall hooks
just exec uv run pre-commit uninstall
just exec uv run pre-commit install
```

## 9. Environment Variables

Key environment variables in `.env`:

```bash
# Required
GOOGLE_API_KEY=your-gemini-api-key

# Database (auto-configured in Docker)
DATABASE_URL=postgresql://sagebase_user:sagebase_password@localhost:5432/sagebase_db

# Optional: Google Cloud Storage
GCS_BUCKET_NAME=your-bucket-name
GCS_UPLOAD_ENABLED=true

# Optional: Development
DEBUG=false
LOG_LEVEL=INFO
```

## 10. Quick Reference: Most Used Commands

```bash
# Start working
just up

# Run application
just up

# Process minutes
just exec uv run sagebase process-minutes

# Code quality check
just format && just lint && uv run pyright

# Run tests
just test

# Database operations
just db                  # Connect
./reset-database.sh      # Reset

# Stop working
just down
```

# Sagebase Command Examples

Real-world workflow examples for common Sagebase operations.

## Example 1: First Time Setup

```bash
# 1. Clone repository (if not already done)
git clone <repository-url>
cd sagebase

# 2. Copy and configure environment
cp .env.example .env
# Edit .env and set GOOGLE_API_KEY

# 3. Start Docker containers
just up

# 4. Install local dependencies (optional, for IDE support)
uv sync

# 5. Verify setup
just exec uv run python -c "from src.config.database import test_connection; test_connection()"

# 6. Run tests to ensure everything works
just test

# 7. Launch Streamlit UI
just up
# Access at http://localhost:<port> (check with `just ports`)
```

## Example 2: Daily Development Workflow

```bash
# Morning: Start environment
just up

# Pull latest changes
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Make code changes
# ... edit files ...

# Format and lint code
just format
just lint

# Run type checking (local)
uv run --frozen pyright

# Run tests
just test

# Commit changes (pre-commit runs automatically)
git add .
git commit -m "feat: Add new feature"

# Push changes
git push origin feature/new-feature

# Evening: Stop containers
just down
```

## Example 3: Processing Meeting Minutes End-to-End

### Scenario: Process a new meeting from PDF

```bash
# 1. Start environment
just up

# 2. Add meeting via Streamlit UI
just up
# Navigate to "会議管理" and add meeting record with PDF path

# 3. Process the PDF minutes (extract speeches)
just exec uv run sagebase process-minutes --meeting-id 123

# Expected output:
# - Conversations extracted and saved to database
# - Processing status updated in meetings table

# 4. Extract speaker information
just exec uv run sagebase extract-speakers

# Expected output:
# - Speaker records created from conversations
# - Speaker names normalized

# 5. Match speakers with politicians using LLM
just exec uv run sagebase update-speakers --use-llm

# Expected output:
# - Speakers linked to politicians table
# - Confidence scores calculated

# 6. View results in Streamlit
just up
# Navigate to "発言者管理" to see matched speakers

# 7. (Optional) Export or analyze data
just db
# Run SQL queries to analyze the data
```

### Scenario: Scrape and process minutes from web

```bash
# 1. Scrape minutes from web and upload to GCS
just exec uv run sagebase scrape-minutes "https://example.com/minutes" --upload-to-gcs

# Expected output:
# - PDF downloaded and uploaded to GCS
# - GCS URI saved to meetings table
# - Meeting record created

# 2. Process from GCS (using meeting ID from step 1)
just exec uv run sagebase process-minutes --meeting-id 124

# 3-6. Same as above (extract speakers, match, view)
```

### Scenario: Batch scrape multiple minutes

```bash
# Batch scrape from kaigiroku.net
just exec uv run sagebase batch-scrape --tenant kyoto --upload-to-gcs

# Expected output:
# - Multiple meetings scraped
# - All uploaded to GCS
# - Meeting records created for each

# Process all new meetings
for meeting_id in $(seq 100 110); do
    just exec uv run sagebase process-minutes --meeting-id $meeting_id
done

# Extract speakers for all
just exec uv run sagebase extract-speakers

# Match all speakers
just exec uv run sagebase update-speakers --use-llm
```

## Example 4: Conference Member Management

### Scenario: Extract and match conference members

```bash
# 1. Add conference members URL via Streamlit
just up
# Navigate to "議会管理"
# Edit conference and set members_introduction_url

# 2. Extract members from URL
just exec uv run sagebase extract-conference-members --conference-id 185

# Expected output:
# - Members extracted to staging table
# - Status: 'pending'

# 3. Review extraction (optional)
just up
# Navigate to "議会委員抽出" to review extracted data

# 4. Match with existing politicians
just exec uv run sagebase match-conference-members --conference-id 185

# Expected output:
# - Fuzzy matching performed
# - Status updated: 'matched', 'needs_review', or 'no_match'
# - Confidence scores calculated

# 5. Check matching status
just exec uv run sagebase member-status --conference-id 185

# Sample output:
# Conference 185: 京都府議会
# Total: 60
# Matched: 55 (91.7%)
# Needs Review: 3 (5.0%)
# No Match: 2 (3.3%)

# 6. Review matches needing manual review (optional)
just up
# Navigate to "議会委員抽出" and filter by "needs_review"

# 7. Create affiliations (only for matched records)
just exec uv run sagebase create-affiliations --conference-id 185

# Expected output:
# - Politician affiliations created
# - Roles assigned
# - Affiliation dates set

# 8. Verify in database
just db
# Query:
SELECT p.name, pa.role, pa.start_date
FROM politician_affiliations pa
JOIN politicians p ON pa.politician_id = p.id
WHERE pa.conference_id = 185
ORDER BY p.name;
```

## Example 5: Politician Scraping Workflow

### Scenario: Scrape all party members

```bash
# 1. Configure party URLs via Streamlit
just up
# Navigate to "政党管理"
# For each party, set members_list_url field

# 2. Scrape all parties (dry run first to preview)
just exec uv run sagebase scrape-politicians --all-parties --dry-run

# Expected output:
# - Shows politicians that would be created/updated
# - No database changes

# 3. Actually scrape and save
just exec uv run sagebase scrape-politicians --all-parties

# Expected output:
# - Politicians created or updated
# - Duplicates avoided (checks by name + party)

# 4. Scrape specific party with hierarchical mode
just exec uv run sagebase scrape-politicians --party-id 5 --hierarchical --max-depth 3

# Expected output:
# - Follows links recursively up to depth 3
# - More comprehensive member discovery

# 5. View results
just up
# Navigate to "政治家管理" to see new politicians
```

## Example 6: Database Management

### Scenario: Backup before major operation

```bash
# 1. Create backup before risky operation
just exec uv run sagebase database backup

# Expected output:
# - Backup saved to database/backups/
# - Also uploaded to GCS (if configured)
# - Filename includes timestamp

# 2. Perform risky operation
just exec uv run sagebase process-minutes --meeting-id 999

# 3. If something went wrong, restore
just exec uv run sagebase database restore database/backups/backup_2025-01-30_120000.sql

# Or restore from GCS
just exec uv run sagebase database restore gs://bucket/backups/backup_2025-01-30_120000.sql
```

### Scenario: Database migration

```bash
# 1. Check latest migration number
ls database/migrations/ | tail -5

# Expected output:
# 013_create_llm_processing_history.sql
# 014_add_...
# 015_...

# 2. Create new migration (016)
# Edit: database/migrations/016_add_email_to_politicians.sql

# 3. CRITICAL: Add to run script
# Edit: database/02_run_migrations.sql
# Add line: \i /docker-entrypoint-initdb.d/migrations/016_add_email_to_politicians.sql

# 4. Test migration
./reset-database.sh

# Expected output:
# - All migrations run successfully
# - Database recreated

# 5. Verify migration applied
just db
\d politicians
# Should show new email column

# 6. Commit migration
git add database/migrations/016_add_email_to_politicians.sql
git add database/02_run_migrations.sql
git commit -m "migration: Add email column to politicians"
```

## Example 7: Testing Workflow

### Scenario: Test-driven development

```bash
# 1. Write failing test first
# Edit: tests/unit/domain/test_new_feature.py

def test_new_feature_works():
    service = NewFeatureService()
    result = service.process("input")
    assert result == "expected"

# 2. Run test (should fail)
just exec uv run pytest tests/unit/domain/test_new_feature.py -v

# Expected output:
# FAILED - NameError: NewFeatureService not defined

# 3. Implement feature
# Edit: src/domain/services/new_feature_service.py

# 4. Run test again (should pass)
just exec uv run pytest tests/unit/domain/test_new_feature.py -v

# Expected output:
# PASSED

# 5. Run all tests
just test

# 6. Check coverage
just exec uv run pytest --cov=src/domain/services --cov-report=term

# 7. Format and lint
just format
just lint

# 8. Type check
uv run --frozen pyright src/domain/services/new_feature_service.py

# 9. Commit
git add tests/unit/domain/test_new_feature.py
git add src/domain/services/new_feature_service.py
git commit -m "feat: Add new feature service with tests"
```

### Scenario: Debugging failing test

```bash
# 1. Identify failing test
just test

# Expected output shows failure:
# FAILED tests/unit/application/test_usecase.py::test_execute

# 2. Run single test with verbose output
just exec uv run pytest tests/unit/application/test_usecase.py::test_execute -vv --tb=long

# 3. Add debug breakpoint in code
# Edit test or source file:
import pdb; pdb.set_trace()

# 4. Run with pdb
just exec uv run pytest tests/unit/application/test_usecase.py::test_execute -s

# 5. Debug interactively
# (pdb) print(variable)
# (pdb) step
# (pdb) continue

# 6. Fix the issue
# Edit source file

# 7. Remove breakpoint and verify fix
just exec uv run pytest tests/unit/application/test_usecase.py::test_execute -v

# Expected output:
# PASSED
```

## Example 8: Code Quality Workflow

### Scenario: Pre-commit hook failure

```bash
# 1. Make changes
# Edit: src/domain/entities/politician.py

# 2. Try to commit
git add .
git commit -m "Update politician entity"

# Expected output:
# ruff....................................................Failed
# - hook id: ruff
# - exit code: 1
#
# src/domain/entities/politician.py:10:1: F401 [*] `datetime` imported but unused

# 3. Fix the issue
just format
just lint

# Or manually:
just exec uv run ruff check . --fix

# 4. Try commit again
git add .
git commit -m "Update politician entity"

# Expected output:
# All hooks passed successfully!
```

### Scenario: Type checking errors

```bash
# 1. Run type checker
uv run --frozen pyright

# Expected output shows errors:
# src/domain/services/speaker_service.py:45:12 - error: Argument of type "str | None" cannot be assigned to parameter "name" of type "str"

# 2. Fix type errors
# Edit: src/domain/services/speaker_service.py
# Add None check:
if name is None:
    raise ValueError("Name cannot be None")

# 3. Run type checker again
uv run --frozen pyright

# Expected output:
# 0 errors, 0 warnings, 0 informations
```

## Example 9: Monitoring and Analysis

### Scenario: Monitor data coverage

```bash
# 1. Check current coverage
just exec uv run sagebase coverage

# Expected output:
# === Coverage Statistics ===
#
# Prefectures: 47 total
#   With conferences: 45 (95.7%)
#   Without conferences: 2 (4.3%)
#
# Municipalities: 1,966 total
#   With conferences: 150 (7.6%)
#   Without conferences: 1,816 (92.4%)

# 2. Launch monitoring dashboard
just monitoring

# View in browser at http://localhost:<port>

# 3. Analyze specific region in database
just db

SELECT
    gb.name,
    COUNT(DISTINCT c.id) as conference_count,
    COUNT(DISTINCT m.id) as meeting_count,
    COUNT(DISTINCT conv.id) as conversation_count
FROM governing_bodies gb
LEFT JOIN conferences c ON c.governing_body_id = gb.id
LEFT JOIN meetings m ON m.conference_id = c.id
LEFT JOIN conversations conv ON conv.meeting_id = m.id
WHERE gb.organization_type = '都道府県'
GROUP BY gb.name
ORDER BY conference_count DESC;
```

## Example 10: Troubleshooting Common Issues

### Issue: Port conflict

```bash
# Symptom: just up fails with port already in use

# 1. Check what's using the port
lsof -i :8501

# 2. Kill the process
kill -9 $(lsof -t -i:8501)

# 3. Or stop all containers and restart
just down
just up
```

### Issue: Database connection failed

```bash
# Symptom: Tests fail with connection errors

# 1. Check PostgreSQL is running
docker ps | grep postgres

# 2. If not running, start it
just up

# 3. Test connection
just exec uv run python -c "from src.config.database import test_connection; test_connection()"

# 4. Check logs if still failing
docker compose -f docker/docker-compose.yml -f docker/docker-compose.override.yml logs postgres

# 5. Restart PostgreSQL
just restart
```

### Issue: Migration not applied

```bash
# Symptom: Table doesn't exist but migration file created

# 1. Check if migration is in run script
grep "016_" database/02_run_migrations.sql

# 2. If not found, add it
# Edit: database/02_run_migrations.sql

# 3. Reset database
./reset-database.sh

# 4. Verify table exists
just db
\dt
```

### Issue: Tests pass locally but fail in CI

```bash
# Common cause: Real API calls instead of mocks

# 1. Check test file for API calls
grep -r "GOOGLE_API_KEY" tests/

# 2. Replace with mocks
# Edit test file to use AsyncMock

# 3. Run tests locally
just test

# 4. Push changes
git push
```

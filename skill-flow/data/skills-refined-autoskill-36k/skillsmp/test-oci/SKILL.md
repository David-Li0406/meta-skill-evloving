---
name: test-oci
description: Run the TMI comprehensive test suite against Oracle ADB (OCI) including unit tests, integration tests, API tests, and CATS security fuzzing. Use when asked to run tests against Oracle database.
allowed-tools: Bash, Read
---

# Comprehensive Test Suite Skill (Oracle ADB)

You are executing the TMI comprehensive test suite against Oracle Autonomous Database (OCI). This skill runs all test levels in sequence, stopping at the first failure to allow investigation.

## Prerequisites

Before running this skill, ensure:
1. Oracle Instant Client is installed
2. Wallet is extracted to `./wallet` directory
3. `scripts/oci-env.sh` exists with your OCI credentials (copy from `scripts/oci-env.sh.example`)

## Test Execution Order

The test suite runs in the following order, with each stage only running if the previous stage passed:

1. **Environment Setup** - Clean and rebuild the server with Oracle support
2. **Unit Tests** - Fast tests with no external dependencies (~5-10 seconds)
3. **Integration Tests (OCI)** - Full Oracle ADB integration tests (~30-60 seconds)
4. **API Tests** - Postman/Newman API test suite (~2 minutes)
5. **CATS Fuzzing (OCI)** - Security fuzzing with CATS (~9 minutes)

## Execution Instructions

### Step 0: Environment Setup

First, stop any running server and clean up, then rebuild with Oracle support and start fresh:

```bash
make stop-server
make clean-everything
```

Build the server with Oracle support:
```bash
. scripts/oci-env.sh && go build -tags oracle -o bin/tmiserver ./cmd/server/
```

Start the development environment with OCI:
```bash
make start-dev-oci
```

Wait for the server to be fully ready before proceeding. You can verify with:
```bash
curl -s http://localhost:8080/ > /dev/null && echo "Server ready"
```

### Step 1: Unit Tests

Run unit tests (these don't use the database):
```bash
make test-unit
```

**Analysis**:
- Look for `PASS` or `FAIL` in the output
- Check the final line for `ok` (pass) or `FAIL` (failure)
- If any test fails, report the failing test name(s) and error message(s)
- **Stop here if any unit tests fail**

### Step 2: Integration Tests (OCI)

If unit tests passed, run integration tests against Oracle ADB:
```bash
make test-integration-oci
```

**Analysis**:
- Look for `PASS` or `FAIL` in the output
- Check for Oracle database connection errors
- If any test fails, report the failing test name(s) and error message(s)
- **Stop here if any integration tests fail**

### Step 3: API Tests

If integration tests passed, run API tests. The server should already be running from Step 0:
```bash
make test-api
```

**Analysis**:
- Look for Newman test results summary
- Check for `assertions` passed/failed counts
- Look for `iterations` and `requests` counts
- If any assertions fail, report the failing endpoint(s) and assertion(s)
- **Stop here if any API tests fail**

### Step 4: CATS Fuzzing (OCI)

If API tests passed, run CATS security fuzzing against the OCI-backed server:
```bash
make cats-fuzz-oci
```

This takes approximately 9 minutes. The output will show progress through various fuzzers.

### Step 5: Parse and Analyze CATS Results

After CATS completes, parse the results:
```bash
make parse-cats-results
```

Then analyze the database. Run these queries to understand the results:

```bash
# Summary statistics (excluding OAuth false positives)
sqlite3 test/outputs/cats/cats-results.db <<'SQL'
.mode column
.headers on
SELECT
    rt.name AS result,
    COUNT(*) AS count,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM tests t
JOIN result_types rt ON t.result_type_id = rt.id
WHERE t.is_oauth_false_positive = 0
GROUP BY rt.name
ORDER BY count DESC;
SQL

# Count OAuth false positives (expected, not real issues)
sqlite3 test/outputs/cats/cats-results.db "SELECT COUNT(*) as oauth_false_positives FROM tests WHERE is_oauth_false_positive = 1;"

# Actual errors by path (top 10)
sqlite3 test/outputs/cats/cats-results.db <<'SQL'
.mode column
.headers on
SELECT
    p.path,
    COUNT(*) AS error_count,
    GROUP_CONCAT(DISTINCT f.name) AS fuzzers
FROM tests t
JOIN result_types rt ON t.result_type_id = rt.id
JOIN paths p ON t.path_id = p.id
JOIN fuzzers f ON t.fuzzer_id = f.id
WHERE rt.name = 'error' AND t.is_oauth_false_positive = 0
GROUP BY p.path
ORDER BY error_count DESC
LIMIT 10;
SQL

# Warnings by path (top 10)
sqlite3 test/outputs/cats/cats-results.db <<'SQL'
.mode column
.headers on
SELECT
    p.path,
    COUNT(*) AS warn_count
FROM tests t
JOIN result_types rt ON t.result_type_id = rt.id
JOIN paths p ON t.path_id = p.id
WHERE rt.name = 'warn' AND t.is_oauth_false_positive = 0
GROUP BY p.path
ORDER BY warn_count DESC
LIMIT 10;
SQL
```

**Analysis**:
- **OAuth false positives** are expected (401/403 responses from auth tests) - these are NOT real issues
- Focus on the **error** and **warn** results where `is_oauth_false_positive = 0`
- Report any actual errors by path and fuzzer
- Warnings are less critical but should be noted

## Reporting Guidelines

### On Success
If all tests pass, report:
- Unit tests: X tests passed
- Integration tests (OCI): X tests passed
- API tests: X assertions passed
- CATS fuzzing (OCI): X tests run, Y errors (Z oauth false positives excluded)

### On Failure
If any stage fails:
1. Clearly state which stage failed (unit/integration/API/CATS)
2. List the specific failing tests or endpoints
3. Include relevant error messages
4. Stop execution - do not proceed to later stages
5. Suggest next steps for investigation

## Important Notes

- **Oracle Support**: The server must be built with `-tags oracle` for OCI support. The `make start-dev-oci` target handles this automatically.
- **CATS Seeding Tool**: The CATS seeding tool (`bin/cats-seed`) must also be built with Oracle support. Use `make build-cats-seed-oci` or let `make cats-seed-oci` (called by `make cats-fuzz-oci`) build it automatically.
- **OAuth false positives**: CATS will flag 401/403 responses as "errors" but these are expected for auth testing. The `is_oauth_false_positive` flag identifies these.
- **CATS duration**: The fuzzing stage takes ~9 minutes - this is normal
- **Server must be running**: All tests except unit tests require the dev server (`make start-dev-oci`)
- **Redis required**: API and CATS tests require Redis (`make start-redis` - started automatically by `start-dev-oci`)
- **No server restart during tests**: The API tests and CATS fuzzing run against the already-running server; they do not restart it

## Database Schema Reference

The CATS results database has these key tables:
- `tests` - Individual test results with `is_oauth_false_positive` flag
- `result_types` - Result categories: `success`, `warn`, `error`, `skip`
- `paths` - API endpoints tested
- `fuzzers` - CATS fuzzer names
- `test_results_view` - Convenient view joining all tables
- `test_results_filtered_view` - View excluding OAuth false positives

## Troubleshooting

### Oracle Connection Issues
If you see Oracle connection errors:
1. Verify `scripts/oci-env.sh` has correct credentials
2. Check wallet is extracted to `./wallet`
3. Verify `DYLD_LIBRARY_PATH` points to Oracle Instant Client
4. Check `TNS_ADMIN` points to the wallet directory

### Server Fails to Start
Check the logs:
```bash
tail -50 logs/tmi.log
```

Common issues:
- Missing Oracle environment variables
- Wallet not found
- Database user not created in OCI ADB

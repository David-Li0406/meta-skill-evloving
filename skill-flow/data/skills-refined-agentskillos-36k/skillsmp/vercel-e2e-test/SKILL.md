---
name: vercel-e2e-test
description: Deploy to Vercel preview and run Playwright E2E tests against staging database. Use when user says "vercel e2e test", "test on vercel", "deploy and test", "e2e on staging", or "preview deploy test".
allowed-tools: Bash, Read, AskUserQuestion, TodoWrite
version: 1.11.0
---

# Vercel E2E Test

> Deploy to Vercel preview and run Playwright E2E tests against staging Supabase.

<when_to_use>

## When to Use

Invoke when user says:

- "vercel e2e test"
- "test on vercel"
- "deploy and test"
- "e2e on staging"
- "preview deploy test"

**Optional argument**: Specific test file pattern (e.g., `vercel e2e test session-creation`)

</when_to_use>

<workflow>

## Workflow Overview

| Phase | Action                   | Duration      |
| ----- | ------------------------ | ------------- |
| 0     | **Prerequisite checks**  | 5-10s         |
| 1     | Deploy to Vercel preview | 60-120s       |
| 2     | Extract preview URL      | 2s            |
| 3     | Start local worker       | 20-30s        |
| 4     | Start edge functions     | 10-20s        |
| 5     | Run Playwright tests     | 2-10min       |
| 6     | Stop worker & functions  | 2s            |
| 7     | Report results           | 5s            |
| 8     | Offer next steps         | User decision |

**CRITICAL**: Phase 0 must pass before proceeding. Fail fast, don't waste 30 minutes to discover missing config.

Track progress with TodoWrite.

</workflow>

<execution>

## Execution Details

### Phase 0: Prerequisite Checks (REQUIRED)

**Run ALL checks before proceeding. STOP immediately if any fail.**

#### Check 1: Environment Files Exist

```bash
# Verify .env.e2e exists (staging database config)
test -f .env.e2e && echo "✓ .env.e2e exists" || echo "✗ MISSING: .env.e2e"

# Verify supabase/.env.local exists (edge function secrets)
test -f supabase/.env.local && echo "✓ supabase/.env.local exists" || echo "✗ MISSING: supabase/.env.local"
```

#### Check 2: Required Environment Variables

```bash
# Check .env.e2e has staging Supabase config
grep -q "VITE_SUPABASE_URL=https://vsrlvwhnchughfcbilqn" .env.e2e && echo "✓ Staging URL configured" || echo "✗ MISSING: VITE_SUPABASE_URL in .env.e2e"
grep -q "SUPABASE_SERVICE_ROLE_KEY" .env.e2e && echo "✓ Service role key present" || echo "✗ MISSING: SUPABASE_SERVICE_ROLE_KEY in .env.e2e"

# Check supabase/.env.local has AI key for edge functions
grep -q "ANTHROPIC_API_KEY" supabase/.env.local && echo "✓ Anthropic API key present" || echo "✗ MISSING: ANTHROPIC_API_KEY in supabase/.env.local"
```

#### Check 3: Docker Running (Required for Edge Functions)

```bash
docker info > /dev/null 2>&1 && echo "✓ Docker is running" || echo "✗ FAILED: Docker is not running - start Docker Desktop"
```

#### Check 4: Ports Available

```bash
# Check port 3001 (worker) is free
curl -s http://localhost:3001/health > /dev/null 2>&1 && echo "⚠ Port 3001 in use (worker may already be running)" || echo "✓ Port 3001 available"

# Check port 54321 (edge functions) is free
curl -s http://localhost:54321/functions/v1/ > /dev/null 2>&1 && echo "⚠ Port 54321 in use (edge functions may already be running)" || echo "✓ Port 54321 available"
```

#### Check 5: Vercel CLI Authenticated

```bash
npx vercel whoami > /dev/null 2>&1 && echo "✓ Vercel CLI authenticated" || echo "✗ FAILED: Run 'npx vercel login' first"
```

#### Gate Decision

| Check                      | Required | If Failed                            |
| -------------------------- | -------- | ------------------------------------ |
| .env.e2e exists            | Yes      | STOP - Create from .env.e2e.example  |
| supabase/.env.local exists | Yes      | STOP - Create with ANTHROPIC_API_KEY |
| Staging URL in .env.e2e    | Yes      | STOP - Add VITE_SUPABASE_URL         |
| Service role key           | Yes      | STOP - Add SUPABASE_SERVICE_ROLE_KEY |
| Anthropic API key          | Yes      | STOP - Add to supabase/.env.local    |
| Docker running             | Yes      | STOP - Start Docker Desktop          |
| Port 3001 free             | No       | OK if worker already running         |
| Port 54321 free            | No       | OK if edge functions already running |
| Vercel authenticated       | Yes      | STOP - Run `npx vercel login`        |

**Only proceed to Phase 1 if all required checks pass.**

### Phase 1: Deploy to Vercel Preview

Run the deployment command:

```powershell
npx vercel
```

Parse output to find preview URL. Vercel output includes:

```
Preview: https://project-xxx.vercel.app
```

If deployment fails:

- Check for "error" in output
- Common issues: not logged in, build failed, missing env vars
- STOP and report error to user

### Phase 2: Extract Preview URL

Capture URL from deployment output using pattern: `Preview: (https://[^\s]+)`

Store URL for test execution.

### Phase 3: Start Local Worker

Start a local worker against staging Supabase so worker-dependent tests can run.

**CRITICAL**: Use `--env-file=.env.e2e` to load staging credentials. The worker will connect to whichever database is specified in its environment.

```bash
# Build worker
npm run worker:build

# Start worker with staging env and capture ALL output (stdout + stderr)
node --env-file=.env.e2e dist/worker.mjs 2>&1
```

**Important**: Run in background and capture output to a file:

```bash
node --env-file=.env.e2e dist/worker.mjs 2>&1
```

Wait for health check at `http://localhost:3001/health` (max 30 seconds).

**Verify worker connection**: Check worker logs for:

- `Starting automation worker...`
- `Connecting to Supabase` with `supabaseUrl: "https://vsrlvwhnchughfcbilqn.supabase.co"`
- `Supabase connectivity verified` (confirms database connection)
- `Worker started successfully`
- `Started polling`

If connectivity check fails, worker will retry 5 times with exponential backoff before failing.

If worker fails to start:

- Check `.env.e2e` has `SUPABASE_SERVICE_ROLE_KEY`
- Check port 3001 is available (`curl http://localhost:3001/health`)
- Check worker build is up to date
- Verify logs show staging URL (`vsrlvwhnchughfcbilqn.supabase.co`)
- Check for "Cannot connect to Supabase" error (network/DNS issue)

### Phase 4: Start Edge Functions

Start Supabase edge functions locally so `@needs-edge-functions` tests can run.

**Prerequisites**: Ensure `supabase/.env.local` contains:

- `ANTHROPIC_API_KEY` - Required for AI chat functions
- `SUPABASE_SERVICE_ROLE_KEY` - For database access

```bash
# Start edge functions in background
npx supabase functions serve --env-file supabase/.env.local
```

**Important**: Run in background with `run_in_background: true`.

Wait for functions to be ready by checking health (max 30 seconds):

```bash
curl -s http://localhost:54321/functions/v1/ai-chat -X OPTIONS
```

A 200 response indicates functions are ready.

If edge functions fail to start:

- Check Docker is running (required for Supabase CLI)
- Verify `supabase/.env.local` exists with required keys
- Check port 54321 is available
- Run `npx supabase start` if local Supabase isn't running

### Phase 5: Run Playwright Tests

Run tests and wait for completion:

```bash
# Run all chromium projects with retries for flaky test resilience
# Use cross-env for cross-platform compatibility (Windows + Unix)
npx cross-env PLAYWRIGHT_BASE_URL="<preview-url>" npx playwright test --project=chromium --project=chromium-clean --project=chromium-admin --project=chromium-with-worker --project=chromium-with-edge-functions --retries=2
```

User can watch progress directly in the terminal output.

**Test projects available** (all 5 run by default):

| Project                        | Description                        | When to Use         |
| ------------------------------ | ---------------------------------- | ------------------- |
| `chromium`                     | Main test suite                    | Default             |
| `chromium-clean`               | Login/onboarding tests             | Fresh browser       |
| `chromium-admin`               | Admin panel tests                  | Admin features      |
| `chromium-with-worker`         | Tests tagged @needs-worker         | Worker-dependent    |
| `chromium-with-edge-functions` | Tests tagged @needs-edge-functions | Edge function tests |

All projects work because local worker and edge functions are running.

### Phase 6: Stop Worker & Edge Functions

After tests complete (pass or fail), stop the local worker and edge functions.

**If started with `run_in_background: true`**: Use the `KillShell` tool with the task IDs returned when processes were started.

**Alternative** - kill by port (cross-platform):

```bash
# Stop worker
npx kill-port 3001

# Stop edge functions
npx kill-port 54321
```

### Phase 7: Report Results

Parse test output for:

- Total tests run
- Passed / Failed / Skipped counts
- Failed test names (if any)

Display summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vercel E2E Test Results
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Preview URL: https://...vercel.app
Tests: 42 passed, 0 failed, 0 skipped

Status: PASS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Phase 8: Next Steps

Use AskUserQuestion to offer options:

- View Playwright report (`npx playwright show-report`)
- Diagnose failures (invoke test-or-bug skill)
- Run additional test projects
- Done

</execution>

<environment>

## Environment Configuration

**Vercel Preview uses staging Supabase** (`vsrlvwhnchughfcbilqn`).

| Config           | Source                   | Database |
| ---------------- | ------------------------ | -------- |
| Vercel Preview   | Vercel env vars          | Staging  |
| Playwright local | `.env.e2e` (auto-loaded) | Staging  |

The playwright.config.ts auto-detects external URLs:

```typescript
const isExternalUrl = process.env.PLAYWRIGHT_BASE_URL?.startsWith("https://");
config({ path: isExternalUrl ? ".env.e2e" : ".env.local" });
```

**NEVER run tests against production** (`www.eoscrm.org`).

**Playwright Workers**: 4 locally (configurable), 2 in CI

Since frontend runs on Vercel and tests run locally, you can increase workers:

- Default: 4 workers
- Increase: `npx playwright test --workers=8`
- Maximum practical: ~CPU cores

</environment>

<staging_maintenance>

## Staging Maintenance

Keep staging Supabase in sync with production schema.

### When Migrations Change

After adding new migrations to the codebase:

```powershell
# Link to staging (if not already linked)
npx supabase link --project-ref vsrlvwhnchughfcbilqn

# Push migrations
npx supabase db push
```

### When Seed Data Changes

If `supabase/seed.sql` is updated:

```bash
npx cross-env PGPASSWORD='<staging-password>' psql -h aws-0-us-west-2.pooler.supabase.com -p 5432 -d postgres -U postgres.vsrlvwhnchughfcbilqn -f supabase/seed.sql
```

Use pooler connection for reliability.

### Vercel Env Var Updates

```powershell
# Remove existing Preview value
npx vercel env rm VITE_SUPABASE_URL preview

# Add new value for Preview only
echo "<new-value>" | npx vercel env add VITE_SUPABASE_URL preview
```

</staging_maintenance>

<troubleshooting>

## Troubleshooting

| Issue                        | Cause                                        | Fix                                                       |
| ---------------------------- | -------------------------------------------- | --------------------------------------------------------- |
| "Failed to fetch" in tests   | Staging Supabase down or wrong env           | Check `.env.e2e` points to staging                        |
| "Seed user not found"        | Staging missing seed data                    | Re-run `supabase/seed.sql` on staging                     |
| Deployment fails             | Not logged in / build error                  | Run `npx vercel login`, fix build                         |
| Test timeout                 | Vercel cold start                            | Increase timeout or retry                                 |
| Auth tests fail              | Dev login form not showing                   | Verify `VITE_ENABLE_E2E_LOGIN` in Vercel                  |
| Worker health check fails    | Port 3001 in use or build stale              | Kill port 3001, run `npm run worker:build`                |
| Worker tests timeout         | Worker not processing events                 | Check worker logs, verify staging DB                      |
| "Cannot connect to Supabase" | DNS/network issue, wrong URL                 | Check network, verify `.env.e2e` URL, worker will retry   |
| "Invalid JWT" 401            | Supabase ES256 JWT migration (GitHub #41691) | Add `verify_jwt = false` to config.toml, redeploy         |
| Auth cache mismatch          | Local tokens used against staging            | Clear `playwright/.auth/*.json` before running            |
| CORS errors on preview       | Preview URL not in allowlist                 | Update `getCorsHeaders()` to allow `*.vercel.app` pattern |
| Worker events stay pending   | Tests using different DB than worker         | Use `cross-env` for PLAYWRIGHT_BASE_URL (see Phase 5)     |
| Edge function tests fail     | Edge functions not running                   | Run Phase 0 checks, start `supabase functions serve`      |
| Docker not running           | Required for edge functions                  | Start Docker Desktop before running skill                 |
| Missing ANTHROPIC_API_KEY    | Edge functions need AI key                   | Add to `supabase/.env.local`                              |

</troubleshooting>

<approval_gates>

## Approval Gates

| Gate          | Phase | Question                         |
| ------------- | ----- | -------------------------------- |
| Prerequisites | 0     | STOP if any required check fails |
| View Report   | 7     | "Open Playwright report?"        |

</approval_gates>

<safety_rules>

## Safety Rules

1. **NEVER test against production URL** - Only use Vercel preview URLs
2. **Verify URL format** - Must match `*.vercel.app` pattern

</safety_rules>

<quick_reference>

## Quick Reference

```bash
# Phase 0: Prerequisite checks (run ALL before proceeding)
test -f .env.e2e && echo "✓ .env.e2e" || echo "✗ MISSING .env.e2e"
test -f supabase/.env.local && echo "✓ supabase/.env.local" || echo "✗ MISSING supabase/.env.local"
grep -q "SUPABASE_SERVICE_ROLE_KEY" .env.e2e && echo "✓ Service key" || echo "✗ MISSING key"
grep -q "ANTHROPIC_API_KEY" supabase/.env.local && echo "✓ Anthropic key" || echo "✗ MISSING key"
docker info > /dev/null 2>&1 && echo "✓ Docker running" || echo "✗ START DOCKER"
npx vercel whoami > /dev/null 2>&1 && echo "✓ Vercel auth" || echo "✗ RUN: npx vercel login"

# Phase 1: Deploy preview (only if Phase 0 passes)
npx vercel

# Build and start worker against staging (CRITICAL: use --env-file)
npm run worker:build
node --env-file=.env.e2e dist/worker.mjs 2>&1

# Start edge functions (requires Docker running)
npx supabase functions serve --env-file supabase/.env.local

# Run tests against preview (all 5 chromium projects)
# cross-env required for Windows compatibility
npx cross-env PLAYWRIGHT_BASE_URL="<url>" npx playwright test --project=chromium --project=chromium-clean --project=chromium-admin --project=chromium-with-worker --project=chromium-with-edge-functions --retries=2

# Run specific test
npx cross-env PLAYWRIGHT_BASE_URL="<url>" npx playwright test session-creation --retries=2

# Stop worker and edge functions (use KillShell tool with task ID, or kill by port)
npx kill-port 3001 54321

# View report
npx playwright show-report
```

</quick_reference>

<version_history>

## Version History

- **v1.11.0** (2026-01-20): Add prerequisite checks and edge function support
  - **Phase 0: Prerequisite Checks** - Fail fast before expensive operations
    - Check .env.e2e and supabase/.env.local exist
    - Verify required env vars (SUPABASE_SERVICE_ROLE_KEY, ANTHROPIC_API_KEY)
    - Check Docker is running (required for edge functions)
    - Verify Vercel CLI is authenticated
    - Check ports 3001 and 54321 are available
  - **Edge Functions**: Start `supabase functions serve` for `@needs-edge-functions` tests
  - Added troubleshooting for edge function failures
- **v1.10.0** (2026-01-20): Fix cross-platform compatibility
  - Use `cross-env` for PLAYWRIGHT_BASE_URL and PGPASSWORD
  - Previous Unix/PowerShell syntax didn't work across platforms
  - Replace PowerShell `Get-Process | Stop-Process` with `npx kill-port`
  - Note to use `KillShell` tool for background worker processes
  - Added troubleshooting entry for "Worker events stay pending"
- **v1.9.0** (2026-01-20): Add worker connectivity verification
  - Worker now logs Supabase URL at startup for debugging
  - Added connectivity check with 5 retries and exponential backoff
  - Worker fails fast with clear error if cannot reach Supabase
  - Updated troubleshooting for "Cannot connect to Supabase" error
- **v1.8.0** (2026-01-18): Consolidate staging maintenance from pattern file
  - Added staging maintenance section (migrations, seed data, Vercel env vars)
  - Deleted redundant `e2e-vercel-testing-patterns.md`
- **v1.7.0** (2026-01-18): Fix worker database connection
  - Use `node --env-file=.env.e2e` to load staging credentials
  - Previously worker connected to local DB while tests used staging
  - Add `2>&1` to capture all worker output (pino logs go to stdout)
  - Update quick reference with correct bash syntax
- **v1.6.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
- **v1.5.0** (2026-01-17): Remove progress polling to reduce context usage
  - Tests run synchronously; user watches progress in terminal
- **v1.4.0** (2026-01-17): Run all chromium test projects
  - Now runs all 5 chromium projects: chromium, chromium-clean, chromium-admin, chromium-with-worker, chromium-with-edge-functions
  - Increases test coverage from ~280 to 300+ tests
- **v1.3.0** (2026-01-17): Added retries for flaky test resilience
  - Enable `--retries=2` by default to match CI behavior
  - Flaky tests due to Vercel cold starts will pass on retry
- **v1.2.0** (2025-01-17): Added progress updates (removed in v1.5.0)
- **v1.1.0** (2025-01-17): Added local worker mode
  - Skill starts local worker against staging before tests
  - All test projects now supported including `chromium-with-worker`
  - Worker auto-stopped after tests complete
- **v1.0.0** (2025-01-17): Initial release

</version_history>

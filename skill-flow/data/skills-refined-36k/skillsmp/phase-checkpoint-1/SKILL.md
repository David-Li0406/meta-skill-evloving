---
name: phase-checkpoint
description: Run checkpoint criteria after completing a phase
argument-hint: [phase-number]
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion, WebFetch, WebSearch
---

Phase $1 is complete. Read EXECUTION_PLAN.md and run the checkpoint criteria.

## External Tool Documentation Protocol

**CRITICAL:** Before providing verification instructions for external integrations, you MUST read the latest official documentation first.

### When to Fetch Docs

Fetch documentation when ANY of these apply:
- Checkpoint criteria involve verifying external service integration
- Manual verification steps reference third-party dashboards or APIs
- You need to guide users through external service verification (webhooks, API responses, etc.)

### How to Fetch Docs

1. **Identify external services** from checkpoint criteria
2. **Fetch relevant docs** using WebFetch or WebSearch:
   - Focus on testing/verification sections
   - Look for troubleshooting guides for common issues
3. **Cache per session** — Don't re-fetch docs already fetched in this session
4. **Handle failures gracefully:**
   - Retry with exponential backoff (2-3 attempts)
   - If all retries fail: warn user and proceed with best available info

### Documentation URLs by Service

| Service | Verification/Testing Doc |
|---------|-------------------------|
| Supabase | https://supabase.com/docs/guides/getting-started |
| Firebase | https://firebase.google.com/docs/web/setup |
| Stripe | https://stripe.com/docs/testing |
| Auth0 | https://auth0.com/docs/troubleshoot |
| Vercel | https://vercel.com/docs/deployments/overview |
| Resend | https://resend.com/docs/dashboard/emails/logs |

For services not listed, use WebSearch: `{service name} testing verification documentation`

### Integration with Verification

When guiding manual verification of external integrations:
1. Fetch docs FIRST to understand current testing procedures
2. Provide accurate dashboard navigation (UI may have changed)
3. Include expected responses/behaviors from official docs
4. Reference troubleshooting steps for common failures

## Context Detection

Determine working context:

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Directory Guard (Wrong Directory Check)

Before starting, confirm `EXECUTION_PLAN.md` exists in the current working directory.

- If it does not exist, **STOP** and tell the user to `cd` into their project/feature directory (the one containing `EXECUTION_PLAN.md`) and re-run `/phase-checkpoint $1`.

## Context Check

**Before starting:** If context is below 40% remaining, run `/compact` first. This ensures the full command instructions remain in context throughout execution. Compaction mid-command loses procedural instructions.

## Tool Availability Check

Before running checks, detect which optional tools are available by attempting a harmless call:

| Tool | Check Method | Fallback |
|------|--------------|----------|
| ExecuteAutomation Playwright | Check for `mcp__playwright__*` or `mcp__executeautomation__*` | Next in chain |
| Browser MCP | Check for `mcp__browsermcp__*` tools | Next in chain |
| Microsoft Playwright MCP | Check for `mcp__playwright__*` tools | Next in chain |
| Chrome DevTools MCP | Call `mcp__chrome-devtools__list_pages` | Manual verification |
| code-simplifier | Check if agent type available | Skip code simplification |
| Trigger.dev MCP | `mcp__trigger__list_projects` | Skip Trigger.dev checks |

**Browser tool fallback chain:** ExecuteAutomation Playwright → Browser MCP → Microsoft Playwright → Chrome DevTools → Manual

Read `.claude/verification-config.json` from PROJECT_ROOT. Use it to determine
commands for tests, lint, typecheck, build, coverage, and dev server.

If the config is missing or required commands are empty:
- Run `/configure-verification`
- Do not proceed with automated checks until commands are configured

## Local Verification (Must Pass First)

**IMPORTANT**: All local verification must pass before proceeding to production verification.
If any local check fails, stop and report — do not run production checks.

### Automated Local Checks

Run these commands and report results:

1. **Tests**
   ```
   {commands.test from verification-config}
   ```
   (if empty, block and ask to configure)

2. **Type Checking**
   ```
   {commands.typecheck from verification-config}
   ```
   (if empty, mark as not applicable or configure)

3. **Linting**
   ```
   {commands.lint from verification-config}
   ```
   (if empty, mark as not applicable or configure)

4. **Build** (if applicable)
   ```
   {commands.build from verification-config}
   ```
   (if empty and project has build step, ask to configure)

5. **Dev Server Starts**
   ```
   {devServer.command from verification-config}
   ```
   Verify it starts without errors and is accessible at `{devServer.url}`.

6. **Security Scan**

   Run security checks:
   - Use the project's configured security tooling (if documented)
   - Run secrets detection (pattern-based)
   - Run static analysis via documented tools or ask for a command

   For CRITICAL or HIGH issues:
   - Present each issue with resolution options
   - Apply fixes based on user choices
   - Re-scan to confirm resolution

   Security scan blocks checkpoint if CRITICAL or HIGH issues remain unresolved.

7. **Code Quality Metrics**

   Collect and report these metrics for the phase:

   ```
   CODE QUALITY METRICS
   --------------------
   Test Coverage: {X}% (target: 80%)
   Files changed in phase: {N}
   Lines added: {N}
   Lines removed: {N}
   New dependencies added: {list or "None"}
   ```

   To get coverage:
   - Use `commands.coverage` from verification-config if present
   - If empty, mark coverage as not applicable or ask to configure

   Flag if coverage dropped compared to before the phase (if a baseline exists).

### Optional Local Checks

These checks run only if the required tools are available (detected above).

8. **Code Simplification** (requires: code-simplifier plugin)

   If available, run code-simplifier on files changed in this phase:
   ```bash
   git diff --name-only HEAD~{commits-in-phase}
   ```

   Focus: reduce complexity, improve naming, eliminate redundancy. Preserve all functionality.

9. **Browser Verification** (requires browser MCP tools)

   First, check if phase includes UI work by scanning for `BROWSER:*` criteria.

   **If browser criteria exist:**

   a. **Resolve target URL** (deployment config check):
      - Read `deployment.enabled` from verification-config.json
      - If enabled: Invoke vercel-preview skill to get preview URL
      - If preview URL found: TARGET = preview URL
      - If not found and `fallbackToLocal`: TARGET = localhost (with warning)
      - If not found and NO fallback: BLOCK verification
      - If deployment not enabled: TARGET = localhost (devServer.url)

   b. Check tool availability (fallback chain):
      - ExecuteAutomation Playwright → Browser MCP → Microsoft Playwright → Chrome DevTools

   c. **If at least one tool available:**
      - Use the browser-verification skill with each criterion's `Verify:` metadata
      - Take snapshots for verification
      - Test against TARGET URL

   **Display target in output:**
   ```
   Browser Verification:
   - Target: Vercel Preview (https://my-app-xyz.vercel.app)
   [Or]
   - Target: Local Dev Server (http://localhost:3000)
   - Target: Local Dev Server (fallback - no preview deployment found)
   ```

   c. **If NO browser tools available (SOFT BLOCK):**
      - Display warning:
        ```
        ⚠️  BROWSER VERIFICATION BLOCKED

        This phase has {N} browser-based acceptance criteria but no browser
        MCP tools are available.

        Criteria requiring browser verification:
        - {list each BROWSER:* criterion}

        Options:
        1. Continue anyway (browser criteria become manual verification)
        2. Stop and configure browser tools first

        To enable automated browser verification, install one of:
        - ExecuteAutomation Playwright: Add to .mcp.json
        - Browser MCP: Install extension from browsermcp.io
        - Chrome DevTools MCP: Often pre-installed
        ```
      - Use AskUserQuestion to let user choose:
        - "Continue with manual verification" → Add browser checks to Human Required section
        - "Stop to configure tools" → Halt checkpoint, provide setup instructions

10. **Technical Debt Check** (optional)

    If `.claude/skills/tech-debt-check/SKILL.md` exists:
    - Run duplication analysis
    - Run complexity analysis
    - Check file sizes
    - Detect AI code smells

    Report findings with severity levels. Informational only (does not block).

### Manual Local Verification

From the "Phase $1 Checkpoint" section in EXECUTION_PLAN.md, extract LOCAL items
marked for manual verification.

**Before listing for human review, attempt automation using the auto-verify skill:**

For each manual item:
1. Invoke auto-verify skill with item text and available tools
2. Record attempt result (PASS, FAIL, or MANUAL)

**Categorize and report results:**

```
Automated Successfully:
- [x] "{item}" — PASS ({method}, {duration})
```

For items requiring manual verification ("Automation Failed" or "Truly Manual"), generate a **comprehensive verification guide** as described below.

### Manual Verification Guide Format

When ANY items require manual verification, produce a detailed, standalone guide that anyone could follow without prior project knowledge.

**CRITICAL:** Do not use placeholder text like "{First action to take}". Generate specific, actionable instructions based on the actual criterion and project context.

#### Guide Structure

For each manual item, generate ALL of the following sections.

**CRITICAL: URL Resolution for Manual Guides**

Before generating instructions, resolve the BASE_URL:

1. Read `deployment.enabled` from verification-config.json
2. If deployment enabled:
   - Invoke vercel-preview skill to get preview URL
   - If found: BASE_URL = preview URL
   - If not found: BASE_URL = devServer.url (note fallback)
3. If deployment not enabled:
   - BASE_URL = devServer.url

**All URLs in the guide MUST use BASE_URL** — never hardcode localhost when
deployment is enabled with a preview URL available.

```
═══════════════════════════════════════════════════════════════════════════════
MANUAL VERIFICATION: {criterion title}
═══════════════════════════════════════════════════════════════════════════════

## What We're Verifying
{1-2 sentence plain-English explanation of what this criterion tests and why it matters}

## Prerequisites

{If using Vercel preview:}
- [ ] Vercel deployment ready at {BASE_URL}
- [ ] Browser open (Chrome/Firefox recommended)
- [ ] {Any test accounts, API keys, or data needed}
- [ ] {Any specific state the app must be in}

{If using localhost:}
- [ ] Dev server running at {BASE_URL} (start with: `{command}`)
- [ ] Browser open (Chrome/Firefox recommended)
- [ ] {Any test accounts, API keys, or data needed}
- [ ] {Any specific state the app must be in}

## Step-by-Step Verification

### Step 1: {Action title}
1. Open your browser and navigate to: `{BASE_URL}{route}`
2. You should see: {description of expected initial state}
   - If you don't see this: {troubleshooting hint}

### Step 2: {Action title}
1. {Exact action to take, e.g., "Click the 'Sign In' button in the top-right corner"}
2. {Next action}
3. You should see: {expected result}
   - Screenshot reference: {if applicable, what the UI should look like}

### Step 3: {Action title}
1. {Continue with specific actions}
2. {Include exact text to enter, buttons to click, etc.}

{Continue with as many steps as needed - be thorough}

## Expected Results
✓ {Specific observable outcome 1}
✓ {Specific observable outcome 2}
✓ {Specific observable outcome 3}

## How to Confirm Success
The criterion PASSES if ALL of the following are true:
1. {Concrete, verifiable condition}
2. {Concrete, verifiable condition}
3. {Concrete, verifiable condition}

## Common Issues & Troubleshooting

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| {What you might see} | {Why it happens} | {How to fix it} |
| {Another symptom} | {Cause} | {Solution} |

## If Verification Fails
1. Check the browser console for errors (F12 → Console tab)
2. Check the terminal running the dev server for errors
3. Try: {specific recovery steps}
4. If still failing, note the exact error and report it

───────────────────────────────────────────────────────────────────────────────
```

#### Examples of Good vs Bad Instructions

**BAD (too vague):**
```
1. First action to take
2. What to verify/look for
3. How to confirm success
```

**GOOD (specific and actionable - localhost):**
```
### Step 1: Navigate to Login Page
1. Open your browser and go to: `http://localhost:3000/login`
2. You should see a login form with email and password fields
   - If you see a 404 error: Make sure the dev server is running with `npm run dev`

### Step 2: Enter Test Credentials
1. In the "Email" field, enter: `test@example.com`
2. In the "Password" field, enter: `testpassword123`
3. Click the blue "Sign In" button below the form

### Step 3: Verify Successful Login
1. You should be redirected to: `http://localhost:3000/dashboard`
2. The top-right corner should show "Welcome, Test User"
3. The navigation should now include "My Account" and "Logout" options
```

**GOOD (specific and actionable - Vercel preview):**
```
### Step 1: Navigate to Login Page
1. Open your browser and go to: `https://my-app-abc123-team.vercel.app/login`
2. You should see a login form with email and password fields
   - If you see a 404 error: Verify the deployment is ready in Vercel dashboard

### Step 2: Enter Test Credentials
1. In the "Email" field, enter: `test@example.com`
2. In the "Password" field, enter: `testpassword123`
3. Click the blue "Sign In" button below the form

### Step 3: Verify Successful Login
1. You should be redirected to: `https://my-app-abc123-team.vercel.app/dashboard`
2. The top-right corner should show "Welcome, Test User"
3. The navigation should now include "My Account" and "Logout" options
```

#### Context to Use When Generating Instructions

When writing verification guides, reference:
1. **EXECUTION_PLAN.md** — for acceptance criteria context
2. **Project files** — to find exact URLs, component names, test credentials
3. **package.json / config files** — for correct commands
4. **Previous phase implementations** — for understanding current app state

**Note:** Only items in "Truly Manual" genuinely require human action. Items in
"Automation Failed" may be automatable once the underlying issue is fixed.

### Update EXECUTION_PLAN.md Checkboxes (Auto-Verified Items)

After auto-verify passes items, immediately update their checkboxes in EXECUTION_PLAN.md:

1. **For each item that auto-verify marked PASS:**
   - Read EXECUTION_PLAN.md
   - Find the "### Phase $1 Checkpoint" section
   - Locate the exact line: `- [ ] {criterion text}`
   - Edit: change `- [ ]` to `- [x]`
   - Verify edit succeeded

2. **Matching rules:**
   - Match the exact checkbox text (criterion may be truncated in reports)
   - Use the phase section as anchor to avoid updating wrong items
   - Skip items already checked (`- [x]`)

### Human Confirmation (Batch)

For items in "Automation Failed" or "Truly Manual" categories, ask human for batch confirmation:

1. **List all items needing human verification:**
   ```
   Manual verification needed for {N} items:
   1. {item 1 text}
   2. {item 2 text}
   ...
   ```

2. **Ask ONE question using AskUserQuestion:**
   - Question: "Which items have you verified?"
   - Options:
     - "All verified" → Update ALL remaining checkboxes at once
     - "Some verified" → Follow up asking which ones (comma-separated numbers)
     - "None yet" → Leave all unchecked, continue to next section

3. **Accept natural language responses:**
   - "they're all good", "verified", "all done" → Treat as "All verified"
   - "all except 2" or "1 and 3 only" → Update specified items only

4. **Update checkboxes:**
   - For confirmed items, edit EXECUTION_PLAN.md to change `- [ ]` to `- [x]`
   - Use a single Edit call when updating multiple items in sequence
   - Do NOT ask follow-up confirmation questions after user says "all verified"

### Approach Review (Human)

Ask the human to review the phase's implementation approach against these criteria:

- Solutions use appropriate abstractions (not over/under-engineered)
- New code follows existing codebase patterns and conventions
- No unnecessary dependencies were added
- Error handling is consistent with rest of codebase
- Any "almost correct" AI solutions that need refinement?

**Reporting format:**
- Only list items that have issues or need attention
- If all criteria pass, report: "Approach Review: No issues noted"
- If issues exist, report each one briefly with context

### Regression Check (if feature work)

- Confirm existing tests still pass
- Note any changes to existing functionality

---

## Production Verification (After Local Passes)

**BLOCKED** until all Local Verification passes.

If local verification has any failures, show:
```
## Production Verification

(Blocked: Complete local verification first)

Pending production checks:
- [ ] {list items from EXECUTION_PLAN.md marked for production/staging}
```

### When Local Verification Passes

Extract PRODUCTION items from "Phase $1 Checkpoint" in EXECUTION_PLAN.md:

1. **Staging/Production Deployment Verification**
   - If phase includes deployment: verify staging environment works
   - Check production logs for errors (if applicable)
   - Verify no regressions in deployed environment

2. **External Integration Verification**
   - Third-party API connections working
   - External services responding correctly
   - Webhooks/callbacks functioning

3. **Production-Only Manual Checks**
   - Items that can only be verified in production environment
   - Performance under real load (if applicable)
   - Cross-browser/device testing on production URLs

## State Update

After checkpoint passes, update `.claude/phase-state.json`:

1. Set phase status to `CHECKPOINTED`
2. Add `completed_at` timestamp
3. Record checkpoint results

```json
{
  "phases": [
    {
      "number": 1,
      "status": "CHECKPOINTED",
      "completed_at": "{ISO timestamp}",
      "checkpoint": {
        "tests_passed": true,
        "type_check_passed": true,
        "lint_passed": true,
        "security_passed": true,
        "coverage_percent": 85,
        "manual_verified": true
      }
    }
  ]
}
```

If checkpoint fails, keep status as `IN_PROGRESS` and add `checkpoint_failed` with details.

## Verification Evidence and Logs

After running checks:
- Write a checkpoint report to `.claude/verification/phase-$1.md`
- Append results to `.claude/verification-log.jsonl`
  - Include check type, status, timestamp, and evidence path
 - Ensure `.claude/verification/` exists before writing evidence files

Example log entry:
```json
{
  "timestamp": "{ISO timestamp}",
  "scope": "phase-checkpoint",
  "phase": "$1",
  "check": "tests",
  "status": "PASS",
  "evidence": ".claude/verification/phase-$1.md"
}
```

---

## Report

```
Phase $1 Checkpoint Results
===========================

Tool Availability:
- ExecuteAutomation Playwright: ✓ | ✗ (primary)
- Browser MCP Extension: ✓ | ✗
- Microsoft Playwright MCP: ✓ | ✗
- Chrome DevTools MCP: ✓ | ✗
- code-simplifier: ✓ | ✗
- Trigger.dev MCP: ✓ | ✗ | N/A

## Local Verification

Automated Checks:
- Tests: PASSED | FAILED
- Type Check: PASSED | FAILED | SKIPPED
- Linting: PASSED | FAILED | SKIPPED
- Build: PASSED | FAILED | SKIPPED
- Dev Server: PASSED | FAILED | SKIPPED
- Security: PASSED | FAILED | X critical, Y high
- Coverage: {X}% (target: 80%)

Optional Checks:
- Code Simplification: APPLIED | SKIPPED
- Browser Verification: PASSED | SKIPPED
  - Target: Vercel Preview ({URL}) | Local Dev Server ({URL}) | Fallback ({URL})
- Tech Debt: PASSED | NOTES | SKIPPED

Manual Local Checks:
- Automated: {X} items verified automatically
- Failed automation: {Y} items (see details below)
- Truly manual: {Z} items (human judgment required)

Automated Successfully:
- [x] "{item}" — PASS ({method}, {duration})

Items Requiring Manual Verification: {N}
(See detailed verification guide below)

Approach Review: No issues noted | {list specific issues}
```

**If any items require manual verification, append the full Manual Verification Guide (see format above) after this summary report.** The guide should be comprehensive enough that anyone unfamiliar with the project could complete the verification.

```

Local Verification: ✓ PASSED | ✗ FAILED (address issues above)

---

## Production Verification

[If local passed:]
- [ ] Staging deployment verified
- [ ] Production logs clean
- [ ] External integrations working
- [ ] {other production items from EXECUTION_PLAN.md}

[If local failed:]
(Blocked: Complete local verification first)

---

Overall: Ready to proceed | Local issues to address | Production issues to address
```

## Auto-Advance (After Checkpoint Passes)

Check if auto-advance is enabled and this checkpoint passes all criteria.

### Configuration Check

Read `.claude/settings.local.json` for auto-advance configuration:

```json
{
  "autoAdvance": {
    "enabled": true      // default: true
  }
}
```

If `autoAdvance` is not configured, use defaults (`enabled: true`).

### Auto-Advance Conditions

Auto-advance to `/phase-prep {N+1}` ONLY if ALL of these are true:

1. ✓ All automated checks passed (tests, lint, types, security)
2. ✓ No "truly manual" verification items remain (auto-verify was attempted above)
3. ✓ No production verification items exist
4. ✓ Phase $1 is not the final phase
5. ✓ `--pause` flag was NOT passed to this command
6. ✓ `autoAdvance.enabled` is true (or not configured, defaulting to true)

**Rationale:** Auto-verify (run in Manual Local Verification above) attempts automation before blocking. Only items that genuinely require human judgment block auto-advance. Production verification items always require human presence to confirm deployed behavior.

### If Auto-Advance Conditions Met

1. **Show brief notification:**
   ```
   AUTO-ADVANCE
   ============
   All Phase $1 criteria verified (no truly manual items remain).
   Proceeding to next phase...
   ```

2. **Execute immediately:**
   - Track this command in auto-advance session log
   - Invoke `/phase-prep {N+1}` using the Skill tool
   - Continue auto-advance chain (phase-prep will continue if it passes)

### If Auto-Advance Conditions NOT Met

Stop and report why:

```
AUTO-ADVANCE STOPPED
====================

Reason: {one of below}
- Truly manual verification items remain (human judgment required)
- Production verification items exist (human intervention required)
- Phase $1 is the final phase
- Auto-advance disabled via --pause flag
- Auto-advance disabled in settings

{If manual/production items exist:}
Human verification required:
- [ ] {item 1}
- [ ] {item 2}

Next steps:
1. Complete the verification items above
2. Run /phase-prep {N+1} manually when ready
```

### Auto-Advance Session Tracking

Maintain `.claude/auto-advance-session.json` during auto-advance:

```json
{
  "started_at": "{ISO timestamp}",
  "commands": [
    {"command": "/phase-checkpoint 1", "status": "PASS", "timestamp": "{ISO}"},
    {"command": "/phase-prep 2", "status": "PASS", "timestamp": "{ISO}"},
    {"command": "/phase-start 2", "status": "PASS", "timestamp": "{ISO}"},
    {"command": "/phase-checkpoint 2", "status": "MANUAL_REQUIRED", "timestamp": "{ISO}"}
  ],
  "stopped_at": "{ISO timestamp}",
  "stop_reason": "manual_verification_required"
}
```

### Session Report (When Auto-Advance Stops)

When auto-advance stops (for any reason), generate a summary:

```
AUTO-ADVANCE SESSION COMPLETE
=============================

Commands executed:
1. /phase-checkpoint 1 → ✓ All criteria passed
2. /phase-prep 2 → ✓ All setup complete
3. /phase-start 2 → ✓ All tasks completed
4. /phase-checkpoint 2 → ⚠ Manual verification required

Summary:
- Phases completed: 1 (Phase 2)
- Steps completed: 4
- Duration: 12m 34s
- Stopped: Manual verification items detected

Requires attention:
- [ ] Verify payment flow works end-to-end (localhost:3000/checkout)
- [ ] Confirm email notifications received

Next: Complete manual items, then run /phase-checkpoint 2 again
```

Delete `.claude/auto-advance-session.json` after reporting (or on fresh `/phase-start 1` with no prior session).

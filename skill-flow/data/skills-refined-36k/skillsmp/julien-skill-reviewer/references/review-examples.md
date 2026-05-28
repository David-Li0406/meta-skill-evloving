# Review Examples

Real-world examples of skill reviews with before/after comparisons.

## Example 1: Bloated SKILL.md with DRY Violations

### Initial State

**File**: skills/api-integrator/SKILL.md (8,500 words)

**Structure**:
```markdown
---
name: api-integrator
description: Integrates with external APIs
---

# API Integrator

## Overview
[500 words explaining what APIs are]

## Complete API Reference
[2000 words of endpoint documentation]

## Example 1: GitHub Integration
[800 words with complete code]

## Example 2: Slack Integration
[800 words with complete code]

## Example 3: Notion Integration
[800 words with complete code]

## Troubleshooting
[1500 words of error scenarios]

## Advanced Configuration
[1200 words of config options]

## Best Practices
[900 words of guidelines]
```

### Initial Scores

| Dimension | Score | Reason |
|-----------|-------|--------|
| Clarity | 3/5 | Clear but too verbose |
| Completeness | 4/5 | Comprehensive |
| Discoverability | 4/5 | Good description |
| **Context Efficiency** | **1/5** | **8500 words - massive violation** |
| Actionability | 3/5 | Steps present but buried |
| **Resource Organization** | **1/5** | **Everything in one file** |
| Examples | 4/5 | Many examples (but too long) |
| Skill Chaining | 2/5 | Missing |
| Error Handling | 4/5 | Comprehensive troubleshooting |
| **AVERAGE** | **2.9/5** | **Below threshold** |

### Issues Identified

#### Issue 1: Bloated SKILL.md - Context Efficiency 1/5

**Problem**: 8,500 words in SKILL.md (should be <5,000)

**Suggested Refactoring**:
1. Keep overview and high-level workflow only (~1,000 words)
2. Move API reference → `references/api-reference.md`
3. Move examples → `references/examples.md`
4. Move troubleshooting → `references/troubleshooting.md`
5. Move advanced config → `references/advanced-configuration.md`
6. Move best practices → `references/best-practices.md`

**Expected Impact**: Context Efficiency 1/5 → 5/5

#### Issue 2: No Progressive Disclosure - Resource Organization 1/5

**Problem**: No `references/` directory, all content in SKILL.md

**Suggested Refactoring**:
Create proper structure:
```
skills/api-integrator/
├── SKILL.md (2,000 words - lean)
├── references/
│   ├── api-reference.md (2,000 words)
│   ├── examples.md (2,400 words - 3 examples)
│   ├── troubleshooting.md (1,500 words)
│   ├── advanced-configuration.md (1,200 words)
│   └── best-practices.md (900 words)
└── scripts/
    └── validate-api-response.py
```

**Expected Impact**: Resource Organization 1/5 → 5/5

#### Issue 3: Missing Skill Chaining - Skill Chaining 2/5

**Problem**: Only mentions "can be used with other skills" - no specifics

**Suggested Fix**: Add comprehensive Skill Chaining section with:
- Input Expected: API keys, config file format
- Output Produced: Formatted responses, logs
- Compatible Skills After: data-processor, report-generator
- Visual workflow diagram

**Expected Impact**: Skill Chaining 2/5 → 5/5

### Refactoring Executed

#### 1. Created references/ structure

**New SKILL.md** (2,000 words):
```markdown
---
name: api-integrator
description: Integrates with external APIs (GitHub, Slack, Notion, etc.)
             for automated workflows. Use when connecting Claude to external
             services via REST APIs.
---

# API Integrator

## Purpose

Integrate Claude with external APIs through a unified interface.
Supports authentication, request/response handling, and error recovery.

## When to Use

- ✅ Connecting Claude to external services
- ✅ Automating API calls in workflows
- ✅ Processing API responses

## High-Level Workflow

1. Configure API credentials (see references/configuration.md)
2. Define endpoint and parameters
3. Execute request with error handling
4. Process response

For detailed instructions, see `references/detailed-guide.md`.

## Quick Example

```python
# Basic API call
from scripts import api_client

response = api_client.call(
    service='github',
    endpoint='/repos/user/repo',
    method='GET'
)
```

For more examples, see `references/examples.md`.

## API Reference

Brief overview of supported services:
- **GitHub**: Repos, Issues, PRs
- **Slack**: Messages, Channels
- **Notion**: Pages, Databases

Complete API documentation: `references/api-reference.md`

## Troubleshooting

Common errors and quick fixes:
- Authentication failed → Check API key in config
- Rate limit exceeded → Use backoff strategy

Full troubleshooting guide: `references/troubleshooting.md`

## 🔗 Skill Chaining

[Complete Skill Chaining section added]
```

#### 2. Created references/examples.md (2,400 words)

Moved all 3 examples with full code and explanations.

#### 3. Created references/api-reference.md (2,000 words)

Complete endpoint documentation.

#### 4. Created references/troubleshooting.md (1,500 words)

All error scenarios with solutions.

#### 5. Created references/advanced-configuration.md (1,200 words)

Config options and customization.

#### 6. Created references/best-practices.md (900 words)

Guidelines and recommendations.

### Re-evaluation Results

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Clarity | 3/5 | 4/5 | +1 ✅ |
| Completeness | 4/5 | 4/5 | - |
| Discoverability | 4/5 | 4/5 | - |
| **Context Efficiency** | **1/5** | **5/5** | **+4 ✅✅✅✅** |
| Actionability | 3/5 | 4/5 | +1 ✅ |
| **Resource Organization** | **1/5** | **5/5** | **+4 ✅✅✅✅** |
| Examples | 4/5 | 5/5 | +1 ✅ |
| **Skill Chaining** | **2/5** | **5/5** | **+3 ✅✅✅** |
| Error Handling | 4/5 | 5/5 | +1 ✅ |
| **AVERAGE** | **2.9/5** | **4.6/5** | **+1.7** ✅✅ |

**Status**: ✅ **Production ready** - Exceeds threshold (4.5/5 = excellent)

**Summary**:
- SKILL.md: 8,500 → 2,000 words (-76% reduction)
- Created 5 reference files properly organized
- Added comprehensive Skill Chaining section
- Score improved from 2.9/5 → 4.6/5
- **Result**: From "needs major rework" to "excellent"

---

## Example 2: Missing Skill Chaining

### Initial State

**File**: skills/deployment-manager/SKILL.md (3,000 words - good length)

**Scores**:
- Most dimensions: 4-5/5 ✅
- **Skill Chaining: 1/5** ❌ (no workflow documentation)
- Average: 3.8/5 (just above threshold but could be better)

### Issue

```markdown
## Issue: No Workflow Context - Skill Chaining 1/5

**Problem**: Skill appears isolated, no documentation of:
- What comes before this skill
- What inputs are expected
- What outputs are produced
- What skills can follow

**Impact**: Users don't know:
- When to use this skill in a larger workflow
- What prerequisites are needed
- What to do after deployment succeeds

**Example**: Skill mentions "deploys to VPS" but:
- ❌ Doesn't specify input format (which files? which branch?)
- ❌ Doesn't specify prerequisites (SSH keys? config files?)
- ❌ Doesn't specify what happens after (monitoring? validation?)
```

### Suggested Fix

Add complete Skill Chaining section:

```markdown
## 🔗 Skill Chaining

### Skills Required Before

- **local-testing** (recommandé): Validates build locally before deploy
- **git-workflow** (optionnel): Ensures correct branch is checked out

### Input Expected

- **Git state**: Branch `main` or `staging` with clean working tree
- **Config file**: `ecosystem.config.cjs` on VPS (not in repo)
- **Environment**: SSH access to `automation@69.62.108.82`
- **Prerequisites**: Node.js v18+, PM2 installed on VPS

### Output Produced

- **Format**: Application deployed and running at URL
  - Production: https://example.com
  - Staging: https://preview.example.com
- **Side effects**:
  - PM2 process restarted
  - New code deployed to `/var/www/app/`
  - Build artifacts generated
  - Logs created at `/var/log/pm2/`
- **Duration**: 2-3 minutes
  - rsync: ~30s
  - npm install: ~60s
  - build: ~60s
  - PM2 restart: ~5s

### Compatible Skills After

**Recommandés**:
- **webapp-testing**: Validate deployment succeeded
- **monitoring-setup**: Enable error tracking

**Optionnels**:
- **performance-audit**: Check Lighthouse scores
- **notification-sender**: Alert team of deployment

### Called By

- **git-workflow-manager**: Complete deployment pipeline
- **post-push hook**: Automatic deploy after git push
- Direct user invocation: Manual deployment

### Tools Used

- `Bash` (usage: rsync, ssh, npm, pm2 commands)
- `Read` (usage: verify ecosystem.config.cjs exists)
- `AskUserQuestion` (usage: confirm production deploys)

### Visual Workflow

\`\`\`
User: git push origin main
    ↓
pre-push hook validation
    ├─► npm run build (local)
    ├─► npm run check
    └─► Detect secrets
    ↓
Push succeeds
    ↓
[THIS SKILL: deployment-manager]
    ├─► rsync code → VPS
    ├─► SSH to VPS
    ├─► npm install --production
    ├─► npm run build
    └─► pm2 restart app
    ↓
Deployed at https://example.com
    ↓
[Optional next steps]
    ├─► webapp-testing (verify)
    └─► monitoring-setup
\`\`\`

### Usage Example

**Scenario**: Deploy new feature to production

**Command**: `/deployment-manager main`

**Result**:
- Site updated at https://example.com
- Deployment completed in ~2.5 minutes
- PM2 logs confirm successful restart
- Ready for post-deployment validation
```

### After Adding Skill Chaining

**Score change**: Skill Chaining 1/5 → 5/5
**Average change**: 3.8/5 → 4.2/5
**Status**: ✅ Production ready with clear workflow context

---

## Example 3: DRY Violation - Duplication Between Files

### Initial State

**Files**:
- SKILL.md: Contains API docs (150 lines)
- references/api-reference.md: Contains same API docs (150 lines)

### Issue

```markdown
## Issue: DRY Violation - Context Efficiency 2/5

**Location**:
- SKILL.md lines 120-270
- references/api-reference.md lines 1-150

**Problem**: API reference documentation duplicated identically in both files

**Example Duplication**:

SKILL.md:
\`\`\`markdown
### Endpoint: GET /api/users
**Description**: Retrieves paginated list of users
**Parameters**:
  - page (int): Page number (default: 1)
  - limit (int): Items per page (default: 20)
**Response**: Array of user objects
[...150 lines of identical content...]
\`\`\`

references/api-reference.md:
\`\`\`markdown
### Endpoint: GET /api/users
**Description**: Retrieves paginated list of users
**Parameters**:
  - page (int): Page number (default: 1)
  - limit (int): Items per page (default: 20)
**Response**: Array of user objects
[...150 lines of identical content...]
\`\`\`

**Impact**: Maintenance nightmare - updates must be made in two places

**Suggested Fix**:

SKILL.md (10 lines):
\`\`\`markdown
## API Reference

This skill integrates with the XYZ API. For complete endpoint
documentation including parameters, response formats, and examples,
see \`references/api-reference.md\`.

**Quick reference of main endpoints**:
- GET /api/users - List users (paginated)
- POST /api/users - Create new user
- GET /api/users/{id} - Get user details
\`\`\`

references/api-reference.md (150 lines):
[Keep complete documentation here only]
```

### Refactoring

**Actions**:
1. ✅ Removed API docs from SKILL.md (deleted lines 120-270)
2. ✅ Added brief overview + pointer in SKILL.md (10 lines)
3. ✅ Kept complete docs in references/api-reference.md

**Result**:
- SKILL.md: 4,000 → 3,860 words
- No duplication
- Single source of truth: references/api-reference.md
- Context Efficiency: 2/5 → 4/5

---

## Example 4: Unclear Instructions - Clarity Issues

### Initial State

**SKILL.md excerpt**:
```markdown
## Deployment Process

Handle the deployment appropriately based on the environment.
Make sure everything is configured correctly before proceeding.
If errors occur, debug them as needed.
```

### Issue

```markdown
## Issue: Vague Instructions - Clarity 2/5

**Location**: SKILL.md lines 45-48

**Problem**: Instructions use vague language like "appropriately",
"make sure", "as needed" without concrete steps

**Current text**:
"Handle the deployment appropriately based on the environment.
Make sure everything is configured correctly before proceeding.
If errors occur, debug them as needed."

**Problems**:
- ❌ "appropriately" - what does this mean?
- ❌ "make sure everything is configured" - how? what to check?
- ❌ "debug them as needed" - no guidance on how

**Suggested Fix**:

\`\`\`markdown
## Deployment Process

### Step 1: Validate Environment

Check prerequisites are met:
\`\`\`bash
# Verify Node.js version
node --version  # Should be v18+

# Verify SSH access
ssh automation@69.62.108.82 "echo OK"  # Should print "OK"

# Verify config exists
ssh automation@69.62.108.82 "ls /var/www/app/ecosystem.config.cjs"
\`\`\`

### Step 2: Deploy Based on Branch

**For staging branch**:
\`\`\`bash
git checkout staging
npm run deploy:staging
\`\`\`

**For main branch**:
\`\`\`bash
git checkout main
npm run deploy:production
\`\`\`

### Step 3: Handle Common Errors

**If rsync fails with "Permission denied"**:
\`\`\`bash
# Fix permissions on VPS
ssh automation@69.62.108.82 "chmod -R u+w /var/www/app"
\`\`\`

**If npm install fails with "EACCES"**:
\`\`\`bash
# Clear npm cache and retry
ssh automation@69.62.108.82 "cd /var/www/app && npm cache clean --force"
\`\`\`

**If PM2 restart fails**:
\`\`\`bash
# Check PM2 status
ssh automation@69.62.108.82 "pm2 status"

# Force restart
ssh automation@69.62.108.82 "pm2 delete app && pm2 start ecosystem.config.cjs"
\`\`\`
\`\`\`
```

### After Fix

**Score change**: Clarity 2/5 → 5/5
**Impact**: Instructions now actionable, copy-paste ready, error scenarios covered

---

## Common Patterns Summary

### Pattern 1: Bloat (Context Efficiency)
**Symptom**: SKILL.md >5000 words
**Fix**: Extract to references/

### Pattern 2: DRY Violation
**Symptom**: Same content in multiple files
**Fix**: Keep in one place, add pointers

### Pattern 3: Missing Workflow Context
**Symptom**: Skill Chaining score <3/5
**Fix**: Add comprehensive Skill Chaining section

### Pattern 4: Vague Instructions
**Symptom**: Clarity score <3/5
**Fix**: Replace vague terms with concrete steps, commands, examples

### Pattern 5: No Examples
**Symptom**: Examples score <3/5
**Fix**: Add 2-3 concrete, realistic examples (in references/examples.md)

### Pattern 6: No Error Handling
**Symptom**: Error Handling score <3/5
**Fix**: Document common errors with solutions (in references/troubleshooting.md)

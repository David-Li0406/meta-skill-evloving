# Formulate Skill Examples

Detailed examples of formula creation and instantiation scenarios.

---

## Example 1: Simple Multi-Step Formula

**User Request**: "/formulate Add OAuth2 support for GitLab integration"

**Agent Actions**:

```bash
# Phase 0: Context Discovery
mcp__smart-connections-work__lookup --query="OAuth2 GitLab authentication" --limit=10
cat docs/code-map/README.md | grep -i auth

# Phase 0.5: Prior Formula Check
ls .agents/formulas/*.formula.toml | xargs grep -l "OAuth\|GitLab"
bd list --type=epic | grep -i oauth

# Phase 1: Research
# Found existing auth patterns in services/gateway/
# GitLab MCP server already exists at services/mcp-servers/gitlab/

# Phase 2: Decomposition
# Step 1: Add OAuth2 callback endpoint (no deps)
# Step 2: Implement token exchange flow (depends on callback)
# Step 3: Add session token storage (depends on token-exchange)
# Step 4: Update GitLab MCP to use OAuth tokens (depends on session-storage)
# Step 5: Add OAuth2 config to Helm values (no deps, parallel)

# Phase 3: Create Formula Template
```

**Formula output** (`.agents/formulas/oauth-gitlab.formula.toml`):

```toml
# Formula: OAuth2 GitLab Integration
# Reusable pattern for adding OAuth2 to service integrations

formula = "oauth-gitlab"
description = "Add OAuth2 authentication for GitLab integration"
version = 2
type = "workflow"

[vars]
provider = "gitlab"

[[steps]]
id = "callback-endpoint"
title = "Add OAuth2 callback endpoint"
description = """
Add OAuth2 callback endpoint for {{provider}}:
- Create callback route in services/gateway/routes.py
- Implement callback handler in services/gateway/oauth.py
- Handle authorization code exchange
"""
needs = []

[[steps]]
id = "token-exchange"
title = "Implement token exchange flow"
description = """
Implement OAuth2 token exchange:
- Exchange authorization code for access token
- Handle refresh tokens
- Store tokens securely
"""
needs = ["callback-endpoint"]

[[steps]]
id = "session-storage"
title = "Add session token storage"
description = """
Add session-based token storage:
- Create session module in services/gateway/session.py
- Integrate with Redis for token storage
- Handle session expiration
"""
needs = ["token-exchange"]

[[steps]]
id = "mcp-update"
title = "Update {{provider}} MCP to use OAuth tokens"
description = """
Update {{provider}} MCP server to use OAuth:
- Modify services/mcp-servers/{{provider}}/ to use stored tokens
- Remove hardcoded credentials
- Add token refresh logic
"""
needs = ["session-storage"]

[[steps]]
id = "helm-config"
title = "Add OAuth2 config to Helm values"
description = """
Add OAuth2 configuration:
- Add oauth section to charts/ai-platform/values.yaml
- Include clientId, clientSecret placeholders
- Document configuration options
"""
needs = []
```

```bash
# Phase 4: Cook and Pour
bd cook .agents/formulas/oauth-gitlab.formula.toml --persist
# -> Cooked proto: oauth-gitlab

bd mol pour oauth-gitlab
# -> Created mol ai-platform-101 with children:
#    ai-platform-101.callback-endpoint, ai-platform-101.token-exchange, etc.
```

**Result**: 5 steps, computed waves:
- Wave 1: callback-endpoint, helm-config (parallel, different files)
- Wave 2: token-exchange
- Wave 3: session-storage
- Wave 4: mcp-update

---

## Example 2: Reusing an Existing Formula

**Scenario**: User wants to add OAuth2 for a different provider.

**Agent Actions**:

```bash
# Phase 0.5: Find existing formula
ls .agents/formulas/*.formula.toml | xargs grep -l "oauth"
# Found: oauth-gitlab.formula.toml

cat .agents/formulas/oauth-gitlab.formula.toml
# Formula is parameterized with {{provider}}
```

**Agent Response**:

"I found an existing formula `oauth-gitlab.formula.toml` that's parameterized for different
OAuth providers. I can instantiate it with `provider=github`:

```bash
# Pour with different provider variable
bd mol pour oauth-gitlab --var provider=github
```

This will create the same 5-step structure but for GitHub instead of GitLab."

---

## Example 3: Formula From Research

**Scenario**: `/research` was already run, now creating a formula from findings.

**Agent Actions**:

```bash
# Find recent research
ls -lt .agents/research/*.md | head -3
cat .agents/research/2026-01-03-oauth-investigation.md

# Research document contains:
# ## Recommendations
# 1. Implement token refresh (P1) - security critical
# 2. Add rate limiting (P2) - prevents abuse
# 3. Add audit logging (P2) - compliance requirement
```

**Formula output** (`.agents/formulas/oauth-hardening.formula.toml`):

```toml
# Formula: OAuth Hardening
# Based on research: 2026-01-03-oauth-investigation.md

formula = "oauth-hardening"
description = "Security hardening for OAuth implementations"
version = 2
type = "workflow"

[[steps]]
id = "token-refresh"
title = "Implement token refresh mechanism"
description = """
Implement automatic token refresh:
- Add refresh token handling
- Implement token rotation
- Handle refresh failures gracefully

Based on research: 2026-01-03-oauth-investigation.md
"""
needs = []

[[steps]]
id = "rate-limiting"
title = "Add OAuth rate limiting"
description = """
Add rate limiting to OAuth endpoints:
- Limit auth attempts per IP
- Add exponential backoff on failures
- Log rate limit events
"""
needs = []

[[steps]]
id = "audit-logging"
title = "Add OAuth audit logging"
description = """
Add comprehensive audit logging:
- Log all auth events
- Include user, timestamp, outcome
- Integrate with SIEM if available
"""
needs = []
```

**Result**: All 3 steps can run in parallel (Wave 1) - no dependencies between them.

---

## Example 4: Complex Dependency Graph Formula

**Scenario**: Feature with multiple parallel tracks that merge.

**Formula output** (`.agents/formulas/multi-tenant.formula.toml`):

```toml
# Formula: Multi-tenant Support
# Complex formula with parallel tracks and merge points

formula = "multi-tenant"
description = "Add multi-tenant support to the platform"
version = 2
type = "workflow"

# Track 1: Database changes
[[steps]]
id = "db-tenant-column"
title = "Add tenant column to all tables"
description = """
Database schema changes for multi-tenancy:
- Add tenant_id column to all entity tables
- Create migration scripts
- Update indexes for tenant queries
"""
needs = []

[[steps]]
id = "db-rls"
title = "Implement row-level security"
description = """
Add PostgreSQL row-level security:
- Create RLS policies per table
- Test isolation between tenants
- Document RLS configuration
"""
needs = ["db-tenant-column"]

# Track 2: API changes (parallel with Track 1)
[[steps]]
id = "api-middleware"
title = "Add tenant middleware"
description = """
Add tenant context middleware:
- Extract tenant from request headers/JWT
- Inject tenant context into request
- Handle missing tenant gracefully
"""
needs = []

[[steps]]
id = "api-endpoints"
title = "Update all endpoints for tenant context"
description = """
Update API endpoints:
- Add tenant filter to all queries
- Validate tenant access on mutations
- Update OpenAPI specs
"""
needs = ["api-middleware"]

# Merge point: depends on both tracks
[[steps]]
id = "integration-tests"
title = "Integration tests for multi-tenant"
description = """
Comprehensive integration testing:
- Test tenant isolation
- Test cross-tenant access prevention
- Performance testing with multiple tenants
"""
needs = ["db-rls", "api-endpoints"]
```

**Computed Waves:**
- Wave 1: db-tenant-column, api-middleware (parallel start)
- Wave 2: db-rls, api-endpoints (parallel, different tracks)
- Wave 3: integration-tests (merge point, needs both tracks done)

---

## Example 5: Quick Formula (3 Steps or Less)

**Scenario**: Small goal, simple formula.

**Formula output** (`.agents/formulas/rate-limiting-quick.formula.toml`):

```toml
# Formula: Rate Limiting (Quick)
# Simple formula for adding rate limiting

formula = "rate-limiting-quick"
description = "Quick rate limiting implementation"
version = 2
type = "workflow"

[vars]
endpoint = "/api/auth"

[[steps]]
id = "impl"
title = "Add rate limiting to {{endpoint}}"
description = """
Implement rate limiting:
- Add RateLimitMiddleware to services/gateway/middleware.py
- Configure limits for {{endpoint}}
- Return 429 with Retry-After header
"""
needs = []

[[steps]]
id = "config"
title = "Add rate limit config to Helm values"
description = """
Add configuration:
- Add rateLimit section to charts/ai-platform/values.yaml
- Include requestsPerMinute and burstSize
- Document in values.yaml comments
"""
needs = []
```

**Summary output:**
```markdown
# Formula Instantiated: Rate Limiting for Auth

**Formula:** `.agents/formulas/rate-limiting-quick.formula.toml`
**Steps:** 2 steps (Wave 1 only - all parallel)

| ID | Step | Ready |
|----|------|-------|
| xxx.impl | Add rate limiting to /api/auth | Ready |
| xxx.config | Add rate limit config to Helm values | Ready |

Both can run in parallel (different files). Use:
```bash
bd ready
/implement xxx.impl
```
```

---

## Anti-Pattern Examples

### WRONG: Using Old Formula Format

```toml
# WRONG - This format will fail with bd cook!
[formula]                              # WRONG: use top-level `formula = "..."`
name = "oauth-gitlab"
version = "1.0.0"                      # WRONG: use integer version = 2

[variables]                            # WRONG: use [vars] with simple values
provider = { type = "string" }         # WRONG: complex type definitions

[[tasks]]                              # WRONG: use [[steps]]
id = "callback-endpoint"
title = "Add callback"
type = "feature"                       # WRONG: no type in steps
priority = "P1"                        # WRONG: no priority in steps
depends_on = []                        # WRONG: use needs = []
files_affected = ["..."]               # WRONG: no files_affected

[waves]                                # WRONG: waves are computed, not declared
1 = ["callback-endpoint", "helm-config"]
```

**Correct version:**

```toml
formula = "oauth-gitlab"
description = "Add OAuth2 authentication for GitLab integration"
version = 2
type = "workflow"

[vars]
provider = "gitlab"

[[steps]]
id = "callback-endpoint"
title = "Add callback"
description = "Add OAuth2 callback endpoint..."
needs = []
```

### WRONG: Children Depending on Epic

```bash
# DON'T DO THIS with --immediate mode
bd create "Epic: OAuth" --type epic
# -> ai-platform-400

bd create "Add callback" --type feature
# -> ai-platform-401

bd dep add ai-platform-401 ai-platform-400  # WRONG!
# Result: ai-platform-401 will NEVER become ready because
# the epic can't be closed until children are done (deadlock)
```

### WRONG: Skipping Description in Steps

```toml
# WRONG - description is required!
[[steps]]
id = "impl"
title = "Implement feature"
needs = []
# Missing description field - will fail validation!
```

### WRONG: Creating Too Many Steps

```toml
# DON'T DO THIS - 15+ steps is too many
# Better: Break into 2-3 formulas of 5 steps each
# Or: Create first 5, complete, then plan next 5
```

### WRONG: One-Off Plans for Repeatable Patterns

```bash
# DON'T DO THIS
# Creating a new plan document every time you add OAuth to a service

# Better: Create a formula template once, pour with variables
bd mol pour oauth-gitlab --var provider=github
```

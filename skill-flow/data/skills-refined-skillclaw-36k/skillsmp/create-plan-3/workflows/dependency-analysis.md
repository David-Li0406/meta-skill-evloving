# Phase 3: Identify Dependencies

**Purpose**: Discover file dependencies and task ordering constraints using project-intel.mjs.

---

## Step 3.1: File Dependencies

**Intelligence Queries**:

```bash
# Find what files we'll need to modify
project-intel.mjs --search "auth|session|oauth" --json > /tmp/plan_target_files.json

# Check dependencies of key files
project-intel.mjs --dependencies src/auth/session.ts --direction upstream --json > /tmp/plan_deps_upstream.json

# Check what depends on files we'll modify (impact analysis)
project-intel.mjs --dependencies src/auth/session.ts --direction downstream --json > /tmp/plan_deps_downstream.json

# Analyze symbols we'll need to understand
project-intel.mjs --symbols src/auth/session.ts --json > /tmp/plan_symbols.json
```

**Why This Matters**:
- **Upstream dependencies**: What our code relies on (libraries, utils)
- **Downstream dependencies**: What code relies on us (breaking changes impact)
- **Symbol analysis**: Functions/classes we need to understand or modify

---

## Step 3.2: CoD^Σ Dependency Discovery

**Evidence-Based Process**:

```markdown
Step 1: ⇄ IntelQuery("target files")
  ↳ Query: project-intel.mjs --search "auth" --json
  ↳ Data: src/auth/session.ts, src/auth/middleware.ts, src/auth/oauth.ts

Step 2: ⇄ IntelQuery("file dependencies")
  ↳ Query: project-intel.mjs --dependencies src/auth/session.ts --direction upstream --json
  ↳ Data: Imports: crypto (stdlib), jsonwebtoken (lib), ./utils/validation (local)

Step 3: ⇄ IntelQuery("impact analysis")
  ↳ Query: project-intel.mjs --dependencies src/auth/session.ts --direction downstream --json
  ↳ Data: Used by: src/api/routes.ts:23, src/middleware/auth.ts:15

Step 4: → AnalyzeImpact
  ↳ Modifying session.ts affects routes and middleware
  ↳ Must update tests in tests/auth/ directory
  ↳ Breaking changes require migration guide
```

**Token Efficiency**:
- Intel queries: ~500 tokens
- Targeted reads of key files: ~800 tokens
- **Total: ~1,300 tokens vs 15,000+ (91% savings)**

---

## Step 3.3: Task Dependency Graph

**Identify Ordering Constraints**:

**Sequential Dependencies** (must run in order):
```
T1 (Add DB schema)
 ↓
T2 (Backend OAuth flow) → depends on schema
 ↓
T3 (Frontend UI) → depends on backend API
 ↓
T6 (E2E test) → depends on full flow working
```

**Parallel Opportunities** (can run simultaneously):
```
T1 (DB schema)
 ├→ T2 (OAuth flow) ─→ T3 (UI) ─→ T6 (E2E test)
 └→ T4 (Session mgmt) ─→ T5 (Logout) ─┘
```

**Marking Parallelization** (Article VIII):
- Mark independent tasks with `[P]` in plan
- Example: `T2 [P] Implement OAuth flow`
- Example: `T4 [P] Implement session management`

---

## Step 3.4: Dependency Matrix

**Document Relationships**:

| Task | Depends On | Blocks | Can Run Parallel With |
|------|-----------|--------|----------------------|
| T1 (DB) | None | T2, T4 | None |
| T2 (OAuth) | T1 | T3, T6 | T4 |
| T3 (UI) | T2 | T6 | T5 |
| T4 (Session) | T1 | T5 | T2, T3 |
| T5 (Logout) | T4 | T6 | T3 |
| T6 (E2E) | T2, T3, T5 | None | None |

**Key Insights**:
- **Critical path**: T1 → T2 → T3 → T6 (longest sequence)
- **Parallel work**: T2 and T4 can run simultaneously after T1
- **Bottleneck**: T1 must complete before anything else starts

---

## Step 3.5: External Dependencies

**Libraries and Services**:
- OAuth provider (Google, GitHub, etc.)
- JWT library for token management
- Database migration tool
- Testing framework

**Document**:
```markdown
External Dependencies:
- Google OAuth API (requires client ID/secret)
- jsonwebtoken library (already in package.json)
- Database migration framework (already exists)
- E2E testing: Playwright (already configured)
```

---

## Step 3.6: Cross-Team Dependencies

**If Applicable**:
- Waiting for API from another team
- Requires infrastructure/DevOps setup
- Design assets not yet available

**Document Explicitly**:
```markdown
Blockers:
- Design team: Need OAuth button mockups (estimated: 2 days)
- DevOps: OAuth credentials in production (estimated: 1 day)
```

---

## Step 3.7: Circular Dependency Detection

**Check for Cycles**:
```
T1 → T2 → T3 → T1  ❌ Circular!
```

**Resolution**:
- Break cycle by identifying which dependency is optional
- Restructure tasks to eliminate cycle
- Example: T3 doesn't actually need T1 output, just T2

---

## Output of Phase 3

**Data Structure**:
```
File Dependencies:
  Upstream: [Libraries, utils we depend on]
  Downstream: [Code that depends on us]

Task Dependencies:
  Graph: T1 → T2 → T3 → T6
         T1 → T4 → T5 ─┘
  Critical Path: [T1, T2, T3, T6]
  Parallel Opportunities: [(T2, T4), (T3, T5)]

External Dependencies: [Libraries, services, teams]
```

**Article I Compliance**:
- ✓ Intelligence queries executed before assumptions
- ✓ File:line evidence in dependency docs
- ✓ Token-efficient discovery process

**Proceed to Phase 4**: Validate Plan

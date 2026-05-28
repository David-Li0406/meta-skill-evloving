---
name: flight-research
description: Temporal research for dependencies and domain validation. Validates package versions, discovers issues, updates landmines. Also validates .flight domain files against current API documentation. Use for existing projects, mid-project dependency additions, domain file validation, or when /flight-prd --no-research was used.
---

## ⚠️ EXECUTION RULES (MANDATORY)

1. **EXECUTE EACH STEP** - Do not skip steps based on "prior context"
2. **USE TOOLS** - You MUST call Read/Bash tools, not recall from memory
3. **SHOW WORK** - Each step must produce visible tool output
4. **NO SHORTCUTS** - "I already read this" is NOT acceptable

### Anti-Patterns (DO NOT DO THESE)
- ❌ "I already read the domain files earlier"
- ❌ "From earlier analysis..."
- ❌ Summarizing steps without executing them
- ❌ Claiming knowledge from "this conversation"

---

# /flight-research

Temporal research with **input-aware routing**. Handles three input types:

1. **Package Research** - Validates versions, discovers breaking changes, updates landmines
2. **Domain File Validation** - Validates .flight rules against current API documentation
3. **General Questions** - Research any Flight-related topic

## Input Detection (Step 0)

**BEFORE doing anything else**, classify the input:

| Input Pattern | Route To | Example |
|---------------|----------|---------|
| `*.flight` file path | Domain File Validation | `/flight-research api.flight` |
| Package names with optional versions | Package Research | `/flight-research express@5 react@19` |
| Question or topic | General Research | `/flight-research "REST API best practices 2026"` |
| No arguments | Package Research (auto-detect) | `/flight-research` |

**Classification Rules:**
1. If argument ends in `.flight` → Domain File Validation mode
2. If argument looks like `package@version` or known package name → Package Research mode
3. If argument is quoted or contains question words → General Research mode
4. If no arguments → Package Research with auto-detection

---

## Usage

```
/flight-research [input...] [flags]
```

## Arguments

- `$ARGUMENTS` - Can be:
  - Specific packages (e.g., `express@5 react@19`) → Package Research
  - A .flight file path (e.g., `api.flight`, `.flight/domains/clerk.flight`) → Domain Validation
  - A quoted question or topic → General Research
  - Empty → Package Research with auto-detection from package.json

## Flags

| Flag | Behavior | Modes |
|------|----------|-------|
| (none) | Standard research depth | All |
| `--quick` | Check staleness only, no new searches | Package, Domain |
| `--deep` | Thorough research with Firecrawl | All |
| `--include-all` | Include tooling deps (eslint, prettier, @types) | Package |
| `--emit-provenance` | Output schema v2 provenance YAML | Domain |

---

# ROUTE A: Package Research

Use this route when researching npm packages, dependencies, or version compatibility.

**Note:** For new projects, `/flight-prd` runs temporal research automatically (Step 2B). Use this standalone skill for:
- Existing projects needing dependency validation
- Adding new dependencies mid-project
- Re-checking stale landmines (>3 months old)
- After using `/flight-prd --no-research`

## Process

### Step 0: Date Anchor (MANDATORY)

**BEFORE ANY TOOL CALLS**, output:

```
📅 Research Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
```

This anchors ALL subsequent searches. Without this, queries will return stale results.

**Example:**
```
📅 Research Date: January 16, 2026
🔍 Research Window: 2025-01-01 to 2026-01-16
```

---

### Step 1: Identify Dependencies

Detect dependencies in priority order:

1. **$ARGUMENTS** (if provided) - Use exactly what user specified
2. **package.json** - Parse `dependencies` + `devDependencies`
3. **PRD.md** - Extract tech stack from "## Tech Stack" or similar
4. **tasks/*.md** - Grep for `npm install` commands

#### Skip Patterns (Default)

Skip tooling deps unless `--include-all`:

```
@types/*
eslint*
prettier*
*-loader
*-plugin
typescript  (unless explicitly requested)
```

**Heuristic:** If a breaking change would require CODE changes (not just config), research it.

#### Output Step 1:

```markdown
## Dependencies to Research

**Source:** {package.json|PRD.md|args}

| Package | Current | Category |
|---------|---------|----------|
| express | ^5.0.0 | Backend |
| react | ^19.0.0 | Frontend |
| tailwindcss | ^4.0.0 | Styling |

**Skipped (tooling):** eslint, prettier, @types/node
```

---

### Step 2: Check Existing Landmines

If `.flight/known-landmines.md` exists:

1. **Read the "Last Full Review" date**
2. **If >3 months old:** Mark ALL entries as NEEDS_VERIFICATION
3. **Check each entry against dependencies being researched**
4. **Use entries as research STARTING POINTS, not facts**

#### Output Step 2:

```markdown
## Existing Landmines Check

**Last Review:** 2025-10-15 (3+ months ago - treating as unverified)

| Entry | Status | Action |
|-------|--------|--------|
| Express 5.x middleware hang | NEEDS_VERIFICATION | Will re-verify |
| Tailwind v4 PostCSS | NEEDS_VERIFICATION | Will re-verify |
```

If no landmines file exists, note: "No existing landmines file. Will create."

---

### Step 3: Research Each Dependency

For each dependency, run date-anchored searches.

#### 3a. Breaking Changes (GitHub)

```
"{library} breaking changes {YEAR-1}-{YEAR}" site:github.com
```

**Why GitHub first:** Issues surface pain 6-12 months before blog posts.

#### 3b. Migration Guide

```
"{library} v{X} migration guide after:{YEAR-1}-01-01"
```

**Why:** Indicates major version transitions requiring code changes.

#### 3c. Integration Issues (if using scaffold tools)

```
"vite {library} {YEAR}" OR "create-react-app {library} {YEAR}"
```

**Why:** Scaffold tools may install incompatible versions.

#### 3d. Stack Overflow

```
"{library} {framework} after:{YEAR-1}-01-01" site:stackoverflow.com
```

**Why:** Community pain points surface here. Date filter critical.

#### 3e. Context7 Documentation (version-pinned)

```
context7 "{library}@{version}"  # ALWAYS include version
```

**NEVER:** `context7 "{library}"` without version - will get wrong docs.

#### --deep mode only: Firecrawl

If initial searches are inconclusive, use Firecrawl for deep dives:
- Official changelog pages
- GitHub release notes
- Migration guide sites

---

### Step 4: Update Landmines File

Update `.flight/known-landmines.md`:

#### New Issues → Add Entry

```markdown
### {Issue Title}
**Discovered:** {CURRENT_DATE}
**Status:** ACTIVE
**Re-verify After:** {CURRENT_DATE + 6 months}
**Issue:** {description}
**Verify By:** Search "{library} {issue} fixed {YEAR}"
**Solution (if active):** {workaround or version pin}
```

#### Existing Issues → Update Status

- Still valid → Keep as ACTIVE, update "Last Verified"
- Fixed → Change to RESOLVED, note which version fixed it
- Uncertain → Keep as NEEDS_VERIFICATION

#### Update File Header

```markdown
> **Last Full Review:** {CURRENT_DATE}
```

---

### Step 5: Update Existing Files (if they exist)

**Principle:** Update what exists, don't create new artifacts.

#### If `tasks/*.md` exist with `npm install`:

Update version pins:

```diff
- npm install express
+ npm install express@4.21.0  # Pinned - v5.x has middleware issues (see landmines)
```

#### If `PRD.md` exists:

Append to "Known Technical Issues" section (create section if missing):

```markdown
## Known Technical Issues

### Express v5.x Middleware Hang
**Risk:** High
**Issue:** `express.json()` causes silent hangs on POST requests
**Mitigation:** Pin to express@4.21.0 in Task 001
**Source:** [GitHub Issue #5678](url)
```

---

### Step 6: Output Summary

```markdown
## Research Summary

📅 **Research Date:** {CURRENT_DATE}
🔍 **Research Window:** {YEAR-1}-01-01 to {CURRENT_DATE}
📦 **Dependencies Researched:** {count}

### Version Recommendations

| Package | Latest | Recommended | Reason |
|---------|--------|-------------|--------|
| express | 5.1.0 | 4.21.0 | v5.x middleware hang |
| react | 19.0.0 | 19.0.0 | Stable |
| tailwindcss | 4.0.0 | 3.4.0 | v4 requires PostCSS changes |

### New Landmines Discovered
- Express 5.x: middleware hang (ACTIVE)
- Tailwind 4.x: PostCSS plugin requirement (ACTIVE)

### Landmines Verified Still Active
- (none from previous research)

### Landmines Now Resolved
- React 18 hydration bug: Fixed in 18.3.0

### Files Updated
- `.flight/known-landmines.md` - 2 entries added
- `tasks/001-setup.md` - version pins updated
- `PRD.md` - Known Technical Issues section added
```

---

## Critical Rules

1. **DATE ANCHOR IS MANDATORY** - Step 0 must happen BEFORE any searches
2. **VERSION-PIN CONTEXT7 QUERIES** - Always `{library}@{version}`
3. **LANDMINES ARE STARTING POINTS** - Never trust without re-verification
4. **UPDATE, DON'T CREATE** - Only modify existing files
5. **SKIP TOOLING BY DEFAULT** - Focus on decision dependencies
6. **PREFER OFFICIAL SOURCES** - GitHub releases > official docs > Stack Overflow > blog posts

---

## Tool Usage

| Tool | When | Query Format |
|------|------|--------------|
| Web Search | Always (primary) | `"{lib} breaking changes {YEAR-1}-{YEAR}"` |
| Context7 | Docs lookup | `"{lib}@{version}"` (versioned!) |
| Firecrawl | --deep mode only | Changelog URLs, release notes |
| Read | Check existing files | package.json, landmines.md, PRD.md |
| Edit | Update task files | Version pins |

---

## When to Use

| Situation | Use This? |
|-----------|-----------|
| New project via `/flight-prd` | No → `/flight-prd` does this automatically |
| `/flight-prd --no-research` was used | Yes - run standalone to validate deps |
| Adding new dependencies to existing project | Yes |
| Resuming work on stale project (>3 months) | Yes - use `--quick` first |
| Mid-project dependency additions | Yes - with specific packages |
| Already know exact versions needed | No |
| Only changing internal code (no new deps) | No |

---

## Workflow Integration

### New Project (automatic)

```
/flight-prd "my app idea"
  → Step 2B runs temporal research automatically
  → Outputs PRD.md, tasks/, known-landmines.md
  → Versions already pinned in task files

/flight-prime tasks/001-*.md
  → Begin implementation
```

### Existing Project, New Dependencies

```
/flight-research express@5 mongodb@7
  → Researches specific deps
  → Updates landmines
  → Updates existing task files (if any)
```

### Stale Project (>3 months since last work)

```
/flight-research --quick
  → Checks landmine staleness
  → Flags what needs re-verification

/flight-research
  → Full re-verification
```

### After /flight-prd --no-research

```
/flight-prd "my app idea" --no-research
  → Fast output, no temporal validation

/flight-research
  → Standalone research before implementation
```

---

## Next Step (Package Research)

After standalone research completes:

```
/flight-prime tasks/001-*.md
```

| Response | Action |
|----------|--------|
| `prime` or `p` | Proceed to `/flight-prime tasks/001-*.md` |
| `deep` | Re-run with `--deep` for more thorough research |

---

# ROUTE B: Domain File Validation

Use this route when validating a `.flight` domain file against current API documentation.

**Purpose:** Validates that domain rules are still accurate by researching the external APIs, frameworks, or standards they reference. Outputs schema v2 provenance metadata.

**When to use:**
- Before trusting an existing `.flight` file for code generation
- When `next_audit_due` date has passed
- After major version releases of referenced APIs
- When compiler warns about stale rules

## Process (Domain Validation)

### Step D0: Date Anchor (MANDATORY)

**BEFORE ANY TOOL CALLS**, output:

```
📅 Validation Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
📄 Domain File: {file_path}
```

---

### Step D1: Parse Domain File

Read and analyze the `.flight` file:

1. **Read the file** using Read tool
2. **Extract metadata**: domain name, version, schema_version
3. **Extract existing provenance** (if schema v2): last_full_audit, sources_consulted
4. **List all rules** with their IDs, titles, and current provenance (if any)
5. **Identify external references**: APIs, RFCs, frameworks, libraries mentioned

#### Output Step D1:

```markdown
## Domain Analysis

**File:** {file_path}
**Domain:** {domain_name}
**Version:** {version}
**Schema Version:** {schema_version | "1 (no provenance)"}
**Last Audit:** {last_full_audit | "Never"}

### Rules to Validate

| ID | Title | Last Verified | Confidence | Needs Re-verify |
|----|-------|---------------|------------|-----------------|
| N1 | Verbs in URIs | 2025-06-01 | high | Yes (>6mo) |
| N2 | 200 OK Error | Never | - | Yes (new) |

### External References Detected

| Reference | Type | Rules Using |
|-----------|------|-------------|
| RFC 9110 | Standard | M1, M2 |
| RFC 9457 | Standard | M3 |
| OWASP API Security | Guide | N5, N8 |
| Express.js | Framework | Examples |
```

---

### Step D2: Research External References

For each external reference, verify current accuracy:

#### 2a. RFCs and Standards

```
"{RFC number} current status {YEAR}"
"{standard name} latest version {YEAR}"
```

**Check for:** Superseded standards, errata, new versions

#### 2b. API Documentation

```
"{API name} documentation {YEAR}"
"{API name} breaking changes {YEAR}"
```

**Use Context7** for framework/library docs (version-pinned!)

#### 2c. Security Guidelines

```
"{guideline} updates {YEAR}" site:owasp.org
"{security topic} best practices {YEAR}"
```

#### 2d. Deep Dive (--deep mode)

Use Firecrawl on:
- Official documentation sites
- RFC text (for exact quotes)
- API reference pages

---

### Step D3: Validate Each Rule

For each mechanical rule, verify:

1. **Is the rule still accurate?** Does current documentation support it?
2. **Is the pattern still correct?** Has the API changed syntax?
3. **Are examples still valid?** Do good/bad examples reflect current reality?
4. **Is there new information?** Updates that should modify the rule?

#### Output Step D3:

```markdown
## Rule Validation Results

### N1: Verbs in URIs
**Status:** ✅ VERIFIED
**Confidence:** high
**Sources Found:**
- RFC 9110 Section 4.2.1: "URIs identify resources..."
- Microsoft REST Guidelines: "Use nouns for resources"
**Notes:** Rule is accurate. No changes needed.

### N5: Sensitive Data in Query Strings
**Status:** ⚠️ UPDATE RECOMMENDED
**Confidence:** medium
**Sources Found:**
- OWASP API Security Top 10 2023: Now explicitly covers API keys
**Recommended Change:** Add `client_secret` to pattern

### M3: Error Response Format
**Status:** 🔄 NEEDS UPDATE
**Confidence:** high
**Sources Found:**
- RFC 9457 supersedes RFC 7807 (2023)
**Required Change:** Update references from RFC 7807 to RFC 9457
```

---

### Step D4: Generate Provenance Output

If `--emit-provenance` flag is set, output schema v2 provenance YAML:

```yaml
## Provenance Output (copy to .flight file)

# Add to domain level:
provenance:
  last_full_audit: "{CURRENT_DATE}"
  audited_by: "flight-research"
  next_audit_due: "{CURRENT_DATE + 6 months}"

  sources_consulted:
    - url: "https://www.rfc-editor.org/rfc/rfc9110"
      accessed: "{CURRENT_DATE}"
      note: "HTTP Semantics"
    - url: "https://www.rfc-editor.org/rfc/rfc9457"
      accessed: "{CURRENT_DATE}"
      note: "Problem Details for HTTP APIs"
    # ... additional sources

# Add to each validated rule:
# N1:
#   provenance:
#     last_verified: "{CURRENT_DATE}"
#     confidence: high
#     re_verify_after: "{CURRENT_DATE + 12 months}"
#     sources:
#       - url: "..."
#         accessed: "{CURRENT_DATE}"
#         quote: "exact quote from source"
```

---

### Step D5: Output Summary (Domain Validation)

```markdown
## Domain Validation Summary

📅 **Validation Date:** {CURRENT_DATE}
📄 **Domain:** {domain_name}
📊 **Rules Validated:** {count}

### Validation Results

| Status | Count | Rules |
|--------|-------|-------|
| ✅ Verified | 18 | N1, N2, N3, M1, M2, ... |
| ⚠️ Update Recommended | 3 | N5, S3, S12 |
| 🔄 Needs Update | 2 | M3, M8 |
| ❌ Invalid/Outdated | 0 | - |

### Recommended Actions

1. **M3:** Update RFC reference from 7807 to 9457
2. **N5:** Add `client_secret` to sensitive data pattern
3. **S12:** Update hardcoded URL examples

### Provenance Status

- **Schema v2 Ready:** {Yes|No - needs migration}
- **Provenance Output:** {Generated|Use --emit-provenance}

### Next Steps

| Response | Action |
|----------|--------|
| `apply` | Update the .flight file with provenance |
| `compile` | Run flight-domain-compile after updates |
| `skip` | Note findings for manual update later |
```

---

# ROUTE C: General Research

Use this route for general Flight-related research questions.

## Process (General Research)

### Step G0: Date Anchor (MANDATORY)

```
📅 Research Date: {CURRENT_DATE}
🔍 Research Window: {YEAR-1}-01-01 to {CURRENT_DATE}
❓ Topic: {quoted question or topic}
```

### Step G1: Research Topic

Use appropriate tools based on topic:

| Topic Type | Primary Tool | Query Format |
|------------|--------------|--------------|
| Best practices | Web Search | `"{topic} best practices {YEAR}"` |
| API standards | Web Search + Firecrawl | `"{standard} specification"` |
| Framework patterns | Context7 | `"{framework}@{version}"` |
| Security | Web Search | `"{topic} security" site:owasp.org` |

### Step G2: Synthesize Findings

Output findings with:
- **Date context** - When was this information published?
- **Source quality** - Official docs > RFCs > guides > blog posts
- **Applicability** - How does this apply to Flight domains?

### Step G3: Recommend Domain Updates

If research reveals information relevant to existing domains:

```markdown
## Domain Impact

| Domain | Potential Update | Priority |
|--------|------------------|----------|
| api.flight | New status code guidance | Medium |
| security.flight | Updated OWASP Top 10 | High |
```

---

## Notes

- Research is TEMPORAL - findings have expiration dates
- The landmines file is institutional memory, not gospel
- Date anchoring prevents the #1 cause of stale research
- When in doubt, re-verify with fresh searches
- Domain validation produces schema v2 provenance for traceability
- Always version-pin Context7 queries: `{library}@{version}`

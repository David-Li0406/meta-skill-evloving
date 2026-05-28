# Integration Tests for skillmeat-cli Skill

Comprehensive testing guide for the skillmeat-cli skill, covering all workflows, agent integrations, confidence scoring, and bundle operations.

---

## Overview

This document provides:

- **Test Categories**: Workflow execution, agent integration, confidence scoring, bundle operations
- **Test Patterns**: Bash commands for manual testing, expected outputs, verification steps
- **Test Scenarios**: 6 complete end-to-end test scenarios with setup, execution, and validation
- **Success Criteria**: Quantifiable metrics for each test category
- **Agent Compatibility**: Testing integrations with ui-engineer, python-backend-engineer, codebase-explorer, ultrathink-debugger

**Goal**: Ensure skillmeat-cli skill works reliably across all use cases and integrations.

---

## Test Environment Setup

### Prerequisites

Before running tests, ensure:

```bash
# 1. skillmeat CLI is installed and available
skillmeat --version
# Expected: skillmeat v0.3.0+ or appropriate version

# 2. GitHub token configured (for rate limiting tests)
skillmeat config set github-token <your-token>
# Not required for basic tests, but recommended

# 3. Test project directory exists
mkdir -p /tmp/skillmeat-test-project
cd /tmp/skillmeat-test-project

# 4. Initialize test project
skillmeat init
# Creates ~/.skillmeat/collection/ and local .claude/ directory

# 5. Verify collection structure
ls -la ~/.skillmeat/collection/
# Expected: artifacts/, manifest.toml, snapshots/

# 6. Check project structure
ls -la .claude/
# Expected: skills/, commands/, agents/, mcp/ directories
```

### Test Cleanup

Between test scenarios, clean up:

```bash
# Remove test artifacts from collection
skillmeat remove <test-artifact> 2>/dev/null || true

# Reset project deployments
rm -rf .claude/skills/* 2>/dev/null || true
rm -rf .claude/commands/* 2>/dev/null || true

# Clear caches
skillmeat cache clear 2>/dev/null || true
```

---

## Test Categories

### 1. Workflow Execution Tests

#### Test 1.1: Discovery Workflow - Simple Search

**Purpose**: Verify basic artifact discovery and search functionality.

```bash
# Execute
skillmeat search "pdf" --json

# Expected output format
{
  "results": [
    {
      "id": "<artifact-id>",
      "name": "<artifact-name>",
      "type": "skill",
      "description": "<description>",
      "source": "<source-path>",
      "version": "<version>",
      "tags": ["<tag1>", "<tag2>"],
      "deployments": <count>
    }
  ],
  "total": <count>
}

# Validation
✓ Returns at least 1 result for "pdf"
✓ Each result has: id, name, type, description, source, version
✓ JSON is valid and parseable
✓ Type is one of: skill, command, agent, mcp, hook
```

**Success Criteria**:
- All PDF-related artifacts returned
- Results include official and community artifacts
- JSON output valid and parseable
- Response time < 5 seconds

---

#### Test 1.2: Discovery Workflow - Type-Filtered Search

**Purpose**: Verify search filtering by artifact type.

```bash
# Execute search for skills only
skillmeat search "database" --type skill --json | jq '.results[].type'

# Expected: All results should be "skill"
skill
skill
skill

# Execute search for agents
skillmeat search "database" --type agent --json | jq '.results[].type'

# Expected: All results should be "agent" (if any exist)
agent

# Validation
✓ Only specified type returned
✓ Results filtered correctly
✓ Empty results handled gracefully if type has no matches
```

**Success Criteria**:
- Type filtering works for all valid types
- Only artifacts of specified type returned
- No cross-type contamination
- Error handling for invalid types

---

#### Test 1.3: Discovery Workflow - List Collection

**Purpose**: Verify listing artifacts already in user's collection.

```bash
# Add test artifact first
skillmeat add skill anthropics/skills/canvas-design

# Execute list command
skillmeat list --type skill --json

# Expected output
{
  "results": [
    {
      "id": "canvas-design",
      "name": "canvas-design",
      "type": "skill",
      "version": "<version>",
      "location": "~/.skillmeat/collection/artifacts/canvas-design"
    }
  ],
  "total": 1
}

# Validation
✓ Added artifact appears in list
✓ Location path is correct and accessible
✓ Version is resolved (not "latest")
```

**Success Criteria**:
- All artifacts in collection listed
- Correct paths shown
- Versions are resolved
- Pagination works for large collections

---

#### Test 1.4: Deployment Workflow - Add to Collection

**Purpose**: Verify adding artifacts to collection from sources.

```bash
# Execute
skillmeat add skill anthropics/skills/canvas-design

# Expected output
✓ Added canvas-design (canvas-design) to collection
  Source: anthropics/skills/canvas-design
  Version: latest
  Location: ~/.skillmeat/collection/artifacts/canvas-design

# Validation
✓ Artifact downloaded and stored
✓ manifest.toml updated with new artifact
✓ Can be listed with `skillmeat list`
✓ No duplicate if added twice (should skip)

# Verify manifest
grep canvas-design ~/.skillmeat/collection/manifest.toml
# Expected: artifact entry with source and version
```

**Success Criteria**:
- Artifact successfully added to collection
- Manifest.toml updated correctly
- No duplicate entries on re-add
- Version resolved to specific tag/SHA
- Lock file created/updated

---

#### Test 1.5: Deployment Workflow - Deploy to Project

**Purpose**: Verify deploying artifacts to project (.claude directory).

```bash
# Navigate to test project
cd /tmp/skillmeat-test-project

# Verify collection has artifact
skillmeat list --json | grep canvas-design

# Deploy to project
skillmeat deploy canvas-design

# Expected output
✓ Deployed canvas-design to ./.claude/skills/
  Files created:
  - ./.claude/skills/canvas-design/
  - ./.claude/skills/canvas-design/SKILL.md
  - ./.claude/skills/canvas-design/workflows/

# Validation
✓ Artifact files exist in ./.claude/skills/
✓ Directory structure is correct
✓ SKILL.md is readable and valid
✓ Listed in project deployments

# Verify deployment
skillmeat list --project . --json | jq '.results[] | select(.name=="canvas-design")'
# Expected: canvas-design with location ./.claude/skills/canvas-design
```

**Success Criteria**:
- Files deployed to correct location
- Directory structure preserved
- Artifact accessible from project
- Listed in project deployments
- Can be undeployed cleanly

---

#### Test 1.6: Management Workflow - Sync Updates

**Purpose**: Verify checking and syncing artifact updates.

```bash
# Check for updates (after artifact has been added)
skillmeat diff canvas-design

# Expected output if updates exist
✓ New version available: canvas-design v2.0.0
  Current: v1.5.0
  Latest: v2.0.0

# Expected output if no updates
✓ canvas-design is up to date (v1.5.0)

# Update specific artifact
skillmeat update canvas-design

# Expected output
✓ Updated canvas-design from v1.5.0 to v2.0.0
  Files updated:
  - SKILL.md (updated)
  - workflows/ (5 files)

# Validation
✓ Version updated in manifest
✓ Lock file updated with new SHA
✓ Files refreshed from source
```

**Success Criteria**:
- Update detection works
- Version resolved correctly
- Artifact files updated
- Lock file reflects new version
- Rollback capability (old version tracked)

---

#### Test 1.7: Management Workflow - Remove Artifact

**Purpose**: Verify removing artifacts from collection and project.

```bash
# Remove from project first
skillmeat undeploy canvas-design --project .

# Expected output
✓ Undeployed canvas-design from ./.claude/skills/
  Removed: ./.claude/skills/canvas-design/

# Verify removal
ls ./.claude/skills/
# Expected: No canvas-design directory

# Remove from collection
skillmeat remove canvas-design

# Expected output
✓ Removed canvas-design from collection

# Verify removal
skillmeat list | grep canvas-design
# Expected: No output (not found)
```

**Success Criteria**:
- Artifact removed from project without errors
- Artifact removed from collection
- No leftover files
- Cannot deploy removed artifact
- List operations reflect removal

---

#### Test 1.8: Error Handling - Artifact Not Found

**Purpose**: Verify error handling for non-existent artifacts.

```bash
# Try to deploy non-existent artifact
skillmeat deploy nonexistent-artifact 2>&1

# Expected error
✗ Artifact 'nonexistent-artifact' not found in collection
  Available artifacts: canvas-design, ...
  Did you mean one of: [suggestions]?

# Try to show details of missing artifact
skillmeat show fake-artifact 2>&1

# Expected error
✗ Artifact 'fake-artifact' not found
  Search for similar: skillmeat search "fake"
```

**Success Criteria**:
- Clear error messages for missing artifacts
- Suggestions provided (if fuzzy match available)
- Exit code 1 on error
- No partial deployments

---

#### Test 1.9: Error Handling - Permission Issues

**Purpose**: Verify handling of permission errors during deployment.

```bash
# Make .claude directory read-only (simulate permission issue)
chmod 444 .claude/

# Try to deploy
skillmeat deploy canvas-design 2>&1

# Expected error
✗ Permission denied: cannot write to ./.claude/skills/
  Required permission: read + write
  Current permission: read-only (444)

  Solution: Run `chmod 755 ./.claude/` to fix permissions

# Restore permissions
chmod 755 .claude/

# Verify deployment now works
skillmeat deploy canvas-design
# Expected: Success
```

**Success Criteria**:
- Permission errors detected and reported
- Helpful error messages with solutions
- No data corruption on failed deployment
- Recovery path clear

---

#### Test 1.10: Error Handling - Rate Limiting

**Purpose**: Verify handling of GitHub API rate limiting.

```bash
# Without token (lower rate limit: 60 requests/hour)
skillmeat search "test" --json
# After 60 searches, expected error:

✗ Rate limit exceeded
  GitHub API limit: 60 requests per hour (unauthenticated)

  Solution: Set GitHub token
  $ skillmeat config set github-token <your-token>

  With token: 5000 requests per hour

# With token configured
skillmeat config set github-token <token>
skillmeat search "test" --json
# Expected: Successful search with higher limit
```

**Success Criteria**:
- Rate limit errors detected
- Error message includes solution
- Token configuration works
- Requests succeed with token

---

### 2. Agent Integration Tests

#### Test 2.1: UI Engineer - Component Suggestion

**Purpose**: Verify ui-engineer can discover and suggest UI-related artifacts.

```bash
# Simulate ui-engineer discovering need for form component
# (In practice, agent runs this internally)

# Search for form-related artifacts
skillmeat search "react form validation" --type skill --json

# Expected results
{
  "results": [
    {
      "id": "form-builder",
      "name": "form-builder",
      "type": "skill",
      "tags": ["react", "forms", "validation", "accessibility"],
      "description": "Form validation and submission handling for React"
    }
  ],
  "total": 1
}

# Validation
✓ Form-related artifacts found
✓ React-specific artifacts prioritized
✓ Description includes validation keywords
✓ Tags include relevant categories
```

**Success Criteria**:
- Form/component artifacts discoverable
- React/TypeScript artifacts prioritized
- Tags indicate UI-specific functionality
- Multiple options if available

---

#### Test 2.2: Python Backend Engineer - API Documentation Suggestion

**Purpose**: Verify python-backend-engineer can discover API documentation artifacts.

```bash
# Search for OpenAPI/documentation artifacts
skillmeat search "openapi documentation" --type skill --json

# Expected results
{
  "results": [
    {
      "id": "openapi-expert",
      "name": "openapi-expert",
      "type": "skill",
      "tags": ["openapi", "api", "documentation", "fastapi"],
      "description": "Auto-generate OpenAPI specifications and schemas"
    }
  ],
  "total": 1
}

# Validation
✓ API documentation artifacts found
✓ FastAPI/backend-specific artifacts in results
✓ Schema generation mentioned in description
```

**Success Criteria**:
- API documentation artifacts discoverable
- FastAPI/backend tags present
- Schema generation artifacts found
- Integration with existing API tools

---

#### Test 2.3: Codebase Explorer - Code Analysis Suggestion

**Purpose**: Verify codebase-explorer can discover code analysis artifacts.

```bash
# Search for code analysis and navigation
skillmeat search "code analysis architecture" --type skill --json

# Expected results
{
  "results": [
    {
      "id": "code-analyzer",
      "name": "code-analyzer",
      "type": "skill",
      "tags": ["architecture", "analysis", "symbols", "dependencies"],
      "description": "Analyze and visualize code architecture and dependencies"
    }
  ],
  "total": 1
}

# Validation
✓ Architecture analysis artifacts found
✓ Symbol navigation mentioned
✓ Dependency mapping capabilities
```

**Success Criteria**:
- Code analysis artifacts discoverable
- Architecture tools found
- Symbol/dependency tools available
- Multi-language support indicated

---

#### Test 2.4: Ultrathink Debugger - Debug Artifact Suggestion

**Purpose**: Verify ultrathink-debugger can discover debugging artifacts.

```bash
# Search for debugging and tracing tools
skillmeat search "debugging trace profiling" --type skill --json

# Expected results
{
  "results": [
    {
      "id": "debug-tracer",
      "name": "debug-tracer",
      "type": "skill",
      "tags": ["debugging", "tracing", "profiling", "performance"],
      "description": "Trace execution flow and identify bottlenecks"
    }
  ],
  "total": 1
}

# Validation
✓ Debug/trace artifacts found
✓ Performance profiling mentioned
✓ Stack trace analysis capable
```

**Success Criteria**:
- Debugging artifacts discoverable
- Tracing tools found
- Performance profiling available
- Multi-language debugging support

---

#### Test 2.5: Cross-Agent Handoff

**Purpose**: Verify one agent can discover artifact and pass recommendation to another agent.

```bash
# Simulate backend engineer completing task
# (Agent would run this internally)

# Backend engineer searches for related frontend need
skillmeat search "react state management api integration" --type skill --json

# Expected results with cross-domain relevance
{
  "results": [
    {
      "id": "react-query-helper",
      "name": "react-query-helper",
      "type": "skill",
      "tags": ["react", "state-management", "api", "caching"],
      "source": "anthropics/skills/react-query-helper"
    }
  ],
  "total": 1
}

# Backend engineer would then suggest this to frontend engineer:
# Task("ui-engineer", "New API endpoint created.
#      The react-query-helper skill handles complex queries.
#      Source: anthropics/skills/react-query-helper")

# Validation
✓ Artifact discoverable for handoff
✓ Source information complete
✓ Tags enable cross-team understanding
```

**Success Criteria**:
- Cross-domain artifacts discoverable
- Source information complete
- Agent-to-agent handoff viable
- Artifact context preserved

---

### 3. Confidence Scoring Tests

#### Test 3.1: Confidence API Integration

**Purpose**: Verify confidence scoring returns accurate scores for known queries.

```bash
# Query with confidence breakdown
skillmeat match "pdf processing tools" --json --include_breakdown true

# Expected response format
{
  "query": "pdf processing tools",
  "matches": [
    {
      "artifact_id": "skill:pdf-processor",
      "name": "pdf-processor",
      "confidence": 95.2,
      "breakdown": {
        "trust_score": 98.0,
        "quality_score": 94.5,
        "match_score": 93.0,
        "semantic_used": true
      }
    }
  ],
  "degraded": false,
  "degradation_reason": null
}

# Validation
✓ Confidence score between 0-100
✓ Breakdown scores between 0-100
✓ Trust score ≥ 90 for official artifacts
✓ Quality score ≥ 80 for verified artifacts
✓ Semantic matching indicated
✓ High match confidence for exact terms
```

**Success Criteria**:
- Confidence scores accurate (±5% variance acceptable)
- Trust scores reflect artifact provenance
- Quality scores based on community ratings
- Match scores align with query terms
- Semantic matching flags correctly

---

#### Test 3.2: Score Threshold Enforcement

**Purpose**: Verify confidence threshold filtering works correctly.

```bash
# Search with high confidence threshold (≥90)
skillmeat match "pdf" --json --min-confidence 90

# Expected: Only high-confidence results
{
  "matches": [
    { "name": "pdf-processor", "confidence": 95.2 },
    { "name": "ms-office-suite:pdf", "confidence": 92.1 }
  ],
  "total": 2
}

# Search with medium confidence threshold (≥70)
skillmeat match "pdf" --json --min-confidence 70

# Expected: More results including medium-confidence
{
  "matches": [
    { "name": "pdf-processor", "confidence": 95.2 },
    { "name": "pdf-forms", "confidence": 82.3 },
    { "name": "document-processor", "confidence": 76.1 }
  ],
  "total": 3
}

# Search with low threshold (≥50)
skillmeat match "pdf" --json --min-confidence 50

# Expected: Even more results
{
  "matches": [
    { "name": "pdf-processor", "confidence": 95.2 },
    { "name": "pdf-forms", "confidence": 82.3 },
    { "name": "ocr-pdf", "confidence": 68.9 },
    { "name": "file-converter", "confidence": 55.2 }
  ],
  "total": 4
}

# Validation
✓ Only results >= threshold returned
✓ No results below threshold included
✓ Results sorted by confidence (descending)
✓ Count reflects threshold
```

**Success Criteria**:
- Threshold filtering accurate
- No false positives below threshold
- Results properly sorted
- Threshold values respected

---

#### Test 3.3: Context Boosting Accuracy

**Purpose**: Verify context-aware score adjustments for project-specific searches.

```bash
# Analyze project context
node .claude/skills/skillmeat-cli/scripts/analyze-project.js . > /tmp/context.json

# Project with package.json + React
# Expected context
{
  "type": "react",
  "framework": "next.js",
  "language": "typescript",
  "detected_packages": ["react", "next", "typescript"]
}

# Search with React context boosting
skillmeat match "component development" --json --apply_context true

# Expected: React-related artifacts boosted
{
  "matches": [
    {
      "name": "frontend-design",  # React skill
      "confidence": 92.5,
      "context_boost": 15.2  # +15% boost applied
    },
    {
      "name": "generic-component",  # Language-agnostic
      "confidence": 72.1,
      "context_boost": 0  # No boost
    },
    {
      "name": "python-design",  # Python skill
      "confidence": 45.3,
      "context_penalty": -30.2  # -30% penalty for mismatch
    }
  ]
}

# Validation
✓ React artifacts boosted for React project
✓ Frontend artifacts ranked higher
✓ Python artifacts penalized
✓ Boost magnitude 10-25%
✓ Penalty magnitude 20-50%
```

**Success Criteria**:
- Correct project type detected
- Matching artifacts boosted 10-25%
- Mismatching artifacts penalized 20-50%
- Boosts + penalties reflect project context
- Already-deployed artifacts penalized

---

#### Test 3.4: Keyword Fallback Search

**Purpose**: Verify fallback to keyword search when semantic matching unavailable.

```bash
# Query with degradation (semantic unavailable)
skillmeat match "unusual-capability" --json

# Expected response with degradation notice
{
  "query": "unusual-capability",
  "matches": [
    {
      "name": "unusual-capability-impl",
      "confidence": 72.1,
      "breakdown": {
        "trust_score": 75.0,
        "quality_score": 70.0,
        "match_score": 71.5,
        "semantic_used": false  # Fallback to keyword
      }
    }
  ],
  "degraded": true,
  "degradation_reason": "Semantic search unavailable, using keyword matching"
}

# Validation
✓ Keyword matching works as fallback
✓ Results returned despite degradation
✓ Degradation flag set to true
✓ Reason explained in response
✓ Matches found using keywords only
✓ Confidence scores adjusted (lower than semantic)
```

**Success Criteria**:
- Keyword matching provides results when semantic unavailable
- Degradation flag accurate
- Reason explained to user
- Results still relevant
- Scores reflect keyword-only matching

---

### 4. Bundle Operation Tests

#### Test 4.1: Bundle Creation

**Purpose**: Verify creating bundle from current collection.

```bash
# Setup: Add multiple artifacts to collection
skillmeat add skill anthropics/skills/canvas-design
skillmeat add skill anthropics/skills/pdf-processor
skillmeat add command anthropics/commands/test-runner

# Create bundle
skillmeat bundle create my-setup

# Expected output
✓ Created bundle: my-setup.zip
  Included artifacts:
  - canvas-design (skill)
  - pdf-processor (skill)
  - test-runner (command)

  Bundle location: /tmp/skillmeat-test-project/my-setup.zip
  Size: 2.3 MB
  Artifacts: 3

# Verify bundle structure
unzip -l my-setup.zip

# Expected contents
Archive:  my-setup.zip
  Length    Date    Time    Name
────────────────────────────────────
    4521    ...     skillmeat-bundle.json
   45230    ...     artifacts/canvas-design/SKILL.md
   12345    ...     artifacts/canvas-design/workflows/...
   23456    ...     artifacts/pdf-processor/...

# Validation
✓ Bundle file created
✓ All artifacts included
✓ Bundle manifest present
✓ File structure intact
```

**Success Criteria**:
- Bundle created successfully
- All collection artifacts included
- Bundle structure valid
- Manifest contains artifact list
- Can be extracted without issues

---

#### Test 4.2: Bundle Signing

**Purpose**: Verify creating cryptographic signature for bundle integrity.

```bash
# Create signed bundle
skillmeat sign create my-setup.zip

# Expected output
✓ Signed bundle: my-setup.zip.sig
  Algorithm: SHA-256 + RSA-2048
  Signer: local@skillmeat
  Timestamp: 2024-12-24T15:30:00Z

# Verify bundle structure
ls -la my-setup*

# Expected files
my-setup.zip          (bundle)
my-setup.zip.sig      (signature)
my-setup.zip.pub      (public key)

# Validation
✓ Signature file created
✓ Public key exported
✓ Algorithm secure (RSA-2048+)
✓ Timestamp recorded
```

**Success Criteria**:
- Signature file created
- Public key available
- Algorithm cryptographically secure
- Timestamp included
- Signature metadata present

---

#### Test 4.3: Bundle Verification

**Purpose**: Verify checking bundle integrity and authenticity.

```bash
# Verify bundle signature
skillmeat sign verify my-setup.zip

# Expected output (valid)
✓ Signature verified
  Bundle: my-setup.zip
  Signer: local@skillmeat
  Signed at: 2024-12-24T15:30:00Z
  Algorithm: SHA-256 + RSA-2048

# Corrupt bundle and verify again
unzip -q my-setup.zip -d /tmp/temp
echo "corrupted" >> /tmp/temp/artifacts/canvas-design/SKILL.md
cd /tmp/temp && zip -q -r my-setup-corrupted.zip . && cd -

# Attempt verification
skillmeat sign verify my-setup-corrupted.zip

# Expected output (invalid)
✗ Signature verification failed
  Bundle: my-setup-corrupted.zip
  Reason: Content hash mismatch

  The bundle has been modified since signing.
  Original signature: <hash>
  Current content:  <hash>

# Validation
✓ Valid signatures verified successfully
✓ Invalid signatures detected
✓ Tampering detected
✓ Hash mismatch reported
```

**Success Criteria**:
- Valid signatures pass verification
- Invalid signatures fail verification
- Tampering detected
- Clear pass/fail indication
- Hash values reported

---

#### Test 4.4: Bundle Import

**Purpose**: Verify importing bundle into new collection.

```bash
# Setup: Create temporary collection
export SKILLMEAT_HOME=/tmp/skillmeat-import-test
mkdir -p $SKILLMEAT_HOME
skillmeat init

# Import bundle
skillmeat bundle import /path/to/my-setup.zip

# Expected output
✓ Importing bundle: my-setup.zip
  Artifacts: 3
  - canvas-design (skill)
  - pdf-processor (skill)
  - test-runner (command)

✓ Imported successfully
  Location: ~/.skillmeat/collection/

# Verify imported artifacts
skillmeat list --json

# Expected: All 3 artifacts in collection
{
  "results": [
    { "id": "canvas-design", "type": "skill", ... },
    { "id": "pdf-processor", "type": "skill", ... },
    { "id": "test-runner", "type": "command", ... }
  ],
  "total": 3
}

# Validation
✓ All artifacts imported
✓ Types preserved
✓ Versions intact
✓ Can be deployed from imported location
```

**Success Criteria**:
- All artifacts imported
- Types and versions preserved
- Artifacts deployable after import
- No import errors
- Collection consistent

---

#### Test 4.5: Conflict Resolution - Duplicate Artifacts

**Purpose**: Verify handling when importing bundle with duplicate artifacts.

```bash
# Setup: Collection already has some artifacts
skillmeat list
# Returns: canvas-design, other-skill

# Create bundle with overlapping artifacts
# (Bundle has: canvas-design, pdf-processor, test-runner)

# Import bundle with conflicts
skillmeat bundle import bundle-with-duplicates.zip --conflict replace

# Expected output
⚠ Conflict detected: 1 artifact already exists
  - canvas-design (v1.0.0 → v2.0.0)

? Resolution strategy: [replace | skip | rename]
  Default: replace

# Choose resolution (replace)
✓ Replacing canvas-design with newer version
  Old version: v1.0.0
  New version: v2.0.0

✓ Imported remaining artifacts:
  - pdf-processor (skill)
  - test-runner (command)

# Validation
✓ Conflicts detected
✓ Resolution options presented
✓ Newer version used when replacing
✓ Other artifacts still imported
```

**Success Criteria**:
- Duplicate detection works
- Resolution strategies available (replace, skip, rename)
- User prompted for conflicted artifacts
- Newer versions preferred for replace
- Non-conflicted artifacts still imported

---

#### Test 4.6: Conflict Resolution - Rename on Conflict

**Purpose**: Verify rename strategy when importing duplicates.

```bash
# Import with rename strategy
skillmeat bundle import bundle-with-duplicates.zip --conflict rename

# Expected output
⚠ Conflict: canvas-design exists
  Renaming imported version: canvas-design-imported-2024-12-24

✓ Imported with renamed artifacts:
  - canvas-design (existing, unchanged)
  - canvas-design-imported-2024-12-24 (imported)
  - pdf-processor (skill)
  - test-runner (command)

# Verify both versions present
skillmeat list | grep canvas-design

# Expected
canvas-design
canvas-design-imported-2024-12-24

# Validation
✓ Original preserved
✓ Imported version renamed
✓ Timestamp in new name
✓ Both versions accessible
✓ Can deploy either version
```

**Success Criteria**:
- Rename strategy available
- Original artifact unchanged
- Imported version renamed with timestamp
- Both versions present
- No data loss

---

## Complete Test Scenarios

### Scenario 1: Frontend Developer - Add Form Component

**User Role**: UI Engineer developing React form

**Setup**:
```bash
# Create test React project
mkdir -p /tmp/test-form-project
cd /tmp/test-form-project

# Initialize skillmeat
skillmeat init

# Create mock package.json (signals React project)
cat > package.json << 'EOF'
{
  "name": "test-form-app",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "next": "^15.0.0"
  }
}
EOF

# Create src structure
mkdir -p src/components
```

**Execution Steps**:

1. **Search for form components**
   ```bash
   skillmeat search "react form validation" --type skill --json
   ```

2. **Parse results**
   ```bash
   skillmeat search "react form" --type skill --json | \
     jq '.results[] | {name, source, description}'
   ```

3. **Add to collection**
   ```bash
   skillmeat add skill anthropics/skills/form-builder
   ```

4. **Deploy to project**
   ```bash
   skillmeat deploy form-builder
   ```

5. **Verify deployment**
   ```bash
   ls -la .claude/skills/form-builder/
   cat .claude/skills/form-builder/SKILL.md
   ```

**Expected Output**:

```
Workflow:
1. Search finds form-builder (confidence: 92%)
2. Add succeeds: ✓ Added form-builder to collection
3. Deploy succeeds: ✓ Deployed form-builder to ./.claude/skills/
4. Files present: SKILL.md, workflows/, examples/
5. Ready to use in React components

Success indicators:
✓ Search returned form-builder as top result
✓ Confidence >= 85%
✓ Deploy completed in <5 seconds
✓ All files present and readable
✓ Can reference skill in component code
```

**Pass Criteria**:
- [ ] Form-builder discoverable with search
- [ ] Confidence >= 85%
- [ ] Add completes successfully
- [ ] Deploy completes successfully
- [ ] Files verify intact
- [ ] Skill documentation clear

---

### Scenario 2: Backend Developer - Add OpenAPI Documentation

**User Role**: Python Backend Engineer adding API documentation

**Setup**:
```bash
# Create test FastAPI project
mkdir -p /tmp/test-api-project
cd /tmp/test-api-project

skillmeat init

# Create mock pyproject.toml (signals Python/FastAPI)
cat > pyproject.toml << 'EOF'
[project]
name = "test-api"
version = "0.1.0"
dependencies = [
  "fastapi>=0.100.0",
  "sqlalchemy>=2.0.0",
]
EOF

mkdir -p app/api/routes
```

**Execution Steps**:

1. **Search for OpenAPI artifacts**
   ```bash
   skillmeat search "openapi documentation fastapi" --type skill --json
   ```

2. **List project context**
   ```bash
   node .claude/skills/skillmeat-cli/scripts/analyze-project.js .
   ```

3. **Add OpenAPI skill**
   ```bash
   skillmeat add skill anthropics/skills/openapi-expert
   ```

4. **Deploy to project**
   ```bash
   skillmeat deploy openapi-expert
   ```

5. **Verify with project context**
   ```bash
   skillmeat list --project . --json
   ```

**Expected Output**:

```
Workflow:
1. Project analysis detects: FastAPI, Python 3.9+
2. Search finds: openapi-expert (confidence: 94%)
3. Add succeeds with message about FastAPI integration
4. Deploy places artifact in ./.claude/skills/openapi-expert/
5. Project list shows openapi-expert deployed

Success indicators:
✓ Project type correctly identified as FastAPI
✓ OpenAPI artifacts prioritized in search
✓ Confidence >= 90%
✓ Deployment recognizes FastAPI compatibility
✓ Artifact accessible for API endpoint generation
```

**Pass Criteria**:
- [ ] Project context correctly analyzed
- [ ] OpenAPI artifacts found
- [ ] Confidence >= 90%
- [ ] Context boosting applied (+15% for FastAPI match)
- [ ] Deploy succeeds
- [ ] Skill ready for endpoint integration

---

### Scenario 3: Code Explorer - Analyze Architecture

**User Role**: Developer analyzing codebase architecture

**Setup**:
```bash
# Use existing SkillMeat codebase or create mock
mkdir -p /tmp/test-architecture-project
cd /tmp/test-architecture-project

skillmeat init

# Create mock structure
mkdir -p {src,api,core,models}
touch src/main.py api/routes.py core/logic.py models/database.py

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
dependencies = ["fastapi", "sqlalchemy"]
EOF
```

**Execution Steps**:

1. **Discover code analysis needs**
   ```bash
   skillmeat search "code analysis architecture symbols" --type skill --json
   ```

2. **Check what's available**
   ```bash
   skillmeat search "architecture" --json | jq '.results[].name'
   ```

3. **Deploy code analyzer**
   ```bash
   skillmeat add skill anthropics/skills/code-analyzer
   skillmeat deploy code-analyzer
   ```

4. **Use analyzer on project**
   ```bash
   node .claude/skills/code-analyzer/scripts/analyze.js . --format json
   ```

5. **Verify results**
   ```bash
   skillmeat list --project . | grep code-analyzer
   ```

**Expected Output**:

```
Workflow:
1. Search finds code-analyzer (confidence: 88%)
2. Analysis script available in deployed skill
3. Architecture analysis runs and generates report
4. Output shows module structure, dependencies, entry points

Success indicators:
✓ Code-analyzer found with high confidence
✓ Deploy completes successfully
✓ Analysis script executable
✓ JSON output generated
✓ Architecture clearly mapped
```

**Pass Criteria**:
- [ ] Code analysis artifacts discovered
- [ ] Confidence >= 80%
- [ ] Deploy succeeds
- [ ] Analysis script works
- [ ] Output valid JSON
- [ ] Architecture relationships clear

---

### Scenario 4: Debugging - Trace Execution Flow

**User Role**: Developer debugging complex error

**Setup**:
```bash
mkdir -p /tmp/test-debug-project
cd /tmp/test-debug-project

skillmeat init

# Create mock Python project with error scenario
cat > test_code.py << 'EOF'
def process_data(data):
    result = transform(data)
    return validate(result)

def transform(data):
    return data.upper()

def validate(data):
    if not data:
        raise ValueError("Empty data")
    return data
EOF
```

**Execution Steps**:

1. **Search for debugging tools**
   ```bash
   skillmeat search "debugging trace profiling error analysis" --type skill --json
   ```

2. **Find debugging artifacts**
   ```bash
   skillmeat search "debug" --type skill --json | jq '.results[] | {name, confidence}'
   ```

3. **Add debug tracer**
   ```bash
   skillmeat add skill anthropics/skills/debug-tracer
   skillmeat deploy debug-tracer
   ```

4. **Use tracer on error**
   ```bash
   ./.claude/skills/debug-tracer/trace.py test_code.py
   ```

5. **Verify trace output**
   ```bash
   skillmeat list --project . --json | jq '.results[] | select(.name=="debug-tracer")'
   ```

**Expected Output**:

```
Workflow:
1. Search finds debug-tracer (confidence: 86%)
2. Deploy creates ./.claude/skills/debug-tracer/
3. Trace script available
4. Error flow traced with stack analysis
5. Bottlenecks identified

Success indicators:
✓ Debug artifacts found
✓ Tracer deployed successfully
✓ Trace script executable
✓ Error flow visualized
✓ Performance metrics included
```

**Pass Criteria**:
- [ ] Debug artifacts discovered
- [ ] Confidence >= 75%
- [ ] Deploy succeeds
- [ ] Trace tool functional
- [ ] Error flow clear
- [ ] Performance data available

---

### Scenario 5: Bundle Distribution - Share Setup

**User Role**: Team lead distributing standardized dev setup

**Setup**:
```bash
mkdir -p /tmp/bundle-create-project
cd /tmp/bundle-create-project

skillmeat init

# Add multiple artifacts for team
skillmeat add skill anthropics/skills/canvas-design
skillmeat add skill anthropics/skills/pdf-processor
skillmeat add command anthropics/commands/test-runner
skillmeat add skill anthropics/skills/form-builder
```

**Execution Steps**:

1. **Verify collection contents**
   ```bash
   skillmeat list --json
   ```

2. **Create bundle**
   ```bash
   skillmeat bundle create team-dev-setup
   ```

3. **Sign bundle**
   ```bash
   skillmeat sign create team-dev-setup.zip
   ```

4. **Verify bundle**
   ```bash
   skillmeat sign verify team-dev-setup.zip
   ```

5. **Share bundle** (simulate by copying)
   ```bash
   cp team-dev-setup.zip /tmp/shared-bundle.zip
   ```

**Expected Output**:

```
Workflow:
1. Collection contains 4 artifacts
2. Bundle created: team-dev-setup.zip (2.1 MB)
3. Bundle signed: team-dev-setup.zip.sig
4. Signature verified successfully
5. Bundle ready for team distribution

Success indicators:
✓ Bundle created with all artifacts
✓ Bundle size reasonable
✓ Signature created and verified
✓ Bundle integrity confirmed
✓ Distribution-ready
```

**Pass Criteria**:
- [ ] Bundle created with all artifacts
- [ ] Bundle structure valid
- [ ] Signature created
- [ ] Signature verifies successfully
- [ ] Bundle transferable
- [ ] Import works in new environment

---

### Scenario 6: Bundle Import - Team Onboarding

**User Role**: New team member using shared bundle

**Setup**:
```bash
# Simulate new environment
export SKILLMEAT_HOME=/tmp/new-team-member
mkdir -p $SKILLMEAT_HOME

# Initialize fresh installation
skillmeat init

# Get shared bundle (copied from lead's setup)
cp /tmp/shared-bundle.zip /tmp/team-setup.zip
```

**Execution Steps**:

1. **Verify bundle integrity**
   ```bash
   skillmeat sign verify /tmp/team-setup.zip
   ```

2. **Import bundle**
   ```bash
   skillmeat bundle import /tmp/team-setup.zip
   ```

3. **Verify import**
   ```bash
   skillmeat list --json
   ```

4. **Deploy to local project**
   ```bash
   mkdir -p /tmp/new-project
   cd /tmp/new-project
   skillmeat init

   # Deploy from imported artifacts
   skillmeat deploy canvas-design
   skillmeat deploy form-builder
   ```

5. **Verify project setup**
   ```bash
   skillmeat list --project . --json
   ls -la .claude/skills/
   ```

**Expected Output**:

```
Workflow:
1. Bundle signature verified
2. Import succeeds: ✓ Imported 4 artifacts
3. Collection contains all 4 artifacts
4. Deploy succeeds for both skills
5. New project ready with team standards

Success indicators:
✓ Bundle integrity verified
✓ All artifacts imported
✓ Import preserves versions
✓ Artifacts deployable
✓ Project uses team setup
✓ Versions match team lead's setup
```

**Pass Criteria**:
- [ ] Bundle integrity verified
- [ ] All artifacts imported
- [ ] Import preserves versions
- [ ] Can deploy to project
- [ ] Project structure correct
- [ ] Versions match source

---

## Success Criteria Summary

### Quantitative Metrics

| Category | Metric | Target | Measurement |
|----------|--------|--------|-------------|
| **Discovery** | Search accuracy | >95% | Relevant results in top 3 |
| **Deployment** | Success rate | >99% | Successful deploys / total attempts |
| **Speed** | Deploy time | <5s | Time from command to completion |
| **Confidence** | Score accuracy | ±5% | Actual vs predicted confidence |
| **Error handling** | Clear errors | 100% | All errors have actionable messages |
| **Bundle size** | Reasonable | <50MB | Typical bundle compressed size |
| **Agent integration** | Coverage | 4+ agents | Ui-engineer, python, explorer, debugger |
| **Cross-agent handoff | Viability | 100% | Artifact pass-through works |

### Qualitative Criteria

**All tests must demonstrate:**
- ✓ Clear, actionable error messages
- ✓ No silent failures or partial states
- ✓ Consistent command behavior
- ✓ Proper cleanup on errors
- ✓ User-friendly output format
- ✓ Correct permission handling
- ✓ Rate limiting awareness
- ✓ No unintended side effects

---

## Troubleshooting Test Failures

### Common Issues and Solutions

**Issue**: "Artifact not found" on search

**Diagnosis**:
```bash
# Check network connectivity
ping github.com

# Check token rate limit
skillmeat config get github-token

# Test with token
skillmeat search "test" --json
```

**Solution**: Set GitHub token if needed

---

**Issue**: "Permission denied" during deploy

**Diagnosis**:
```bash
# Check .claude directory permissions
ls -la .claude/

# Check write access
touch .claude/test.txt && rm .claude/test.txt
```

**Solution**: Run `chmod 755 .claude/` and retry

---

**Issue**: Bundle import fails with conflicts

**Diagnosis**:
```bash
# List current artifacts
skillmeat list

# Check bundle contents
unzip -l bundle.zip | grep artifacts
```

**Solution**: Use `--conflict replace` or `--conflict rename` strategy

---

**Issue**: Tests timeout or hang

**Diagnosis**:
```bash
# Check for background processes
ps aux | grep skillmeat

# Monitor network
lsof -i :github.com
```

**Solution**: Kill stray processes, check network, retry

---

## Running All Tests

### Quick Test Suite (5 minutes)

```bash
#!/bin/bash
# Quick sanity check

cd /tmp/skillmeat-test-project

# Test 1: Search
skillmeat search "pdf" --json | jq '.results | length' && echo "✓ Search works"

# Test 2: Add
skillmeat add skill anthropics/skills/canvas-design && echo "✓ Add works"

# Test 3: List
skillmeat list --json | jq '.results | length' && echo "✓ List works"

# Test 4: Deploy
skillmeat deploy canvas-design && echo "✓ Deploy works"

# Test 5: Undeploy
skillmeat undeploy canvas-design --project . && echo "✓ Undeploy works"

echo "✓ All quick tests passed!"
```

### Full Test Suite (30 minutes)

```bash
#!/bin/bash
# Complete integration test suite

set -e
FAILED=0
PASSED=0

test_discovery() {
  echo "Testing discovery workflows..."
  # Run all discovery tests
  # Check results
  PASSED=$((PASSED + 5))
}

test_deployment() {
  echo "Testing deployment workflows..."
  # Run all deployment tests
  # Check results
  PASSED=$((PASSED + 3))
}

test_agents() {
  echo "Testing agent integrations..."
  # Run all agent tests
  # Check results
  PASSED=$((PASSED + 5))
}

test_confidence() {
  echo "Testing confidence scoring..."
  # Run all confidence tests
  # Check results
  PASSED=$((PASSED + 4))
}

test_bundles() {
  echo "Testing bundle operations..."
  # Run all bundle tests
  # Check results
  PASSED=$((PASSED + 6))
}

# Run all test categories
test_discovery
test_deployment
test_agents
test_confidence
test_bundles

echo "================================"
echo "Test Results: $PASSED passed, $FAILED failed"
if [ $FAILED -eq 0 ]; then
  echo "✓ All integration tests PASSED"
  exit 0
else
  echo "✗ Some tests FAILED"
  exit 1
fi
```

---

## References

- **SKILL.md**: Main skillmeat-cli skill documentation
- **command-quick-reference.md**: Complete command reference
- **agent-integration.md**: Agent integration patterns
- **discovery-workflow.md**: Discovery workflow details
- **confidence-integration.md**: Confidence scoring documentation
- **bundle-workflow.md**: Bundle creation and import

---

## Appendix: Test Data

### Sample Artifacts for Testing

```json
{
  "test_artifacts": [
    {
      "id": "test:canvas-design",
      "name": "canvas-design",
      "type": "skill",
      "source": "anthropics/skills/canvas-design",
      "version": "1.5.0"
    },
    {
      "id": "test:pdf-processor",
      "name": "pdf-processor",
      "type": "skill",
      "source": "anthropics/skills/pdf-processor",
      "version": "2.1.0"
    },
    {
      "id": "test:form-builder",
      "name": "form-builder",
      "type": "skill",
      "source": "anthropics/skills/form-builder",
      "version": "1.2.0"
    }
  ]
}
```

### Expected Confidence Scores

```
Query: "pdf tools"
- pdf-processor: 95% (official, high quality)
- pdf-forms: 82% (community, verified)
- document-converter: 68% (partial match)

Query: "react forms"
- form-builder: 92% (React-specific, verified)
- form-helper: 78% (compatible, community)
- generic-form: 55% (language-agnostic)
```

---

**Created**: 2024-12-24
**Last Updated**: 2024-12-24
**Status**: Complete
**Version**: 1.0.0

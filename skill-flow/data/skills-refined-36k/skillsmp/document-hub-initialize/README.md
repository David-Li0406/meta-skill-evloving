# Document Hub Skills

A comprehensive documentation management system for software projects. Automatically maintain architecture diagrams, module responsibilities, technology stack, and domain glossaries.

## Quick Start

```bash
# Initialize documentation for a new project
/document-hub initialize

# Update documentation after code changes
/document-hub update

# View current documentation state
/document-hub read

# Analyze documentation quality and drift
/document-hub analyze
```

---

## Overview

The Document Hub system creates and maintains a structured documentation hub in your project's `cline-docs/` directory:

```
project-root/
└── cline-docs/
    ├── systemArchitecture.md      # Architecture diagrams (Mermaid)
    ├── keyPairResponsibility.md   # Module responsibilities
    ├── glossary.md                # Domain-specific terms
    └── techStack.md               # Technologies used
```

### Why Document Hub?

- **Automatic Detection**: Scans your codebase to detect modules, technologies, and domain terms
- **Git-Aware Updates**: Analyzes git history to scope documentation updates intelligently
- **Drift Detection**: Identifies gaps between documentation and actual code
- **Zero-Dependency Tools**: Python scripts using only standard library
- **Validation Built-In**: Ensures documentation structure and syntax correctness

---

## Available Skills

### 1. `/document-hub initialize`

**Purpose:** Bootstrap a new project with complete documentation structure

**When to Use:**
- Starting a new project
- Adding documentation to an existing project
- Recreating missing documentation

**What It Does:**
1. Creates `cline-docs/` directory structure
2. Detects existing modules from `src/` directory
3. Detects technologies from `package.json`/`requirements.txt`
4. Extracts domain-specific terms from code
5. Generates 4 core documentation files with initial content
6. Validates the result

**Tool Calls Used:**

| Tool | Purpose | Output |
|------|---------|--------|
| `validate_hub.py` | Check if hub already exists and is valid | `{"valid": bool, "errors": [], "warnings": []}` |
| `detect_drift.py` | Detect existing modules and technologies | `{"module_drift": {...}, "technology_drift": {...}}` |
| `extract_glossary.py` | Extract domain terms from codebase | `{"terms": [{term, contexts, score}...]}` |

**Example Flow:**
```bash
# 1. Detect what exists
python scripts/detect_drift.py /path/to/project

# 2. Extract glossary terms
python scripts/extract_glossary.py /path/to/project

# 3. Create 4 files with detected content
# [Files created using templates + detected data]

# 4. Validate result
python scripts/validate_hub.py /path/to/project
```

**Output:** 4 markdown files populated with project-specific content

---

### 2. `/document-hub update`

**Purpose:** Intelligently update documentation based on code changes and drift

**When to Use:**
- After completing a major feature
- After significant refactoring
- After dependency updates
- Monthly maintenance

**What It Does:**
1. Validates current documentation structure
2. Analyzes git history since last doc update
3. Detects drift between docs and code
4. Proposes specific, prioritized updates
5. Applies updates after user approval
6. Validates the result

**Tool Calls Used:**

| Tool | Purpose | Output |
|------|---------|--------|
| `validate_hub.py` | Pre-update validation check | `{"valid": bool, "errors": [], "warnings": []}` |
| `analyze_changes.py` | Git-based change analysis | `{"changed_files": N, "categories": {...}, "suggestions": [...]}` |
| `detect_drift.py` | Identify documentation gaps | `{"drift_score": 0.23, "undocumented": [...], "recommendations": [...]}` |
| `extract_glossary.py` | Find new domain terms | `{"terms": [...], "total_terms": N}` |
| `validate_hub.py` | Post-update validation | `{"valid": bool, "errors": [], "warnings": []}` |

**Example Flow:**
```bash
# 1. Pre-validation
python scripts/validate_hub.py /path/to/project

# 2. Analyze git changes
python scripts/analyze_changes.py /path/to/project
# Returns: {"categories": {"modules": 3, "dependencies": 1}, "suggestions": [...]}

# 3. Detect drift
python scripts/detect_drift.py /path/to/project
# Returns: {"drift_score": 0.23, "undocumented": ["analytics", "webhooks"]}

# 4. Extract new terms
python scripts/extract_glossary.py /path/to/project

# 5. Present proposal to user
# [User approves]

# 6. Apply updates
# [Update systemArchitecture.md, keyPairResponsibility.md, etc.]

# 7. Post-validation
python scripts/validate_hub.py /path/to/project
```

**Output:** Updated documentation files, validation report

---

### 3. `/document-hub read`

**Purpose:** Quick overview of current documentation state

**When to Use:**
- Onboarding to a new project
- Before starting work on a feature
- Periodic documentation health checks
- Checking if documentation exists

**What It Does:**
1. Validates documentation structure
2. Reads all 4 core files
3. Extracts key information
4. Presents formatted summary
5. Identifies any issues or warnings

**Tool Calls Used:**

| Tool | Purpose | Output |
|------|---------|--------|
| `validate_hub.py` | Validate structure and get health status | `{"valid": bool, "errors": [], "warnings": []}` |

**Example Flow:**
```bash
# 1. Validate
python scripts/validate_hub.py /path/to/project

# 2. Read all files
# [Read systemArchitecture.md, keyPairResponsibility.md, glossary.md, techStack.md]

# 3. Extract key info
# - Count diagrams, modules, terms, technologies
# - Extract summaries

# 4. Present formatted summary
```

**Output:** Structured summary with:
- Validation status
- System architecture overview
- Module count and key modules
- Technology stack summary
- Glossary term count
- Health check warnings

---

### 4. `/document-hub analyze`

**Purpose:** Deep analysis of documentation quality and drift (read-only)

**When to Use:**
- Before planning a documentation update
- Monthly documentation audits
- Checking documentation health
- Diagnosing documentation issues

**What It Does:**
1. Validates documentation structure
2. Analyzes module drift (src/ vs docs)
3. Analyzes technology drift (dependencies vs docs)
4. Identifies missing glossary terms
5. Calculates health score (0-100)
6. Generates prioritized recommendations
7. **Makes NO changes** - analysis only

**Tool Calls Used:**

| Tool | Purpose | Output |
|------|---------|--------|
| `validate_hub.py` | Check structure validity | `{"valid": bool, "errors": [], "warnings": []}` |
| `detect_drift.py` | Comprehensive drift analysis | `{"drift_score": 0.23, "module_drift": {...}, "technology_drift": {...}, "recommendations": [...]}` |
| `extract_glossary.py` | Find missing domain terms | `{"terms": [{term, contexts, score}...], "total_terms": N}` |

**Example Flow:**
```bash
# 1. Validate structure
python scripts/validate_hub.py /path/to/project

# 2. Detect drift
python scripts/detect_drift.py /path/to/project
# Returns: {
#   "drift_score": 0.23,
#   "module_drift": {
#     "undocumented": ["analytics", "webhooks"],
#     "documented_but_missing": ["legacy"]
#   },
#   "technology_drift": {
#     "undocumented": ["Redis", "BullMQ"]
#   }
# }

# 3. Extract glossary gaps
python scripts/extract_glossary.py /path/to/project

# 4. Compare with existing glossary
# [Read cline-docs/glossary.md]
# [Identify terms in code but not in glossary]

# 5. Calculate health score
# Health = 100 - (drift_score * 100)

# 6. Generate report with prioritized recommendations
```

**Output:** Comprehensive analysis report with:
- Overall health score (0-100)
- Drift score by category
- Undocumented modules list
- Missing technologies list
- Glossary gaps (ranked by relevance)
- HIGH/MEDIUM/LOW priority recommendations
- Suggested next steps

---

## Tool Reference

All skills use Python helper scripts in `scripts/` directory.

### validate_hub.py

**Purpose:** Validate documentation structure and syntax

**Usage:**
```bash
python scripts/validate_hub.py /path/to/project
```

**Output:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "file": "systemArchitecture.md",
      "line": 42,
      "message": "Complex diagram with 22 nodes"
    }
  ],
  "checks_run": 5
}
```

**What It Checks:**
- ✓ All required files exist
- ✓ Mermaid diagram syntax is valid
- ✓ Cross-references between files work
- ✓ Glossary is alphabetically ordered
- ✓ /arch subfolder structure (if exists)
- ✓ Diagram complexity (warns if > 20 nodes)

**Used By:** All 4 skills

---

### detect_drift.py

**Purpose:** Detect gaps between documentation and codebase

**Usage:**
```bash
python scripts/detect_drift.py /path/to/project
```

**Output:**
```json
{
  "drift_score": 0.23,
  "status": "needs_attention",
  "module_drift": {
    "documented_count": 5,
    "actual_count": 7,
    "undocumented": ["analytics", "webhooks"],
    "documented_but_missing": ["legacy"],
    "drift_score": 0.30
  },
  "technology_drift": {
    "documented_count": 8,
    "actual_count": 10,
    "undocumented": ["Redis", "BullMQ"],
    "documented_but_missing": ["MongoDB"],
    "drift_score": 0.15
  },
  "recommendations": [
    "Document the 'analytics' module in keyPairResponsibility.md",
    "Add Redis to techStack.md"
  ]
}
```

**What It Detects:**
- Modules in `src/` not documented
- Documented modules that don't exist
- Technologies in `package.json`/`requirements.txt` not documented
- Documented technologies not in dependencies
- Configuration files not mentioned

**Used By:** initialize, update, analyze

---

### analyze_changes.py

**Purpose:** Analyze git history to scope updates

**Usage:**
```bash
# Auto-detect since last doc update
python scripts/analyze_changes.py /path/to/project

# Or specify commit
python scripts/analyze_changes.py /path/to/project abc123
```

**Output:**
```json
{
  "changed_files": 42,
  "since_commit": "abc123",
  "categories": {
    "architecture": 2,
    "modules": 3,
    "config": 1,
    "dependencies": 1,
    "api": 8,
    "ui": 15
  },
  "category_details": {
    "modules": ["src/auth", "src/payments", "src/webhooks"],
    "dependencies": ["package.json"]
  },
  "descriptions": [
    "Updated 1 dependency file(s)",
    "Changes in modules: src/auth, src/payments, src/webhooks",
    "Modified 8 API/route file(s)"
  ],
  "suggestions": [
    {
      "file": "systemArchitecture.md",
      "reason": "core architecture files changed",
      "priority": "high"
    },
    {
      "file": "keyPairResponsibility.md",
      "reason": "3 module(s) modified",
      "priority": "high"
    }
  ],
  "commit_messages": [
    "Add payment processing module",
    "Refactor authentication flow",
    "Update Redis configuration"
  ]
}
```

**What It Analyzes:**
- Git diff since last doc update (or specified commit)
- Categorizes changes by type
- Identifies which doc files need updates
- Prioritizes updates (high/medium/low)
- Extracts recent commit messages for context

**Used By:** update

---

### extract_glossary.py

**Purpose:** Extract domain-specific terms from codebase

**Usage:**
```bash
# Default: scan all .ts, .tsx, .js, .jsx, .py files
python scripts/extract_glossary.py /path/to/project

# Custom patterns
python scripts/extract_glossary.py /path/to/project "**/*.ts,**/*.py"

# With minimum occurrence threshold
python scripts/extract_glossary.py /path/to/project "**/*.ts" 3
```

**Output:**
```json
{
  "total_terms": 42,
  "scanned_files": 156,
  "min_occurrences": 2,
  "terms": [
    {
      "term": "FulfillmentJob",
      "occurrences": 15,
      "contexts": [
        "Represents a job in the fulfillment pipeline",
        "Tracks order processing status and completion"
      ],
      "files": ["src/fulfillment/job.ts", "src/api/jobs.ts"],
      "score": 45
    },
    {
      "term": "BatchProcessor",
      "occurrences": 8,
      "contexts": ["Processes items in configurable batch sizes"],
      "files": ["src/processing/batch.ts"],
      "score": 38
    }
  ]
}
```

**What It Extracts:**
- Class names (TypeScript, JavaScript, Python)
- Function names with domain significance
- Interface and type definitions
- Context from comments and docstrings

**What It Filters Out:**
- Generic terms (data, config, handler, etc.)
- Common verbs (get, set, create, etc.)
- Test files
- node_modules and similar directories

**Used By:** initialize, update, analyze

---

## Tool Summary Matrix

| Tool | initialize | update | read | analyze | Purpose |
|------|:----------:|:------:|:----:|:-------:|---------|
| **validate_hub.py** | ✅ | ✅ (2x) | ✅ | ✅ | Structure validation |
| **detect_drift.py** | ✅ | ✅ | ❌ | ✅ | Gap detection |
| **analyze_changes.py** | ❌ | ✅ | ❌ | ❌ | Git-based scoping |
| **extract_glossary.py** | ✅ | ✅ | ❌ | ✅ | Term extraction |

---

## Workflow Examples

### Example 1: Setting Up a New Project

```bash
# Step 1: Initialize documentation
/document-hub initialize

# Behind the scenes:
# → validate_hub.py (check if exists)
# → detect_drift.py (find modules & tech)
# → extract_glossary.py (get domain terms)
# → Create 4 files with detected content
# → validate_hub.py (verify result)

# Step 2: Review and refine
/document-hub read

# Step 3: User adds context, then update
/document-hub update
```

### Example 2: Maintaining Documentation

```bash
# Monthly health check
/document-hub analyze

# Output shows:
# - Health Score: 77/100
# - Drift Score: 0.23
# - 2 undocumented modules
# - 2 missing technologies
# - 18 glossary gaps

# Fix high-priority issues
/document-hub update

# Behind the scenes:
# → validate_hub.py (pre-check)
# → analyze_changes.py (git analysis)
# → detect_drift.py (gap detection)
# → extract_glossary.py (new terms)
# → Present proposal
# → User approves
# → Apply updates
# → validate_hub.py (post-check)
```

### Example 3: After Feature Development

```bash
# Developer completes payment module

# Check what needs updating
/document-hub analyze

# Output:
# - New module detected: src/payments
# - New technology: Stripe SDK
# - 5 new glossary terms

# Apply updates
/document-hub update

# Behind the scenes:
# → analyze_changes.py detects payment module changes
# → detect_drift.py finds undocumented "payments" module
# → extract_glossary.py finds "PaymentIntent", "StripeWebhook", etc.
# → Updates keyPairResponsibility.md
# → Updates techStack.md
# → Updates glossary.md
```

---

## Health Score Interpretation

The analyze skill calculates a health score (0-100):

| Score | Status | Drift Score | Action |
|-------|--------|-------------|--------|
| 90-100 | ✅ Excellent | < 0.10 | Continue monitoring |
| 75-89 | ✅ Good | 0.10-0.25 | Minor updates needed |
| 60-74 | ⚠️ Needs Attention | 0.25-0.40 | Plan update soon |
| < 60 | ❌ Poor | > 0.40 | Update immediately |

---

## Best Practices

### When to Use Each Skill

- **Use `/document-hub initialize`:**
  - New project setup
  - Adding docs to existing project
  - Rebuilding corrupted docs

- **Use `/document-hub update`:**
  - After major features
  - After refactoring
  - After dependency changes
  - Monthly maintenance

- **Use `/document-hub read`:**
  - Onboarding new developers
  - Before starting feature work
  - Quick health checks

- **Use `/document-hub analyze`:**
  - Before planning updates
  - Monthly audits
  - Diagnosing issues
  - When drift suspected

### Workflow Recommendations

1. **Daily Development:** `/document-hub read` to check context
2. **After Features:** `/document-hub analyze` → `/document-hub update`
3. **Monthly:** `/document-hub analyze` to monitor health
4. **New Projects:** `/document-hub initialize` → review → `/document-hub update`

---

## Dependencies

**Zero!** All Python scripts use standard library only:
- `json` - JSON parsing
- `sys` - Command-line arguments
- `re` - Regular expressions
- `pathlib` - File path handling
- `subprocess` - Git commands
- `collections` - Data structures

No `pip install` required.

---

## File Locations

```
skills/hub/
├── README.md                      ← You are here
├── document-hub-initialize.md     ← Skill: Initialize
├── document-hub-update.md         ← Skill: Update
├── document-hub-read.md           ← Skill: Read
├── document-hub-analyze.md        ← Skill: Analyze
└── scripts/
    ├── README.md                  ← Tool documentation
    ├── validate_hub.py            ← Tool: Validation
    ├── detect_drift.py            ← Tool: Drift detection
    ├── analyze_changes.py         ← Tool: Git analysis
    ├── extract_glossary.py        ← Tool: Glossary extraction
    └── requirements.txt           ← (Empty - no deps needed)
```

---

## Getting Help

- **For skill usage:** Read individual skill files (`document-hub-*.md`)
- **For tool details:** See `scripts/README.md`
- **For planning docs:** Check `.claude/planning/`
- **For examples:** Each skill file contains complete examples

---

## Status

**Phase 1 Complete ✅**
- 4 skills fully documented
- 4 Python tools implemented
- Zero dependencies
- Following Anthropic pattern
- Ready for production use

**Phase 2: Hooks** ✅ (Partially Complete)
- ✅ Automatic session-start documentation loading
- ⏳ Task-complete update suggestions (deferred)
- ⏳ File-watch validation (deferred)
- ⏳ Module-added term extraction (deferred)

---

## Automatic Context Loading (Hook)

### Session-Start Hook ✅

**Status:** Implemented and enabled by default
**Location:** `hooks/hub/document-hub-session-start.md`

**What It Does:**
- Automatically loads documentation hub at the start of every session
- Reads all 4 core files silently (no user notification)
- Validates structure in background
- Provides instant project context

**Benefits:**
- "Brain" persona: Documentation as your memory
- No manual `/document-hub read` needed
- Immediate context-aware responses
- Zero user friction

**Performance:**
- Overhead: ~2 seconds per session start
- Silent operation (no output to user)
- Graceful degradation (skips if no docs exist)

**Example:**
```
[Session starts - hook loads documentation silently]

User: "Where should I add the payment logic?"

Claude: "Based on the system architecture, add it to the
src/payments module, which handles all payment integrations..."

[Response uses knowledge from loaded documentation]
```

**See:** `hooks/hub/README.md` for complete documentation

### Why Only One Hook?

We implemented only the session-start hook because:
- ✅ Core "Brain" behavior
- ✅ No notification fatigue
- ✅ High value, low overhead
- ✅ Works for 100% of users

Other hooks (task-complete, file-watch) were deferred to avoid notification fatigue. Users can manually invoke skills when needed.

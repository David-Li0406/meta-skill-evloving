---
name: analyze
description: Perform initial analysis of a codebase - detect tech stack, directory structure, and completeness. This is Step 1 of the 6-step reverse engineering process that transforms incomplete applications into spec-driven codebases. Automatically detects programming languages, frameworks, architecture patterns, and generates comprehensive analysis-report.md. Use when starting reverse engineering on any codebase.
---

# Initial Analysis

**Step 1 of 6** in the Reverse Engineering to Spec-Driven Development process.

**Estimated Time:** 5 minutes
**Output:** `analysis-report.md`

---

## When to Use This Skill

Use this skill when:
- Starting reverse engineering on a new or existing codebase
- Need to understand tech stack and architecture before making changes
- Want to assess project completeness and identify gaps
- First time analyzing this project with the toolkit
- User asks "analyze this codebase" or "what's in this project?"

**Trigger Phrases:**
- "Analyze this codebase"
- "What tech stack is this using?"
- "How complete is this application?"
- "Run initial analysis"
- "Start reverse engineering process"

---

## What This Skill Does

This skill performs comprehensive initial analysis by:

1. **Asking which path you want** - Greenfield (new app) or Brownfield (manage existing)
2. **Auto-detecting application context** - Identifies programming languages, frameworks, and build systems
3. **Analyzing directory structure** - Maps architecture patterns and key components
4. **Scanning existing documentation** - Assesses current documentation quality
5. **Estimating completeness** - Evaluates how complete the implementation is
6. **Generating analysis report** - Creates `analysis-report.md` with all findings
7. **Storing path choice** - Saves your selection to guide subsequent steps

---

## Choose Your Path

**FIRST:** Determine which path aligns with your goals.

### Path A: Greenfield (Build New App from Business Logic)

**Use when:**
- Building a new application based on existing app's business logic
- Migrating to a different tech stack
- Want flexibility in implementation choices
- Need platform-agnostic specifications

**Result:**
- Specifications focus on WHAT, not HOW
- Business requirements only
- Can implement in any technology
- Tech-stack agnostic

**Example:** "Extract the business logic from this Rails app so we can rebuild it in Next.js"

### Path B: Brownfield (Manage Existing with Spec Kit)

**Use when:**
- Managing an existing codebase with GitHub Spec Kit
- Want spec-code validation with `/speckit.analyze`
- Planning upgrades or refactoring
- Need specs that match current implementation exactly

**Result:**
- Specifications include both WHAT and HOW
- Business logic + technical implementation
- Tech-stack prescriptive
- `/speckit.analyze` can validate alignment

**Example:** "Add GitHub Spec Kit to this Next.js app so we can manage it with specs going forward"

### Batch Session Auto-Configuration

**Before showing questions, check for batch session by walking up directories:**

```bash
# Function to find batch session file (walks up like .git search)
find_batch_session() {
  local current_dir="$(pwd)"
  while [[ "$current_dir" != "/" ]]; do
    if [[ -f "$current_dir/.stackshift-batch-session.json" ]]; then
      echo "$current_dir/.stackshift-batch-session.json"
      return 0
    fi
    current_dir="$(dirname "$current_dir")"
  done
  return 1
}

# Check if batch session exists
BATCH_SESSION=$(find_batch_session)
if [[ -n "$BATCH_SESSION" ]]; then
  echo "✅ Using batch session configuration from: $BATCH_SESSION"
  cat "$BATCH_SESSION" | jq '.answers'
  # Auto-apply answers from batch session
  # Skip questionnaire entirely
fi
```

**If batch session exists:**
1. Walk up directory tree to find `.stackshift-batch-session.json`
2. Load answers from found batch session file
3. Show: "Using batch session configuration: route=osiris, spec_output=~/git/specs, ..."
4. Skip all questions below
5. Proceed directly to analysis with pre-configured answers
6. Save answers to local `.stackshift-state.json` as usual

**Example directory structure:**
```
~/git/osiris/
  ├── .stackshift-batch-session.json  ← Batch session here
  ├── ws-vehicle-details/
  │   └── [agent working here finds parent session]
  ├── ws-hours/
  │   └── [agent working here finds parent session]
  └── ws-contact/
      └── [agent working here finds parent session]
```

**If no batch session:**
- Continue with normal questionnaire below

---

### Step 1: Auto-Detect Application Type

**Before asking questions, detect what kind of application this is:**

```bash
# Check repository name and structure
REPO_NAME=$(basename $(pwd))
PARENT_DIR=$(basename $(dirname $(pwd)))

# Detection patterns (in priority order)
# Add your own patterns here for your framework/architecture!

# Monorepo service detection
if [[ "$PARENT_DIR" == "services" || "$PARENT_DIR" == "apps" ]] && [ -f "../../package.json" ]; then
  DETECTION="monorepo-service"
  echo "📦 Detected: Monorepo Service (services/* or apps/* directory)"

# Nx workspace detection
elif [ -f "nx.json" ] || [ -f "../../nx.json" ]; then
  DETECTION="nx-app"
  echo "⚡ Detected: Nx Application"

# Turborepo detection
elif [ -f "turbo.json" ] || [ -f "../../turbo.json" ]; then
  DETECTION="turborepo-package"
  echo "🚀 Detected: Turborepo Package"

# Lerna package detection
elif [ -f "lerna.json" ] || [ -f "../../lerna.json" ]; then
  DETECTION="lerna-package"
  echo "📦 Detected: Lerna Package"

# Generic application (default)
else
  DETECTION="generic"
  echo "🔍 Detected: Generic Application"
fi

echo "Detection type: $DETECTION"
```

**How Detection Patterns Work:**

Detection identifies WHAT patterns to look for during analysis:
- **monorepo-service**: Look for shared packages, inter-service calls, monorepo structure
- **nx-app**: Look for project.json, workspace deps, Nx-specific patterns
- **generic**: Standard application analysis

**Add Your Own Patterns:**
```bash
# Example: Custom framework detection
# elif [[ "$REPO_NAME" =~ ^my-widget- ]]; then
#   DETECTION="my-framework-widget"
#   echo "🎯 Detected: My Framework Widget"
```

**Detection determines what to analyze, but NOT how to spec it!**

---

### Step 2: Initial Questionnaire

Now that we know what kind of application this is, let's configure the extraction approach:

**Question 1: Choose Your Route**
```
Which path best aligns with your goals?

A) Greenfield: Extract for migration to new tech stack
   → Extract business logic only (tech-agnostic)
   → Can implement in any stack
   → Suitable for platform migrations
   → Example: Extract Rails app business logic → rebuild in Next.js

B) Brownfield: Extract for maintaining existing codebase
   → Extract business logic + technical details (tech-prescriptive)
   → Manage existing codebase with specs
   → Suitable for in-place improvements
   → Example: Add specs to Express API for ongoing maintenance
```

**This applies to ALL detection types:**
- Monorepo Service + Greenfield = Business logic for platform migration
- Monorepo Service + Brownfield = Full implementation for maintenance
- Nx App + Greenfield = Business logic for rebuild
- Nx App + Brownfield = Full Nx/Angular details for refactoring
- Generic + Greenfield = Business logic for rebuild
- Generic + Brownfield = Full implementation for management

**Question 2: Implementation Framework**
```
Which implementation framework do you want to use?

A) GitHub Spec Kit (Recommended for most projects)
   → Feature-level specifications in .specify/
   → Task-driven implementation with /speckit.* commands
   → Simpler, lightweight workflow
   → Best for: small-medium projects, focused features

B) BMAD Method (For larger/enterprise projects)
   → Uses same reverse-engineering docs as Spec Kit
   → Hands off to BMAD's collaborative PM/Architect agents
   → BMAD creates PRD + Architecture through conversation
   → Best for: large projects, multi-team, enterprise

After StackShift extracts documentation (Gear 2):
- Both frameworks get the same 9 docs in docs/reverse-engineering/
- Spec Kit: Gears 3-6 create .specify/ specs, use /speckit.implement
- BMAD: Skip to Gear 6, hand off to *workflow-init with rich context
```

**Question 3: Brownfield Mode** _(If Brownfield selected)_
```
Do you want to upgrade dependencies after establishing specs?

A) Standard - Just create specs for current state
   → Document existing implementation as-is
   → Specs match current code exactly
   → Good for maintaining existing versions

B) Upgrade - Create specs + upgrade all dependencies
   → Spec current state first (100% coverage)
   → Then upgrade all dependencies to latest versions
   → Fix breaking changes with spec guidance
   → Improve test coverage to spec standards
   → End with modern, fully-spec'd application
   → Perfect for modernizing legacy apps

**Upgrade mode includes:**
- npm update / pip upgrade / go get -u (based on tech stack)
- Automated breaking change detection
- Test-driven upgrade fixes
- Spec updates for API changes
- Coverage improvement to 85%+
```

**Question 4: Choose Your Transmission**
```
How do you want to shift through the gears?

A) Manual - Review each gear before proceeding
   → You're in control
   → Stop at each step
   → Good for first-time users

B) Cruise Control - Shift through all gears automatically
   → Hands-free
   → Unattended execution
   → Good for experienced users or overnight runs
```

**Question 5: Specification Thoroughness**
```
How thorough should specification generation be in Gear 3?

A) Specs only (30 min - fast)
   → Generate specs for all features
   → Create plans manually with /speckit.plan as needed
   → Good for: quick assessment, flexibility

B) Specs + Plans (45-60 min - recommended)
   → Generate specs for all features
   → Auto-generate implementation plans for incomplete features
   → Ready for /speckit.tasks when you implement
   → Good for: most projects, balanced automation

C) Specs + Plans + Tasks (90-120 min - complete roadmap)
   → Generate specs for all features
   → Auto-generate plans for incomplete features
   → Auto-generate comprehensive task lists (300-500 lines each)
   → Ready for immediate implementation
   → Good for: large projects, maximum automation
```

**Question 6: Clarifications Strategy** _(If Cruise Control selected)_
```
How should [NEEDS CLARIFICATION] markers be handled?

A) Defer - Mark them, continue implementation around them
   → Fastest
   → Can clarify later with /speckit.clarify

B) Prompt - Stop and ask questions interactively
   → Most thorough
   → Takes longer

C) Skip - Only implement fully-specified features
   → Safest
   → Some features won't be implemented
```

**Question 7: Implementation Scope** _(If Cruise Control selected)_
```
What should be implemented in Gear 6?

A) None - Stop after specs are ready
   → Just want specifications
   → Will implement manually later

B) P0 only - Critical features only
   → Essential features
   → Fastest implementation

C) P0 + P1 - Critical + high-value features
   → Good balance
   → Most common choice

D) All - Every feature (may take hours/days)
   → Complete implementation
   → Longest runtime
```

**Question 8: Spec Output Location** _(If Greenfield selected)_
```
Where should specifications and documentation be written?

A) Current repository (default)
   → Specs in: ./docs/reverse-engineering/, ./.specify/
   → Simple, everything in one place
   → Good for: small teams, single repo

B) New application repository
   → Specs in: ~/git/my-new-app/.specify/
   → Specs live with NEW codebase
   → Good for: clean separation, NEW repo already exists

C) Separate documentation repository
   → Specs in: ~/git/my-app-docs/.specify/
   → Central docs repo for multiple apps
   → Good for: enterprise, multiple related apps

D) Custom location
   → Your choice: [specify path]

Default: Current repository (A)
```

**Question 9: Target Stack** _(If Greenfield + Implementation selected)_
```
What tech stack for the new implementation?

Examples:
- Next.js 15 + TypeScript + Prisma + PostgreSQL
- Python/FastAPI + SQLAlchemy + PostgreSQL
- Go + Gin + GORM + PostgreSQL
- Your choice: [specify your preferred stack]
```

**Question 10: Build Location** _(If Greenfield + Implementation selected)_
```
Where should the new application be built?

A) Subfolder (recommended for Web)
   → Examples: greenfield/, v2/, new-app/
   → Keeps old and new in same repo
   → Works in Claude Code Web

B) Separate directory (local only)
   → Examples: ~/git/my-new-app, ../my-app-v2
   → Completely separate location
   → Requires local Claude Code (doesn't work in Web)

C) Replace in place (destructive)
   → Removes old code as new is built
   → Not recommended
```

**Then ask for the specific path:**

**If subfolder (A):**
```
Folder name within this repo? (default: greenfield/)

Examples: v2/, new-app/, nextjs-version/, rebuilt/
Your choice: [or press enter for greenfield/]
```

**If separate directory (B):**
```
Full path to new application directory:

Examples:
- ~/git/my-new-app
- ../my-app-v2
- /Users/you/projects/new-version

Your choice: [absolute or relative path]

⚠️  Note: Directory will be created if it doesn't exist.
Claude Code Web users: This won't work in Web - use subfolder instead.
```

All answers are stored in `.stackshift-state.json` and guide the entire workflow.

**State file example:**
```json
{
  "detection_type": "monorepo-service",  // What kind of app: monorepo-service, nx-app, generic, etc.
  "route": "greenfield",                  // How to spec it: greenfield or brownfield
  "implementation_framework": "speckit",  // speckit or bmad
  "config": {
    "spec_output_location": "~/git/my-new-app",  // Where to write specs/docs
    "build_location": "~/git/my-new-app",         // Where to build new code (Gear 6)
    "target_stack": "Next.js 15 + React 19 + Prisma",
    "clarifications_strategy": "defer",
    "implementation_scope": "p0_p1"
  }
}
```

**Key fields:**
- `detection_type` - What we're analyzing (monorepo-service, nx-app, turborepo-package, generic)
- `route` - How to spec it (greenfield = tech-agnostic, brownfield = tech-prescriptive)
- `implementation_framework` - Which tool for implementation (speckit = GitHub Spec Kit, bmad = BMAD Method)

**Examples:**
- Monorepo Service + Greenfield = Extract business logic for platform migration
- Monorepo Service + Brownfield = Extract full implementation for maintenance
- Nx App + Greenfield = Extract business logic (framework-agnostic)
- Nx App + Brownfield = Extract full Nx/Angular implementation details

**How it works:**

**Spec Output Location:**
- Gear 2 writes to: `{spec_output_location}/docs/reverse-engineering/`
- Gear 3 writes to: `{spec_output_location}/.specify/memory/`
- If not set: defaults to current directory

**Build Location:**
- Gear 6 writes code to: `{build_location}/src/`, `{build_location}/package.json`, etc.
- Can be same as spec location OR different
- If not set: defaults to `greenfield/` subfolder

### Implementing the Questionnaire

Use the `AskUserQuestion` tool to collect all configuration upfront:

```typescript
// Example implementation
AskUserQuestion({
  questions: [
    {
      question: "Which route best aligns with your goals?",
      header: "Route",
      multiSelect: false,
      options: [
        {
          label: "Greenfield",
          description: "Shift to new tech stack - extract business logic only (tech-agnostic)"
        },
        {
          label: "Brownfield",
          description: "Manage existing code with specs - extract full implementation (tech-prescriptive)"
        }
      ]
    },
    {
      question: "Which implementation framework do you want to use?",
      header: "Framework",
      multiSelect: false,
      options: [
        {
          label: "GitHub Spec Kit (Recommended)",
          description: "Feature specs in .specify/, task-driven, simpler workflow"
        },
        {
          label: "BMAD Method",
          description: "Handoff to BMAD agents for collaborative artifact creation"
        }
      ]
    },
    {
      question: "How do you want to shift through the gears?",
      header: "Transmission",
      multiSelect: false,
      options: [
        {
          label: "Manual",
          description: "Review each gear before proceeding - you're in control"
        },
        {
          label: "Cruise Control",
          description: "Shift through all gears automatically - hands-free, unattended execution"
        }
      ]
    }
  ]
});

// Then based on answers, ask follow-up questions conditionally:
// - If cruise control: Ask clarifications strategy, implementation scope
// - If greenfield + implementing: Ask target stack
// - If greenfield subfolder: Ask folder name (or accept default: greenfield/)
// - If BMAD selected: Skip spec thoroughness question (BMAD handles its own planning)
// - If BMAD + cruise control: Gear 6 hands off to BMAD instead of /speckit.implement
```

**For custom folder name:** Use free-text input or accept default.

**Example:**
```
StackShift: "What folder name for the new application? (default: greenfield/)"

User: "v2/"  (or just press enter for greenfield/)

StackShift: "✅ New app will be built in: v2/"
```

Stored in state as:
```json
{
  "config": {
    "greenfield_location": "v2/"  // Relative (subfolder)
    // OR
    "greenfield_location": "~/git/my-new-app"  // Absolute (separate)
  }
}
```

**How it works:**

**Subfolder (relative path):**
```bash
# Building in: /Users/you/git/my-app/greenfield/
cd /Users/you/git/my-app
# StackShift creates: ./greenfield/
# Everything in one repo
```

**Separate directory (absolute path):**
```bash
# Current repo: /Users/you/git/my-app
# New app: /Users/you/git/my-new-app

# StackShift:
# - Reads specs from: /Users/you/git/my-app/.specify/
# - Builds new app in: /Users/you/git/my-new-app/
# - Two completely separate repos
```

---

## Step 0: Install Slash Commands (FIRST!)

**Before any analysis, ensure /speckit.* commands are available:**

```bash
# Create project commands directory
mkdir -p .claude/commands

# Copy StackShift's slash commands to project
cp ~/.claude/plugins/stackshift/.claude/commands/speckit.*.md .claude/commands/
cp ~/.claude/plugins/stackshift/.claude/commands/stackshift.modernize.md .claude/commands/

# Verify installation
ls .claude/commands/speckit.*.md
```

**You should see:**
- ✅ speckit.analyze.md
- ✅ speckit.clarify.md
- ✅ speckit.implement.md
- ✅ speckit.plan.md
- ✅ speckit.specify.md
- ✅ speckit.tasks.md
- ✅ stackshift.modernize.md

**Why this is needed:**
- Claude Code looks for slash commands in project `.claude/commands/` directory
- Plugin-level commands are not automatically discovered
- This copies them to the current project so they're available
- Only needs to be done once per project

**After copying:**
- `/speckit.*` commands will be available for this project
- No need to restart Claude Code
- Commands work immediately

### Critical: Commit Commands to Git

**Add to .gitignore (or create if missing):**

```bash
# Allow .claude directory structure
!.claude/
!.claude/commands/

# Track slash commands (team needs these!)
!.claude/commands/*.md

# Ignore user-specific settings
.claude/settings.json
.claude/mcp-settings.json
```

**Then commit:**

```bash
git add .claude/commands/
git commit -m "chore: add StackShift and Spec Kit slash commands

Adds /speckit.* and /stackshift.* slash commands for team use.

Commands added:
- /speckit.specify - Create feature specifications
- /speckit.plan - Create technical plans
- /speckit.tasks - Generate task lists
- /speckit.implement - Execute implementation
- /speckit.clarify - Resolve ambiguities
- /speckit.analyze - Validate specs match code
- /stackshift.modernize - Upgrade dependencies

These commands enable spec-driven development workflow.
All team members will have access after cloning.
"
```

**Why this is critical:**
- ✅ Teammates get commands when they clone
- ✅ Commands are versioned with project
- ✅ No setup needed for new team members
- ✅ Commands always available

**Without committing:**
- ❌ Each developer needs to run StackShift or manually copy
- ❌ Confusion: "Why don't slash commands work?"
- ❌ Inconsistent developer experience

---

## Process Overview

The analysis follows 5 steps:

### Step 1: Auto-Detect Application Context
- Run detection commands for all major languages/frameworks
- Identify the primary technology stack
- Extract version information

See [operations/detect-stack.md](operations/detect-stack.md) for detailed instructions.

### Step 2: Extract Core Metadata
- Application name from manifest or directory
- Version number from package manifests
- Description from README or manifest
- Git repository URL if available
- Technology stack summary

### Step 3: Analyze Directory Structure
- Identify architecture patterns (MVC, microservices, monolith, etc.)
- Find configuration files
- Count source files by type
- Map key components (backend, frontend, database, API, infrastructure)

See [operations/directory-analysis.md](operations/directory-analysis.md) for detailed instructions.

### Step 4: Check for Existing Documentation
- Scan for docs folders and markdown files
- Assess documentation quality
- Identify what's documented vs. what's missing

See [operations/documentation-scan.md](operations/documentation-scan.md) for detailed instructions.

### Step 5: Assess Completeness
- Look for placeholder files (TODO, WIP, etc.)
- Check README for mentions of incomplete features
- Count test files and estimate test coverage
- Verify deployment/CI setup

See [operations/completeness-assessment.md](operations/completeness-assessment.md) for detailed instructions.

---

## Output Format

This skill generates `analysis-report.md` in the project root with:

- **Application Metadata** - Name, version, description, repository
- **Technology Stack** - Languages, frameworks, libraries, build system
- **Architecture Overview** - Directory structure, key components
- **Existing Documentation** - What docs exist and their quality
- **Completeness Assessment** - Estimated % completion with evidence
- **Source Code Statistics** - File counts, lines of code estimates
- **Recommended Next Steps** - Focus areas for reverse engineering
- **Notes** - Additional observations

See [operations/generate-report.md](operations/generate-report.md) for the complete template.

---

## Success Criteria

After running this skill, you should have:

- ✅ `analysis-report.md` file created in project root
- ✅ Technology stack clearly identified
- ✅ Directory structure and architecture understood
- ✅ Completeness estimated (% done for backend, frontend, tests, docs)
- ✅ Ready to proceed to Step 2 (Reverse Engineer)

---

## Next Step

Once `analysis-report.md` is created and reviewed, proceed to:

**Step 2: Reverse Engineer** - Use the reverse-engineer skill to generate comprehensive documentation.

---

## Principles

For guidance on performing effective initial analysis:
- [principles/multi-language-detection.md](principles/multi-language-detection.md) - Detecting polyglot codebases
- [principles/architecture-pattern-recognition.md](principles/architecture-pattern-recognition.md) - Identifying common patterns

---

## Common Workflows

**New Project Analysis:**
1. User asks to analyze codebase
2. Run all detection commands in parallel
3. Generate analysis report
4. Present summary and ask if ready for Step 2

**Re-analysis:**
1. Check if analysis-report.md already exists
2. Ask user if they want to update it or skip to Step 2
3. If updating, re-run analysis and show diff

**Partial Analysis:**
1. User already knows tech stack
2. Skip detection, focus on completeness assessment
3. Generate abbreviated report

---

## Technical Notes

- **Parallel execution:** Run all language detection commands in parallel for speed
- **Error handling:** Missing manifest files are normal (return empty), don't error
- **File limits:** Use `head` to limit output for large codebases
- **Exclusions:** Always exclude node_modules, vendor, .git, build, dist, target
- **Platform compatibility:** Commands work on macOS, Linux, WSL

---

## Example Invocation

When a user says:

> "I need to reverse engineer this application and create specifications. Let's start."

This skill auto-activates and:
1. Detects tech stack (e.g., Next.js, TypeScript, Prisma, AWS)
2. Analyzes directory structure (identifies app/, lib/, prisma/, infrastructure/)
3. Scans documentation (finds README.md, basic setup docs)
4. Assesses completeness (estimates backend 100%, frontend 60%, tests 30%)
5. Generates analysis-report.md
6. Presents summary and recommends proceeding to Step 2

---

**Remember:** This is Step 1 of 6. After analysis, you'll proceed to reverse-engineer, create-specs, gap-analysis, complete-spec, and implement. Each step builds on the previous one.

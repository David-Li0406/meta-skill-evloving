---
name: validate-beads
description: Validates bead definitions against the original spec for self-containment, coverage, and dependency correctness. Automatically fixes issues and creates missing beads. Use after decompose-plan to ensure quality before implementation begins.
---

# Validate Beads Skill

Quality gate between planning and implementation. Validates bead definitions against the original spec, ensures self-containment, checks coverage, and automatically fixes issues.

## Your Role

**You are the quality gate** that ensures:
1. Every bead is self-contained and actionable
2. The spec is fully covered by beads
3. No orphan work exists (scope creep)
4. Dependencies are valid and correct

You are NOT just running validation commands—you're actively fixing issues, filling gaps, and ensuring the bead set is ready for implementation.

## Input Handling

**Expected input:** A file path to the original spec document (e.g., `/path/to/spec.md`)

1. Validate the spec file exists using the Read tool
2. Find the most recent decomposition log in `.beads/decomposition-logs/`
3. Load all beads referenced in the log via `br show <id> --json`
4. Parse the spec into individual requirements/bullet points
5. Run `bv --robot-suggest` to get initial structural analysis

If the decomposition log is not found, report error and suggest running `decompose-plan` first.

## bv Integration

The `bv` (beads viewer) tool provides structural analysis features:

| bv Command | Use Case |
|------------|----------|
| `bv --robot-suggest --suggest-type=duplicate` | Detect potential duplicate beads |
| `bv --robot-suggest --suggest-type=dependency` | Find missing dependencies |
| `bv --robot-suggest --suggest-type=cycle` | Detect circular dependencies |
| `bv --robot-related <bead-id>` | Find related beads by file/commit overlap |
| `bv --search "requirement" --robot-search` | Semantic matching for coverage validation |

Run `bv --robot-suggest` early to get a baseline of structural issues.

## Validation Checks

Perform these four validation checks in order:

1. **Self-Containment** - Does each bead have all required sections?
2. **Spec Coverage** - Is every spec requirement covered by at least one bead?
3. **Orphan Detection** - Does every bead trace back to a spec requirement?
4. **Dependency Validity** - Are dependencies correct, acyclic, and complete?

## Check 1: Self-Containment Validation

Each bead must pass the "future self" test: Would someone reading ONLY this bead understand what to do, why to do it, and how to verify it's done?

### Required Sections (MUST have)

| Section | Purpose | Fix if Missing |
|---------|---------|----------------|
| **Task** | Clear, actionable statement | Pull from spec or infer from title |
| **Acceptance Criteria** | Specific, testable criteria with verification commands | Extract from spec requirements |

### Recommended Sections (SHOULD have, warn if missing)

| Section | Purpose | Enhancement Source |
|---------|---------|-------------------|
| Background & Reasoning | Why this exists, project context | Original spec introduction |
| Key Files | Files to create/modify | Infer from task or related beads |
| Implementation Details | Patterns, APIs, integration points | Related beads, spec details |
| Considerations & Edge Cases | Gotchas, security, performance | Spec caveats, inference |
| Notes for Future Self | Helpful context | Spec footnotes, inference |

### Fix Process

```
For each bead:
  1. Parse description for section headers
  2. If missing REQUIRED section:
     a. Search spec for relevant content
     b. Check related beads for patterns
     c. Infer from task title if needed
     d. If still unclear, use AskUserQuestion to gather info
     e. Run: br update <id> --description="<enhanced description>"
  3. If missing RECOMMENDED section:
     a. Pull from spec/related beads/inference
     b. Update bead with enhanced content
  4. Log all changes made
```

## Check 2: Spec Coverage Validation

Every requirement in the spec must be traceable to at least one bead.

### Using bv Semantic Search

```bash
# For each requirement, find matching beads
bv --search "user authentication with email" --robot-search --search-limit=5
```

### Validation Process

```
1. Parse spec into discrete requirements (bullets, numbered items, headers)
2. For each requirement:
   a. Run: bv --search "<requirement text>" --robot-search
   b. If high-relevance match (score > 0.7) → Mark as covered, record mapping
   c. If low/no match → Flag as coverage gap
3. For each coverage gap:
   a. Create new bead with full context from spec
   b. Use bead-template.md format
   c. Run: br create --title="<requirement>" --type=task --description="..."
   d. Establish dependencies to related beads
```

### Coverage Report Format

```markdown
## Coverage Analysis
| Spec Requirement | Covered By | Status |
|------------------|------------|--------|
| User login with email | br-101, br-102 | Covered |
| Password reset flow | - | GAP - Created br-107 |
```

## Check 3: Orphan Work Detection

Every bead must trace back to a spec requirement. However, implementation beads that SUPPORT spec requirements are valid.

### Valid vs Invalid Orphans

| Bead | Spec Says | Status |
|------|-----------|--------|
| "Setup database connection" | "Persist user data" | Valid (supports requirement) |
| "Add email notification system" | No mention of email | Potential scope creep |

### Detection Process

```
For each bead:
  1. Search spec for direct matches of bead task
  2. If direct match → Valid
  3. If no direct match, check if it SUPPORTS a requirement:
     - Database/infrastructure beads supporting persistence
     - Auth middleware supporting security requirements
     - Utility functions supporting multiple features
  4. If neither → Flag as potential scope creep
```

### Handling Orphans

- If bead supports a requirement → Add note explaining the relationship
- If truly orphan → Remove with `br delete <id>` or flag for manual review

## Check 4: Dependency Validity

Use bv tools to validate the dependency graph.

### Structural Analysis

```bash
# Get all suggestions
bv --robot-suggest

# Specific checks
bv --robot-suggest --suggest-type=cycle
bv --robot-suggest --suggest-type=dependency
bv --robot-suggest --suggest-type=duplicate

# Find related beads for potential links
bv --robot-related <bead-id>
```

### Checks Performed

| Issue | Detection | Resolution |
|-------|-----------|------------|
| Cycles | `bv --robot-suggest --suggest-type=cycle` | Report for manual resolution |
| Missing deps | `bv --robot-suggest --suggest-type=dependency` | Auto-add if confidence > 0.7 |
| Epic direction | Parse epic beads, check dep direction | Fix with `br dep remove` + `br dep add` |
| Duplicates | `bv --robot-suggest --suggest-type=duplicate` | Merge or flag for review |

### Epic Dependency Direction (CRITICAL)

```bash
# CORRECT: Epic depends on children (children are READY)
br dep add <epic-id> <child-id>

# WRONG: This blocks children forever!
br dep add <child-id> <epic-id>  # FIX THIS IF FOUND
```

### Fix Process

```
1. For reversed epic deps:
   br dep remove <child-id> <epic-id>
   br dep add <epic-id> <child-id>

2. For missing deps (confidence > 0.7):
   br dep add <dependent-id> <dependency-id>

3. For cycles:
   Report for manual resolution (too complex for auto-fix)

4. For duplicates:
   Report with similarity score, suggest merge
```

## Using AskUserQuestion

When a bead fails the "future self" test and you cannot enhance it from available context:

```
AskUserQuestion(
  questions=[{
    "question": "The bead '<title>' lacks sufficient detail for implementation. <specific question>",
    "header": "<short header>",
    "options": [
      {"label": "Option A", "description": "Description of option A"},
      {"label": "Option B", "description": "Description of option B"}
    ],
    "multiSelect": false
  }]
)
```

After receiving the answer, update the bead with the clarified information and log the change.

## Auto-Fix Process

All fixes use `br update`:

```bash
# Update description with enhanced content
br update <id> --description="<full enhanced description>"

# Add new bead for coverage gap
br create --title="<title>" --type=task --priority=<0-4> --description="..."

# Fix dependencies
br dep add <dependent-id> <dependency-id>
br dep remove <wrong-dependent-id> <wrong-dependency-id>
```

### Enhancement Source Priority

When fixing self-containment issues, pull content in this order:

1. **Original spec (primary)** - Pull exact wording, context, requirements
2. **Related beads (secondary)** - Copy patterns from sibling beads in same epic
3. **Inference (tertiary)** - Use LLM judgment based on task title and context
4. **User clarification (fallback)** - Use AskUserQuestion when truly unclear

## Updating the Decomposition Log

After making any changes, update the decomposition log with a new section:

```markdown
## Validation Pass [N]

**Validated at:** 2026-01-22T14:30:00Z
**Issues found:** X
**Issues fixed:** Y
**Manual action required:** Z

### Self-Containment Fixes
- br-102: Added missing Acceptance Criteria from spec section 2.1
- br-105: Enhanced with Implementation Details from related br-104

### Coverage Gaps Filled
- Created br-113 for "Password reset via email" (was uncovered)
  - Dependencies: br-113 → br-101 (needs auth middleware)

### Orphan Resolution
- br-110: Documented as supporting requirement 3.2 (persistence)

### Dependency Fixes
- Fixed reversed epic: br-100 now depends on br-101 (was wrong direction)
- Added missing: br-105 → br-102 (confidence 0.85)

### User Clarifications
- Authentication method: JWT tokens (user selected)
  - Updated br-101, br-102 with JWT implementation details

### Remaining Issues (Manual Review Required)
- Cycle detected: br-108 → br-109 → br-108
```

## Validation Report Output

Write the validation report to the decomposition log (update it, don't create a separate file).

### Report Sections

1. **Summary table** - Pass/Fail/Fixed counts by check type
2. **bv Analysis Results** - Duplicates, missing deps, cycles found
3. **Issues & Resolutions** - Detailed list of what was found and fixed
4. **Final State** - Overall validation status

## Guidelines

### DO
- Read the ENTIRE spec before validating
- Use bv tools for structural analysis
- Auto-fix issues when confident
- Use AskUserQuestion when specifications are unclear
- Create missing beads for coverage gaps
- Document all decisions in the decomposition log
- Ensure each bead passes the "future self" test

### DON'T
- Skip any of the four validation checks
- Leave required sections missing
- Ignore bv suggestions without reviewing
- Create empty or skeleton beads for gaps
- Auto-fix cycles (report for manual review)
- Re-validate priorities (trust decompose-plan)

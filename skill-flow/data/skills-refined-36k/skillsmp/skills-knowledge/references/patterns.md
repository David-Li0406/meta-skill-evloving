# Skill Refinement Patterns

## Table of Contents

- [Pattern 1: Add Mandatory URL Fetching](#pattern-1-add-mandatory-url-fetching)
- [Official Documentation](#official-documentation)
- [🚨 MANDATORY: Read BEFORE Proceeding](#mandatory-read-before-proceeding)
- [Pattern 2: Improve Skill Triggers](#pattern-2-improve-skill-triggers)
- [Pattern 3: Enhance Progressive Disclosure](#pattern-3-enhance-progressive-disclosure)
- [Quick Start](#quick-start)
- [Key Concepts](#key-concepts)
- [Pattern 4: Fix Skill Autonomy](#pattern-4-fix-skill-autonomy)
- [Generate Report](#generate-report)
- [Generate Report](#generate-report)
- [Executive summary](#executive-summary)
- [Key findings](#key-findings)
- [Recommendations](#recommendations)
- [Pattern 5: Add Workflow Checklists](#pattern-5-add-workflow-checklists)
- [Database Migration](#database-migration)
- [Database Migration](#database-migration)
- [Pattern 6: Implement Feedback Loops](#pattern-6-implement-feedback-loops)
- [Edit Configuration](#edit-configuration)
- [Edit Configuration](#edit-configuration)
- [Pattern 7: Add Argument Validation](#pattern-7-add-argument-validation)
- [Validate Environment](#validate-environment)
- [Deployment Steps](#deployment-steps)
- [Pattern 8: Create Template Patterns](#pattern-8-create-template-patterns)
- [Generate Summary](#generate-summary)
- [Generate Summary](#generate-summary)
- [Overview](#overview)
- [Key Points](#key-points)
- [Next Steps](#next-steps)
- [Pattern 9: Add Examples Pattern](#pattern-9-add-examples-pattern)
- [Create Commit Message](#create-commit-message)
- [Commit Message Format](#commit-message-format)
- [Pattern 10: Fix Tool Restrictions](#pattern-10-fix-tool-restrictions)
- [Pre-flight Checks](#pre-flight-checks)
- [Deploy](#deploy)
- [Verify](#verify)
- [Pattern 11: Implement Progressive Disclosure](#pattern-11-implement-progressive-disclosure)
- [Pattern 12: Add Hard Preconditions](#pattern-12-add-hard-preconditions)
- [Setup](#setup)
- [🚨 Hard Preconditions (BLOCKING)](#hard-preconditions-blocking)
- [Pattern 13: Create Domain Organization](#pattern-13-create-domain-organization)
- [Available Datasets](#available-datasets)
- [Quick Search](#quick-search)
- [Pattern 14: Add Conditional Workflows](#pattern-14-add-conditional-workflows)
- [Process Data](#process-data)
- [Process Data](#process-data)
- [Pattern 15: Implement Error Recovery](#pattern-15-implement-error-recovery)
- [Deploy](#deploy)
- [Deploy](#deploy)
- [Pattern 16: Add Visual Analysis](#pattern-16-add-visual-analysis)
- [Analyze Image](#analyze-image)
- [Analyze Image](#analyze-image)
- [Pattern 17: Create Verifiable Outputs](#pattern-17-create-verifiable-outputs)
- [Generate Report](#generate-report)
- [Generate Report](#generate-report)
- [Pattern 18: Bundle Dependencies](#pattern-18-bundle-dependencies)
- [Use Library](#use-library)
- [Dependencies](#dependencies)
- [Pattern 19: Add Tool-Specific Guidance](#pattern-19-add-tool-specific-guidance)
- [Search](#search)
- [Search](#search)
- [Pattern 20: Create Evaluation Checks](#pattern-20-create-evaluation-checks)
- [Test Skill](#test-skill)
- [Test Skill](#test-skill)
- [Applying Patterns](#applying-patterns)
- [Pattern Catalog Summary](#pattern-catalog-summary)
- [Anti-Patterns to Avoid](#anti-patterns-to-avoid)
- [Best Practices Summary](#best-practices-summary)

Common patterns for improving skill quality and addressing specific issues.

## Pattern 1: Add Mandatory URL Fetching

**Problem**: Skill missing required URL fetching sections

**Before**:
```markdown
## Official Documentation

Start Here: https://code.claude.com/docs/en/skills
```

**After**:
```markdown
## 🚨 MANDATORY: Read BEFORE Proceeding

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Official Skills Guide**: https://code.claude.com/docs/en/skills
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any skill creation
  - **Content**: Skills architecture, progressive disclosure
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
```

**Implementation**:
1. Add "🚨 MANDATORY" header
2. Include MUST READ section with URLs
3. Specify tool (simpleWebFetch preferred)
4. Add cache recommendation
5. Include blocking rules

## Pattern 2: Improve Skill Triggers

**Problem**: Description too generic, poor auto-discovery

**Before**:
```yaml
description: "Use when creating skills"
```

**After**:
```yaml
description: "Create self-sufficient skills following Agent Skills standard. Use when building autonomous capabilities with progressive disclosure. Do not use for general programming or non-Claude contexts."
```

**Improvements**:
- WHAT: "Create self-sufficient skills"
- WHEN: "Use when building autonomous capabilities"
- NOT: "Do not use for general programming"
- Includes specific keywords: "Agent Skills", "progressive disclosure"

## Pattern 3: Enhance Progressive Disclosure

**Problem**: SKILL.md too long, no Tier 3 content

**Before**:
```markdown
# Skill Name

[500+ lines of content in one file]
```

**After**:
```markdown
# Skill Name

Build [capability] using official documentation for always-current best practices.

## Quick Start
[Essential workflow]

## Key Concepts
[Brief overview]

See [references/detailed.md](references/detailed.md) for complete guide.
```

**Implementation**:
1. Keep SKILL.md under 200 lines
2. Create references/ directory
3. Move detailed content to reference files
4. Link from SKILL.md
5. Add table of contents for 100+ line files

## Pattern 4: Fix Skill Autonomy

**Problem**: Skill requires too many questions

**Before**:
```markdown
## Generate Report

Create a report based on user requirements.

[No specific guidance, asks many questions]
```

**After**:
```markdown
## Generate Report

Use this template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1
- Finding 2
- Finding 3

## Recommendations
1. Actionable item
2. Actionable item
```

Always include:
- Specific templates
- Clear steps
- Expected outputs
- Validation criteria
```

## Pattern 5: Add Workflow Checklists

**Problem**: Complex workflows without structure

**Before**:
```markdown
## Database Migration

Run migration scripts and verify.
```

**After**:
```markdown
## Database Migration

Copy this checklist and track progress:

```
Migration Progress:
- [ ] Step 1: Backup database
- [ ] Step 2: Run migration script
- [ ] Step 3: Verify data integrity
- [ ] Step 4: Update application config
- [ ] Step 5: Test functionality
```

**Step 1: Backup database**
!`pg_dump production_db > backup.sql`

**Step 2: Run migration script**
!`psql production_db < migration_v2.sql`

Continue with remaining steps...
```

**Benefits**:
- Clear progress tracking
- Prevents skipping steps
- Easy verification
- Structured approach

## Pattern 6: Implement Feedback Loops

**Problem**: No validation or error handling

**Before**:
```markdown
## Edit Configuration

Modify the config file as needed.
```

**After**:
```markdown
## Edit Configuration

1. Modify config: Edit config.yaml
2. **Validate immediately**: Run validation script
3. If validation fails:
   - Review error message
   - Fix issues
   - Re-validate
4. **Only proceed when validation passes**
5. Test configuration

**Validation**:
```bash
./scripts/validate-config.sh config.yaml
```

The validation loop catches errors early.
```

## Pattern 7: Add Argument Validation

**Problem**: No argument validation

**Before**:
```yaml
---
name: deploy
description: "Deploy to environment"
---

Deploy to $ARGUMENTS:
```

**After**:
```yaml
---
name: deploy
description: "Deploy to environment"
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $ARGUMENTS:

## Validate Environment
!`echo "$ARGUMENTS" | grep -E "^(dev|staging|prod)$"`

If validation fails, report error and stop.

## Deployment Steps
[Steps...]
```

**Improvements**:
- Validate arguments before proceeding
- Provide specific error messages
- Stop on validation failure

## Pattern 8: Create Template Patterns

**Problem**: Inconsistent output formats

**Before**:
```markdown
## Generate Summary

Summarize the findings.
```

**After**:
```markdown
## Generate Summary

ALWAYS use this template:

```markdown
# Summary: [Topic]

## Overview
[2-3 sentence overview]

## Key Points
- Point 1 with data
- Point 2 with data
- Point 3 with data

## Next Steps
1. Action item
2. Action item
```
```

## Pattern 9: Add Examples Pattern

**Problem**: No concrete examples

**Before**:
```markdown
## Create Commit Message

Follow conventional commits format.
```

**After**:
```markdown
## Commit Message Format

Follow these examples:

**Example 1:**
Input: Added user authentication
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed date formatting bug
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies
Output:
```
chore: update dependencies

- Upgrade lodash to 4.17.21
- Standardize error response format
```

Follow this style: type(scope): brief description, then detailed explanation.
```

## Pattern 10: Fix Tool Restrictions

**Problem**: No tool restrictions for safety

**Before**:
```yaml
---
name: deploy
description: "Deploy to production"
---

# Deploy to production
!`kubectl apply -f production.yaml`
```

**After**:
```yaml
---
name: deploy
description: "Deploy to production"
disable-model-invocation: true
allowed-tools: Bash(kubectl:*), Bash(docker:*), Read
---

# Deploy to production

## Pre-flight Checks
- Verify environment: Read .env
- Check tests: !`npm test`

## Deploy
!`kubectl apply -f k8s/production.yaml`

## Verify
!`kubectl rollout status deployment/app`

Report status after each step.
```

## Pattern 11: Implement Progressive Disclosure

**Problem**: No progressive disclosure structure

**Before**:
```
skill-name/
└── SKILL.md (800 lines)
```

**After**:
```
skill-name/
├── SKILL.md (150 lines)
│   - Quick reference
│   - Links to detailed docs
│
├── references/
│   ├── detailed-guide.md (300 lines)
│   ├── examples.md (200 lines)
│   ├── troubleshooting.md (150 lines)
│   └── advanced.md (250 lines)
│
└── scripts/
    ├── validate.sh
    └── helper.py
```

**Tier Distribution**:
- **Tier 1**: Metadata (~100 tokens)
- **Tier 2**: SKILL.md (150 lines)
- **Tier 3**: references/ + scripts/ (loaded on-demand)

## Pattern 12: Add Hard Preconditions

**Problem**: No validation of prerequisites

**Before**:
```markdown
## Setup

Install dependencies and configure environment.
```

**After**:
```markdown
## 🚨 Hard Preconditions (BLOCKING)

**Before using this skill, you MUST**:

1. **[REQUIRED] Install dependencies**
   ```bash
   npm install
   ```
   - FAILURE: "DEPENDENCIES_REQUIRED - Run npm install"

2. **[REQUIRED] Configure environment**
   ```bash
   cp .env.example .env
   ```
   - FAILURE: "ENV_NOT_CONFIGURED - Copy .env.example to .env"

3. **[REQUIRED] Validate setup**
   ```bash
   ./scripts/validate-setup.sh
   ```
   - FAILURE: "SETUP_INVALID - Fix validation errors"

**Cannot proceed without satisfying all preconditions.**
```

## Pattern 13: Create Domain Organization

**Problem**: No organization by domain/context

**Before**:
```markdown
# API Review

[All API concepts in one file]
```

**After**:
```markdown
# API Review

## Available Datasets

**REST APIs**: Example: [reference/rest.md](reference/rest.md)
**GraphQL**: Example: [reference/graphql.md](reference/graphql.md)
**Webhooks**: Example: [reference/webhooks.md](reference/webhooks.md)

## Quick Search

Find specific topics:
```bash
grep -i "authentication" reference/*.md
grep -i "pagination" reference/*.md
```
```

**Structure**:
- Organize by domain
- Clear navigation
- Quick search capability
- One level deep references

## Pattern 14: Add Conditional Workflows

**Problem**: One-size-fits-all workflow

**Before**:
```markdown
## Process Data

Apply standard processing pipeline.
```

**After**:
```markdown
## Process Data

1. Determine data type:

   **JSON data?** → Follow JSON workflow
   **CSV data?** → Follow CSV workflow
   **XML data?** → Follow XML workflow

2. JSON workflow:
   - Validate schema
   - Transform data
   - Export to database

3. CSV workflow:
   - Parse CSV
   - Validate columns
   - Import to database

4. XML workflow:
   - Parse XML
   - Extract elements
   - Transform to JSON
```

## Pattern 15: Implement Error Recovery

**Problem**: No recovery from failures

**Before**:
```markdown
## Deploy

Run deployment commands.
```

**After**:
```markdown
## Deploy

1. Build application: !`npm run build`
2. If build fails:
   - Check error messages
   - Fix compilation errors
   - Re-run build

3. Deploy to staging: !`kubectl apply -f staging.yaml`
4. If deployment fails:
   - Check resource availability
   - Verify credentials
   - Run deployment rollback: !`kubectl rollout undo`

5. Verify deployment: !`kubectl rollout status`
6. If verification fails:
   - Check pod status: !`kubectl get pods`
   - Review logs: !`kubectl logs deployment/app`
   - Fix issues and redeploy

Each step includes recovery instructions.
```

## Pattern 16: Add Visual Analysis

**Problem**: No visual processing guidance

**Before**:
```markdown
## Analyze Image

Look at the image and report findings.
```

**After**:
```markdown
## Analyze Image

1. Convert image to analysis format:
   ```bash
   python scripts/prepare-image.py input.jpg
   ```

2. Analyze visual elements:
   - Layout and structure
   - Color scheme and design
   - Text content and readability
   - UI/UX patterns

3. Report findings with specific observations

**Note**: Use image analysis for:
- Document layouts
- UI screenshots
- Design mockups
- Visual comparisons
```

## Pattern 17: Create Verifiable Outputs

**Problem**: No way to verify output quality

**Before**:
```markdown
## Generate Report

Create a report with findings.
```

**After**:
```markdown
## Generate Report

1. Create initial report: Generate report.md
2. **Validate immediately**: Run validation script
   ```bash
   ./scripts/validate-report.sh report.md
   ```
3. If validation fails:
   - Missing sections? → Add required sections
   - Invalid format? → Fix formatting
   - Missing data? → Add data
   - Re-validate
4. **Only proceed when validation passes**
5. Output final report

**Validation checks**:
- All required sections present
- Executive summary < 100 words
- Data points include sources
- Recommendations are actionable
```

## Pattern 18: Bundle Dependencies

**Problem**: No documentation of requirements

**Before**:
```markdown
## Use Library

Use the pdf library for processing.
```

**After**:
```markdown
## Dependencies

Install required packages:
```bash
pip install pypdf pdfplumber
```

**Verify installation**:
```bash
python -c "import pypdf, pdfplumber; print('OK')"
```

**Package versions**:
- pypdf >= 3.0.0
- pdfplumber >= 0.9.0

**Note**: If packages unavailable in your environment, use alternative approaches.
```

## Pattern 19: Add Tool-Specific Guidance

**Problem**: Generic tool recommendations

**Before**:
```markdown
## Search

Use search tools to find information.
```

**After**:
```markdown
## Search

**Use Grep for**:
- Code searches: `Grep "pattern" type: py`
- File finding: `Glob "**/*.js"`

**Use WebSearch for**:
- Current information: `WebSearch "latest React trends 2026"`
- Specific queries: `WebSearch "PCI DSS requirements"`

**Use MCP tools**:
- Structured data: `MCP:search_web`
- API access: `MCP:database_query`

Choose the right tool for the search type.
```

## Pattern 20: Create Evaluation Checks

**Problem**: No way to measure success

**Before**:
```markdown
## Test Skill

Verify skill works correctly.
```

**After**:
```markdown
## Test Skill

Create test scenarios:

**Test 1: Auto-discovery**
- Trigger: "API design review"
- Expected: Skill auto-activates
- Pass/Fail: [ ]

**Test 2: Manual invocation**
- Trigger: /api-review
- Expected: Skill executes
- Pass/Fail: [ ]

**Test 3: Completeness**
- Query: Review this API design
- Expected: All checklist items covered
- Pass/Fail: [ ]

**Test 4: Autonomy**
- Query: Review API without additional input
- Expected: Completes without questions
- Pass/Fail: [ ]

Record results and address failures.
```

## Applying Patterns

### Pattern Selection

**Choose patterns based on issues**:
- URL fetching missing? → Pattern 1
- Poor auto-discovery? → Pattern 2
- SKILL.md too long? → Pattern 3, 11
- Requires too many questions? → Pattern 4
- No structure? → Pattern 5
- No validation? → Pattern 6, 17
- Inconsistent output? → Pattern 8
- No examples? → Pattern 9
- Security concerns? → Pattern 10
- Missing prerequisites? → Pattern 12

### Implementation Order

1. **Critical patterns first** (URL fetching, security)
2. **Structural patterns** (progressive disclosure)
3. **Quality patterns** (autonomy, examples)
4. **Enhancement patterns** (advanced features)

### Testing After Changes

After applying patterns:
1. Test auto-discovery
2. Verify manual invocation
3. Check autonomy
4. Validate progressive disclosure
5. Re-run quality audit

## Pattern Catalog Summary

| Pattern           | Purpose              | When to Use          |
| ----------------- | -------------------- | -------------------- |
| 1: URL Fetching   | Add mandatory docs   | Always               |
| 2: Triggers       | Improve discovery    | If poor activation   |
| 3: Progressive    | Reduce SKILL.md size | If >500 lines        |
| 4: Autonomy       | Reduce questions     | If requires input    |
| 5: Checklists     | Structure workflows  | For complex tasks    |
| 6: Feedback       | Add validation       | For quality-critical |
| 7: Arguments      | Validate inputs      | If accepts args      |
| 8: Templates      | Standardize output   | For consistency      |
| 9: Examples       | Show concrete cases  | Always               |
| 10: Security      | Restrict tools       | For safety           |
| 11: Structure     | Organize content     | For complexity       |
| 12: Preconditions | Validate setup       | For prerequisites    |
| 13: Domain        | Organize by context  | For large skills     |
| 14: Conditional   | Multiple paths       | For variations       |
| 15: Recovery      | Handle failures      | For robustness       |
| 16: Visual        | Process images       | For visual content   |
| 17: Verify        | Check outputs        | For quality          |
| 18: Dependencies  | Document needs       | For requirements     |
| 19: Tools         | Guide selection      | For tool choice      |
| 20: Evaluation    | Measure success      | Always               |

## Anti-Patterns to Avoid

### Anti-Pattern: Over-Documentation
**Problem**: Explaining concepts Claude already knows
**Solution**: Challenge every piece of information

### Anti-Pattern: Over-Engineering
**Problem**: Complex patterns for simple needs
**Solution**: Use appropriate complexity level

### Anti-Pattern: Over-Restriction
**Problem**: Too many tool restrictions
**Solution**: Balance safety and flexibility

### Anti-Pattern: Under-Example
**Problem**: Too few examples
**Solution**: Include concrete, varied examples

### Anti-Pattern: No Validation
**Problem**: No way to verify quality
**Solution**: Add validation and feedback loops

## Best Practices Summary

### DO ✅
- Use specific patterns to address issues
- Test changes thoroughly
- Start with critical patterns
- Document pattern selection rationale
- Re-audit after applying patterns
- Share patterns with team

### DON'T ❌
- Don't apply patterns randomly
- Don't skip testing after changes
- Don't over-engineer solutions
- Don't ignore pattern purpose
- Don't skip validation steps
- Don't apply all patterns at once

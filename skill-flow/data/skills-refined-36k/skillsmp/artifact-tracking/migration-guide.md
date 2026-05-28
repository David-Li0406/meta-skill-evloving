---
title: "Tracking Artifacts - Migration & Validation Guide"
description: "Step-by-step guide for migrating existing artifacts to YAML+Markdown format and validating implementation"
audience: [ai-agents, developers, architects]
tags: [migration, validation, implementation, artifacts]
created: 2025-11-15
updated: 2025-11-15
category: "ai-artifacts"
status: "published"
related:
  - /ai/TRACKING-ARTIFACTS-DESIGN.md
  - /ai/TRACKING-ARTIFACTS-QUICK-REFERENCE.md
---

# Tracking Artifacts - Migration & Validation Guide

## Overview

This guide covers:
1. **Migration Path** - How to convert existing markdown to YAML+Markdown format
2. **Manual Migration** - Step-by-step for small files
3. **Automated Migration** - Script approach for bulk conversion
4. **Validation Checklist** - How to verify correct implementation
5. **Rollback Plan** - How to revert if needed

---

## Migration Strategies

### Strategy 1: New Files Only (Recommended)

**Pros**: No disruption, incremental adoption, easy to rollback
**Cons**: Gradual efficiency gains, mix of formats
**Timeline**: Start immediately, build format portfolio over time

**Implementation**:
1. Create new progress/context files with YAML format
2. Leave existing files unchanged
3. Agents gradually migrate as they update files
4. After 3-4 weeks, most files will be new format

**Best for**: Starting fresh, low risk, gradual improvement

---

### Strategy 2: Hybrid Period (Balanced)

**Pros**: Better efficiency gains, controlled migration
**Cons**: Requires tooling, more planning
**Timeline**: Week 1 (design), Week 2 (tools), Week 3+ (migration)

**Implementation**:
1. Build migration utilities (scripts)
2. Automatically convert files to YAML+Markdown
3. Manually review converted files
4. Gradually move to new format over 2-3 weeks
5. Retire old format after transition

**Best for**: Teams wanting full efficiency gains, have tooling resources

---

### Strategy 3: Big Bang (Complete)

**Pros**: Full efficiency immediately, one conversion event
**Cons**: High risk, requires careful testing, potential disruption
**Timeline**: Week 1-2 (prep), Week 3 (migration), Week 4 (validation)

**Implementation**:
1. Create comprehensive migration script
2. Backup all files
3. Run migration on all artifacts simultaneously
4. Extensive testing and validation
5. Deploy to production

**Best for**: Well-resourced teams, high tolerance for change

---

## Detailed Migration: Strategy 2 (Recommended)

### Phase 1: Preparation (Week 1)

#### Step 1.1: Audit Existing Files

```bash
# Find all tracking artifacts
find .claude/progress -name "*.md" | wc -l
find .claude/worknotes -name "*.md" | wc -l

# Sample one of each type
cat .claude/progress/advanced-editing-v2/phase-1-progress.md
cat .claude/worknotes/blocks-v2/all-phases-context.md
cat .claude/worknotes/fixes/bug-fixes-tracking-11-25.md
cat .claude/worknotes/observations/observation-log-11-25.md
```

**Output**: Know how many files to migrate, understand current format

#### Step 1.2: Create Backup

```bash
# Backup all tracking artifacts
tar -czf .claude-backup-$(date +%Y%m%d).tar.gz .claude/
git add .claude-backup-*.tar.gz
git commit -m "Backup: Before artifact format migration"
```

#### Step 1.3: Document Mapping

Create mapping between old structure and new YAML schema:

```markdown
# Old Progress File Structure
- Status keywords in prose: ✅ DONE, ❌ BLOCKED, 🟡 IN PROGRESS
- Tasks: Manual parsing from "## TASK-X" headers
- Effort: Regex extract from "**Effort**: N story points"
- Assigned: Grep "**Assigned**: agent-name"

# New Progress File Structure
- Status: frontmatter.status = "complete" | "in-progress" | "blocked"
- Tasks: frontmatter.phases[0].tasks = [{ id, title, status, effort, ... }]
- Effort: task.effort = number
- Assigned: task.assigned = string

# Mapping Rules
- ✅ DONE → status: "complete"
- 🟡 IN PROGRESS → status: "in-progress"
- ❌ BLOCKED → status: "blocked"
```

---

### Phase 2: Tooling (Week 2)

#### Step 2.1: Create Migration Script

**File**: `scripts/migrate-artifact-to-yaml.js`

```javascript
#!/usr/bin/env node

/**
 * Migrate tracking artifact from pure markdown to YAML+Markdown format
 * Usage: node migrate-artifact-to-yaml.js <input-file> <type>
 * Types: progress, context, bug-fixes, observations
 */

import { readFileSync, writeFileSync } from 'fs'
import { stringify as stringifyYaml } from 'yaml'
import matter from 'gray-matter'

const ARTIFACT_TYPES = {
  'progress': {
    required_fields: ['type', 'prd', 'phase', 'status', 'overall_progress'],
    defaults: {
      type: 'progress',
      overall_progress: 0,
      total_tasks: 0,
      completed_tasks: 0,
      owners: []
    }
  },
  'context': {
    required_fields: ['type', 'prd', 'status'],
    defaults: {
      type: 'context',
      blockers: [],
      gotchas: [],
      decisions: []
    }
  },
  'bug-fixes': {
    required_fields: ['type', 'month', 'year'],
    defaults: {
      type: 'bug-fixes',
      severity_breakdown: { critical: 0, high: 0, medium: 0, low: 0 }
    }
  },
  'observations': {
    required_fields: ['type', 'month', 'year'],
    defaults: {
      type: 'observations',
      observation_counts: {}
    }
  }
}

function migrateArtifact(inputPath, type) {
  console.log(`Migrating ${inputPath} as type: ${type}`)

  // 1. Read file
  const content = readFileSync(inputPath, 'utf-8')
  const { data: existingFrontmatter, content: body } = matter(content)

  // 2. Create new frontmatter from schema defaults
  const defaults = ARTIFACT_TYPES[type]?.defaults || {}
  const newFrontmatter = {
    ...defaults,
    ...existingFrontmatter
  }

  // 3. Validate required fields
  const required = ARTIFACT_TYPES[type]?.required_fields || []
  const missing = required.filter(f => !newFrontmatter[f])
  if (missing.length > 0) {
    console.warn(`Warning: Missing required fields: ${missing.join(', ')}`)
  }

  // 4. Construct output
  const output = `---\n${stringifyYaml(newFrontmatter)}---\n\n${body}`

  // 5. Validate YAML
  try {
    matter(output) // This will error if YAML is invalid
    console.log('✓ YAML is valid')
  } catch (e) {
    console.error('✗ YAML validation failed:', e.message)
    return null
  }

  return output
}

// Main
const [inputPath, type] = process.argv.slice(2)
if (!inputPath || !type) {
  console.error('Usage: migrate-artifact-to-yaml.js <input-file> <type>')
  console.error('Types: progress, context, bug-fixes, observations')
  process.exit(1)
}

const migrated = migrateArtifact(inputPath, type)
if (migrated) {
  const outputPath = inputPath.replace(/\.md$/, '.migrated.md')
  writeFileSync(outputPath, migrated)
  console.log(`✓ Migrated to: ${outputPath}`)
  console.log('Please review and test before committing')
}
```

**Usage**:
```bash
# Migrate single file (creates .migrated.md)
node scripts/migrate-artifact-to-yaml.js .claude/progress/phase-1-progress.md progress

# Review output
diff .claude/progress/phase-1-progress.md .claude/progress/phase-1-progress.migrated.md

# If good, replace original
mv .claude/progress/phase-1-progress.migrated.md .claude/progress/phase-1-progress.md
```

#### Step 2.2: Create Validation Script

**File**: `scripts/validate-artifact-schema.js`

```javascript
#!/usr/bin/env node

/**
 * Validate artifact YAML schema
 * Usage: node validate-artifact-schema.js <file> [type]
 */

import { readFileSync } from 'fs'
import matter from 'gray-matter'

const SCHEMAS = {
  progress: {
    required: ['type', 'prd', 'phase', 'status'],
    enums: {
      type: ['progress'],
      status: ['planning', 'in-progress', 'review', 'complete', 'blocked']
    }
  },
  context: {
    required: ['type', 'prd', 'status'],
    enums: {
      type: ['context'],
      status: ['complete', 'blocked', 'in-progress']
    }
  },
  'bug-fixes': {
    required: ['type', 'month', 'year'],
    enums: {
      type: ['bug-fixes']
    }
  },
  observations: {
    required: ['type', 'month', 'year'],
    enums: {
      type: ['observations']
    }
  }
}

function validateArtifact(filePath, declaredType = null) {
  const content = readFileSync(filePath, 'utf-8')
  const { data } = matter(content)

  // Infer type from frontmatter
  const type = declaredType || data.type
  const schema = SCHEMAS[type]

  if (!schema) {
    console.error(`✗ Unknown artifact type: ${type}`)
    return false
  }

  let isValid = true

  // Check required fields
  for (const field of schema.required) {
    if (!data[field]) {
      console.error(`✗ Missing required field: ${field}`)
      isValid = false
    }
  }

  // Check enum values
  for (const [field, allowedValues] of Object.entries(schema.enums || {})) {
    if (data[field] && !allowedValues.includes(data[field])) {
      console.error(`✗ Invalid value for ${field}: ${data[field]}`)
      console.error(`   Allowed: ${allowedValues.join(', ')}`)
      isValid = false
    }
  }

  // Check type consistency
  if (data.type !== type) {
    console.error(`✗ Declared type mismatch: ${declaredType} vs ${data.type}`)
    isValid = false
  }

  if (isValid) {
    console.log(`✓ ${type} artifact is valid`)
  }

  return isValid
}

// Main
const [filePath, type] = process.argv.slice(2)
if (!filePath) {
  console.error('Usage: validate-artifact-schema.js <file> [type]')
  process.exit(1)
}

const isValid = validateArtifact(filePath, type)
process.exit(isValid ? 0 : 1)
```

**Usage**:
```bash
# Validate single file
node scripts/validate-artifact-schema.js .claude/progress/phase-1-progress.md

# Validate all progress files
for f in .claude/progress/**/*.md; do
  node scripts/validate-artifact-schema.js "$f" progress || exit 1
done

echo "✓ All artifacts are valid"
```

---

### Phase 3: Manual Migration (Week 2-3)

#### Step 3.1: Choose Files to Migrate

Start with 2-3 files of each type:

```bash
# Pick 1 progress file
# Pick 1 context file
# Pick 1 bug-fixes file
# Pick 1 observations file

# Total: 4 files to migrate first
```

#### Step 3.2: Migrate Each File

For each file:

1. **Backup the original**
   ```bash
   cp .claude/progress/phase-1-progress.md .claude/progress/phase-1-progress.backup.md
   ```

2. **Extract metadata from body**
   - Read prose to identify status, tasks, blockers
   - Convert prose descriptions to structured fields
   - Calculate counts (total_tasks, completed_tasks, etc.)

3. **Build YAML frontmatter**
   - Use template from quick reference
   - Fill in extracted metadata
   - Validate with YAML validator

4. **Preserve body content**
   - Keep all narrative text
   - Minor formatting: move task details from body to YAML
   - Keep overview, decisions, gotchas in body

5. **Example Conversion**

**Before** (Pure Markdown):
```markdown
# Advanced Editing V2 - Phase 1 Progress

**Phase**: Prompt Creation Modal Enhancements
**Status**: In Progress (35% complete)
**Duration**: 2 days
**Owner**: ui-engineer-enhanced

## Overview
Achieve parity between Prompt Creation, Editing, and Viewing flows...

## Phase 1: Prompt Creation Modal Enhancements

### Tasks

#### TASK-1.1: Add "Use Blocks" Button ✅
**Status**: Complete
**Assigned**: ui-engineer-enhanced
**Effort**: 3 story points
**Description**: Add "Use Blocks" button next to "Prompt Content" header...

#### TASK-1.2: Implement Tabs System
**Status**: In Progress
**Assigned**: ui-engineer-enhanced
**Effort**: 8 story points
```

**After** (YAML+Markdown):
```markdown
---
type: progress
prd: "advanced-editing-v2"
phase: 1
title: "Prompt Creation Modal Enhancements"
status: "in-progress"
overall_progress: 35
completion_estimate: "on-track"
total_tasks: 4
completed_tasks: 1
in_progress_tasks: 1
owners: ["ui-engineer-enhanced"]
contributors: []
blockers: []
success_criteria: [
  { id: "SC-1", description: "CreatePromptModal has tab system...", status: "pending" }
]
files_modified: ["apps/web/src/components/modals/CreatePromptModal/CreatePromptForm.tsx"]
---

# Advanced Editing V2 - Phase 1: Prompt Creation Modal Enhancements

**Phase**: 1 of 3
**Status**: In Progress (35% complete)
**Duration**: Started 2025-11-09, estimated completion 2025-11-18
**Owner**: ui-engineer-enhanced

## Overview
Achieve parity between Prompt Creation, Editing, and Viewing flows...

## Tasks

### TASK-1.1: Add "Use Blocks" Button

**Status**: ✅ Complete
**Assigned**: ui-engineer-enhanced
**Effort**: 3 story points
**Duration**: 2 hours
**Priority**: critical

**Description**: Add "Use Blocks" button next to "Prompt Content" header...

[Rest of body content...]
```

#### Step 3.3: Validate Migrated Files

```bash
# Validate YAML
node scripts/validate-artifact-schema.js .claude/progress/phase-1-progress.md

# Check diffs
diff .claude/progress/phase-1-progress.backup.md .claude/progress/phase-1-progress.md

# Manual review
cat .claude/progress/phase-1-progress.md | head -30
```

#### Step 3.4: Test with Query Helpers

```javascript
import { getPendingTasksForAgent } from './query-helpers'

// Test that queries work
const tasks = getPendingTasksForAgent(
  '.claude/progress/phase-1-progress.md',
  'ui-engineer-enhanced'
)

console.log(tasks)
// Should return: [{ id, title, status, effort, duration }]
```

---

### Phase 4: Bulk Migration (Week 3)

Once 4 files are validated:

```bash
# Migrate all progress files
for f in .claude/progress/**/phase-*.md; do
  node scripts/migrate-artifact-to-yaml.js "$f" progress
  # Review .migrated.md file
  # If good: mv "$f.migrated.md" "$f"
done

# Migrate all context files
for f in .claude/worknotes/**/phase-*-context.md; do
  node scripts/migrate-artifact-to-yaml.js "$f" context
done

# Migrate all bug-fix files
for f in .claude/worknotes/fixes/bug-fixes-*.md; do
  node scripts/migrate-artifact-to-yaml.js "$f" bug-fixes
done

# Migrate all observation files
for f in .claude/worknotes/observations/observation-log-*.md; do
  node scripts/migrate-artifact-to-yaml.js "$f" observations
done
```

---

## Validation Checklist

### Pre-Migration Checklist

- [ ] Backup all .claude/ files created
- [ ] Migration scripts reviewed and tested
- [ ] Team notified of upcoming migration
- [ ] Rollback plan documented
- [ ] Test environment prepared

### Post-Migration Validation

#### For Each Migrated File:

- [ ] YAML frontmatter is valid (no parsing errors)
- [ ] All required fields present
- [ ] Status values match enum (planning, in-progress, review, complete, blocked)
- [ ] Counts accurate (total_tasks == actual task count)
- [ ] Dates in ISO8601 format (YYYY-MM-DD)
- [ ] File paths are absolute, not relative
- [ ] No prose in structured fields (status, effort, dates)
- [ ] Body content preserved (nothing lost in conversion)
- [ ] No duplicate information (data in both frontmatter and body)

#### Query Helper Testing:

```javascript
// Test each query type with migrated files

// Progress file queries
getPendingTasksForAgent(file, 'agent-name')
getPhaseProgress(file)
getPhaseBlockers(file)
getSuccessCriteria(file)

// Context file queries
getAllBlockers(file)
getPhaseStatuses(file)
getGotchas(file)
getDecisions(file)

// Bug fix file queries
getCriticalBugFixes(file)
getBugFixesByComponent(file, 'component')
getBugFixesByDate(file, '2025-11-15')

// Observation file queries
getHighImpactObservations(file)
getObservationsByCategory(file, 'pattern-discoveries')
getObservationsByDate(file, '2025-11-15')

// All should return structured objects, not errors
```

#### Integration Testing:

- [ ] Agents can read and query migrated files
- [ ] Grep still works on body content
- [ ] GitHub renders YAML frontmatter correctly
- [ ] VSCode shows syntax highlighting
- [ ] File diffs are readable (meaningful changes only)
- [ ] Git blame still works

---

## Rollback Plan

If migration goes wrong:

### Immediate Rollback (Hour 0-1)

```bash
# Restore from backup
tar -xzf .claude-backup-$(date +%Y%m%d).tar.gz

# Commit rollback
git revert HEAD
git push

# Notify team
# Migration on hold, investigating issues
```

### Partial Rollback (If some files bad)

```bash
# Restore only affected files
git checkout HEAD~1 .claude/progress/bad-file.md

# Keep good files
# Fix issue with migration script
# Re-migrate carefully

git commit -m "Rollback: Revert bad migration for [file]"
```

### Prevention

- Test migration script thoroughly (on copies first)
- Validate each file before committing
- Migrate incrementally (not all at once)
- Keep backups for 1 week

---

## Common Issues & Fixes

### Issue 1: YAML Parse Error

**Error**: `Error: bad indentation of mapping value`

**Cause**: YAML indentation wrong, usually with nested arrays

**Fix**:
```yaml
# Wrong
blockers:
- id: "BLK-1"
title: "Title"

# Right
blockers:
  - id: "BLK-1"
    title: "Title"
```

### Issue 2: Missing Status Enum Value

**Error**: Status value "waiting" not recognized

**Cause**: Used custom status not in enum list

**Fix**: Use only: planning, in-progress, review, complete, blocked

### Issue 3: Query Returns Wrong Data

**Error**: Query for agent "ui-engineer" returns no results

**Cause**: Agent name doesn't match (typo or spacing)

**Fix**:
```javascript
// Check what's actually in file
const allTasks = frontmatter.phases[0].tasks
console.log(allTasks.map(t => t.assigned))  // See actual values

// Use exact match
const tasks = allTasks.filter(t => t.assigned === 'ui-engineer') // with hyphen
```

### Issue 4: Date Query Fails

**Error**: Query `getObservationsByDate(file, '2025-11-15')` returns empty

**Cause**: Date format mismatch (ISO timestamp vs YYYY-MM-DD)

**Fix**: Use ISO8601 format consistently
```javascript
// Right
{ date: "2025-11-15T10:30:00Z" }

// Query with date
observations.filter(o => o.date.startsWith('2025-11-15'))
```

---

## Post-Migration Steps

### After All Files Migrated

1. **Update Agent Prompts**
   - Document new YAML format
   - Provide query helper imports
   - Show example queries

2. **Update Templates**
   - Update progress file template with YAML frontmatter
   - Update context file template with YAML frontmatter
   - Share with team

3. **Train Agents**
   - Provide quick reference card
   - Show query examples
   - Demonstrate token efficiency gains

4. **Monitor Usage**
   - Track if agents are using new format
   - Collect feedback
   - Refine schema based on usage

5. **Retire Old Format**
   - After 4 weeks, old files should be migrated
   - Update templates to YAML-only
   - Document old format as deprecated

---

## Success Metrics

After migration, track:

| Metric | Target | How to Measure |
|--------|--------|-----------------|
| File Coverage | 90%+ of tracking files migrated | Count .md files with YAML frontmatter |
| Query Success | 95%+ query success rate | Run test suite on all migrated files |
| Token Efficiency | 95%+ average reduction | Measure bytes for common queries |
| Agent Adoption | 80%+ agents using new format | Survey agent usage |
| File Growth | < 5% monthly increase | Monitor .claude/ directory size |

---

## Timeline Summary

| Phase | Duration | Activities | Output |
|-------|----------|-----------|--------|
| 1: Prep | Week 1 | Audit, backup, map structure | Migration plan |
| 2: Tools | Week 2 | Build scripts, test | Migration tools |
| 3: Pilot | Week 2-3 | Migrate 4 test files | Validated examples |
| 4: Bulk | Week 3 | Migrate all files | All files converted |
| 5: Validate | Week 4 | Test, document, train | Ready for production |

**Total**: 3-4 weeks to full adoption

---

## Getting Help

For issues during migration:

- **YAML validation**: Use online YAML validator
- **Script errors**: Check Node.js version (need 16+)
- **Query issues**: Test with provided query-helpers.js
- **Format questions**: See TRACKING-ARTIFACTS-QUICK-REFERENCE.md

Contact `ai-artifacts-engineer` for complex issues.

---

## Appendix: Migration Checklist Template

Copy and fill out for each file:

```markdown
# Migration Checklist: [filename]

## Pre-Migration
- [ ] File backed up
- [ ] Artifact type identified: _____ (progress/context/bug-fixes/observations)
- [ ] Metadata extracted from prose

## During Migration
- [ ] YAML frontmatter created
- [ ] Required fields filled in
- [ ] Status values validated (enum check)
- [ ] Counts calculated and verified
- [ ] Body content preserved

## Post-Migration
- [ ] YAML validates (no parsing errors)
- [ ] Diffs reviewed (expected changes only)
- [ ] Query helpers tested successfully
- [ ] File renders correctly in GitHub/VSCode
- [ ] Ready to commit: YES / NO

## Issues Encountered
[List any issues and how resolved]

## Reviewer Sign-Off
- [ ] Reviewed by: _________________
- [ ] Date: _________________
- [ ] Status: APPROVED / NEEDS REWORK
```

---

**This guide ensures safe, validated migration to the new YAML+Markdown format.**

Last Updated: 2025-11-15 | Version: 1.0 | Status: Ready for Implementation

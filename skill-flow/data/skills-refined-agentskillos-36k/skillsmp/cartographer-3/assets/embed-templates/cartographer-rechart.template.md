<!--
Embedded Cartographer Command: rechart
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Write, Bash(mkdir:*), Bash(test:*), Bash(ls:*), Bash(git log:*), Bash(git diff:*), AskUserQuestion
argument-hint: [--full | --domain <name>]
description: Incrementally update atlas with change detection
---

## Context

Arguments: `/rechart [OPTIONS]`
- **--full** - Full regeneration
- **--domain <name>** - Update only specified domain
- **(empty)** - Smart incremental update

Current directory: !`pwd`

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found → Error: "No atlas found. Run `/chart` first."

**Load current schema:**
- Read `.claude/skills/atlas/references/schema.yaml`
- Extract metadata, domains, last updated timestamp

### 2. Detect Changes

**Parse mode:**
- `--full` → Skip detection, regenerate all
- `--domain <name>` → Focus on specific domain
- Empty → Detect changes automatically

**For automatic mode:**
```bash
git log --since="{last_updated}" --name-only --pretty=format: | sort | uniq
```

**Categorize:**
- New files/directories
- Deleted files
- Modified files

**Map to domains:**
- Identify affected domains
- Flag domains with >20% change

### 3. Re-analyze Affected Areas

**For full mode:** Analyze entire codebase (same as /chart)

**For domain mode:** Analyze only specified domain

**For automatic mode:**
- Analyze affected domains
- Preserve unchanged domains

### 4. Merge with Existing

**Merge strategy:**
- Unchanged domains: Keep existing
- Updated domains: Replace with new analysis
- New domains: Add
- Deleted domains: Remove or mark deprecated

**Handle customizations:**
If user has customized reference files:
- Detect customizations
- Ask: Keep customizations or regenerate?

### 5. Update Files

**Update schema.yaml:**
- Bump timestamp
- Update/add/remove domains
- Update file counts

**Update SKILL.md:**
- Regenerate domain router
- Update pattern router

**Update references:**
- Update modified domain references
- Create new domain references
- Remove deleted (or archive)

### 6. Report

```markdown
## Atlas Updated

**Mode:** {full|domain|incremental}

**Updates applied:**
- Domains updated: {list}
- Domains added: {list}
- Domains removed: {list}

**Next steps:**
- Run `/calibrate` to verify
```

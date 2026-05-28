---
model: sonnet
allowed-tools: Task, Glob, Grep, Read, Write, Bash(mkdir:*), Bash(test:*), Bash(ls:*), Bash(git log:*), Bash(git diff:*), AskUserQuestion
argument-hint: [--full | --domain <name>]
description: Incrementally update atlas with auto-migration support
---

## Context

Arguments: `/cartographer:rechart [OPTIONS]`
- **--full** - Full regeneration (equivalent to chart with overwrite)
- **--domain <name>** - Update only specified domain
- **(empty)** - Smart incremental update based on changes

Current directory: !`pwd`

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

If not found → Error: "No atlas found. Run `/cartographer:chart` first."

**Load current schema:**
- Read `.claude/skills/atlas/references/schema.yaml`
- Parse metadata, domains, patterns
- Extract last updated timestamp

**Check schema version:**
- If version incompatible → Trigger migration (see Migration section)

### 2. Detect Changes

**Parse mode from arguments:**
- `--full` → Skip change detection, do full regeneration
- `--domain <name>` → Focus on specific domain
- Empty → Detect changes automatically

**For automatic mode, detect changes since last update:**

```bash
# Get files changed since last update
git log --since="{last_updated}" --name-only --pretty=format: | sort | uniq
```

**Categorize changes:**
- New files/directories → May need new domains
- Deleted files → May invalidate domains
- Modified files → May affect counts/patterns

**Identify affected domains:**
- Map changed paths to documented domains
- Flag domains with >20% change

### 3. Invoke Surveyor Agent (Scoped)

**For full mode:**
```
Use surveyor agent to analyze entire codebase.
```

**For domain-specific mode:**
```
Use surveyor agent to analyze only:
- Domain: {domain_name}
- Path: {domain_path}

Focus on:
- File count accuracy
- Key files update
- Pattern changes within domain
```

**For automatic mode:**
```
Use surveyor agent to analyze:
- Affected domains: {list}
- New directories: {list}

Preserve unchanged domains from current schema.
```

### 4. Merge Analysis with Existing

**Merge strategy:**

1. **Unchanged domains:** Keep existing documentation
2. **Updated domains:** Replace with new analysis
3. **New domains:** Add from analysis
4. **Deleted domains:** Remove or mark deprecated

**For each domain:**
```
if domain in analysis AND domain in existing:
    if analysis.count differs by >10%:
        use analysis (updated)
    else:
        keep existing (preserve customizations)
elif domain in analysis only:
    add as new domain
elif domain in existing only:
    if path_exists(domain.location):
        keep existing
    else:
        mark for removal
```

### 5. Handle Conflicts

**If customizations detected in existing atlas:**
- User-added comments in reference files
- Custom domain descriptions
- Manual pattern additions

**Use AskUserQuestion:**
```
Domain "{name}" has been customized. The codebase shows different structure.

Customizations detected:
- {list of customizations}

Options:
1. Keep customizations, update counts only
2. Regenerate from analysis (lose customizations)
3. Review changes before deciding
```

### 6. Update Schema

**Update schema.yaml:**
1. Bump "Last Updated" timestamp
2. Update/add/remove domains
3. Update file pattern counts
4. Update config files if changed
5. Preserve validation commands

**Write to:** `.claude/skills/atlas/references/schema.yaml`

### 7. Update SKILL.md

**Regenerate domain router:**
- Add rows for new domains
- Remove rows for deleted domains
- Update keywords if purposes changed

**Regenerate pattern router:**
- Update based on current patterns

**Write to:** `.claude/skills/atlas/SKILL.md`

### 8. Update Domain References

**For updated domains:**
- Regenerate reference file
- Preserve user notes section if exists

**For new domains:**
- Generate new reference file

**For deleted domains:**
- Remove reference file
- Or archive to `.atlas-archive/` if has customizations

### 9. Update Pattern Guides

**Refresh pattern guides:**
- Update file counts
- Update examples if better ones found
- Add new patterns if detected

### 10. Validate Updated Atlas

**Run same validation as chart:**
- All paths exist
- No broken links
- Valid YAML

### 11. Report Results

```markdown
## Atlas Updated Successfully

**Mode:** {full|domain|incremental}
**Changes detected:** {count} files changed

**Updates applied:**
- Domains updated: {list}
- Domains added: {list}
- Domains removed: {list}
- Patterns updated: {list}

**Files modified:**
{list of changed files}

**Preserved customizations:**
{list if any}

**Next steps:**
- Run `/cartographer:health` to verify accuracy
```

---

## Migration Support

### Schema Version Detection

Check schema header for version:
```yaml
# Schema Version: 1.0.0
```

### Migration Rules

**1.0.0 → 1.1.0:**
- Add `task_mappings` section (can be empty)

**1.x → 2.0.0:**
- Restructure domains format
- Prompt user for manual review

### Migration Workflow

1. Detect version mismatch
2. Inform user: "Schema migration needed (v{old} → v{new})"
3. Create backup: `.claude/skills/atlas.backup/`
4. Apply migrations in order
5. Validate migrated schema
6. Report migration success/issues

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas found | Error message | Run /cartographer:chart |
| Schema parse error | Report parse issue | Manual fix or regenerate |
| Version incompatible | Trigger migration | Auto-migrate or manual |
| Merge conflicts | Interactive prompt | User decides |
| Validation fails | Report issues | Auto-fix or manual |

## Responsibilities

**YOU (handler):**
- Load and parse existing atlas
- Detect changes and scope
- Invoke surveyor with appropriate scope
- Merge analysis with existing
- Handle conflicts interactively
- Update all atlas files
- Validate and report

**Surveyor agent:**
- Analyze scoped codebase areas
- Return structured analysis

**You manage the merge logic. The surveyor only analyzes.**

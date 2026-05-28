---
name: swe-feature-update
version: 1.0.0
description: Update a specific feature's memory files to reflect current codebase state
workflow:
  aware: true
  callable_from:
    - WF_START
    - WF_CLASSIFY
    - WF_CONTINUE
  default_return: WF_START
  supports_standalone: true
  auto_transition: true
args:
  - name: key
    description: Feature key (REQUIRED - e.g., BLOCKS, THEME_DISTRICT)
    required: true
---

## ⚠️ WORKFLOW INITIALIZATION

**If starting a new session**, first read workflow initialization:
```
mcp__plugin_swe_serena__read_memory("WF_INIT")
```
Follow WF_INIT instructions before executing this skill.

---

# /swe-update-feature [KEY]

Update a specific feature's memory files to accurately reflect current codebase state.

## Usage

```bash
/swe-update-feature BLOCKS           # Update BLOCKS feature memories
/swe-update-feature THEME_DISTRICT   # Update THEME_DISTRICT feature memories
/swe-update-feature TESTS            # Update TESTS feature memories
```

## Purpose

Synchronize feature documentation with actual codebase:

- Update directory listings and file inventories
- Refresh architecture layers and patterns
- Update entry points and key files
- Sync related memories (ARCH_*, INDEX_*, DOM_*)

---

## Stage 1: Validate Feature

**Verify feature exists:**

```javascript
mcp__plugin_swe_serena__read_memory("INDEX_FEATURES")
```

**Check:** Feature key exists in registered features table.

**If not found:**
```
> Feature [KEY] not registered. Use /swe-feature-onboard [KEY] to register it first.
```
Exit skill with `needs_clarification` status.

---

## Stage 2: Load Current Feature Memory

```javascript
mcp__plugin_swe_serena__read_memory("FEATURE_[KEY]")
```

**Extract from current memory:**
- Root path(s)
- Primary language
- Framework
- Type
- Architecture layers
- Related memories list

---

## Stage 3: Analyze Current Codebase State

**For each root path in the feature:**

### 3.1 Directory Structure

```javascript
mcp__plugin_swe_serena__list_dir({ relative_path: "[root_path]", depth: 2 })
```

### 3.2 Key Files Inventory

```javascript
mcp__plugin_swe_serena__get_symbols_overview({ relative_path: "[root_path]" })
```

### 3.3 Pattern Detection

Use Serena tools to detect:
- Entry points (main files, index files)
- Configuration files
- Test files
- Template files

---

## Stage 4: Compare and Identify Changes

**Compare current state vs. documented state:**

| Aspect | Check For |
|--------|-----------|
| Directories | New directories, removed directories |
| Key files | New files, renamed files, removed files |
| Layers | Layer changes, new components |
| Dependencies | New internal/external dependencies |
| Entry points | Changed entry points |

**Report changes found:**
```
Changes detected for [KEY]:
- [+] Added: [new items]
- [-] Removed: [removed items]
- [~] Modified: [changed items]
```

---

## Stage 5: Update Feature Memory

### ⚠️ SPECIAL CASE: SWE Feature

When updating the **SWE** feature itself, memories follow a dual-location architecture:

1. **Edit FIRST** in the plugin folder: `.claude/plugins/serena-workflow-engine/memories/`
2. **Then sync** to local project using `/swe-sync`

This ensures changes are preserved in the portable plugin and propagated correctly.

**DO NOT** edit SWE memories directly in `.serena/memories/` - they will be overwritten on sync.

### 5.1 Update FEATURE_[KEY]

```javascript
mcp__plugin_swe_serena__write_memory("FEATURE_[KEY]", "<updated content>")
```

**Preserve:**
- Feature name and metadata
- Workflow context sections
- Related memories list

**Update:**
- Directory listings
- Key files table
- Architecture layers (if changed)
- Last updated timestamp

### 5.2 Update Related Memories (if needed)

Check and update as needed:
- `ARCH_[KEY]` - Architecture documentation
- `INDEX_[KEY]_*` - File/symbol indexes
- `DOM_[KEY]_*` - Domain documentation

**Only update if significant changes detected.**

---

## Stage 6: Summary Report

Output to user:

```markdown
## Feature Update Complete: [KEY]

### Changes Applied
- FEATURE_[KEY]: [summary of changes]
- [Other memories updated]: [summary]

### Current State
| Property | Value |
|----------|-------|
| Root Path(s) | [paths] |
| Key Files | [count] |
| Last Updated | [timestamp] |
```

---

## Skill Return

```markdown
## Skill Return
- **Skill**: swe-feature-update
- **Status**: success
- **Feature Key**: [KEY]
- **Memories Updated**: [list]
- **Changes Summary**: [brief description]
- **Next Step Hint**: WF_START
```

---

## Exit

```
> **Skill /swe-feature-update complete** - Feature [KEY] memories updated
```

---

## Troubleshooting

### Feature not found
```
Feature [KEY] is not registered in INDEX_FEATURES.
Run: /swe-feature-onboard [KEY]
```

### Root path doesn't exist
- Check if paths have moved
- Update FEATURE_[KEY] with correct paths
- Suggest re-onboarding if structure changed significantly

### No changes detected
```
> Feature [KEY] is up to date. No changes needed.
```
Exit with `success` status (no changes to make is still success).

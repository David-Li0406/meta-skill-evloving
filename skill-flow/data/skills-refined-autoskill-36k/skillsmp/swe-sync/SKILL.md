---
name: swe-sync
version: 1.0.0
description: Sync plugin memories to local project using ruv-swarm
workflow:
  aware: true
  callable_from:
    - WF_INIT
    - WF_START
    - WF_EXECUTE
    - WF_DONE
  default_return: WF_DONE
  supports_standalone: true
  auto_transition: false
args:
  - name: direction
    description: Sync direction - plugin-to-local (default), local-to-plugin, or bidirectional
    required: false
  - name: category
    description: Memory category to sync - wf, ref, all (default)
    required: false
  - name: dry-run
    description: Show what would be synced without making changes
    required: false
---

## ⚠️ WORKFLOW INITIALIZATION

**If starting a new session**, first read workflow initialization:
```
mcp__plugin_swe_serena__read_memory("WF_INIT")
```
Follow WF_INIT instructions before executing this skill.

---

# /swe-sync

Synchronize Serena memories between plugin and local project using ruv-swarm coordination.

## Usage

```
/swe-sync                           # Sync all memories plugin → local
/swe-sync --dry-run                 # Preview changes without syncing
/swe-sync category=wf               # Sync only WF_ workflow files
/swe-sync category=ref              # Sync only REF_ reference files
/swe-sync direction=local-to-plugin # Sync local changes back to plugin
```

## Process

### Step 1: Initialize Swarm

```javascript
// Initialize ruv-swarm with mesh topology
mcp__ruv-swarm__swarm_init({ topology: "mesh", strategy: "balanced", maxAgents: 5 })

// NOTE: daa_init is NOT needed here - we use agent_spawn + task_orchestrate pattern
// DAA is only needed when using daa_agent_create + daa_workflow_execute pattern
```

### Step 2: Spawn Comparison Agents

```javascript
// Spawn agents for parallel comparison
mcp__ruv-swarm__agent_spawn({ type: "analyst", name: "plugin-scanner", capabilities: ["file_analysis"] })
mcp__ruv-swarm__agent_spawn({ type: "analyst", name: "local-scanner", capabilities: ["file_analysis"] })
mcp__ruv-swarm__agent_spawn({ type: "coordinator", name: "diff-reporter", capabilities: ["synthesis"] })
```

### Step 3: Orchestrate Comparison Task

```javascript
mcp__ruv-swarm__task_orchestrate({
  task: "Compare memory files between plugin and local project",
  strategy: "parallel",
  priority: "high"
})
```

### Step 4: Execute File Comparison

**Plugin Path:** `.claude/plugins/serena-workflow-engine/memories/`
**Local Path:** `.serena/memories/`

**Categories:**
| Category | Pattern | Description |
|----------|---------|-------------|
| wf | `wf/WF_*.md` | Workflow state files |
| ref | `ref/REF_*.md` | Reference documentation |
| all | `*/*.md` | All memory files |

**Comparison Logic:**
```bash
# For each plugin file in category:
for file in plugin_path/category/*.md; do
  local_file="local_path/category/$(basename $file)"
  if [ ! -f "$local_file" ]; then
    echo "MISSING: $file"
  elif ! diff -q "$file" "$local_file"; then
    echo "DIFF: $file"
  fi
done

# Check for local-only files
for file in local_path/category/*.md; do
  plugin_file="plugin_path/category/$(basename $file)"
  if [ ! -f "$plugin_file" ]; then
    echo "LOCAL_ONLY: $file"
  fi
done
```

### Step 5: Report Results

Output a structured table:

```markdown
## Sync Report

| Category | File | Status | Action |
|----------|------|--------|--------|
| wf | WF_INIT.md | SYNCED | - |
| wf | WF_NEW.md | MISSING_LOCAL | Copy to local |
| ref | REF_WM.md | DIFF | Update local |
```

### Step 6: Execute Sync (if not dry-run)

**Direction: plugin-to-local (default)**
```bash
cp -f plugin_file local_file
```

**Direction: local-to-plugin**
```bash
cp -f local_file plugin_file
```

**Direction: bidirectional**
- Plugin newer → copy to local
- Local newer → copy to plugin
- Same age, different content → CONFLICT (report, don't overwrite)

### Step 7: Verify Sync

Re-run comparison to confirm all files synced.

## Exit

Output sync summary:
```
✅ Sync complete: X files synced, Y unchanged, Z conflicts
```

Return to calling workflow or end if standalone.

## Swarm Shutdown

```javascript
mcp__ruv-swarm__swarm_shutdown()
```

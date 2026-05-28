---
name: cleanup-health-inline
description: Use this skill when you need to orchestrate a workflow for detecting and removing dead code in your codebase, ensuring a systematic approach with priority-based cleanup and verification.
---

# Cleanup Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Beads Init → Detection → Create Issues → Remove by Priority → Close Issues → Verify → Beads Complete
```

**Max iterations**: 3  
**Priorities**: critical → high → medium → low  
**Beads integration**: Automatic issue tracking

---

## Phase 1: Pre-flight & Beads Init

1. **Setup directories**:
   ```bash
   mkdir -p .tmp/current/{plans,changes,backups}
   ```

2. **Validate environment**:
   - Check `package.json` exists
   - Check `type-check` and `build` scripts exist

3. **Create Beads wisp**:
   ```bash
   bd mol wisp exploration --vars "question=Dead code cleanup scan"
   ```
   **IMPORTANT**: Save the wisp ID (e.g., `mc2-xxx`) for later use.

4. **Initialize TodoWrite**:
   ```json
   [
     {"content": "Dead code detection", "status": "in_progress", "activeForm": "Detecting dead code"},
     {"content": "Create Beads issues", "status": "pending", "activeForm": "Creating issues"},
     {"content": "Remove critical dead code", "status": "pending", "activeForm": "Removing critical dead code"},
     {"content": "Remove high priority dead code", "status": "pending", "activeForm": "Removing high dead code"},
     {"content": "Remove medium priority dead code", "status": "pending", "activeForm": "Removing medium dead code"},
     {"content": "Remove low priority dead code", "status": "pending", "activeForm": "Removing low dead code"},
     {"content": "Verification scan", "status": "pending", "activeForm": "Verifying cleanup"},
     {"content": "Complete Beads wisp", "status": "pending", "activeForm": "Completing wisp"}
   ]
   ```

---

## Phase 2: Detection

**Invoke dead-code-hunter** via Task tool:

```
subagent_type: "dead-code-hunter"
description: "Detect all dead code"
prompt: |
  Scan the entire codebase for dead code:
  - Unused imports and exports
  - Commented out code blocks
  - Unreachable code
  - Debug statements (console.log, debugger)
  - Unused variables and functions
  - Unused dependencies
  - Categorize by priority (critical/high/medium/low)

  Generate: dead-code-report.md
```

**After dead-code-hunter returns**:
1. Read `dead-code-report.md`
2. Parse dead code counts by priority
3. If zero dead code → skip to Final Summary
4. Update TodoWrite: mark detection complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to removal
- If fail → report to user, exit

---

## Phase 4: Removal Loop

**For each priority** (critical, high, medium, low):
1. **Remove dead code** as per the priority.
2. **Close issues** in Beads for completed tasks.
3. **Verify** the cleanup by running the verification scan.

---

## Final Summary

1. **Complete Beads wisp** and document the results.
2. **Report** on the dead code counts and actions taken.
3. **End of workflow**.
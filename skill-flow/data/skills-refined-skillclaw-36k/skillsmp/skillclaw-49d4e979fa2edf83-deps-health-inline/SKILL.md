---
name: deps-health-inline
description: Use this skill when you need to perform a comprehensive dependency audit and update workflow, integrating with Beads for issue tracking and prioritization.
---

# Dependency Health Check (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Beads Init → Audit → Create Issues → Update by Priority → Close Issues → Verify → Beads Complete
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
   - Check lockfile exists (pnpm-lock.yaml, package-lock.json, yarn.lock)

3. **Create Beads wisp**:
   ```bash
   bd mol wisp exploration --vars "question=Dependency audit and update"
   ```
   **IMPORTANT**: Save the wisp ID (e.g., `mc2-xxx`) for later use.

4. **Initialize TodoWrite**:
   ```json
   [
     {"content": "Dependency audit", "status": "in_progress", "activeForm": "Auditing dependencies"},
     {"content": "Create Beads issues", "status": "pending", "activeForm": "Creating issues"},
     {"content": "Fix critical dependency issues", "status": "pending", "activeForm": "Fixing critical deps"},
     {"content": "Fix high priority dependency issues", "status": "pending", "activeForm": "Fixing high deps"},
     {"content": "Fix medium priority dependency issues", "status": "pending", "activeForm": "Fixing medium deps"},
     {"content": "Fix low priority dependency issues", "status": "pending", "activeForm": "Fixing low deps"},
     {"content": "Verification audit", "status": "pending", "activeForm": "Verifying updates"},
     {"content": "Complete Beads wisp", "status": "pending", "activeForm": "Completing wisp"}
   ]
   ```

---

## Phase 2: Detection

**Invoke dependency-auditor** via Task tool:

```
subagent_type: "dependency-auditor"
description: "Audit all dependencies"
prompt: |
  Audit the entire codebase for dependency issues:
  - Security vulnerabilities (npm audit / pnpm audit)
  - Outdated packages (major/minor/patch)
  - Unused dependencies (via Knip)
  - Deprecated packages
  - License compliance issues
  - Categorize by priority (critical/high/medium/low)

  Generate: dependency-scan-report.md

  Return summary with issue counts per priority.
```

**After dependency-auditor returns**:
1. Read `dependency-scan-report.md`
2. Parse issue counts by priority
3. If zero issues → skip to Final Summary
4. Update TodoWrite: mark audit complete

---

## Phase 3: Quality Gate (Detection)

Run inline validation:

```bash
pnpm type-check
pnpm build
```

- If both pass → proceed to updates
- If fail → report to TodoWrite and halt the process.
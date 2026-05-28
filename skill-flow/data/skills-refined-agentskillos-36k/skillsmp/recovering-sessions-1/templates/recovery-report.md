# Session Recovery Report

**Generated**: {{TIMESTAMP}}
**Project**: {{PROJECT_PATH}}
**Log Directory**: {{LOG_DIR}}
**Time Window**: Last {{MINUTES}} minutes

---

## Quick Summary

| Status | Count |
|--------|-------|
| COMPLETE | {{COMPLETE_COUNT}} |
| IN_PROGRESS | {{IN_PROGRESS_COUNT}} |
| FAILED | {{FAILED_COUNT}} |
| NOT_STARTED | {{NOT_STARTED_COUNT}} |
| UNKNOWN | {{UNKNOWN_COUNT}} |

---

## Agent Status Summary

| Agent ID | Task | Status | Files Created | Files Modified | Tests | Notes |
|----------|------|--------|---------------|----------------|-------|-------|
| {{AGENT_ID}} | {{TASK_ID}} | {{STATUS}} | {{FILES_CREATED}} | {{FILES_MODIFIED}} | {{TEST_RESULTS}} | {{NOTES}} |

---

## Completed Work

### Successfully Verified Deliverables

<!-- Repeat for each COMPLETE agent -->

#### {{TASK_ID}}: {{TASK_NAME}}

**Agent**: {{AGENT_ID}}
**Status**: COMPLETE

**Files Created:**
- `{{FILE_PATH}}` ({{FILE_SIZE}})

**Files Modified:**
- `{{FILE_PATH}}`

**Test Results:**
{{TEST_RESULTS}}

**Coverage:**
{{COVERAGE}}

---

## Interrupted Tasks

<!-- Repeat for each IN_PROGRESS agent -->

### {{TASK_ID}}: {{TASK_NAME}}

**Agent**: {{AGENT_ID}}
**Status**: IN_PROGRESS (crashed mid-execution)

**Last Known State:**
- Work was in progress when session terminated
- Partial implementation may exist

**Files Created (need verification):**
- `{{FILE_PATH}}` (exists: {{EXISTS}}, size: {{SIZE}})

**Files Modified:**
- `{{FILE_PATH}}`

**What's Missing:**
- [ ] Complete implementation
- [ ] Full test coverage
- [ ] Accessibility attributes
- [ ] Documentation

**Resumption Command:**
```
Task("{{AGENT_TYPE}}", "Complete {{TASK_ID}}: {{TASK_NAME}}

Last state: Work in progress (crashed mid-execution)

Files to complete:
{{FILE_LIST}}

Missing:
- Complete implementation
- Full test coverage
- Documentation

Follow project patterns from existing components.")
```

---

## Failed Tasks

<!-- Repeat for each FAILED agent -->

### {{TASK_ID}}: {{TASK_NAME}}

**Agent**: {{AGENT_ID}}
**Status**: FAILED

**Error Encountered:**
```
{{ERROR_MESSAGE}}
```

**Possible Root Cause:**
{{ROOT_CAUSE_ANALYSIS}}

**Files Affected:**
- `{{FILE_PATH}}`

**Remediation Command:**
```
Task("{{AGENT_TYPE}}", "Fix {{TASK_ID}}: {{TASK_NAME}}

Error: {{ERROR_SUMMARY}}
Location: {{ERROR_LOCATION}}

Fix: {{FIX_SUGGESTION}}
Test: Ensure tests cover the error case")
```

---

## Unknown Status Tasks

<!-- Repeat for each UNKNOWN agent -->

### {{TASK_ID}}: {{TASK_NAME}}

**Agent**: {{AGENT_ID}}
**Status**: UNKNOWN (requires manual review)

**Reason**: Unable to determine completion status from log

**Log Stats:**
- Messages: {{MESSAGE_COUNT}}
- Size: {{LOG_SIZE}}
- Modified: {{MODIFIED_TIME}}

**Recommendation:**
Review the agent log manually:
```bash
less {{LOG_PATH}}
```

Or analyze with script:
```bash
node analyze-agent-log.js {{LOG_PATH}} --verbose
```

---

## File Verification Summary

### Verified Files ({{VERIFIED_COUNT}})

| File | Size | Modified |
|------|------|----------|
| `{{FILE_PATH}}` | {{SIZE}} | {{MODIFIED}} |

### Missing Files ({{MISSING_COUNT}})

| Expected File | Reason |
|---------------|--------|
| `{{FILE_PATH}}` | {{REASON}} |

### Issues Found ({{ISSUES_COUNT}})

| File | Issue |
|------|-------|
| `{{FILE_PATH}}` | {{ISSUE}} |

---

## Git Status

**Branch**: {{BRANCH}}
**Uncommitted Changes**: {{UNCOMMITTED_COUNT}}

### Untracked Files
```
{{UNTRACKED_FILES}}
```

### Modified Files
```
{{MODIFIED_FILES}}
```

### Staged Files
```
{{STAGED_FILES}}
```

---

## Recommended Actions

### Immediate Actions

1. **Commit completed work**
   ```bash
   git add {{VERIFIED_FILE_LIST}}
   git commit -m "$(cat <<'EOF'
   feat: recover work from interrupted session

   Completed:
   {{COMPLETED_TASK_LIST}}

   Interrupted (to resume):
   {{INTERRUPTED_TASK_LIST}}

   {{#if FAILED_TASKS}}
   Failed (needs fix):
   {{FAILED_TASK_LIST}}
   {{/if}}

   Recovered via session-recovery skill
   EOF
   )"
   ```

2. **Update progress tracking**
   ```
   Task("artifact-tracker", "Update {{PRD}} phase {{PHASE}}:
   {{#each COMPLETED}}
   - {{TASK_ID}}: complete (recovered)
   {{/each}}
   {{#each INTERRUPTED}}
   - {{TASK_ID}}: in_progress (interrupted)
   {{/each}}
   {{#each FAILED}}
   - {{TASK_ID}}: blocked (error)
   {{/each}}
   - Add note: Recovered from session crash at {{TIMESTAMP}}")
   ```

### Resume/Fix Tasks (Priority Order)

{{#each PRIORITY_ACTIONS}}
#### Priority {{PRIORITY}}: {{TASK_ID}}

**Status**: {{STATUS}}
**Reason**: {{PRIORITY_REASON}}

```
{{RESUMPTION_COMMAND}}
```

{{/each}}

---

## Prevention Recommendations

Based on this crash, consider:

{{#if LARGE_BATCH}}
1. **Reduce parallel agent count**
   - This session had {{AGENT_COUNT}} parallel agents
   - Recommend: Max 3-4 agents per batch
{{/if}}

{{#if NO_CHECKPOINTING}}
2. **Add checkpointing**
   - Progress was not updated during execution
   - Recommend: Update progress after each task completion
{{/if}}

{{#if LONG_RUNNING}}
3. **Use background execution with timeouts**
   - Some agents ran for extended periods
   - Recommend: Use `run_in_background: true` with status checks
{{/if}}

See `.claude/skills/recovering-sessions/references/prevention-patterns.md` for complete guidance.

---

## Session Metadata

- **Session Start**: {{SESSION_START}}
- **Session End**: {{SESSION_END}} (estimated)
- **Duration**: {{DURATION}}
- **Log Directory**: {{LOG_DIR}}
- **Agents Analyzed**: {{AGENT_COUNT}}
- **Files Discovered**: {{FILE_COUNT}}
- **Recovery Script Version**: 1.0.0

---

*Generated by session-recovery skill*

# Verification Flow

This document is the single source of truth for verification-related protocols in Unit Work, including which subagents to use, confidence calculation, and self-correcting review.

## Which Verification Subagent to Use

```
Code changes to verify:
                    |
+-----------------------------------------------+
| Changed test files?                            |
|   YES -> Test Runner (run the changed tests)   |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Changed API endpoints?                         |
|   YES -> Test Runner + API Prober              |
|         + Browser Automation (for e2e via UI)  |
|         (API Prober: read-only without         |
|          permission, mutating requires         |
|          user confirmation)                    |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Changed UI components?                         |
|   YES -> Test Runner + Browser Automation      |
|         (Browser: screenshots + element        |
|          verification, flag layout for         |
|          human review)                         |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Changed database schema/migrations?            |
|   YES -> Test Runner only                      |
|         (NEVER run migrations automatically)   |
|         (Flag for human verification)          |
+-----------------------------------------------+
                    |
+-----------------------------------------------+
| Changed configuration/environment?             |
|   YES -> No automated verification             |
|         (Document changes, flag for human)     |
+-----------------------------------------------+
```

## Browser-Automation for All Change Types

Browser-automation is NOT limited to UI changes. Use it when:
- Verifying API endpoints through the app UI
- Testing end-to-end flows that involve backend changes
- Validating that frontend correctly displays data from backend
- Any change that affects user-visible behavior

**Setup for backend testing:**
1. Determine app URL based on repository (see table below)
2. Determine backend port (agent's server, user-specified, or default 8000)
3. Ensure local backend is running
4. Agent sets `localStorage.setItem('api-url', 'http://localhost:{PORT}')`
5. Browser uses local backend for all API calls

**Repository to URL mapping:**
| Repository | App URL |
|------------|---------|
| `relevance-app` | `https://app-development.relevanceai.com` |
| `relevance-chat-app` | `https://chat-development.relevanceai.com` |
| Other | Ask user |

**Note:** Both apps use the same localStorage key (`api-url`).

## Confidence Calculation

Start at 100%, subtract for uncertainties:
- -5% for each untested edge case
- -20% if UI layout changes
- -10% if complex state management
- -15% if external API integration

### Confidence Thresholds

**Confidence >= 95%:** Continue automatically to next unit.

**Confidence < 95%:** Pause for human review. Present:
- What was verified
- What needs human judgment
- Specific items to check

## Self-Correcting Review (Fix Checkpoints Only)

**This section ONLY applies to fix checkpoints** (e.g., `checkpoint(2.1)`, `checkpoint(3.2)`, `checkpoint(pr-123-1)`). Skip this for regular unit checkpoints.

When you create a fix checkpoint, the fix itself may introduce new issues. Before continuing, assess whether the fix needs re-review.

### Risk Assessment (Fast - No Agent Spawning)

Analyze the fix diff to determine review intensity:

**No Review Needed** - ALL conditions must be true:
- <=3 lines changed
- File matches low-risk patterns: `*.test.*, *.spec.*, *.md, *.json, *.yaml, *.yml, *.config.*`
- Pure additions (no deletions)

**Light Review** - ANY condition true:
- 4-30 lines changed
- Single file in `src/` or main code directory
- Changes with <5 deletions

**Full Review** - ANY condition true:
- >30 lines changed
- >3 files modified
- >10 lines deleted
- Security-related file patterns (auth, crypto, permissions)

### Selective Agent Invocation

Based on the type of issue being fixed, spawn only the relevant review agent(s):

| Original Issue Type | Re-Review Agent |
|---------------------|-----------------|
| Type safety issue | `type-safety` |
| Pattern/utility issue | `patterns-utilities` |
| Performance issue | `performance-database` |
| Architecture issue | `architecture` |
| Security issue | `security` |
| Simplicity issue | `simplicity` |

**For mixed fix types** (fix addresses multiple categories): Spawn ALL relevant agents.

**Scope-guard for review agents:** When spawning agents to review a fix, include this context:

> "You are reviewing a FIX to a specific issue. DO NOT suggest additional refactoring beyond the fix. DO NOT expand scope. Only verify the fix addresses the original issue without introducing new problems."

### Cycle Handling

**If re-review finds no new issues:** Continue to next unit/step.

**If re-review finds new issues:** Present to user via AskUserQuestion:
- **Fix the new issue** - Implement fix and create another fix checkpoint (triggers another cycle)
- **Accept and continue** - Break cycle, proceed with current state
- **Revert fix** - Execute `git reset --soft HEAD~1` to unstage, let user review

**Hard limit: 3 cycles maximum.** After 3 fix-review cycles on the same original issue:

```
Fix-review cycle limit reached (3 iterations).

**Attempts made:**
1. {first fix attempt and result}
2. {second fix attempt and result}
3. {third fix attempt and result}

**Recommendation:** {continue manually | accept current state | revert to pre-fix}

What would you like to do?
```

Use AskUserQuestion with options:
- **Continue manually** - User takes over fixing
- **Accept current state** - Proceed with existing fixes
- **Revert all fixes** - Execute `git reset --soft HEAD~{n}` to revert fix attempts

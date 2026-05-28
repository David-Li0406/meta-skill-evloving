---
name: submit-pr
description: |
  Complete PR submission pipeline with local sub-agent review before pushing, CI verification, and automated review integration. Always dispatches code-reviewer and code-simplifier for code changes, plus conditional reviewers (security, performance, dependency, accessibility, i18n, type-design, etc.) based on change type. Waits for CI with `gh pr checks --watch`. Integrates CodeRabbit and Greptile feedback.
---

# Submit PR

## CRITICAL: Complete ALL 8 Phases

> **This skill has 8 phases. PR creation (Phase 5) is NOT the end.**
>
> **You MUST execute ALL phases. Do NOT stop after creating the PR.**

```
Phase 0: Update Plan    → Document what's being submitted
Phase 1: Pre-Submit     → Local verification
Phase 2: Sub-Agents     → Dispatch reviewers
Phase 3: Fix Findings   → Address issues
Phase 4: Push & PR      → Create PR ← THIS IS NOT THE END
Phase 5: CI Wait        → Wait for CI  ← MUST DO
Phase 6: Review Feed    → Read feedback ← MUST DO
Phase 7: Human Review   → Request review ← MUST DO
```

**Completion = Phase 7 done. Not before.**

---

## Mandatory: Track All Phases with TodoWrite

**BEFORE starting Phase 0**, create todos for ALL 8 phases:

```
TodoWrite([
  { content: "Phase 0: Update plan with PR summary", status: "pending" },
  { content: "Phase 1: Pre-submit checks", status: "pending" },
  { content: "Phase 2: Dispatch sub-agent reviewers", status: "pending" },
  { content: "Phase 3: Address sub-agent findings", status: "pending" },
  { content: "Phase 4: Push branch and create PR", status: "pending" },
  { content: "Phase 5: Wait for CI verification", status: "pending" },
  { content: "Phase 6: Read automated review feedback", status: "pending" },
  { content: "Phase 7: Request human review", status: "pending" }
])
```

**Mark each phase `in_progress` before starting, `completed` after finishing.**

This ensures phases 5-7 remain visible and tracked.

---

## Decision Tree (Reference)

```
Phase 0: Update Plan
         ↓
Phase 1: Pre-Submit Checks Pass?
├── NO → Fix issues, re-run checks
└── YES → Phase 2: Dispatch Sub-Agents
           ↓
      Phase 2: Sub-Agent Review Complete?
      ├── Any FAIL? → Phase 3: Fix issues, re-dispatch
      └── All PASS? → Phase 4: Push & Create PR
                      ↓
                 Phase 5: CI Passes? ← YOU ARE NOT DONE YET
                 ├── NO → Fix, push, re-watch
                 └── YES → Phase 6: Read Automated Feedback
                           ↓
                      Issues Found?
                      ├── YES → Fix, push, verify
                      └── NO → Phase 7: Request Human Review
                               ↓
                          ✅ SKILL COMPLETE
```

---

## Overview

Orchestrates the full PR lifecycle: pre-submit verification → local sub-agent review → push → CI verification → automated review feedback → human review request. Catches issues at the earliest possible stage.

## When to Use

**Invoke this skill when:**
- Feature implementation is complete and ready for review
- Bug fix is tested and ready to merge
- Creating your first PR in a new repository
- Unsure about PR description format or best practices
- Need comprehensive pre-push quality checks

**Do NOT use when:**
- Work is still in progress (use draft PR instead)
- Tests are failing (fix tests first)
- You haven't rebased on main recently
- Changes include sensitive data or secrets

---

## Phase 0: Update Plan

**Mark todo: Phase 0 → in_progress**

Document what's being submitted before starting verification. This creates a clear record of intent.

### Update Session/Plan File

If a session or plan file exists, update it with PR summary:

```markdown
## PR Summary

**Branch:** feature/my-feature
**Target:** main
**Type:** feat | fix | refactor | docs | chore

### Changes
- [What changed and why]
- [Key files modified]

### Reviewers to Dispatch
- [ ] code-reviewer (always)
- [ ] code-simplifier (always)
- [ ] security-reviewer (if applicable)
- [ ] [others based on change type]

### Risk Assessment
- **Breaking changes:** Yes/No
- **Database migrations:** Yes/No
- **Config changes:** Yes/No
```

### If No Session File

Create a brief summary in your response:

```
PR Summary:
- Branch: feature/my-feature → main
- Changes: [1-2 sentence summary]
- Key files: [list]
- Reviewers needed: [list based on change type]
```

**Mark todo: Phase 0 → completed**

**→ IMMEDIATELY proceed to Phase 1**

---

## Phase 1: Pre-Submit Checklist

**Mark todo: Phase 1 → in_progress**

**MANDATORY before proceeding:**

```bash
# 1. Verify all tests pass
npm test

# 2. Run linter
npm run lint

# 3. Type check
npm run typecheck

# 4. Review your changes
git diff main...HEAD --stat

# 5. Check for secrets/sensitive data
git diff main...HEAD | grep -E "(password|secret|api_key|token)" || echo "Clean"

# 6. Verify branch is up to date
git fetch origin main
git rebase origin/main
```

**Do NOT proceed if any check fails.**

**Mark todo: Phase 1 → completed**

**→ IMMEDIATELY proceed to Phase 2**

---

## Phase 2: Local Sub-Agent Review

**Mark todo: Phase 2 → in_progress**

**BEFORE pushing**, dispatch specialized review agents to catch issues early.

### Determine Which Agents to Dispatch

Analyze changes to select appropriate reviewers:

```bash
# Get changed files for analysis
git diff main...HEAD --stat
git diff main...HEAD --name-only
```

### Core Reviewers (Always Dispatch for Code Changes)

| Agent | Purpose |
|-------|---------|
| `code-reviewer` | Comprehensive multi-file review, logic correctness |
| `code-simplifier` | Clarity, consistency, maintainability |

### Conditional Reviewers (Based on Change Type)

| Change Type | Dispatch Agent |
|-------------|----------------|
| Auth, secrets, user data, APIs | `security-reviewer` |
| Database queries, loops, rendering, large data | `performance-reviewer` |
| package.json, lock files, dependencies | `dependency-reviewer` |
| New files, folder changes, reorganization | `structure-reviewer` |
| Test additions or modifications | `test-coverage-analyzer` |
| UI components, frontend changes | `accessibility-auditor` |
| User-facing strings, locale files | `i18n-validator` |
| New types, interfaces, generics | `type-design-analyzer` |
| Error handling, try/catch, promises | `silent-failure-hunter` |
| Meta tags, SEO content, schema markup | `seo-specialist` |

### Dispatch Review Agents in Parallel

Use the Task tool to run specialized reviewers simultaneously.

**Core reviewers (ALWAYS dispatch for code changes):**

```markdown
Task: @code-reviewer (ALWAYS dispatch for code changes)
Comprehensive review of all changed files.
Focus: logic correctness, edge cases, error handling, code quality.

---

Task: @code-simplifier (ALWAYS dispatch for code changes)
Simplify and refine recently modified code.
Focus: clarity, consistency, maintainability while preserving functionality.
```

**Conditional reviewers (dispatch based on change type):**

```markdown
Task: @security-reviewer (if auth, secrets, user data, APIs)
Review changes for security vulnerabilities.
Focus: authentication, authorization, input validation, data exposure, XSS, injection.

---

Task: @performance-reviewer (if queries, loops, rendering, large data)
Analyze performance implications of changes.
Focus: query efficiency, N+1 problems, rendering, bundle size, memory leaks.

---

Task: @dependency-reviewer (if package.json or lock files)
Review dependency changes.
Check: known vulnerabilities, license compatibility, maintenance status.

---

Task: @structure-reviewer (if new files or reorganization)
Review file organization and project structure.
Focus: naming conventions, folder hierarchy, module boundaries.

---

Task: @test-coverage-analyzer (if test additions or modifications)
Analyze test adequacy and coverage gaps.
Focus: edge cases, error paths, integration points.

---

Task: @accessibility-auditor (if UI components or frontend)
WCAG 2.1 AA compliance review.
Focus: keyboard navigation, screen reader, color contrast, ARIA.

---

Task: @i18n-validator (if user-facing strings or locale files)
Internationalization coverage review.
Focus: hardcoded strings, locale support, RTL compatibility.

---

Task: @type-design-analyzer (if new types, interfaces, generics)
Type design quality review.
Focus: encapsulation, invariants, type safety, usefulness.

---

Task: @silent-failure-hunter (if error handling, try/catch, promises)
Find unhandled errors and silent failures.
Focus: missing catch blocks, swallowed errors, promise rejection handling.

---

Task: @seo-specialist (if meta tags, SEO content, schema markup)
SEO review for web content.
Focus: meta tags, structured data, content optimization.
```

### Aggregate Sub-Agent Results

Collect and assess findings:

```markdown
## Local Review Summary

### Core Reviews (Always Run)
| Agent | Status | Findings |
|-------|--------|----------|
| Code Review | [PASS/WARN/FAIL] | [summary] |
| Code Simplification | [DONE/SKIPPED] | [files refined] |

### Conditional Reviews (Based on Changes)
| Agent | Status | Findings |
|-------|--------|----------|
| Security | [PASS/WARN/FAIL/N/A] | [summary] |
| Performance | [PASS/WARN/FAIL/N/A] | [summary] |
| Dependencies | [PASS/WARN/FAIL/N/A] | [summary] |
| Structure | [PASS/WARN/FAIL/N/A] | [summary] |
| Test Coverage | [PASS/WARN/FAIL/N/A] | [summary] |
| Accessibility | [PASS/WARN/FAIL/N/A] | [summary] |
| i18n | [PASS/WARN/FAIL/N/A] | [summary] |
| Type Design | [PASS/WARN/FAIL/N/A] | [summary] |
| Silent Failures | [PASS/WARN/FAIL/N/A] | [summary] |
| SEO | [PASS/WARN/FAIL/N/A] | [summary] |

### Critical Issues: [count]
### Warnings: [count]
### Overall: [READY TO PUSH / NEEDS FIXES]
```

**Mark todo: Phase 2 → completed**

**→ IMMEDIATELY proceed to Phase 3**

---

## Phase 3: Address Sub-Agent Findings

**Mark todo: Phase 3 → in_progress**

**If any sub-agent reports FAIL or critical issues:**

1. Fix the identified issues
2. Re-run affected tests
3. Re-dispatch the sub-agent that found issues
4. Verify PASS before proceeding

**Do NOT push with unresolved critical findings.**

**If all sub-agents report PASS:** Mark complete and proceed.

**Mark todo: Phase 3 → completed**

**→ IMMEDIATELY proceed to Phase 4**

---

## Phase 4: Push & Create PR

**Mark todo: Phase 4 → in_progress**

Only after local sub-agent review passes:

### Push Branch

For pushes with pre-push hooks, use background execution with TaskOutput:

```typescript
// Start push in background (hooks may run tests)
Bash("CLAUDE_SUBMIT_PR_SKILL=1 git push -u origin feature/my-feature", run_in_background: true)
// → task_id: "push_123"

// Wait for push + hooks to complete (up to 3 min)
TaskOutput(task_id: "push_123", block: true, timeout: 180000)
// → Returns push result
```

**See `background-tasks` skill for efficient waiting patterns.**

For quick pushes without hooks:
```bash
# Direct push (no pre-push hooks)
CLAUDE_SUBMIT_PR_SKILL=1 git push -u origin feature/my-feature
```

### Create PR

```bash
CLAUDE_SUBMIT_PR_SKILL=1 gh pr create --title "feat: add feature" --body "$(cat <<'EOF'
## Summary
- [What changed and why]

## Test Plan
- [ ] Unit tests added/updated
- [ ] Integration tests pass

## Local Review
- [x] Security review passed
- [x] Performance review passed
- [x] Tests pass locally

Closes #[issue]
EOF
)"

# Capture PR number for subsequent phases
PR_NUMBER=$(gh pr view --json number -q '.number')
echo "Created PR #$PR_NUMBER"
```

**Mark todo: Phase 4 → completed**

> **IMPORTANT: Creating the PR is NOT the end. You MUST continue.**

**→ IMMEDIATELY proceed to Phase 5**

---

## Phase 5: CI Verification

**Mark todo: Phase 5 → in_progress**

**Wait for CI checks to complete using background execution:**

```typescript
// Start CI watch in background (can take several minutes)
Bash("gh pr checks $PR_NUMBER --watch", run_in_background: true)
// → task_id: "ci_watch_123"

// Wait for CI to complete (up to 10 min)
TaskOutput(task_id: "ci_watch_123", block: true, timeout: 600000)
// → Returns CI results when all checks complete
```

**Do NOT poll repeatedly. Use TaskOutput with block: true.**

| CI Status | Action |
|-----------|--------|
| All pass | Proceed to Phase 6 |
| Tests fail | Fix, push, re-watch |
| Lint/Type errors | Fix, push, re-watch |

**Mark todo: Phase 5 → completed**

**→ IMMEDIATELY proceed to Phase 6**

---

## Phase 6: Automated Review Feedback

**Mark todo: Phase 6 → in_progress**

> **IRON LAW: Every conversation MUST be resolved. No exceptions.**

### The Rule

```
┌─────────────────────────────────────────────────────────────┐
│  EVERY comment → Reply → Click "Resolve conversation"       │
│                                                             │
│  No comment should EVER be left unresolved.                 │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: Fetch All Comments and Discussions

```bash
# Get all review threads
gh pr view $PR_NUMBER --comments

# Check for unresolved conversations
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 1) {
            nodes { body }
          }
        }
      }
    }
  }
}' -f owner="OWNER" -f repo="REPO" -F pr="$PR_NUMBER"
```

### Step 2: Process EACH Comment

**For EVERY comment, follow this flow:**

```
Comment received
    ↓
Categorize:
├── FIX → Make change → Reply "Fixed in [commit]" → RESOLVE
├── DEFER → Create tracking issue → Reply "Tracked in #X" → RESOLVE
├── OUT OF SCOPE → Reply "Out of scope: [reason]" → RESOLVE
└── DISMISS → Reply "Intentional: [reason]" → RESOLVE
                                                    ↑
                                        ALL paths end here
```

### Categories and Actions

| Category | When to Use | Reply Template | Creates Issue? |
|----------|-------------|----------------|----------------|
| **Fixed** | You made the code change | "Fixed in abc123" | No |
| **Deferred** | Valid feedback, but not this PR | "Valid point. Tracked in #X for follow-up" | **Yes** |
| **Out of Scope** | Trivial nitpick or unrelated | "Out of scope for this PR" | No |
| **Dismissed** | You disagree with the feedback | "Intentional: [explanation]" | No |

### Step 3: Create Tracking Issues for Deferred Items

Use `pr-feedback-tracker` or manually create:

```bash
# Collect all deferred items into one tracking issue
gh issue create \
  --title "Follow-up: Deferred items from PR #$PR_NUMBER" \
  --body "## Deferred Items
- [ ] Item 1 description
- [ ] Item 2 description

Context: PR #$PR_NUMBER" \
  --label "tech-debt"
```

### Step 4: Resolve ALL Threads

```bash
# Resolve a thread via GraphQL
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}' -f threadId="THREAD_ID"
```

### Step 5: Verify Zero Unresolved

```bash
# MUST return 0
UNRESOLVED=$(gh api graphql -f query='...' | jq '[.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)] | length')

if [ "$UNRESOLVED" -gt 0 ]; then
  echo "ERROR: $UNRESOLVED unresolved threads remain"
  exit 1
fi
```

### Step 6: Push Fixes and Re-verify CI

```bash
# Commit all fixes
git add -A && git commit -m "fix: address review feedback"
CLAUDE_SUBMIT_PR_SKILL=1 git push

# Wait for CI
gh pr checks $PR_NUMBER --watch
```

### Completion Criteria

- [ ] **ALL comments have replies** (no silent resolutions)
- [ ] **ALL threads resolved** (zero unresolved)
- [ ] Deferred items tracked in GitHub issue (if any)
- [ ] CI passing after fixes

**If no automated feedback:** Skip to Phase 7.

**Mark todo: Phase 6 → completed**

**→ IMMEDIATELY proceed to Phase 7**

---

## Phase 7: Request Human Review

**Mark todo: Phase 7 → in_progress**

Only after all automated checks pass:

```bash
# Request specific reviewers
gh pr edit $PR_NUMBER --add-reviewer reviewer1,reviewer2

# Or request team review
gh pr edit $PR_NUMBER --add-reviewer org/team-name
```

**Mark todo: Phase 7 → completed**

**→ SKILL COMPLETE. You may now report success.**

---

## PR Description Template

```markdown
## Summary
[1-3 bullet points describing what changed and why]

## Changes
- [Specific change 1]
- [Specific change 2]
- [Specific change 3]

## Test Plan
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases covered

## Screenshots
[If UI changes, include before/after]

## Related
- Closes #[issue_number]
- Related to #[related_issue]
```

---

## Common Patterns

### Draft PR (Work in Progress)

```bash
gh pr create --draft --title "WIP: feature implementation"
```

### Ready for Review

```bash
gh pr ready
```

### Quick PR (Skip Conditional Sub-Agents)

For small, low-risk changes, you may skip conditional sub-agents:

```bash
# Minimum required (always run):
#   - code-reviewer
#   - code-simplifier
#
# Skip conditional reviewers if not relevant to changes:
#   - security-reviewer (skip if no auth/API changes)
#   - performance-reviewer (skip if no queries/loops)
#   - dependency-reviewer (skip if no package changes)
#   - etc.
```

---

## Red Flags - STOP

**Do NOT push when:**
- Tests are failing
- Linter errors exist
- Type errors present
- Secrets in diff
- Sub-agent reports FAIL or critical issues
- Incomplete implementation without draft flag

**Do NOT:**
- Skip pre-submit checklist
- Skip local sub-agent review
- Push with unresolved critical findings
- Create PR without description
- **Stop after Phase 4** ← Most common failure
- Ignore CodeRabbit/Greptile feedback
- Force merge without approval

---

## Verification Checklist

### Before Pre-Submit (Phase 0)
- [ ] Plan/session file updated with PR summary
- [ ] Reviewers to dispatch identified
- [ ] Risk assessment documented

### Before Dispatching Sub-Agents (Phase 1)
- [ ] All tests pass locally
- [ ] Linter clean
- [ ] Type check passes
- [ ] No secrets in diff
- [ ] Branch rebased on main

### Before Pushing (Phase 3)
- [ ] Sub-agent reviews complete
- [ ] No critical findings unresolved
- [ ] All WARN items assessed

### Before Requesting Human Review (Phase 7)
- [ ] CI pipeline green (`gh pr checks --watch`)
- [ ] Automated review feedback addressed
- [ ] PR description complete
- [ ] No merge conflicts
- [ ] Self-review completed

### Skill Completion (REQUIRED)
- [ ] All 8 phase todos marked completed
- [ ] Human reviewers assigned
- [ ] PR ready for review

---

## Integration

**Parent skill:** git-expert
**Related skills:** coderabbit, tdd, verification, dispatching-parallel-agents, background-tasks, **pr-feedback-tracker**

**Phase 6 skill:**
- `pr-feedback-tracker` - Categorizes feedback, creates tracking issues for deferred items

**Core sub-agents (always run for code changes):**
- `code-reviewer` - Comprehensive multi-file review, logic correctness
- `code-simplifier` - Clarity, consistency, maintainability

**Conditional sub-agents (based on change type):**
- `security-reviewer` - XSS, injection, auth vulnerabilities
- `performance-reviewer` - Queries, rendering, bundle size
- `dependency-reviewer` - Vulnerabilities, licenses, maintenance
- `structure-reviewer` - File organization, patterns
- `test-coverage-analyzer` - Test adequacy and gaps
- `accessibility-auditor` - WCAG compliance for UI
- `i18n-validator` - Internationalization coverage
- `type-design-analyzer` - Type design quality
- `silent-failure-hunter` - Unhandled errors
- `seo-specialist` - SEO for web content

**Architecture note:** Uses supervisor pattern. Sub-agents provide context isolation - each reviewer operates in a clean context focused on its domain. Results aggregate without any single context bearing the full burden.

---

## Metadata

**Version:** 3.5.0
**Last Updated:** 2026-01-15

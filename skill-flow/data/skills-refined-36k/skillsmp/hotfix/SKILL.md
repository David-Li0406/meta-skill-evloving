---
name: hotfix
description: Fix bugs or modify existing features with deep exploration
model: opus
argument-hint: <issue description>
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: |
            if [[ -d "backend" ]]; then
              cd backend && go build ./... 2>&1 | head -10 || true
            fi
          once: true
---

Follow CLAUDE.md rules for Clean Architecture.

## Ultra Think Strategy

Ultra think before each phase transition:
- After clarification: ensure you fully understand the issue
- After exploration results: reflect on completeness before analyzing
- Before implementation: consider edge cases, patterns to follow, potential issues
- After validation: ensure the fix addresses root cause, not symptoms

---

## 1. PARSE ISSUE

From: `$ARGUMENTS`

Extract:
- **Feature area**: Which part of the app?
- **Bug type**: Logic error, UI, data, performance, error handling?
- **Layers**: Backend / Frontend / Both / Database?
- **Database env**: Detect from description (prod/dev) - default to DEV

---

## 2. CLARIFY ISSUE

Use AskUserQuestion to clarify before exploration:

### Bug context (if not specified)
- Can you reproduce the bug? Steps to reproduce?
- What is the expected vs actual behavior?
- When did it start happening? (recent deploy, config change?)
- Are there error logs or screenshots available?

### Impact & Priority (if not specified)
- Is this blocking production?
- Who/what is affected?
- Is there a temporary workaround in place?

### Scope (if not specified)
- Should we fix root cause or apply quick workaround first?
- Are there related issues to address at the same time?
- Environment affected: dev, staging, prod?

Do not proceed until the issue is fully understood.

---

## 3. EXPLORE (PARALLEL)

Launch agents based on issue scope (single message, parallel execution):

| Need | Agent | Prompt |
|------|-------|--------|
| Backend | explore-codebase | "Find all [feature] related code in backend/" |
| Frontend | explore-codebase | "Find all [feature] related code in frontend/src/" |
| Database | explore-db | "[env] - Find [feature] tables, schema, RLS" |
| Library | explore-docs | "[library] [error/feature] documentation" |

---

## 3.5 POST-EXPLORATION CHECK

After agents return, verify:
1. Information complete? If not -> launch additional agents
2. For fixes adding validation: Do I know ALL places where similar patterns exist?

---

## 4. ANALYZE

Produce analysis:

```markdown
## Bug Analysis

### Current Behavior
[What the code currently does]

### Expected Behavior
[What it should do]

### Root Cause
[Why the bug happens - with file:line references]

### Files Affected
- `path/to/file.go:123` - [how it's affected]
```

---

## 5. SHOW FIX PLAN (MANDATORY CHECKPOINT)

Create and display the complete fix strategy, then **STOP**. Do NOT proceed without user validation.

```markdown
## Fix Strategy

### Root Cause Summary
[One sentence]

### Changes Required

**Backend:**
- `path/to/file.go:XX` - [specific change]

**Frontend:**
- `path/to/file.tsx:XX` - [specific change]

### Patterns to Follow
[From exploration - exact code snippets]

### Risks & Mitigations
- [Risk]: [Mitigation]
```

---

## 6. VALIDATE (BLOCKING)

**MANDATORY**: You MUST wait for user approval before ANY implementation.

Ask with AskUserQuestion: "Validate this fix approach?"
- "Apply fix"
- "Investigate more"
- "Modify approach"

**DO NOT proceed to implementation without explicit user selection.**

---

## 7. IMPLEMENT

**ONLY after user selects "Apply fix"**, implement:
1. Backend changes first
2. Frontend changes second

**Rules:**
- Stay in scope - change only what's needed
- Fix root cause, not symptoms
- Add defensive checks where appropriate

For significant UI: `Skill(skill="frontend-design:frontend-design")`

---

## 8. VERIFY

```bash
cd backend && go build ./... && go vet ./...
cd frontend && npm run build
```

Database verification: `mcp__supabase-dev__get_advisors` or `mcp__supabase-prod__get_advisors`

---

## 9. SUMMARY

```markdown
## Fix Complete

### Issue
[Original issue]

### Root Cause
[What was wrong]

### Changes Made
- `path/to/file.go` - [change]

### Testing Recommendation
- [How to verify]
```

---

## Rules

- **CLARIFY FIRST** - fully understand the issue before exploring
- **EXPLORE SECOND** - never assume, always investigate
- **ROOT CAUSE** - fix the cause, not the symptom
- **VALIDATE IS BLOCKING** - NEVER implement without explicit user approval on the fix plan
- **STAY IN SCOPE** - change only what's needed

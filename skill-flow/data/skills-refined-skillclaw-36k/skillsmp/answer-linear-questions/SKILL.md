---
name: answer-linear-questions
description: "Answer Linear issues tagged with \"question\". Explores codebase and produces decisions - never code changes or PRs. Triggers - answer questions, linear questions, question triage."
---

# Answer Linear Questions

**Iron Law:** Questions produce DECISIONS, not CODE. No GitHub PRs, no implementation.

## Overview

This skill handles Linear issues tagged with "question". It reviews pending questions and produces decisions that guide future work.

```
Question → Analysis → Codebase Exploration → Informed Decision → Action Item
                              ↓                      ↓
                   Explore agent / Search    Never: Code changes, PRs
```

## Valid Outcomes

| Outcome | When to Use | Linear Action |
|---------|-------------|---------------|
| **Create Issue** | Question reveals work needed | Create new issue with details |
| **Create Spec** | Question needs discovery/requirements | `/create-linear-spec` |
| **Add to Project** | Work belongs in existing project | Add issue to project |
| **Update Existing** | Answer affects existing issue | Comment or update issue |
| **Close as Resolved** | Question answered, no work needed | Comment answer, close issue |
| **Close as Won't Do** | Out of scope or declined | Comment reasoning, close issue |

## Invalid Outcomes

- Writing code
- Creating GitHub PRs
- Making implementation changes
- Modifying files in the codebase

---

## The Workflow

### Step 1: List Pending Questions

```typescript
mcp__linear-server__list_issues({
  label: "question",
  state: "started",  // Or "triage", "backlog" based on your workflow
  limit: 20
});
```

### Step 2: Select a Question

Present questions to user or work through them:

```markdown
## Pending Questions

| ID | Title | Created | Priority |
|----|-------|---------|----------|
| PEA-123 | How should we handle auth tokens? | 2 days ago | High |
| PEA-145 | What's the pagination limit? | 1 week ago | Medium |

Which question would you like to address?
```

### Step 3: Analyze the Question

Read the full issue:

```typescript
mcp__linear-server__get_issue({ id: "issue-uuid" });
```

Understand:
- What is being asked?
- What context is provided?
- Who is asking? (stakeholder, team member, external)
- What's the impact of the answer?

### Step 4: Explore Codebase (MANDATORY)

**Before making any decision, explore the codebase to provide informed context.**

Use the Explore agent or direct search to understand:

```typescript
// Dispatch Explore agent for comprehensive analysis
Task({
  subagent_type: "Explore",
  prompt: `
    Research context for Linear question: "[question title]"

    Question details: [paste question description]

    Find:
    1. Related code files and patterns
    2. Existing implementations that might answer this
    3. Dependencies or constraints relevant to the question
    4. Similar patterns already in the codebase
    5. Documentation or comments that provide context

    Return findings to inform the decision.
  `,
  description: "Explore codebase for question context"
});
```

Or use direct search for targeted queries:

```bash
# Find related files
Glob: "**/*[relevant-pattern]*"

# Search for related code
Grep: "pattern-from-question"

# Read specific files
Read: path/to/relevant/file.ts
```

**Present findings to user:**

```markdown
## Codebase Analysis

### Related Files Found
- `src/auth/tokens.ts` - Current token handling (lines 45-89)
- `src/middleware/auth.ts` - Auth middleware implementation
- `src/config/auth.config.ts` - Auth configuration

### Existing Patterns
- Currently using JWT with 24h expiry
- Token refresh implemented in `refreshToken()` at auth/tokens.ts:67

### Relevant Context
- No OAuth implementation exists
- Auth middleware supports multiple strategies (line 23)
- Config has placeholder for OAuth providers (commented out)

### Dependencies
- `jsonwebtoken` - Current JWT library
- `passport` - Auth framework (supports OAuth plugins)

### Key Findings
1. [Finding 1 with code reference]
2. [Finding 2 with code reference]
3. [Finding 3 with code reference]
```

### Step 4b: Research External Context (If Needed)

After codebase exploration, if more context needed:
- Check existing documentation
- Review related Linear issues
- Consult external resources (WebSearch for best practices)

### Step 5: Formulate Decision

The decision should be:
- **Clear** - Unambiguous answer or direction
- **Actionable** - What happens next is obvious
- **Documented** - Reasoning is captured

### Step 6: Execute Decision

Based on decision type:

#### Create New Issue
```typescript
mcp__linear-server__create_issue({
  title: "[Resulting work from question]",
  description: `## Context\nFrom question PEA-123: [original question]\n\n## Decision\n[What we decided]\n\n## Work Required\n[Scope of work]`,
  team: "Engineering",
  labels: ["from-question"]
});
```

#### Create Spec
```
Use /create-linear-spec skill to explore requirements
```

#### Add to Project
```typescript
mcp__linear-server__update_issue({
  id: "existing-issue-uuid",
  project: "relevant-project"
});
```

#### Close with Answer
```typescript
// Add comment with answer
mcp__linear-server__create_comment({
  issueId: "question-issue-uuid",
  body: "## Answer\n\n[Your answer here]\n\n## Reasoning\n[Why this is the answer]"
});

// Close the issue
mcp__linear-server__update_issue({
  id: "question-issue-uuid",
  state: "Done"  // Or "Canceled" if won't do
});
```

### Step 7: Confirm Resolution

```markdown
## Question Resolved

**Question:** PEA-123 - How should we handle auth tokens?
**Decision:** Create spec for token management strategy
**Action Taken:** Created project "Auth Token Strategy" via /create-linear-spec
**Original Issue:** Closed with comment linking to new project

Next question or done for now?
```

---

## Decision Framework

Use this framework to decide outcomes:

```
Is the answer known?
├── YES → Does it require work?
│         ├── YES → Is scope clear?
│         │         ├── YES → Create Issue
│         │         └── NO → Create Spec
│         └── NO → Close with Answer
└── NO → Need more info?
          ├── YES → Research, then return to top
          └── NO → Close as Won't Do (with reasoning)
```

---

## Example Session

**User says:** `/answer-linear-questions`

**Step 1 - List:**
```
Found 3 questions:

1. PEA-201: Should we support OAuth2? (High priority, 3 days old)
2. PEA-215: What's the rate limit for API? (Medium, 1 week old)
3. PEA-220: Can we use Redis for caching? (Low, 2 weeks old)

Which question would you like to address?
```

**User:** "Let's do PEA-201"

**Step 3 - Analyze:**
```
## Question Analysis: PEA-201

**Question:** Should we support OAuth2?
**Asked by:** Product Manager
**Context:** Customer requests for SSO integration
**Impact:** High - affects architecture
```

**Step 4 - Explore Codebase (MANDATORY):**
```
Dispatching Explore agent to research OAuth2 context...

## Codebase Analysis

### Related Files Found
- `src/auth/index.ts` - Main auth module (lines 1-89)
- `src/auth/strategies/local.ts` - Current local auth strategy
- `src/middleware/authenticate.ts` - Auth middleware
- `src/config/auth.config.ts` - Auth configuration

### Existing Patterns
- Using Passport.js for auth strategies (src/auth/index.ts:12)
- LocalStrategy configured for email/password (strategies/local.ts)
- Auth middleware supports multiple strategies via `passport.authenticate()`

### Dependencies (from package.json)
- `passport` v0.6.0 - Supports OAuth plugins
- `passport-local` - Current strategy
- No OAuth packages installed yet

### Key Findings
1. **Passport architecture ready for OAuth** - Already using passport,
   adding OAuth is a plugin install (passport-google-oauth20, etc.)
2. **No user.oauthProvider field** - Database schema needs update
3. **Session handling exists** - `src/auth/session.ts` already handles sessions
4. **Config has OAuth placeholders** - `auth.config.ts:45` has commented OAuth config

### Effort Estimate
- Database migration: Add oauth columns to users table
- New strategy files: ~200 lines each provider
- Config updates: Minimal
- Existing code changes: Low impact
```

**Research findings indicate this is feasible with moderate effort.**

**Step 5 - Decision (informed by codebase exploration):**
```
## Decision

Based on codebase analysis:
- ✅ Passport.js already supports OAuth plugins
- ✅ Session infrastructure exists
- ⚠️ Database schema needs oauth columns
- ⚠️ Need to decide which providers (Google, GitHub, etc.)

**Recommendation:** Create a spec to explore OAuth2 requirements
- Which OAuth providers to support (customer feedback needed)
- Scope: login only vs full authorization
- Security requirements for token storage
- Migration strategy for existing users

**Technical feasibility:** Moderate effort, architecture supports it.

Proceed with /create-linear-spec for OAuth2?
```

**User:** "Yes"

**Step 6-7 - Execute:**
```
Created spec project "OAuth2 Integration" via /create-linear-spec
Closed PEA-201 with comment linking to new project

## Question Resolved

**Question:** PEA-201 - Should we support OAuth2?
**Decision:** Create spec for proper requirements discovery
**Action:** Created "OAuth2 Integration" project
**Status:** Original question closed

Next question?
```

---

## Quick Reference

```
PROCESS: List → Select → Analyze → EXPLORE CODEBASE → Decide → Execute → Confirm
OUTPUT:  Decisions and Linear actions (issues, comments, state changes)
NEVER:   Code changes, GitHub PRs, file modifications

MANDATORY EXPLORATION:
- Use Explore agent for comprehensive analysis
- Search for related files, patterns, dependencies
- Present findings BEFORE making decisions
- Include file paths and line numbers in analysis

VALID OUTCOMES:
- Create issue (clear scope)
- Create spec (unclear scope)
- Add to project (existing work)
- Close with answer (no work needed)
- Close as won't do (out of scope)

TOOLS:
- Task(subagent_type: "Explore") - Codebase exploration
- Glob, Grep, Read - Direct search
- mcp__linear-server__list_issues (find questions)
- mcp__linear-server__get_issue (read details)
- mcp__linear-server__create_issue (new work)
- mcp__linear-server__create_comment (add answer)
- mcp__linear-server__update_issue (close/update)
```

## Red Flags - STOP

- About to write code → STOP, this is a question skill
- About to create a PR → STOP, questions produce decisions
- About to modify files → STOP, read-only research allowed
- Unclear decision → STOP, ask for clarification

---

## Integration

**Uses:**
- **Linear MCP** - All issue operations
- **create-linear-spec** - When question needs requirements discovery
- **create-linear-plan** - When question reveals clear work items

**Does NOT use:**
- Git operations
- File write/edit operations
- PR submission skills

## Trigger Keywords

- "linear questions"
- "answer questions"
- "review questions"
- "question triage"
- "pending questions"

---
name: delegate
description: Delegate tasks to specialized subagents. Analyzes requirements, selects appropriate agents, and launches them with proper context while enforcing the max-2-parallel rule.
---

# Delegate Skill

Automatically delegate tasks to the most appropriate specialized subagent.

## Usage

```
/delegate "implement user authentication"
/delegate "review the payment module for security issues"
/delegate "write unit tests for the API endpoints"
```

## How It Works

### Step 1: Analyze Task Requirements

Parse the task description to identify:
- **Domain**: frontend, backend, API, database, security, testing, etc.
- **Action**: implement, review, test, refactor, analyze, document
- **Technology**: React, Django, Node, Python, etc. (if detectable from codebase)

### Step 1.5: Load Coding Standards

Before delegating, auto-inject relevant coding standards based on the project's tech stack:

1. Read `.claude/config/coding-standards.json` for detection rules
2. Check `TECHSTACK.md` or codebase patterns to identify technologies
3. Load matching AGENTS.md files as additional context for the subagent

**Detection Rules:**

| Pattern Detected | Standards Loaded |
|------------------|------------------|
| WordPress, wp-content, Divi, Elementor | wordpress, php, mysql |
| Next.js, App Router, use client | nextjs, react, javascript |
| Laravel, Eloquent, Blade, Livewire | laravel, php, mysql |
| Supabase, RLS, auth.uid() | supabase |
| MariaDB, Galera | mariadb, mysql |
| React, useState, JSX | react, javascript |
| PHP, composer.json | php |
| MySQL, my.cnf | mysql |

**Include in Subagent Prompt:**

```markdown
## Coding Standards

Follow these coding standards for this task. Focus on CRITICAL and HIGH impact rules:

[Include relevant AGENTS.md content here]

Key rules to follow:
- [List 3-5 most relevant CRITICAL rules from loaded standards]
```

**Example:**
If `TECHSTACK.md` mentions "Next.js" and "Supabase":
- Load: `setup/skills/nextjs-best-practices/AGENTS.md`
- Load: `setup/skills/react-best-practices/AGENTS.md`
- Load: `setup/skills/javascript-best-practices/AGENTS.md`
- Load: `setup/skills/supabase-best-practices/AGENTS.md`

### Step 2: Check Parallel Execution Slots

Read `CLAUDE-activeContext.md` to check parallel execution tracking:

```markdown
## Parallel Execution Tracking

**Maximum Concurrent Agents:** 2

| Slot | Agent | Task | Status |
|------|-------|------|--------|
| 1 | [agent] | [task] | Active/Available |
| 2 | [agent] | [task] | Active/Available |
```

**Rules:**
- If both slots are Active, QUEUE the task and notify user
- If at least one slot is Available, proceed with delegation

### Step 3: Select Appropriate Agent

#### Agent Selection Hierarchy

1. **Exact match**: Task mentions specific technology → use specialist
2. **Domain match**: Task domain matches agent specialty → use domain expert
3. **Universal fallback**: No specialist → use general-purpose agent

#### Available Agents (from `setup/agents/critical/`)

| Agent | Specialty | Use When |
|-------|-----------|----------|
| `software-engineer` | Implementation | Building features, writing code |
| `code-reviewer` | Quality | Reviewing code for issues |
| `qa-engineer` | Testing | Writing tests, quality assurance |
| `product-manager` | Requirements | Clarifying scope, priorities |

#### Phase-Based Agent Assignment

If current phase is known (from `CLAUDE-activeContext.md`), prefer phase-appropriate agent:

| Phase | Preferred Agent |
|-------|-----------------|
| 2-3 | Requirements Analyst / Solution Architect |
| 4-5 | Technical Planner / Software Engineer |
| 6 | QA Engineer |
| 7 | Security Auditor |
| 8 | Code Reviewer |
| 9 | DevOps Engineer |

### Step 4: Launch Subagent

Use the Task tool to launch the selected agent:

```
Task:
  description: "[3-5 word summary]"
  prompt: |
    ## Context
    [Current phase and project context from CLAUDE-activeContext.md]

    ## Task
    [Full task description from user]

    ## Coding Standards
    Follow these coding standards for this task. Focus on CRITICAL and HIGH impact rules:

    [Include relevant AGENTS.md content based on detected tech stack]

    Key rules to enforce:
    - [List 3-5 most relevant CRITICAL rules]

    ## Constraints
    - Follow patterns in CLAUDE-patterns.md
    - Follow coding standards loaded above
    - Update CLAUDE-activeContext.md when complete
    - Report findings back to main agent

    ## Deliverables
    [Expected outputs]
  subagent_type: [agent-type]
```

### Step 5: Update Tracking

Update `CLAUDE-activeContext.md`:

```markdown
## Active Tasks

| ID | Task | Agent | Status | Started |
|----|------|-------|--------|---------|
| T-001 | [task summary] | [agent] | In Progress | [timestamp] |

## Parallel Execution Tracking

| Slot | Agent | Task | Status |
|------|-------|------|--------|
| 1 | [agent] | [task] | Active |
| 2 | - | - | Available |
```

## Agent Matching Examples

### Example 1: Security Task
```
Input: "review the API for SQL injection vulnerabilities"

Analysis:
- Domain: security
- Action: review
- Technology: API/backend

Selection: Security Auditor (if available) or Code Reviewer
Reasoning: Security-focused review requires security expertise
```

### Example 2: Implementation Task
```
Input: "implement user registration with email verification"

Analysis:
- Domain: backend
- Action: implement
- Technology: authentication

Selection: Software Engineer
Reasoning: Implementation task for new feature
```

### Example 3: Testing Task
```
Input: "write integration tests for the checkout flow"

Analysis:
- Domain: testing
- Action: write tests
- Technology: e-commerce

Selection: QA Engineer
Reasoning: Testing task requires QA expertise
```

### Example 4: Parallel Limit Reached
```
Current State:
- Slot 1: Active (software-engineer working on auth)
- Slot 2: Active (qa-engineer writing tests)

Input: "refactor the database models"

Response:
"Cannot delegate now - maximum 2 agents already running.
Current tasks:
1. software-engineer: implementing auth
2. qa-engineer: writing tests

Task queued. Will delegate when a slot becomes available."
```

## Subagent Types Mapping

Map agents to Claude Code subagent types:

| Agent | subagent_type | Model |
|-------|---------------|-------|
| software-engineer | Explore or general-purpose | sonnet |
| code-reviewer | Explore | sonnet |
| qa-engineer | general-purpose | sonnet |
| code-searcher | Explore | sonnet |
| product-manager | Plan | sonnet |

## Task Completion Handling

When a subagent completes:

1. Update `CLAUDE-activeContext.md`:
   - Change task status to "Completed"
   - Free the parallel execution slot
   - Add completion entry to Session Log

2. Check queued tasks:
   - If tasks are queued, delegate the next one

3. Report results:
   - Summarize findings to user
   - Suggest next actions if applicable

## Error Handling

- **No matching agent**: Use `general-purpose` subagent with detailed context
- **Agent definition not found**: Fall back to built-in subagent types
- **Memory bank missing**: Create `CLAUDE-activeContext.md` with default structure

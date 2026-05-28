# The Agentic Shift: Deep Dive Guide

> Optional reading. Start with [Quick Start](QUICK_START.md) if you just want to get going.

This document covers the full workflow in detail, including team rollout considerations, MCP configuration, and governance. Read this when you're ready to go beyond the basics.

**Also see:**
- [Limitations](LIMITATIONS.md) — When not to use this
- [Enterprise Guide](ENTERPRISE.md) — Compliance, security, large orgs

---

## Overview

The core workflow is simple: you write specs, Claude generates code, you approve.

### The New Developer Role

| Traditional Role | Agentic Role |
|-----------------|--------------|
| Write every line of code | Write specs describing WHAT you want |
| Write tests manually | Review Claude-generated tests |
| Debug through trial and error | Validate against spec requirements |
| Context-switch between tools | Answer Claude's context questions |
| Manual code review | Approve or iterate on generated code |
| Repeat patterns manually | Capture patterns as reusable skills |

---

## Phase 1: Foundation

### 1.1 Environment Setup

#### Individual Developer Setup

```bash
# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login

# Verify installation
claude --version
```

#### Team Configuration Checklist

| Component | Action | Notes |
|-----------|--------|-------|
| API Access | Provision API keys via Anthropic Console | Required for all setups |
| SSO Integration | Configure SAML/OIDC | Enterprise only, skip if not needed |
| Usage Limits | Set token budgets per developer | Recommended to avoid surprise costs |
| Audit Logging | Enable API request logging | Optional, useful for compliance |

#### Repository Initialization

```bash
# In each project repository
claude /init

# This creates:
# - .claude/settings.json (project config)
# - CLAUDE.md (context document)
```

### 1.2 Security Guardrails

#### Tier 1: Mandatory Controls

Document and communicate these security boundaries to your team:

**Commands requiring confirmation** (Claude Code prompts for these by default):
- `git push`, `git push --force`
- `npm publish`, `docker push`
- `terraform apply`, `kubectl delete`
- Any destructive file operations

**Patterns to watch for** (add to your CLAUDE.md "Do NOT" section):
- Hardcoded secrets, API keys, tokens
- Direct database credential strings
- `rm -rf` on system or home directories
- Piping curl/wget output to shell

**Team guidelines to document**:
```markdown
## Security Rules for Claude Code

1. Never commit secrets - use environment variables
2. Review all generated shell commands before confirming
3. Don't allow Claude to modify CI/CD or infrastructure configs without review
4. Keep sensitive files in .gitignore
```

#### Tier 2: Code Review Gates

Use pre-commit hooks for automated checks. See the `templates/` folder in the onboarding skill for ready-to-use hooks, or create your own:

**Simple secrets detection** (no Claude required):
```bash
#!/bin/bash
# .git/hooks/pre-commit
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
if grep -rE "(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]{8,}" $STAGED 2>/dev/null; then
  echo "Potential secrets detected. Please review."
  exit 1
fi
```

**Claude-assisted review** (optional, for deeper analysis):
```bash
#!/bin/bash
# Requires Claude Code CLI
STAGED=$(git diff --cached --name-only --diff-filter=ACM)
[ -z "$STAGED" ] && exit 0
echo "Files to review: $STAGED"
claude -p "Review these files for security issues: $STAGED. Be concise."
```

> **Tip**: Start with simple pattern matching. Add Claude-powered analysis once your team is comfortable with the basics.

#### Tier 3: Network & Data Controls

| Control | Implementation |
|---------|----------------|
| Egress Filtering | Restrict Claude's web access to approved domains |
| PII Scanning | Prevent sensitive data in prompts via preprocessing |
| Audit Trail | Log all Claude interactions with timestamps |
| Data Residency | Configure region-specific API endpoints if required |

---

## Phase 2: Tooling Integration

### 2.1 Model Context Protocol (MCP) Selection

MCPs extend Claude Code with real-time access to external systems. Select based on your team's needs:

| MCP Server | Use Case | Priority | Setup Complexity |
|------------|----------|----------|------------------|
| **GitHub** | PR reviews, issue triage, code search | High | Low |
| **Filesystem** | Enhanced file operations | High | Low |
| **Postgres** | Schema exploration, query generation | High | Medium |
| **Figma** | Frontend: design specs, component generation | High (frontend) | Low |
| **Slack** | Team notifications, standup automation | Medium | Low |
| **Jira** | Sprint planning, ticket management | Medium | Medium |
| **Playwright** | E2E test generation, browser automation | Medium | High |
| **Memory** | Persistent context across sessions | Low | Low |

### 2.2 MCP Configuration

Create or update `~/.claude/mcp_servers.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/directory"]
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "${FIGMA_ACCESS_TOKEN}"
      }
    }
  }
}
```

### 2.3 Validation Checklist

After configuration, verify each MCP:

```bash
# GitHub: List recent issues
claude "List the 5 most recent open issues in this repository"

# Postgres: Describe schema
claude "Show me all tables and their columns in the database"

# Slack: Test notification
claude "Send a test message to #engineering-test channel"
```

---

## Phase 3: Workflow Transformation

### 3.1 The Architect-Reviewer Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRADITIONAL WORKFLOW                          │
│  Developer → Code → Test → Debug → Code → Test → PR → Review    │
│                    [High cognitive load]                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    AGENTIC WORKFLOW                              │
│                                                                  │
│  ARCHITECT PHASE          AGENT PHASE           REVIEW PHASE    │
│  ┌──────────────┐        ┌──────────────┐      ┌──────────────┐ │
│  │ Define Intent│   →    │ Claude Code  │  →   │ Validate &   │ │
│  │ Set Constraints│      │ Implements   │      │ Refine       │ │
│  │ Write Tests  │        │ Iterates     │      │ Approve      │ │
│  └──────────────┘        └──────────────┘      └──────────────┘ │
│      [Human]                 [Agent]               [Human]       │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 The Specification-Driven Cycle

This is the core workflow pattern:

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│  1. SPECIFY    2. CONTEXT     3. PLAN       4. GENERATE    5. REVIEW      │
│     (You)        (Claude)       (Interactive)  (Claude)       (AI)        │
│                                                                           │
│  PRD/spec/    "What patterns  "Here's my    Tests first,   AI-assisted   │
│  story        do you use?"    execution     then code      code review   │
│                               plan..."                                    │
│                               [You approve]                               │
│                                                                           │
│         └────────────┴──────────────┴──────────────┴──────────────┘       │
│                                      ▼                                    │
│                               6. VALIDATE                                 │
│                            (Claude iterates)                              │
│                                                                           │
│              Run tests → Fix failures → Repeat until passing              │
│                         Then you approve final result                     │
└───────────────────────────────────────────────────────────────────────────┘
```

**Key Principle**: You define WHAT should exist. Claude figures out HOW, runs AI review, iterates on test failures, and presents the final result for your approval.

#### Example Session

**Step 1: You write a spec**
```markdown
## Feature: JWT Token Validation

### Requirements
- Validate JWT tokens and extract user data
- Return userId and role from valid tokens
- Throw TokenError for expired tokens
- Use jose library for JWT handling
```

**Step 2: Give spec to Claude**
```
Here's my feature spec: [paste spec]

Ask me clarifying questions, then:
1. Create an execution plan for my approval
2. Propose tests based on requirements
3. Wait for my approval
4. Implement to pass the tests
```

**Step 3: Claude asks context questions**
```
"Where should this module live? What's your error handling pattern?"
```

**Step 4: Claude presents execution plan, you approve or adjust**
```
"Here's my plan: create src/auth/jwt.ts, add tests in src/auth/jwt.test.ts,
use your existing TokenError class. Does this look right?"
```

**Step 5: Claude proposes tests, you approve**

**Step 6: Claude implements, runs AI code review**
```
"Code review complete. Found 1 suggestion: use async bcrypt.
Should I fix this before running tests?"
```

**Step 7: Claude runs tests, iterates on failures**
```
"Running tests... 3/4 passing. Fixing duplicate email handler..."
"Running tests... 4/4 passing. Here's the final diff for your approval."
```

**Step 8: You approve the final implementation**

### 3.3 Daily Workflow Integration

#### Morning Standup

```bash
claude "Analyze my git commits from yesterday and any Jira tickets
        I'm assigned to. Generate a standup summary with:
        - What I completed
        - What I'm working on today
        - Any blockers"
```

#### Feature Development

1. **Understand**: "Explain how the current authentication flow works"
2. **Plan**: "What files need to change to add OAuth support?"
3. **Specify**: Write tests describing the new behavior
4. **Implement**: "Make these tests pass following our patterns"
5. **Validate**: Review diff, run full test suite
6. **Ship**: Approve and merge

#### Code Review

```bash
claude "Review PR #123. Check for:
        - Logic errors
        - Security issues
        - Performance concerns
        - Style consistency
        Provide specific, actionable feedback."
```

---

## Phase 4: Governance & Compliance

### 4.1 Pre-Push Audit Pipeline

For comprehensive pre-push auditing, use the templates provided in `agentic-shift-skill/templates/`:

- `pre-commit.template` - Fast checks before each commit
- `pre-push.template` - Deeper analysis before pushing

**Installation:**
```bash
cp templates/pre-push.template .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

**What the hooks check:**
- Hardcoded secrets and credentials
- Common security anti-patterns
- Code style violations (optional)

> **Start simple**: Begin with just the pre-commit hook. Add pre-push later once your team is comfortable with the workflow.

### 4.2 Metrics & KPIs (Optional)

Track these metrics if your team values data-driven improvement:

| Metric | How to Measure | What to Look For |
|--------|---------------|------------------|
| **Time to First PR** | Git timestamps | Reduction over time |
| **PR Review Cycles** | Rounds of feedback per PR | Fewer iterations needed |
| **Bug Escape Rate** | Post-deploy bugs / total deploys | Decreasing trend |
| **Test Coverage** | Coverage reports | Steady improvement |
| **Developer Feedback** | Regular check-ins or surveys | Positive sentiment |

> **Note**: Don't over-optimize for metrics. The goal is better developer experience, not perfect numbers.

### 4.3 Compliance Checklist

Before declaring the transition complete:

- [ ] All repositories have CLAUDE.md files
- [ ] Pre-commit/pre-push hooks installed organization-wide
- [ ] MCP servers configured for critical integrations
- [ ] Team completed onboarding skill (all 5 modules)
- [ ] At least 3 team-specific skills created
- [ ] Metrics dashboard operational
- [ ] Security review of Claude Code permissions complete
- [ ] Incident response plan updated for AI-assisted development

---

## Quick Reference

### Essential Commands

```bash
# Start Claude Code in a project
claude

# Use a skill
claude /skill-name

# Get help
claude /help

# Common prompting patterns
claude "Explain how the auth module works"
claude "Write tests for src/utils.ts"
claude "Review my staged changes for issues"
```

### Effective Prompting Patterns

| Pattern | Example |
|---------|---------|
| **Constrained** | "Modify ONLY the handleAuth function in src/auth.ts" |
| **Test-First** | "Make tests/auth.test.ts pass without changing the tests" |
| **Pattern-Following** | "Follow the existing error handling pattern in src/errors.ts" |
| **Incremental** | "First, explain your plan. Then implement step by step." |
| **Review-Oriented** | "Show me the diff before applying any changes" |

### Red Flags to Watch For

- Claude suggesting changes outside the requested scope
- Generated code that doesn't match project patterns
- Security-sensitive operations without confirmation
- Modifications to configuration or infrastructure files
- Any action that feels "too automatic"

---

## Appendix: Self-Paced Milestone Tracker

Use this checklist to track your team's progress. Complete each phase before moving to the next.

### Phase 1: Foundation
- [ ] All developers have Claude Code CLI installed and authenticated
- [ ] Every active repository has a CLAUDE.md file
- [ ] Security guardrails documented and communicated

### Phase 2: Tooling Integration
- [ ] At least one MCP server configured (start with GitHub)
- [ ] Team can query external systems through Claude
- [ ] MCP configuration documented for new team members

### Phase 3: Workflow Transformation
- [ ] Team completed TDA training (Module 3 of onboarding)
- [ ] At least one feature shipped using the TDA cycle
- [ ] Daily workflow patterns established

### Phase 4: Governance & Compliance
- [ ] Pre-commit/pre-push hooks installed on all repositories
- [ ] Metrics tracking operational (optional but recommended)
- [ ] At least one team-specific skill created and shared

### Graduation
- [ ] Retrospective completed with team feedback
- [ ] Documentation updated with team learnings
- [ ] Continuous improvement process established

---

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Onboarding Skill](/agentic-shift-onboard) - Interactive tutorial

---

*The Agentic Shift v1.0 - Transform how your team builds software.*

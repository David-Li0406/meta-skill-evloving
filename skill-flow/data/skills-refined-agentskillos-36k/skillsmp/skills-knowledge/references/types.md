# Skill Types Reference

## Table of Contents

- [Comparison Table](#comparison-table)
- [Type 1: Auto-Discoverable Skills](#type-1-auto-discoverable-skills)
- [Checklist](#checklist)
- [Best Practices](#best-practices)
- [Security Checklist](#security-checklist)
- [Type 2: User-Triggered Skills](#type-2-user-triggered-skills)
- [Pre-deployment Checks](#pre-deployment-checks)
- [Deployment Steps](#deployment-steps)
- [Rollback (if needed)](#rollback-if-needed)
- [Type 3: Background Context Skills](#type-3-background-context-skills)
- [Session Management](#session-management)
- [User Roles](#user-roles)
- [Migration Path](#migration-path)
- [Code Style](#code-style)
- [Git Workflow](#git-workflow)
- [Testing Standards](#testing-standards)
- [Invocation Control Matrix](#invocation-control-matrix)
- [Argument Handling](#argument-handling)
- [Migration Path](#migration-path)
- [Key Differences Summary](#key-differences-summary)
- [Choosing the Right Type](#choosing-the-right-type)

Detailed comparison of the three skill types with examples and use cases.

## Comparison Table

| Need | Choose | Example |
|------|--------|---------|
| Rich workflow with supporting files | Skill | `skills/api-review/SKILL.md` |
| Simple bash/file wrapper | Command | `commands/quick-deploy.md` |
| Complex analysis in isolation | Subagent | `context: fork, agent: Explore` |
| Read/modify files | Native Tools | `Read`, `Edit`, `Grep` |

## Type 1: Auto-Discoverable Skills

### Description
Claude discovers and uses when relevant. User can also invoke via `/name`.

### When to Use
- Domain expertise that should be auto-discovered
- Reference content that enhances understanding
- Workflows that benefit from automatic activation
- Context that should always be available

### Example 1: API Review
```yaml
---
name: api-review
description: "API design review patterns for this codebase. Use when designing, reviewing, or modifying API endpoints."
---

# API Review

When reviewing API endpoints:

## Checklist
- [ ] RESTful naming conventions
- [ ] Consistent error formats
- [ ] Request validation implemented
- [ ] Response schemas documented
- [ ] Authentication documented

## Best Practices
1. Use nouns for resources
2. Pluralize resource names
3. Use HTTP verbs appropriately (GET, POST, PUT, DELETE)
4. Return meaningful status codes
5. Include pagination for lists
```

### Example 2: Security Review
```yaml
---
name: security-review
description: "Security review patterns and checklists. Use when reviewing code for security vulnerabilities."
---

# Security Review

## Security Checklist
- [ ] Input validation
- [ ] Authentication checks
- [ ] Authorization verification
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] CSRF tokens
- [ ] Secure session management
```

## Type 2: User-Triggered Skills

### Description
Only user can invoke via `/name`. Use for side-effects, timing-critical, or destructive actions.

### When to Use
- Deploy operations
- Git commits
- Send messages
- Database migrations
- Production actions
- Any operation with side effects

### Example 1: Deploy Skill
```yaml
---
name: deploy
description: "Deploy application to specified environment"
disable-model-invocation: true
argument-hint: [environment]
allowed-tools: Bash(kubectl:*), Bash(docker:*), Read
---

# Deploy

Deploy to $ARGUMENTS:

## Pre-deployment Checks
- Verify environment: !`echo "$ARGUMENTS" | grep -E "^(dev|staging|prod)$"`
- Check tests passing: !`npm test 2>&1 | tail -1`
- Verify build: !`npm run build 2>&1 | tail -1`

## Deployment Steps
1. Build application: !`npm run build`
2. Push to registry: !`docker build -t app:$ARGUMENTS .`
3. Deploy to $ARGUMENTS: !`kubectl apply -f k8s/$ARGUMENTS.yaml`
4. Verify health: !`kubectl rollout status deployment/app`

## Rollback (if needed)
If deployment fails:
!`kubectl rollout undo deployment/app`

Report status after each step.
```

### Example 2: Commit Skill
```yaml
---
name: commit
description: "Create well-formatted git commits"
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Create Commit

Create commit for staged changes:

1. Analyze staged changes: !`git diff --cached --stat`
2. Generate descriptive commit message following conventional commits
3. Create commit
4. Show result
```

### Example 3: Fix Issue Skill
```yaml
---
name: fix-issue
description: "Fix a GitHub issue by number"
disable-model-invocation: true
argument-hint: [issue-number]
---

Fix GitHub issue $ARGUMENTS following our coding standards.
```

### When NOT to Use disable-model-invocation

Don't use for domain expertise:

```yaml
# ❌ WRONG - This should be auto-discoverable
---
name: api-conventions
description: "API design patterns"
disable-model-invocation: true
---

# ✅ CORRECT - Let Claude discover when relevant
---
name: api-conventions
description: "API design patterns for this codebase. Use when writing API endpoints."
---
```

## Type 3: Background Context Skills

### Description
Only Claude uses. Hidden from `/` menu. Use for context that enhances understanding.

### When to Use
- Legacy system documentation
- Project-specific context
- Team conventions
- Historical information
- Background knowledge

### Example 1: Legacy System Context
```yaml
---
name: legacy-auth-context
description: "Explains the legacy authentication architecture"
user-invocable: false
---

# Legacy Authentication System

The legacy auth system uses session-based authentication with the following characteristics:

## Session Management
- Sessions stored in Redis
- 24-hour expiration
- Automatic refresh on activity

## User Roles
- admin: Full system access
- user: Standard access
- guest: Read-only access

## Migration Path
We are migrating to JWT-based auth. See migration-guide.md for details.
```

### Example 2: Team Conventions
```yaml
---
name: team-conventions
description: "Documents team coding conventions and standards"
user-invocable: false
---

# Team Conventions

## Code Style
- Use TypeScript for all new code
- 2-space indentation
- Semicolons required
- ESLint configuration in .eslintrc.json

## Git Workflow
- main: Production-ready code only
- develop: Integration branch
- feature/*: Feature branches
- hotfix/*: Production fixes

## Testing Standards
- Minimum 80% code coverage
- All PRs require tests
- Use Jest for unit tests
- Use Cypress for E2E tests
```

## Invocation Control Matrix

| Frontmatter | User Can Invoke | Claude Can Invoke | Use Case |
|-------------|-----------------|-------------------|----------|
| (default) | ✅ Yes | ✅ Yes | Domain expertise, reference content |
| `disable-model-invocation: true` | ✅ Yes | ❌ No | Deploy, commit, send actions |
| `user-invocable: false` | ❌ No | ✅ Yes | Background context |

## Argument Handling

### Basic Arguments
```yaml
---
name: deploy
description: "Deploy to environment"
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $ARGUMENTS:
```

### Positional Arguments
```yaml
---
name: deploy-version
description: "Deploy specific version to environment"
disable-model-invocation: true
argument-hint: [environment] [version]
---

Deploy version $2 to $1 environment.
```

## Migration Path

### From Commands to Skills

**Old: `.claude/commands/deploy.md`**
```yaml
---
description: "Deploy application"
---
Deploy application:
1. Build
2. Deploy
3. Verify
```

**New: `.claude/skills/deploy/SKILL.md`**
```yaml
---
name: deploy
description: "Deploy application to production"
disable-model-invocation: true
argument-hint: [environment]
---

Deploy to $ARGUMENTS:
1. Build
2. Deploy
3. Verify
```

Both create the same `/deploy` invocation, but skills offer more features.

## Key Differences Summary

| Feature | Auto-Discoverable | User-Triggered | Background |
|---------|-------------------|----------------|------------|
| User invokes | ✅ | ✅ | ❌ |
| Claude invokes | ✅ | ❌ | ✅ |
| Hidden from `/` | ❌ | ❌ | ✅ |
| Side effects | ❌ | ✅ | ❌ |
| Auto-activation | ✅ | ❌ | ✅ |
| Use case | Domain expertise | Destructive actions | Context |

## Choosing the Right Type

### Decision Tree

```
START: What is the skill for?
│
├─ Background knowledge only?
│  └─→ user-invocable: false
│
├─ User controls timing?
│  ├─ Has side effects?
│  │  └─→ disable-model-invocation: true
│  └─ No side effects?
│     └─→ Default (auto-discoverable)
│
└─ Should Claude auto-use?
   └─→ Default (auto-discoverable)
```

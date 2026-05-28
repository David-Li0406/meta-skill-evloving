# GitHub Issue Guidelines (5W1H Principle)

> **Version**: 1.5.0
> **Extracted from**: workflow.md
> **Purpose**: Comprehensive framework for creating actionable GitHub issues

When creating GitHub issues, follow the **5W1H framework** to ensure comprehensive and actionable documentation.

## Language and Attribution Policy

### Language Requirement

**All issues MUST be written in English** for:
- Global accessibility and collaboration
- Consistency with codebase and documentation standards
- Integration with automated tools and CI/CD systems

```markdown
<!-- ✅ Correct: English issue -->
## What
The user authentication endpoint returns 500 error when...

<!-- ❌ Incorrect: Non-English issue -->
## 내용
사용자 인증 엔드포인트에서 500 에러가...
```

### No AI/Claude Attribution

**Exclude all AI-related references** from issues:

```markdown
<!-- ❌ Do NOT include -->
🤖 Generated with Claude Code
Created with AI assistance
Co-Authored-By: Claude <noreply@anthropic.com>
```

This policy ensures:
- Professional appearance in public repositories
- Focus on the technical content
- Compliance with organizational standards

## 1. What

**Describe the task or problem clearly**

- **Title**: Concise, descriptive summary (50 characters or less ideal)
- **Description**: Detailed explanation of what needs to be done or what the problem is
- **Current behavior**: What is happening now (for bugs)
- **Expected behavior**: What should happen instead
- **Scope**: Define boundaries - what IS and IS NOT included in this issue

```markdown
## What
- Implement user authentication using JWT tokens
- Current: No authentication exists
- Expected: Users can register, login, and access protected routes
- Scope: Backend API only (frontend will be separate issue)
```

## 2. Why

**Explain the motivation and business value**

- **Problem statement**: Why does this issue exist?
- **Impact**: What happens if this is not addressed?
- **Business value**: How does solving this benefit users or the project?
- **Priority justification**: Why this priority level?

```markdown
## Why
- Users cannot securely access personal data without authentication
- Impact: Security vulnerability, cannot launch to production
- Value: Enables personalized features and data protection
- Priority: Critical - blocks all user-facing features
```

## 3. Who

**Identify stakeholders and responsibilities**

- **Assignee**: Who will work on this?
- **Reviewer**: Who should review the solution?
- **Stakeholders**: Who is affected by this issue?
- **Reporter**: Who identified this issue? (for context/questions)

```markdown
## Who
- Assignee: @backend-team
- Reviewer: @security-lead
- Stakeholders: All users requiring login
- Reporter: @product-manager (for requirement clarification)
```

## 4. When

**Define timeline and milestones**

- **Due date**: When should this be completed?
- **Milestone**: Which release or sprint does this belong to?
- **Dependencies**: What must be completed before this can start?
- **Blockers**: What is preventing progress? (if applicable)

```markdown
## When
- Due: 2024-12-15
- Milestone: v2.0.0 Release
- Dependencies: Database schema migration (#123)
- Blockers: Waiting for security audit results
```

## 5. Where

**Specify location and context**

- **Affected files/components**: Which parts of the codebase are involved?
- **Environment**: Development, staging, production?
- **Platform**: Web, mobile, API, specific OS?
- **Related issues/PRs**: Links to connected work

```markdown
## Where
- Files: `src/auth/`, `src/middleware/auth.ts`
- Environment: All environments
- Platform: REST API (Node.js backend)
- Related: #120 (user model), #125 (frontend login page)
```

## 6. How

**Outline the implementation approach**

- **Technical approach**: High-level solution design
- **Acceptance criteria**: Specific, testable conditions for completion
- **Steps to reproduce**: (for bugs) Exact steps to recreate the issue
- **Testing requirements**: How will this be verified?

```markdown
## How

### Technical Approach
1. Implement JWT token generation on login
2. Create authentication middleware
3. Add token refresh endpoint
4. Integrate with existing user model

### Acceptance Criteria
- [ ] User can register with email/password
- [ ] User can login and receive JWT token
- [ ] Protected routes reject requests without valid token
- [ ] Token expires after 24 hours
- [ ] Refresh token extends session

### Testing Requirements
- Unit tests for auth service (>80% coverage)
- Integration tests for auth endpoints
- Security penetration test for token handling
```

## Issue Template

```markdown
## What
<!-- Clear description of the task or problem -->

## Why
<!-- Motivation, impact, and business value -->

## Who
- Assignee:
- Reviewer:
- Stakeholders:

## When
- Due:
- Milestone:
- Dependencies:

## Where
- Files/Components:
- Environment:
- Related Issues:

## How

### Technical Approach
<!-- High-level implementation plan -->

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Additional Context
<!-- Screenshots, logs, references -->
```

## Quick Reference

### Pre-Submit Checklist

- [ ] **What**: Is the task/problem clearly described?
- [ ] **Why**: Is the motivation and impact explained?
- [ ] **Who**: Are assignees and stakeholders identified?
- [ ] **When**: Are deadlines and dependencies specified?
- [ ] **Where**: Are affected areas and related issues linked?
- [ ] **How**: Are acceptance criteria and approach defined?

### Issue Types and Required Fields

| Issue Type | Required 5W1H | Optional |
|------------|---------------|----------|
| **Bug** | What, Why, Where, How (reproduce) | When, Who |
| **Feature** | What, Why, How (criteria) | When, Where, Who |
| **Task** | What, How (criteria) | Why, When, Where, Who |
| **Epic** | What, Why, When | Where, How, Who |
| **Hotfix** | What, Why, Where, How | When (ASAP), Who |

### Priority Labels

Use priority labels to indicate urgency and importance:

| Label | Description | Response Time | Examples |
|-------|-------------|---------------|----------|
| `priority/critical` | System down, security breach, data loss | Immediate (< 4h) | Production outage, security vulnerability |
| `priority/high` | Major feature broken, blocking release | Same day (< 24h) | Core functionality failure, critical bug |
| `priority/medium` | Important but not urgent, planned work | This sprint | Feature requests, non-critical bugs |
| `priority/low` | Nice to have, minor improvements | Backlog | Minor UI issues, documentation updates |

**Priority Selection Guidelines:**

1. **Critical**: Assign only when business operations are severely impacted
2. **High**: Use for issues blocking other work or affecting many users
3. **Medium**: Default for most planned features and improvements
4. **Low**: For issues that can wait without significant impact

### Type Labels

Classify issues by their nature:

| Label | Description | When to Use |
|-------|-------------|-------------|
| `type/bug` | Something isn't working | Unexpected behavior, errors, crashes |
| `type/feature` | New functionality | Adding new capabilities |
| `type/enhancement` | Improvement to existing feature | Better UX, performance, etc. |
| `type/docs` | Documentation only | README, API docs, comments |
| `type/refactor` | Code restructuring | No behavior change, cleaner code |
| `type/test` | Test-related changes | Adding/fixing tests |
| `type/chore` | Maintenance tasks | Dependencies, configs, cleanup |
| `type/security` | Security-related | Vulnerabilities, hardening |

### Area Labels

Identify affected codebase areas (customize per project):

| Label | Description | Examples |
|-------|-------------|----------|
| `area/api` | API layer | REST endpoints, GraphQL resolvers |
| `area/auth` | Authentication/Authorization | Login, permissions, tokens |
| `area/ui` | User interface | Components, styling, UX |
| `area/db` | Database layer | Schema, queries, migrations |
| `area/infra` | Infrastructure | CI/CD, deployment, Docker |
| `area/core` | Core business logic | Domain models, services |
| `area/config` | Configuration | Settings, environment variables |
| `area/deps` | Dependencies | Package updates, vulnerabilities |

**Defining Project-Specific Areas:**

```markdown
<!-- Recommended: 5-10 areas based on your architecture -->
area/api          # API endpoints
area/auth         # Authentication
area/billing      # Payment & subscriptions
area/notifications # Email, push, SMS
area/analytics    # Metrics, tracking
area/admin        # Admin dashboard
```

### Status Labels

Track issue lifecycle:

| Label | Description | When to Apply |
|-------|-------------|---------------|
| `status/needs-triage` | Awaiting review | Auto-applied to new issues |
| `status/confirmed` | Verified and accepted | After triage review |
| `status/in-progress` | Actively being worked | When work starts |
| `status/needs-info` | Waiting for reporter | Missing details |
| `status/blocked` | Cannot proceed | Dependency or external blocker |
| `status/wontfix` | Will not be addressed | Out of scope, by design |
| `status/duplicate` | Already reported | Link to original issue |

### Label Combinations

```markdown
<!-- Bug report -->
Labels: `type/bug`, `priority/high`, `area/auth`, `status/confirmed`

<!-- New feature -->
Labels: `type/feature`, `priority/medium`, `area/api`, `area/db`

<!-- Security issue -->
Labels: `type/security`, `priority/critical`, `area/auth`

<!-- Documentation -->
Labels: `type/docs`, `priority/low`, `area/api`

<!-- Technical debt -->
Labels: `type/refactor`, `priority/medium`, `area/core`
```

## Mandatory Label Checklist

**IMPORTANT**: Every issue MUST have at least the required labels before submission.

### Required Labels by Issue Type

| Issue Type | Required Labels | Recommended Labels |
|------------|-----------------|-------------------|
| **Bug** | `type/bug`, `priority/*`, `area/*` | `status/*`, `size/*` |
| **Feature** | `type/feature`, `priority/*` | `area/*`, `size/*` |
| **Enhancement** | `type/enhancement`, `priority/*`, `area/*` | `size/*` |
| **Security** | `type/security`, `priority/critical` or `priority/high` | `area/*` |
| **Documentation** | `type/docs` | `area/*` |
| **Refactor** | `type/refactor`, `area/*` | `priority/*`, `size/*` |
| **Task** | `type/task` or `type/chore` | `area/*`, `size/*` |

### Label Validation Checklist

Before creating an issue, verify:

- [ ] **Type label**: One `type/*` label is applied
- [ ] **Priority label**: One `priority/*` label is applied (required for bugs, features, security)
- [ ] **Area label**: At least one `area/*` label is applied (when applicable)
- [ ] **Size label**: One `size/*` label is applied (for sprint planning)
- [ ] **No conflicting labels**: Only one priority, one size, one type

### Label Decision Tree

Use this decision tree to select appropriate labels:

```
┌─ Is it broken/not working?
│   └─ YES → type/bug
│       └─ Production issue? → priority/critical
│       └─ Blocking work? → priority/high
│       └─ Annoying but workaround exists? → priority/medium
│       └─ Minor inconvenience? → priority/low
│
├─ Is it a new capability?
│   └─ YES → type/feature
│       └─ Business critical? → priority/high
│       └─ Nice to have? → priority/medium or priority/low
│
├─ Is it improving existing functionality?
│   └─ YES → type/enhancement
│
├─ Is it security-related?
│   └─ YES → type/security + priority/critical or priority/high
│
├─ Is it code restructuring without behavior change?
│   └─ YES → type/refactor
│
├─ Is it documentation only?
│   └─ YES → type/docs
│
└─ Is it maintenance/configuration?
    └─ YES → type/chore
```

## gh CLI Label Commands

Use the GitHub CLI (`gh`) for efficient issue creation with labels.

### Creating Issues with Labels

```bash
# Basic issue with labels
gh issue create \
  --title "[Bug]: Authentication fails on timeout" \
  --body "$(cat <<'EOF'
## What
Authentication endpoint returns 500 error after 30s timeout.

## Why
Users cannot log in, blocking all authenticated features.

## How
### Steps to Reproduce
1. Navigate to login page
2. Enter credentials
3. Wait 30+ seconds

### Acceptance Criteria
- [ ] Login succeeds within reasonable timeout
- [ ] Proper error message on timeout
EOF
)" \
  --label "type/bug" \
  --label "priority/high" \
  --label "area/auth" \
  --label "size/M"

# Feature request with multiple areas
gh issue create \
  --title "[Feature]: Add OAuth2 support" \
  --body "..." \
  --label "type/feature" \
  --label "priority/medium" \
  --label "area/auth" \
  --label "area/api" \
  --label "size/L"

# Security issue (always high priority)
gh issue create \
  --title "[Security]: SQL injection vulnerability in search" \
  --body "..." \
  --label "type/security" \
  --label "priority/critical" \
  --label "area/db" \
  --label "area/api"
```

### Adding Labels to Existing Issues

```bash
# Add single label
gh issue edit 123 --add-label "priority/high"

# Add multiple labels
gh issue edit 123 --add-label "type/bug" --add-label "area/auth"

# Remove label
gh issue edit 123 --remove-label "status/needs-triage"

# Replace labels (remove old, add new)
gh issue edit 123 \
  --remove-label "priority/medium" \
  --add-label "priority/high"
```

### Listing Issues by Label

```bash
# Find all high priority bugs
gh issue list --label "type/bug" --label "priority/high"

# Find all issues in auth area
gh issue list --label "area/auth"

# Find all critical issues
gh issue list --label "priority/critical" --state open

# Find issues needing triage
gh issue list --label "status/needs-triage" --limit 50
```

### Batch Label Operations

```bash
# Add label to multiple issues
for issue in 101 102 103; do
  gh issue edit $issue --add-label "milestone/v2.0"
done

# Label all untriaged issues as needs-info
gh issue list --label "status/needs-triage" --json number -q '.[].number' | \
  xargs -I {} gh issue edit {} --add-label "status/needs-info"
```

## Automatic Labeling

### GitHub Actions Labeler

Create `.github/labeler.yml` to automatically apply area labels based on changed files:

```yaml
# .github/labeler.yml
area/api:
  - changed-files:
    - any-glob-to-any-file: 'src/api/**/*'
    - any-glob-to-any-file: 'src/routes/**/*'

area/auth:
  - changed-files:
    - any-glob-to-any-file: 'src/auth/**/*'
    - any-glob-to-any-file: 'src/middleware/auth*'

area/db:
  - changed-files:
    - any-glob-to-any-file: 'src/models/**/*'
    - any-glob-to-any-file: 'src/migrations/**/*'
    - any-glob-to-any-file: 'prisma/**/*'

area/ui:
  - changed-files:
    - any-glob-to-any-file: 'src/components/**/*'
    - any-glob-to-any-file: 'src/pages/**/*'
    - any-glob-to-any-file: '**/*.css'
    - any-glob-to-any-file: '**/*.scss'

area/infra:
  - changed-files:
    - any-glob-to-any-file: '.github/**/*'
    - any-glob-to-any-file: 'docker/**/*'
    - any-glob-to-any-file: 'Dockerfile'
    - any-glob-to-any-file: 'docker-compose*.yml'

area/config:
  - changed-files:
    - any-glob-to-any-file: 'config/**/*'
    - any-glob-to-any-file: '*.config.js'
    - any-glob-to-any-file: '*.config.ts'

type/docs:
  - changed-files:
    - any-glob-to-any-file: '**/*.md'
    - any-glob-to-any-file: 'docs/**/*'

type/test:
  - changed-files:
    - any-glob-to-any-file: '**/*.test.*'
    - any-glob-to-any-file: '**/*.spec.*'
    - any-glob-to-any-file: 'tests/**/*'
    - any-glob-to-any-file: '__tests__/**/*'
```

### Labeler Workflow

```yaml
# .github/workflows/labeler.yml
name: Pull Request Labeler

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  labeler:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/labeler@v5
        with:
          repo-token: "${{ secrets.GITHUB_TOKEN }}"
          configuration-path: .github/labeler.yml
```

### Issue Auto-Labeling Workflow

Automatically label new issues based on content:

```yaml
# .github/workflows/issue-labeler.yml
name: Issue Labeler

on:
  issues:
    types: [opened, edited]

permissions:
  issues: write

jobs:
  label-issues:
    runs-on: ubuntu-latest
    steps:
      - name: Auto-label based on title/content
        uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const title = issue.title.toLowerCase();
            const body = (issue.body || '').toLowerCase();
            const content = title + ' ' + body;

            const labelsToAdd = [];

            // Type detection from title prefix
            if (title.startsWith('[bug]')) {
              labelsToAdd.push('type/bug');
            } else if (title.startsWith('[feature]')) {
              labelsToAdd.push('type/feature');
            } else if (title.startsWith('[security]')) {
              labelsToAdd.push('type/security');
              labelsToAdd.push('priority/critical');
            } else if (title.startsWith('[docs]')) {
              labelsToAdd.push('type/docs');
            } else if (title.startsWith('[task]')) {
              labelsToAdd.push('type/task');
            }

            // Area detection from content keywords
            const areaKeywords = {
              'area/auth': ['authentication', 'login', 'logout', 'jwt', 'oauth', 'password', 'session'],
              'area/api': ['endpoint', 'rest', 'graphql', 'api', 'request', 'response'],
              'area/db': ['database', 'query', 'migration', 'schema', 'sql', 'postgres', 'mysql'],
              'area/ui': ['component', 'button', 'form', 'modal', 'css', 'style', 'frontend'],
              'area/infra': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'pipeline']
            };

            for (const [label, keywords] of Object.entries(areaKeywords)) {
              if (keywords.some(kw => content.includes(kw))) {
                labelsToAdd.push(label);
              }
            }

            // Always add needs-triage for new issues
            if (context.payload.action === 'opened') {
              labelsToAdd.push('status/needs-triage');
            }

            // Add labels if any detected
            if (labelsToAdd.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: [...new Set(labelsToAdd)]  // Remove duplicates
              });
            }
```

### Label Validation Workflow

Ensure required labels are present:

```yaml
# .github/workflows/label-validation.yml
name: Label Validation

on:
  issues:
    types: [opened, labeled, unlabeled]
  pull_request:
    types: [opened, labeled, unlabeled]

jobs:
  validate-labels:
    runs-on: ubuntu-latest
    steps:
      - name: Check required labels
        uses: actions/github-script@v7
        with:
          script: |
            const labels = context.payload.issue?.labels || context.payload.pull_request?.labels || [];
            const labelNames = labels.map(l => l.name);

            // Check for type label
            const hasType = labelNames.some(l => l.startsWith('type/'));

            // Check for priority label (required for bugs and features)
            const hasPriority = labelNames.some(l => l.startsWith('priority/'));
            const isBugOrFeature = labelNames.includes('type/bug') || labelNames.includes('type/feature');

            const warnings = [];

            if (!hasType) {
              warnings.push('⚠️ Missing type label (e.g., type/bug, type/feature)');
            }

            if (isBugOrFeature && !hasPriority) {
              warnings.push('⚠️ Bugs and features require a priority label');
            }

            if (warnings.length > 0) {
              console.log('Label validation warnings:');
              warnings.forEach(w => console.log(w));

              // Optionally add a comment
              const number = context.issue?.number || context.payload.pull_request?.number;
              if (number) {
                await github.rest.issues.createComment({
                  owner: context.repo.owner,
                  repo: context.repo.repo,
                  issue_number: number,
                  body: `## Label Validation\n\n${warnings.join('\n')}\n\nPlease add the required labels to this issue.`
                });
              }
            }
```

### Size Labels

Estimate effort for sprint planning:

| Label | Effort | Time Estimate | Examples |
|-------|--------|---------------|----------|
| `size/XS` | Trivial | < 1 hour | Typo fix, config change |
| `size/S` | Small | 1-4 hours | Simple bug fix, minor feature |
| `size/M` | Medium | 1-2 days | Standard feature, moderate bug |
| `size/L` | Large | 3-5 days | Complex feature, significant refactor |
| `size/XL` | Extra Large | 1+ week | Major feature, architecture change |

**Size Estimation Guidelines:**

1. **Include**: Development, testing, code review, documentation
2. **Exclude**: Waiting time, meetings, deployment
3. **When uncertain**: Choose the larger size
4. **Re-estimate**: Update if scope changes during work

```markdown
<!-- Size estimation examples -->
size/XS  → Fix typo in error message
size/S   → Add input validation to form
size/M   → Implement password reset flow
size/L   → Add OAuth2 integration
size/XL  → Migrate from REST to GraphQL
```

## Issue Splitting Rules

**MANDATORY**: Issues estimated to exceed **2-3 days** of work MUST be split into smaller, manageable issues.

### Why Split Large Issues?

1. **Better tracking**: Smaller issues provide clearer progress visibility
2. **Easier review**: Smaller PRs are easier to review and less error-prone
3. **Reduced risk**: Large issues have higher risk of scope creep and delays
4. **Parallel work**: Split issues can be worked on by multiple team members
5. **Incremental value**: Deliver value sooner with smaller, deployable units

### When to Split

| Estimated Duration | Action Required |
|--------------------|-----------------|
| ≤ 2 days (`size/XS`, `size/S`, `size/M`) | No split needed |
| 3-5 days (`size/L`) | **Consider splitting** - evaluate if natural boundaries exist |
| 1+ week (`size/XL`) | **Must split** - break down into smaller tasks immediately |

### How to Split Issues

#### Step 1: Identify Natural Boundaries

Look for these splitting points:

- **By layer**: Frontend / Backend / Database
- **By functionality**: CRUD operations (Create, Read, Update, Delete)
- **By component**: Individual UI components or services
- **By phase**: Setup → Implementation → Testing → Documentation
- **By dependency**: Independent features vs. dependent features

#### Step 2: Apply the INVEST Criteria

Each split issue should be:

| Criteria | Description |
|----------|-------------|
| **I**ndependent | Minimal dependencies on other issues |
| **N**egotiable | Flexible in implementation details |
| **V**aluable | Delivers some value when completed |
| **E**stimable | Can be reasonably estimated |
| **S**mall | Fits within 2 days of work |
| **T**estable | Has clear acceptance criteria |

#### Step 3: Create Parent-Child Structure

```markdown
## Parent Issue (Epic/Story)
- Title: [Feature]: User Authentication System
- Labels: `hierarchy/epic`, `size/XL`
- Description: Overview of the complete feature

### Child Issues (Tasks)
1. [Task]: Set up authentication database schema (#201)
   - size/S, 1-2 days
2. [Task]: Implement JWT token generation (#202)
   - size/M, 1-2 days
3. [Task]: Create login/logout API endpoints (#203)
   - size/M, 1-2 days
4. [Task]: Add authentication middleware (#204)
   - size/S, 1 day
5. [Task]: Write integration tests for auth flow (#205)
   - size/M, 1-2 days
```

### Splitting Patterns by Issue Type

#### Feature Development

```markdown
Original: "Implement user dashboard" (size/XL, ~2 weeks)

Split into:
1. Create dashboard layout component (size/S)
2. Implement user stats widget (size/M)
3. Implement recent activity widget (size/M)
4. Implement notifications widget (size/M)
5. Add dashboard API endpoints (size/M)
6. Write E2E tests for dashboard (size/S)
```

#### Bug Fix (Complex)

```markdown
Original: "Fix data synchronization issues" (size/L, ~4 days)

Split into:
1. Investigate and document sync failure scenarios (size/S)
2. Fix race condition in data fetching (size/M)
3. Add retry logic for failed syncs (size/S)
4. Add monitoring for sync failures (size/S)
```

#### Refactoring

```markdown
Original: "Refactor authentication module" (size/XL, ~1 week)

Split into:
1. Extract auth service from monolith (size/M)
2. Add unit tests for extracted service (size/M)
3. Migrate existing code to use new service (size/M)
4. Remove deprecated auth code (size/S)
5. Update documentation (size/S)
```

### Issue Splitting Checklist

Before creating a large issue, verify:

- [ ] **Estimated duration**: Is it > 2-3 days?
- [ ] **Splittable**: Can it be broken into independent units?
- [ ] **Dependencies mapped**: Are inter-issue dependencies clear?
- [ ] **Parent created**: Is there an Epic/Story to track the whole feature?
- [ ] **Each child valid**: Does each child meet INVEST criteria?
- [ ] **Total coverage**: Do all children together complete the parent?

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Arbitrary splitting | "Part 1", "Part 2" without logic | Split by functionality or layer |
| Over-splitting | 20 tiny issues for a simple feature | Keep reasonable granularity (3-7 issues) |
| Missing parent | Child issues without tracking Epic | Always create parent for visibility |
| Circular dependencies | Issues that block each other | Reorder or restructure splits |
| Incomplete splits | Some work not captured in any child | Audit split completeness |

### Label Naming Convention

| Rule | Example | Rationale |
|------|---------|-----------|
| Use `/` as separator | `type/bug`, `area/api` | Clear categorization |
| Lowercase only | `priority/high` not `Priority/High` | Consistency |
| Singular nouns | `type/bug` not `type/bugs` | Simplicity |
| No spaces | `area/user-management` | URL-safe |

## Issue Hierarchy

Structure issues in a hierarchy for complex projects:

```
Epic (Large initiative, multiple sprints)
├── Story (User-facing feature, fits in one sprint)
│   ├── Task (Technical work item, 1-3 days)
│   │   └── Subtask (Checkbox items within a task)
│   └── Task
└── Story
    └── Task
```

### Hierarchy Definitions

| Level | Scope | Duration | Example |
|-------|-------|----------|---------|
| **Epic** | Major initiative or theme | Multiple sprints | "User Authentication System" |
| **Story** | User-facing functionality | 1 sprint or less | "As a user, I can reset my password" |
| **Task** | Technical implementation | 1-3 days | "Implement password reset API endpoint" |
| **Subtask** | Granular checklist item | < 1 day | "Add email validation" |

### Hierarchy Labels

| Label | Description |
|-------|-------------|
| `hierarchy/epic` | Top-level initiative |
| `hierarchy/story` | User story |
| `hierarchy/task` | Technical task |

## Issue Linking

Use consistent syntax to connect related issues:

### Linking Keywords

| Keyword | Purpose | Example |
|---------|---------|---------|
| `Parent:` | Link to parent Epic/Story | `Parent: #100` |
| `Child:` | Link to child issues | `Child: #101, #102` |
| `Blocks:` | This issue blocks others | `Blocks: #103` |
| `Blocked by:` | This issue is blocked | `Blocked by: #99` |
| `Related:` | Related but not dependent | `Related: #105, #106` |
| `Duplicate of:` | Mark as duplicate | `Duplicate of: #50` |

### Auto-Close Keywords (in PRs)

These keywords in PR descriptions automatically close issues when merged:

| Keyword | Usage |
|---------|-------|
| `Closes #123` | Closes issue #123 |
| `Fixes #123` | Fixes issue #123 |
| `Resolves #123` | Resolves issue #123 |

```markdown
## Example Issue with Links

Parent: #100 (Epic: User Authentication)
Blocked by: #110 (Database migration)
Related: #115 (Login UI design)

## What
Implement JWT token refresh endpoint...
```

## GitHub Issue Templates

Create templates in `.github/ISSUE_TEMPLATE/` for consistent issue creation.

### Directory Structure

```
.github/
└── ISSUE_TEMPLATE/
    ├── bug_report.yml
    ├── feature_request.yml
    ├── task.yml
    └── config.yml
```

### Bug Report Template (bug_report.yml)

```yaml
name: Bug Report
description: Report a bug or unexpected behavior
title: "[Bug]: "
labels: ["type/bug", "status/needs-triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill out the sections below.

  - type: textarea
    id: what
    attributes:
      label: What happened?
      description: Clear description of the bug
      placeholder: Describe the bug...
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: What should have happened?
    validations:
      required: true

  - type: textarea
    id: reproduce
    attributes:
      label: Steps to reproduce
      description: How can we reproduce this issue?
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium
        - High
        - Critical
    validations:
      required: true

  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, browser, version, etc.
      placeholder: |
        - OS: macOS 14.0
        - Browser: Chrome 120
        - Version: v2.1.0

  - type: textarea
    id: context
    attributes:
      label: Additional context
      description: Screenshots, logs, related issues
```

### Feature Request Template (feature_request.yml)

```yaml
name: Feature Request
description: Suggest a new feature or enhancement
title: "[Feature]: "
labels: ["type/feature", "status/needs-triage"]
body:
  - type: textarea
    id: what
    attributes:
      label: What feature do you want?
      description: Clear description of the feature
    validations:
      required: true

  - type: textarea
    id: why
    attributes:
      label: Why do you need this?
      description: Problem this solves or value it provides
    validations:
      required: true

  - type: textarea
    id: how
    attributes:
      label: Proposed solution
      description: How should this work? (optional)

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered
      description: Other solutions you've considered

  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options:
        - Low
        - Medium
        - High
    validations:
      required: true

  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance criteria
      description: How will we know this is complete?
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
```

### Task Template (task.yml)

```yaml
name: Task
description: Create a technical task
title: "[Task]: "
labels: ["type/task"]
body:
  - type: textarea
    id: what
    attributes:
      label: What needs to be done?
      description: Clear description of the task
    validations:
      required: true

  - type: textarea
    id: approach
    attributes:
      label: Technical approach
      description: How will this be implemented?

  - type: textarea
    id: acceptance
    attributes:
      label: Acceptance criteria
      placeholder: |
        - [ ] Criterion 1
        - [ ] Criterion 2
    validations:
      required: true

  - type: dropdown
    id: size
    attributes:
      label: Size estimate
      options:
        - XS (< 1 hour)
        - S (1-4 hours)
        - M (1-2 days)
        - L (3-5 days)
        - XL (1+ week)

  - type: input
    id: parent
    attributes:
      label: Parent issue
      description: Link to parent Epic or Story
      placeholder: "#123"
```

### Config Template (config.yml)

```yaml
blank_issues_enabled: false
contact_links:
  - name: Documentation
    url: https://docs.example.com
    about: Check the documentation before opening an issue
  - name: Discussions
    url: https://github.com/org/repo/discussions
    about: For questions and general discussion
```

## Issue-PR Bidirectional Linking

### Updating Issues with PR Information

**MANDATORY**: When a PR is created for an issue, update the issue with PR information.

#### Why Update Issues?

1. **Traceability**: Easy to find the solution from the problem description
2. **Status visibility**: Stakeholders can track progress without navigating to PRs
3. **Review coordination**: Reviewers can access related context quickly
4. **Historical record**: Complete documentation of how issues were resolved

#### How to Update Issues

When creating a PR that addresses an issue, add a comment to the issue:

```markdown
## Implementation PR

PR #[number] has been created to address this issue.

**PR**: #245
**Status**: In Review
**Branch**: `feature/auth-jwt-implementation`

### Summary of Changes
- Implemented JWT token generation
- Added authentication middleware
- Created login/logout endpoints

### Expected Timeline
- Review: 2024-12-10
- Merge: 2024-12-11 (pending approval)
```

#### Automated Updates

GitHub automatically links PRs to issues when using keywords in PR descriptions:

| PR Description | Effect on Issue |
|---------------|-----------------|
| `Closes #123` | Issue closed when PR is merged |
| `Fixes #123` | Issue closed when PR is merged |
| `Resolves #123` | Issue closed when PR is merged |
| `Relates to #123` | Link created, issue stays open |

**Best Practice**: Use `Closes` keywords in PR AND manually update the issue with PR details for complete visibility.

#### Issue Update Template

Add this comment when a PR is created:

```markdown
## 📋 Implementation Update

| Field | Value |
|-------|-------|
| **PR** | #[PR_NUMBER] |
| **Branch** | `[BRANCH_NAME]` |
| **Status** | 🔄 In Progress / 👀 In Review / ✅ Merged |
| **Assignee** | @[USERNAME] |

### Implementation Notes
<!-- Brief notes about the implementation approach -->

### Remaining Work
- [ ] Item 1
- [ ] Item 2
```

#### Multiple PRs for Single Issue

For large issues requiring multiple PRs:

```markdown
## 📋 Implementation Progress

### Related PRs
| PR | Description | Status |
|----|-------------|--------|
| #201 | Database schema changes | ✅ Merged |
| #205 | Backend API implementation | 👀 In Review |
| #210 | Frontend integration | 🔄 In Progress |

### Overall Progress: 66% (2/3 PRs merged)
```

---
*Part of the workflow guidelines module*

---
name: branch-manager
version: 1.0.0
description: Intelligent git branch management with naming conventions, cleanup suggestions, and workflow optimization
triggers:
  - 'manage my branches'
  - 'branch management'
  - 'create feature branch'
  - 'cleanup branches'
  - 'branch status'
  - 'check branch naming'
  - 'branch visualization'
  - 'merge strategy'
  - 'new branch for'
examples:
  - 'Create a new feature branch for user authentication'
  - 'Check my branch naming conventions'
  - 'Show me branches that can be cleaned up'
  - 'Generate a branch relationship diagram'
  - 'What merge strategy should I use?'
---

This skill provides comprehensive git branch management with intelligent naming conventions, automated cleanup suggestions, and workflow optimization. It follows established branching patterns and helps maintain clean, organized repositories.

## Core Features

### 1. Intelligent Branch Creation

Creates properly named branches based on your task description with automatic issue ID detection and naming validation.

### 2. Naming Convention Enforcement

Validates and enforces consistent branch naming across your repository with configurable patterns.

### 3. Automated Cleanup Detection

Identifies merged, stale, and orphaned branches with cleanup recommendations and automated scripts.

### 4. Branch Relationship Visualization

Generates ASCII diagrams showing branch relationships, merge status, and development flow.

### 5. Merge Strategy Recommendations

Analyzes branch relationships and suggests optimal merge strategies (merge, rebase, squash).

## Branch Naming Conventions

### Supported Patterns

| Type         | Pattern                               | With Issue ID                    | Without Issue ID               |
| ------------ | ------------------------------------- | -------------------------------- | ------------------------------ |
| **Feature**  | `feature/[<issue-id>-]<description>`  | `feature/PROJ-123-user-auth`     | `feature/user-auth`            |
| **Bugfix**   | `bugfix/[<issue-id>-]<description>`   | `bugfix/PROJ-456-fix-header`     | `bugfix/fix-header`            |
| **Refactor** | `refactor/[<issue-id>-]<description>` | `refactor/PROJ-789-cleanup-code` | `refactor/cleanup-code`        |
| **Hotfix**   | `hotfix/<version>-<description>`      | `hotfix/v1.2.3-security-patch`   | `hotfix/v1.2.3-security-patch` |
| **Release**  | `release/<version>`                   | `release/v2.0.0`                 | `release/v2.0.0`               |
| **Epic**     | `epic/[<epic-id>-]<description>`      | `epic/EPIC-789-new-dashboard`    | `epic/new-dashboard`           |

### Issue ID Detection

Automatically detects and extracts issue IDs from:

- Commit messages
- Pull request descriptions
- Branch descriptions
- Current task context

## Usage Examples

### Create New Feature Branch

```
"Create a new feature branch for implementing user authentication with OAuth"

Analysis Process:
1. Detects task type: feature (authentication)
2. Searches for related issues: PROJ-123 (user auth)
3. Validates naming: feature/PROJ-123-user-auth
4. Creates branch and switches to it
5. Shows branch status and next steps

Output:
✅ Created and switched to branch: feature/PROJ-123-user-auth
📋 Branch follows naming conventions
🔄 Ready to start implementing user authentication
```

### Branch Health Check

```
"Check the health of my branches and suggest cleanup"

Analysis Process:
1. Scans all local branches
2. Checks naming convention compliance
3. Identifies merged/stale branches
4. Analyzes branch age and activity
5. Generates cleanup recommendations

Output:
## Branch Health Report

### ✅ Well-formed Branches (8)
- feature/PROJ-123-user-auth (2 days old, active)
- bugfix/PROJ-456-fix-header (1 day old, active)
- main (updated today)

### ⚠️ Cleanup Candidates (5)
- feature/old-feature (merged 45 days ago)
- bugfix/completed-fix (merged 30 days ago)
- experiment/test-branch (stale 60 days)

### 🏷️ Naming Issues (2)
- fix-bug (missing type prefix)
- Feature-NewUI (wrong case)

**Recommendation**: Run cleanup to remove 5 merged branches
```

### Branch Visualization

```
"Show me the branch relationships in my repository"

Analysis Process:
1. Analyzes git log and branch structure
2. Maps parent-child relationships
3. Identifies merge points and conflicts
4. Generates ASCII relationship diagram

Output:
## Branch Relationship Diagram

main (v2.1.0)
├── release/v2.0.0 [merged]
├── feature/PROJ-123-user-auth [active]
│   ├── bugfix/PROJ-456-fix-header [merged → main]
│   └── hotfix/v2.0.3-security [merged → main]
└── epic/EPIC-789-dashboard [active]
    ├── feature/PROJ-200-api-endpoints [merged → epic/EPIC-789-dashboard]
    └── feature/PROJ-201-ui-components [active]

Legend: [merged] = safe to delete, [active] = in development
```

### Merge Strategy Advice

````
"I'm ready to merge my feature branch, what strategy should I use?"

Analysis Process:
1. Analyzes branch history and changes
2. Checks for conflicts with target branch
3. Considers team workflow preferences
4. Evaluates change complexity

Output:
## Merge Strategy Recommendation

**Branch**: feature/PROJ-123-user-auth → main
**Changes**: 12 commits, 8 files modified
**Conflicts**: None detected

### Recommended: 🔄 Rebase and Merge
**Why**: Clean history, single commit on main
**Commands**:
```bash
git checkout feature/PROJ-123-user-auth
git rebase main
git checkout main
git merge feature/PROJ-123-user-auth
````

**Alternative**: 📋 Squash Merge (if team prefers single commits)
**Avoid**: 🔀 Regular Merge (would create merge commit)

````

## Configuration

Customize branch management behavior via `.claude/branch-manager.md`:

```yaml
---
# Branch naming patterns (regex supported)
patterns:
  feature: "^feature/([A-Z]+-[0-9]+-)?[^/]+$"  # Optional issue ID
  bugfix: "^bugfix/([A-Z]+-[0-9]+-)?[^/]+$"   # Optional issue ID
  refactor: "^refactor/([A-Z]+-[0-9]+-)?[^/]+$" # Optional issue ID
  hotfix: "^hotfix/[^/]+-.+$"
  release: "^release/[^/]+$"
  epic: "^epic/([A-Z]+-[0-9]+-)?[^/]+$"       # Optional issue ID

# Cleanup policies
cleanup:
  merged_branches_older_than_days: 30
  stale_branches_older_than_days: 90
  keep_branches_with_open_prs: true
  protected_branches: ["main", "master", "develop", "staging"]

# Issue tracking integration
issue_tracking:
  enabled: true
  patterns:
    - "PROJ-[0-9]+"
    - "ISSUE-[0-9]+"
    - "#[0-9]+"
  auto_detect_from_commits: true
  require_issue_id: false  # Allow branches without issue IDs
  allow_no_id_branches: true  # Enable creation of branches without issue IDs

# Visualization settings
visualization:
  max_depth: 10
  show_merge_commits: true
  include_remote_branches: false

# Default merge strategies by branch type
merge_strategies:
  feature: "rebase_merge"  # rebase then merge
  bugfix: "squash_merge"   # squash into single commit
  refactor: "regular_merge" # keep full history for review
  hotfix: "regular_merge"  # keep full history
  release: "regular_merge" # preserve release commits
---
````

## Advanced Features

### Issue ID Auto-Detection

Automatically extracts issue references from:

- Current task description
- Recent commit messages
- Open pull requests
- Branch context

### Smart Branch Classification

Intelligently categorizes branches based on:

- Commit message patterns
- File modification types
- Development velocity
- Team conventions

### Conflict Prediction

Analyzes potential merge conflicts before they occur by:

- Examining file overlap
- Checking for related changes
- Historical conflict patterns

## Integration Examples

### Pre-commit Branch Validation

```bash
# .git/hooks/pre-commit
branch=$(git branch --show-current)
if ! claude "validate branch name: $branch"; then
    echo "Branch name doesn't follow conventions"
    exit 1
fi
```

### CI/CD Branch Checks

```yaml
# .github/workflows/branch-check.yml
- name: Validate Branch
  run: |
    if ! claude "check branch naming for CI"; then
      echo "Branch naming violation"
      exit 1
    fi
```

### IDE Integration

```json
// .vscode/tasks.json
{
  "label": "Create Feature Branch",
  "command": "claude",
  "args": ["create feature branch for ${input:taskDescription}"],
  "type": "shell"
}
```

## Performance & Scalability

- **Speed**: Analysis completes in 5-15 seconds for typical repositories
- **Scalability**: Handles repositories with 100+ branches efficiently
- **Memory**: Minimal memory footprint using streaming git operations
- **Compatibility**: Works with Git 2.0+ and standard hosting platforms

## Troubleshooting

### Branch Creation Fails

```
Issue: "Cannot create branch with that name"
Solution:
- Check if branch already exists
- Verify naming pattern compliance
- Ensure issue ID is valid
- Check repository permissions
```

### Cleanup Detection Inaccurate

```
Issue: "Cleanup suggests removing active branches"
Solution:
- Update cleanup configuration
- Check branch age calculation
- Verify merge status detection
- Review protected branch settings
```

### Visualization Too Complex

```
Issue: "Branch diagram is overwhelming"
Solution:
- Reduce max_depth in configuration
- Filter by branch type or age
- Use --simple flag for basic view
- Focus on specific branch subtrees
```

## Best Practices

### Naming Conventions

- Use descriptive, hyphen-separated names
- Include issue IDs when available
- Keep names under 50 characters
- Use lowercase for consistency

### Branch Lifecycle

- Create branches from latest main
- Regular rebasing to avoid conflicts
- Delete merged branches promptly
- Use consistent merge strategies

### Repository Hygiene

- Run weekly cleanup checks
- Archive important branches before deletion
- Document branching strategy
- Train team on conventions

## Technical Architecture

### Agent-Based Analysis

Uses specialized agents for different aspects:

- **Naming Validator**: Regex pattern matching and format validation
- **Branch Analyzer**: Git history analysis and relationship mapping
- **Cleanup Advisor**: Age and merge status evaluation
- **Strategy Planner**: Conflict analysis and merge optimization

### Git Operations

- Streaming git commands for memory efficiency
- Error handling for various git states
- Support for worktrees and submodules
- Remote branch synchronization

### Data Structures

```typescript
interface BranchInfo {
  name: string
  type: BranchType
  age: number
  isMerged: boolean
  hasConflicts: boolean
  lastCommit: Date
  author: string
  relatedIssues: string[]
}

interface BranchRelationship {
  parent: string
  children: string[]
  mergeCommits: string[]
  conflicts: ConflictInfo[]
}
```

This comprehensive branch management system ensures clean, organized, and efficient git workflows while maintaining flexibility for different team preferences and project requirements.

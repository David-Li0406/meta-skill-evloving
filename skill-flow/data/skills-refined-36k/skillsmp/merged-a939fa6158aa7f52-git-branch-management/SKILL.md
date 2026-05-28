---
name: git-branch-management
description: Use this skill for comprehensive management of Git branches, including naming conventions, cleanup suggestions, and workflow optimization.
---

# Body of the merged SKILL.md

This skill provides intelligent Git branch management with features for naming conventions, automated cleanup suggestions, and workflow optimization. It follows established branching patterns to help maintain clean, organized repositories.

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
Automatically detects and extracts issue IDs from commit messages, pull request descriptions, branch descriptions, and current task context.

## Usage Examples

### Create New Feature Branch
```
"Create a new feature branch for implementing user authentication with OAuth"
```
**Output:**
✅ Created and switched to branch: `feature/PROJ-123-user-auth`  
📋 Branch follows naming conventions  
🔄 Ready to start implementing user authentication  

### Branch Health Check
```
"Check the health of my branches and suggest cleanup"
```
**Output:**
## Branch Health Report
### ✅ Well-formed Branches (8)
- `feature/PROJ-123-user-auth (2 days old, active)`
- `bugfix/PROJ-456-fix-header (1 day old, active)`
- `main (updated today)`

### ⚠️ Cleanup Candidates (5)
- `feature/old-feature (merged 45 days ago)`
- `bugfix/completed-fix (merged 30 days ago)`

### 🏷️ Naming Issues (2)
- `fix-bug (missing type prefix)`
- `Feature-NewUI (wrong case)`

**Recommendation**: Run cleanup to remove 5 merged branches

### Branch Visualization
```
"Show me the branch relationships in my repository"
```
**Output:**
## Branch Relationship Diagram
```
main (v2.1.0)
├── release/v2.0.0 [merged]
├── feature/PROJ-123-user-auth [active]
└── epic/EPIC-789-dashboard [active]
```

### Merge Strategy Advice
```
"I'm ready to merge my feature branch, what strategy should I use?"
```
**Output:**
## Merge Strategy Recommendation
**Branch**: `feature/PROJ-123-user-auth → main`  
**Recommended**: 🔄 Rebase and Merge  

## Configuration
Customize branch management behavior via configuration settings for naming patterns, cleanup policies, issue tracking integration, and visualization settings.

## Advanced Features
- **Issue ID Auto-Detection**: Automatically extracts issue references from task descriptions and recent commit messages.
- **Smart Branch Classification**: Categorizes branches based on commit message patterns and development velocity.
- **Conflict Prediction**: Analyzes potential merge conflicts before they occur.

## Best Practices
- Use descriptive, hyphen-separated names.
- Create branches from the latest main.
- Regularly run cleanup checks.

This comprehensive branch management system ensures clean, organized, and efficient Git workflows while maintaining flexibility for different team preferences and project requirements.
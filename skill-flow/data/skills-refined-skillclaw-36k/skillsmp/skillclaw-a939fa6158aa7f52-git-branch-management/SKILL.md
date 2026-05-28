---
name: git-branch-management
description: Use this skill when you need to manage Git branches effectively, ensuring proper naming conventions and workflows.
---

# Skill body

## Overview

This skill provides comprehensive Git branch management, including intelligent naming conventions, automated cleanup suggestions, and workflow optimization. It helps maintain clean, organized repositories by following established branching patterns.

## Core Features

### 1. Intelligent Branch Creation
- Creates properly named branches based on your task description with automatic issue ID detection and naming validation.

### 2. Naming Convention Enforcement
- Validates and enforces consistent branch naming across your repository with configurable patterns.

### 3. Automated Cleanup Detection
- Identifies merged, stale, and orphaned branches with cleanup recommendations and automated scripts.

### 4. Branch Relationship Visualization
- Generates ASCII diagrams showing branch relationships, merge status, and development flow.

### 5. Merge Strategy Recommendations
- Analyzes branch relationships and suggests optimal merge strategies (merge, rebase, squash).

## Branch Naming Conventions

### Supported Patterns

| Type         | Pattern                               | With Issue ID                    | Without Issue ID               |
| ------------ | ------------------------------------- | -------------------------------- | ------------------------------ |
| **Feature**  | `feature/[<issue-id>-]<description>`  | `feature/PROJ-123-user-auth`     | `feature/user-auth`            |
| **Bugfix**   | `bugfix/[<issue-id>-]<description>`   | `bugfix/PROJ-456-fix-header`     | `bugfix/fix-header`            |
| **Refactor** | `refactor/[<issue-id>-]<description>` | `refactor/PROJ-789-cleanup-code` | `refactor/cleanup-code`        |
| **Hotfix**   | `hotfix/<version>-<description>`      | `hotfix/v1.2.3-security-patch`   | `hotfix/v1.2.3-security-patch` |
| **Release**  | `release/<version>`                   | `release/v2.0.0`                 | `release/v2.0.0`               |

## Usage Examples
- Create a new feature branch for user authentication.
- Check my branch naming conventions.
- Show me branches that can be cleaned up.
- Generate a branch relationship diagram.
- What merge strategy should I use?
<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# CODEOWNERS File Best Practices

## Overview

CODEOWNERS files automate code review assignment and enforce ownership policies in Git platforms (GitHub, GitLab, Bitbucket). This document provides comprehensive best practices for creating and maintaining effective CODEOWNERS files.

## Core Syntax

### Basic Structure

```
# Comments start with #
# Last matching pattern takes precedence

# Pattern    Owner(s)
* @default-team
/docs/ @documentation-team
*.js @javascript-experts
```

### Common Patterns

**Wildcard Matching**:
```
# All files (default fallback)
* @core-team

# All files in directory (non-recursive)
/src/* @dev-team

# All files recursively
/src/** @dev-team
```

**File Type Matching**:
```
*.js @javascript-team
*.py @python-team
*.go @golang-team
*.sql @database-team
```

**Specific Files**:
```
/README.md @docs-team @engineering-leads
/package.json @dependencies-team
/Dockerfile @devops-team
```

**Multiple Owners**:
```
# All must approve in GitHub (with branch protection)
/security/** @security-lead @engineering-lead

# Team + individual
/api/** @api-team @api-lead
```

## Strategic Implementation Models

### 1. Basic Single Owner

Simple ownership for small repositories:

```
* @repository-owner
```

**When to Use**:
- Small repositories
- Personal projects
- Prototypes
- Single-person maintenance

**Limitations**:
- Creates single point of failure
- No redundancy
- Review bottleneck

### 2. Department-Based Structure

Different teams own different code sections:

```
* @engineering

# Frontend
/frontend/** @frontend-team
/public/** @frontend-team

# Backend
/backend/** @backend-team
/api/** @backend-team

# Infrastructure
/infrastructure/** @devops-team
*.yml @devops-team
Dockerfile* @devops-team

# Documentation
*.md @tech-writers
/docs/** @tech-writers
```

**Benefits**:
- Clear team boundaries
- Streamlined review mechanism
- Automatic reviewer identification
- Scalable structure

**Best For**:
- Medium to large organizations
- Cross-functional teams
- Service-oriented architectures

### 3. Multilevel Ownership

Combines broad responsibility with specialized expertise:

```
# Default: entire core team
* @core-team

# Specific expertise required
/auth/** @security-team @backend-team
/payments/** @payments-team @security-team @compliance

# Language-specific
*.py @python-experts @core-team
*.rs @rust-experts @core-team

# Critical paths
/migrations/** @database-team @backend-lead
```

**Benefits**:
- Multiple layers of review
- Specialist input where needed
- Maintains team awareness
- Flexible responsibility

**Best For**:
- Complex systems
- Regulated environments
- High-risk code areas

### 4. Component-Based

Organized by architectural components:

```
# Services
/services/auth/** @auth-squad
/services/billing/** @billing-squad @finance-reviewer
/services/notifications/** @platform-squad

# Shared libraries
/lib/common/** @platform-squad
/lib/security/** @security-team

# Client applications
/apps/web/** @web-team
/apps/mobile/** @mobile-team
```

**Benefits**:
- Aligns with architecture
- Squad autonomy
- Clear boundaries
- Microservices-friendly

**Best For**:
- Microservices architectures
- Squad-based organizations
- Large codebases

## Critical Mistakes to Avoid

### 1. Empty CODEOWNERS Files

**Problem**:
```
# CODEOWNERS
# (empty - no owners assigned)
```

Creates file without assigning users, defeating the purpose.

**Solution**: Always define at least a default owner:
```
* @default-team
```

### 2. Paths Without Owners

**Problem**:
```
/src/*
/docs/*
# No @ mentions - no owners assigned!
```

**Solution**: Every pattern must have owners:
```
/src/* @dev-team
/docs/* @docs-team
```

### 3. Teams With No Members

**Problem**: Assigning ownership to empty teams blocks PRs.

```
/feature/** @nonexistent-team
```

**Solution**:
- Verify team exists before assignment
- Use individuals as backup
- Automated validation in CI/CD

### 4. Insufficient Permissions

**Problem**: Users without write access cannot be code owners.

**Platform Requirements**:
- **GitHub**: Write access or higher
- **GitLab**: Maintainer role minimum
- **Bitbucket**: Write permission

**Solution**:
- Verify permissions before adding owners
- Use teams with appropriate access
- Document permission requirements

### 5. Overly Broad Patterns

**Problem**:
```
* @single-person
# One person reviews EVERYTHING
```

**Solution**: Be specific, distribute load:
```
* @core-team
/critical/** @senior-devs
/docs/** @writers
```

### 6. Overly Specific Patterns

**Problem**:
```
/src/component1.ts @alice
/src/component2.ts @alice
/src/component3.ts @alice
/src/component4.ts @alice
```

**Solution**: Use patterns:
```
/src/component*.ts @alice
```

### 7. Stale Ownership

**Problem**: Listed owners no longer active:
```
/legacy/** @former-employee  # Left 6 months ago
```

**Solution**:
- Regular audits (quarterly minimum)
- Automated staleness checks
- Update on team changes

### 8. No Default Owner

**Problem**: Missing fallback pattern means new files have no owner.

**Solution**: Always include default:
```
# At top of file
* @default-team

# More specific patterns follow...
/api/** @api-team
```

### 9. Pattern Order Confusion

**Problem**: Not understanding last-match-wins rule:
```
/api/** @api-team
* @everyone
# Everyone reviews API changes (probably not intended!)
```

**Solution**: Put broad patterns first, specific last:
```
* @core-team           # Default
/api/** @api-team      # Override for API
```

### 10. Ignoring Exclusions

**Problem**: Cannot exclude paths in GitHub CODEOWNERS (limited support).

**Workaround**:
```
# Want: /src/** except /src/generated/
# Solution: Be specific about what to include
/src/app/** @dev-team
/src/lib/** @dev-team
# /src/generated/ not mentioned, no owner required
```

## Platform-Specific Syntax

### GitHub

**Location**: `.github/CODEOWNERS`, `docs/CODEOWNERS`, or `CODEOWNERS` (root)

**Features**:
```
# Basic syntax
/path/ @username @org/team

# No sections or advanced features
# Last match wins
```

### GitLab

**Location**: `.gitlab/CODEOWNERS`, `docs/CODEOWNERS`, or `CODEOWNERS` (root)

**Features**:
```
# Sections for clarity
[Backend]
*.rb @backend-team
/app/models/** @backend-team

[Frontend]
*.vue @frontend-team

# Required approvals
[Security]^2
/security/** @security-team
# ^2 means 2 approvals required
```

### Bitbucket

**Location**: `CODEOWNERS` or `reviewers.txt` (root)

**Features**:
```
# Similar to .gitignore syntax
**/*.java @java-team
**/tests/** @qa-team
```

## Best Practices

### 1. Start Simple, Evolve

```
# Phase 1: Basic
* @core-team

# Phase 2: Major divisions
/frontend/** @frontend-team
/backend/** @backend-team

# Phase 3: Refined
/frontend/dashboard/** @dashboard-squad
/backend/api/payments/** @payments-team @security-team
```

### 2. Document Intent

```
# Payment processing - requires security review
/services/payments/** @payments-team @security-lead

# Auto-generated - no review needed (no owner)
# /generated/** (intentionally excluded)

# Critical infrastructure - requires approval from both
/kubernetes/** @devops-lead @platform-lead
```

### 3. Balance Granularity

**Too Granular**:
```
/src/auth/login.ts @alice
/src/auth/logout.ts @alice
/src/auth/signup.ts @alice
```

**Too Broad**:
```
/src/** @everyone
```

**Just Right**:
```
/src/auth/** @auth-team
/src/auth/oauth/** @oauth-specialist @auth-team
```

### 4. Use Teams Over Individuals

**Avoid**:
```
/api/** @alice  # Single point of failure
```

**Prefer**:
```
/api/** @api-team  # Distributes load, provides backup
```

**Best**:
```
/api/** @api-team @api-lead  # Team + experienced lead
```

### 5. Primary + Backup Pattern

```
# Critical code always has backup
/security/** @security-lead @security-team
/payments/** @payments-lead @payments-team @compliance
/infrastructure/** @devops-lead @devops-team
```

### 6. Align With Architecture

```
# Microservices structure
/services/user-service/** @user-squad
/services/order-service/** @order-squad
/services/notification-service/** @platform-squad

# Libraries
/libs/common/** @platform-squad
/libs/security/** @security-team
```

### 7. Layer-Based Ownership

```
# Data layer
**/models/** @backend-team
**/migrations/** @database-team

# API layer
**/controllers/** @api-team
**/routes/** @api-team

# View layer
**/views/** @frontend-team
**/components/** @frontend-team

# Tests
**/tests/** @qa-team @owning-team
```

## Testing and Validation

### Automated Validation

```yaml
# GitHub Actions
name: Validate CODEOWNERS
on: [pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate CODEOWNERS
        run: |
          # Check syntax
          # Verify teams/users exist
          # Check for stale owners
          # Validate coverage
```

### Manual Review Checklist

- [ ] All patterns have assigned owners
- [ ] No empty teams or non-existent users
- [ ] All owners have appropriate permissions
- [ ] Patterns ordered correctly (broad -> specific)
- [ ] Critical paths have backup owners
- [ ] Documentation explains non-obvious choices
- [ ] Quarterly review date scheduled

## Maintenance Schedule

**Weekly**:
- Monitor for new files without owners
- Check review bottlenecks

**Monthly**:
- Validate owner activity (are they still reviewing?)
- Check review turnaround times

**Quarterly**:
- Full CODEOWNERS audit
- Update for team changes
- Refine patterns based on actual contributions
- Remove stale owners

**Annually**:
- Comprehensive review of ownership strategy
- Align with organizational changes
- Major restructuring if needed

## Integration Benefits

Properly implemented CODEOWNERS provides:

1. **Enhanced Security**: Mandatory designated reviews for sensitive code
2. **Accelerated Review Cycles**: Right reviewers automatically assigned
3. **Increased Accountability**: Clear ownership and responsibility
4. **Better Code Quality**: Domain experts review relevant changes
5. **Knowledge Distribution**: Backup owners learn through reviews
6. **Onboarding Aid**: New team members see who owns what
7. **Compliance**: Audit trail of required approvals
8. **Automation**: CI/CD integration for ownership enforcement

## References

- "A Modern Guide to CODEOWNERS" (Aviator.co, 2024)
- GitHub CODEOWNERS documentation
- GitLab Code Owners documentation
- Bitbucket default reviewers documentation

# Branch Manager Usage Scenarios

This document demonstrates real-world usage scenarios for the branch-manager skill, showing how it handles different development workflows and edge cases.

## Scenario 1: New Feature Development (With Issue ID)

### User Request

```
"Create a new feature branch for implementing user authentication with OAuth integration"
```

### Skill Analysis Process

1. **Task Classification**: Identifies as "feature" type due to "implementing" + "authentication"
2. **Issue Detection**: Scans recent commits for PROJ-123 references
3. **Name Generation**: Creates `feature/PROJ-123-user-auth-oauth`
4. **Validation**: Confirms naming follows conventions
5. **Creation**: Creates branch and sets upstream

### Output Result

```
✅ Created and switched to branch: feature/PROJ-123-user-auth-oauth

## Branch Details
- **Type**: Feature branch
- **Issue**: PROJ-123 (detected from recent commits)
- **Naming**: ✅ Follows conventions
- **Upstream**: Set to origin/feature/PROJ-123-user-auth-oauth

## Next Steps
1. Implement OAuth authentication logic
2. Add unit tests for auth functions
3. Update API documentation
4. Create pull request when ready

## Related Files to Modify
- src/auth/
- src/api/auth-endpoints.ts
- tests/auth/
- docs/api-auth.md
```

## Scenario 1.5: Refactor Codebase

### User Request

```
"Create a refactor branch to restructure the authentication module and improve code organization"
```

### Skill Analysis Process

1. **Task Classification**: Identifies as "refactor" type due to "refactor", "restructure", "improve code organization"
2. **Issue Detection**: Searches for related issues in commit messages
3. **Name Generation**: Creates `refactor/PROJ-321-restructure-auth-module`
4. **Validation**: Confirms naming follows conventions
5. **Creation**: Creates branch with refactor-specific guidance

### Output Result

```
🔄 Created refactor branch: refactor/PROJ-321-restructure-auth-module

## Refactor Details
- **Type**: Refactor branch
- **Issue**: PROJ-321 (detected from recent commits)
- **Scope**: Authentication module restructuring
- **Risk Level**: Medium (structural changes)

## Refactoring Guidelines
- **Preserve Functionality**: Ensure all existing tests pass
- **Incremental Changes**: Break large refactorings into smaller commits
- **Documentation**: Update any affected documentation
- **Team Coordination**: Notify team members of structural changes

## Suggested Refactoring Steps
1. Extract common authentication logic into utility functions
2. Reorganize file structure for better separation of concerns
3. Update import statements across the codebase
4. Add new tests for refactored components

## Files to Focus On
- src/auth/
- src/utils/auth-helpers.ts
- tests/auth/
- docs/api/authentication.md

⚠️ **Refactoring Reminder**: This branch contains structural changes that may affect other parts of the codebase. Coordinate with team members and ensure comprehensive testing.
```

## Scenario 1.6: Feature Development (Without Issue ID)

### User Request

```
"Create a feature branch for adding dark mode support"
```

### Skill Analysis Process

1. **Task Classification**: Identifies as "feature" type due to "adding" + feature description
2. **Issue Detection**: No issue IDs found in recent commits or description
3. **Name Generation**: Creates `feature/dark-mode-support` (no issue ID)
4. **Validation**: Confirms naming follows conventions (optional issue ID)
5. **Creation**: Creates branch with helpful suggestions

### Output Result

```
✅ Created and switched to branch: feature/dark-mode-support

## Branch Details
- **Type**: Feature branch
- **Issue**: 未关联 (将在后续创建Issue后重命名)
- **Naming**: ✅ Follows conventions
- **Upstream**: Set to origin/feature/dark-mode-support

## 💡 Issue关联建议
如果后续需要关联Issue，可以使用:
```

claude "associate this branch with PROJ-456"

```

## Next Steps
1. Implement dark mode toggle functionality
2. Add CSS variables for theme switching
3. Update component styles
4. Test across different devices

## Related Files to Modify
- src/components/ThemeToggle/
- src/styles/themes.css
- src/hooks/useTheme.ts
- src/styles/variables.css
```

## Scenario 2: Bug Fix Creation

### User Request

```
"There's a bug in the header component causing layout issues on mobile. Create a branch to fix it."
```

### Skill Analysis Process

1. **Task Classification**: Identifies as "bugfix" from "bug" + "fix"
2. **Issue Detection**: Searches for related issues in commit messages
3. **Name Generation**: Creates `bugfix/PROJ-456-fix-header-mobile`
4. **Impact Analysis**: Checks which files are likely affected

### Output Result

```
🐛 Created bugfix branch: bugfix/PROJ-456-fix-header-mobile

## Bug Fix Details
- **Type**: Bug fix
- **Issue**: PROJ-456 (referenced in recent commits)
- **Priority**: High (affects user experience)
- **Affected Component**: Header component

## Investigation Checklist
- [ ] Reproduce issue on mobile devices
- [ ] Check responsive CSS in header styles
- [ ] Verify flexbox/grid layout issues
- [ ] Test on different screen sizes

## Files to Examine
- src/components/Header/
- src/styles/header.css
- src/hooks/useViewport.ts
- tests/components/Header.test.tsx
```

## Scenario 3: Branch Health Audit

### User Request

```
"Check the health of all my branches and suggest cleanup"
```

### Skill Analysis Process

1. **Branch Inventory**: Lists all local and remote branches
2. **Age Analysis**: Calculates days since last activity
3. **Merge Status**: Checks if branches are merged to main
4. **Naming Audit**: Validates naming conventions
5. **Relationship Mapping**: Builds dependency graph

### Output Result

````
## Branch Health Report - 2024-01-20

### 📊 Repository Overview
- Total branches: 24 (18 local, 6 remote)
- Active branches: 8
- Stale branches: 12
- Merged branches: 4

### ✅ Healthy Branches (8)
| Branch | Age | Status | Activity |
|--------|-----|--------|----------|
| feature/PROJ-123-user-auth | 2d | Active | 3 commits today |
| bugfix/PROJ-456-header-fix | 1d | Active | 1 commit yesterday |
| main | 0d | Current | Updated today |
| develop | 1d | Active | Merged 2 PRs |

### 🧹 Cleanup Candidates (12)

#### Recently Merged (Safe to Delete)
| Branch | Merged | Age | Action |
|--------|--------|-----|--------|
| feature/PROJ-100-login-form | 2024-01-15 | 35d | `git branch -d feature/PROJ-100-login-form` |
| bugfix/PROJ-200-api-error | 2024-01-10 | 40d | `git branch -d bugfix/PROJ-200-api-error` |
| feature/PROJ-150-search-ui | 2024-01-05 | 45d | `git branch -d feature/PROJ-150-search-ui` |
| release/v1.2.0 | 2024-01-01 | 49d | `git branch -d release/v1.2.0` |

#### Stale Branches (Review Carefully)
| Branch | Last Activity | Age | Risk |
|--------|----------------|-----|------|
| experiment/new-ui-framework | 2023-12-01 | 50d | Medium - has 15 commits |
| feature/old-payment-system | 2023-11-15 | 66d | High - 8 uncommitted files |
| bugfix/deprecated-api | 2023-10-30 | 82d | Low - fully merged |

### 🏷️ Naming Convention Issues (3)
| Branch | Current Name | Suggested Rename |
|--------|--------------|------------------|
| fix-critical-bug | ❌ No prefix | `bugfix/PROJ-XXX-fix-critical-bug` |
| Feature-NewUI | ❌ Wrong case | `feature/PROJ-XXX-new-ui` |
| hotfix_urgent | ❌ Underscore | `hotfix/v1.3.1-urgent-fix` |

### 💡 Recommendations

#### Immediate Actions (Safe)
```bash
# Delete recently merged branches
git branch -d feature/PROJ-100-login-form
git branch -d bugfix/PROJ-200-api-error
git branch -d feature/PROJ-150-search-ui
git branch -d release/v1.2.0
````

#### Review Required

1. **experiment/new-ui-framework**: Check if experiment is still valuable
2. **feature/old-payment-system**: Contains uncommitted work - archive or merge
3. **Stale branches**: Review with team before deletion

#### Process Improvements

1. **Naming Enforcement**: Consider pre-commit hooks for naming validation
2. **Regular Cleanup**: Set up weekly automated cleanup checks
3. **Branch Policies**: Document when branches should be deleted

**Potential Space Savings**: ~120MB from deleted branches
**Compliance Rate**: 87% (21/24 branches follow conventions)

```

## Scenario 4: Branch Relationship Visualization

### User Request
```

"Show me how all the branches in my repository are related"

```

### Skill Analysis Process
1. **Git Log Analysis**: Parses commit history and merge relationships
2. **Branch Topology**: Maps parent-child relationships
3. **Merge Detection**: Identifies merge commits and conflict resolutions
4. **Activity Tracking**: Shows recent commits on each branch

### Output Result
```

## Branch Relationship Tree

main (v2.1.0) [current]
├── release/v2.0.0 [merged 2024-01-01] ──┐
│ │
├── hotfix/v2.0.3-security [merged 2024-01-10] │
│ │
├── feature/PROJ-123-user-auth [active] ──────┼── main
│ ├── bugfix/PROJ-456-header-fix [merged → feature/PROJ-123-user-auth]
│ └── feature/PROJ-123-oauth-integration [active]
│ └── bugfix/PROJ-500-oauth-timeout [active, 2 commits]
│
├── epic/EPIC-789-new-dashboard [active]
│ ├── feature/PROJ-200-api-refactor [merged → epic/EPIC-789-new-dashboard]
│ ├── feature/PROJ-201-ui-redesign [active]
│ │ └── bugfix/PROJ-300-responsive-fix [merged → feature/PROJ-201-ui-redesign]
│ └── feature/PROJ-202-data-visualization [active, 5 commits]
│
└── develop [active, 8 commits behind main]
└── feature/PROJ-150-experimental-feature [stale, 45 days]

## Relationship Summary

### Active Development Lines

- **User Auth Epic**: feature/PROJ-123-\* branches (3 active)
- **Dashboard Redesign**: epic/EPIC-789-\* branches (3 active)
- **Main Development**: develop branch (needs sync)

### Merge Readiness

- **Ready for Main**: bugfix/PROJ-456-header-fix, feature/PROJ-200-api-refactor
- **Needs Testing**: feature/PROJ-201-ui-redesign, feature/PROJ-202-data-visualization
- **Has Conflicts**: develop (8 commits behind)

### Risk Assessment

- **Low Risk**: Isolated bugfix branches
- **Medium Risk**: Feature branches in active epics
- **High Risk**: develop branch (significant divergence)

## Recommended Actions

### Immediate Merges (Low Risk)

1. Merge `bugfix/PROJ-456-header-fix` → `feature/PROJ-123-user-auth`
2. Merge `feature/PROJ-200-api-refactor` → `epic/EPIC-789-new-dashboard`

### Planning Required

1. **Sync develop**: Rebase or merge from main
2. **Test feature branches**: Ensure dashboard features work together
3. **Resolve stale branches**: Archive or delete experimental features

### Branch Strategy Notes

- **Epic branches work well** for organizing related features
- **Develop branch is diverging** - consider sync frequency
- **Good isolation** between different feature sets

```

## Scenario 5: Merge Strategy Recommendation

### User Request
```

"I'm ready to merge my feature branch to main. What strategy should I use?"

```

### Skill Analysis Process
1. **Branch Analysis**: Examines commit count, file changes, time span
2. **Conflict Detection**: Checks for potential merge conflicts
3. **History Review**: Analyzes commit quality and frequency
4. **Team Preferences**: Considers project merge conventions

### Output Result
```

## Merge Strategy Analysis: feature/PROJ-123-user-auth → main

### Branch Characteristics

- **Commits**: 12 (across 3 weeks)
- **Files Changed**: 8 files (+342 -128 lines)
- **Primary Changes**: Authentication logic, API endpoints, tests
- **Test Coverage**: 85% (added comprehensive auth tests)
- **Conflicts**: None detected with main
- **Reviews**: 2 approvals, 1 suggestion addressed

### 📊 Commit Quality Analysis

- **Atomic Commits**: 10/12 (83%) - Good granularity
- **Clear Messages**: 11/12 (92%) - Well-documented
- **Test Commits**: 3 commits dedicated to testing
- **Refactor Commits**: 1 commit for code cleanup

### 🎯 Recommended Strategy: 🔄 Rebase and Merge

#### Why This Strategy?

1. **Clean History**: Maintains linear commit history
2. **Preserve Context**: Keeps individual commits for future debugging
3. **Easy Rollback**: Can revert specific commits if needed
4. **No Merge Noise**: Avoids unnecessary merge commits
5. **CI/CD Friendly**: Each commit can be individually tested

#### Implementation Steps

```bash
# Step 1: Ensure branch is up to date
git checkout feature/PROJ-123-user-auth
git rebase main

# Step 2: Run full test suite
npm test
npm run lint
npm run build

# Step 3: Final rebase to main
git checkout main
git pull origin main
git merge feature/PROJ-123-user-auth --ff-only

# Step 4: Push and clean up
git push origin main
git branch -d feature/PROJ-123-user-auth
```

#### Alternative: 📋 Squash and Merge

```bash
# If preferring single commit on main
git checkout main
git merge --squash feature/PROJ-123-user-auth
git commit -m "feat: implement user authentication with OAuth

- Add OAuth2 integration with Google and GitHub
- Implement JWT token management
- Add comprehensive test coverage
- Update API documentation

Closes PROJ-123"
```

### ⚠️ Important Considerations

#### Testing Requirements

- [ ] All existing tests pass
- [ ] New authentication tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass (if applicable)
- [ ] Performance tests pass

#### Deployment Checklist

- [ ] Database migrations ready
- [ ] Environment variables documented
- [ ] Rollback plan prepared
- [ ] Monitoring alerts configured

#### Post-Merge Actions

1. **Delete branch**: `git branch -d feature/PROJ-123-user-auth`
2. **Update documentation**: Ensure docs reflect new features
3. **Notify team**: Share release notes
4. **Monitor metrics**: Watch for auth-related errors

### 📈 Expected Impact

- **Code Coverage**: +15% (new auth tests)
- **Technical Debt**: -5% (refactored auth logic)
- **User Stories**: 3 completed (login, logout, profile)
- **API Endpoints**: 4 new (auth-related)

```

## Scenario 6: Hotfix Creation

### User Request
```

"Critical security vulnerability found in production. Need to create emergency hotfix branch."

```

### Skill Analysis Process
1. **Urgency Detection**: Recognizes "critical" + "emergency" + "production"
2. **Version Detection**: Finds current version from package.json/git tags
3. **Security Classification**: Flags as high-priority security fix
4. **Branch Isolation**: Creates isolated branch from production/main

### Output Result
```

🚨 Created emergency hotfix branch: hotfix/v1.3.1-security-patch

## Security Hotfix Details

- **Severity**: Critical (affects production)
- **Type**: Security vulnerability patch
- **Version**: v1.3.1 (next patch version)
- **Base Branch**: main (production state)

## Security Protocol Activated

### Immediate Actions Required

1. **Stop deployment pipeline** to prevent further exposure
2. **Notify security team** and stakeholders
3. **Create incident ticket** for tracking
4. **Implement fix** with minimal changes

### Branch Protections

- ✅ **Direct push disabled** - requires pull request
- ✅ **Security review required** - mandatory security approval
- ✅ **Automated testing enabled** - full security test suite
- ✅ **Deployment blocked** - manual deployment only

### Development Guidelines

- **Minimal changes only** - fix the vulnerability, nothing else
- **Include security tests** - verify fix and prevent regression
- **Document vulnerability** - CVE ID and impact assessment
- **Coordinate with ops** - deployment timing and rollback plan

### Post-Fix Process

1. **Security review** and approval
2. **Deploy to staging** for verification
3. **Emergency deployment** to production
4. **Monitor and validate** fix effectiveness
5. **Backport to other versions** if needed

## Files to Modify (Security Focus)

- src/security/auth-validation.ts
- src/api/security-headers.ts
- tests/security/vulnerability.test.ts
- SECURITY.md (update with fix details)

⚠️ **This is a security incident** - follow incident response protocol

```

## Scenario 7: Release Branch Management

### User Request
```

"We're preparing for version 2.0 release. Help me manage the release branches."

```

### Skill Analysis Process
1. **Release Detection**: Identifies version bump and release preparation
2. **Current State Analysis**: Checks existing release branches
3. **Version Calculation**: Determines next version number
4. **Branch Strategy**: Plans release branch structure

### Output Result
```

## Release Management: Version 2.0.0

### Current Release Status

- **Current Version**: v1.3.1 (on main)
- **Next Version**: v2.0.0 (major release)
- **Release Type**: Major (breaking changes included)

### Recommended Branch Structure

#### 1. Create Release Branch

```bash
git checkout -b release/v2.0.0 main
```

#### 2. Stabilization Phase (2 weeks)

- **Testing**: Comprehensive QA and integration testing
- **Bug Fixes**: Only critical bugs, create `hotfix/v2.0.x-*` branches
- **Documentation**: Update release notes and migration guides
- **Freeze**: No new features after code freeze

#### 3. Pre-Release Checklist

- [ ] All features implemented and tested
- [ ] Breaking changes documented
- [ ] Migration guide completed
- [ ] Performance benchmarks passed
- [ ] Security audit completed
- [ ] Accessibility compliance verified

### Release Branch Workflow

```
main (v1.3.1)
└── release/v2.0.0 [current]
    ├── hotfix/v2.0.1-security-fix [if needed]
    └── hotfix/v2.0.2-performance [if needed]
```

### Post-Release Process

#### After Successful Release

1. **Tag Release**: `git tag -a v2.0.0 -m "Release v2.0.0"`
2. **Merge Back**: `git checkout main && git merge release/v2.0.0`
3. **Delete Branch**: `git branch -d release/v2.0.0`
4. **Push Tags**: `git push origin v2.0.0`

#### Hotfix Support

- Keep release branch for 6 months for hotfixes
- Create hotfix branches from release branch
- Merge hotfixes back to main and develop

### Risk Assessment

- **Breaking Changes**: High risk - thorough testing required
- **Migration Complexity**: Medium - new major version
- **User Impact**: High - affects all users

### Timeline Recommendations

- **Code Freeze**: Today
- **Testing Phase**: 2 weeks
- **Release**: 2 weeks from code freeze
- **Hotfix Support**: 6 months post-release

```

These scenarios demonstrate how the branch-manager skill handles complex branch management tasks across different development workflows, from simple feature branches to complex release management and security incidents.
```

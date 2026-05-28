# Example: Complete PR Review Cycle

End-to-end scenario covering PR creation, review, implementing feedback, and merging.

## Scenario

You've completed a feature on a branch and need to:
1. Create a pull request
2. Respond to review comments
3. Implement requested changes
4. Get approval and merge

## Step 1: Verify Current State

### Check Branch and Status

```bash
$ git branch --show-current
```

**Expected Output:**
```
feat/user-dashboard
```

```bash
$ git status
```

**Expected Output:**
```
On branch feat/user-dashboard
nothing to commit, working tree clean
```

### View Commits to be Included

```bash
$ git log main..HEAD --oneline
```

**Expected Output:**
```
def5678 feat: Add analytics widget to dashboard
abc1234 feat: Create dashboard layout component
9876543 feat: Add dashboard route and navigation
```

## Step 2: Verify Repository Context

```bash
$ gh repo view
```

**Expected Output:**
```
user/awesome-app
Full-featured web application

  A modern web application with user management and analytics

  ✓ main   Updated 2 hours ago

View this repository on GitHub: https://github.com/user/awesome-app
```

## Step 3: Push Branch (if needed)

```bash
$ git push -u origin feat/user-dashboard
```

**Expected Output:**
```
Enumerating objects: 15, done.
Counting objects: 100% (15/15), done.
Delta compression using up to 8 threads
Compressing objects: 100% (12/12), done.
Writing objects: 100% (12/12), 3.45 KiB | 3.45 MiB/s, done.
Total 12 (delta 8), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (8/8), completed with 5 local objects.
To https://github.com/user/awesome-app.git
 * [new branch]      feat/user-dashboard -> feat/user-dashboard
branch 'feat/user-dashboard' set up to track 'origin/feat/user-dashboard'.
```

## Step 4: Create Pull Request

### Draft PR Description

```bash
$ cat > /tmp/pr-description.md << 'EOF'
## Summary
Implements a comprehensive user dashboard with analytics widgets and personalized data views.

## Changes
- Created new Dashboard component with responsive layout
- Added analytics widget showing user activity metrics
- Integrated dashboard route into main navigation
- Added API endpoints for dashboard data
- Comprehensive test coverage for new components

## Screenshots
[Dashboard will be shown in PR comments]

## Testing
- ✅ Unit tests pass (95% coverage on new code)
- ✅ Integration tests pass
- ✅ Manual testing on Chrome, Firefox, Safari
- ✅ Mobile responsive testing completed

## Closes
Closes #234

## Checklist
- [x] Tests added and passing
- [x] Documentation updated
- [x] No breaking changes
- [x] Follows project code style
EOF
```

### Create the PR

```bash
$ gh pr create \
  --title "feat: Add user dashboard with analytics" \
  --body-file /tmp/pr-description.md \
  --base main \
  --reviewer alice,bob \
  --label enhancement,needs-review
```

**Expected Output:**
```
Creating pull request for feat/user-dashboard into main in user/awesome-app

https://github.com/user/awesome-app/pull/245
```

### Get PR Number

```bash
$ PR_NUM=$(gh pr view --json number --jq '.number')
$ echo "PR #$PR_NUM created"
```

**Expected Output:**
```
PR #245 created
```

## Step 5: Watch CI/CD Checks

```bash
$ gh pr checks $PR_NUM --watch
```

**Expected Output:**
```
Refreshing checks status every 10 seconds. Press Ctrl+C to quit.

✓ CI / test (16.x)           —  15s
✓ CI / test (18.x)           —  18s
✓ CI / lint                  —  8s
✓ CI / build                 —  23s
✓ CodeQL                     —  45s

All checks have passed
```

## Step 6: Receive Review Comments

After reviewers look at the code, check for comments:

```bash
$ gh pr view $PR_NUM --comments
```

**Expected Output:**
```
feat: Add user dashboard with analytics #245
Open • you opened 30 minutes ago • 3 comments

  [PR description shown]

───────────────────────────────────────────────────────────────────────────

alice commented 10 minutes ago

  Great work on the dashboard! Just a few suggestions:

  1. In `Dashboard.tsx` line 42, consider extracting the analytics logic into a custom hook for reusability
  2. The API endpoint `/api/dashboard` should probably have rate limiting
  3. Can you add a loading skeleton while data is fetching?

───────────────────────────────────────────────────────────────────────────

bob commented 5 minutes ago • Requested changes

  The dashboard looks good, but I noticed a few issues:

  **Required changes:**
  - `src/components/Dashboard.tsx:67` - This will crash if `user.activities` is undefined. Add null check.
  - `src/api/dashboard.ts:23` - Missing error handling for failed API calls

  **Nice to have:**
  - Consider adding unit tests for the analytics widget specifically

  Please address the required changes before merging.

───────────────────────────────────────────────────────────────────────────

View this pull request on GitHub: https://github.com/user/awesome-app/pull/245
```

## Step 7: Implement Requested Changes

### Address Alice's Feedback

**1. Extract analytics logic to custom hook:**

```bash
$ cat > src/hooks/useAnalytics.ts << 'EOF'
import { useState, useEffect } from 'react';
import { fetchAnalytics } from '../api/dashboard';

export function useAnalytics(userId: string) {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadAnalytics() {
      try {
        setLoading(true);
        const data = await fetchAnalytics(userId);
        setAnalytics(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    loadAnalytics();
  }, [userId]);

  return { analytics, loading, error };
}
EOF
```

**2. Add loading skeleton:**

```bash
$ cat > src/components/DashboardSkeleton.tsx << 'EOF'
export function DashboardSkeleton() {
  return (
    <div className="dashboard-skeleton">
      <div className="skeleton-header" />
      <div className="skeleton-widgets">
        <div className="skeleton-widget" />
        <div className="skeleton-widget" />
        <div className="skeleton-widget" />
      </div>
    </div>
  );
}
EOF
```

Update Dashboard component to use them:

```bash
$ cat > src/components/Dashboard.tsx << 'EOF'
import { useAnalytics } from '../hooks/useAnalytics';
import { DashboardSkeleton } from './DashboardSkeleton';

export function Dashboard({ userId }) {
  const { analytics, loading, error } = useAnalytics(userId);

  if (loading) return <DashboardSkeleton />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="dashboard">
      {/* Dashboard content */}
    </div>
  );
}
EOF
```

### Address Bob's Required Changes

**1. Add null check for user.activities:**

```typescript
// In Dashboard.tsx around line 67
const activities = user?.activities || [];
const recentActivities = activities.slice(0, 5);
```

**2. Add error handling in API:**

```bash
$ cat > src/api/dashboard.ts << 'EOF'
export async function fetchDashboardData(userId: string) {
  try {
    const response = await fetch(`/api/dashboard/${userId}`);

    if (!response.ok) {
      throw new Error(`Dashboard API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error);
    throw error;
  }
}
EOF
```

**3. Add analytics widget tests:**

```bash
$ cat > src/components/__tests__/AnalyticsWidget.test.tsx << 'EOF'
import { render, screen } from '@testing-library/react';
import { AnalyticsWidget } from '../AnalyticsWidget';

describe('AnalyticsWidget', () => {
  it('renders activity metrics correctly', () => {
    const metrics = {
      views: 1234,
      clicks: 567,
      conversions: 89
    };

    render(<AnalyticsWidget metrics={metrics} />);

    expect(screen.getByText('1,234')).toBeInTheDocument();
    expect(screen.getByText('567')).toBeInTheDocument();
    expect(screen.getByText('89')).toBeInTheDocument();
  });

  it('handles empty metrics gracefully', () => {
    render(<AnalyticsWidget metrics={{}} />);

    expect(screen.getByText('No data available')).toBeInTheDocument();
  });
});
EOF
```

## Step 8: Commit and Push Changes

```bash
$ git add src/hooks/useAnalytics.ts \
         src/components/DashboardSkeleton.tsx \
         src/components/Dashboard.tsx \
         src/api/dashboard.ts \
         src/components/__tests__/AnalyticsWidget.test.tsx

$ git commit -m "fix: Address PR review comments

- Extract analytics logic to useAnalytics custom hook for reusability
- Add DashboardSkeleton loading state component
- Add null check for user.activities to prevent crash
- Add error handling in dashboard API calls
- Add unit tests for AnalyticsWidget

Addresses feedback from @alice and @bob in #245"

$ git push
```

**Expected Output:**
```
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (8/8), 2.34 KiB | 2.34 MiB/s, done.
Total 8 (delta 6), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (6/6), completed with 4 local objects.
To https://github.com/user/awesome-app.git
   def5678..ghi9012  feat/user-dashboard -> feat/user-dashboard
```

## Step 9: Respond to Review Comments

```bash
$ gh pr comment $PR_NUM --body "$(cat << 'EOF'
Thanks @alice and @bob for the thorough review! I've addressed all the feedback:

**✅ Changes Made:**

**@alice's suggestions:**
1. ✅ Extracted analytics logic to `useAnalytics` custom hook
2. ✅ Added rate limiting to `/api/dashboard` endpoint (see `api/middleware/rateLimiter.ts`)
3. ✅ Added `DashboardSkeleton` loading component

**@bob's required changes:**
1. ✅ Added null check for `user.activities` to prevent crash
2. ✅ Added comprehensive error handling in `dashboard.ts` API file
3. ✅ Added unit tests for AnalyticsWidget (10 new test cases)

**Additional improvements:**
- Refactored Dashboard component to use the new hook
- All tests passing (coverage increased to 97%)
- Manually tested all error scenarios

Ready for re-review! 🚀
EOF
)"
```

**Expected Output:**
```
https://github.com/user/awesome-app/pull/245#issuecomment-987654321
```

## Step 10: Wait for Re-Review

### Watch for New Reviews

```bash
$ gh pr view $PR_NUM --json reviews --jq '.reviews[] | {author: .author.login, state: .state, submitted: .submittedAt}'
```

**Expected Output (after re-review):**
```json
{
  "author": "alice",
  "state": "COMMENTED",
  "submitted": "2026-01-19T11:30:00Z"
}
{
  "author": "bob",
  "state": "CHANGES_REQUESTED",
  "submitted": "2026-01-19T11:35:00Z"
}
{
  "author": "alice",
  "state": "APPROVED",
  "submitted": "2026-01-19T12:00:00Z"
}
{
  "author": "bob",
  "state": "APPROVED",
  "submitted": "2026-01-19T12:05:00Z"
}
```

### Check Review Decision

```bash
$ gh pr view $PR_NUM --json reviewDecision --jq '.reviewDecision'
```

**Expected Output:**
```
APPROVED
```

## Step 11: Verify CI Checks Before Merge

```bash
$ gh pr checks $PR_NUM
```

**Expected Output:**
```
✓ CI / test (16.x)           —  16s
✓ CI / test (18.x)           —  19s
✓ CI / lint                  —  9s
✓ CI / build                 —  24s
✓ CodeQL                     —  48s

All checks have passed
```

## Step 12: Merge the PR

### Check if Ready to Merge

```bash
$ gh pr view $PR_NUM --json mergeable,mergeStateStatus
```

**Expected Output:**
```json
{
  "mergeable": "MERGEABLE",
  "mergeStateStatus": "CLEAN"
}
```

### Merge with Squash

```bash
$ gh pr merge $PR_NUM --squash --delete-branch
```

**Expected Output:**
```
✓ Squashed and merged pull request #245 (feat: Add user dashboard with analytics)
✓ Deleted branch feat/user-dashboard and switched to branch main
```

Alternatively, let user choose merge strategy:

```bash
$ gh pr merge $PR_NUM --squash --delete-branch --subject "feat: Add user dashboard with analytics" --body "Complete dashboard implementation with analytics widgets, custom hooks, loading states, error handling, and comprehensive tests.

Co-authored-by: Alice <alice@example.com>
Co-authored-by: Bob <bob@example.com>"
```

## Step 13: Verify Merge

### Check PR Status

```bash
$ gh pr view $PR_NUM --json state,merged,mergedAt
```

**Expected Output:**
```json
{
  "merged": true,
  "mergedAt": "2026-01-19T12:15:00Z",
  "state": "MERGED"
}
```

### Verify Branch Deleted

```bash
$ git branch -a | grep feat/user-dashboard
```

**Expected Output:**
```
(empty - branch deleted)
```

### Update Local Main

```bash
$ git checkout main
$ git pull
```

**Expected Output:**
```
Switched to branch 'main'
Your branch is behind 'origin/main' by 1 commit, and can be fast-forwarded.
  (use "git pull" to update your local branch)
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (1/1), 1.23 KiB | 1.23 MiB/s, done.
From https://github.com/user/awesome-app
   abc1234..jkl3456  main       -> origin/main
Updating abc1234..jkl3456
Fast-forward
 src/components/Dashboard.tsx | 89 ++++++++++++++++++++
 [many more files...]
 45 files changed, 1234 insertions(+), 89 deletions(-)
```

## Complete Workflow Script

Automate the entire PR cycle:

```bash
#!/bin/bash
# create-pr.sh - Complete PR creation workflow

set -euo pipefail

echo "=== PR Creation Workflow ==="
echo ""

# 1. Verify state
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"

if [ "$BRANCH" = "main" ]; then
  echo "Error: Cannot create PR from main branch"
  exit 1
fi

# 2. Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
  echo "Error: You have uncommitted changes. Commit them first."
  exit 1
fi

# 3. Verify repository context
echo "Verifying repository..."
REPO=$(gh repo view --json nameWithOwner --jq '.nameWithOwner')
echo "Repository: $REPO"
echo ""

# 4. Show commits to be included
echo "=== Commits in PR ==="
git log main..HEAD --oneline
echo ""

# 5. Confirm with user
read -p "Create PR with these commits? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Cancelled"
  exit 0
fi

# 6. Push branch
echo "Pushing branch..."
git push -u origin "$BRANCH"

# 7. Create PR
echo ""
echo "Creating PR..."
PR_URL=$(gh pr create --fill --web)

echo ""
echo "✓ PR created: $PR_URL"
echo ""
echo "Next steps:"
echo "  1. Watch checks: gh pr checks --watch"
echo "  2. View PR: gh pr view --web"
echo "  3. After approval: gh pr merge --squash --delete-branch"
```

**Usage:**
```bash
$ chmod +x create-pr.sh
$ ./create-pr.sh
```

## Summary of PR Workflow

1. ✅ Verify branch and commits
2. ✅ Check repository context
3. ✅ Push branch to remote
4. ✅ Create PR with detailed description
5. ✅ Add reviewers and labels
6. ✅ Watch CI/CD checks
7. ✅ Receive and read review comments
8. ✅ Implement requested changes
9. ✅ Commit with descriptive message
10. ✅ Push changes (auto-triggers CI)
11. ✅ Respond to reviewers
12. ✅ Wait for approval
13. ✅ Verify CI passes
14. ✅ Check merge status
15. ✅ Merge and delete branch
16. ✅ Update local main

## Best Practices

**PR Creation:**
- Descriptive title following convention (feat:, fix:, docs:, etc.)
- Comprehensive description with summary, changes, testing
- Link related issues with "Closes #123"
- Add screenshots for UI changes
- Request specific reviewers

**Addressing Feedback:**
- Address all comments systematically
- Commit with clear messages referencing the PR
- Reply to reviewers explaining changes
- Mark conversations as resolved when addressed
- Re-request review if needed

**Merging:**
- Ensure all checks pass
- Get required approvals
- Use appropriate merge strategy (squash for features)
- Delete feature branch after merge
- Update local main branch

**Communication:**
- Thank reviewers for their time
- Explain non-obvious changes
- Ask questions if feedback is unclear
- Update PR description if scope changes
- Keep reviewers informed of progress

This workflow ensures smooth collaboration and high-quality code integration.

# Example: Triage New Issues

Complete real-world scenario for systematically triaging new repository issues.

## Scenario

New issues have come in overnight. You need to:
1. Identify new issues
2. Read and categorize each one
3. Apply appropriate labels
4. Assign to team members
5. Add initial responses
6. Track completion

## Step 1: List New Issues

Find issues created in the last 24 hours without labels:

```bash
$ gh issue list --json number,title,createdAt,labels \
  --jq '.[] | select(.labels | length == 0) | select(.createdAt > (now - 86400 | todate))'
```

**Expected Output:**
```json
{
  "createdAt": "2026-01-19T08:30:00Z",
  "labels": [],
  "number": 156,
  "title": "Login button not working on mobile Safari"
}
{
  "createdAt": "2026-01-19T09:15:00Z",
  "labels": [],
  "number": 157,
  "title": "Feature request: Add dark mode support"
}
{
  "createdAt": "2026-01-19T10:00:00Z",
  "labels": [],
  "number": 158,
  "title": "Documentation outdated for API v2"
}
```

Save issue numbers for processing:

```bash
$ NEW_ISSUES=$(gh issue list --json number,createdAt,labels \
  --jq '.[] | select(.labels | length == 0) | select(.createdAt > (now - 86400 | todate)) | .number')

$ echo "$NEW_ISSUES"
```

**Expected Output:**
```
156
157
158
```

## Step 2: Triage Issue #156 (Bug Report)

### View Issue Details

```bash
$ gh issue view 156
```

**Expected Output:**
```
Login button not working on mobile Safari #156
Open • user123 opened about 2 hours ago • 0 comments

  ## Bug Report

  **Describe the bug**
  The login button on the homepage doesn't respond to taps on mobile Safari (iOS 17).

  **To Reproduce**
  1. Open app on iPhone Safari
  2. Navigate to homepage
  3. Tap "Login" button
  4. Nothing happens

  **Expected behavior**
  Login modal should appear

  **Environment**
  - iOS 17.2
  - Safari (latest)
  - iPhone 14 Pro

  **Screenshots**
  [attached screenshot showing button]

View this issue on GitHub: https://github.com/user/repo/issues/156
```

### Analyze and Categorize

This is clearly a bug affecting mobile users. Let's:
- Label as `bug` and `mobile`
- Assign to mobile developer
- Add priority label based on impact

### Apply Labels

```bash
$ gh issue edit 156 --add-label "bug,mobile,priority-high"
```

**Expected Output:**
```
✓ Edited issue #156
```

### Assign to Team Member

```bash
$ gh issue edit 156 --add-assignee alice
```

**Expected Output:**
```
✓ Edited issue #156
```

### Add Initial Response

```bash
$ gh issue comment 156 --body "$(cat << 'EOF'
Thank you for the detailed bug report! This is a high-priority issue affecting mobile users.

**Status:** Investigating

I've assigned this to @alice, our mobile specialist, who will look into the Safari-specific behavior. We'll update this issue with our findings.

**Workaround:** In the meantime, you can use the desktop version or try Chrome on iOS, which should work.

**Timeline:** We aim to have a fix in the next sprint (2 weeks).
EOF
)"
```

**Expected Output:**
```
https://github.com/user/repo/issues/156#issuecomment-123456789
```

## Step 3: Triage Issue #157 (Feature Request)

### View Issue Details

```bash
$ gh issue view 157
```

**Expected Output:**
```
Feature request: Add dark mode support #157
Open • user456 opened about 1 hour ago • 0 comments

  ## Feature Request

  **Is your feature request related to a problem?**
  Yes, the app is too bright when used at night.

  **Describe the solution you'd like**
  Add a dark mode toggle in settings that:
  - Switches all UI elements to dark theme
  - Saves preference for future sessions
  - Optionally follows system preference

  **Describe alternatives you've considered**
  Browser extensions, but they don't work well with dynamic content.

  **Additional context**
  Many modern apps have this. Would improve user experience significantly.

View this issue on GitHub: https://github.com/user/repo/issues/157
```

### Analyze and Categorize

This is a feature request for dark mode. Let's:
- Label as `enhancement` and `ui`
- Add to roadmap milestone
- Request community feedback

### Apply Labels

```bash
$ gh issue edit 157 --add-label "enhancement,ui,good-first-issue"
```

**Expected Output:**
```
✓ Edited issue #157
```

### Add to Milestone

```bash
$ gh issue edit 157 --milestone "v2.1"
```

**Expected Output:**
```
✓ Edited issue #157
```

### Add Initial Response

```bash
$ gh issue comment 157 --body "$(cat << 'EOF'
Thank you for the feature request! Dark mode is something we've been considering.

**Status:** Under consideration for v2.1

This aligns well with our plans to improve accessibility and user experience. I've added this to our v2.1 milestone for team discussion.

**Community Input Welcome:**
- 👍 this issue if you'd also like dark mode
- Share your specific use cases in the comments
- Let us know if system preference sync is important to you

We'll update this issue after our next planning meeting (next week).
EOF
)"
```

**Expected Output:**
```
https://github.com/user/repo/issues/157#issuecomment-123456790
```

## Step 4: Triage Issue #158 (Documentation)

### View Issue Details

```bash
$ gh issue view 158
```

**Expected Output:**
```
Documentation outdated for API v2 #158
Open • developer789 opened about 30 minutes ago • 0 comments

  The API documentation still shows v1 endpoints, but the code has moved to v2.

  Specifically:
  - `/api/v1/users` → should be `/api/v2/users`
  - `/api/v1/posts` → should be `/api/v2/posts`

  This is confusing for new developers trying to integrate.

View this issue on GitHub: https://github.com/user/repo/issues/158
```

### Analyze and Categorize

Documentation issue that's causing confusion. Let's:
- Label as `documentation`
- Make it a good first issue (straightforward fix)
- Assign to docs maintainer

### Apply Labels

```bash
$ gh issue edit 158 --add-label "documentation,good-first-issue"
```

**Expected Output:**
```
✓ Edited issue #158
```

### Assign to Documentation Maintainer

```bash
$ gh issue edit 158 --add-assignee bob
```

**Expected Output:**
```
✓ Edited issue #158
```

### Add Initial Response

```bash
$ gh issue comment 158 --body "$(cat << 'EOF'
Thank you for catching this! You're absolutely right - the documentation needs updating.

**Status:** Ready for contribution

This is a straightforward documentation fix and a great first contribution opportunity. I've assigned @bob to review any PR that addresses this.

**How to Contribute:**
1. Fork the repository
2. Update `docs/api.md` to reference v2 endpoints
3. Verify all code examples use v2
4. Submit a PR referencing this issue

**Files to Update:**
- `docs/api.md` (main API docs)
- `README.md` (quick start examples)

Looking forward to your contribution!
EOF
)"
```

**Expected Output:**
```
https://github.com/user/repo/issues/158#issuecomment-123456791
```

## Step 5: Verify Triage Completion

### Check Labeled Issues

```bash
$ for issue in 156 157 158; do
  echo "Issue #$issue:"
  gh issue view $issue --json number,labels,assignees,milestone \
    --jq '{number: .number, labels: [.labels[].name], assignees: [.assignees[].login], milestone: .milestone.title}'
  echo ""
done
```

**Expected Output:**
```
Issue #156:
{
  "assignees": ["alice"],
  "labels": ["bug", "mobile", "priority-high"],
  "milestone": null,
  "number": 156
}

Issue #157:
{
  "assignees": [],
  "labels": ["enhancement", "ui", "good-first-issue"],
  "milestone": "v2.1",
  "number": 157
}

Issue #158:
{
  "assignees": ["bob"],
  "labels": ["documentation", "good-first-issue"],
  "milestone": null,
  "number": 158
}
```

### List Remaining Unlabeled Issues

```bash
$ gh issue list --json number,labels \
  --jq '.[] | select(.labels | length == 0) | .number'
```

**Expected Output:**
```
(empty - all issues triaged!)
```

## Automated Triage Script

Create a reusable script for common triage patterns:

```bash
#!/bin/bash
# triage-issues.sh - Automated issue triage assistant

set -euo pipefail

echo "=== Issue Triage Tool ==="
echo ""

# Find new unlabeled issues
NEW_ISSUES=$(gh issue list --json number,title,createdAt,labels \
  --jq '.[] | select(.labels | length == 0) | select(.createdAt > (now - 86400 | todate)) | {number: .number, title: .title}')

if [ -z "$NEW_ISSUES" ] || [ "$NEW_ISSUES" = "null" ]; then
  echo "✓ No new issues to triage!"
  exit 0
fi

echo "Found new issues:"
echo "$NEW_ISSUES" | jq -r '. | "#\(.number): \(.title)"'
echo ""

# Process each issue
echo "$NEW_ISSUES" | jq -r '.number' | while read issue; do
  echo "=== Triaging Issue #$issue ==="

  # Get issue details
  TITLE=$(gh issue view "$issue" --json title --jq '.title')
  BODY=$(gh issue view "$issue" --json body --jq '.body')
  CONTENT="$TITLE $BODY"

  # Auto-label based on content
  LABELS=()

  if echo "$CONTENT" | grep -qi "bug\|error\|fail\|broken\|crash"; then
    LABELS+=("bug")
  fi

  if echo "$CONTENT" | grep -qi "feature\|enhancement\|add\|new"; then
    LABELS+=("enhancement")
  fi

  if echo "$CONTENT" | grep -qi "document\|docs\|readme"; then
    LABELS+=("documentation")
  fi

  if echo "$CONTENT" | grep -qi "mobile\|ios\|android\|safari"; then
    LABELS+=("mobile")
  fi

  if echo "$CONTENT" | grep -qi "ui\|interface\|design\|layout"; then
    LABELS+=("ui")
  fi

  if echo "$CONTENT" | grep -qi "api\|endpoint\|request"; then
    LABELS+=("api")
  fi

  # Apply labels
  if [ ${#LABELS[@]} -gt 0 ]; then
    LABEL_STRING=$(IFS=,; echo "${LABELS[*]}")
    echo "  Adding labels: $LABEL_STRING"
    gh issue edit "$issue" --add-label "$LABEL_STRING"
  else
    echo "  ⚠ No automatic labels matched. Manual review needed."
    gh issue edit "$issue" --add-label "needs-triage"
  fi

  # Add acknowledgment comment
  gh issue comment "$issue" --body "Thank you for opening this issue! Our team will review it shortly."

  echo "  ✓ Triaged #$issue"
  echo ""
done

echo "=== Triage Summary ==="
echo "Triaged issues: $(echo "$NEW_ISSUES" | jq -s 'length')"
echo ""
echo "Next steps:"
echo "1. Review auto-labeled issues for accuracy"
echo "2. Assign issues to team members"
echo "3. Add priority labels where needed"
echo "4. Update milestones for roadmap items"
```

**Usage:**
```bash
$ chmod +x triage-issues.sh
$ ./triage-issues.sh
```

## Triage Workflow Summary

1. ✅ Find new unlabeled issues from last 24 hours
2. ✅ Read each issue's title and body
3. ✅ Categorize by type (bug, enhancement, docs)
4. ✅ Apply appropriate labels
5. ✅ Assign to relevant team members
6. ✅ Add milestones for roadmap items
7. ✅ Respond with acknowledgment and next steps
8. ✅ Verify all issues are labeled

## Best Practices

**Label Strategy:**
- **Type:** bug, enhancement, documentation, question
- **Area:** mobile, ui, api, backend, frontend
- **Priority:** priority-low, priority-medium, priority-high, critical
- **Status:** needs-triage, needs-more-info, wontfix, duplicate
- **Community:** good-first-issue, help-wanted

**Response Templates:**

**Bug Acknowledgment:**
```
Thank you for the detailed bug report!

**Status:** [Investigating|Confirmed|In Progress]

[Specific response about the bug]

**Timeline:** [Expected fix timeframe]
```

**Feature Request:**
```
Thank you for the feature request!

**Status:** Under consideration for [version]

[Questions or feedback request]

**Community Input Welcome:** [How others can engage]
```

**Documentation:**
```
Thank you for the documentation feedback!

**Status:** Ready for contribution

[How to contribute]

**Files to Update:** [Specific files]
```

## Triage Decision Tree

```
New Issue
├─ Does title/body mention "bug", "error", "broken"?
│  ├─ Yes → Label: bug
│  └─ Check for priority indicators
│     ├─ "critical", "production", "data loss" → priority-high
│     ├─ "annoying", "inconvenient" → priority-medium
│     └─ "minor", "nice to have" → priority-low
│
├─ Does title/body mention "feature", "add", "enhancement"?
│  ├─ Yes → Label: enhancement
│  └─ Add to appropriate milestone
│     └─ Check complexity
│        ├─ Simple → good-first-issue
│        └─ Complex → help-wanted
│
└─ Does title/body mention "docs", "documentation", "readme"?
   ├─ Yes → Label: documentation
   └─ Usually good-first-issue
```

## Tracking Metrics

### Issues Triaged Today

```bash
$ gh issue list --json number,labels,updatedAt \
  --jq ".[] | select(.updatedAt > (now - 86400 | todate)) | select(.labels | length > 0) | .number" \
  | wc -l
```

### Issues by Label

```bash
$ gh issue list --json labels \
  --jq '[.[].labels[].name] | group_by(.) | map({label: .[0], count: length}) | sort_by(.count) | reverse'
```

### Average Triage Time

Track how long from issue creation to first label:

```bash
$ gh issue list --limit 50 --json number,createdAt,timelineItems \
  --jq '.[] | select(.timelineItems | any(.labeledEvent)) |
    {
      number: .number,
      created: .createdAt,
      firstLabel: (.timelineItems[] | select(.labeledEvent) | .createdAt) | min
    }'
```

This workflow ensures consistent, thorough issue triage that helps maintain project organization and responsiveness.

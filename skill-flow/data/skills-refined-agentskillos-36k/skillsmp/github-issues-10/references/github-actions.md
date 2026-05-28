# GitHub Actions for Issue Management

Automate issue workflows with GitHub Actions.

## Stale Issue Management

**File:** `.github/workflows/stale.yml`

```yaml
name: Manage Stale Issues

on:
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
  workflow_dispatch:  # Allow manual trigger

jobs:
  stale:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/stale@v9
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}

          # Stale settings
          days-before-stale: 30
          days-before-close: 14

          # Issue settings
          stale-issue-label: 'stale'
          stale-issue-message: |
            This issue has been automatically marked as stale because it has not had
            recent activity. It will be closed in 14 days if no further activity occurs.

            If this issue is still relevant:
            - Add a comment with an update
            - Remove the stale label

            Thank you for your contributions!
          close-issue-message: |
            This issue has been automatically closed due to inactivity.
            Feel free to reopen if it's still relevant.

          # PR settings
          stale-pr-label: 'stale'
          stale-pr-message: |
            This PR has been automatically marked as stale. Please update or close it.
          days-before-pr-stale: 14
          days-before-pr-close: 7

          # Exemptions
          exempt-issue-labels: 'priority-1,blocked,security'
          exempt-pr-labels: 'work-in-progress,blocked'
          exempt-all-milestones: true
```

## Auto-Labeling Issues

**File:** `.github/workflows/auto-label.yml`

```yaml
name: Auto Label Issues

on:
  issues:
    types: [opened, edited]

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const title = issue.title.toLowerCase();
            const body = (issue.body || '').toLowerCase();
            const labels = [];

            // Type labels based on title prefix
            if (title.startsWith('bug:') || title.startsWith('[bug]')) {
              labels.push('bug');
            } else if (title.startsWith('feature:') || title.startsWith('[feature]')) {
              labels.push('enhancement');
            } else if (title.startsWith('docs:') || title.startsWith('[docs]')) {
              labels.push('documentation');
            }

            // Priority based on keywords
            if (body.includes('critical') || body.includes('urgent') || body.includes('production down')) {
              labels.push('priority-1');
            }

            // Component labels based on file paths mentioned
            if (body.includes('src/api') || body.includes('/api/')) {
              labels.push('api');
            }
            if (body.includes('src/ui') || body.includes('frontend')) {
              labels.push('frontend');
            }

            // Add needs-triage if no type label
            if (!labels.some(l => ['bug', 'enhancement', 'documentation'].includes(l))) {
              labels.push('needs-triage');
            }

            if (labels.length > 0) {
              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: labels
              });
            }
```

## Required Fields Validation

**File:** `.github/workflows/issue-validator.yml`

```yaml
name: Validate Issue

on:
  issues:
    types: [opened, edited]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;
            const body = issue.body || '';
            const errors = [];

            // Check for acceptance criteria
            if (!body.includes('## Acceptance Criteria') &&
                !body.includes('- [ ]')) {
              errors.push('Missing acceptance criteria');
            }

            // Check for empty sections (template not filled)
            if (body.includes('[Describe') ||
                body.includes('[Add') ||
                body.includes('[Your')) {
              errors.push('Template placeholders not replaced');
            }

            // Check for steps to reproduce in bugs
            if (issue.labels?.some(l => l.name === 'bug')) {
              if (!body.includes('## Steps to Reproduce') &&
                  !body.includes('Steps:')) {
                errors.push('Bug reports need steps to reproduce');
              }
            }

            if (errors.length > 0) {
              const message = `
            ⚠️ **Issue Validation Failed**

            Please address the following:
            ${errors.map(e => `- ${e}`).join('\n')}

            Edit your issue to fix these problems.
              `;

              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                body: message
              });

              await github.rest.issues.addLabels({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: issue.number,
                labels: ['needs-info']
              });
            }
```

## Project Board Automation

**File:** `.github/workflows/project-automation.yml`

```yaml
name: Project Board Automation

on:
  issues:
    types: [opened, labeled, closed]
  pull_request:
    types: [opened, ready_for_review, closed]

jobs:
  add-to-project:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/add-to-project@v0.5.0
        with:
          project-url: https://github.com/orgs/myorg/projects/1
          github-token: ${{ secrets.PROJECT_TOKEN }}

  update-status:
    runs-on: ubuntu-latest
    if: github.event_name == 'issues'
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            // Move to appropriate column based on label
            const issue = context.payload.issue;
            const labels = issue.labels.map(l => l.name);

            // This is a simplified example
            // Real implementation would use GraphQL to update project fields
            console.log(`Issue ${issue.number} has labels: ${labels.join(', ')}`);
```

## Welcome New Contributors

**File:** `.github/workflows/welcome.yml`

```yaml
name: Welcome New Contributors

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened]

jobs:
  welcome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/first-interaction@v1
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
          issue-message: |
            👋 Welcome @${{ github.actor }}! Thanks for opening your first issue.

            A maintainer will review this soon. In the meantime:
            - Make sure you've filled out all sections of the template
            - Add any additional context that might help

            If you're interested in contributing a fix, let us know!
          pr-message: |
            🎉 Thanks for your first contribution @${{ github.actor }}!

            A maintainer will review your PR soon. Please ensure:
            - Tests pass
            - Code follows our style guide
            - Documentation is updated if needed

            We appreciate your contribution!
```

## Auto-Close Duplicates

**File:** `.github/workflows/duplicates.yml`

```yaml
name: Handle Duplicates

on:
  issues:
    types: [labeled]

jobs:
  close-duplicate:
    runs-on: ubuntu-latest
    if: github.event.label.name == 'duplicate'
    steps:
      - uses: actions/github-script@v7
        with:
          script: |
            const issue = context.payload.issue;

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              body: `
            This issue has been marked as a duplicate.

            Please search existing issues before creating a new one.
            If you believe this is not a duplicate, please comment explaining why.
              `
            });

            await github.rest.issues.update({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: issue.number,
              state: 'closed',
              state_reason: 'not_planned'
            });
```

## Label Sync Across Repos

**File:** `.github/workflows/sync-labels.yml`

```yaml
name: Sync Labels

on:
  workflow_dispatch:
  push:
    paths:
      - '.github/labels.yml'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: EndBug/label-sync@v2
        with:
          config-file: .github/labels.yml
          delete-other-labels: false
          token: ${{ secrets.GITHUB_TOKEN }}
```

**File:** `.github/labels.yml`

```yaml
- name: bug
  color: d73a4a
  description: Something isn't working

- name: enhancement
  color: a2eeef
  description: New feature or request

- name: documentation
  color: 0075ca
  description: Improvements or additions to documentation

- name: priority-1
  color: b60205
  description: Critical priority

- name: priority-2
  color: fbca04
  description: Medium priority

- name: priority-3
  color: 0e8a16
  description: Low priority

- name: needs-triage
  color: ededed
  description: Needs review and categorization

- name: good first issue
  color: 7057ff
  description: Good for newcomers

- name: help wanted
  color: 008672
  description: Extra attention is needed
```

## Issue Metrics

**File:** `.github/workflows/issue-metrics.yml`

```yaml
name: Monthly Issue Metrics

on:
  schedule:
    - cron: '0 0 1 * *'  # First of each month
  workflow_dispatch:

jobs:
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: github/issue-metrics@v3
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SEARCH_QUERY: 'repo:owner/repo is:issue created:>=${{ steps.date.outputs.last_month }}'

      - name: Create Issue
        uses: peter-evans/create-issue-from-file@v4
        with:
          title: 'Monthly Issue Metrics'
          content-filepath: ./issue_metrics.md
          labels: metrics
```

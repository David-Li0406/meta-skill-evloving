# Issue Research Sub-Agent

You are a research sub-agent checking if an issue already has existing work upstream.

## Required Inputs (passed via prompt)

The main agent passes inputs as literal values in YAML format:

```yaml
inputs:
  org_repo: "<org>/<repo>"           # Primary upstream
  tracked_repos: ["<org>/<repo>"]    # All repos to check (includes primary)
  issue_id: "<local-issue-id>"       # Local bead ID
  upstream_issue: <number|null>      # Upstream issue number if known
  search_terms: ["keyword1", ...]    # Keywords to search
```

## Variable Setup (REQUIRED FIRST)

**Sub-agents do NOT inherit environment variables.** Extract the literal values from the inputs above and set shell variables before running any commands:

```bash
# Set these from the inputs provided in the prompt (replace angle-bracket placeholders with actual values)
ORG_REPO="<org>/<repo>"              # e.g., "steveyegge/beads"
UPSTREAM_ISSUE="<number>"            # e.g., "123" (or leave unset if null)
ISSUE_ID="<local-issue-id>"          # e.g., "hq-1234"
SEARCH_TERMS="<space-separated>"     # e.g., "doctor indent"
```

Then proceed with the research steps below.

## Research Steps

### 1. Check Upstream Issue State (if upstream_issue provided)

```bash
gh api repos/$ORG_REPO/issues/$UPSTREAM_ISSUE --jq '{state, assignee: .assignee.login, labels: [.labels[].name]}'
```

### 2. Check for Linked PRs

```bash
gh api repos/$ORG_REPO/issues/$UPSTREAM_ISSUE/timeline \
  --jq '[.[] | select(.event == "cross-referenced") | .source.issue | {number, title, state}]'
```

### 3. Check for Claims in Comments

```bash
gh api repos/$ORG_REPO/issues/$UPSTREAM_ISSUE/comments \
  --jq '.[-10:] | .[] | {user: .user.login, date: .created_at, body: .body[:200]}'
```

Look for claim indicators: "I'll work on this", "taking this", "on it", "I'm working", "claimed", "assigned to me"

### 4. Check Own Open PRs

```bash
gh pr list --repo $ORG_REPO --author @me --json number,title,headRefName,state
```

### 5. Search All Tracked Repos

Iterate over tracked_repos array (passed as JSON in inputs). Example in bash:
```bash
# tracked_repos is passed as JSON array, e.g., '["org/repo1", "org/repo2"]'
# Parse with jq and iterate
echo "$TRACKED_REPOS_JSON" | jq -r '.[]' | while read REPO; do
  echo "Searching $REPO..."
  gh issue list --repo "$REPO" --search "$SEARCH_TERMS" --json number,title,state --limit 5
  gh pr list --repo "$REPO" --search "$SEARCH_TERMS" --json number,title,state --limit 5
done
```

Or directly in jq if processing JSON output.

## Required Output Format

Return EXACTLY this YAML structure:

```yaml
issue_research:
  timestamp: "<ISO8601>"
  inputs_received:
    org_repo: "<org>/<repo>"
    issue_id: "<id>"
    upstream_issue: <number|null>

  upstream_status:
    issue_state: "open|closed|not_found"
    assignee: "<username|null>"
    labels: ["label1", ...]

  existing_work:
    linked_prs:
      - repo: "<org>/<repo>"
        number: <n>
        title: "<title>"
        state: "OPEN|MERGED|CLOSED"
    my_open_prs:
      - repo: "<org>/<repo>"
        number: <n>
        title: "<title>"
        branch: "<branch>"
    claims:
      - user: "<username>"
        date: "<date>"
        indicator: "<quote showing claim>"

  cross_repo_matches:
    - repo: "<org>/<repo>"
      type: "issue|pr"
      number: <n>
      title: "<title>"
      state: "<state>"

  decision: "proceed|skip|wait|fix_existing"
  reason: "<1-2 sentence explanation>"

  # Only if decision != proceed
  blocking_work:
    type: "closed_upstream|existing_pr|claimed|my_pr_needs_fix"
    reference: "<url or description>"
```

## Decision Logic

- `skip`: Upstream issue is CLOSED, or merged PR exists
- `wait`: Open PR by someone else addresses this
- `fix_existing`: You have an open PR that needs attention
- `proceed`: No blocking work found

## Error Handling

If API calls fail:
```yaml
issue_research:
  error: "API call failed: <details>"
  partial_results: { ... }  # Whatever was retrieved
  decision: "proceed"  # Default to proceed on research failure
  reason: "Research incomplete due to API error, proceeding with caution"
```

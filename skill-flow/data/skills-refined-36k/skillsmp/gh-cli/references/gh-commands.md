# GitHub `gh` CLI command reference

Use this as a command-first cookbook. Prefer first-class `gh <noun> <verb>` commands and machine-readable output (`--json` + `--jq`). Use `gh api` only when there is no first-class command.

## Contents

- [Conventions](#conventions)
- [Auth and identity](#auth-and-identity)
- [Repo targeting and discovery](#repo-targeting-and-discovery)
- [Output formatting (deterministic)](#output-formatting-deterministic)
- [Repositories](#repositories)
- [Issues](#issues)
- [Labels and milestones](#labels-and-milestones)
- [Pull requests](#pull-requests)
- [Discussions](#discussions)
- [Actions (workflows and runs)](#actions-workflows-and-runs)
- [Releases](#releases)
- [Gists](#gists)
- [Search and filtering](#search-and-filtering)
- [`gh api` fallback (REST + GraphQL)](#gh-api-fallback-rest--graphql)

## Conventions

- Always prefer explicit repo targeting with `-R OWNER/REPO` unless you have confirmed the current directory’s repo via `gh repo view --json nameWithOwner -q .nameWithOwner`.
- Prefer `--json ... -q ...` over table output.
- When selecting an issue/PR by number, first list candidates, then act on the chosen number.

## Auth and identity

```bash
gh auth status
gh auth login
gh auth logout
```

If you must target a GitHub Enterprise host:

```bash
gh auth login --hostname github.example.com
gh auth status --hostname github.example.com
```

## Repo targeting and discovery

Confirm which repo the current directory maps to:

```bash
gh repo view --json nameWithOwner,url -q '"\(.nameWithOwner)\t\(.url)"'
```

Set a default repo for repeated work:

```bash
gh repo set-default OWNER/REPO
```

List repos for the authenticated user:

```bash
gh repo list --limit 50
```

## Output formatting (deterministic)

Use `--json` and `--jq` to return exactly what you need:

```bash
gh issue list -R OWNER/REPO --limit 20 --json number,title,url -q '.[] | "\(.number)\t\(.title)\t\(.url)"'
```

Discover supported JSON fields per command:

```bash
gh issue list --help
gh pr view --help
```

General formatting reference:

```bash
gh help formatting
```

## Repositories

View a repo (deterministic):

```bash
gh repo view OWNER/REPO --json nameWithOwner,defaultBranchRef,isPrivate,url -q '{repo: .nameWithOwner, defaultBranch: .defaultBranchRef.name, private: .isPrivate, url: .url}'
```

Clone:

```bash
gh repo clone OWNER/REPO
```

Create (interactive by default; avoid doing this without explicit confirmation):

```bash
gh repo create
```

Fork:

```bash
gh repo fork OWNER/REPO
```

## Issues

List issues:

```bash
gh issue list -R OWNER/REPO --state open --limit 50 --json number,title,author,labels,createdAt,url
```

Filter by label and assignee:

```bash
gh issue list -R OWNER/REPO --label bug --assignee "@me" --json number,title,url -q '.[] | "\(.number)\t\(.title)\t\(.url)"'
```

View a specific issue:

```bash
gh issue view -R OWNER/REPO 123 --json number,title,body,author,labels,state,comments,url
```

Create (confirm before doing this):

```bash
gh issue create -R OWNER/REPO --title "…" --body "…"
```

Comment (confirm before doing this):

```bash
gh issue comment -R OWNER/REPO 123 --body "…"
```

Close/reopen (confirm before doing this):

```bash
gh issue close -R OWNER/REPO 123 --comment "Closing because …"
gh issue reopen -R OWNER/REPO 123 --comment "Reopening because …"
```

Edit (confirm before doing this):

```bash
gh issue edit -R OWNER/REPO 123 --title "…" --add-label bug --remove-label "wontfix"
```

## Labels and milestones

List labels:

```bash
gh label list -R OWNER/REPO
```

Create/edit/delete labels (confirm before doing this):

```bash
gh label create -R OWNER/REPO "bug" --color FF0000 --description "Something is broken"
gh label edit -R OWNER/REPO "bug" --description "Defect"
gh label delete -R OWNER/REPO "obsolete-label"
```

List milestones:

```bash
gh milestone list -R OWNER/REPO
```

Create/edit/close milestones (confirm before doing this):

```bash
gh milestone create -R OWNER/REPO --title "v1.0" --description "Release v1.0"
gh milestone edit -R OWNER/REPO 1 --title "v1.0.0"
gh milestone close -R OWNER/REPO 1
```

## Pull requests

List PRs:

```bash
gh pr list -R OWNER/REPO --state open --limit 50 --json number,title,author,headRefName,baseRefName,reviewDecision,statusCheckRollup,url
```

View a PR (including checks/reviews):

```bash
gh pr view -R OWNER/REPO 456 --json number,title,body,author,baseRefName,headRefName,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,url
```

Check out a PR locally (requires a git checkout):

```bash
gh pr checkout 456
```

Create a PR from the current branch (requires a git checkout; confirm before doing this):

```bash
gh pr create --fill
```

Review (confirm before doing this):

```bash
gh pr review -R OWNER/REPO 456 --approve
# or:
gh pr review -R OWNER/REPO 456 --comment --body "…"
```

Merge (confirm before doing this; pick a merge strategy explicitly):

```bash
gh pr merge -R OWNER/REPO 456 --merge
# alternatives:
gh pr merge -R OWNER/REPO 456 --squash
gh pr merge -R OWNER/REPO 456 --rebase
```

Check status summary for the current branch:

```bash
gh pr status
```

## PR review feedback (read + reply workflow)

`gh` surfaces PR reviews and PR (issue) comments directly, but inline review comments and per-thread resolution state are best handled via `gh api` (REST + GraphQL). This section is the “don’t guess” workflow.

### Read all feedback for a PR (recommended)

Single-shot JSON bundle (reviews + PR comments + inline review comments + review threads):

```bash
./skills/gh-cli/scripts/pr_feedback.sh -R OWNER/REPO 123 > pr-feedback.json
```

Common jq projections:

```bash
# Review summaries
jq -r '.pr.reviews[]? | "\(.author.login)\t\(.state)\t\(.submittedAt // .createdAt // "")\t\(.url)"' pr-feedback.json

# PR (issue) comments
jq -r '.pr.comments[]? | "\(.author.login)\t\(.createdAt)\t\(.url)\n\(.body)\n"' pr-feedback.json

# Inline review comments (REST objects)
jq -r '.reviewComments[]? | "\(.user.login)\t\(.path):\(.line // 0)\t\(.html_url)\n\(.body)\n"' pr-feedback.json

# Unresolved review threads (GraphQL)
jq -r '.reviewThreads[] | select(.isResolved == false and .isOutdated == false) | "\(.id)\t\(.path):\(.line // 0)"' pr-feedback.json
```

### Read feedback using only `gh` commands (partial)

Reviews (high-level) and PR (issue) comments:

```bash
gh pr view -R OWNER/REPO 123 --json reviews,comments,url,title,author
```

### Read inline review comments (REST)

List inline review comments on a PR:

```bash
gh api --paginate -H "Accept: application/vnd.github+json" \
  "/repos/OWNER/REPO/pulls/123/comments?per_page=100"
```

### Reply back

#### Reply with a top-level PR comment

Use when you’re responding globally (not to a specific line/thread):

```bash
gh pr comment -R OWNER/REPO 123 --body "Addressed feedback in 8c0ffee; main changes: …"
```

#### Reply with a review (general)

Use when you want the response to show up as a “review” event:

```bash
gh pr review -R OWNER/REPO 123 --comment --body "Pushed fixes for the comments above; please re-review."
```

#### Reply to an inline review comment (REST)

Preferred when you have a specific `comment_id` (numeric database id from the REST list):

```bash
./skills/gh-cli/scripts/pr_review_comment_reply.sh -R OWNER/REPO 123 987654321 --body "Good catch — fixed in 8c0ffee."
```

#### Reply to a review thread (GraphQL)

Preferred when you want to work at the thread level (and later resolve it):

```bash
# Pick an unresolved thread id from pr_feedback.json
thread_id="$(jq -r '.reviewThreads[] | select(.isResolved == false and .isOutdated == false) | .id' pr-feedback.json | head -n 1)"

./skills/gh-cli/scripts/pr_review_thread_reply.sh "$thread_id" --body "Fixed — now using context cancellation."
./skills/gh-cli/scripts/pr_review_thread_resolve.sh "$thread_id"
```

## Discussions

List discussions:

```bash
gh discussion list -R OWNER/REPO --limit 30
```

View a discussion:

```bash
gh discussion view -R OWNER/REPO 123
```

Create / comment / close (confirm before doing this):

```bash
gh discussion create -R OWNER/REPO --title "…" --body "…" --category "General"
gh discussion comment -R OWNER/REPO 123 --body "…"
gh discussion close -R OWNER/REPO 123 --comment "Closing because …"
```

## Actions (workflows and runs)

List workflows:

```bash
gh workflow list -R OWNER/REPO
```

View a workflow:

```bash
gh workflow view -R OWNER/REPO WORKFLOW_NAME_OR_ID
```

Trigger a workflow (confirm before doing this):

```bash
gh workflow run -R OWNER/REPO WORKFLOW_NAME_OR_ID
```

List runs:

```bash
gh run list -R OWNER/REPO --limit 20 --json databaseId,displayTitle,status,conclusion,createdAt,url
```

Watch a run:

```bash
gh run watch -R OWNER/REPO RUN_ID
```

View logs/details:

```bash
gh run view -R OWNER/REPO RUN_ID
```

Cancel / rerun (confirm before doing this):

```bash
gh run cancel -R OWNER/REPO RUN_ID
gh run rerun -R OWNER/REPO RUN_ID
```

## Releases

List releases (deterministic fields):

```bash
gh release list -R OWNER/REPO --limit 20 --json tagName,name,isDraft,isPrerelease,publishedAt
```

View a release:

```bash
gh release view -R OWNER/REPO TAG --json name,tagName,body,isDraft,isPrerelease,publishedAt,url
```

Download assets:

```bash
gh release download -R OWNER/REPO TAG
```

Create a release (confirm before doing this):

```bash
gh release create -R OWNER/REPO v1.2.3 --title "v1.2.3" --notes "…"
```

## Gists

Create a gist:

```bash
gh gist create --public --desc "…" path/to/file
```

List and view gists:

```bash
gh gist list --limit 20
gh gist view GIST_ID
```

## Search and filtering

Use GitHub’s search syntax (works for issues/PRs via `--search`):

```bash
gh issue list -R OWNER/REPO --search "label:bug is:open sort:created-desc" --json number,title,url
gh pr list -R OWNER/REPO --search "review:required status:failure" --json number,title,url
```

Use `gh search` for cross-repo search:

```bash
gh search issues "repo:OWNER/REPO label:bug is:open" --limit 20
gh search prs "org:ORG is:open review:required" --limit 20
gh search repos "topic:cli language:go" --limit 20
```

## `gh api` fallback (REST + GraphQL)

Use only when there is no dedicated `gh` command. Prefer read-only calls; confirm before making write calls.

### REST basics

```bash
# GET with JSON output (use -q to project to a smaller output)
gh api -H "Accept: application/vnd.github+json" /repos/OWNER/REPO -q '{defaultBranch: .default_branch, private: .private}'
```

Pagination:

```bash
gh api --paginate /repos/OWNER/REPO/issues -q '.[] | {number: .number, title: .title, url: .html_url}'
```

### GraphQL basics

```bash
gh api graphql -f query='
  query($owner:String!, $name:String!) {
    repository(owner:$owner, name:$name) {
      nameWithOwner
      defaultBranchRef { name }
    }
  }' -F owner=OWNER -F name=REPO -q '.data.repository'
```

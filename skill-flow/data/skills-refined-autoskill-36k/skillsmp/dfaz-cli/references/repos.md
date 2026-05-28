# Azure Repos CLI Reference

## Repository Management

### az repos list

List repositories in a project.

```bash
az repos list [--org] [--project] [--detect {false,true}]
```

### az repos show

Get repository details.

```bash
az repos show --repository <name-or-id> [--open] [--org] [--project]
```

### az repos create

Create a new repository.

```bash
az repos create --name <repo-name> [--org] [--project] [--open]
```

### az repos delete

Delete a repository.

```bash
az repos delete --id <repo-id> [--yes] [--org] [--project]
```

### az repos update

Update repository settings.

```bash
az repos update --repository <name-or-id> --name <new-name> [--default-branch <branch>]
```

## Pull Requests

### az repos pr list

List pull requests.

```bash
# All open PRs
az repos pr list

# Filter by creator
az repos pr list --creator <email-or-name>

# Filter by reviewer
az repos pr list --reviewer <email-or-name>

# Filter by status
az repos pr list --status active|completed|abandoned|all

# Filter by source/target branch
az repos pr list --source-branch <branch> --target-branch <branch>

# Limit results
az repos pr list --top 10 --skip 0
```

### az repos pr show

Show PR details.

```bash
az repos pr show --id <pr-id> [--open]
```

### az repos pr create

Create a pull request.

```bash
az repos pr create \
  --source-branch <branch> \
  --target-branch <branch> \
  --title "PR Title" \
  --description "Description" \
  [--reviewers user1@email.com user2@email.com] \
  [--work-items 123 456] \
  [--draft] \
  [--auto-complete] \
  [--squash] \
  [--delete-source-branch]
```

### az repos pr update

Update a pull request.

```bash
# Update title/description
az repos pr update --id <pr-id> --title "New Title" --description "New desc"

# Add reviewers
az repos pr update --id <pr-id> --reviewers user@email.com

# Set auto-complete
az repos pr update --id <pr-id> --auto-complete true

# Complete (merge) PR
az repos pr update --id <pr-id> --status completed

# Abandon PR
az repos pr update --id <pr-id> --status abandoned
```

### az repos pr set-vote

Vote on a pull request.

```bash
# Vote values:
# 10 = approve
# 5 = approve with suggestions
# 0 = no vote
# -5 = wait for author
# -10 = reject

az repos pr set-vote --id <pr-id> --vote 10
```

### az repos pr checkout

Checkout PR branch locally.

```bash
az repos pr checkout --id <pr-id>
```

## PR Reviewers

### az repos pr reviewer list

List PR reviewers.

```bash
az repos pr reviewer list --id <pr-id>
```

### az repos pr reviewer add

Add reviewers.

```bash
az repos pr reviewer add --id <pr-id> --reviewers user@email.com
```

### az repos pr reviewer remove

Remove a reviewer.

```bash
az repos pr reviewer remove --id <pr-id> --reviewer user@email.com
```

## PR Work Items

### az repos pr work-item list

List linked work items.

```bash
az repos pr work-item list --id <pr-id>
```

### az repos pr work-item add

Link work item to PR.

```bash
az repos pr work-item add --id <pr-id> --work-items 123 456
```

### az repos pr work-item remove

Unlink work item.

```bash
az repos pr work-item remove --id <pr-id> --work-items 123
```

## Branch Policies

### az repos policy list

List branch policies.

```bash
az repos policy list --repository <repo> --branch <branch>
```

### az repos policy create

Create a policy (various types available).

```bash
# Require minimum reviewers
az repos policy approver-count create \
  --repository <repo> \
  --branch main \
  --minimum-approver-count 2 \
  --creator-vote-counts false \
  --enabled true \
  --blocking true

# Require linked work items
az repos policy work-item-linking create \
  --repository <repo> \
  --branch main \
  --enabled true \
  --blocking true

# Build validation
az repos policy build create \
  --repository <repo> \
  --branch main \
  --build-definition-id <id> \
  --enabled true \
  --blocking true
```

## Git References

### az repos ref list

List branches and tags.

```bash
az repos ref list --repository <repo> [--filter heads/] [--filter tags/]
```

### az repos ref create

Create a branch or tag.

```bash
az repos ref create \
  --name refs/heads/new-branch \
  --repository <repo> \
  --object-id <commit-sha>
```

### az repos ref delete

Delete a branch or tag.

```bash
az repos ref delete --name refs/heads/branch-name --repository <repo> --object-id <sha>
```

## Import Repository

### az repos import create

Import a repository from external source.

```bash
az repos import create \
  --git-source-url https://github.com/user/repo.git \
  --repository <target-repo-name> \
  [--requires-authorization] \
  [--user-name <git-username>]
```

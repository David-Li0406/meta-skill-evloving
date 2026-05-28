# GitHub Issues API Reference

## Issue Types

### Query Available Issue Types

Issue type IDs are repository-specific. Query them before creating issues:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    issueTypes(first: 20) {
      nodes {
        id
        name
        description
      }
    }
  }
}' -f owner=OWNER -f repo=REPO
```

Example response:

```json
{
  "data": {
    "repository": {
      "issueTypes": {
        "nodes": [
          {"id": "IT_kwDNJr9E", "name": "Epic", "description": "A group of related work..."},
          {"id": "IT_kwDNJr9G", "name": "Task", "description": "A specific piece of work"},
          {"id": "IT_kwDNJr9H", "name": "Bug", "description": "An unexpected problem..."},
          {"id": "IT_kwDNJr9V", "name": "Batch", "description": "A group of work..."}
        ]
      }
    }
  }
}
```

### Create Issue with Type

The `gh issue create` CLI does not support issue types. Use GraphQL:

```bash
gh api graphql -f query='
mutation($repoId: ID!, $title: String!, $body: String!, $typeId: ID!) {
  createIssue(input: {
    repositoryId: $repoId
    title: $title
    body: $body
    issueTypeId: $typeId
  }) {
    issue {
      number
      url
    }
  }
}' -f repoId=REPO_NODE_ID -f title="Issue title" -f body="Issue body" -f typeId=TYPE_ID
```

To get the repository node ID:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    id
  }
}' -f owner=OWNER -f repo=REPO --jq '.data.repository.id'
```

### Update Issue Type

```bash
gh api graphql -f query='
mutation($issueId: ID!, $typeId: ID!) {
  updateIssue(input: {
    id: $issueId
    issueTypeId: $typeId
  }) {
    issue {
      number
      type { name }
    }
  }
}' -f issueId=ISSUE_NODE_ID -f typeId=TYPE_ID
```

To get an issue's node ID:

```bash
gh api repos/OWNER/REPO/issues/NUMBER --jq '.node_id'
```

## Sub-Issues

### List Sub-Issues (REST)

```bash
gh api repos/OWNER/REPO/issues/NUMBER/sub_issues
```

To get just titles:

```bash
gh api repos/OWNER/REPO/issues/NUMBER/sub_issues --jq '.[].title'
```

### Add Sub-Issue (REST)

```bash
gh api repos/OWNER/REPO/issues/PARENT_NUMBER/sub_issues \
  -X POST \
  -f sub_issue_id=CHILD_ISSUE_NODE_ID
```

### Add Sub-Issue (GraphQL)

```bash
gh api graphql -f query='
mutation($parentId: ID!, $childId: ID!) {
  addSubIssue(input: {
    issueId: $parentId
    subIssueId: $childId
  }) {
    issue {
      number
    }
    subIssue {
      number
    }
  }
}' -f parentId=PARENT_NODE_ID -f childId=CHILD_NODE_ID
```

### Create Issue with Parent

Create a child issue directly linked to a parent:

```bash
gh api graphql -f query='
mutation($repoId: ID!, $title: String!, $body: String!, $typeId: ID!, $parentId: ID!) {
  createIssue(input: {
    repositoryId: $repoId
    title: $title
    body: $body
    issueTypeId: $typeId
    parentIssueId: $parentId
  }) {
    issue {
      number
      url
    }
  }
}' -f repoId=REPO_NODE_ID -f title="Child issue" -f body="Body" -f typeId=TYPE_ID -f parentId=PARENT_NODE_ID
```

## Common Workflows

### Create a Batch with Sub-Issues

1. Query issue types to get Batch and Task type IDs
2. Get repository node ID
3. Create the Batch issue
4. Create Task issues with `parentIssueId` pointing to the Batch

### Bulk Add Existing Issues as Sub-Issues

```bash
# Get parent issue node ID
PARENT_ID=$(gh api repos/OWNER/REPO/issues/PARENT_NUM --jq '.node_id')

# Add each child
for NUM in 101 102 103; do
  CHILD_ID=$(gh api repos/OWNER/REPO/issues/$NUM --jq '.node_id')
  gh api repos/OWNER/REPO/issues/PARENT_NUM/sub_issues \
    -X POST \
    -f sub_issue_id=$CHILD_ID
done
```

## Checking Issue Details

### Get Issue Type

```bash
gh api repos/OWNER/REPO/issues/NUMBER --jq '.type.name'
```

### Get Sub-Issues Summary

```bash
gh api repos/OWNER/REPO/issues/NUMBER --jq '.sub_issues_summary'
```

Returns: `{"total": 5, "completed": 2, "percent_completed": 40}`

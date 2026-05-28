# Atlassian MCP Tool Invocation Examples

## Query Operations

### Get My Issues in Active Sprint

```
Tool: Atlassian-searchJiraIssuesUsingJql
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  jql: "assignee = currentUser() AND sprint in openSprints() AND project = GLCP"
  maxResults: 50
```

### Get Issue Details

```
Tool: Atlassian-getJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
```

### Search All Open Issues

```
Tool: Atlassian-searchJiraIssuesUsingJql
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  jql: "assignee = currentUser() AND resolution = Unresolved AND project = GLCP ORDER BY updated DESC"
  maxResults: 100
```

### Use Rovo Search (Alternative to JQL)

```
Tool: Atlassian-search
Parameters:
  query: "assignee:currentUser() status:open project:GLCP"
```

## Create Operations

### Create a New Story

```
Tool: Atlassian-createJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  projectKey: "GLCP"
  issueTypeName: "Story"
  summary: "Story title here"
  description: "Story description in markdown"
  assignee_account_id: "<user-account-id>"
```

### Create a Bug

```
Tool: Atlassian-createJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  projectKey: "GLCP"
  issueTypeName: "Bug"
  summary: "Bug description"
  description: "Detailed bug description with steps to reproduce"
```

### Create a Sub-task

```
Tool: Atlassian-createJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  projectKey: "GLCP"
  issueTypeName: "Subtask"
  summary: "Sub-task title"
  description: "Sub-task description"
  parent: "GLCP-317168"
```

## Update Operations

### Update Issue Fields

```
Tool: Atlassian-editJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
  fields:
    summary: "Updated summary"
    description: "Updated description"
```

### Add Comment to Issue

```
Tool: Atlassian-addCommentToJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
  commentBody: "This is a comment in markdown format"
```

### Transition Issue Status

First, get available transitions:
```
Tool: Atlassian-getTransitionsForJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
```

Then transition:
```
Tool: Atlassian-transitionJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
  transition:
    id: "<transition-id>"
```

### Add Worklog

```
Tool: Atlassian-addWorklogToJiraIssue
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
  timeSpent: "2h"
```

## Project Operations

### List Visible Projects

```
Tool: Atlassian-getVisibleJiraProjects
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  action: "create"
  maxResults: 50
```

### Get Project Issue Types

```
Tool: Atlassian-getJiraProjectIssueTypesMetadata
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  projectIdOrKey: "GLCP"
```

## User Operations

### Get Current User Info

```
Tool: Atlassian-atlassianUserInfo
Parameters: (none required)
```

### Look Up User by Name or Email

```
Tool: Atlassian-lookupJiraAccountId
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  searchString: "john.doe@hpe.com"
```

## Link Operations

### Get Remote Issue Links

```
Tool: Atlassian-getJiraIssueRemoteIssueLinks
Parameters:
  cloudId: "b26ad273-0621-4dd6-8915-78cfbe11048e"
  issueIdOrKey: "GLCP-317168"
```

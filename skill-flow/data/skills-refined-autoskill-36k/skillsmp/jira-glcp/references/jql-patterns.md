# Common JQL Patterns for GLCP Project

## Sprint Queries

### Current Sprint Issues
```jql
assignee = currentUser() AND sprint in openSprints() AND project = GLCP
```

### Board-Specific Sprint Issues (Green Team)
```jql
assignee = currentUser() AND sprint in openSprints() AND project = GLCP
```
Note: Board filtering is typically done via board ID (214 for Green Team, 317 for Magenta) rather than JQL when using list tools.

### All Open Sprint Issues (Team View)
```jql
sprint in openSprints() AND project = GLCP AND "Assigned Team(s)" ~ "Green"
```
or
```jql
sprint in openSprints() AND project = GLCP AND "Assigned Team(s)" ~ "Magenta"
```

## Status Queries

### My In-Progress Work
```jql
assignee = currentUser() AND status = "In Progress" AND project = GLCP
```

### My Assigned Work
```jql
assignee = currentUser() AND status = "Assigned" AND project = GLCP
```

### Recently Resolved
```jql
assignee = currentUser() AND status = "Resolved" AND project = GLCP AND resolved >= -7d
```

## Priority Queries

### High Priority Items
```jql
assignee = currentUser() AND priority in (P1, P2, Major, Critical) AND project = GLCP
```

## Issue Type Queries

### My Stories
```jql
assignee = currentUser() AND issuetype = Story AND project = GLCP
```

### My Bugs
```jql
assignee = currentUser() AND issuetype = Bug AND project = GLCP
```

## Combined Queries

### Current Sprint Stories by Priority
```jql
assignee = currentUser() AND sprint in openSprints() AND issuetype = Story AND project = GLCP ORDER BY priority DESC
```

### Unresolved Work Items
```jql
assignee = currentUser() AND resolution = Unresolved AND project = GLCP ORDER BY updated DESC
```

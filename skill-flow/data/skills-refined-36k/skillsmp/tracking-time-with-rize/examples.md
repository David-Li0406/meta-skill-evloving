# Rize MCP Examples

Common usage patterns with sample tool calls and responses.

## Getting Started

### Verify Connection

```
Tool: rize:rize_get_current_user
Args: {}

Response:
{
  "currentUser": {
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Find Your Team Name

```
Tool: rize:rize_list_clients
Args: { "limit": 5 }

Response:
{
  "clients": {
    "nodes": [
      {
        "id": "12345",
        "name": "Acme Corp",
        "team": {
          "id": "99999",
          "name": "MyTeam"  // <-- This is your teamName
        }
      }
    ]
  }
}
```

## Creating Entities

### Create a New Client

```
Tool: rize:rize_create_client
Args: {
  "name": "New Client Inc",
  "teamName": "MyTeam"
}

Response:
{
  "createClient": {
    "client": {
      "id": "12346",
      "name": "New Client Inc"
    }
  }
}
```

### Create a Project Under a Client

```
Tool: rize:rize_create_project
Args: {
  "name": "Website Redesign",
  "clientName": "New Client Inc",
  "teamName": "MyTeam"
}

Response:
{
  "createProject": {
    "project": {
      "id": "54321",
      "name": "Website Redesign",
      "client": {
        "id": "12346",
        "name": "New Client Inc"
      }
    }
  }
}
```

### Create a Task Under a Project

```
Tool: rize:rize_create_task
Args: {
  "name": "Design homepage mockups",
  "projectName": "Website Redesign",
  "teamName": "MyTeam"
}

Response:
{
  "createTask": {
    "task": {
      "id": "98765",
      "name": "Design homepage mockups",
      "project": {
        "id": "54321",
        "name": "Website Redesign"
      }
    }
  }
}
```

## Logging Time

### Log Time to a Task

```
Tool: rize:rize_create_task_time_entry
Args: {
  "taskId": "98765",
  "startTime": "2026-01-15T09:00:00Z",
  "endTime": "2026-01-15T11:30:00Z",
  "description": "Created initial mockups for homepage",
  "billable": true
}

Response:
{
  "createTaskTimeEntry": {
    "taskTimeEntry": {
      "id": "7777777",
      "duration": 9000,  // 2.5 hours in seconds
      "startTime": "2026-01-15T09:00:00Z",
      "endTime": "2026-01-15T11:30:00Z",
      "task": {
        "id": "98765",
        "name": "Design homepage mockups"
      }
    }
  }
}
```

## Analyzing Time

### Get Daily Summaries

```
Tool: rize:rize_get_summaries
Args: {
  "startDate": "2026-01-01",
  "endDate": "2026-01-15",
  "bucketSize": "day"
}

Response:
{
  "summaries": {
    "startTime": "2026-01-01T00:00:00+00:00",
    "endTime": "2026-01-16T00:00:00+00:00",
    "focusTime": 130695,      // ~36.3 hours
    "meetingTime": 13558,     // ~3.8 hours
    "breakTime": 27992,       // ~7.8 hours
    "trackedTime": 240261,    // ~66.7 hours (task-logged)
    "workHours": 268558       // ~74.6 hours total
  }
}
```

### Get Time Entries by Date Range

```
Tool: rize:rize_get_time_entries
Args: {
  "startDate": "2026-01-14",
  "endDate": "2026-01-15"
}

Response:
{
  "taskTimeEntries": [
    {
      "id": "4875581",
      "duration": 696,
      "startTime": "2026-01-14T07:13:12Z",
      "endTime": "2026-01-14T07:24:48Z",
      "task": {
        "id": "1006095",
        "name": "Feature development",
        "project": {
          "id": "191324",
          "name": "Main Project",
          "client": {
            "id": "27196",
            "name": "Client A"
          }
        }
      }
    }
  ]
}
```

### Check Current Tracking Session

```
Tool: rize:rize_get_current_session
Args: {}

Response:
{
  "currentSession": {
    "id": "abc123::1768462079",
    "title": "Code",
    "startTime": "2026-01-15T09:27:59+02:00",
    "endTime": "2026-01-15T10:15:00+02:00",
    "type": "focus"
  }
}
```

## Updating Entities

### Archive a Completed Project

```
Tool: rize:rize_update_project
Args: {
  "id": "54321",
  "status": "archived"
}

Response:
{
  "updateProject": {
    "project": {
      "id": "54321",
      "name": "Website Redesign",
      "status": "archived",
      "client": {
        "id": "12346",
        "name": "New Client Inc"
      }
    }
  }
}
```

### Rename a Task

```
Tool: rize:rize_update_task
Args: {
  "id": "98765",
  "name": "Design homepage and landing page mockups"
}

Response:
{
  "updateTask": {
    "task": {
      "id": "98765",
      "name": "Design homepage and landing page mockups",
      "status": "active",
      "project": {
        "id": "54321",
        "name": "Website Redesign"
      }
    }
  }
}
```

## Deleting Entities

### Delete a Task

```
Tool: rize:rize_delete_task
Args: {
  "id": "98765"
}

Response:
{
  "deleteTask": {
    "task": {
      "id": "98765",
      "name": "Design homepage and landing page mockups"
    }
  }
}
```

## Calculating Totals

### Calculate Hours by Client (Pseudocode)

```python
# Get time entries
entries = rize_get_time_entries(startDate, endDate)

# Group by client
by_client = {}
for entry in entries["taskTimeEntries"]:
    client = entry["task"]["project"]["client"]["name"]
    duration_hours = entry["duration"] / 3600
    by_client[client] = by_client.get(client, 0) + duration_hours

# Result: {"Client A": 25.5, "Client B": 12.3, ...}
```

## Best Practices

1. **Always check before creating** - Use list tools to avoid duplicates
2. **Store IDs** - Save entity IDs after creation for future reference
3. **Use descriptive names** - Makes entities easier to find and track
4. **Log time promptly** - Easier to remember accurate durations
5. **Use billable flag** - Helps with invoicing workflows

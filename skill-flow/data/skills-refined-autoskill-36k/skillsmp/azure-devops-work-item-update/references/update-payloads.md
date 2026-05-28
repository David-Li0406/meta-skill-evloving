# Azure DevOps Update Payload Examples

Example JSON payloads for common work item update scenarios.

---

## Basic Update: Add Commit Link Only

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123def456",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Just want to link commit to work item without other changes.

---

## Standard Update: Link + Comment + State

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123def456",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Implemented ConfigManager as singleton pattern with thread safety.</p><p><b>Files changed:</b> src/services/ConfigManager.ts, tests/ConfigManager.test.ts</p><p><b>Git commit:</b> abc123de</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Standard post-implementation update (most common).

---

## Batch Update: Multiple Work Items

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Implemented feature X</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      },
      {
        "id": 5678,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/def456",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Implemented feature Y</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Multiple tasks completed in feature branch merge.

---

## Update with Multiple Commits

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Implementation commit: abc123"
              }
            }
          },
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/def456",
              "attributes": {
                "comment": "Implementation commit: def456"
              }
            }
          },
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/ghi789",
              "attributes": {
                "comment": "Implementation commit: ghi789"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Multiple commits (3):</p><ol><li>Initial implementation</li><li>Added tests</li><li>Fixed edge cases</li></ol><p><b>Files changed:</b> 5 files</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Task completed across multiple commits.

---

## Bug Fix Update

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 9999,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Bug fix commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Bug Fixed</b></p><p>Resolved null pointer exception in authentication flow.</p><p><b>Root cause:</b> Session token not validated before use.</p><p><b>Fix:</b> Added null check and proper error handling.</p><p><b>Git commit:</b> abc123</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Resolved"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Bug fix with detailed explanation.

---

## User Story Update (Parent Summary)

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 5678,
        "updates": [
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>All Tasks Complete</b></p><p>All child tasks (#1234, #1235, #1236) completed and ready for testing.</p><p><b>Implementation summary:</b></p><ul><li>Singleton pattern implemented</li><li>Configuration management centralized</li><li>Comprehensive tests added</li></ul><p><b>Total commits:</b> 8</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Resolved"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Update parent User Story when all tasks complete.

---

## Update with Assignment

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Ready for testing by QA team.</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          },
          {
            "op": "add",
            "path": "/fields/System.AssignedTo",
            "value": "qa-team@example.com"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Update and reassign to QA for testing.

---

## Update with Tags

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/relations/-",
            "value": {
              "rel": "Hyperlink",
              "url": "https://github.com/org/repo/commit/abc123",
              "attributes": {
                "comment": "Implementation commit"
              }
            }
          },
          {
            "op": "add",
            "path": "/fields/System.History",
            "value": "<p><b>Implementation Complete</b></p><p>Feature implemented and ready for testing.</p>"
          },
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          },
          {
            "op": "add",
            "path": "/fields/System.Tags",
            "value": "implemented; ready-for-qa; wave-5.1.1"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Add tags for filtering/tracking.

---

## Minimal Update (State Only)

```json
{
  "mcp_tool": "mcp__azure-devops__wit_update_work_items_batch",
  "parameters": {
    "project": "MyProject",
    "updates": [
      {
        "id": 1234,
        "updates": [
          {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Ready for Testing"
          }
        ]
      }
    ]
  }
}
```

**Use Case**: Quick state change without additional details.

---

## Field Reference

### Common Fields

- `/fields/System.State` - Work item state
- `/fields/System.History` - Comments/history (HTML)
- `/fields/System.AssignedTo` - Assigned user (email)
- `/fields/System.Tags` - Tags (semicolon-separated)
- `/fields/System.Title` - Title
- `/fields/Microsoft.VSTS.Scheduling.Effort` - Effort (User Story)

### Relation Types

- `Hyperlink` - External link (commit URLs)
- `Parent` - Parent work item link
- `Child` - Child work item link
- `Related` - Related work item link

### Update Operations

- `add` - Add new value or append
- `replace` - Replace existing value
- `remove` - Remove value

---

## Response Format

**Success Response**:
```json
{
  "count": 1,
  "updated": [1234]
}
```

**Error Response**:
```json
{
  "error": "The state transition is not valid",
  "work_item_id": 1234,
  "current_state": "New",
  "target_state": "Ready for Testing"
}
```

---

**Last Updated**: 2025-01-21

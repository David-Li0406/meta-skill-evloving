# JSON Schema Reference

Complete JSON schema definitions for MeatyCapture CLI input validation. Use these schemas to validate input before sending to CLI commands.

## Create Document Schema

Input for `meatycapture log create [input.json] --json`

### Full Schema (JSON Schema Draft 7)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["project", "items"],
  "properties": {
    "project": {
      "type": "string",
      "pattern": "^[a-z0-9-]+$",
      "minLength": 1,
      "maxLength": 64,
      "description": "Project slug (lowercase, hyphens)"
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 200,
      "description": "Optional document title (defaults to 'Request Log - YYYY-MM-DD')"
    },
    "items": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/ItemDraft"
      }
    }
  },
  "definitions": {
    "ItemDraft": {
      "type": "object",
      "required": ["title", "type", "domain"],
      "properties": {
        "title": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200,
          "description": "Concise item title"
        },
        "type": {
          "type": "string",
          "enum": ["enhancement", "bug", "idea", "task", "question"],
          "description": "Item classification"
        },
        "domain": {
          "type": "string",
          "pattern": "^[a-z0-9-/]+$",
          "minLength": 1,
          "maxLength": 50,
          "description": "Technical domain (e.g., 'core', 'web', 'api')"
        },
        "context": {
          "type": "string",
          "maxLength": 100,
          "description": "Optional module/component context"
        },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"],
          "default": "medium",
          "description": "Urgency level"
        },
        "status": {
          "type": "string",
          "enum": ["triage", "backlog", "planned", "in-progress", "done", "wontfix"],
          "default": "triage",
          "description": "Current state in lifecycle"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[a-z0-9-]+$",
            "minLength": 1,
            "maxLength": 50
          },
          "uniqueItems": true,
          "description": "Categorization tags (lowercase, hyphens)"
        },
        "notes": {
          "type": "string",
          "description": "Detailed markdown description"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### TypeScript Interface

```typescript
interface CreateDocumentInput {
  project: string;          // Required: project slug
  title?: string;           // Optional: document title
  items: ItemDraft[];       // Required: at least one item
}

interface ItemDraft {
  title: string;            // Required: item title (1-200 chars)
  type: ItemType;           // Required: enhancement|bug|idea|task|question
  domain: string;           // Required: technical domain
  context?: string;         // Optional: module/component
  priority?: Priority;      // Optional: low|medium|high|critical (default: medium)
  status?: Status;          // Optional: triage|backlog|... (default: triage)
  tags?: string[];          // Optional: lowercase, hyphenated tags
  notes?: string;           // Optional: markdown description
}

type ItemType = 'enhancement' | 'bug' | 'idea' | 'task' | 'question';
type Priority = 'low' | 'medium' | 'high' | 'critical';
type Status = 'triage' | 'backlog' | 'planned' | 'in-progress' | 'done' | 'wontfix';
```

### Minimal Valid Example

```json
{
  "project": "meatycapture",
  "items": [
    {
      "title": "Fix tag aggregation bug",
      "type": "bug",
      "domain": "core"
    }
  ]
}
```

### Complete Example

```json
{
  "project": "meatycapture",
  "title": "Security Audit Findings - 2025-12-29",
  "items": [
    {
      "title": "Sanitize user input in project names",
      "type": "bug",
      "domain": "core",
      "context": "validation",
      "priority": "critical",
      "status": "triage",
      "tags": ["security", "input-validation", "injection"],
      "notes": "Problem: Project names not sanitized, allowing path traversal.\n\nGoal: Add strict validation regex and sanitization.\n\nSeverity: Critical - allows arbitrary file access."
    },
    {
      "title": "Add file permission checks before write",
      "type": "enhancement",
      "domain": "adapters",
      "context": "fs-local",
      "priority": "high",
      "status": "backlog",
      "tags": ["security", "file-io", "permissions"],
      "notes": "Goal: Verify write permissions before attempting file operations to prevent privilege escalation."
    }
  ]
}
```

---

## Append Items Schema

Input for `meatycapture log append <doc-path> [items.json] --json`

### Full Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["items"],
  "properties": {
    "items": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/ItemDraft"
      }
    }
  },
  "definitions": {
    "ItemDraft": {
      "type": "object",
      "required": ["title", "type", "domain"],
      "properties": {
        "title": {
          "type": "string",
          "minLength": 1,
          "maxLength": 200
        },
        "type": {
          "type": "string",
          "enum": ["enhancement", "bug", "idea", "task", "question"]
        },
        "domain": {
          "type": "string",
          "pattern": "^[a-z0-9-/]+$",
          "minLength": 1,
          "maxLength": 50
        },
        "context": {
          "type": "string",
          "maxLength": 100
        },
        "priority": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"],
          "default": "medium"
        },
        "status": {
          "type": "string",
          "enum": ["triage", "backlog", "planned", "in-progress", "done", "wontfix"],
          "default": "triage"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[a-z0-9-]+$"
          },
          "uniqueItems": true
        },
        "notes": {
          "type": "string"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

### TypeScript Interface

```typescript
interface AppendItemsInput {
  items: ItemDraft[];  // Required: at least one item (ItemDraft same as create)
}
```

### Example

```json
{
  "items": [
    {
      "title": "Add keyboard shortcuts for wizard",
      "type": "enhancement",
      "domain": "web",
      "context": "wizard",
      "priority": "low",
      "tags": ["ux", "accessibility", "keyboard-nav"]
    }
  ]
}
```

**Note**: Project is inferred from the document path, not specified in JSON.

---

## Response Schemas

### Create Document Response

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success"],
  "properties": {
    "success": {
      "type": "boolean",
      "description": "Whether operation succeeded"
    },
    "doc_id": {
      "type": "string",
      "pattern": "^REQ-\\d{8}-[a-z0-9-]+$",
      "description": "Generated document ID (e.g., 'REQ-20251229-meatycapture')"
    },
    "doc_path": {
      "type": "string",
      "description": "Absolute path to created document"
    },
    "items_created": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_id": {
            "type": "string",
            "pattern": "^REQ-\\d{8}-[a-z0-9-]+-\\d{2}$",
            "description": "Generated item ID (e.g., 'REQ-20251229-meatycapture-01')"
          },
          "title": {
            "type": "string",
            "description": "Item title"
          }
        }
      }
    },
    "warnings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field": {
            "type": "string"
          },
          "message": {
            "type": "string"
          }
        }
      },
      "description": "Non-critical validation warnings"
    },
    "error": {
      "type": "string",
      "description": "Error message if success=false"
    },
    "details": {
      "type": "object",
      "description": "Error details (validation failures, etc.)"
    }
  }
}
```

#### Success Response Example

```json
{
  "success": true,
  "doc_id": "REQ-20251229-meatycapture",
  "doc_path": "/Users/username/.meatycapture/meatycapture/REQ-20251229-meatycapture.md",
  "items_created": [
    {
      "item_id": "REQ-20251229-meatycapture-01",
      "title": "Fix tag aggregation bug"
    },
    {
      "item_id": "REQ-20251229-meatycapture-02",
      "title": "Add keyboard shortcuts"
    }
  ]
}
```

#### Error Response Example

```json
{
  "success": false,
  "error": "Validation failed",
  "details": {
    "field": "type",
    "value": "feature",
    "allowed": ["enhancement", "bug", "idea", "task", "question"],
    "message": "Invalid value 'feature' for field 'type'"
  }
}
```

#### Warning Response Example

```json
{
  "success": true,
  "doc_id": "REQ-20251229-meatycapture",
  "doc_path": "/Users/username/.meatycapture/meatycapture/REQ-20251229-meatycapture.md",
  "items_created": [
    {
      "item_id": "REQ-20251229-meatycapture-01",
      "title": "Custom domain item"
    }
  ],
  "warnings": [
    {
      "field": "domain",
      "message": "Domain 'custom-domain' not in project catalog. Consider adding to fields.json"
    }
  ]
}
```

### Append Items Response

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success"],
  "properties": {
    "success": {
      "type": "boolean"
    },
    "doc_id": {
      "type": "string",
      "pattern": "^REQ-\\d{8}-[a-z0-9-]+$"
    },
    "items_appended": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "item_id": {
            "type": "string",
            "pattern": "^REQ-\\d{8}-[a-z0-9-]+-\\d{2}$"
          },
          "title": {
            "type": "string"
          }
        }
      }
    },
    "updated_metadata": {
      "type": "object",
      "properties": {
        "item_count": {
          "type": "number",
          "description": "Total items after append"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Aggregated tags after append"
        }
      }
    },
    "error": {
      "type": "string"
    },
    "details": {
      "type": "object"
    }
  }
}
```

#### Example

```json
{
  "success": true,
  "doc_id": "REQ-20251229-meatycapture",
  "items_appended": [
    {
      "item_id": "REQ-20251229-meatycapture-03",
      "title": "Performance optimization"
    }
  ],
  "updated_metadata": {
    "item_count": 3,
    "tags": ["bug", "enhancement", "performance", "tags", "ux"]
  }
}
```

### List Documents Response

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success", "docs"],
  "properties": {
    "success": {
      "type": "boolean"
    },
    "docs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "doc_id": {
            "type": "string",
            "pattern": "^REQ-\\d{8}-[a-z0-9-]+$"
          },
          "path": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "item_count": {
            "type": "number"
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "created": {
            "type": "string",
            "format": "date"
          },
          "updated": {
            "type": "string",
            "format": "date"
          }
        }
      }
    },
    "error": {
      "type": "string"
    }
  }
}
```

#### Example

```json
{
  "success": true,
  "docs": [
    {
      "doc_id": "REQ-20251229-meatycapture",
      "path": "/Users/username/.meatycapture/meatycapture/REQ-20251229-meatycapture.md",
      "title": "Security Audit Findings",
      "item_count": 3,
      "tags": ["security", "performance", "ux"],
      "created": "2025-12-29",
      "updated": "2025-12-29"
    },
    {
      "doc_id": "REQ-20251228-meatycapture",
      "path": "/Users/username/.meatycapture/meatycapture/REQ-20251228-meatycapture.md",
      "title": "Request Log - 2025-12-28",
      "item_count": 5,
      "tags": ["bug", "enhancement", "tags"],
      "created": "2025-12-28",
      "updated": "2025-12-28"
    }
  ]
}
```

### Search Documents Response

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success", "matches"],
  "properties": {
    "success": {
      "type": "boolean"
    },
    "query": {
      "type": "string",
      "description": "Search query"
    },
    "matches": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "doc_id": {
            "type": "string"
          },
          "item_id": {
            "type": "string"
          },
          "title": {
            "type": "string"
          },
          "type": {
            "type": "string"
          },
          "domain": {
            "type": "string"
          },
          "status": {
            "type": "string"
          },
          "tags": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "match_context": {
            "type": "string",
            "description": "Snippet showing where query matched"
          }
        }
      }
    },
    "error": {
      "type": "string"
    }
  }
}
```

#### Example

```json
{
  "success": true,
  "query": "tag aggregation",
  "matches": [
    {
      "doc_id": "REQ-20251228-meatycapture",
      "item_id": "REQ-20251228-meatycapture-03",
      "title": "Fix tag aggregation edge case",
      "type": "bug",
      "domain": "core",
      "status": "in-progress",
      "tags": ["tags", "edge-case", "serializer"],
      "match_context": "...Problem: Tag aggregation fails when items array is empty..."
    },
    {
      "doc_id": "REQ-20251229-meatycapture",
      "item_id": "REQ-20251229-meatycapture-02",
      "title": "Optimize tag aggregation performance",
      "type": "enhancement",
      "domain": "core",
      "status": "backlog",
      "tags": ["performance", "tags", "optimization"],
      "match_context": "...Current tag aggregation uses O(n²) algorithm..."
    }
  ]
}
```

### View Document Response

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["success"],
  "properties": {
    "success": {
      "type": "boolean"
    },
    "doc": {
      "type": "object",
      "properties": {
        "doc_id": {
          "type": "string"
        },
        "title": {
          "type": "string"
        },
        "item_count": {
          "type": "number"
        },
        "tags": {
          "type": "array",
          "items": {
            "type": "string"
          }
        },
        "created": {
          "type": "string",
          "format": "date"
        },
        "updated": {
          "type": "string",
          "format": "date"
        },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "item_id": {
                "type": "string"
              },
              "title": {
                "type": "string"
              },
              "type": {
                "type": "string"
              },
              "domain": {
                "type": "string"
              },
              "context": {
                "type": "string"
              },
              "priority": {
                "type": "string"
              },
              "status": {
                "type": "string"
              },
              "tags": {
                "type": "array",
                "items": {
                  "type": "string"
                }
              },
              "notes": {
                "type": "string"
              }
            }
          }
        }
      }
    },
    "error": {
      "type": "string"
    }
  }
}
```

#### Example

```json
{
  "success": true,
  "doc": {
    "doc_id": "REQ-20251229-meatycapture",
    "title": "Security Audit Findings",
    "item_count": 2,
    "tags": ["security", "input-validation", "file-io"],
    "created": "2025-12-29",
    "updated": "2025-12-29",
    "items": [
      {
        "item_id": "REQ-20251229-meatycapture-01",
        "title": "Sanitize user input in project names",
        "type": "bug",
        "domain": "core",
        "context": "validation",
        "priority": "critical",
        "status": "triage",
        "tags": ["security", "input-validation", "injection"],
        "notes": "Problem: Project names not sanitized, allowing path traversal.\n\nGoal: Add strict validation regex and sanitization."
      },
      {
        "item_id": "REQ-20251229-meatycapture-02",
        "title": "Add file permission checks before write",
        "type": "enhancement",
        "domain": "adapters",
        "context": "fs-local",
        "priority": "high",
        "status": "backlog",
        "tags": ["security", "file-io", "permissions"],
        "notes": "Goal: Verify write permissions before file operations."
      }
    ]
  }
}
```

---

## Validation with jq

Validate JSON input before sending to CLI:

### Check Required Fields

```bash
# Validate create input
echo "$JSON_INPUT" | jq -e '.project and .items and (.items | length > 0)' >/dev/null
if [ $? -eq 0 ]; then
  echo "Valid structure"
else
  echo "Missing required fields" >&2
  exit 1
fi

# Validate each item has required fields
echo "$JSON_INPUT" | jq -e '.items[] | .title and .type and .domain' >/dev/null
```

### Validate Enum Values

```bash
# Check type values
INVALID_TYPES=$(echo "$JSON_INPUT" | jq -r '
  .items[] |
  select(.type | IN("enhancement", "bug", "idea", "task", "question") | not) |
  .type
')

if [ -n "$INVALID_TYPES" ]; then
  echo "Invalid type values: $INVALID_TYPES" >&2
  exit 1
fi
```

### Validate String Lengths

```bash
# Check title length
TOO_LONG=$(echo "$JSON_INPUT" | jq -r '
  .items[] |
  select(.title | length > 200) |
  .title
')

if [ -n "$TOO_LONG" ]; then
  echo "Title exceeds 200 characters" >&2
  exit 1
fi
```

### Complete Validation Script

```bash
#!/usr/bin/env bash
# validate-meatycapture-input.sh

set -euo pipefail

JSON_INPUT="$1"

# Required fields
echo "$JSON_INPUT" | jq -e '.project and .items and (.items | length > 0)' >/dev/null || {
  echo "Error: Missing required fields (project, items)" >&2
  exit 1
}

# Each item required fields
echo "$JSON_INPUT" | jq -e '.items[] | .title and .type and .domain' >/dev/null || {
  echo "Error: Items missing required fields (title, type, domain)" >&2
  exit 1
}

# Valid type enum
INVALID_TYPES=$(echo "$JSON_INPUT" | jq -r '.items[] | select(.type | IN("enhancement", "bug", "idea", "task", "question") | not) | .type' || true)
if [ -n "$INVALID_TYPES" ]; then
  echo "Error: Invalid type values: $INVALID_TYPES" >&2
  exit 1
fi

# Valid priority enum (if present)
INVALID_PRIORITY=$(echo "$JSON_INPUT" | jq -r '.items[] | select(.priority) | select(.priority | IN("low", "medium", "high", "critical") | not) | .priority' || true)
if [ -n "$INVALID_PRIORITY" ]; then
  echo "Error: Invalid priority values: $INVALID_PRIORITY" >&2
  exit 1
fi

# Title length
TOO_LONG=$(echo "$JSON_INPUT" | jq -r '.items[] | select(.title | length > 200) | .title' || true)
if [ -n "$TOO_LONG" ]; then
  echo "Error: Title exceeds 200 characters" >&2
  exit 1
fi

echo "Validation passed"
```

---

## Error Codes

| Exit Code | Meaning | Common Causes |
|-----------|---------|---------------|
| 0 | Success | Operation completed successfully |
| 1 | Validation Error | Invalid JSON, missing required fields, enum violations |
| 2 | File I/O Error | Path not writable, document not found, permission denied |
| 3 | Command Error | Unknown command, missing arguments, invalid flags |

### Handling Errors in Scripts

```bash
# Capture and parse error
RESULT=$(echo "$JSON_INPUT" | meatycapture log create --json 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  DOC_ID=$(echo "$RESULT" | jq -r '.doc_id')
  echo "Success: $DOC_ID"
elif [ $EXIT_CODE -eq 1 ]; then
  ERROR=$(echo "$RESULT" | jq -r '.error')
  echo "Validation failed: $ERROR" >&2
elif [ $EXIT_CODE -eq 2 ]; then
  echo "File I/O error" >&2
else
  echo "Unknown error (exit code: $EXIT_CODE)" >&2
fi

exit $EXIT_CODE
```

---

## Reference

- **Main Skill**: `../SKILL.md`
- **Field Options**: `./field-options.md`
- **Templates**: `../templates/`

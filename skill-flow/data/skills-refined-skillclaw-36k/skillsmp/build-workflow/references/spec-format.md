# Workflow Spec JSON Format

## Two Formats

The workflow designer exports one format, but the generator expects another. Use `scripts/transform-spec.py` to convert between them.

### Designer Export Format (Input)

What you get when exporting from the workflow designer UI:

```typescript
interface DesignerSpec {
  metadata: {
    title: string;                 // Workflow title
    description?: string;
    version?: string;
    author?: string;
  };
  nodes: DesignerNode[];
  edges: WorkflowEdge[];
}

interface DesignerNode {
  id: string;
  type: string;                    // May use "loop-container" etc.
  label: string;                   // At root level
  config: Record<string, unknown>; // At root level
  position: { x: number; y: number };
  description?: string;
}
```

### Generator Expected Format (Output)

What the CLI generator expects:

```typescript
interface WorkflowSpec {
  name: string;                    // Workflow name (kebab-case)
  description?: string;
  nodes: WorkflowNode[];
  edges: WorkflowEdge[];
  metadata?: {
    version?: string;
    author?: string;
  };
}

interface WorkflowNode {
  id: string;
  type: NodeType;                  // Must use generator types (e.g., "loop" not "loop-container")
  position: { x: number; y: number };
  data: {                          // Nested data object
    label: string;
    description?: string;
    config: Record<string, unknown>;
  };
}
```

### Key Differences

| Field | Designer | Generator |
|-------|----------|-----------|
| Name | `metadata.title` | `name` (kebab-case) |
| Node label | `node.label` | `node.data.label` |
| Node config | `node.config` | `node.data.config` |
| Loop type | `loop-container` | `loop` |
| Validate with expression | `data-validate` + `expression` | `data-transform` |

**Note:** Designer's `data-validate` with an `expression` is for filtering data (JSONata). Generator's `data-validate` expects a JSON Schema. The transform script converts expression-based validation to `data-transform`.

### Edge Format (Same for Both)

```typescript
interface WorkflowEdge {
  id: string;                      // Unique edge ID
  source: string;                  // Source node ID
  target: string;                  // Target node ID
  sourceHandle?: string;           // For conditions: "true" or "false"
  targetHandle?: string;
  label?: string;
  data?: Record<string, unknown>;
}
```

## Node Types

### Control Nodes

#### `start`
Entry point for the workflow. Every workflow must have exactly one.
```json
{
  "id": "start-1",
  "type": "start",
  "data": { "label": "Start", "config": {} }
}
```

#### `end`
Exit point. Returns the workflow result.
```json
{
  "id": "end-1",
  "type": "end",
  "data": {
    "label": "End",
    "config": {
      "outputPath": "$.result"  // JSONata path to final output
    }
  }
}
```

#### `condition`
Branching logic. Must have two outgoing edges with `sourceHandle: "true"` and `sourceHandle: "false"`.
```json
{
  "id": "condition-1",
  "type": "condition",
  "data": {
    "label": "Check Status",
    "config": {
      "expression": "status = 200",     // JSONata boolean expression
      "trueLabel": "Success",
      "falseLabel": "Failure"
    }
  }
}
```

#### `loop`
Iterates over an array.
```json
{
  "id": "loop-1",
  "type": "loop",
  "data": {
    "label": "Process Items",
    "config": {
      "itemsPath": "$.items",           // JSONata path to array
      "maxIterations": 100              // Safety limit
    }
  }
}
```

### Action Nodes

#### `http-request`
Makes HTTP API calls.
```json
{
  "id": "http-1",
  "type": "http-request",
  "data": {
    "label": "Fetch Data",
    "config": {
      "url": "https://api.example.com/data",
      "method": "GET",                   // GET, POST, PUT, DELETE, PATCH
      "headers": {
        "Authorization": "Bearer ${token}"
      },
      "body": null,                      // For POST/PUT/PATCH
      "timeout": 30000,                  // Milliseconds
      "retries": 3
    }
  }
}
```

#### `ai-generate-text`
Generates unstructured text via AI.
```json
{
  "id": "ai-text-1",
  "type": "ai-generate-text",
  "data": {
    "label": "Generate Summary",
    "config": {
      "prompt": "Summarize: ${content}",
      "systemPrompt": "You are a helpful assistant.",
      "model": "gemini-3-flash-preview", // Optional, defaults to gemini
      "maxTokens": 1000,
      "temperature": 0.7
    }
  }
}
```

#### `ai-generate-object`
Generates structured data via AI.
```json
{
  "id": "ai-obj-1",
  "type": "ai-generate-object",
  "data": {
    "label": "Extract Entities",
    "config": {
      "prompt": "Extract entities from: ${text}",
      "systemPrompt": "Extract structured data.",
      "outputSchema": {
        "type": "object",
        "properties": {
          "entities": {
            "type": "array",
            "items": { "type": "string" }
          }
        },
        "required": ["entities"]
      },
      "model": "gemini-3-flash-preview",
      "temperature": 0.3
    }
  }
}
```

#### `data-transform`
Transforms data using JSONata expressions.
```json
{
  "id": "transform-1",
  "type": "data-transform",
  "data": {
    "label": "Format Output",
    "config": {
      "expression": "{ \"items\": data.results, \"count\": $count(data.results) }",
      "inputPath": "$"                   // Optional path to input data
    }
  }
}
```

#### `data-validate`
Validates data against JSON Schema.
```json
{
  "id": "validate-1",
  "type": "data-validate",
  "data": {
    "label": "Validate Input",
    "config": {
      "schema": {
        "type": "object",
        "properties": {
          "email": { "type": "string", "format": "email" }
        },
        "required": ["email"]
      },
      "inputPath": "$.user"
    }
  }
}
```

#### `human-approval`
Pauses workflow for human decision.
```json
{
  "id": "approval-1",
  "type": "human-approval",
  "data": {
    "label": "Manager Approval",
    "config": {
      "title": "Approve Request",
      "description": "Please review and approve this request.",
      "timeout": "24 hours"             // Duration string
    }
  }
}
```

## Edge Structure

Edges connect nodes in sequence:

```json
{
  "edges": [
    { "id": "e1", "source": "start-1", "target": "http-1" },
    { "id": "e2", "source": "http-1", "target": "condition-1" },
    { "id": "e3", "source": "condition-1", "target": "ai-text-1", "sourceHandle": "true" },
    { "id": "e4", "source": "condition-1", "target": "end-1", "sourceHandle": "false" },
    { "id": "e5", "source": "ai-text-1", "target": "end-1" }
  ]
}
```

## Variable Interpolation

Use `${variableName}` syntax in string configs to reference workflow data:
- `${input.field}` - Access input fields
- `${previousNode.result}` - Access previous node output
- Expressions are evaluated at runtime using JSONata

## Complete Example

```json
{
  "name": "fetch-and-summarize",
  "description": "Fetches data and generates an AI summary",
  "nodes": [
    {
      "id": "start-1",
      "type": "start",
      "position": { "x": 0, "y": 0 },
      "data": { "label": "Start", "config": {} }
    },
    {
      "id": "http-1",
      "type": "http-request",
      "position": { "x": 0, "y": 100 },
      "data": {
        "label": "Fetch Article",
        "config": {
          "url": "${input.articleUrl}",
          "method": "GET",
          "timeout": 30000
        }
      }
    },
    {
      "id": "ai-1",
      "type": "ai-generate-text",
      "position": { "x": 0, "y": 200 },
      "data": {
        "label": "Summarize",
        "config": {
          "prompt": "Summarize this article:\n${http-1.body}",
          "maxTokens": 500
        }
      }
    },
    {
      "id": "end-1",
      "type": "end",
      "position": { "x": 0, "y": 300 },
      "data": { "label": "End", "config": { "outputPath": "$.ai-1.text" } }
    }
  ],
  "edges": [
    { "id": "e1", "source": "start-1", "target": "http-1" },
    { "id": "e2", "source": "http-1", "target": "ai-1" },
    { "id": "e3", "source": "ai-1", "target": "end-1" }
  ]
}
```

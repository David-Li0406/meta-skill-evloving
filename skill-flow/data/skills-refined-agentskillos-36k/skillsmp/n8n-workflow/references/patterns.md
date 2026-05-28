# n8n Workflow Patterns

## Table of Contents
1. [API Polling](#api-polling)
2. [Webhook Handler](#webhook-handler)
3. [LLM Chain with Fallback](#llm-chain-with-fallback)
4. [Database Sync](#database-sync)
5. [Batch Processing](#batch-processing)
6. [Error Handling](#error-handling)
7. [Conditional Branching](#conditional-branching)
8. [Sub-workflow Execution](#sub-workflow-execution)

---

## API Polling

Poll an API on schedule, process new data:

```json
{
  "name": "API Polling",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "name": "Every 5 Minutes",
      "parameters": {
        "rule": { "interval": [{ "field": "minutes", "minutesInterval": 5 }] }
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Fetch API Data",
      "parameters": {
        "url": "https://api.example.com/items",
        "authentication": "predefinedCredentialType"
      }
    },
    {
      "type": "n8n-nodes-base.code",
      "name": "Process Data",
      "parameters": {
        "jsCode": "return $input.all().flatMap(item => item.json.data.map(d => ({ json: d })));"
      }
    }
  ],
  "connections": {
    "Every 5 Minutes": { "main": [[{ "node": "Fetch API Data", "type": "main", "index": 0 }]] },
    "Fetch API Data": { "main": [[{ "node": "Process Data", "type": "main", "index": 0 }]] }
  }
}
```

---

## Webhook Handler

Receive webhook, validate, respond:

```json
{
  "name": "Webhook Handler",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "name": "Receive Webhook",
      "webhookId": "webhook-uuid",
      "parameters": {
        "path": "incoming-data",
        "httpMethod": "POST",
        "responseMode": "responseNode",
        "options": {}
      }
    },
    {
      "type": "n8n-nodes-base.if",
      "name": "Validate Payload",
      "parameters": {
        "conditions": {
          "conditions": [{
            "leftValue": "={{ $json.body.apiKey }}",
            "rightValue": "={{ $env.EXPECTED_API_KEY }}",
            "operator": { "type": "string", "operation": "equals" }
          }]
        }
      }
    },
    {
      "type": "n8n-nodes-base.respondToWebhook",
      "name": "Success Response",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={ \"status\": \"received\", \"id\": \"{{ $json.body.id }}\" }"
      }
    },
    {
      "type": "n8n-nodes-base.respondToWebhook",
      "name": "Error Response",
      "parameters": {
        "respondWith": "json",
        "responseCode": 401,
        "responseBody": "{ \"error\": \"Unauthorized\" }"
      }
    }
  ],
  "connections": {
    "Receive Webhook": { "main": [[{ "node": "Validate Payload", "type": "main", "index": 0 }]] },
    "Validate Payload": {
      "main": [
        [{ "node": "Success Response", "type": "main", "index": 0 }],
        [{ "node": "Error Response", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## LLM Chain with Fallback

Primary model with fallback on failure:

```json
{
  "nodes": [
    {
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "name": "AI Analysis",
      "parameters": {
        "promptType": "define",
        "text": "Analyze this: {{ $json.content }}",
        "options": {}
      },
      "onError": "continueErrorOutput"
    },
    {
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
      "name": "Primary Model",
      "parameters": {
        "model": "anthropic/claude-3.5-sonnet"
      }
    },
    {
      "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
      "name": "Fallback Model",
      "parameters": {
        "model": "google/gemini-2.0-flash-001"
      }
    }
  ],
  "connections": {
    "Primary Model": {
      "ai_languageModel": [[{ "node": "AI Analysis", "type": "ai_languageModel", "index": 0 }]]
    },
    "Fallback Model": {
      "ai_languageModel": [[{ "node": "AI Analysis", "type": "ai_languageModel", "index": 1 }]]
    }
  }
}
```

---

## Database Sync

Fetch, transform, upsert to database:

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "name": "Daily Sync",
      "parameters": {
        "rule": { "interval": [{ "triggerAtHour": 2 }] }
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Fetch Source Data",
      "parameters": { "url": "https://api.source.com/data" }
    },
    {
      "type": "n8n-nodes-base.code",
      "name": "Transform Data",
      "parameters": {
        "jsCode": "return $input.all().map(item => ({\n  json: {\n    id: item.json.source_id,\n    name: item.json.title,\n    updated_at: new Date().toISOString()\n  }\n}));"
      }
    },
    {
      "type": "n8n-nodes-base.supabase",
      "name": "Upsert Records",
      "parameters": {
        "operation": "upsert",
        "tableId": "synced_data",
        "fieldsUi": {
          "fieldValues": [
            { "fieldId": "id", "fieldValue": "={{ $json.id }}" },
            { "fieldId": "name", "fieldValue": "={{ $json.name }}" },
            { "fieldId": "updated_at", "fieldValue": "={{ $json.updated_at }}" }
          ]
        }
      }
    }
  ]
}
```

---

## Batch Processing

Process large datasets in batches:

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.splitInBatches",
      "name": "Loop Over Items",
      "parameters": {
        "batchSize": 10,
        "options": { "reset": false }
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "name": "Process Batch",
      "parameters": {
        "method": "POST",
        "url": "https://api.example.com/batch",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [{ "name": "items", "value": "={{ $json }}" }]
        }
      }
    },
    {
      "type": "n8n-nodes-base.wait",
      "name": "Rate Limit Delay",
      "parameters": {
        "resume": "timeInterval",
        "amount": 1,
        "unit": "seconds"
      }
    }
  ],
  "connections": {
    "Loop Over Items": {
      "main": [
        [{ "node": "Aggregate Results", "type": "main", "index": 0 }],
        [{ "node": "Process Batch", "type": "main", "index": 0 }]
      ]
    },
    "Process Batch": { "main": [[{ "node": "Rate Limit Delay", "type": "main", "index": 0 }]] },
    "Rate Limit Delay": { "main": [[{ "node": "Loop Over Items", "type": "main", "index": 0 }]] }
  }
}
```

**Note:** Loop Over Items has two outputs:
- Index 0: Loop complete (all items processed)
- Index 1: Current batch to process

---

## Error Handling

Catch errors and notify:

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.errorTrigger",
      "name": "On Error",
      "parameters": {}
    },
    {
      "type": "n8n-nodes-base.slack",
      "name": "Notify Slack",
      "parameters": {
        "channel": "#alerts",
        "text": "Workflow failed: {{ $json.workflow.name }}\nError: {{ $json.execution.error.message }}"
      }
    }
  ]
}
```

**Per-node error handling:**
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "name": "API Call",
  "onError": "continueRegularOutput",
  "retryOnFail": true,
  "maxTries": 3
}
```

**Error output modes:**
- `stopWorkflow` - Default, stops execution
- `continueRegularOutput` - Continue with empty output
- `continueErrorOutput` - Route to error branch (second output)

---

## Conditional Branching

Route data based on conditions:

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.switch",
      "name": "Route by Type",
      "parameters": {
        "mode": "rules",
        "rules": {
          "values": [
            {
              "outputKey": "Order",
              "conditions": {
                "conditions": [{
                  "leftValue": "={{ $json.type }}",
                  "rightValue": "order",
                  "operator": { "type": "string", "operation": "equals" }
                }]
              }
            },
            {
              "outputKey": "Refund",
              "conditions": {
                "conditions": [{
                  "leftValue": "={{ $json.type }}",
                  "rightValue": "refund",
                  "operator": { "type": "string", "operation": "equals" }
                }]
              }
            }
          ]
        },
        "fallbackOutput": "extra"
      }
    }
  ],
  "connections": {
    "Route by Type": {
      "main": [
        [{ "node": "Process Order", "type": "main", "index": 0 }],
        [{ "node": "Process Refund", "type": "main", "index": 0 }],
        [{ "node": "Handle Unknown", "type": "main", "index": 0 }]
      ]
    }
  }
}
```

---

## Sub-workflow Execution

Call another workflow:

```json
{
  "nodes": [
    {
      "type": "n8n-nodes-base.executeWorkflow",
      "name": "Call Sub-workflow",
      "parameters": {
        "source": "database",
        "workflowId": "workflow-uuid",
        "mode": "each"
      }
    }
  ]
}
```

**In the sub-workflow (trigger):**
```json
{
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "name": "Workflow Called",
  "parameters": {}
}
```

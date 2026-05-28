# n8n Nodes Reference

## Table of Contents
1. [Trigger Nodes](#trigger-nodes)
2. [Core Action Nodes](#core-action-nodes)
3. [Flow Control Nodes](#flow-control-nodes)
4. [Data Manipulation Nodes](#data-manipulation-nodes)
5. [AI/LangChain Nodes](#ailangchain-nodes)

---

## Trigger Nodes

### Manual Trigger
```json
{
  "type": "n8n-nodes-base.manualTrigger",
  "typeVersion": 1,
  "position": [0, 0],
  "id": "manual-1",
  "name": "Manual Trigger",
  "parameters": {}
}
```

### Schedule Trigger
```json
{
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.2,
  "parameters": {
    "rule": {
      "interval": [{ "triggerAtHour": 9 }]
    }
  }
}
```

**Cron expression:**
```json
"parameters": {
  "rule": {
    "interval": [{
      "field": "cronExpression",
      "expression": "0 9 * * 1-5"
    }]
  }
}
```

### Webhook Trigger
```json
{
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "webhookId": "unique-webhook-id",
  "parameters": {
    "path": "my-endpoint",
    "httpMethod": "POST",
    "responseMode": "onReceived",
    "options": {}
  }
}
```

### Chat Trigger (AI)
```json
{
  "type": "@n8n/n8n-nodes-langchain.chatTrigger",
  "typeVersion": 1.1,
  "parameters": {
    "options": {}
  }
}
```

---

## Core Action Nodes

### HTTP Request
```json
{
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "parameters": {
    "method": "GET",
    "url": "https://api.example.com/data",
    "authentication": "none",
    "options": {}
  }
}
```

**With headers and body:**
```json
"parameters": {
  "method": "POST",
  "url": "https://api.example.com/data",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      { "name": "Authorization", "value": "Bearer {{ $json.token }}" }
    ]
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      { "name": "data", "value": "={{ $json }}" }
    ]
  }
}
```

### Code Node (JavaScript)
```json
{
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "parameters": {
    "jsCode": "const items = $input.all();\n\nconst processed = items.map(item => {\n  return {\n    json: {\n      ...item.json,\n      timestamp: new Date().toISOString()\n    }\n  };\n});\n\nreturn processed;"
  }
}
```

### Code Node (Python)
```json
{
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "parameters": {
    "mode": "runOnceForAllItems",
    "language": "python",
    "pythonCode": "items = _input.all()\nfor item in items:\n    item.json['processed'] = True\nreturn items"
  }
}
```

### Set Node
```json
{
  "type": "n8n-nodes-base.set",
  "typeVersion": 3.4,
  "parameters": {
    "mode": "raw",
    "jsonOutput": "={ \"field\": \"{{ $json.value }}\", \"static\": \"value\" }",
    "options": {}
  }
}
```

**Manual field assignment:**
```json
"parameters": {
  "mode": "manual",
  "fields": {
    "values": [
      { "name": "newField", "stringValue": "={{ $json.existingField }}" }
    ]
  }
}
```

---

## Flow Control Nodes

### IF Node
```json
{
  "type": "n8n-nodes-base.if",
  "typeVersion": 2.2,
  "parameters": {
    "conditions": {
      "options": { "caseSensitive": true, "typeValidation": "strict" },
      "conditions": [{
        "id": "condition-uuid",
        "leftValue": "={{ $json.status }}",
        "rightValue": "active",
        "operator": { "type": "string", "operation": "equals" }
      }],
      "combinator": "and"
    }
  }
}
```

**Operators:**
- String: `equals`, `notEquals`, `contains`, `startsWith`, `endsWith`, `regex`
- Number: `equals`, `gt`, `gte`, `lt`, `lte`
- Boolean: `true`, `false`
- Array: `contains`, `lengthEquals`, `lengthGt`, `lengthLt`

### Switch Node
```json
{
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3.2,
  "parameters": {
    "mode": "rules",
    "rules": {
      "values": [
        { "outputKey": "High", "conditions": { "conditions": [{ "leftValue": "={{ $json.priority }}", "rightValue": "high", "operator": { "type": "string", "operation": "equals" } }] } },
        { "outputKey": "Low", "conditions": { "conditions": [{ "leftValue": "={{ $json.priority }}", "rightValue": "low", "operator": { "type": "string", "operation": "equals" } }] } }
      ]
    }
  }
}
```

### Merge Node
```json
{
  "type": "n8n-nodes-base.merge",
  "typeVersion": 3.2,
  "parameters": {
    "mode": "chooseBranch",
    "useDataOfInput": 2
  }
}
```

**Modes:**
- `chooseBranch` - Wait for all inputs, output one branch
- `append` - Combine all items from inputs
- `combine` - Match items between inputs
- `multiplex` - All combinations of items

### Loop Over Items
```json
{
  "type": "n8n-nodes-base.splitInBatches",
  "typeVersion": 3,
  "parameters": {
    "batchSize": 1,
    "options": { "reset": false }
  }
}
```

### Wait Node
```json
{
  "type": "n8n-nodes-base.wait",
  "typeVersion": 1.1,
  "parameters": {
    "resume": "timeInterval",
    "amount": 5,
    "unit": "seconds"
  }
}
```

---

## Data Manipulation Nodes

### Remove Duplicates
```json
{
  "type": "n8n-nodes-base.removeDuplicates",
  "typeVersion": 2,
  "parameters": {
    "compare": "selectedFields",
    "fieldsToCompare": "id,email"
  }
}
```

### Filter
```json
{
  "type": "n8n-nodes-base.filter",
  "typeVersion": 2,
  "parameters": {
    "conditions": {
      "conditions": [{
        "leftValue": "={{ $json.active }}",
        "rightValue": true,
        "operator": { "type": "boolean", "operation": "true" }
      }]
    }
  }
}
```

### Sort
```json
{
  "type": "n8n-nodes-base.sort",
  "typeVersion": 1,
  "parameters": {
    "sortFieldsUi": {
      "sortField": [{ "fieldName": "createdAt", "order": "descending" }]
    }
  }
}
```

### Limit
```json
{
  "type": "n8n-nodes-base.limit",
  "typeVersion": 1,
  "parameters": { "maxItems": 10 }
}
```

### Aggregate
```json
{
  "type": "n8n-nodes-base.aggregate",
  "typeVersion": 1,
  "parameters": {
    "aggregate": "aggregateAllItemData",
    "destinationFieldName": "allData"
  }
}
```

---

## AI/LangChain Nodes

### Basic LLM Chain
```json
{
  "type": "@n8n/n8n-nodes-langchain.chainLlm",
  "typeVersion": 1.7,
  "parameters": {
    "promptType": "define",
    "text": "={{ $json.prompt }}",
    "options": {}
  }
}
```

### Chat Model (OpenRouter)
```json
{
  "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
  "typeVersion": 1,
  "parameters": {
    "model": "anthropic/claude-3.5-sonnet",
    "options": { "responseFormat": "json_object" }
  },
  "credentials": {
    "openRouterApi": { "id": "cred-id", "name": "OpenRouter" }
  }
}
```

**AI node connections use special types:**
```json
"AI Chain": {
  "ai_languageModel": [[
    { "node": "Chat Model", "type": "ai_languageModel", "index": 0 }
  ]]
}
```

### AI Agent
```json
{
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 1.7,
  "parameters": {
    "promptType": "define",
    "text": "You are a helpful assistant.",
    "options": { "systemMessage": "Be concise." }
  }
}
```

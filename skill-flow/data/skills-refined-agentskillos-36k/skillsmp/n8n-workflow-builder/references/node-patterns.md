# Node Patterns

Advanced configuration patterns for common n8n nodes.

## Contents

1. [Webhook Patterns](#webhook-patterns)
2. [Code Node Patterns](#code-node-patterns)
3. [HTTP Request Patterns](#http-request-patterns)
4. [Merge Node Patterns](#merge-node-patterns)
5. [Error Handling Patterns](#error-handling-patterns)

---

## Webhook Patterns

### Basic Webhook with Response

```javascript
{
  "name": "Webhook",
  "type": "n8n-nodes-base.webhook",
  "typeVersion": 2,
  "parameters": {
    "httpMethod": "POST",
    "path": "my-endpoint",
    "responseMode": "responseNode",
    "options": {}
  },
  "webhookId": "unique-id-here"
}
```

### Webhook Response Node

```javascript
{
  "name": "Respond",
  "type": "n8n-nodes-base.respondToWebhook",
  "typeVersion": 1,
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ { success: true, data: $json } }}"
  }
}
```

### Webhook with Error Response

```javascript
{
  "parameters": {
    "respondWith": "json",
    "responseBody": "={{ $json.error ? { success: false, error: $json.error } : { success: true, data: $json.result } }}",
    "options": {
      "responseCode": "={{ $json.error ? 400 : 200 }}"
    }
  }
}
```

---

## Code Node Patterns

### Basic Data Transformation

```javascript
const items = $input.all();

return items.map(item => ({
  json: {
    ...item.json,
    processed: true,
    timestamp: new Date().toISOString()
  }
}));
```

### HTTP Request with Error Handling

```javascript
try {
  const response = await this.helpers.httpRequest({
    method: 'POST',
    url: 'https://api.example.com/endpoint',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${$env.API_KEY}`
    },
    body: $input.first().json,
    timeout: 30000
  });

  return [{ json: { success: true, data: response } }];
} catch (error) {
  return [{ json: { success: false, error: error.message } }];
}
```

### Access Upstream Node Data

```javascript
// Get data from specific node
const configData = $('Config Builder').first().json;
const webhookData = $('Webhook').first().json;

// Get all items from a node
const allItems = $('Split Items').all();

// Safely access with fallback
const value = $('Optional Node').first()?.json?.field || 'default';
```

### Conditional Routing Output

```javascript
const data = $input.first().json;

// Return to different outputs based on condition
if (data.priority === 'high') {
  return [[{ json: data }], []];  // Output 0
} else {
  return [[], [{ json: data }]];  // Output 1
}
```

---

## HTTP Request Patterns

### With Retry Logic

```javascript
{
  "name": "API Call",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4,
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/endpoint",
    "options": {
      "timeout": 30000,
      "retry": {
        "maxRetries": 3,
        "retryInterval": 1000
      }
    }
  },
  "onError": "continueRegularOutput"
}
```

---

## Merge Node Patterns

### Wait for All Parallel Branches

```javascript
{
  "name": "Merge Results",
  "type": "n8n-nodes-base.merge",
  "typeVersion": 3,
  "parameters": {
    "mode": "append",
    "numberInputs": 3
  }
}
```

### Left Join (Enrich Input 1)

```javascript
{
  "parameters": {
    "mode": "combine",
    "combineBy": "combineByFields",
    "fields": ["id"],
    "joinMode": "enrichInput1",
    "outputDataFrom": "both"
  }
}
```

---

## Error Handling Patterns

### Continue on Error with Flag

```javascript
{
  "name": "Risky Operation",
  "type": "n8n-nodes-base.httpRequest",
  "onError": "continueRegularOutput",
  "parameters": { ... }
}

// Next node: Check for error
{
  "type": "n8n-nodes-base.if",
  "parameters": {
    "conditions": {
      "conditions": [{
        "leftValue": "={{ $json.error }}",
        "rightValue": "",
        "operator": { "type": "string", "operation": "notEmpty" }
      }]
    }
  }
}
```

### Error Output Branch

```javascript
{
  "name": "API Call",
  "type": "n8n-nodes-base.httpRequest",
  "onError": "continueErrorOutput",
  "parameters": { ... }
}
// Output 0 → Success path
// Output 1 (error) → Error handling path
```

---

## Performance Patterns

### Batch Processing

```javascript
const items = $input.first().json.items;
const batchSize = 100;
const batches = [];

for (let i = 0; i < items.length; i += batchSize) {
  batches.push({
    json: {
      batch: Math.floor(i / batchSize) + 1,
      items: items.slice(i, i + batchSize)
    }
  });
}

return batches;
```

### Rate Limiting

```javascript
{
  "type": "n8n-nodes-base.wait",
  "parameters": {
    "amount": 1,
    "unit": "seconds"
  }
}
// Place between API calls to avoid rate limits
```

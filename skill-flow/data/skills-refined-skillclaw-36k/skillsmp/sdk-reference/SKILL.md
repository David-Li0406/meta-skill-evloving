---
name: sdk-reference
description: Definitive API reference for the TypeScript SDK (@simpleplatform/sdk).
---
# SDK Reference Skill

Complete API reference for the TypeScript SDK (`@simpleplatform/sdk`), designed for use within Simple Platform **Actions** (WASM modules).

## 1. Core Concepts

### Entry Point (`simple.Handle`)
Every Action must export a handler using `simple.Handle`.

```typescript
import simple, { type Request } from '@simpleplatform/sdk'

simple.Handle(async (request: Request) => {
  const input = request.parse<{ name: string }>()
  return { message: `Hello, ${input.name}!` }
})
```

### Request Object
*   `parse<T>()`: Returns typed input payload (JSON).
*   `data()`: Returns raw input string.
*   `context`: **CRITICAL**. Usage: `request.context`. Must be passed to all SDK functions.
*   `headers`: HTTP headers (if applicable).

### Context (`Context`)
Carries security tokens (Tenant, User, Logic ID). You pass this to every SDK function (DB, AI, Storage) to authorize the call.

---

## 2. Data Access (`@simpleplatform/sdk/graphql`)

Reading and writing database records via GraphQL.

```typescript
import { query, mutate } from '@simpleplatform/sdk/graphql'
```

### Query (Read)
```typescript
const data = await query<{ orders: Order[] }>(
  `query GetOrders($status: String!) {
    orders: com_my_app__orders(where: { status: { _eq: $status } }) {
      id
      total
    }
  }`,
  { status: 'valid' }, // Variables
  request.context      // Context
)
```

### Mutate (Write)
```typescript
const result = await mutate<{ insert_order: { id: string } }>(
  `mutation Create($data: JSON!) {
    insert_order: insert_com_my_app__order(object: $data) {
      id
    }
  }`,
  { data: { total: 100 } },
  request.context
)
```

---

## 3. File Storage (`@simpleplatform/sdk/storage`)

Importing files for use in records (`:document` fields) or AI processing.

### `uploadExternal`
Uploads a file from a URL. Returns a `DocumentHandle`.

```typescript
import { uploadExternal } from '@simpleplatform/sdk/storage'

const invoiceHandle = await uploadExternal(
  {
    url: 'https://example.com/invoice.pdf',
    auth: { type: 'bearer', bearer_token: '...' } // Optional
  },
  {
    app_id: 'com.mycompany.myapp',
    table_name: 'invoices',
    field_name: 'attachment'
  },
  request.context
)

// Result (DocumentHandle):
// { file_hash: "...", mime_type: "application/pdf", ... }
```

**Usage:** Save this handle to a `:document` field in your database.

---

## 4. Artificial Intelligence (`@simpleplatform/sdk/ai`)

Extract, Summarize, and Transcribe using the host platform's LLM mesh.

```typescript
import { extract, summarize, transcribe } from '@simpleplatform/sdk/ai'
```

### `extract` (Structured Data)
Convert text or files (PDF/Image) into JSON.

```typescript
const userDetails = await extract(
  "My name is Alice and I am 30 years old.", // OR DocumentHandle
  {
    prompt: "Extract user details",
    model: "medium", // lite, medium, large, xl
    schema: {
      type: "object",
      properties: {
        name: { type: "string" },
        age: { type: "number" }
      },
      required: ["name"]
    }
  },
  request.context
)
// userDetails.data.name === "Alice"
```

### `summarize`
Generate a concise summary.

```typescript
const summary = await summarize(
  invoiceHandle, // DocumentHandle
  { prompt: "Summarize line items" },
  request.context
)
```

### `transcribe`
Audio/Video to Text.

```typescript
const transcript = await transcribe(
  callRecordingHandle,
  { includeTimestamps: true, participants: ['Agent', 'Customer'] },
  request.context
)
```

---

## 5. Utilities

### HTTP Requests (`@simpleplatform/sdk/http`)
Securely call external APIs.

```typescript
import { get, post, fetch } from '@simpleplatform/sdk/http'

await post('https://api.slack.com/webhook', { text: 'Hello' }, {}, request.context)

// Advanced
await fetch({
  url: '...',
  method: 'PUT',
  body: { ... },
  headers: { ... }
}, request.context)
```

### Settings (`@simpleplatform/sdk/settings`)
Access App Configuration.

```typescript
import { get } from '@simpleplatform/sdk/settings'

const config = await get('com.my_app', ['api_key'], request.context)
const key = config['api_key']
```

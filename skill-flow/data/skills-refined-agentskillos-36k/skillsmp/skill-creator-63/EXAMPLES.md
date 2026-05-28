# Examples

This file is an example placeholder referenced by the Skill Creator skill.

## Example: API Client Usage

```ts
import { Client } from "./client";

const client = new Client({ baseUrl: "https://api.example.com" });

async function demo() {
  const result = await client.users.list({ page: 1, pageSize: 50 });
  console.log(result.items.length);
}
```

## Example: Error Handling

```ts
try {
  await client.orders.create({ /* ... */ });
} catch (error) {
  // Handle retryable vs non-retryable errors
}
```

## Example: Pagination Pattern

```ts
let page = 1;
while (true) {
  const res = await client.users.list({ page, pageSize: 100 });
  if (res.items.length === 0) break;
  // process items
  page += 1;
}
```

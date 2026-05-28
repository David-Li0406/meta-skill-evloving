---
name: openapi-to-typescript
description: Use this skill when you need to convert OpenAPI 3.0 JSON/YAML specifications into TypeScript interfaces and type guards.
---

# OpenAPI to TypeScript

Converts OpenAPI 3.0 specifications to TypeScript interfaces and type guards.

**Input:** OpenAPI file (JSON or YAML)  
**Output:** TypeScript file with interfaces and type guards

## When to Use

- "generate types from OpenAPI"
- "convert OpenAPI to TypeScript"
- "create API interfaces"
- "generate TypeScript types from an API specification"

## Workflow

1. Request the OpenAPI file path (if not provided).
2. Read and validate the file (must be OpenAPI 3.0.x).
3. Extract schemas from `components/schemas`.
4. Extract endpoints from `paths` (request/response types).
5. Generate TypeScript (interfaces + type guards).
6. Ask where to save (default: `types/api.ts` in the current directory).
7. Write the file.

## OpenAPI Validation

Check before processing:

```
- Field "openapi" must exist and start with "3.0"
- Field "paths" must exist
- Field "components.schemas" must exist (if there are types)
```

If invalid, report the error and stop.

## Type Mapping

### Primitives

| OpenAPI     | TypeScript   |
|-------------|--------------|
| `string`    | `string`     |
| `number`    | `number`     |
| `integer`   | `number`     |
| `boolean`   | `boolean`    |
| `null`      | `null`       |

### Format Modifiers

| Format        | TypeScript              |
|---------------|-------------------------|
| `uuid`        | `string` (comment UUID) |
| `date`        | `string` (comment date) |
| `date-time`   | `string` (comment ISO)  |
| `email`       | `string` (comment email)|
| `uri`         | `string` (comment URI)  |

### Complex Types

**Object:**
```typescript
// OpenAPI: type: object, properties: {id, name}, required: [id]
interface Example {
  id: string;      // required: no ?
  name?: string;   // optional: with ?
}
```

**Array:**
```typescript
// OpenAPI: type: array, items: {type: string}
type Names = string[];
```

**Enum:**
```typescript
// OpenAPI: type: string, enum: [active, draft]
type Status = "active" | "draft";
```

**oneOf (Union):**
```typescript
// OpenAPI: oneOf: [{$ref: Cat}, {$ref: Dog}]
type Pet = Cat | Dog;
```

**allOf (Intersection/Extends):**
```typescript
// OpenAPI: allOf: [{$ref: Base}, {type: object, properties: ...}]
interface Extended extends Base {
```
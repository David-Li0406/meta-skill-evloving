---
name: openapi
description: >
  OpenAPI 3.1 specification patterns. Use when defining API schemas,
  operations, or documentation.
  Triggers: openapi.go, OpenAPI, Spec.*, openapi.Operation, openapi.Schema,
  openapi.Response, RequestBodyJSON, ResponseJSON, ResponseRef, SchemaRef,
  Schemas(), /docs endpoint, Scalar UI.
  File patterns: internal/*/openapi.go, pkg/openapi/*.go, cmd/server/openapi.go
---

# OpenAPI Patterns

## When This Skill Applies

- Defining API schemas for new domains
- Adding OpenAPI metadata to routes
- Creating request/response types
- Working with Scalar UI documentation
- Adding shared components

## OpenAPI 3.1 Alignment

OpenAPI 3.1 aligns with JSON Schema Draft 2020-12. Schema Objects are used everywhere - properties within an object schema are themselves Schema Objects.

### Schema Object Fields

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | Data type (string, number, integer, boolean, array, object) |
| `format` | string | Extended format (uuid, date-time, int64, binary, etc.) |
| `description` | string | Human-readable description |
| `properties` | map[string]*Schema | Object properties (each is a Schema) |
| `required` | []string | Required property names |
| `items` | *Schema | Array item schema |
| `$ref` | string | JSON Reference to another schema |
| `example` | any | Example value |
| `default` | any | Default value |
| `enum` | []any | Enumerated values |
| `minimum/maximum` | *float64 | Numeric constraints |
| `minLength/maxLength` | *int | String length constraints |
| `pattern` | string | Regex pattern for strings |

## Principles

### 1. Schema Ownership

**Infrastructure** (`pkg/openapi/components.go`):
- Shared responses: `BadRequest`, `NotFound`, `Conflict`
- Shared schemas: `PageRequest`

**Domains** (`internal/<domain>/openapi.go`):
- Domain-specific schemas
- Operation definitions

### 2. Domain OpenAPI File Structure

```go
// internal/providers/openapi.go
package providers

import "github.com/JaimeStill/agent-lab/pkg/openapi"

var Spec = spec{
    Create: &openapi.Operation{
        Summary:     "Create provider",
        Description: "Validates and stores a new provider configuration",
        RequestBody: openapi.RequestBodyJSON("CreateProviderCommand", true),
        Responses: map[int]*openapi.Response{
            201: openapi.ResponseJSON("Provider created", "Provider"),
            400: openapi.ResponseRef("BadRequest"),
            409: openapi.ResponseRef("Conflict"),
        },
    },
    List: &openapi.Operation{
        Summary:     "List providers",
        Description: "Returns paginated list of providers",
        Parameters: []openapi.Parameter{
            openapi.QueryParam("page", "integer", "Page number", false),
            openapi.QueryParam("page_size", "integer", "Items per page", false),
            openapi.QueryParam("search", "string", "Search term", false),
        },
        Responses: map[int]*openapi.Response{
            200: openapi.ResponseJSON("Providers list", "ProviderPageResult"),
        },
    },
    Find: &openapi.Operation{
        Summary: "Get provider by ID",
        Parameters: []openapi.Parameter{
            openapi.PathParam("id", "Provider UUID"),
        },
        Responses: map[int]*openapi.Response{
            200: openapi.ResponseJSON("Provider details", "Provider"),
            404: openapi.ResponseRef("NotFound"),
        },
    },
}

type spec struct {
    Create *openapi.Operation
    List   *openapi.Operation
    Find   *openapi.Operation
    Update *openapi.Operation
    Delete *openapi.Operation
}

func (spec) Schemas() map[string]*openapi.Schema {
    return map[string]*openapi.Schema{
        "Provider": {
            Type: "object",
            Properties: map[string]*openapi.Schema{
                "id":         {Type: "string", Format: "uuid"},
                "name":       {Type: "string"},
                "config":     {Type: "object"},
                "created_at": {Type: "string", Format: "date-time"},
                "updated_at": {Type: "string", Format: "date-time"},
            },
        },
        "CreateProviderCommand": {
            Type:     "object",
            Required: []string{"name", "config"},
            Properties: map[string]*openapi.Schema{
                "name":   {Type: "string"},
                "config": {Type: "object"},
            },
        },
        "ProviderPageResult": {
            Type: "object",
            Properties: map[string]*openapi.Schema{
                "data":        {Type: "array", Items: openapi.SchemaRef("Provider")},
                "total":       {Type: "integer"},
                "page":        {Type: "integer"},
                "page_size":   {Type: "integer"},
                "total_pages": {Type: "integer"},
            },
        },
    }
}
```

### 3. Route Integration

Routes reference domain operations:

```go
func (h *Handler) Routes() routes.Group {
    return routes.Group{
        Prefix:      "/providers",  // API module adds /api prefix
        Tags:        []string{"Providers"},
        Description: "Provider configuration management",
        Routes: []routes.Route{
            {Method: "POST", Pattern: "", Handler: h.Create, OpenAPI: Spec.Create},
            {Method: "GET", Pattern: "", Handler: h.List, OpenAPI: Spec.List},
            {Method: "GET", Pattern: "/{id}", Handler: h.Find, OpenAPI: Spec.Find},
            {Method: "PUT", Pattern: "/{id}", Handler: h.Update, OpenAPI: Spec.Update},
            {Method: "DELETE", Pattern: "/{id}", Handler: h.Delete, OpenAPI: Spec.Delete},
        },
    }
}
```

### 4. Helper Functions

```go
// Reference to component schema
openapi.SchemaRef("Provider")  // "#/components/schemas/Provider"

// Reference to component response
openapi.ResponseRef("NotFound")  // "#/components/responses/NotFound"

// JSON request body
openapi.RequestBodyJSON("CreateProviderCommand", true)

// JSON response
openapi.ResponseJSON("Provider created", "Provider")

// Path parameter (always type string with uuid format)
openapi.PathParam("id", "Provider UUID")

// Query parameter
openapi.QueryParam("page", "integer", "Page number", false)
```

### 5. Generation Flow

1. Server startup calls `registerRoutes()`
2. Domain handlers registered with optional `OpenAPI` metadata on routes
3. `loadOrGenerateSpec()` generates spec in memory from route metadata
4. Compares with existing file, writes only if changed
5. Spec served from memory at `/api/openapi.json`

### 6. Environment-Specific Specs

- Output location: `web/scalar/openapi.{env}.json`
- Environment determined by `SERVICE_ENV` (default: `local`)
- Example: `web/scalar/openapi.local.json`, `web/scalar/openapi.prod.json`

## Patterns

### Schema Registration

Schemas are registered during API module initialization:

```go
// In cmd/server/modules.go or similar
components.AddSchemas(providers.Spec.Schemas())
components.AddSchemas(agents.Spec.Schemas())
```

### Multipart File Upload Schema

```go
RequestBody: &openapi.RequestBody{
    Required: true,
    Content: map[string]*openapi.MediaType{
        "multipart/form-data": {
            Schema: &openapi.Schema{
                Type: "object",
                Properties: map[string]*openapi.Schema{
                    "file": {Type: "string", Description: "File to upload"},
                    "name": {Type: "string"},
                },
                Required: []string{"file"},
            },
        },
    },
}
```

**Important**: For binary file upload fields, only use `Type` and `Description`. Do NOT include `Format: "binary"` - this causes Scalar UI to display "BINARY" as a placeholder instead of rendering a file upload button.

HTTP multipart naturally supports multiple same-named fields for multi-file uploads.

### PageResult Schema

```go
"ProviderPageResult": {
    Type: "object",
    Properties: map[string]*openapi.Schema{
        "data":        {Type: "array", Items: openapi.SchemaRef("Provider")},
        "total":       {Type: "integer"},
        "page":        {Type: "integer"},
        "page_size":   {Type: "integer"},
        "total_pages": {Type: "integer"},
    },
}
```

### Inline vs Referenced Schemas

Use **references** for:
- Reusable domain entities (Resource, CreateCommand)
- Shared response schemas
- Pagination results

Use **inline schemas** for:
- Multipart form definitions (specific to single endpoint)
- Simple one-off response structures

## Validation Checklist

After API changes:

1. Start server - spec auto-generates to `web/scalar/openapi.{env}.json`
2. Visit `/scalar/` to verify Scalar UI renders correctly
3. Test "Try It" functionality for new endpoints
4. Verify schema references resolve correctly

## Import Hierarchy

```
pkg/openapi          - Types and helpers only (no internal imports)
internal/<domain>    - Domain-owned schemas and operations
cmd/server           - Generator logic (imports pkg and internal)
web/scalar           - Scalar UI module
```

## Anti-Patterns

### Inline Schema Definitions

```go
// Bad: Schema defined inline in operation
Responses: map[int]*openapi.Response{
    200: {
        Description: "Provider",
        Content: map[string]*openapi.MediaType{
            "application/json": {
                Schema: &openapi.Schema{Type: "object", ...},  // Inline
            },
        },
    },
}

// Good: Reference component schema
Responses: map[int]*openapi.Response{
    200: openapi.ResponseJSON("Provider details", "Provider"),
}
```

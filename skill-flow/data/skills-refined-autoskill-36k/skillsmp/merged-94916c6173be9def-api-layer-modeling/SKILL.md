---
name: api-layer-modeling
description: Use this skill when defining REST API contracts using OpenAPI 3.0, specifying endpoints, operations, request/response schemas, and security requirements.
---

# API Layer Skill

**Layer Number:** 06  
**Specification:** Metadata Model Spec v0.7.0  
**Purpose:** Defines REST API contracts using OpenAPI 3.0, specifying endpoints, operations, request/response schemas, and security requirements.

---

## Layer Overview

The API Layer captures **API contracts**:

- **OPERATIONS** - HTTP methods on paths (GET, POST, PUT, DELETE, PATCH)
- **SCHEMAS** - Request/response data structures
- **SECURITY** - Authentication and authorization schemes
- **DOCUMENTATION** - API metadata, descriptions, examples
- **INTEGRATION** - Links to business services, application services, data models

This layer uses **OpenAPI 3.0.3** (de facto industry standard) with custom extensions for cross-layer traceability.

**Central Entity:** The **Operation** (HTTP method on a path) is the core modeling unit.

---

## Entity Types

### Core OpenAPI Entities (13 entities)

| Entity Type         | Description                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------- |
| **OpenAPIDocument** | Root of an OpenAPI specification file (version 3.0.3)                                       |
| **Info**            | Metadata about the API (title, description, version, contact, license)                      |
| **Server**          | Server where the API is available (with URL and variables)                                  |
| **Paths**           | Available API endpoints and operations                                                      |
| **PathItem**        | Operations available on a path                                                              |
| **Operation**       | Single API operation (HTTP method on a path) - **CENTRAL ENTITY**                           |
| **Parameter**       | Parameter for an operation (locations: query, header, path, cookie)                         |
| **RequestBody**     | Request payload for an operation                                                            |
| **Responses**       | Possible responses from an operation                                                        |
| **Response**        | Single response definition with status code                                                 |
| **MediaType**       | Media type and schema for request/response body                                             |
| **Components**      | Reusable component definitions (schemas, responses, parameters, examples, security schemes) |
| **Schema**          | Data type definition (JSON Schema subset)                                                   |

### Metadata Entities (11 entities)

| Entity Type               | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| **Tag**                   | Metadata label for grouping operations                                 |
| **ExternalDocumentation** | Reference to external documentation                                    |
| **Contact**               | Contact information for API owner                                      |
| **License**               | Legal license for API                                                  |
| **ServerVariable**        | Variable placeholder in server URL templates                           |
| **Header**                | HTTP header parameters for requests/responses                          |
| **Link**                  | Relationship between API responses and subsequent operations (HATEOAS) |
| **Callback**              | Webhook or callback URL pattern                                        |
| **Example**               | Sample values for documentation and testing                            |
| **Encoding**              | Serialization details for multipart content                            |
| **SecurityScheme**        | Security mechanism (types: apiKey, http, oauth2, openIdConnect)        |

### Supporting Entities (3 entities)

| Entity Type         | Description                              |
| ------------------- | ---------------------------------------- |
| **OAuthFlows**      | Configuration for OAuth 2.0 flows        |
| **Condition**       | Logical expression for policy evaluation |
| **RetentionPolicy** | Data retention policies                  |
| **ValidationRule**  | Data validation constraints              |

---

## Intra-Layer Relationships

### Composition Relationships (Part cannot exist without whole)

| Source          | Predicate | Target         | Example                          |
| --------------- | --------- | -------------- | -------------------------------- |
| OpenAPIDocument | composes  | Info           | Document has metadata            |
| OpenAPIDocument | composes  | Paths          | Document defines endpoints       |
| OpenAPIDocument | composes  | Components     | Document has reusable components |
| Paths           | composes  | PathItem       | Paths contain path items         |
| PathItem        | composes  | Operation      | Path has HTTP methods            |
| PathItem        | composes  | Parameter      | Path-level parameters            |
| Operation       | composes  | Parameter      | Operation-specific parameters    |
| Operation       | composes  | RequestBody    | Request payload definition       |
| Operation       | composes  | Responses      | Response definitions             |
| Responses       | composes  | Response       | Individual status responses      |
| RequestBody     | composes  | MediaType      | Request content types            |
| Response        | composes  | MediaType      | Response content types           |
| Response        | composes  | Header         | Response headers                 |
| Response        | composes  | Link           | HATEOAS links                    |
| MediaType       | composes  | Schema         | Data structure                   |
| MediaType       | composes  | Example        | Sample data                      |
| MediaType       | composes  | Encoding       | Serialization details            |
| Components      | composes  | Schema         | Reusable schemas                 |
| Components      | composes  | Response       | Reusable responses               |
| Components      | composes  | Parameter      | Reusable parameters              |
| Components      | composes  | Example        | Reusable examples                |
| Components      | composes  | RequestBody    | Reusable request bodies          |
| Components      | composes  | Header         | Reusable headers                 |
| Components      | composes  | SecurityScheme | Security definitions             |
| Components      | composes  | Link           | Reusable links                   |
| Components      | composes  | Callback       | Reusable callbacks               |
| Info            | composes  | Contact        | API owner contact                |
| Info            | composes  | License        | API license                      |
| SecurityScheme  | composes  | OAuthFlows     | OAuth2 configuration             |

### Aggregation Relationships (Part can exist independently)

| Source          | Predicate  | Target              | Example                  |
| --------------- | ---------- | ------------------- | ------------------------ |
| OpenAPIDocument | aggregates | Server              | API deployment servers   |
| OpenAPIDocument | aggregates | Tag                 | Operation tags           |
| OpenAPIDocument | aggregates | SecurityRequirement | Global security          |
| Server          | aggregates | ServerVariable      | URL template variables   |
| PathItem        | aggregates | Parameter           | Shared parameters        |
| Operation       | aggregates | Callback            | Webhooks                 |
| Operation       | aggregates | SecurityRequirement | Operation-level security |

### Reference Relationships

| Source          | Predicate  | Target                | Example                                |
| --------------- | ---------- | --------------------- | -------------------------------------- |
| Schema          | references | Schema                | Schema $ref to another schema          |
| Parameter       | references | Schema                | Parameter uses schema                  |
| Header          | references | Schema                | Header uses schema                     |
| Link            | references | Operation             | Link points to operation (operationId) |
| Callback        | references | PathItem              | Callback references path definition    |
| Operation       | references | Tag                   | Operation tagged for grouping          |
| Tag             | references | ExternalDocumentation | Tag links to external docs             |
| OpenAPIDocument | references | ExternalDocumentation | Document links to external docs        |
| Encoding        | references | Header                | Encoding uses headers                  |

### Specialization Relationships

| Source | Predicate   | Target | Example                                  |
| ------ | ----------- | ------ | ---------------------------------------- |
| Schema | specializes | Schema | Schema inheritance (allOf, oneOf, anyOf) |

### Behavioral Relationships

| Source         | Predicate | Target    | Example                            |
| -------------- | --------- | --------- | ---------------------------------- |
| Operation      | triggers  | Callback  | Operation invokes webhook          |
| SecurityScheme | serves    | Operation | Security scheme protects operation |

### Association Relationships

| Source  | Predicate       | Target          | Example              |
| ------- | --------------- | --------------- | -------------------- |
| Contact | associated-with | OpenAPIDocument | Contact info for API |
| License | associated-with | OpenAPIDocument | Legal license        |

---

## Cross-Layer References

### Outgoing References (API → Other Layers)

OpenAPI specification includes **custom extensions** (x-\* properties) for cross-layer traceability:

| Target Layer              | Extension Property              | Example                                             |
| ------------------------- | ------------------------------- | --------------------------------------------------- |
| **Layer 1 (Motivation)**  | `x-supports-goals`              | Operation supports business goals                   |
| **Layer 1 (Motivation)**  | `x-fulfills-requirements`       | Operation fulfills functional requirements          |
| **Layer 1 (Motivation)**  | `x-governed-by-principles`      | Operation follows architectural principles          |
| **Layer 1 (Motivation)**  | `x-constrained-by`              | Operation subject to constraints (GDPR, HIPAA, SOX) |
| **Layer 2 (Business)**    | `x-business-service-ref`        | Operation realizes business service                 |
| **Layer 2 (Business)**    | `x-business-interface-ref`      | Operation exposed via business interface            |
| **Layer 4 (Application)** | `x-archimate-ref`               | OpenAPI document realizes ApplicationService        |
| **Layer 7 (Data Model)**  | `schema.$ref`                   | Schema references JSON Schema definition            |
| **Layer 3 (Security)**    | `x-security-resource`           | Operation protected by SecureResource               |
| **Layer 3 (Security)**    | `x-required-permissions`        | Operation requires specific permissions             |
| **Layer 3 (Security)**    | `x-rate-limit`                  | Rate limiting configuration                         |
| **Layer 11 (APM)**        | `x-apm-business-metrics`        | Operation tracked by business metrics               |
| **Layer 11 (APM)**        | `x-apm-sla-target-latency`      | Expected response time (e.g., "100ms")              |
| **Layer 11 (APM)**        | `x-apm-sla-target-availability` | Expected availability (e.g., "99.9%")               |
| **Layer 11 (APM)**        | `x-apm-trace`                   | Distributed tracing enabled                         |
| **Layer 11 (APM)**        | `x-apm-criticality`             | Business criticality (critical, high, medium, low)  |

### Incoming References (Lower Layers → API)

Lower layers reference API layer to show implementation and data structure.

---

## Codebase Detection Patterns

### Pattern 1: FastAPI Python

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="User Management API",  # OpenAPIDocument: Info.title
    description="API for managing user accounts",  # Info.description
    version="1.0.0"  # Info.version
)

class UserCreateRequest(BaseModel):  # Schema (RequestBody)
    username: str
    email: str
    full_name: str

class UserResponse(BaseModel):  # Schema (Response)
    user_id: str
    username: str
    email: str
    created_at: datetime

@app.post(
    "/api/users",  # PathItem + Operation (POST)
    response_model=UserResponse,  # Response schema
    status_code=201,  # Response status
    tags=["Users"],  # Tag
    summary="Create a new user",  # Operation.summary
    description="Creates a new user account with the provided details"  # Operation.description
)
async def create_user(user: UserCreateRequest) -> UserResponse:  # RequestBody + Response
    """
    x-business-service-ref: business/service/user-management
    x-apm-sla-target-latency: 200ms
    x-required-permissions: users.write
    """
    pass
```

**Maps to:**

- OpenAPIDocument: "User Management API"
- PathItem: "/api/users"
- Operation: "POST /api/users"
- RequestBody: MediaType (application/json) with Schema (UserCreateRequest)
- Response: 201 with Schema (UserResponse)
- Tag: "Users"

### Pattern 2: Express.js TypeScript

```typescript
import express from "express";
import { body, param, query, validationResult } from "express-validator";

const router = express.Router();

/**
 * @openapi
 * /api/orders/{orderId}:
 *   get:
 *     summary: Get order by ID
 *     description: Retrieves a single order by its unique identifier
 *     tags:
 *       - Orders
 *     parameters:
 *       - name: orderId
 *         in: path
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *     responses:
 *       200:
 *         description: Order found
 *         content:
 *           application/json:
 *             schema:
 *               $ref: '#/components/schemas/Order'
 *       404:
 *         description: Order not found
 *     x-business-service-ref: business/service/order-management
 *     x-apm-sla-target-latency: 100ms
 *     x-apm-criticality: high
 */
router.get("/api/orders/:orderId", param("orderId").isUUID(), async (req, res) => {
  // Implementation
});
```

**Maps to:**

- PathItem: "/api/orders/{orderId}"
- Operation: "GET /api/orders/{orderId}"
- Parameter: "orderId" (in: path, type: string, format: uuid)
- Response: 200 with schema reference
- Response: 404 error response
- Custom extensions: x-business-service-ref, x-apm-sla-target-latency, x-apm-criticality

### Pattern 3: Spring Boot Java

```java
@RestController
@RequestMapping("/api/products")
@Tag(name = "Products", description = "Product management operations")
public class ProductController {

    @Operation(
        summary = "List products",
        description = "Returns a paginated list of products",
        extensions = {
            @Extension(name = "x-apm-sla-target-latency", properties = @ExtensionProperty(name = "latency", value = "150ms")),
            @Extension(name = "x-required-permissions", properties = @ExtensionProperty(name = "permissions", value = "products.read"))
        }
    )
    @ApiResponses({
        @ApiResponse(
            responseCode = "200",
            description = "Products retrieved successfully",
            content = @Content(
                mediaType = "application/json",
                schema = @Schema(implementation = ProductListResponse.class)
            )
        )
    })
    @GetMapping
    public ResponseEntity<ProductListResponse> listProducts(
        @Parameter(description = "Page number", example = "1") @RequestParam(defaultValue = "1") int page,
        @Parameter(description = "Page size", example = "20") @RequestParam(defaultValue = "20") int size
    ) {
        // Implementation
    }
}
```

**Maps to:**

- PathItem: "/api/products"
- Operation: "GET /api/products"
- Parameters: "page" (query), "size" (query)
- Response: 200 with ProductListResponse schema
- Tag: "Products"
- Custom extensions

### Pattern 4: OpenAPI YAML Definition

```yaml
openapi: 3.0.3
info:
  title: Payment Processing API
  description: API for processing customer payments
  version: 2.1.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
  x-governed-by-principles:
    - motivation/principle/api-first-design
    - motivation/principle/security-by-design

servers:
  - url: https://api.example.com/v2
    description: Production server
  - url: https://staging-api.example.com/v2
    description: Staging server

paths:
  /payments:
    post:
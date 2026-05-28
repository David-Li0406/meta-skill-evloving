# API Versioning Strategies (2026)

## Header-based Versioning (The "Elite" Choice)
In 2026, header-based versioning is preferred for its cleanliness and ability to support multiple concurrent versions without changing URLs.

### Implementation:
- **Request Header**: `X-API-Version: 2026-01-23`
- **Backend Logic**: Use middleware to route requests to the correct handler based on the date-based version string.

---

## URL-based Versioning (The Standard)
The traditional `/v1/`, `/v2/` approach is still widely used for its simplicity and cacheability.

### Pros:
- Easy for external developers to understand.
- Direct routing at the proxy/load balancer level.

### Cons:
- Forces updates to client base URLs for every major version.

---

## Evolution with OpenAPI
Maintain separate OpenAPI specifications for each version:
- `openapi/v1.yaml`
- `openapi/v2.yaml`

### Versioning the Contract:
Use Git branches or tags to track the evolution of your `openapi.yaml`. When a breaking change is introduced, bump the `info.version` field and the major version in the URL/header.

---

## Breaking Changes Checklist
Before bumping a version, check if you have:
1. Removed a field.
2. Changed a field's type.
3. Changed a required field to optional (or vice-versa).
4. Changed a status code for a common error.
5. Changed authentication requirements.

# API Versioning

**Category**: api-security/versioning
**Description**: Detection patterns for API versioning practices and issues

---

## Overview

API versioning is essential for maintaining backward compatibility while evolving APIs.
This scanner identifies versioning patterns and potential issues.

**Note:** This scanner is informational and NOT included in the security profile.

---

## URL Path Versioning

### Version in URL Path
**Pattern**: `\/v[0-9]+\/`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python, java, go]
- Common URL path versioning pattern (e.g., /v1/, /v2/)

### Major Minor Versioning
**Pattern**: `\/v[0-9]+\.[0-9]+\/`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python, java, go]
- Major.minor version in URL path (e.g., /v1.2/)

---

## Header Versioning

### Custom Version Header
**Pattern**: `(X-API-Version|Accept-Version|Api-Version)\s*[=:]`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- Custom HTTP header for API versioning

### Accept Header Versioning
**Pattern**: `Accept.*application\/vnd\.[^+]+\+json;\s*version=`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- Content negotiation versioning via Accept header

---

## Query Parameter Versioning

### Version Query String
**Pattern**: `[\?&]version=[0-9]`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- Version passed as query parameter

### API Version Query Param
**Pattern**: `[\?&]api[-_]?version=[0-9]`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- API version as query parameter

---

## Deprecated API Endpoints

### Deprecated Annotation
**Pattern**: `(@deprecated|@Deprecated|# deprecated|// deprecated|DEPRECATED)`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript, python, java]
- Deprecated annotation or comment marker

### Sunset Header
**Pattern**: `Sunset\s*[=:]`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript, python]
- RFC 8594 Sunset header indicating API retirement

### Deprecation Header
**Pattern**: `Deprecation\s*[=:]`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript, python]
- HTTP Deprecation header

---

## Version Issues

### Version Mismatch
**Pattern**: `(\/v1\/.*\/v2\/|\/v2\/.*\/v1\/)`
**Type**: regex
**Severity**: low
**Languages**: [javascript, typescript, python]
- Multiple conflicting version definitions in URL

### Missing Version
**Pattern**: `app\.(get|post|put|delete)\s*\(\s*['"]\/api\/(?!v[0-9])`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript]
- API routes without version prefix

### Legacy API Versions
**Pattern**: `\/v[0-1]\/`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- Very old API versions (v0, v1) still active

---

## GraphQL Versioning

### GraphQL Schema Version
**Pattern**: `(schemaVersion|schema_version|apiVersion)\s*[=:]\s*['"][0-9]`
**Type**: regex
**Severity**: info
**Languages**: [javascript, typescript, python]
- GraphQL schema version field

---

## OpenAPI Version Spec

### OpenAPI Version Field
**Pattern**: `(openapi|swagger)\s*[=:]\s*['"][0-9]+\.[0-9]+`
**Type**: regex
**Severity**: info
**Languages**: [yaml, json]
- OpenAPI/Swagger specification version

### API Info Version
**Pattern**: `info\s*:[\s\S]*?version\s*[=:]\s*['"][0-9]+\.[0-9]+`
**Type**: regex
**Severity**: info
**Languages**: [yaml, json]
- API version in OpenAPI info block

---

## Best Practices Summary

### Recommended Patterns

1. **URL Path Versioning** (Most Common)
   - `/api/v1/users`
   - Clear, easy to understand
   - Works well with caching

2. **Header Versioning**
   - `Accept: application/vnd.myapi.v2+json`
   - Cleaner URLs
   - More RESTful

3. **Sunset Headers**
   - `Sunset: Sat, 31 Dec 2024 23:59:59 GMT`
   - Communicate deprecation timeline

### Anti-Patterns

1. **Query Parameter Versioning**
   - `?version=2`
   - Caching issues
   - Less RESTful

2. **No Versioning**
   - Breaking changes affect all clients
   - No migration path

---

## References

- [API Versioning Best Practices](https://www.postman.com/api-platform/api-versioning/)
- [REST API Versioning](https://restfulapi.net/versioning/)
- [Sunset HTTP Header](https://datatracker.ietf.org/doc/html/rfc8594)

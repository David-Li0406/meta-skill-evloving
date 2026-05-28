---
name: api-design-and-best-practices
description: Use this skill when designing REST APIs, ensuring security, validation, and error handling best practices.
---

# API Design and Best Practices

## 📋 Pre-execution Checklist (Mandatory)

### Should you use this skill?
- [ ] Are you designing a REST API?
- [ ] Are you creating new endpoints?
- [ ] Are you considering error response formats?
- [ ] Are you evaluating API versioning?

### Prerequisites
- [ ] Have you clearly defined the target resources?
- [ ] Do you understand the client usage scenarios?
- [ ] Are you aware of the authentication and authorization requirements?
- [ ] Have you checked for consistency with existing APIs?

### Prohibited Practices
- [ ] Are you trying to include verbs in the endpoint? (/getUsers → /users)
- [ ] Are you exposing internal details in 500 errors?
- [ ] Are you attempting breaking changes without versioning?
- [ ] Are you using inconsistent response formats?

---

## Triggers

- When designing REST APIs
- When creating new endpoints
- When considering error response formats
- When evaluating API versioning

---

## 🚨 Core Principle

**APIs are contracts. Changes after publication are difficult.**

---

## RESTful Design

```
GET    /users          # List
GET    /users/123      # Retrieve
POST   /users          # Create
PUT    /users/123      # Full update
PATCH  /users/123      # Partial update
DELETE /users/123      # Delete
```

---

## Status Codes

```
200 OK           - Success
201 Created      - Creation successful
400 Bad Request  - ⚠️ Validation error
401 Unauthorized - Authentication required
403 Forbidden    - No permission
404 Not Found    - Resource not found
500 Internal     - 🚫 Hide details
```

---

## Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      { "field": "email", "message": "Invalid format" }
    ]
  }
}
```

---

## ⚠️ Versioning

```
/v1/users
/v2/users
```
Breaking changes require a major version upgrade.

---

## Rate Limiting

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95

429 Too Many Requests
Retry-After: 60
```

---

## API Security Best Practices

### Principles (Investigate existing code for specifications)

- OWASP Compliance: Secure cookies, rate limiting, no hard-coded secrets
- Input Validation: Zod schema required
- Error Handling: Appropriate HTTP status and error messages
- Authentication: Retrieve secret keys from environment variables

### Workflow for Implementation

1. **Investigation (Mandatory before implementation)**
   ```bash
   # Check existing APIs
   find app/api -name "*.ts" | head -20

   # Check authentication patterns
   grep -r "auth" app/api/ --include="*.ts"

   # Check existing schemas
   grep -r "z.object" src/ --include="*.ts"

   # Check for environment variable usage
   grep -r "process.env" src/lib/ --include="*.ts"
   ```

2. **Security Check (Mandatory)**
   ```bash
   # Detect hard-coded secret keys
   grep -r "secret\|password\|key" src/ --include="*.ts" | grep -v "process.env"

   # Check for endpoints without authentication
   grep -L "auth" app/api/**/route.ts
   ```

3. **Implementation**
   - Follow existing patterns
   - Validate input with Zod
   - Ensure appropriate error handling

4. **Validation (Mandatory)**
   ```bash
   # Static analysis
   npm run type-check
   npm run lint

   # Build verification
   npm run build

   # API testing (curl or fetch MCP)
   curl -X GET http://localhost:3000/api/endpoint
   ```

5. **API Functionality Check (using fetch MCP)**
   - Normal case: Expected response
   - Abnormal case: Invalid input, authentication error
   - Edge case: Rate limiting, timeout

## Reporting Format

```
## API Implementation Report

### Security Check Results
- [ ] No hard-coded secret keys
- [ ] Endpoints requiring authentication are protected
- [ ] Input validation implemented

### Changes
- File: Summary of changes

### API Validation Results
- Endpoint: URL
- Normal case: Status, Response
- Abnormal case: Status, Error message
```
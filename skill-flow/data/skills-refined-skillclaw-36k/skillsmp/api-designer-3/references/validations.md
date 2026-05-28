# Api Designer - Validations

## Verb in URL Path

### **Id**
verb-in-url
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - /create[A-Z]
  - /get[A-Z]
  - /update[A-Z]
  - /delete[A-Z]
  - /fetch[A-Z]
  - path.*=.*/(create|get|update|delete|fetch)
### **Message**
URL contains verb. REST uses HTTP methods as verbs.
### **Fix Action**
Use POST /resources, GET /resources/{id}, etc.
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.yaml
  - **/*.json

## Inconsistent ID Format

### **Id**
inconsistent-id-format
### **Severity**
info
### **Type**
regex
### **Pattern**
  - id:\s*number
  - id:\s*integer
  - _id:\s*number
### **Message**
Using numeric IDs. Consider UUIDs or prefixed IDs for better security.
### **Fix Action**
Use UUID or prefixed string IDs (e.g., 'mem_abc123')
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/schema*.yaml
  - **/openapi*.yaml

## Error Response Without Code

### **Id**
no-error-code
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - error.*message(?!.*code)
  - throw new Error\(["'][^"']+["']\)
  - raise.*Exception\(["'][^"']+["']\)
### **Message**
Error response without machine-readable code. Clients can't programmatically handle.
### **Fix Action**
Add error code: {error: {code: 'NOT_FOUND', message: '...'}}
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## List Endpoint Without Pagination

### **Id**
unbounded-list
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - findMany\(\)(?!.*take)
  - find\(\{\}\)(?!.*limit)
  - SELECT.*FROM(?!.*LIMIT)
### **Message**
List query without limit. Response can grow unbounded.
### **Fix Action**
Add pagination: findMany({take: 100}), add limit parameter
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.sql

## Rate Limiting Without Headers

### **Id**
missing-rate-limit-headers
### **Severity**
info
### **Type**
regex
### **Pattern**
  - status.*429(?!.*X-RateLimit)
  - Too Many Requests(?!.*Retry-After)
  - rate.*limit(?!.*header)
### **Message**
Rate limiting without standard headers. Clients can't implement backoff.
### **Fix Action**
Return X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After headers
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## Datetime Without Timezone

### **Id**
datetime-no-timezone
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - datetime\.now\(\)(?!.*utc)
  - new Date\(\)\.toISOString\(\)(?!.*Z)
  - strftime\([^)]+\)(?!.*%z|%Z)
### **Message**
Datetime without explicit timezone. Causes interpretation issues.
### **Fix Action**
Use UTC with timezone: datetime.now(timezone.utc), include 'Z' suffix
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## Response Without Request ID

### **Id**
no-request-id
### **Severity**
info
### **Type**
regex
### **Pattern**
  - return.*json\((?!.*request_id|requestId)
  - Response\((?!.*x-request-id)
### **Message**
Response without request ID. Difficult to correlate logs with client issues.
### **Fix Action**
Include request_id in response meta or X-Request-Id header
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## GraphQL Without Depth Limit

### **Id**
graphql-no-depth-limit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - createSchema\((?!.*depthLimit)
  - ApolloServer\((?!.*validationRules)
  - graphql.*server(?!.*depth)
### **Message**
GraphQL without depth limit. Vulnerable to nested query attacks.
### **Fix Action**
Add depth limit: depthLimit(5) in validation rules
### **Applies To**
  - **/*.ts
  - **/*.js

## Internal Error Details Exposed

### **Id**
expose-internal-error
### **Severity**
error
### **Type**
regex
### **Pattern**
  - catch.*return.*err\.message
  - catch.*response.*error.*stack
  - 500.*Internal.*Server.*Error.*\+.*err
### **Message**
Internal error details exposed to client. Security and privacy risk.
### **Fix Action**
Return generic message, log details server-side
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## Response Without Content-Type

### **Id**
no-content-type
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - return.*json\((?!.*content.*type)
  - Response\((?!.*headers.*content-type)
### **Message**
Response without explicit Content-Type. Clients may misinterpret.
### **Fix Action**
Set Content-Type: application/json or appropriate type
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.js

## Removing or Renaming Enum Value

### **Id**
breaking-enum-change
### **Severity**
error
### **Type**
regex
### **Pattern**
  - // removed:.*enum
  - # deprecated.*status
  - enum.*\{[^}]*//.*removed
### **Message**
Removing enum value is breaking change. Clients parsing old values will fail.
### **Fix Action**
Keep old values, mark deprecated, add new values
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/schema*.yaml

## Offset Pagination on Large Table

### **Id**
offset-pagination-large-table
### **Severity**
info
### **Type**
regex
### **Pattern**
  - OFFSET\s+\$
  - offset:\s*number
  - \.skip\(offset\)
### **Message**
Offset pagination inefficient for large tables. Consider cursor-based.
### **Fix Action**
Use cursor-based pagination with keyset (WHERE id > :last_id)
### **Applies To**
  - **/*.ts
  - **/*.py
  - **/*.sql
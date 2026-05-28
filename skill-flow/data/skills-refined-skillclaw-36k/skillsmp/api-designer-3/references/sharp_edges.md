# Api Designer - Sharp Edges

## Breaking Optional To Required

### **Id**
breaking-optional-to-required
### **Summary**
Making optional field required breaks all clients
### **Severity**
critical
### **Situation**
Evolving API to require previously optional field
### **Why**
  Clients built against old API don't send the field. Suddenly their
  requests fail with validation errors. Can't rollback without data loss
  if you already have new records requiring the field.
  
### **Solution**
  1. Never make optional fields required
  2. If must require, version the API:
     - v1: field optional, default value used
     - v2: field required, migration path documented
  3. Add validation gradually:
     - Week 1: Log when field missing
     - Week 2: Return warning header
     - Week 3: Return error in new version only
  4. Provide migration guide and timeline
  
### **Symptoms**
  - Sudden spike in 400 errors after deployment
  - Client complaints "it worked yesterday"
  -     ##### **Error**
field X is required
### **Detection Pattern**
required.*true|\.required\(\)|NotNull

## Offset Pagination Drift

### **Id**
offset-pagination-drift
### **Summary**
Offset pagination returns duplicates or skips items during writes
### **Severity**
medium
### **Situation**
Paginating through actively changing data
### **Why**
  User is on page 3 (offset 200). New item is inserted at position 50.
  Page 3 now starts at what was page 3 item 2. User sees duplicate.
  Or item at position 199 is deleted. User skips an item entirely.
  
### **Solution**
  1. Use cursor-based pagination:
     GET /items?after=item_abc&limit=100
  2. Cursor encodes position in stable ordering:
     {"created_at": "2024-01-15T10:30:00Z", "id": "item_abc"}
  3. Query uses cursor for consistent position:
     WHERE (created_at, id) > (:cursor_created_at, :cursor_id)
  4. If must use offset, accept the limitation and document it
  
### **Symptoms**
  - Duplicate items in paginated results
  - Missing items when iterating all pages
  - "I saw this item already" user reports
### **Detection Pattern**
offset|page.*number|skip

## N Plus One Includes

### **Id**
n-plus-one-includes
### **Summary**
Include/expand parameters cause N+1 database queries
### **Severity**
high
### **Situation**
API supports including related resources
### **Why**
  GET /memories?include=entities,relationships looks innocent.
  But if you fetch 100 memories, that's 100 queries for entities,
  100 queries for relationships. 201 queries instead of 3.
  
### **Solution**
  1. Batch fetch included resources:
     memory_ids = [m.id for m in memories]
     entities = Entity.where(memory_id__in=memory_ids)
  2. Use DataLoader pattern for GraphQL
  3. Limit include depth:
     ?include=entities (ok)
     ?include=entities.mentions.users (too deep)
  4. Consider if you need includes at all - maybe separate endpoint
  
### **Symptoms**
  - Slow response with includes, fast without
  - Database CPU spike on list endpoints
  - Linear slowdown as page size increases
### **Detection Pattern**
include=|expand=|embed=

## Unbounded Array Response

### **Id**
unbounded-array-response
### **Summary**
Endpoint returns array that can grow indefinitely
### **Severity**
medium
### **Situation**
List endpoint without pagination or limits
### **Why**
  Today you have 100 memories. Works fine. Next year you have 10 million.
  Single request tries to return 10 million items. OOM, timeout, client crash.
  
### **Solution**
  1. Always paginate list endpoints:
     GET /memories → GET /memories?limit=100
  2. Set server-side max limit:
     limit = min(request.limit, 1000)
  3. Return pagination info even on first page:
     {"data": [...], "pagination": {"has_more": true}}
  4. For truly unbounded, use streaming:
     Transfer-Encoding: chunked
     Content-Type: application/x-ndjson
  
### **Symptoms**
  - Timeout on list endpoints as data grows
  - Out of memory errors
  - Clients hanging on large accounts
### **Detection Pattern**
limit|max.*results|pagination

## Rate Limit Without Headers

### **Id**
rate-limit-without-headers
### **Summary**
Rate limiting without informative headers
### **Severity**
medium
### **Situation**
Implementing rate limiting
### **Why**
  Client gets 429. How long to wait? How many requests left? No idea.
  Client either hammers retry (making it worse) or waits too long.
  
### **Solution**
  1. Return standard rate limit headers:
     X-RateLimit-Limit: 1000
     X-RateLimit-Remaining: 42
     X-RateLimit-Reset: 1704067200  # Unix timestamp
  2. On 429, include Retry-After:
     HTTP/1.1 429 Too Many Requests
     Retry-After: 30
  3. Response body explains limit:
     {
       "error": {
         "code": "RATE_LIMITED",
         "message": "Rate limit exceeded. 1000 requests per hour.",
         "retry_after": 30
       }
     }
  4. Different limits for different endpoints (writes vs reads)
  
### **Symptoms**
  - Clients retry immediately on 429
  - Support tickets asking "why am I blocked?"
  - Clients implement arbitrary backoff
### **Detection Pattern**
X-RateLimit|Retry-After|rate.*limit

## Enum Evolution Breaking

### **Id**
enum-evolution-breaking
### **Summary**
Adding enum value breaks clients with strict parsing
### **Severity**
medium
### **Situation**
Evolving enum types over time
### **Why**
  Client deserializes status into StatusEnum. You add new status "pending_review".
  Client's parser fails on unknown value. Client crashes or drops the record.
  
### **Solution**
  1. Document that enums may grow - clients MUST handle unknown values
  2. Use "unknown" fallback in client SDKs:
     status = StatusEnum.from_str(value) or StatusEnum.UNKNOWN
  3. Consider strings instead of enums for extensibility
  4. Version API if adding enum value changes semantics
  5. Pre-announce new values before deploying:
     "New status 'pending_review' coming in 2 weeks"
  
### **Symptoms**
  - Client errors after adding enum value
  - "Unknown enum value" errors in client logs
  - Records disappearing from client apps
### **Detection Pattern**
enum|status.*type|Literal\[

## Timestamp Timezone Chaos

### **Id**
timestamp-timezone-chaos
### **Summary**
Timestamp fields without timezone cause interpretation issues
### **Severity**
medium
### **Situation**
Returning datetime fields in API responses
### **Why**
  "2024-01-15 10:30:00" - is that UTC? Server timezone? Client timezone?
  Client in Tokyo, server in NYC. They disagree by 14 hours.
  
### **Solution**
  1. Always use ISO 8601 with timezone:
     "created_at": "2024-01-15T10:30:00Z"  # UTC
     "created_at": "2024-01-15T10:30:00+09:00"  # With offset
  2. Prefer UTC for storage and API, convert for display
  3. Document timezone policy in API docs
  4. Accept timezone in input, normalize to UTC:
     Input: "2024-01-15T10:30:00+09:00"
     Stored: "2024-01-15T01:30:00Z"
  
### **Symptoms**
  - Events showing wrong time
  - "This happened 8 hours ago" when it was just now
  - Scheduling off by hours
### **Detection Pattern**
datetime|timestamp|created_at|ISO.*8601

## Graphql Depth Attack

### **Id**
graphql-depth-attack
### **Summary**
Deeply nested GraphQL query exhausts resources
### **Severity**
high
### **Situation**
GraphQL API without query depth limits
### **Why**
  query { user { friends { friends { friends { friends { ... } } } } } }
  Each level multiplies database queries. 10 levels deep with 100 friends
  each = 100^10 potential queries. DoS via legitimate-looking query.
  
### **Solution**
  1. Limit query depth:
     # graphql-depth-limit
     depthLimit(5)
  2. Limit query complexity:
     # graphql-query-complexity
     complexityLimit(1000)
  3. Limit result size:
     first: 100  # max 100 items
  4. Timeout long-running queries
  5. Log and alert on expensive queries
  
### **Symptoms**
  - GraphQL server OOM
  - Extremely slow queries
  - Database connection exhaustion
### **Detection Pattern**
depth.*limit|complexity|maxDepth
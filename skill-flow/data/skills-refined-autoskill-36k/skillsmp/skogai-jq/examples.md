# examples

real-world use cases showing why we need this.

## use case: chat message normalization

### problem
chat history from different tools (aichat, goose, gptme, claude) have different json shapes:

aichat:
```json
{"role": "user", "content": "hello"}
```

goose:
```json
{"type": "human", "message": "hello", "timestamp": 1234567890}
```

gptme:
```json
{"from": "user", "text": "hello", "created": "2025-01-01T00:00:00Z"}
```

### solution
transformations for each format → standard shape:
```json
{"role": "user", "content": "hello", "timestamp": "2025-01-01T00:00:00Z"}
```

### transformations needed
- extract-aichat-message
- extract-goose-message
- extract-gptme-message
- normalize-timestamp
- validate-message-schema

### current state
~/dev/chat-history/jq-utils/ has ad-hoc scripts for this.
should be in this library with schemas.

---

## use case: api response transformation

### problem
api returns paginated results:
```json
{
  "data": [...],
  "meta": {"page": 1, "total": 100}
}
```

need just the data, formatted differently:
```json
[
  {"id": "1", "name": "item1"},
  ...
]
```

### transformations needed
- extract-field (get .data)
- array-map (transform each item)
- pick-fields (select id, name only)

### composition
```bash
jq -f extract-field.jq --arg field "data" response.json |
jq -f array-map.jq --transform pick-fields.jq --args id,name
```

---

## use case: config file management

### problem
need to update nested config values:
```json
{
  "database": {
    "host": "localhost",
    "port": 5432
  }
}
```

want to change host to "prod.example.com".

### solution
```bash
jq -f crud-set.jq --arg path "database.host" --arg value "prod.example.com" config.json
```

### transformations needed
- crud-set
- crud-get (to verify)
- validate-config (check schema)

---

## use case: log processing

### problem
logs are json lines:
```json
{"level":"info","msg":"request","url":"/api/users"}
{"level":"error","msg":"failed","error":"timeout"}
```

need to:
1. filter by level
2. extract specific fields
3. aggregate by url

### transformations needed
- filter-by-field (level == "error")
- pick-fields (url, error, msg)
- group-by-field (url)
- count-by-field (errors per url)

### pipeline
```bash
cat logs.jsonl |
jq -f filter-by-field.jq --arg field "level" --arg value "error" |
jq -f pick-fields.jq --args url,error,msg |
jq -s -f group-by-field.jq --arg field "url" |
jq -f count-by-field.jq --arg field "url"
```

---

## use case: data migration

### problem
old data format:
```json
{
  "user_name": "skogix",
  "user_email": "email@example.com"
}
```

new format:
```json
{
  "user": {
    "name": "skogix",
    "email": "email@example.com"
  }
}
```

### transformations needed
- rename-field (user_name → name)
- nest-fields (move to .user)
- validate-schema (check new format)

### migration script
```bash
for file in data/*.json; do
  jq -f rename-field.jq --arg old "user_name" --arg new "name" "$file" |
  jq -f rename-field.jq --arg old "user_email" --arg new "email" |
  jq -f nest-fields.jq --arg path "user" --args name,email |
  jq -f validate-schema.jq --schema user-schema.json > "${file}.new"
done
```

---

## use case: structured output for ai

### problem
ai generates freeform json:
```json
{
  "name": "skogix",
  "age": "30",
  "active": "true"
}
```

need specific types:
```json
{
  "name": "skogix",
  "age": 30,
  "active": true
}
```

### transformations needed
- coerce-types (string → number, string → boolean)
- validate-schema (ensure correct types)
- set-defaults (add missing required fields)

---

## use case: multi-source data merging

### problem
user data from multiple sources:

source1.json:
```json
{"id": "1", "name": "skogix", "email": "email@example.com"}
```

source2.json:
```json
{"id": "1", "location": "sweden", "timezone": "CET"}
```

need merged:
```json
{"id": "1", "name": "skogix", "email": "email@example.com", "location": "sweden", "timezone": "CET"}
```

### transformations needed
- index-by-field (create lookup by id)
- deep-merge (combine objects)
- deduplicate (remove conflicts)

---

## use case: api request building

### problem
need to build api request body from config:

config:
```json
{
  "user": "skogix",
  "project": "jq-transforms"
}
```

api expects:
```json
{
  "query": {
    "user": {"eq": "skogix"},
    "project": {"eq": "jq-transforms"}
  },
  "limit": 10
}
```

### transformations needed
- wrap-field (value → {eq: value})
- nest-fields (wrap in .query)
- add-field (add limit)

---

## use case: test data generation

### problem
need test data matching schema.

schema:
```json
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "number"}
  }
}
```

generate:
```json
{"name": "test-user-1", "age": 25}
```

### transformations needed
- generate-from-schema (create random valid data)
- or: template-fill (substitute values in template)

---

## use case: error response normalization

### problem
different apis return errors differently:

api1:
```json
{"error": "not found"}
```

api2:
```json
{"status": "error", "message": "not found", "code": 404}
```

api3:
```json
{"errors": [{"msg": "not found", "field": "id"}]}
```

### transformations needed
- normalize-error (all → standard format)
- extract-error-message
- map-error-code

standard format:
```json
{
  "error": true,
  "message": "not found",
  "code": 404,
  "details": {}
}
```

---

## patterns observed

across these use cases:

1. **extract** - get specific fields/values
2. **transform** - change shape/format
3. **validate** - check against schema
4. **filter** - select subset
5. **aggregate** - combine/group
6. **normalize** - standardize format

these map to transformation categories:
- crud (get/set/delete)
- array (map/filter/reduce)
- object (merge/pick/nest)
- string (split/join/format)
- validation (schema/type/required)

---

## composition patterns

### sequential transformation
```bash
cat input.json | jq -f t1.jq | jq -f t2.jq | jq -f t3.jq
```

### conditional transformation
```bash
if jq -e '.type == "user"' input.json; then
  jq -f transform-user.jq input.json
else
  jq -f transform-guest.jq input.json
fi
```

### parallel transformation
```bash
jq -f transform.jq input1.json > output1.json &
jq -f transform.jq input2.json > output2.json &
wait
```

### batch transformation
```bash
for file in data/*.json; do
  jq -f transform.jq "$file" > "processed/${file}"
done
```

### transformation with fallback
```bash
jq -f transform.jq input.json 2>/dev/null || echo '{"error": true}'
```

---

## anti-patterns observed

### over-complex single transformation
don't try to do everything in one jq script.
break into simple, composable pieces.

### imperative transformation
looping over files calling jq for each field update.
better: one jq call that does all updates.

### ignoring schemas
transforming without validating input/output.
leads to runtime errors that are hard to debug.

### hard-coded values
jq scripts with hard-coded strings instead of args.
not reusable.

---

## what we learn

1. most transformations are simple (5-10 lines of jq)
2. composition is key (pipe simple transformations)
3. validation is critical (schemas catch errors early)
4. patterns repeat (extract, transform, validate)
5. ai needs examples (schema + tests + docs)

these examples guide what transformations to build first.

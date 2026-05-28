# Data CRUD Operations

Manage JSON data in datasets (key-value stores with optional schema validation).

**Important:** Data service paths must be discovered dynamically - they are NOT always at `/data`.

## Step 1: Find Data Services

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# List all data services with their paths and names
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("data.rsm"))) | .[] | {path: .key, name: .value.name}'
```

Example output:
```json
{"path": "/api/users", "name": "User Data"}
{"path": "/api/products", "name": "Product Data"}
```

## Step 2: Select Data Service

**If multiple data services exist**, present them to the user and ask which to use.

**If user specifies a path** in their prompt, use that path directly.

```bash
# Get the first data service (or use user-specified path)
DATA_PATH=$(curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq -r 'to_entries | map(select(.value.source | contains("data.rsm"))) | .[0].key // empty')
```

## Operations

All operations use the discovered `$DATA_PATH`.

### Get JSON Schema

Data stores may have JSON schemas that define validation rules. Retrieve the schema by appending `/.schema` to the dataset path:

```bash
# Get schema for a dataset (e.g., /data/supplier)
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/<dataset>/.schema" | jq '.'
```

**Example:**
```bash
# Get schema for the 'supplier' dataset
curl -s -b cookies.txt "$RESTSPACE_URL/data/supplier/.schema" | jq '.'
```

**Response (200 OK):**
```json
{
  "type": "object",
  "pathPattern": "${code}",
  "properties": {
    "code": {"type": "string"},
    "name": {"type": "string"}
  },
  "required": ["code", "name"]
}
```

**Response (404 Not Found):** Dataset has no schema defined.

**Notes:**
- Not all datasets have schemas
- The `pathPattern` field shows how keys are constructed from object properties
- Schemas use JSON Schema Draft 7 format

### List Items

```bash
# List all items (the path IS the dataset for data services)
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/"

# With pagination
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/?$take=10&$skip=0"
```

**Response (200 OK):**
```json
[
  {"email": "alice@example.com", "name": "Alice"},
  {"email": "bob@example.com", "name": "Bob"}
]
```

### Read Single Item

```bash
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/{key}"
```

**Response (200 OK):**
```json
{
  "email": "alice@example.com",
  "name": "Alice",
  "role": "admin"
}
```

### Create Item

```bash
curl -s -b cookies.txt -X POST "$RESTSPACE_URL$DATA_PATH/{key}" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

**Response (201 Created):** Returns the created item.

### Replace Item (Full Update)

```bash
curl -s -b cookies.txt -X PUT "$RESTSPACE_URL$DATA_PATH/{key}" \
  -H "Content-Type: application/json" \
  -d '{"field": "new value"}'
```

**Response (200 OK or 204 No Content)**

### Partial Update

```bash
curl -s -b cookies.txt -X PATCH "$RESTSPACE_URL$DATA_PATH/{key}" \
  -H "Content-Type: application/json" \
  -d '{"field": "updated value"}'
```

**Response (200 OK):** Returns the updated item.

### Delete Item

```bash
curl -s -b cookies.txt -X DELETE "$RESTSPACE_URL$DATA_PATH/{key}"
```

**Response (200 OK)**

## Complete Example

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# 1. Discover data services
echo "Available data services:"
curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq 'to_entries | map(select(.value.source | contains("data.rsm"))) | .[] | {path: .key, name: .value.name}'

# 2. Use specific service (replace with discovered path)
DATA_PATH="/api/users"

# 3. List items
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/" | jq '.'

# 4. Read specific item
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/alice@example.com" | jq '.'
```

## Working with JSON Data

Use `jq` for parsing and transforming:

```bash
# Extract specific field
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/{key}" | jq '.name'

# List just one field from all items
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/" | jq '.[].email'

# Filter results
curl -s -b cookies.txt "$RESTSPACE_URL$DATA_PATH/" | jq '[.[] | select(.role == "admin")]'
```

## Notes

- Keys are typically email addresses, UUIDs, or slugs
- Datasets may have JSON Schema validation
- Access controlled by `readRoles`/`writeRoles` configuration
- Some servers may have nested paths like `/api/v1/users` - always use discovery

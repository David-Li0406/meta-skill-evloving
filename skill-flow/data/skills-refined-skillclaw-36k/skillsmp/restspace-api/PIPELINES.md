# Pipelines and Transforms

Pipelines compose services into complex workflows. They follow Unix pipes-and-filters philosophy: chain small, single-purpose services together.

## Pipeline Basics

A pipeline is a JSON array where each item is a step:

```json
[
  "GET /json/somepagedata",
  "/templates/pagetemplate.html"
]
```

This fetches JSON from `/json/somepagedata`, then POSTs it to the template service.

**Default method is POST** when none specified.

## Request Spec Syntax

```
[METHOD [json-path]] <url-pattern>
```

| Part | Description |
|------|-------------|
| METHOD | GET, POST, PUT, PATCH, DELETE (default: POST) |
| json-path | Optional path to select part of JSON body |
| url-pattern | URL with optional path pattern substitutions |

**Examples:**
```json
"GET /data/users"           // Simple GET
"POST /api/save"            // Explicit POST
"PUT items /store/$*"       // PUT the 'items' property to a path-patterned URL
```

## Path Patterns

Substitute parts of the original request URL into the pipeline URL:

| Pattern | Meaning |
|---------|---------|
| `$*` | Whole service path |
| `$>0` | First path element |
| `$>1` | Second path element |
| `$<0` | Last path element |
| `$<1` | Second-to-last element |
| `$>1<0` | Second to last (inclusive range) |
| `$?(key)` | Query string value for 'key' |
| `$?*` | Whole query string |
| `${}` | Current message body (for expansion) |
| `${prop}` | Property 'prop' from JSON body |
| `${[]}` | Expand array - creates parallel requests |
| `${$var}` | Value of variable `$var` |

**Example - pass-through subpath:**
```json
[
  "POST /json/records/$*",
  "/sendemail"
]
```
Request to `/email-record/mail-message` → POSTs to `/json/records/mail-message`

## Transforms

JSON objects in a pipeline transform the message body:

```json
[
  "GET /data/user",
  {
    "displayName": "firstName + ' ' + lastName",
    "email": "email"
  }
]
```

### Transform Syntax

Transform values are JavaScript expressions with input properties as variables:

```json
// Input
{ "a": "hello", "b": 2 }

// Transform
{ "c": "a.toUpperCase()", "d": "b * 10" }

// Output
{ "c": "HELLO", "d": 20 }
```

### Special Keys

| Key | Meaning |
|-----|---------|
| `$` or `$this` | Assign to whole output |
| `$varname` | Set a variable (not output) |
| `$$key` | Escape: creates property `$key` |

**Copy-and-modify pattern:**
```json
{
  "$": "$",           // Copy entire input to output
  "name": "'new name'" // Override specific property
}
```

**Remove a property:**
```json
{
  "$": "$",
  "unwantedProp": "undefined"
}
```

### Variables

Variables persist for the pipeline lifetime:

```json
[
  {
    "$userId": "pathPattern('$<0')"
  },
  "GET /users/${$userId}",
  {
    "id": "$userId",
    "data": "$"
  }
]
```

### Literal Values

Use quotes for string literals:

```json
{
  "status": "'active'",     // String "active"
  "count": "100",           // Number 100
  "flag": "true"            // Boolean true
}
```

### Path Properties

Set nested properties or iterate arrays:

```json
{
  "$": "$",
  "user.name": "'John'",           // Set nested property
  "items[0]": "99",                // Set first array item
  "items[item]": "item.value * 2"  // Transform all items
}
```

### Special Functions

| Function | Description |
|----------|-------------|
| `transformMap(array, transform)` | Apply transform to each element |
| `expressionMap(array, expr)` | Map expression over array ($ = item) |
| `expressionFilter(array, expr)` | Filter array by expression |
| `expressionFind(array, expr)` | Find first matching element |
| `expressionSort(array, expr)` | Sort by expression value |
| `expressionGroup(array, expr)` | Group by expression value |
| `expressionReduce(array, init, expr)` | Reduce ($previous = accumulator) |
| `unique(array)` | Remove duplicates |
| `propsToList(obj, keyProp?)` | Convert object to array |
| `merge(obj1, obj2, ...)` | Merge objects |
| `pathPattern(pattern)` | Resolve path pattern |
| `path(jsonpath, obj)` | Query with JSON path |
| `newDate(...)` | Create Date object |
| `formatDate(date, format?)` | Format date string |
| `literal(obj)` | Pass object unchanged (no evaluation) |
| `parseInt(str)` | Parse integer |
| `parseFloat(str)` | Parse float |
| `uuid()` | Generate UUID |
| `canonicalise(str)` | Normalize string (lowercase, strip special chars) |
| `stripHtml(str)` | Remove HTML tags |

**Array function syntax:**
```json
{
  "$": [
    "expressionMap()",
    "items",
    "$ * 2"
  ]
}
```

## Conditionals

Execute steps conditionally:

```json
[
  "if (isJson) PUT /store/data",
  "if (!isJson) PUT /store/files"
]
```

### Conditional Variables

| Variable | Description |
|----------|-------------|
| `mime` | Content-Type |
| `isJson` | Body is JSON |
| `isText` | Body is text |
| `isBinary` | Body is binary |
| `status` | HTTP status code |
| `ok` | Status is success (0 or 200) |
| `method` | Original request method |
| `subpath` | Service subpath as array |
| `isDirectory` | URL ends with `/` |
| `header(key)` | Get header value |
| `body()` | JSON body (if not stream) |
| `query()` | Query parameters object |

**Examples:**
```json
"if (method === 'PUT') /transform-data"
"if (status === 404) GET /fallback"
"if (body().type === 'admin') /admin-handler"
```

## Parallelism

### Splitters and Joiners

| Splitter | Joiner | Description |
|----------|--------|-------------|
| `jsonSplit` | `jsonObject` | Split JSON array/object, join to object |
| `unzip` | `zip` | Split/join zip files |

**Example - process list in parallel:**
```json
[
  "jsonSplit",
  "GET /process/${}",
  "jsonObject"
]
```

Input `["a", "b", "c"]` → parallel GETs → output `{ "0": ..., "1": ..., "2": ..., length: 3 }`

### URL Expansion

Arrays in `${}` create parallel requests:

```json
[
  "GET /data/items",
  "GET /process/${[]}"
]
```

If `/data/items` returns `["x", "y"]`, expands to parallel GETs to `/process/x` and `/process/y`.

## Subpipelines

Nested arrays run in parallel by default:

```json
[
  [
    "GET /data/item1 :item1",
    "GET /data/item2 :item2"
  ],
  "jsonObject"
]
```

Both GETs run simultaneously, then join.

## Message Names

Name results for joining with `:name`:

```json
[
  [
    "GET /users :users",
    "GET /config :config"
  ],
  "jsonObject"
]
```

Output: `{ "users": {...}, "config": {...} }`

**Path pattern names:**
```json
"GET /data/$* :$*"   // Name = service path
```

## Pipeline Modes

Control execution flow with directives:

| Mode | Behavior |
|------|----------|
| `serial` | Execute sequentially (default for main) |
| `parallel` | Execute all simultaneously (default for subpipelines) |
| `tee` | Return original input, continue pipeline in background |
| `teeWait` | Same as tee but wait for completion |

**Mode modifiers:**
| Modifier | Meaning |
|----------|---------|
| `next` | On condition fail, skip to next step |
| `end` | On condition fail, skip to end |

**Example - copy to backup:**
```json
[
  "tee",
  "PUT /backup/$*"
]
```

**Example - try/catch pattern:**
```json
[
  "try GET /data/item",
  "if (status === 404) GET /fallback"
]
```

## Complete Examples

### Fetch and Transform

```json
[
  "GET /api/users",
  {
    "users": [
      "transformMap()",
      "$",
      { "name": "firstName + ' ' + lastName" }
    ]
  }
]
```

### Parallel Fetch and Merge

```json
[
  [
    "GET /data/profile :profile",
    "GET /data/settings :settings"
  ],
  "jsonObject",
  {
    "$": "merge(profile, settings)"
  }
]
```

### Conditional Processing

```json
[
  "serial next end",
  "if (method === 'POST') /validate",
  "if (!ok) /error-handler",
  "/save"
]
```

### Variable Capture

```json
[
  {
    "$id": "pathPattern('$<0')"
  },
  "GET /users/${$id}",
  {
    "userId": "$id",
    "userData": "$"
  }
]
```

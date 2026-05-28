---
name: scl-expressions
description: Comprehensive guide to SCL's dynamic expression language ($var, $jq, pipelines).
---
# SCL Expressions Skill

## 1. The Expression Syntax
SCL allows dynamic values using backtick expressions: `` `...` ``.
Inside backticks, you can call functions and pipe data.

**Canonical Example:**
```scl
# Get ID from variable 'meta', filter with jq, and extract ID
table_id `$var('meta') |> $jq('.tables[] | select(.name == "user") | .id')`
```

## 2. Variables (`var`)
Variables define reusable data blocks. They are commonly used to store GraphQL query results for use in subsequent `set` blocks.

**Syntax:**
```scl
var my_variable_name {
  # A. GraphQL Query
  query ```
  query {
    tables: dev_simple_system__tables { id name }
  }
  ```

  # B. Static JSON
  value ```
  {
    "api_key": "12345",
    "retries": 3
  }
  ```
}
```

## 3. Function Reference

### `$var(name)`
*   **Purpose:** Retrieves the value of a named variable defined earlier in the file.
*   **Returns:** JSON Object (result of query) or Value.
*   **Example:** `$var('metadata')`

### `$jq(filter)`
*   **Purpose:** Transforms JSON input using a [jq](https://jqlang.github.io/jq/) filter string.
*   **Common Patterns:**
    *   `.field`: Access property.
    *   `.[]`: Iterate array.
    *   `select(.x == "y")`: Filter array items.
    *   `map(.id)`: Transform array.
    *   `.users[0].id`: Deep access.
*   **Example:** `$jq('.tables[] | select(.name == "order") | .id')`

### `$json()`
*   **Purpose:** Parses a string into a JSON object. Useful when setting configuration fields that expect `:json` type.
*   **Example:**
    ```scl
    operations `["insert", "update"] |> $json()`
    ```

### `$file(path)`
*   **Purpose:** Reads the contents of a file relative to the app root.
*   **Common Use:** Loading scripts for Record Behaviors.
*   **Example:** `$file('scripts/record-behaviors/user.js')`

### `$env(key)`
*   **Purpose:** Accessing environment variables (e.g., API Keys).
*   **Example:** `$env('STRIPE_SECRET_KEY')`

### `$encode_image(path)`
*   **Purpose:** Loads an image file as a Base64 Data URI.
*   **Example:** `$encode_image('assets/logo.png')`

## 4. Common Patterns

### Pattern A: Dynamic ID Lookup
When creating `metadata`, `logic`, or `binding` records, you need the UUIDs of tables/fields.

```scl
# 1. Fetch Metadata
var meta {
  query ```
  query {
    tables: dev_simple_system__tables(where: { application_id: {_eq: "com.acme.app"} }) {
      id name
    }
  }
  ```
}

# 2. Use ID
set dev_simple_system.record_behavior, user_behavior {
  # dynamic lookup
  table_id `$var('meta') |> $jq('.tables[] | select(.name == "user") | .id')`
}
```

### Pattern B: Injection
Injecting configuration into a JSON field.

```scl
var config {
  value `{ "theme": "dark", "notifications": true }`
}

set dev_simple_system.setting, app_config {
  value `$var('config') |> $json()`
}
```

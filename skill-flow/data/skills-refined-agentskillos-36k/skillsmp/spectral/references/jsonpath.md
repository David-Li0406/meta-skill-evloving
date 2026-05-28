# JSONPath Expressions in Spectral

## Basic Syntax

| Expression | Description |
|------------|-------------|
| `$` | Root object |
| `.property` | Child property |
| `[*]` | All elements |
| `..` | Recursive descent |
| `~` | Property name (key) |

## Common Patterns

### Root Level

```yaml
given: $            # Entire document
given: $.info       # info object
given: $.paths      # paths object
```

### All Properties

```yaml
given: $.paths[*]                    # All path items
given: $.paths[*][*]                 # All operations
given: $.components.schemas[*]       # All schemas
```

### Specific Methods

```yaml
given: $.paths[*].get                # All GET operations
given: $.paths[*][get,post,put]      # Multiple methods
```

### Nested Access

```yaml
given: $.paths[*][*].parameters[*]   # All parameters
given: $.paths[*][*].responses[*]    # All responses
given: $.components.schemas[*].properties[*]  # All properties
```

### Property Names (Keys)

```yaml
given: $.paths[*]~                   # Path names (e.g., "/users")
given: $.components.schemas[*]~      # Schema names
given: $.paths[*][*].responses[*]~   # Status codes
```

### Recursive Descent

```yaml
given: $..description                # All descriptions anywhere
given: $..example                    # All examples anywhere
given: $..$ref                       # All $ref anywhere
```

## OpenAPI-Specific Patterns

### Operations

```yaml
# All operations
given: $.paths[*][get,post,put,patch,delete,options,head,trace]

# Operations with specific property
given: $.paths[*][*][?(@.operationId)]
```

### Parameters

```yaml
# Path-level parameters
given: $.paths[*].parameters[*]

# Operation-level parameters
given: $.paths[*][*].parameters[*]

# All parameters
given: $..parameters[*]
```

### Schemas

```yaml
# Component schemas
given: $.components.schemas[*]

# Inline request body schemas
given: $.paths[*][*].requestBody.content[*].schema

# Response schemas
given: $.paths[*][*].responses[*].content[*].schema

# All schemas anywhere
given: $..schema
```

### Security

```yaml
given: $.security[*]
given: $.paths[*][*].security[*]
given: $.components.securitySchemes[*]
```

## Filter Expressions

```yaml
# Properties with specific value
given: $.paths[*][?(@.deprecated == true)]

# Properties that exist
given: $.components.schemas[*][?(@.type)]

# Numeric comparisons
given: $.paths[*][*].responses[?(@property >= 400)]
```

## Combining with Field

```yaml
rules:
  must-have-summary:
    given: $.paths[*][get,post,put,patch,delete]
    then:
      field: summary      # Check 'summary' on matched objects
      function: truthy
```

## Examples by Use Case

### Check all descriptions exist

```yaml
given: $.paths[*][*]
then:
  field: description
  function: truthy
```

### Validate all operationIds

```yaml
given: $.paths[*][*].operationId
then:
  function: pattern
  functionOptions:
    match: "^[a-z][a-zA-Z0-9]+$"
```

### Ensure no inline schemas

```yaml
given: $.paths[*][*].requestBody.content[*].schema
then:
  field: $ref
  function: truthy
```

### Check path naming

```yaml
given: $.paths[*]~
then:
  function: pattern
  functionOptions:
    match: "^/[a-z][a-z0-9-/{}]*$"
```

# JSON Schema Composition

## allOf - Must match ALL schemas

```json
{
  "allOf": [
    { "type": "object", "required": ["id"] },
    { "type": "object", "required": ["name"] }
  ]
}
```

Use case: Combining schemas, adding constraints to referenced types.

```json
{
  "allOf": [
    { "$ref": "#/$defs/BaseUser" },
    {
      "properties": {
        "role": { "const": "admin" }
      }
    }
  ]
}
```

## anyOf - Must match AT LEAST ONE schema

```json
{
  "anyOf": [
    { "type": "string", "maxLength": 5 },
    { "type": "number", "minimum": 0 }
  ]
}
```

Use case: Multiple valid formats, flexible input types.

## oneOf - Must match EXACTLY ONE schema

```json
{
  "oneOf": [
    { "type": "number", "multipleOf": 3 },
    { "type": "number", "multipleOf": 5 }
  ]
}
```

Use case: Discriminated unions, mutually exclusive options.

### Discriminated Union Pattern

```json
{
  "oneOf": [
    {
      "type": "object",
      "properties": {
        "type": { "const": "circle" },
        "radius": { "type": "number" }
      },
      "required": ["type", "radius"]
    },
    {
      "type": "object",
      "properties": {
        "type": { "const": "rectangle" },
        "width": { "type": "number" },
        "height": { "type": "number" }
      },
      "required": ["type", "width", "height"]
    }
  ]
}
```

## not - Must NOT match schema

```json
{
  "not": { "type": "string" }
}
```

Use case: Exclusion rules, validation negation.

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "not": {
    "required": ["password"]
  }
}
```

## if/then/else - Conditional Schemas

```json
{
  "if": {
    "properties": { "type": { "const": "business" } }
  },
  "then": {
    "required": ["taxId"]
  },
  "else": {
    "required": ["ssn"]
  }
}
```

### Multiple Conditions

```json
{
  "allOf": [
    {
      "if": { "properties": { "country": { "const": "US" } } },
      "then": { "properties": { "state": { "type": "string" } } }
    },
    {
      "if": { "properties": { "country": { "const": "CA" } } },
      "then": { "properties": { "province": { "type": "string" } } }
    }
  ]
}
```

## Combining Patterns

### Extending a Base Schema

```json
{
  "$defs": {
    "Base": {
      "type": "object",
      "properties": {
        "id": { "type": "string" }
      },
      "required": ["id"]
    }
  },
  "allOf": [
    { "$ref": "#/$defs/Base" }
  ],
  "properties": {
    "name": { "type": "string" }
  }
}
```

### Union with Common Properties

```json
{
  "type": "object",
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" }
  },
  "required": ["timestamp"],
  "oneOf": [
    { "$ref": "#/$defs/EventA" },
    { "$ref": "#/$defs/EventB" }
  ]
}
```

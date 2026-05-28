# JSON Schema Keywords Reference

## String Keywords

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100,
  "pattern": "^[A-Z][a-z]+$",
  "format": "email"
}
```

### String Formats

- `date-time` - ISO 8601 date-time
- `date` - ISO 8601 date
- `time` - ISO 8601 time
- `duration` - ISO 8601 duration
- `email` - Email address
- `idn-email` - Internationalized email
- `hostname` - Internet hostname
- `idn-hostname` - Internationalized hostname
- `ipv4` - IPv4 address
- `ipv6` - IPv6 address
- `uri` - URI
- `uri-reference` - URI reference
- `iri` - Internationalized URI
- `iri-reference` - Internationalized URI reference
- `uuid` - UUID
- `json-pointer` - JSON Pointer
- `relative-json-pointer` - Relative JSON Pointer
- `regex` - Regular expression

## Number Keywords

```json
{
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "exclusiveMinimum": 0,
  "exclusiveMaximum": 100,
  "multipleOf": 0.5
}
```

Note: `integer` type is numbers without decimal part.

## Array Keywords

```json
{
  "type": "array",
  "items": { "type": "string" },
  "minItems": 1,
  "maxItems": 10,
  "uniqueItems": true,
  "contains": { "type": "number" },
  "minContains": 1,
  "maxContains": 3
}
```

### Tuple Validation (2020-12)

```json
{
  "type": "array",
  "prefixItems": [
    { "type": "string" },
    { "type": "number" }
  ],
  "items": false
}
```

## Object Keywords

```json
{
  "type": "object",
  "properties": {
    "name": { "type": "string" }
  },
  "required": ["name"],
  "additionalProperties": false,
  "propertyNames": { "pattern": "^[a-z]+$" },
  "minProperties": 1,
  "maxProperties": 10
}
```

### Pattern Properties

```json
{
  "patternProperties": {
    "^x-": { "type": "string" }
  }
}
```

### Dependent Properties

```json
{
  "dependentRequired": {
    "credit_card": ["billing_address"]
  },
  "dependentSchemas": {
    "credit_card": {
      "properties": {
        "billing_address": { "type": "string" }
      }
    }
  }
}
```

## Generic Keywords

```json
{
  "type": ["string", "null"],
  "enum": ["a", "b", "c"],
  "const": "fixed-value",
  "default": "default-value"
}
```

## Annotations

```json
{
  "title": "User Schema",
  "description": "Schema for user objects",
  "examples": [{ "name": "John" }],
  "deprecated": true,
  "readOnly": true,
  "writeOnly": false
}
```

## References

```json
{
  "$ref": "#/$defs/Address",
  "$defs": {
    "Address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" }
      }
    }
  }
}
```

External reference: `{ "$ref": "other-schema.json#/$defs/Type" }`

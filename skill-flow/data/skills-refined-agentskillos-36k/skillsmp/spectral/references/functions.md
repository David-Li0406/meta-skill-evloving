# Spectral Built-in Functions

## truthy

Value must be truthy (not null, undefined, false, 0, "").

```yaml
rules:
  must-have-description:
    given: $.info
    then:
      field: description
      function: truthy
```

## falsy

Value must be falsy.

```yaml
rules:
  no-internal-flag:
    given: $.paths[*][*]
    then:
      field: x-internal
      function: falsy
```

## defined

Value must be defined (not undefined).

```yaml
rules:
  contact-required:
    given: $.info
    then:
      field: contact
      function: defined
```

## undefined

Value must NOT be defined.

```yaml
rules:
  no-deprecated-field:
    given: $.paths[*][*]
    then:
      field: x-deprecated
      function: undefined
```

## pattern

Value must match regex pattern.

```yaml
rules:
  operation-id-format:
    given: $.paths[*][*].operationId
    then:
      function: pattern
      functionOptions:
        match: "^[a-z][a-zA-Z0-9]+$"

  no-trailing-slash:
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        notMatch: "/$"
```

## length

String/array length constraints.

```yaml
rules:
  description-length:
    given: $.info.description
    then:
      function: length
      functionOptions:
        min: 10
        max: 500

  tags-count:
    given: $.tags
    then:
      function: length
      functionOptions:
        min: 1
```

## enumeration

Value must be in allowed list.

```yaml
rules:
  valid-http-methods:
    given: $.paths[*]~
    then:
      function: enumeration
      functionOptions:
        values:
          - get
          - post
          - put
          - patch
          - delete
```

## schema

Validate against JSON Schema.

```yaml
rules:
  info-structure:
    given: $.info
    then:
      function: schema
      functionOptions:
        schema:
          type: object
          required:
            - title
            - version
          properties:
            title:
              type: string
              minLength: 1
            version:
              type: string
              pattern: "^\\d+\\.\\d+\\.\\d+$"
```

## alphabetical

Keys must be in alphabetical order.

```yaml
rules:
  paths-alphabetical:
    given: $.paths
    then:
      function: alphabetical
      functionOptions:
        keyedBy: null  # Sort by key names
```

## casing

Value must follow specific casing.

```yaml
rules:
  property-camelCase:
    given: $.components.schemas[*].properties[*]~
    then:
      function: casing
      functionOptions:
        type: camel
```

Options: `flat`, `camel`, `pascal`, `kebab`, `cobol`, `snake`, `macro`

## xor

Exactly one of the properties must be present.

```yaml
rules:
  example-or-examples:
    given: $.components.schemas[*].properties[*]
    then:
      function: xor
      functionOptions:
        properties:
          - example
          - examples
```

## typedEnum

Enum values must match specified type.

```yaml
rules:
  string-enums:
    given: $.components.schemas[*].properties[*]
    then:
      function: typedEnum
      functionOptions:
        type: string
```

## unreferencedReusableObject

Find unreferenced definitions.

```yaml
rules:
  no-unused-schemas:
    given: $.components.schemas
    then:
      function: unreferencedReusableObject
      functionOptions:
        reusableObjectsLocation: "#/components/schemas"
```

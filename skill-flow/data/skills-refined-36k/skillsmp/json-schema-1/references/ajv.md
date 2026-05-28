# Ajv JSON Schema Validator

## Basic Setup

```typescript
import Ajv from 'ajv';
import addFormats from 'ajv-formats';

const ajv = new Ajv();
addFormats(ajv);  // Add format validators

const schema = {
  type: 'object',
  properties: {
    email: { type: 'string', format: 'email' }
  },
  required: ['email']
};

const validate = ajv.compile(schema);

if (validate(data)) {
  console.log('Valid!');
} else {
  console.log(validate.errors);
}
```

## Configuration Options

```typescript
const ajv = new Ajv({
  allErrors: true,        // Collect all errors (not just first)
  strict: true,           // Strict mode (recommended)
  strictSchema: true,     // Strict schema validation
  strictTypes: true,      // Strict type checking
  coerceTypes: true,      // Coerce types (e.g., string to number)
  removeAdditional: true, // Remove additional properties
  useDefaults: true,      // Apply default values
  verbose: true,          // Include schema in errors
});
```

## Error Handling

```typescript
const validate = ajv.compile(schema);

if (!validate(data)) {
  for (const err of validate.errors!) {
    console.log({
      path: err.instancePath,
      keyword: err.keyword,
      message: err.message,
      params: err.params
    });
  }
}
```

### Better Error Messages

```typescript
import Ajv from 'ajv';
import ajvErrors from 'ajv-errors';

const ajv = new Ajv({ allErrors: true });
ajvErrors(ajv);

const schema = {
  type: 'object',
  properties: {
    age: {
      type: 'integer',
      minimum: 0,
      errorMessage: 'Age must be a positive integer'
    }
  },
  errorMessage: {
    required: {
      age: 'Age is required'
    }
  }
};
```

## Adding Schemas

```typescript
// Add named schema
ajv.addSchema(addressSchema, 'address');

// Reference in other schemas
const schema = {
  properties: {
    home: { $ref: 'address' }
  }
};

// Add keyword
ajv.addKeyword({
  keyword: 'isEven',
  type: 'number',
  validate: (schema, data) => data % 2 === 0
});
```

## Async Validation

```typescript
const ajv = new Ajv();

ajv.addKeyword({
  keyword: 'uniqueEmail',
  async: true,
  validate: async (schema, email) => {
    const exists = await checkEmailExists(email);
    return !exists;
  }
});

const validate = ajv.compile(schema);
const valid = await validate(data);
```

## Formats (ajv-formats)

```typescript
import addFormats from 'ajv-formats';

addFormats(ajv);
// Adds: date, time, date-time, duration, uri, email,
//       hostname, ipv4, ipv6, uuid, json-pointer, regex
```

## Draft Support

```typescript
import Ajv2019 from 'ajv/dist/2019';
import Ajv2020 from 'ajv/dist/2020';

// For draft-2019-09
const ajv2019 = new Ajv2019();

// For draft-2020-12
const ajv2020 = new Ajv2020();
```

## TypeScript Integration

```typescript
import Ajv, { JSONSchemaType } from 'ajv';

interface User {
  name: string;
  age: number;
}

const schema: JSONSchemaType<User> = {
  type: 'object',
  properties: {
    name: { type: 'string' },
    age: { type: 'integer' }
  },
  required: ['name', 'age']
};

const validate = ajv.compile<User>(schema);

if (validate(data)) {
  // data is typed as User
  console.log(data.name);
}
```

## Standalone Validation

```typescript
import Ajv from 'ajv';
import standaloneCode from 'ajv/dist/standalone';

const ajv = new Ajv({ code: { source: true } });
const validate = ajv.compile(schema);
const code = standaloneCode(ajv, validate);

// Write to file for production use
fs.writeFileSync('validate.js', code);
```
